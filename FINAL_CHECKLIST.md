# Final project completion checklist

Status key: **DONE** = prepared and checked; **MANUAL** = requires actual Packet Tracer operation/evidence; **NOT REQUIRED YET** = outside the requested scope or part of a later presentation. No manual evidence is claimed complete.

## A. Assessment 6 submission

| Status | Item | File/evidence |
|---|---|---|
| DONE | Seven-part abstract, preserved unchanged | docs/ABSTRACT.md; docs/ASSESSMENT6.md entry point |
| DONE | Literature-grounded objective and defensible gap | docs/REPORT.md; docs/LITERATURE.md |
| DONE | Synthetic-model claims and measured results correctly qualified | docs/RESULTS_SUMMARY.md |
| DONE | Portable source and clean installation instructions | README.md; requirements.txt |
| DONE | Clean final submission folder and archive | submission/project/; FINAL_Computer_Networks_Project.zip |
| NOT REQUIRED YET | Institution-specific cover form, signatures or portal upload | Not specified; add administrative fields only if required by faculty |

## B. Project demonstration

| Status | Item | File/evidence |
|---|---|---|
| DONE | Source syntax, dependency installation and dependency consistency | audit/01_environment.log through 04_dependencies.log |
| DONE | Five meaningful unit tests | audit/05_tests.log |
| DONE | All 540 main experiments reproduced in a separate clean environment | audit/06_reproduction.log; audit/audit.json |
| DONE | Five CSVs and generated results report reproduce byte-for-byte | audit/audit.json |
| DONE | Nine named figures decode and reproduce identically | audit/07_figures.log; audit/audit.json |
| DONE | Configuration fields, units and safe reproduction workflow documented | docs/CONFIGURATION.md; README.md |
| DONE | Baseline and adaptive routes, sweep and recovery evidence | results/dynamic_routes.csv; figures/selected_routes.png |
| DONE | Default generator and original verifier checked in isolation | audit/09_legacy_verifier.log; audit/10_prepare.log |
| DONE | Original simulation, config, tests, figures, results and abstract preserved | audit/preserved_files_before.json |
| NOT REQUIRED YET | Live presentation of the prepared Python demonstration | Ready to present; no additional implementation required |
| NOT REQUIRED YET | Slide deck, video or cloud deployment | Not requested and unnecessary to run this lab project |

## C. Final report

| Status | Item | File/evidence |
|---|---|---|
| DONE | Title, abstract, introduction, problem, existing work, gap and objectives | docs/REPORT.md |
| DONE | Model, methodology, baseline/proposed algorithms and normalized cost | docs/REPORT.md |
| DONE | Pseudocode, flowchart and textual flowchart description | docs/REPORT.md |
| DONE | Setup, formulas, results, discussion and trade-offs | docs/REPORT.md |
| DONE | Limitations, conclusion, future scope and references | docs/REPORT.md |
| DONE | Complete three-pair results plus separate sweep/dynamic scope | docs/RESULTS_SUMMARY.md |
| DONE | Author lists, venues/types, dates, source URLs and project mapping | docs/LITERATURE.md |
| DONE | All summary-table numbers agree with CSV to displayed precision | package_project.py validation |
| NOT REQUIRED YET | Institution-specific DOCX/PDF template or printed binding | Markdown report is complete; no format/template requirement was provided |

## D. Packet Tracer

| Status | Item | File/evidence |
|---|---|---|
| DONE | Four 2911 routers, zero switches, two PCs and exact six-cable topology | packet_tracer/LAB_GUIDE.md |
| DONE | Full IP/interface/mask/gateway table | packet_tracer/LAB_GUIDE.md |
| DONE | Complete router configurations and ordinary OSPF commands | packet_tracer/ALL_ROUTER_COMMANDS.md; R1.txt through R4.txt |
| DONE | Verification, ping/traceroute and Simulation Mode procedure | packet_tracer/LAB_GUIDE.md |
| DONE | Failure, optional cost change, asymmetry explanation and restoration | packet_tracer/LAB_GUIDE.md |
| DONE | Exact screenshot subjects, filenames and caption guidance | packet_tracer/LAB_GUIDE.md section 9 |
| DONE | Static addressing/cost checks; no claim of actual execution | packet_tracer/CONSISTENCY_REVIEW.md; audit/08_consistency.log |
| MANUAL | Open Packet Tracer, build/configure topology and verify live behavior | Follow the 15–20 minute lab guide |
| MANUAL | Save actual topology in healthy restored state | packet_tracer/Assessment6_QoS_Demo.pkt |
| MANUAL | Capture genuine topology/configuration/ping/path evidence | packet_tracer/screenshots/ |
| DONE | Packaging command ready to include future manual evidence | python package_project.py |

## E. Viva preparation

| Status | Item | File/evidence |
|---|---|---|
| DONE | 30-second, 1-minute and 3-minute explanations | docs/VIVA.md |
| DONE | Five-minute demo order and whiteboard algorithm explanation | docs/VIVA.md |
| DONE | Dijkstra, normalization, weights, baseline and synthetic-model Q&A | docs/VIVA.md |
| DONE | Complexity, results scope, limitations and future work Q&A | docs/VIVA.md |
| DONE | Python versus Packet Tracer distinction and networking questions | docs/VIVA.md |
| NOT REQUIRED YET | Actual oral viva delivery | Materials are complete and ready for rehearsal |

**Remaining deliverable work:** only real Packet Tracer construction/verification, saving the native file, and taking real screenshots. After placing them in packet_tracer/, run package_project.py to refresh the final archive. Update MANUAL entries only after actually completing those tasks; this checklist intentionally does not infer completion from a file merely existing.
