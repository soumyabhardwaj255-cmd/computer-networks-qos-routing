"""Run from any directory: python run.py [--config config.json]."""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
from statistics import mean, stdev
from datetime import datetime, timezone
from src.model import validate, topology, route
from src.simulation import simulate
from src.plots import plots

ROOT = Path(__file__).resolve().parent
METRICS = ['delay_ms', 'loss_pct', 'throughput_mbps', 'pdr_pct', 'hops', 'qos_cost', 'static_cost']


def save_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--config', type=Path, default=ROOT/'config.json')
    args = p.parse_args()
    c = json.loads(args.config.read_text())
    validate(c)
    out = ROOT/'results'
    out.mkdir(exist_ok=True)
    rows = []
    for condition, level in c['conditions'].items():
        g = topology(c, level)
        for pair_index, (s, d) in enumerate(c['pairs']):
            for trial in range(c['trials']):
                seed = c['seed'] + trial + pair_index*10000
                for algorithm in ['baseline', 'proposed']:
                    path = route(g, s, d, algorithm)
                    rows.append(dict(condition=condition, pair=f'{s}-{d}', trial=trial,
                                     seed=seed, algorithm=algorithm, route=' > '.join(path),
                                     **simulate(c, g, path, seed)))
    save_csv(out/'trials.csv', rows)
    summaries, paired = [], []
    for condition in c['conditions']:
        for algorithm in ['baseline', 'proposed']:
            # Average pairs within a seed before CI; do not treat packets as trials.
            trial_means = [{m: mean(r[m] for r in rows if r['condition']==condition
                           and r['algorithm']==algorithm and r['trial']==t) for m in METRICS}
                           for t in range(c['trials'])]
            summary = dict(condition=condition, algorithm=algorithm, trials=c['trials'])
            for m in METRICS:
                values = [r[m] for r in trial_means]
                summary[m] = mean(values)
                summary[m+'_ci95'] = 1.96*stdev(values)/len(values)**0.5
            summaries.append(summary)
        for m in METRICS:
            diffs = []
            for t in range(c['trials']):
                means = {a: mean(r[m] for r in rows if r['condition']==condition and
                         r['trial']==t and r['algorithm']==a) for a in ['baseline','proposed']}
                diffs.append(means['proposed']-means['baseline'])
            paired.append(dict(condition=condition, metric=m, proposed_minus_baseline=mean(diffs),
                               ci95=1.96*stdev(diffs)/len(diffs)**0.5))
    save_csv(out/'summary.csv', summaries)
    save_csv(out/'paired_differences.csv', paired)
    # Sequential state changes on the same topology; routes recomputed every epoch.
    dynamic = []
    for epoch, condition in enumerate(['normal','moderate','high','normal']):
        g = topology(c, c['conditions'][condition])
        for a in ['baseline','proposed']:
            path = route(g, *c['pairs'][0], a)
            dynamic.append(dict(epoch=epoch, condition=condition, algorithm=a,
                           route=' > '.join(path), **simulate(c,g,path,c['seed']+epoch)))
    save_csv(out/'dynamic_routes.csv', dynamic)
    sweep = []
    for level in [0.1,0.3,0.5,0.65,0.8,0.9,0.95]:
        g = topology(c,level)
        for a in ['baseline','proposed']:
            runs = [simulate(c,g,route(g,*c['pairs'][0],a),c['seed']+t) for t in range(c['trials'])]
            sweep.append(dict(utilization=level, algorithm=a, **{m:mean(r[m] for r in runs) for m in METRICS}))
    save_csv(out/'congestion_sweep.csv', sweep)
    plots(c, summaries, sweep, ROOT/'figures')
    text = ['# Executed results', '', f"Means over {len(c['pairs'])} independent pair experiments per trial; {c['trials']} trials.",
            'CI columns in CSV are approximate 95% normal confidence intervals across trial means.', '',
            '| Condition | Algorithm | Delay ms | Loss % | Goodput Mbps | PDR % | Hops | QoS cost |',
            '|---|---|---:|---:|---:|---:|---:|---:|']
    for r in summaries:
        text.append('| '+r['condition']+' | '+r['algorithm']+' | '+' | '.join(f'{r[m]:.4f}' for m in METRICS[:-1])+' |')
    text += ['', '## Interpretation']
    for condition in c['conditions']:
        b,q = [r for r in summaries if r['condition']==condition]
        text.append(f"- {condition}: delay reduction {100*(b['delay_ms']-q['delay_ms'])/b['delay_ms']:.2f}%; "
                    f"loss change {q['loss_pct']-b['loss_pct']:+.2f} percentage points; "
                    f"hop change {q['hops']-b['hops']:+.2f}.")
    text += ['', 'These results apply to the configured synthetic external congestion model, not a real network.',
             'Throughput is delivered cohort payload per offered-traffic duration, not maximum link capacity.',
             'PDR and loss are complements; goodput is proportional to PDR at fixed offered load.', '',
             '## Dynamic demonstration']
    text += [f"- Epoch {r['epoch']} {r['condition']} {r['algorithm']}: {r['route']}" for r in dynamic]
    report = '\n'.join(text)+'\n'
    (out/'FINAL_RESULTS.md').write_text(report, encoding='utf-8')
    (out/'run_metadata.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(), config=c, config_sha256=hashlib.sha256(args.config.read_bytes()).hexdigest()),indent=2))
    print(report)


if __name__ == '__main__':
    main()
