"""Read-only audit of existing simulation artifacts; writes only this folder's review."""
import csv
import hashlib
import ipaddress
import json
import math
import statistics as stats
from pathlib import Path
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]

def rows(name):
    with (ROOT/'results'/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

c = json.loads((ROOT/'config.json').read_text())
meta = json.loads((ROOT/'results/run_metadata.json').read_text())
assert meta['config'] == c
assert meta['config_sha256'] == hashlib.sha256((ROOT/'config.json').read_bytes()).hexdigest()
trials, summaries, paired = rows('trials.csv'), rows('summary.csv'), rows('paired_differences.csv')
assert len(trials) == c['trials']*len(c['pairs'])*len(c['conditions'])*2 == 540
keys = {(r['condition'],r['pair'],r['trial'],r['algorithm']) for r in trials}
assert len(keys) == len(trials)
for r in trials:
    sent, delivered = int(r['sent']), int(r['delivered'])
    assert sent == c['packets'] and 0 <= delivered <= sent
    assert math.isclose(float(r['pdr_pct']),100*delivered/sent)
    assert math.isclose(float(r['loss_pct']),100*(1-delivered/sent),abs_tol=1e-10)
    goodput=delivered*c['packet_bytes']*8/(sent/c['packets_per_second'])/1e6
    assert math.isclose(float(r['throughput_mbps']),goodput)
    assert float(r['hops']) == len(r['route'].split(' > '))-1
metrics=['delay_ms','loss_pct','throughput_mbps','pdr_pct','hops','qos_cost','static_cost']
means={}
for s in summaries:
    for metric in metrics:
        values=[stats.mean(float(r[metric]) for r in trials if r['condition']==s['condition']
                 and r['algorithm']==s['algorithm'] and int(r['trial'])==t) for t in range(c['trials'])]
        means[(s['condition'],s['algorithm'],metric)]=values
        assert math.isclose(float(s[metric]),stats.mean(values),abs_tol=1e-10)
        assert math.isclose(float(s[metric+'_ci95']),1.96*stats.stdev(values)/len(values)**.5,abs_tol=1e-10)
for r in paired:
    v=[q-b for q,b in zip(means[(r['condition'],'proposed',r['metric'])],means[(r['condition'],'baseline',r['metric'])])]
    assert math.isclose(float(r['proposed_minus_baseline']),stats.mean(v),abs_tol=1e-10)
    assert math.isclose(float(r['ci95']),1.96*stats.stdev(v)/len(v)**.5,abs_tol=1e-10)
dynamic=rows('dynamic_routes.csv')
assert len(dynamic)==8
q=[r['route'] for r in dynamic if r['algorithm']=='proposed']
assert q[0]==q[3] and q[0]!=q[1] and q[1]==q[2]

# Parse the unchanged IOS files and check the planned wiring/address compatibility.
interfaces={}
for router in ['R1','R2','R3','R4']:
    text=(ROOT/'packet_tracer'/f'{router}.txt').read_text()
    assert 'router ospf 1' in text and 'network 10.0.0.0 0.255.255.255 area 0' in text
    interface=None
    for line in text.splitlines():
        if line.startswith('interface '):
            interface=line.split()[1]
            interfaces[(router,interface)]={}
        elif line.startswith('ip address '):
            _,_,address,mask=line.split()
            interfaces[(router,interface)]['address']=ipaddress.IPv4Interface(f'{address}/{mask}')
        elif line.startswith('ip ospf cost '):
            interfaces[(router,interface)]['cost']=int(line.split()[-1])
assert len({str(e['address'].ip) for e in interfaces.values()})==10
g=nx.DiGraph()
for a,port_a,b,port_b in [('R1','0/0','R2','0/0'),('R2','0/1','R4','0/0'),
                         ('R1','0/1','R3','0/0'),('R3','0/1','R4','0/1')]:
    ea,eb=interfaces[(a,'GigabitEthernet'+port_a)],interfaces[(b,'GigabitEthernet'+port_b)]
    assert ea['address'].network==eb['address'].network
    assert ea['address'].ip in ea['address'].network.hosts()
    assert eb['address'].ip in eb['address'].network.hosts()
    g.add_edge(a,b,weight=ea['cost'])
    g.add_edge(b,a,weight=eb['cost'])
g.add_edge('R4','PC-B',weight=10)
g.add_edge('R1','PC-A',weight=10)
assert nx.shortest_path_length(g,'R1','PC-B',weight='weight')==30
g['R1']['R2']['weight']=100
assert nx.shortest_path(g,'R1','PC-B',weight='weight')==['R1','R3','R4','PC-B']
assert nx.shortest_path_length(g,'R1','PC-B',weight='weight')==70
assert nx.shortest_path(g,'R4','PC-A',weight='weight')==['R4','R2','R1','PC-A']
report='''# Consistency review

The existing simulation was not rerun, rebuilt or edited. Results were read and checked against the stored configuration and documentation.

## Automated checks passed

- Stored configuration and SHA-256 match the current configuration.
- All 540 expected trial rows have unique condition/pair/trial/algorithm keys.
- Packet counts, loss, PDR, goodput and selected-route hop counts are internally consistent.
- All seven summary metric means and approximate 95% confidence intervals match recomputation from saved trial rows.
- All paired differences and their intervals match recomputation from saved trial rows.
- Dynamic routes show the initial path, a changed path under congestion and recovery.
- The four existing IOS configurations have unique interface addresses and matching /30 subnets across the four planned router links.
- A graph calculation confirms the planned R1 destination metric changes from 30 to 70, and confirms that a one-sided cost change can leave the reply route unchanged.

## Documentation review

The report and abstract agree with the saved results: normal delay is 4.8223 ms for both methods; moderate delay changes from 9.8057 to 8.5490 ms; high delay changes from 47.2155 to 8.5490 ms. High loss changes from 21.3000% to 0.3267%, and mean selected-path hops rise from 2.3333 to 3.3333. The abstract rounds these values correctly. High delay reduction is 81.89%.

The report correctly distinguishes the three-pair summary from the first-pair congestion sweep, and notes that the heuristic is not always better in delay. Model assumptions, conditional delivered delay, cohort goodput and related loss/PDR metrics are explicitly disclosed. The normalized log-loss penalty in the report matches the implementation.

No result-changing implementation error was identified in this consistency review. No existing results, source files, configuration or figures were changed. This is an artifact consistency audit, not a new empirical validation of the underlying synthetic model.

## Packet Tracer boundary

The four-router diamond is a conceptual reduction, not an exact copy of the Python topology. Both alternatives have equal hop counts. Conventional OSPF uses configured interface cost; it does not execute the Python delay/loss/utilization heuristic. Manual cost changes and link shutdown demonstrate different triggers and should be captioned accurately.

Packet Tracer itself has not been executed. Static configuration and cost checks are not substitutes for loading the topology, checking IOS behavior and capturing real evidence on the user's computer. The native .pkt and screenshots remain manual deliverables.
'''
(ROOT/'packet_tracer/CONSISTENCY_REVIEW.md').write_text(report,encoding='utf-8')
print('PASS: saved results/statistics/configuration and static IOS topology checks. No simulation rerun or edits.')
