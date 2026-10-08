# Viva and five-minute demonstration

## 30-second explanation

“My project compares hop-count Dijkstra with a QoS-aware weighted Dijkstra heuristic. It uses delay, loss, utilization and hop penalties to choose a path on a 12-router synthetic network. Under high congestion, it chooses a longer bypass and reduces average delay and loss, while normal results stay unchanged. Python produces the measurements; a separate Packet Tracer topology demonstrates ordinary OSPF routing and failover.”

## 1-minute explanation

“A shortest path by hop count can still perform badly if its links are congested. I modeled 12 routers with several possible routes and configurable bandwidth, delay, loss and utilization. The baseline minimizes hops. My proposed method normalizes four metrics, combines them with weights and uses Dijkstra to minimize that cost. I ran three congestion conditions, three source–destination pairs and 30 seeded trials per pair: 540 algorithm runs. At high congestion, mean delay falls from 47.22 to 8.55 milliseconds and loss from 21.30% to 0.33%, with one extra hop on average. These are synthetic-model results, not measurements from physical routers. The method is inspired by RFC 2676; it is not a new protocol or a guarantee of QoS. Packet Tracer separately demonstrates IPv4, ICMP and conventional OSPF.”

## 3-minute explanation

“The problem is that a route can be short but congested. My aim is to show an understandable trade-off between hop count and performance rather than claim one method always wins.

“The network has 12 routers and multiple corridors. The short core corridor has 10 Mbps links; alternate links have 20 Mbps capacity but greater propagation and processing delay. Core utilization changes between normal, moderate and high settings. The model estimates queue delay from utilization and uses a stated synthetic loss curve. It samples packet drops and waiting times; it does not simulate actual router queues or TCP.

“For the baseline I assign every link cost one and run Dijkstra. For the proposed method I normalize estimated delay, negative-log loss and utilization, and add a normalized hop penalty. The weights are 0.4, 0.3, 0.2 and 0.1 respectively. They are configurable preferences, not learned values. Nonnegative additive weights let Dijkstra find the lowest-cost path efficiently. Routes are recomputed at state changes.

“I generate one thousand packets of twelve hundred bytes per run, at twenty-five packets per second. I repeat thirty seeds for three separate pairs under three conditions, comparing both algorithms. Shared packet/link random values make the comparisons paired. I average pairs within a trial and then compute means and approximate confidence intervals across trials.

“Normal routes and results are identical. High-congestion mean delay changes from 47.22 to 8.55 milliseconds; loss changes from 21.30 to 0.33 percent. Average hops increase by one. The separate R1-to-R12 sweep is not the same as the three-pair summary: at utilization 0.5, the weighted method actually has greater delay but lower loss. This shows why the result is a trade-off. Goodput is delivered payload divided by the generation interval, not maximum capacity; it follows delivery ratio under fixed offered traffic.

“RFC 2676 supports the resource-aware routing framework. Wang and Crowcroft explains why combining metrics does not guarantee all QoS constraints. I do not reproduce either source's complete algorithm. My main limitations are synthetic congestion, ideal current link state, no traffic feedback, no routing overhead and no TCP. Future work would add real queues, competing flows and stale measurements.

“Finally, Packet Tracer uses four routers and two PCs with conventional OSPF. It demonstrates route changes after a manual cost change or link failure. The custom algorithm and all quantitative results remain in Python.”

## Five-minute demonstration sequence

1. State the objective: avoid a congested short path when a healthier alternate route exists.
2. Open `figures/topology.png` and explain the central corridor and bypasses.
3. Show `config.json`: link bandwidth, delay, base loss, utilization, weights and seeds.
4. Run `.venv/Scripts/python.exe run.py`; show numerical results and the saved CSV.
5. Show `figures/selected_routes.png` and `results/dynamic_routes.csv` to demonstrate adaptation and recovery.
6. Explain delay/loss gains together with extra hops. Show confidence intervals and discuss the synthetic model.
7. Run the separately prepared Packet Tracer topology, ping and Simulation-mode path if you have completed the manual build.

## Questions to be ready for

- **Why Dijkstra?** The cost is additive and nonnegative; it finds the minimum scalar-cost path efficiently.
- **Why normalize?** Milliseconds, probabilities and hops have different scales. Fixed reference scales prevent units from accidentally determining importance.
- **Why negative log loss?** Link success probabilities multiply; their negative logarithms add. Clipping then makes it an approximate normalized penalty.
- **Why might hops rise?** A longer bypass can have smaller congestion delay and lower drops.
- **Is this new?** No. It is a small educational adaptation of established QoS routing ideas, primarily RFC 2676.
- **Do weights guarantee QoS?** No. They express preferences; they do not enforce separate constraints.
- **Where does congestion come from?** It is an externally configured utilization input affecting an analytical wait model and declared synthetic drop curve.
- **Does routing relieve modeled congestion?** No. Probe traffic does not update utilization. A traffic-feedback simulator is future work.
- **Is it deterministic?** Runs are reproducible with fixed seeds/configuration, while individual packet outcomes are stochastic.
- **Why multiple trials?** Packet losses and waits vary randomly. Trial intervals show sampling uncertainty.
- **Why paired trials?** Shared packet/link random numbers reduce noise in the algorithm comparison.
- **Why is throughput small?** Offered traffic is only 0.24 Mbps. Reported cohort goodput is not maximum network capacity.
- **Is PDR independent of loss?** No; PDR% = 100 − loss%.
- **Does normal congestion improve?** Read the actual results. Equal routes give exactly equal outcomes under paired randomness.
- **Is TCP implemented?** No. Packets are UDP-like without retransmissions; TCP changes offered load through congestion control.
- **Link-state versus distance-vector?** Link-state shares a network view and supports Dijkstra; distance-vector exchanges distance estimates with neighbors, often using Bellman–Ford-style updates.
- **What does Packet Tracer prove?** Addressing, routing and ICMP packet paths. It does not validate the custom Python algorithm.
- **What about layer boundaries?** Routing is layer 3; UDP/TCP are layer 4; transmission rate and per-link handling influence link delay. ICMP is carried by IP.
- **What is not modeled?** ARQ, CRC/checksum errors, TCP flow control, buffering, convergence, signaling overhead and real packet headers.

## Explain the algorithm at the whiteboard

1. Represent each router as a vertex and each link as an edge.
2. Read a current link-state snapshot. For a packet of L bits on bandwidth B, calculate service time L/B. Add propagation/processing delay and the modeled mean wait.
3. Calculate effective drop probability from base loss and external utilization.
4. Normalize delay and log-loss against fixed reference scales; keep utilization in [0,1), and assign 1/(N−1) per edge for hops.
5. Sum the four weighted terms to obtain a nonnegative link cost.
6. Dijkstra initializes source distance to zero and others to infinity, repeatedly selects the smallest tentative distance and relaxes neighboring edges. Predecessors reconstruct the selected route.
7. Sample packet outcomes on each algorithm's path with paired seeds. Count deliveries and delays; export measurements.
8. When the state changes, repeat path computation. This implementation has no route hysteresis or convergence-delay model.

## More likely faculty questions

| Question | Accurate answer |
|---|---|
| Why these QoS metrics? | Delay measures latency, loss measures reliability, utilization signals load, and hops penalize long routes. Bandwidth also affects transmission and queue-delay estimates. |
| Why a weighted sum? | It is configurable, easy to explain and compatible with ordinary shortest-path computation. It expresses preferences, not hard constraints. |
| Why these particular weights? | They are a declared teaching configuration prioritizing delay and loss. They were not learned or proven optimal. Sensitivity analysis is future work. |
| Why a hop-count baseline? | It is a simple, transparent control that ignores changing QoS. The result is only a comparison against this baseline, not every routing protocol. |
| Why synthetic simulation? | It provides controlled repeatable conditions with little setup and makes algorithm effects visible. It sacrifices fidelity, so the conclusions remain model-specific. |
| What does Dijkstra optimize? | The supplied scalar path cost. Minimizing the QoS cost is not the same as minimizing measured delay alone. |
| Why not Bellman–Ford? | There are no negative edge costs; Dijkstra is suitable and efficient. Bellman–Ford could solve a similar scalar problem but is not needed here. |
| Why not machine learning? | The link attributes and objective are explicit; a deterministic routing rule is sufficient and easier to explain. |
| What is the complexity? | Edge-cost construction O(E); typical heap Dijkstra O((V+E) log V), with O(V+E) graph/search storage. Packet simulation is O(PH), where P is packets and H is path hops. |
| Are metrics normalized over the current graph? | No. Fixed scales of 20 ms and loss reference 0.10 keep state comparisons consistent. Terms above the reference clip at one. |
| Are normalized path costs limited to one? | No. Individual edge components are bounded; the path sums edge costs. |
| Can clipping be harmful? | Yes. Two very bad links may receive the same clipped penalty. Reference-scale sensitivity is future work. |
| Are delay and utilization independent? | No. Utilization already affects modeled queue delay; its separate weight reinforces congestion preference and must not be interpreted as independent evidence. |
| Why do results improve under congestion? | Core link wait and loss rise while bypass links remain lightly loaded. The heuristic selects those bypasses. If all paths congest, improvement is not guaranteed. |
| Does the model measure utilization from packets? | No. Utilization is supplied externally; it is an ideal state input, not inferred telemetry. |
| Can routing itself reduce congestion here? | The probe path changes, but external utilization stays fixed. Modeling load feedback requires additional queues/traffic interaction. |
| Is the waiting-time model exactly M/M/1? | No. The mean expression resembles a simple queue approximation; exponential sampled waiting is a modeling choice, not an exact M/M/1 waiting distribution. |
| Is the loss curve from the literature? | No. It is a disclosed synthetic law with configurable coefficient, used consistently for both algorithms. |
| Are the three pairs simultaneous? | No, each is a separate experiment. Competing flows and fairness are outside the current scope. |
| Why are moderate and high proposed results identical? | The same bypass is selected, bypass attributes remain constant, and the same paired seeds are reused. |
| What does 540 mean? | 3 conditions × 3 pairs × 30 trials × 2 algorithms. The sweep and dynamic trace are additional experiments. |
| What are the sweep and dynamic scopes? | Both use R1–R12 only. The sweep averages 30 trials at each of seven utilization levels. The dynamic trace has one seeded run per algorithm per epoch. |
| Why is high sweep delay not 47.22 ms? | 47.22 ms averages all three pairs. The first-pair sweep has a different scope; its baseline high delay is 60.62 ms. |
| Is there a case with worse proposed delay? | Yes. At sweep utilization 0.50, baseline delay is 8.76 ms and proposed 10.26 ms, but proposed loss is lower. |
| What do the confidence intervals mean? | Approximate uncertainty in the mean due to sampled packet outcomes across 30 trial means; they exclude uncertainty in topology, weights and modeling assumptions. |
| Why not count every packet as an independent trial? | Results are computed within runs; the reported uncertainty is across repeated trial means, preserving the experiment's grouping. |
| Are you claiming statistical significance everywhere? | No. Paired-difference intervals are supplied for interpretation. They are normal approximations under a fixed model, not universal validation. |
| Is zero CI on hops wrong? | No. Routes are deterministic for a given state; packet randomness does not change their hop counts. |
| How is delay calculated when packets drop? | Only delivered packets contribute to mean delay. This is conditional on delivery and can introduce survivorship bias. |
| What if no packets arrive? | Delay is NaN. Default submitted runs all have deliveries. A general all-loss plotting workflow is not claimed. |
| Can I compare baseline static cost to proposed QoS cost? | No, those have different meanings. Both paths are evaluated under both costs in the CSV. |
| Does OSPF use current packet loss by default? | Not in this demonstration. We explicitly set interface costs and demonstrate topology/cost changes. |
| Why might request and reply paths differ? | OSPF costs are outgoing/directional. Changing only R1's cost can leave R4's return route unchanged. |
| What does [110/30] mean? | OSPF administrative distance 110 and accumulated path cost 30. It is not delay or hop count. |
| Why /30 transit links? | Each needs two usable IPv4 addresses; /30 supplies those plus network and broadcast addresses. |
| What does the default gateway do? | It is the PC's local router for reaching remote subnets; routers themselves use routing tables. |
| What changes at a router hop? | The layer-2 encapsulation changes and IPv4 TTL decreases; end-host source/destination IP addresses normally remain unchanged without NAT. |
| Why is the first ping sometimes lost? | ARP resolution or routing convergence can delay initial reachability; repeat after checking convergence. |
| Does failure recovery prove QoS improvement? | No. It demonstrates alternate-route reachability. Quantitative QoS gains come only from the Python experiments. |
| Is this novel research? | No. It is an educational implementation inspired by established QoS routing with explicitly limited claims. |

## Limitations and future work to remember

Current limitations: synthetic topology and loss law; externally fixed load; approximate queue waits; ideal current link state; no distributed routing exchange, TCP, finite buffers, concurrent flows or overhead. All results apply to this workload and chosen weights.

Future work: finite-buffer discrete-event simulation, simultaneous traffic, measured telemetry, delayed updates, route hysteresis, more topologies, weight sensitivity, control-plane cost, fairness and TCP experiments. None should be described as already implemented.

## Faculty follow-up: show the evidence

Point to `results/trials.csv` for per-run seeds/routes, `summary.csv` for aggregate values and intervals, `paired_differences.csv` for paired comparisons, and `audit/` for the clean-environment reproduction logs. Use `docs/RESULTS_SUMMARY.md` to avoid mixing pair-average and first-pair results. The final audit reruns an isolated copy; do not edit the submitted experiment just to show a different result.

Before submitting, insert your name, registration number and faculty details where required by your course, and add only real Packet Tracer evidence after completing its manual demonstration.
