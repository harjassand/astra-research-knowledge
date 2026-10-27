# The N1077 bridge: exact scope and obstructions

27 October 2026. These are bounded deductions from the supplied constructions,
not a claim of a general circuit lower bound or a new tractability class.

## Governing sources

The packet is frozen at:
https://github.com/harjassand/astra-research-knowledge/blob/e1e2272165c8548326c31bb11817c28f871d21e9/knowledge/current/packets/N1077.json

The full governing proof read for this note is:
https://github.com/harjassand/astra-research-knowledge/blob/e1e2272165c8548326c31bb11817c28f871d21e9/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-compiled-physical-interfaces/source/tensor/originals/alternative/representation_operation_20261027/PROOF.md

The ETH manuscript is the attached `eth_paper.pdf`, especially Appendix D.1 and
D.4.6, corresponding to:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf

## 1. What N1077 supplies

For a closed loopless planar trivalent graph with explicit cyclic port order
and eight rational entries per vertex, N1077 first requires nonzero local
hyperdeterminants and all four entries of every CP edge pairing to be nonzero.
On that generic domain it recognizes exactly compatible independent edge
bases making every vertex a ternary parity tensor. The intrinsic predicate at
vertex v is beta_v=1. It acquires the bases using local quadratic algebras,
evaluates in one common quadratic finite field, and uses original-input height
bounds plus CRT for exact rational contraction and original-edge observables.

Its governing proof explicitly credits known heterogeneous parity/matchgate
gauges and Fisher/FKT contraction. Failure of its predicate does not imply
hardness, and neither arbitrary tensor networks nor generic circuits are in
its completion contract.

## 2. AND chains are outside the generic admission contract

Let the Boolean gate tensor be T[a,b,c]=1 if c=a AND b and zero otherwise.
It has the rank-two CP decomposition

    T[a,b,c] = sum_s A[a,s] A[b,s] C[c,s],
    A = [[1,0],[1,1]],       C = [[1,-1],[0,1]].

The factors are invertible and its 2x2x2 hyperdeterminant equals one. Joining
the output of one such AND to an input of another yields the CP pairing

    W = C^T A = I.

This has zero off-diagonal entries. Under any invertible opposite edge basis
change C -> G C, A -> G^{-T} A, the pairing is unchanged. CP uniqueness on
the nonzero-hyperdeterminant domain allows only column permutations and
nonzero rescalings, which preserve the existence of zero entries. Therefore
no such gauge makes the AND-chain edge generic in N1077's required sense.

This is an admission obstruction, not a claim that AND circuits are hard.
Indeed a circuit of AND gates alone is easy. It rules out applying the current
compiler indiscriminately to ordinary gate tensors.

## 3. Generic planar tensors can fail compatibility

Take the two-vertex graph with three parallel edges, embedded in the plane.
At the first vertex use COPY, with CP factor I on each leg. At the second use
CP factor W=[[1,2],[3,5]] on each leg. Both tensor hyperdeterminants equal one,
and every CP edge entry is nonzero. The two intrinsic predicates are

    beta_left  = (W10 W11 / (W00 W01))^3 = 3375/8,
    beta_right = (W01 W11 / (W00 W10))^3 = 1000/27.

Neither is one. By the completeness statement in the governing proof, no
compatible independent-edge parity gauge exists. Its contraction nevertheless
equals 1^3+2^3+3^3+5^3=161 and is directly computable. This distinguishes
failure of the representation from computational hardness.

## 4. Fixed-graph low-degree gauge deformations cannot supply arbitrarily many
## tractable interpolation nodes

Consider a parameterized rank-two CP presentation on a fixed trivalent graph,
with every entry of every leg matrix a polynomial of degree at most d in t.
Assume all legs and pairings remain nondegenerate at the interpolation nodes.
At vertex v define

    P_v(t) = product_{e incident v} W_e[1,0](t) W_e[1,1](t)
           - product_{e incident v} W_e[0,0](t) W_e[0,1](t).

Here pairings are oriented with v as their row endpoint. Each pairing entry
has degree at most 2d, so deg P_v <= 12d. If beta_v(0) != 1, then P_v(0) != 0.
Consequently P_v is a nonzero polynomial and has at most 12d distinct roots.
Every generic parity-admissible interpolation node must be one of those roots.
Thus the number of such nodes is at most 12d.

This does not exclude richer deformations, graph-changing gadgets, Hermite
data of increasing order, or an extension of the admission class. It does
exclude obtaining an unbounded ratio of tractable nodes to coefficient degree
by only this fixed-graph polynomial CP deformation. The contraction polynomial
has degree at most 3d times the number of vertices; ordinary value
interpolation therefore does not automatically get the many-low-degree-node
benefit of the supplied ETH construction.

## 5. Why Appendix D already subsumes the naive tensor reduction

The ETH manuscript's Theorem D.1 contracts arbitrary bipartite Boolean tensor
networks with O(s) edges and maximum degree at most ceil(s^(9/10)), given the
stated entry-evaluation and ring contracts, in

    (s+L)^O(1) * 2^O(s/sqrt(log s))

bit operations and polynomial space. Hence the ordinary gate-to-tensor
encoding with O(n+S) wires, for n independent inputs and S gates, is already
covered. N1077 cannot remove its dependence on the total wires simply by
changing bases: an invertible edge gauge leaves the graph, number of edges,
and degrees unchanged.

Putting the whole program into one implicitly evaluated n-leg tensor keeps
only n wires but gives degree n. It does not meet D.1 at s=Theta(n). To satisfy
n <= ceil(s^(9/10)) by parameter enlargement requires s=Omega(n^(10/9)), giving
a displayed bound worse than brute-force input enumeration. Dropping the
degree restriction would be a substantive extension, not a restatement.

There is also a precise oracle boundary. For arbitrary f:{0,1}^n->{0,1}, exact
summation from Boolean point queries needs all 2^n queries in the worst case:
on an all-zero transcript, any unqueried x could be the sole point with
f(x)=1. In particular evaluating its multilinear extension at
(1/2,...,1/2) already returns 2^(-n) times the desired count. Circuit structure
can defeat an oracle argument, but an alleged compiler must actually use that
description; cheap Boolean entry access alone cannot justify cheap evaluations
of a transformed high-degree tensor.

## Executed checks

`check_bridge.py` verifies the AND factorization and hyperdeterminant, exact
pairing invariance under three rational invertible edge gauges, both theta
hyperdeterminants and failed beta values, and the exact contraction 161.
These checks support the small examples; the structural claims above are
proved algebraically. No practical-speed or historical-priority claim follows.
