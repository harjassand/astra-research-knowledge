# Gap-adaptive stopping under the exact structural promise
2026-10-29. Supplement to v1/v2, unreviewed.

A supplied numerical lower bound g0 is unnecessary for eventual acquisition if g>0 and the exact random-unitary/common-frame structural promise holds. The claim is conditional on that model; no stopping rule here proves the model from data.

At stages j=0,1,... use fresh pooled banks with η_j=2^(−j), per-stage failure allocation δ_j=δ/[2(j+1)²] (sum <δ), and m_j=ceil(2η_j^(−2)log[162(n−1)/δ_j]). Let e_j=9η_j. In each edge's Ahat=I−That, order singular values increasingly s1≤s2≤...≤s9 and set gL_j=min_edges(s2−e_j). Weyl's inequality shows gL_j≤g on the simultaneous entry-error event, because the exact A has s1=0 and s2=g for each star edge.

Stop if gL_j>0 and
8sqrt(6)(n−1)e_j/gL_j ≤ ε,
with 0<ε≤1. This automatically ensures e_j/g<1/[2sqrt(6)], hence the sign-rounding premise. Then v1's uniform service diamond bound is at most ε. Eventually gL_j≥g−2e_j, so for every g>0 the procedure stops at finite stage on the confidence event. Sample count differs from the known-gap pooled bound by logarithms of the stage index and geometric-stage constants. If g=0, the confidence event forbids stopping since s2hat≤e_j. No finite upper runtime is promised for zero gap; aborting at a declared budget returns inconclusive, not a certified encoder.

This does not test whether unobserved bath branches share the learned full joint algebra. A well-conditioned reduced pair estimate alone cannot license memory-robust deployment. Near-identity training remains costly, not magically gap-free.
