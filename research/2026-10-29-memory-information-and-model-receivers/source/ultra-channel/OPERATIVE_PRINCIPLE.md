# Pairwise-output localization

This branch takes accepted N675 as an input. Its working source is the fully read packet at revision ad7ff1b9d15a774d4b4d8362314c7070cac030e5 / input 5788b3479627421d3a67e1e6fced19f66323e94e01ccdaf4bf094a14547aa8b9. This is now a pinned historical snapshot after a later published refresh failed. No claim of present connector completeness is made.

The proposed operation is exact comparison and synthesis for an unbounded-alphabet structured class, rather than bounding the reference dimension of a generic instance. Each output row of each classical channel has at most two nonzero input coefficients. For every pair {i,j}, form the rational Stieltjes difference

    kappa_ij(t) = sum_Q a*b/(a+b*t) - sum_P a*b/(a+b*t), t>0.

Conjectured theorem, with the proof spine already reconstructed: ordinary less-noisy order, complete SLD order, and unrestricted complete Umegaki order P >= Q are equivalent to nonnegativity of every kappa_ij on the positive half-line. No acyclic-support assumption is needed. Quantum-reference sufficiency uses a two-positive-operator pencil; necessity uses a faithful classical baseline concentrating on one edge. Exact rational polynomial isolation then gives a terminating input-dependent compiler.

Precomposing both channels with an arbitrary common quantum measurement preserves the complete order. A strictly positive, noncommuting, linearly independent primitive POVM places an actual synthesized example inside the strict rational-complex input domain of N675. Complete entropy order does not imply stochastic or quantum postprocessing simulation.

The binary core is not being claimed as new. Makur--Polyanskiy supplies the classical Fisher characterization. Eriksson v2 (2026 working paper) explicitly states quantum-reference coefficient collapse on every two-symbol restriction. The present question is whether localization across overlapping pair supports is an established theorem and, if not, what reusable synthesis/composition operation it enables. Historical priority remains UNKNOWN.

Important exclusion: a contraction comparison against an erasure channel with one global row has support arity n, so the theorem would not assert that every sparse channel has its ordinary contraction coefficient after quantum-reference activation.
