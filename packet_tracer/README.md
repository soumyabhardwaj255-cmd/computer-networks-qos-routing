# Packet Tracer demonstration — manual build required

For the complete 15–20 minute procedure, addressing, verification commands, screenshots and submission checklist, use [LAB_GUIDE.md](LAB_GUIDE.md). All four complete router command blocks are collected in [ALL_ROUTER_COMMANDS.md](ALL_ROUTER_COMMANDS.md).

This directory contains ready-to-paste IOS configurations, not a saved `.pkt`. No Packet Tracer execution or screenshot has been verified. Use Cisco 2911 routers (three GigabitEthernet ports), two PCs and automatic cable selection.

```text
             R2
           /    \
PC-A --- R1      R4 --- PC-B
           \    /
             R3
```

## Connections and addressing

| Endpoint A | IP A | Endpoint B | IP B | Mask |
|---|---|---|---|---|
| R1 G0/0 | 10.0.12.1 | R2 G0/0 | 10.0.12.2 | 255.255.255.252 |
| R1 G0/1 | 10.0.13.1 | R3 G0/0 | 10.0.13.2 | 255.255.255.252 |
| R2 G0/1 | 10.0.24.1 | R4 G0/0 | 10.0.24.2 | 255.255.255.252 |
| R3 G0/1 | 10.0.34.1 | R4 G0/1 | 10.0.34.2 | 255.255.255.252 |
| R1 G0/2 | 192.168.1.1 | PC-A FastEthernet0 | 192.168.1.10 | 255.255.255.0 |
| R4 G0/2 | 192.168.4.1 | PC-B FastEthernet0 | 192.168.4.10 | 255.255.255.0 |

PC-A gateway: 192.168.1.1. PC-B gateway: 192.168.4.1. Transit networks are /30 and have two usable host addresses. LANs are /24. All OSPF links are in area 0. The upper path has configured interface costs 10; the lower path costs 30, so the expected initial path is R1–R2–R4.

## Build and verify

1. Place and name the routers and PCs, then connect the ports exactly as listed.
2. Answer `no` to the initial router configuration dialog. Paste each corresponding `R1.txt`–`R4.txt` into its router CLI from user EXEC mode.
3. Set PC addresses, masks and gateways under Desktop → IP Configuration.
4. Wait for links and OSPF adjacencies. Run `show ip interface brief`, `show ip ospf neighbor`, and `show ip route` on the routers.
5. From PC-A run `ping 192.168.4.10` and `tracert 192.168.4.10`. The first ping can lose a packet while ARP resolves; repeat it.
6. Switch to Simulation mode, filter ARP and ICMP, add a Simple PDU from PC-A to PC-B, then use Capture/Forward. Inspect layer-3 source/destination and Echo Request/Reply.
7. On R1, run `configure terminal`, `interface GigabitEthernet0/0`, `shutdown`, `end`. Wait for OSPF convergence and repeat the ping/PDU. The expected alternate path is R1–R3–R4. Restore with `no shutdown` under that interface.
8. Optionally change R1 G0/0 OSPF cost to 100 to illustrate a manual metric change without a failed link. This is not automatic utilization-aware routing. Restore cost 10 afterward.
9. Save as `Assessment6_QoS_Demo.pkt`. Capture your own initial/alternate Simulation-mode screenshots and actual command outputs for submission.

If adjacency fails, check exact cables, addresses, interface names, masks and `no shutdown`. If using another router model, adapt interface names before pasting.

**Boundary:** Python runs the custom QoS algorithm and yields the quantitative comparisons. Packet Tracer runs ordinary OSPF and demonstrates multipath routing/failover. The custom Python weighted algorithm is not executing inside Packet Tracer, and failover is not proof of congestion-aware routing.
