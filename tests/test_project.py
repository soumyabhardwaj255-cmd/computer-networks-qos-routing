import json
import unittest
from pathlib import Path
import networkx as nx
from src.model import topology, route, path_cost, validate
from src.simulation import simulate

c = json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())

class RoutingTests(unittest.TestCase):
    def test_path_optimality_against_exhaustive_search(self):
        for level in c['conditions'].values():
            g = topology(c,level)
            for a,key in [('baseline','static_cost'),('proposed','qos_cost')]:
                p = route(g,'R1','R12',a)
                best = min(path_cost(g,p,key) for p in nx.all_simple_paths(g,'R1','R12'))
                self.assertAlmostEqual(path_cost(g,p,key),best)

    def test_dynamic_route_changes(self):
        low, high = [topology(c,c['conditions'][s]) for s in ['normal','high']]
        self.assertEqual(route(low,'R1','R12','baseline'),route(high,'R1','R12','baseline'))
        self.assertNotEqual(route(low,'R1','R12','proposed'),route(high,'R1','R12','proposed'))

    def test_reproducibility_and_accounting(self):
        g = topology(c,.7)
        p = route(g,'R1','R12','proposed')
        a = simulate(c,g,p,42)
        self.assertEqual(a,simulate(c,g,p,42))
        self.assertAlmostEqual(a['pdr_pct']+a['loss_pct'],100)
        self.assertLessEqual(a['throughput_mbps'],c['packets_per_second']*c['packet_bytes']*8/1e6)

    def test_lossless_hand_calculation(self):
        g=nx.Graph()
        g.add_edge('a','b',index=0,p=0,delay_ms=2,service_ms=1,queue_ms=0,qos_cost=.2,static_cost=1)
        r=simulate(c,g,['a','b'],4)
        self.assertEqual(r['delay_ms'],3)
        self.assertEqual(r['pdr_pct'],100)

    def test_invalid_weights(self):
        bad={**c,'weights':dict(delay=-1,loss=1,utilization=1,hops=0)}
        with self.assertRaises(AssertionError): validate(bad)

if __name__=='__main__': unittest.main()
