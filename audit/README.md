# Final audit evidence

The final audit ran the unchanged project in a fresh temporary Python 3.12 environment installed from requirements.txt. It did not replace any original experimental output.

- `audit.json`: machine-readable status, SHA-256 comparisons and figure reproduction results.
- `preserved_files_before.json`: original source/configuration/tests/results/figures/abstract hashes, confirmed unchanged afterward.
- `01_environment.log` and `02_install.log`: actual clean environment creation and installation output. The Windows short-path/junction location notice is informational; creation succeeded.
- `03_pip_check.log`: dependency consistency check.
- `04_dependencies.log`: exact resolved package versions for this audit.
- `05_tests.log`: all five unit tests passed.
- `06_reproduction.log`: actual isolated simulation output.
- `07_figures.log`: nine PNGs decode; all nine also matched original bytes in audit.json.
- `08_consistency.log`: CSV aggregation/accounting and static IOS topology checks.
- `09_legacy_verifier.log`: original verify_outputs.py passed inside the disposable copy.
- `10_prepare.log`: prepare.py exited successfully without console output; configuration/router hashes also matched.

All five CSVs and FINAL_RESULTS.md reproduced byte-for-byte. Run metadata timestamps naturally change; the configuration and its hash matched. Figure labels, legends and layouts were visually reviewed. No simulation implementation error requiring a result change was identified.

Requirements contain both direct third-party imports: NetworkX and Matplotlib. Their transitive dependencies installed successfully. No extra application dependency is needed for standard-library tests or the new audit/packaging helpers.

The formal report, configuration guide, CSV-based results summary and expanded viva guide were completed after the numerical audit. package_project.py checks their presence, local links, report/summary table agreement and preservation hashes before assembling the final archive.

Packet Tracer remains unexecuted. Static configuration checks do not certify simulator execution, a native .pkt or screenshots. Those three related tasks remain manual.
