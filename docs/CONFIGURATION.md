# Configuration reference

`config.json` contains the submitted experiment. Do not edit it to reproduce the saved results. `run.py --config path/to/copy.json` loads another configuration but still writes outputs in the project containing `run.py`; use a separate project copy for exploratory changes.

| Field | Submitted value / units | Meaning |
|---|---|---|
| seed | 30806 | Base packet-randomness seed; trial and pair offsets are added |
| trials | 30 | Independent seeded trials per pair; integer at least 2 for intervals |
| packets | 1000 | Packets per algorithm run; positive integer |
| packet_bytes | 1200 bytes | Modeled payload size; no protocol-header accounting |
| packets_per_second | 25 packets/s | Offered probe rate, giving 0.24 Mbps and a 40 s cohort interval |
| delay_reference_ms | 20 ms | Fixed normalization scale; delay term clips at 1 |
| loss_reference | 0.10 probability | Reference for negative-log success normalization, in (0,1) |
| congestion_loss_factor | 0.12 | Synthetic extra-drop coefficient k, in [0,1) |
| weights.delay | 0.40 | Weight of normalized estimated delay |
| weights.loss | 0.30 | Weight of normalized log-loss penalty |
| weights.utilization | 0.20 | Weight of utilization |
| weights.hops | 0.10 | Weight of per-edge 1/(N−1) hop penalty |
| conditions.normal | 0.10 | External utilization of links marked core |
| conditions.moderate | 0.70 | External utilization of core links |
| conditions.high | 0.95 | External utilization of core links |
| pairs | R1–R12, R2–R12, R1–R3 | Separately simulated flows, not concurrent traffic |
| positions | 12 node-name → [x,y] entries | Drawing coordinates and N for hop normalization |
| links | 16 objects | Undirected link definitions below |

All four weights must be nonnegative and sum to 1. Utilization must remain below 1 because the queue formula divides by (1−u). Higher probe rate only changes the cohort-goodput calculation; this implementation does not add probe traffic to external utilization. Do not treat changing the rate as a validated congestion-load experiment.

| Per-link field | Meaning and constraint |
|---|---|
| a, b | Endpoint names present in positions; avoid duplicate unordered pairs and self-loops |
| bandwidth_mbps | Positive bandwidth; 10 for core, 20 for bypass links |
| delay_ms | Nonnegative propagation + processing delay; 1 core, 2 bypass |
| loss | Base packet-loss probability in [0,1); default 0.001 |
| utilization | External utilization for non-core links; default 0.15 |
| core | Boolean: true replaces stored utilization with current condition level |

The submitted graph is connected. Each pair must name existing nodes. `validate()` checks principal numerical constraints and graph construction checks connectivity, but this is not a general-purpose schema validator.

The experiment harness expects exactly the three named conditions normal/moderate/high: the dynamic sequence names them explicitly and the bar plots use three positions. Keep these names and count for supported configuration-only experiments. Keep at least one pair because the sweep/dynamic experiment uses the first. The legacy `verify_outputs.py` and consistency review intentionally target the submitted 540-run setup, not arbitrary modified experiments. Run Python normally, without `-O`, so assertion-based validations remain active.

`prepare.py` is an optional default generator: it overwrites `config.json` and the four router TXT files. It is not required for installation or demonstration. The final audit checks it only in a disposable copy.
