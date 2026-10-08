# Results summary

All values below are read from the existing saved CSV files. No new result values were substituted.

## A. Average across all three source-destination pairs

Pairs: R1-R12, R2-R12 and R1-R3, simulated separately. Thirty trials per pair, three conditions and two algorithms give 540 runs. First average the three pairs within a trial; then average across trials. Figures and CSVs report approximate 95% normal confidence intervals across trial means.

| Condition | Algorithm | Delay ms | Loss % | Goodput Mbps | PDR % | Hops | QoS cost | Static cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| normal | baseline | 4.8223 | 0.2278 | 0.2395 | 99.7722 | 2.3333 | 0.1711 | 2.3333 |
| normal | proposed | 4.8223 | 0.2278 | 0.2395 | 99.7722 | 2.3333 | 0.1711 | 2.3333 |
| moderate | baseline | 9.8057 | 6.8089 | 0.2237 | 93.1911 | 2.3333 | 0.7448 | 2.3333 |
| moderate | proposed | 8.5490 | 0.3267 | 0.2392 | 99.6733 | 3.3333 | 0.3114 | 3.3333 |
| high | baseline | 47.2155 | 21.3000 | 0.1889 | 78.7000 | 2.3333 | 2.0879 | 2.3333 |
| high | proposed | 8.5490 | 0.3267 | 0.2392 | 99.6733 | 3.3333 | 0.3114 | 3.3333 |

Static cost equals hops. QoS cost is the same normalized objective evaluated on both routes; neither cost is a physical unit. Goodput is delivered cohort payload per generation duration, not maximum link capacity. Delay includes only delivered packets.

### Observed differences
- normal: delay reduction 0.00%; loss difference +0.00 percentage points; hop difference +0.00.
- moderate: delay reduction 12.82%; loss difference -6.48 percentage points; hop difference +1.00.
- high: delay reduction 81.89%; loss difference -20.97 percentage points; hop difference +1.00.

## B. Separate congestion sweep: R1-R12 only

Thirty trials per algorithm at each utilization level: 420 additional runs aggregated into 14 CSV rows. This is not the three-pair average.

| Core utilization | Algorithm | Delay ms | Loss % | Goodput Mbps | PDR % | Hops | QoS cost |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0.1 | baseline | 6.1995 | 0.3000 | 0.2393 | 99.7000 | 3.0000 | 0.2199 |
| 0.1 | proposed | 6.1995 | 0.3000 | 0.2393 | 99.7000 | 3.0000 | 0.2199 |
| 0.3 | baseline | 7.1128 | 0.5467 | 0.2387 | 99.4533 | 3.0000 | 0.3664 |
| 0.3 | proposed | 7.1128 | 0.5467 | 0.2387 | 99.4533 | 3.0000 | 0.3664 |
| 0.5 | baseline | 8.7557 | 2.4000 | 0.2342 | 97.6000 | 3.0000 | 0.5753 |
| 0.5 | proposed | 10.2586 | 0.4233 | 0.2390 | 99.5767 | 4.0000 | 0.3736 |
| 0.65 | baseline | 11.2213 | 6.5533 | 0.2243 | 93.4467 | 3.0000 | 0.8354 |
| 0.65 | proposed | 10.2586 | 0.4233 | 0.2390 | 99.5767 | 4.0000 | 0.3736 |
| 0.8 | baseline | 17.3908 | 14.4800 | 0.2052 | 85.5200 | 3.0000 | 1.2943 |
| 0.8 | proposed | 10.2586 | 0.4233 | 0.2390 | 99.5767 | 4.0000 | 0.3736 |
| 0.9 | baseline | 31.8100 | 22.1000 | 0.1870 | 77.9000 | 3.0000 | 1.9123 |
| 0.9 | proposed | 10.2586 | 0.4233 | 0.2390 | 99.5767 | 4.0000 | 0.3736 |
| 0.95 | baseline | 60.6218 | 27.0867 | 0.1750 | 72.9133 | 3.0000 | 2.6844 |
| 0.95 | proposed | 10.2586 | 0.4233 | 0.2390 | 99.5767 | 4.0000 | 0.3736 |

At utilization 0.50, proposed delay is worse while loss is lower: the weighted objective trades latency for other metrics. Constant proposed values at higher utilization reflect unchanged bypass state and reused seeds.

## C. Dynamic route trace: R1-R12 only

Four state epochs with one seeded run per algorithm/epoch (8 runs). The packet cohort finishes in a frozen epoch state; queues do not carry over. This demonstrates route recomputation and recovery, not convergence timing.

| Epoch | Condition | Algorithm | Selected route |
|---:|---|---|---|
| 0 | normal | baseline | R1 > R2 > R3 > R12 |
| 0 | normal | proposed | R1 > R2 > R3 > R12 |
| 1 | moderate | baseline | R1 > R2 > R3 > R12 |
| 1 | moderate | proposed | R1 > R4 > R5 > R6 > R12 |
| 2 | high | baseline | R1 > R2 > R3 > R12 |
| 2 | high | proposed | R1 > R4 > R5 > R6 > R12 |
| 3 | normal | baseline | R1 > R2 > R3 > R12 |
| 3 | normal | proposed | R1 > R2 > R3 > R12 |

## Interpretation boundaries

These gains are specific to a synthetic congested primary corridor with available alternate capacity. PDR and loss are complements, and fixed-rate goodput is proportional to PDR. They are not independent proofs of improvement. Confidence intervals cover packet randomness, not model realism or weight uncertainty. Packet Tracer measurements are not included.

Sources: results/summary.csv, results/paired_differences.csv, results/congestion_sweep.csv and results/dynamic_routes.csv.
