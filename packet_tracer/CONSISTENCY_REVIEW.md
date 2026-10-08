# Consistency review

This document records the earlier read-only consistency review. The later final completion audit additionally reproduced the entire experiment in a clean disposable environment; see `../audit/audit.json` and `../audit/README.md`. Original source and saved experimental results remain unchanged. Packet Tracer itself is still unexecuted.

The existing simulation was not rerun, rebuilt or edited. Results were read and checked against the stored configuration and documentation.

## Automated checks passed

- Stored configuration and SHA-256 match the current configuration.
- All 540 expected trial rows have unique condition/pair/trial/algorithm keys.
- Packet counts, loss, PDR, goodput and selected-route hop counts are internally consistent.
- All seven summary metric means and approximate 95% confidence intervals match recomputation from saved trial rows.
- All paired differences and their intervals match recomputation from saved trial rows.
- Dynamic routes show the initial path, a changed path under congestion and recovery.
- The four existing IOS configurations have unique interface addresses and matching /30 subnets across the four planned router links.
- A graph calculation confirms the planned R1 destination metric changes from 30 to 70, and confirms that a one-sided cost change can leave the reply route unchanged.

## Documentation review

The report and abstract agree with the saved results: normal delay is 4.8223 ms for both methods; moderate delay changes from 9.8057 to 8.5490 ms; high delay changes from 47.2155 to 8.5490 ms. High loss changes from 21.3000% to 0.3267%, and mean selected-path hops rise from 2.3333 to 3.3333. The abstract rounds these values correctly. High delay reduction is 81.89%.

The report correctly distinguishes the three-pair summary from the first-pair congestion sweep, and notes that the heuristic is not always better in delay. Model assumptions, conditional delivered delay, cohort goodput and related loss/PDR metrics are explicitly disclosed. The normalized log-loss penalty in the report matches the implementation.

No result-changing implementation error was identified in this consistency review. No existing results, source files, configuration or figures were changed. This is an artifact consistency audit, not a new empirical validation of the underlying synthetic model.

## Packet Tracer boundary

The four-router diamond is a conceptual reduction, not an exact copy of the Python topology. Both alternatives have equal hop counts. Conventional OSPF uses configured interface cost; it does not execute the Python delay/loss/utilization heuristic. Manual cost changes and link shutdown demonstrate different triggers and should be captioned accurately.

Packet Tracer itself has not been executed. Static configuration and cost checks are not substitutes for loading the topology, checking IOS behavior and capturing real evidence on the user's computer. The native .pkt and screenshots remain manual deliverables.
