# Uniform fast collar: width-independent interface degrees

Status: child adversarial audit passed; see INDEPENDENT_UNIFORM_COLLAR_AUDIT.md. No whole-project independent review or global recurrence claim. This removes the finite-width fixture restriction from the interface check in MAJORITY_INSERTION_UNIFORM_GREEN.md, under the explicit structural hypotheses below.

## Structural hypotheses
A fixed finite phase alphabet is repeated on w consecutive composition rows, where w is any fixed positive integer. There are low phases L with no horizontal moves and fast phases F. Phase transitions stay in the same row. Their rates, killing rates, and left/right horizontal rates have positive asymptotic leading powers in N, uniformly when the macroscopic cut fraction stays in a compact subset of (0,1).

- The low-phase block in each row is transient when killed on reaching F or actual killing.
- Every fast phase has BOTH horizontal directions of exact degree D, with positive leading coefficients, including exits at the two collar boundaries.
- Original outgoing rates at fast phases have degree at most D.
- The phase graph and all leading degrees are the same in every row.

No reversibility of phase switching, mixing rate, global stationary law, or Lyapunov barrier is assumed.

## Eliminate low phases exactly
Eliminate L independently within each row. An induced fast-phase rate is an initial fast-to-low rate multiplied by a low-chain exit probability, summed over initial low states. Consequently its size is at most the total initial fast-to-low rate. Every resulting fast-phase or killing rate therefore still has degree at most D. It is a positive rational function with a well-defined leading degree. Its support and degree are independent of the row and of w, since the low block is row-local.

Horizontal degree-D edges are unchanged. Write d_ij<=D for each effective phase edge, and assign cost ell_ij=D-d_ij>=0. Horizontal edges have cost zero. Killing edges have cost D-d_i,*.

## Exact Green degree
Let n=w|F| be the number of fast collar states. The killed generator determinant has leading degree Dn. Upper bound: each spanning-tree edge has degree at most D. Lower bound: orient every horizontal row-line toward an exterior collar exit; this is a rooted forest of degree Dn.

For interior fast states a,b, let dist(a,b) be the shortest directed path cost, using horizontal edges of cost zero. The positive forest numerator of G(a,b) contains a directed path a→b, so its degree is at most D(n−1)−dist(a,b).

For equality, take a shortest simple path a→b. Complete all other vertices into a forest using only horizontal degree-D edges: in each phase line, each interval between path vertices/boundaries is directed toward one of its endpoints. It then flows either into the selected path or into an exterior killing root; it cannot introduce a cycle. This gives a valid Green numerator forest with roots b and the exterior root, with a in the b-tree, and degree D(n−1)−dist(a,b). Hence

    deg G(a,b) = −D − dist(a,b).

If no path exists the Green entry is zero. The argument is exact positive-forest algebra, not a numerical or spectral approximation.

Because horizontal motion connects all rows at zero cost, dist(a,b) equals the shortest cost in the finite phase graph from phase(a) to phase(b). It is independent of the row positions and of w.

## Boundary Schur complement
An entrance edge from a retained boundary fast phase has degree D, as does a horizontal exit to either retained side. Thus an effective off-diagonal boundary rate from phase i to phase j has degree

    D − dist_phase(i,j),

when such a phase path exists. Its support is also independent of w. The killing degree is

    D − min_j [dist_phase(i,j) + D − d_j,*].

The minimum for killing ranges only over existing killing edges; an empty set means the effective killing edge is absent. Self-return edges are discarded as usual; no off-diagonal comparison is claimed for those self-loops. Every nonzero leading coefficient is positive and continuous in the macroscopic cut fraction, hence uniformly comparable on compact cut-fraction intervals.

It follows that the two-row and three-row exact Schur interfaces have identical off-diagonal/killing supports and degrees. This earns the finite interface premise of majority-coordinate insertion structurally for EVERY fixed phase width satisfying the hypotheses.

## Application to the actual coupled hard network
Take any fixed K>=4 and any fixed integer offsets h_0,...,h_K defining the residual shell, retaining exactly delta=0 reactions and killing all others. In an interior composition collar, all A,C reactant conditions are enabled for large N.

Low phases are B=0,1,2,3. They have no fast C moves. Repeated immigration either changes residual and kills, or advances B until it reaches B=4 (or exits the phase range); therefore the low block is transient. Fast phases are B>=4. Their reversible A/C conversion rates have degree D=3 in N with positive coefficients in both directions. All original outgoing rates have degrees 0,1, or3. Connector phase changes do not alter C.

All structural hypotheses hold. Thus the majority-insertion constant Green comparison is valid for arbitrary fixed K and offsets, not merely the earlier K=4,8,12 fixtures. No width-uniform constant is asserted. The operator still describes the exact joint process only until its residual changes; global inter-shell feedback is not solved.
