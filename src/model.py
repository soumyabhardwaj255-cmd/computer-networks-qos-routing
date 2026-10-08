"""Exogenous link-state model; this is not a TCP or discrete-event simulator."""
import math
import networkx as nx


def validate(c):
    assert c['trials'] >= 2 and c['packets'] > 0
    assert c['packet_bytes'] > 0 and c['packets_per_second'] > 0
    assert set(c['weights']) == {'delay', 'loss', 'utilization', 'hops'}
    assert all(v >= 0 for v in c['weights'].values())
    assert math.isclose(sum(c['weights'].values()), 1)
    assert c['delay_reference_ms'] > 0 and 0 < c['loss_reference'] < 1
    assert 0 <= c['congestion_loss_factor'] < 1
    assert len(c['positions']) > 1
    for e in c['links']:
        assert e['bandwidth_mbps'] > 0 and e['delay_ms'] >= 0
        assert 0 <= e['loss'] < 1 and 0 <= e['utilization'] < 1
    assert all(0 <= x < 1 for x in c['conditions'].values())


def topology(c, congestion):
    g = nx.Graph()
    for index, e in enumerate(c['links']):
        # The core corridor carries changing external/background traffic.
        u = congestion if e['core'] else e['utilization']
        p = 1 - (1-e['loss']) * (1-c['congestion_loss_factor'] * u**4)
        service = c['packet_bytes'] * 8 / (e['bandwidth_mbps'] * 1000)
        # Analytical queue approximation: E[Wq] = service*u/(1-u).
        queue = service * u / (1-u)
        delay = e['delay_ms'] + service + queue
        w = c['weights']
        cost = (w['delay'] * min(delay/c['delay_reference_ms'], 1)
                + w['loss'] * min(-math.log1p(-p)/-math.log1p(-c['loss_reference']), 1)
                + w['utilization'] * u + w['hops']/(len(c['positions'])-1))
        g.add_edge(e['a'], e['b'], **{**e, 'index': index, 'u': u, 'p': p,
                   'service_ms': service, 'queue_ms': queue, 'mean_ms': delay,
                   'qos_cost': cost, 'static_cost': 1})
    assert nx.is_connected(g)
    return g


def route(g, source, destination, algorithm):
    return nx.dijkstra_path(g, source, destination,
                            weight='static_cost' if algorithm == 'baseline' else 'qos_cost')


def path_cost(g, path, key):
    return sum(g[a][b][key] for a, b in zip(path, path[1:]))
