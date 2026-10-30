# Independent bounded-scope audit: local Pauli destabilizers bound code distance

2026-10-29, 21:21 UTC. Reviewed root `autonomous_clock_bridge_20261029/WHY_GRAPH_FACTORY_IS_NOT_A_MEMORY_THEOREM.md`.

**Verdict: the stated theorem and proof are correct under the displayed assumptions. No counterexample found or needed; the symplectic argument proves the claim.**

For a standard stabilizer code (abelian stabilizer group without -I), quotient physical Paulis by phases to obtain V=F_2^(2n). Let W=span{s_j,d_j}. Its dimension is at most2m<2n because k>0. The 2n single-qubit X/Z vectors span V, so some one-qubit e lies outside W. Its syndrome set J has cardinality at most r. The vector

    ell=e+sum_(j in J)d_j

has zero syndrome because <s_l,d_j>=delta_lj. If ell were a stabilizer vector, then e would lie in W, a contradiction. Hence ell is a nontrivial logical Pauli, with weight at most1+sum_(j in J)wt(d_j)<=1+rw. This establishes d<=1+rw for degenerate codes as well as nondegenerate ones.

Checks of possible hidden assumptions:

- Mutual commutation of the destabilizers is NOT required. Multiplication order contributes only an irrelevant Pauli phase, and syndrome addition is linear.
- Geometric locality is NOT required by the proof; bounded weight w and bounded syndrome degree r suffice. Geometry alone should not be substituted for the r assumption without bounded check incidence.
- The degree r refers to the chosen independent stabilizer generating family. An overcomplete local check list is not silently interchangeable with that family.
- The hypothesis that every one-qubit Pauli has syndrome degree <=r is slightly stronger than needed: it suffices for the 2n standard X/Z basis operators.
- k>0 is essential to the dimension argument and to existence of a nontrivial logical Pauli. Graph states have k=0 and are outside the conclusion.
- A growing-distance exclusion follows only when r and w remain uniformly bounded as n grows.
- This is not a no-go theorem for arbitrary independently syndrome-repairing CPTP maps, subsystem/gauge codes, collective conditional correction, or autonomous correction generally. The Pauli single-syndrome destabilizer assumptions must stay visible.

Minor presentation recommendation only: the heading could say “independent bounded-weight **Pauli** syndrome clearing” to prevent the broader reading that all local CPTP correction mechanisms are ruled out. The body already states the appropriate limitation.

This preserves a useful elementary failure boundary: the graph-state factory's syndrome-by-syndrome Pauli repair mechanism cannot simply be relabeled a bounded-degree growing-distance unknown-state stabilizer memory. No novelty claim or additional construction follows from this audit.
