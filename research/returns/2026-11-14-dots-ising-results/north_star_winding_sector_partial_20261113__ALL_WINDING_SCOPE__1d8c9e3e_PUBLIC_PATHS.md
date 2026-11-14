# Why the consolidated union covers nonzero essential topology

Use the SAME deterministic physical-plus contour encoding in every branch. The inherited global-tail fixed-triangulation wording is explicitly extended to this encoding by research_notes/n1722_winding_wall_tail_20261113/ADAPTIVE_ENCODING_EXTENSION.md; no homology identification between different resolutions is used. Embedded disjoint essential curves on the torus have parallel primitive homology, and their total mod-two boundary homology is zero. Thus their number is even.

If total essential physical perimeter is at least5L, the already reviewed global winding tail applies, irrespective of contractible defects. Below5L:
- With four or more essential curves, each non-axis primitive curve would cost at least2L, impossible. Hence they are axis curves and one has length<5L/4<=2L-8 at the actual sizes, so the reviewed actual-short-wall transport applies.
- With exactly two curves of primitive homology with Manhattan norm at least3, each costs at least3L, contradicting total<5L.
- Exactly two axis curves are covered by the unrestricted-defect axis six-way decomposition.
- Exactly two diagonal curves are covered by the new total-perimeter>=5L adaptive global tail or intermediate retained-wall native transport.

Therefore the previously paid axis branches plus one global-tail branch cover every nonzero-essential configuration EXCEPT exactly-two-diagonal configurations. Their seven-term sum is bounded by exp(-138), exp(-4356) at R1000,R10000 using7<e^2. The new diagonal two-branch sum is exp(-3196), exp(-34695). Adding the two already-paid bounds and using2<e yields exp(-137), exp(-4355) for ALL nonzero-essential configurations.

This is an occupation normalized by the ORIGINAL core partition Z_A, not a probability under normalized full Gibbs measure. Every mass-tail branch uses v<=1; every transport branch uses the ORIGINAL capacity and site clock. No conclusion is drawn about configurations with zero essential curves. That complement contains important high-mass contractible structures and prevents interpreting this result as the complete residence/exit theorem.
