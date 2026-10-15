# Explicit polynomial final filling

This is a standard cubical chain contraction, not a novelty claim. It makes
the ideal readout decoder in the memory theorem constructive. All chains are
over F2.

For each small vertex-connected syndrome component, use its bounded torus
lift and coordinate hull B=product_i[a_i,b_i]. Let pi_i project coordinate i
to a_i. An i-directed edge projects to zero; every other edge projects to
the parallel edge on that lower face. Define the prism P_i of a j-directed
edge, j!=i, as the strip of ij plaquettes between that edge and its projection.
Set P_i of an i-directed edge to zero. On vertices the prism is the intervening
i-directed path. The elementary cubical identity is

    boundary P_i + P_i boundary = id + pi_i.

If c_0 is the component cycle, put c_i=pi_i(c_(i-1)), i=1,...,4, and

    D_B(c_0)=sum_(i=1..4) P_i(c_(i-1)).

Since each c_i is a cycle, boundaries telescope. All edges vanish after four
projections, so boundary D_B(c_0)=c_0. Every written face lies in B. This
choice is deterministic once the component lift, coordinate order and lower
corner are fixed. Identical unaffected components therefore receive identical
fillings, as the local homology argument requires.

Projection never increases the number of edges. If H=sum_i(b_i-a_i), the
construction requires at most H*|c_0| face toggles. Summing over syndrome
components gives O(L*|s|)=O(L^5) elementary binary toggles in the worst case
on the small-component regime. A dense face bitset uses O(L^4) bits. These
are deliberately crude bounds; syndrome extraction and physical execution
of the recovery are separately idealized.

To define D on every boundary syndrome, including those with large components,
use deterministic binary Gaussian elimination on the torus edge-face boundary
matrix. It has O(L^4) rows and columns, giving a crude O(L^12) preprocessing
bound and O(L^8) bits with dense arithmetic. A solution exists for the supplied
physical syndrome because it is the boundary of an accumulated error 2-chain.
This fallback is never used on the good histories of the theorem.

Use the primal and dual constructions for the two CSS syndromes, apply the
resulting Pauli recovery, then invert a fixed toric-code encoding isometry.
This is a perfect mathematical recovery channel. No noisy measurement,
fault-tolerant implementation, energy cost or latency advantage is established.
