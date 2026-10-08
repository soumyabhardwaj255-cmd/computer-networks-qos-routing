"""Paired packet experiments with reproducible per-packet/per-link randomness."""
import random
import math
from .model import path_cost


def simulate(c, g, path, seed):
    delivered, total_delay = 0, 0.0
    edges = list(zip(path, path[1:]))
    for packet in range(c['packets']):
        delay, success = 0.0, True
        for a, b in edges:
            e = g[a][b]
            # Same variates for a shared link and packet in both algorithms.
            rng = random.Random(seed * 1000000007 + packet * len(c['links']) + e['index'])
            drop, waiting = rng.random(), rng.random()
            if drop < e['p']:
                success = False
                break
            delay += e['delay_ms'] + e['service_ms'] - e['queue_ms'] * math.log1p(-waiting)
        if success:
            delivered += 1
            total_delay += delay
    duration = c['packets']/c['packets_per_second']
    # Cohort goodput: all generated packets are followed through delivery/drop.
    return dict(sent=c['packets'], delivered=delivered,
                delay_ms=total_delay/delivered if delivered else float('nan'),
                loss_pct=100*(1-delivered/c['packets']),
                throughput_mbps=delivered*c['packet_bytes']*8/duration/1e6,
                pdr_pct=100*delivered/c['packets'], hops=len(path)-1,
                qos_cost=path_cost(g, path, 'qos_cost'),
                static_cost=path_cost(g, path, 'static_cost'))
