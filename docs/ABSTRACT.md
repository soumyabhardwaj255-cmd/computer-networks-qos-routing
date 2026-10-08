Title:
QoS-Aware Adaptive Routing for Improved Network Performance under Congestion

Abstract:
This project evaluates a QoS-aware weighted Dijkstra routing heuristic against hop-count shortest-path routing in a 12-router Python simulation. Configurable normalized delay, loss, utilization and hop penalties guide route selection as network conditions change. Experiments use three congestion levels, three source–destination pairs and 30 reproducible trials per pair. Under the configured high-congestion model, average delay decreases from 47.22 ms to 8.55 ms and packet loss from 21.30% to 0.33%, with one additional hop on average. Normal-condition performance is unchanged. Results demonstrate a congestion-avoidance trade-off within a synthetic link model, rather than guaranteed gains in real networks.

Existing Work:
Apostolopoulos et al., RFC 2676, “QoS Routing Mechanisms and OSPF Extensions” (1999), provides the primary resource-aware routing framework. Wang and Crowcroft, “Quality-of-Service Routing for Supporting Multimedia Applications” (1996), discusses multi-metric routing and the limitations of mixed metrics.

Gap Identified:
The selected static hop-count baseline does not consider changing link congestion or packet loss when choosing routes.

Work Proposed:
Implement a configurable normalized QoS cost with Dijkstra, recompute routes at network-state updates, and compare paired packet experiments against the static baseline.

Metrics to be Improved:
Average delivered-packet delay, packet loss, throughput and packet delivery ratio, while recording hop-count and path-cost trade-offs.

Final Output:
An executed Python simulation, CSV results, comparison graphs, dynamic route traces and project/viva documentation. A separate Packet Tracer build guide and router configurations support an IPv4/OSPF/ICMP demonstration; the native Packet Tracer file still requires manual construction and verification.
