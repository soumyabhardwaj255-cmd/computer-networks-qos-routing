# Packet Tracer manual lab guide

**Target: 15–20 minutes. Status: not executed in Packet Tracer.** No `.pkt` file or screenshots are fabricated. All expected routes below are calculated from the existing configurations, not captured outputs. Use this expanded guide with `ALL_ROUTER_COMMANDS.md`.

## 1. Exact topology and connections

Use **4 Cisco 2911 routers, 0 switches and 2 PC-PT PCs**. The 2911 has the three built-in GigabitEthernet ports required by the edge routers; no extra modules are needed. Use six Copper Cross-Over cables, selecting the exact ports below.

```text
                    R2
                   /  \
PC-A ----------- R1    R4 ----------- PC-B
                   \  /
                    R3
```

Preferred path: PC-A → R1 → R2 → R4 → PC-B.
Alternate path: PC-A → R1 → R3 → R4 → PC-B.

Both alternatives have equal router-hop counts. This simplified topology represents the Python project's multiple corridors conceptually; it does not reproduce its 12 routers or extra-hop trade-off. Labels are local to this topology, not a one-to-one mapping to the Python graph.

| Cable | Endpoint A | Endpoint B |
|---|---|---|
| 1 | PC-A FastEthernet0 | R1 GigabitEthernet0/2 |
| 2 | R1 GigabitEthernet0/0 | R2 GigabitEthernet0/0 |
| 3 | R2 GigabitEthernet0/1 | R4 GigabitEthernet0/0 |
| 4 | R1 GigabitEthernet0/1 | R3 GigabitEthernet0/0 |
| 5 | R3 GigabitEthernet0/1 | R4 GigabitEthernet0/1 |
| 6 | R4 GigabitEthernet0/2 | PC-B FastEthernet0 |

Automatic cable selection can work, but check that it selected these ports. Direct PC-router connections are sufficient; switches add no necessary function for two hosts.

## 2. Complete IPv4 addressing table

| Device | Interface | IP address | Subnet mask | Default gateway |
|---|---|---|---|---|
| PC-A | FastEthernet0 | 192.168.1.10 | 255.255.255.0 | 192.168.1.1 |
| R1 | GigabitEthernet0/2 | 192.168.1.1 | 255.255.255.0 | N/A |
| R1 | GigabitEthernet0/0 | 10.0.12.1 | 255.255.255.252 | N/A |
| R2 | GigabitEthernet0/0 | 10.0.12.2 | 255.255.255.252 | N/A |
| R2 | GigabitEthernet0/1 | 10.0.24.1 | 255.255.255.252 | N/A |
| R4 | GigabitEthernet0/0 | 10.0.24.2 | 255.255.255.252 | N/A |
| R1 | GigabitEthernet0/1 | 10.0.13.1 | 255.255.255.252 | N/A |
| R3 | GigabitEthernet0/0 | 10.0.13.2 | 255.255.255.252 | N/A |
| R3 | GigabitEthernet0/1 | 10.0.34.1 | 255.255.255.252 | N/A |
| R4 | GigabitEthernet0/1 | 10.0.34.2 | 255.255.255.252 | N/A |
| R4 | GigabitEthernet0/2 | 192.168.4.1 | 255.255.255.0 | N/A |
| PC-B | FastEthernet0 | 192.168.4.10 | 255.255.255.0 | 192.168.4.1 |

Routers use their routing tables and do not need `ip default-gateway`. R2/R3 G0/2 is unused and unconfigured. Transit networks are 10.0.12.0/30, 10.0.24.0/30, 10.0.13.0/30 and 10.0.34.0/30. Each has usable hosts .1 and .2; .0 is network and .3 is broadcast. LANs are 192.168.1.0/24 and 192.168.4.0/24. DNS is unnecessary for IP-only tests.

## 3. OSPF and the project boundary

Use OSPFv2 process 1, area 0. Upper-path interfaces have cost 10, lower-path interfaces cost 30, and destination LAN interfaces cost 10. Explicit interface costs use `ip ospf cost`. [Cisco IOS command reference](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/m_ospf-a1.html)

Calculated R1 route to 192.168.4.0/24:

| State | Selected routers | Next hop | R1 exit | Metric |
|---|---|---|---|---:|
| Normal | R1–R2–R4 | 10.0.12.2 | G0/0 | 10+10+10 = 30 |
| R1 G0/0 cost raised to 100 | R1–R3–R4 | 10.0.13.2 | G0/1 | 30+30+10 = 70 |
| R1 G0/0 shut down | R1–R3–R4 | 10.0.13.2 | G0/1 | 70 |
| Original state restored | R1–R2–R4 | 10.0.12.2 | G0/0 | 30 |

Expect the destination route marked `O`, with `[110/30]` initially and `[110/70]` after switching. These are expected fields, not captured output. 110 is administrative distance; the second value is path cost. The destination LAN contributes the final 10.

The existing broad `network` statements match interface addresses; they do not create a default route or advertise one /8 summary. Connected subnet masks remain /30 and /24. OSPF process IDs are locally significant; adjacent interfaces must agree on the area. Router IDs are selected automatically and need not equal neighbor link addresses.

**Viva statement:** “Python runs the custom normalized delay/loss/utilization/hop heuristic and produces the quantitative results. Packet Tracer runs conventional OSPF to demonstrate IPv4 routing, ICMP, metric changes and failover. It does not run my Python algorithm or automatically sense congestion.”

## 4. Manual build sequence

1. **Minutes 0–3:** Open a new Logical workspace. Add four 2911 routers under Network Devices → Routers and two PC-PTs under End Devices. Set Display Names to R1–R4, PC-A and PC-B under each device's Config tab. Arrange the diamond.
2. **Minutes 3–5:** Select Connections → Copper Cross-Over and cable the exact ports in section 1. Add subnet and cost text notes. Red router interfaces before configuration are normal.
3. **Minutes 5–10:** Open each router's CLI. Wait for boot, answer `no` to the initial setup dialog if offered, and press Enter to reach `Router>`. Paste its complete block from `ALL_ROUTER_COMMANDS.md` or the corresponding `R1.txt`–`R4.txt`. Do not paste prompt characters. These blocks assume fresh routers. Confirm `write memory` completes.
4. **Minutes 10–12:** On each PC, Desktop → IP Configuration → Static; enter its address, mask and gateway from section 2.
5. **Minutes 12–15:** Stay in Realtime while links/OSPF settle; allow roughly 30–60 seconds if necessary. Run section 5 commands. Initially each router should have two FULL router neighbors. FULL/DR or FULL/BDR is normal for Ethernet; PCs do not become neighbors.
6. **Minutes 15–18:** Capture initial evidence and one ICMP path. Return to Realtime and demonstrate either a manual metric change (section 6) or a link failure (section 7).
7. **Minutes 18–20:** Restore original costs and interface state, verify ping, run `write memory` on changed routers and File → Save As → `Assessment6_QoS_Demo.pkt`. Save the final file in the healthy state.

## 5. Exact verification commands

On **every router**, from privileged EXEC mode:

```text
enable
show ip interface brief
show running-config
show ip protocols
show ip ospf neighbor
show ip route
show ip route ospf
```

Connected interfaces should be up/up. Unused R2/R3 G0/2 may remain administratively down. In `show running-config`, find addresses, interface costs and `router ospf 1`; press Space to page through. `show ip protocols` confirms OSPF and networks. [Cisco OSPF verification command reference](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-s1.html)

On **R1**:

```text
show ip ospf interface GigabitEthernet0/0
show ip ospf interface GigabitEthernet0/1
show ip route 192.168.4.0
ping 10.0.12.2
ping 10.0.13.2
ping 192.168.4.10
traceroute 192.168.4.10
```

These check actual costs, selected route, immediate neighbors and the destination. IOS traceroute starts at R1 and excludes the PC-A-to-R1 hop.

On **PC-A → Desktop → Command Prompt**:

```text
ipconfig
ping 192.168.1.1
ping 192.168.4.10
tracert 192.168.4.10
```

On **PC-B → Desktop → Command Prompt**:

```text
ipconfig
ping 192.168.4.1
ping 192.168.1.10
tracert 192.168.1.10
```

Use `tracert` on PCs and `traceroute` on routers. First pings may lose packets during ARP resolution; repeat after convergence. PC-A's initial path should traverse R1, R2, R4, PC-B; alternate R1, R3, R4, PC-B. Match responding router IPs to the table; exact hop-reply source interfaces may vary. These are expectations to verify, not observed traces.

## 6. Manual metric-change demonstration

Keep all links up. On **R1**:

```text
enable
configure terminal
interface GigabitEthernet0/0
ip ospf cost 100
end
show ip ospf interface GigabitEthernet0/0
show ip route 192.168.4.0
```

Wait for the route update. Repeat PC-A's destination ping and tracert. Upper path cost is now 120; lower remains 70. Say: “I changed the metric manually; OSPF recalculated automatically.” This is not automatic congestion detection.

**Asymmetry:** R1's change affects the request path, but R4 can still send replies through R2. This is valid routing. To show both directions through R3, also change **R4**:

```text
enable
configure terminal
interface GigabitEthernet0/0
ip ospf cost 100
end
show ip route 192.168.1.0
```

After convergence both directions should favor R3. Restore **R1** and, if changed, **R4**, using this block on each:

```text
configure terminal
interface GigabitEthernet0/0
ip ospf cost 10
no shutdown
end
write memory
```

Recheck routes and ping. Changing the `bandwidth` command is not a substitute for generating actual traffic; this guide changes the OSPF cost explicitly.

## 7. Optional link-failure demonstration

Start with original costs restored. On **R1**:

```text
enable
configure terminal
interface GigabitEthernet0/0
shutdown
end
show ip interface brief
show ip ospf neighbor
show ip route 192.168.4.0
```

Wait for convergence, then repeat PC-A ping/tracert. R1 should have one FULL neighbor remaining; request and reply must bypass the failed R1–R2 link via R3. Temporary packet loss during convergence is possible. This is failure recovery, not congestion measurement.

Restore **R1**:

```text
configure terminal
interface GigabitEthernet0/0
no shutdown
ip ospf cost 10
end
write memory
```

Verify two FULL neighbors and route via R2 return. Save the `.pkt` in this restored state.

## 8. Simulation-mode ICMP

1. Get a successful Realtime ping first so ARP is usually resolved.
2. Switch to Simulation → Edit Filters; select ICMP and ARP and hide unrelated events. Hiding OSPF events does not disable OSPF.
3. Select Add Simple PDU (closed envelope), click PC-A, then PC-B.
4. Use Capture/Forward to follow the Echo Request through R1–R2–R4, then the Echo Reply. Capture the Event List's sequential device entries together with the topology; take multiple images if the whole sequence does not fit.
5. Click an ICMP event/envelope and inspect PDU Information → OSI Model / Inbound or Outbound PDU Details. Capture source 192.168.1.10, destination 192.168.4.10 and ICMP information where shown. Routed hops change Ethernet headers while end-host IP addresses remain the same.
6. Return to Realtime, apply the metric change or failure, and verify the changed route. Clear old user-created PDUs/events with the available delete/reset controls; do not reset router configurations.
7. Create a **new** Simple PDU in Simulation and capture request events through R1–R3–R4. With a one-sided cost change, label the potentially different reply path honestly; use the symmetrical change or shutdown for a simpler two-direction demonstration.

## 9. Exact screenshots to capture

These filenames are suggestions for your real captures, not files generated here.

| Suggested file | Capture | Evidence |
|---|---|---|
| 01_topology.png | Full Logical workspace, six labeled devices, subnet/cost notes, six healthy links | Complete topology |
| 02_pc_a_ip.png and 03_pc_b_ip.png | Each Desktop → IP Configuration with IP/mask/gateway | Host addressing |
| 04_R1_interfaces.png through 04_R4_interfaces.png | Each router's `show ip interface brief` | Router addresses and port status |
| 05_R1_ospf.png through 05_R4_ospf.png | Each `show running-config` page containing `router ospf 1` | Routing configuration |
| 06_R1_neighbors.png | Two FULL entries in `show ip ospf neighbor` | Adjacency |
| 07_route_initial.png | R1 route to 192.168.4.0, metric 30, next hop 10.0.12.2 | Preferred route |
| 08_ping_success.png | PC-A destination ping with successful replies after convergence | Connectivity |
| 09_trace_initial.png | PC-A tracert to PC-B | Initial route |
| 10_icmp_initial.png | Simulation topology and request Event List through R2 | ICMP packet path |
| 11_icmp_details.png | ICMP PDU details with end-host IPs | Layer-3/ICMP inspection |
| 12_change.png | R1 OSPF interface cost 100, or shutdown status if using failure | Applied change |
| 13_route_alternate.png | R1 route metric 70 via 10.0.13.2 | Recalculated route |
| 14_trace_alternate.png | PC-A tracert and successful ping after change | Alternate path reachability |
| 15_icmp_alternate.png | New ICMP request events through R3 | Alternate packet path |

Caption each state as normal, manual cost change, or link failure. A single moving envelope does not prove the complete route; include sequential events. Do not label manually changed cost as measured congestion.

## 10. Quick troubleshooting

- Administratively down: apply `no shutdown` on the correct interface.
- Down/down: check exact cable endpoints and device power.
- No FULL neighbors: check both transit addresses, /30 masks, area 0, OSPF network matches and active interfaces; wait in Realtime.
- PC cannot ping gateway: fix PC mask/gateway and G0/2 link before investigating OSPF.
- Gateway works but remote PC fails: check both remote-LAN routes, R4's LAN and PC-B's gateway.
- Wrong path: inspect actual R1 G0/0 cost and allow recalculation.
- Traceroute has `*`: verify ping, wait and retry; use routing tables and ICMP events as additional evidence. Never substitute invented output.
- Rejected commands: verify 2911 interface names and CLI mode. `show` commands run at `R1#`; enter `end` to leave configuration mode.

## 11. Final submission checklist

Follow any additional faculty-specific format; this list describes project completeness.

- [ ] Student name, registration number, course BCSE308P, faculty and assessment details.
- [ ] `docs/ABSTRACT.md` with the exact requested seven-part structure.
- [ ] `docs/REPORT.md` with literature, architecture, formulas, pseudocode, flowchart, methodology, limitations and future scope.
- [ ] Existing Python source, configuration, requirements and run instructions.
- [ ] Existing CSVs, metadata, actual execution/test logs and `results/FINAL_RESULTS.md`.
- [ ] All nine existing output figures.
- [ ] This Packet Tracer guide, `ALL_ROUTER_COMMANDS.md` and R1–R4 configuration files.
- [ ] Your manually created and tested `Assessment6_QoS_Demo.pkt`.
- [ ] Your genuine screenshots with captions from section 9.
- [ ] Clear distinction between Python quantitative QoS simulation and Packet Tracer conventional OSPF.
- [ ] Updated final submission archive after adding the `.pkt` and screenshots. The earlier project ZIP predates this expanded guide and cannot contain future lab evidence.

## 12. Before the demonstration

- [ ] Open the `.pkt` on the college computer and keep a backup.
- [ ] Begin with all links up, original costs restored and two FULL neighbors per router.
- [ ] Demonstrate ping, tracert and an initial ICMP request via R2.
- [ ] Apply a metric change or shutdown, verify route via R3 and repeat ping/ICMP.
- [ ] Restore the original state and show route recovery.
- [ ] Explain /30 vs /24, OSPF area/process, cost vs hop count and administrative distance 110.
- [ ] Explain that Python's normal results are unchanged and moderate/high congestion uses one extra hop on average.
- [ ] Explain delivered-only delay, cohort goodput, paired seeds and complementary loss/PDR.
- [ ] State that Packet Tracer is not running the custom algorithm or reproducing its quantitative gains.

Thirty-second explanation: “Four routers provide two IPv4 paths. OSPF chooses the lowest configured cost, initially through R2. Increasing the outgoing cost or disabling that link causes route recalculation through R3. This demonstrates metric-aware routing and failover. My separate Python experiment implements the QoS-aware heuristic and measures its performance trade-offs.”
