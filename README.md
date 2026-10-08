# QoS-Aware Adaptive Routing for Improved Network Performance under Congestion

VIT BCSE308P — Computer Networks Lab, Assessment 6.

This project compares hop-count Dijkstra with a configurable QoS-weighted Dijkstra heuristic on a 12-router topology. It follows the resource-aware routing framework of RFC 2676; it does not reproduce that RFC's bandwidth-constrained algorithm or implement OSPF extensions.

## Clean-environment run instructions

Install Python 3.12 with pip/venv. Extract the final archive and open a terminal inside its `project` directory. A virtual environment is intentionally not included. Package installation needs internet access or an existing package cache. On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe run.py
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

If the Windows `py` launcher is unavailable, use `python -m venv .venv` with Python 3.12 on PATH, or `& 'C:\path\to\python.exe' -m venv .venv`. No environment activation or PowerShell execution-policy change is required. On Linux/macOS:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run.py
.venv/bin/python -m unittest discover -s tests -v
```

The default run produces the 540 main experiment rows plus the first-pair sweep and dynamic trace. It overwrites generated results and figures in that project copy. Preserve the supplied evidence by demonstrating in a separate extracted copy, or use the isolated audit below. Python 3.12 with the two pinned direct dependencies was tested; the exact resolved dependency list is in `audit/04_dependencies.log`. NumPy and Pillow are installed transitively by Matplotlib; project source directly imports only NetworkX and Matplotlib beyond the standard library.

### Verify without overwriting saved results

```powershell
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe -m unittest discover -s tests -v
.venv/Scripts/python.exe final_audit.py
```

`final_audit.py` installs requirements into a temporary clean environment, runs a disposable project copy, compares all five CSVs and the generated results report byte-for-byte, runs the existing output/consistency checks and confirms original file hashes are unchanged. It writes actual evidence under `audit/`. It requires venv support and package-index/cache access. It does not execute Packet Tracer.

`verify_outputs.py` is the original verifier for the submitted default settings: it checks 540 rows/accounting/nine figures and also creates the older `Assessment6_QoS_Routing.zip`. The final audit runs it only inside its disposable copy. For the clean final package use `package_project.py` instead; it excludes nested ZIPs and development artifacts.

### Configuration and preparation

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for every field, unit and supported customization limit. Keep `config.json` unchanged when reproducing the submission. Run optional variants only in a separate project copy.

`prepare.py` restores the default configuration and router configuration files. It is not a required setup step and overwrites those files if run. Its default reproduction was checked in isolation.

## Deliverables

- `results/FINAL_RESULTS.md`: actual numerical results and interpretation.
- `results/trials.csv`: 540 baseline/proposed runs, each with a seed, route and metrics.
- `results/summary.csv`: condition-level means and approximate 95% confidence intervals.
- `results/paired_differences.csv`: proposed-minus-baseline paired differences and intervals.
- `results/dynamic_routes.csv`: normal → moderate → high → recovery route trace.
- `results/congestion_sweep.csv`: performance across seven congestion levels.
- `results/run_metadata.json`: exact configuration, hash, Python version and timestamp.
- `figures/`: topology, selected routes, six metric charts and congestion response.
- `docs/REPORT.md`: architecture, algorithm, formulas, methodology and limitations.
- `docs/ABSTRACT.md`: requested Assessment 6 submission structure.
- `docs/ASSESSMENT6.md`: entry point to the unchanged abstract and supporting files.
- `docs/RESULTS_SUMMARY.md`: all metrics with three-pair, sweep and dynamic scopes distinguished.
- `docs/LITERATURE.md`: verified authors, publication details and exact project support.
- `docs/CONFIGURATION.md`: configuration field reference and assumptions.
- `docs/VIVA.md`: explanation and demonstration checklist.
- `packet_tracer/LAB_GUIDE.md`: exact devices, wiring, addresses, commands, simulation procedure and screenshots.
- `packet_tracer/ALL_ROUTER_COMMANDS.md`: all four complete configuration blocks; individual TXT files are also supplied.
- `audit/`: genuine clean-environment execution logs, numerical comparisons and preservation hashes.
- `FINAL_CHECKLIST.md`: DONE / MANUAL / NOT REQUIRED YET status for each deliverable.

### Figures

| File in figures/ | Content / scope |
|---|---|
| topology.png | 12-router topology, bandwidth and propagation/processing delay |
| selected_routes.png | R1–R12 paths at three conditions |
| delay_ms.png | Average delivered delay across all three pairs |
| loss_pct.png | Average packet loss across all three pairs |
| throughput_mbps.png | Average cohort goodput across all three pairs |
| pdr_pct.png | Average delivery ratio across all three pairs |
| hops.png | Average selected route hops across all three pairs |
| qos_cost.png | Common QoS cost across all three pairs |
| performance_vs_congestion.png | Delay/loss sweep for R1–R12 only |

The six comparison charts show approximate 95% confidence intervals. The sweep has its own legend; its colors differ from the comparison charts, so identify series by their labels.

### Final package

```powershell
.venv/Scripts/python.exe package_project.py
```

Creates a clean `submission/project/` folder and `FINAL_Computer_Networks_Project.zip` with a SHA-256 manifest. It includes only intended source, documents, figures, results and audit evidence, plus genuine Packet Tracer files/screenshots if later added under `packet_tracer/`. It excludes `.venv`, `.git`, caches, older ZIPs and the submission folder itself. Existing final package files are refreshed; foreign files in the staging folder cause the script to stop rather than silently carry clutter forward.

Only manual deliverables outstanding: construct/verify the Packet Tracer topology, save `packet_tracer/Assessment6_QoS_Demo.pkt`, and put actual screenshots under `packet_tracer/screenshots/`. Then run the packaging command again. Do not claim Packet Tracer evidence exists before doing this.

## Honest scope

Python performs the custom algorithm and quantitative packet experiments. Packet Tracer demonstrates IPv4, OSPF and ICMP using a smaller corresponding multipath topology. A native `.pkt` file has **not** been created or verified: Packet Tracer was not found in the checked installation locations, and this session has no native desktop control. The supplied configurations must be loaded and tested in Packet Tracer. Do not present its expected outputs as captured evidence.

The simulator samples per-packet loss and analytical queue delay using seeded randomness. Utilization and congestion loss are external inputs; it is not a discrete-event queue simulator, a TCP implementation or a real-time network emulator. No screenshots or measurements from Packet Tracer are fabricated.
