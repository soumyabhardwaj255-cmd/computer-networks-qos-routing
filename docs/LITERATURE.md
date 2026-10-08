# Verified literature and project mapping

Checked against primary documents during the final audit. The project is an educational adaptation; no cited source is claimed to validate our chosen weights or synthetic loss law.

## 1. Primary technical reference

**Full author list:** George Apostolopoulos, Doug Williams, Sanjay Kamat, Roch Guerin, Ariel Orda, Tony Przygienda. Names follow the RFC's author-address section; the bibliographic initials are G., D., S., R., A., T.

**Title:** QoS Routing Mechanisms and OSPF Extensions.

**Type/venue:** IETF Network Working Group, RFC 2676, Experimental protocol specification (not an Internet Standard).

**Date:** August 1999.

**DOI:** [10.17487/RFC2676](https://doi.org/10.17487/RFC2676).

**Official source:** [RFC Editor full text and metadata](https://www.rfc-editor.org/info/rfc2676).

**Supports:** using available link-state resources for QoS path selection, considering state updates, and using a Dijkstra-based computation framework (Appendix B). Our project adopts this framework conceptually. Our normalized weighted sum is student-designed; we do not reproduce the RFC's precise constrained algorithm, signaling, reservation or OSPF extensions. Its reported experiments are not our results.

## 2. Multi-metric theory and limitation

**Full author list:** Zheng Wang, Jon Crowcroft.

**Title:** Quality-of-Service Routing for Supporting Multimedia Applications.

**Venue:** IEEE Journal on Selected Areas in Communications, volume 14, issue 7, pages 1228–1234.

**Date:** September 1996.

**Official publication URL:** [IEEE Xplore document 536364](https://ieeexplore.ieee.org/document/536364).

**Primary text checked:** [Author-hosted manuscript](https://www.cl.cam.ac.uk/~jac22/otalks/wang96quality.pdf) and [published article hosted at Purdue](https://engineering.purdue.edu/~ece624/papers/crowcroft.pdf). IEEE's page required browser verification during this audit, so the actual text and venue/page information were checked in these primary paper copies. The official URL is supplied instead of relying on an unverified DOI resolution.

**Supports:** use of multiple QoS attributes, different metric-composition rules and the warning that a single mixed metric is a selection heuristic rather than a guarantee of multiple constraints. This informs our logarithmic reliability penalty and the explicit limitation of the weighted sum. It does not supply our weights, queue sampling, loss curve or measured gains.

## 3. Packet Tracer implementation references

These are vendor documentation, not extra research papers. Corporate author for both is **Cisco Systems, Inc.** No individual author list or DOI is specified.

| Title / publication type | Date | Official URL | Project support |
|---|---|---|---|
| Cisco IOS IP Routing: OSPF Command Reference — OSPF Commands: A through ip ospf demand-circuit; vendor command manual | Updated April 30, 2024 | [Cisco chapter](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/m_ospf-a1.html) | Syntax and meaning of explicit outgoing `ip ospf cost` |
| Cisco IOS IP Routing: OSPF Command Reference — OSPF Commands: show ip ospf through T; vendor command manual | Versioned online manual; publication year not asserted | [Cisco chapter](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-s1.html) | OSPF neighbor/interface verification commands |

These sources verify command semantics, not execution inside our Packet Tracer environment. Device behavior, saved topology and screenshots still require the manual checks in the lab guide. A third research paper would add scope without changing the implemented model, so none has been added.
