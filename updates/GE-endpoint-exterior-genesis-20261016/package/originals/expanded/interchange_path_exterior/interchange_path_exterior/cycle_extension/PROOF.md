# Weighted-cycle two-discrepancy reduction and its branching boundary

This is a self-contained algebraic extension of a classical exterior-power representation, not a claim of historical novelty. Nonnegative fixed symmetric edge rates are assumed. No physical input acquisition is implied.

Let a cycle have vertices 0,...,n-1, n>=3. Let H on unordered distinct pairs have diagonal d_x+d_y, and off-diagonal -w for each allowed single-endpoint move; moves into the other occupied vertex are killed. Thus its killing rate is twice the weight of the joining edge.

Define the signed one-particle matrix A with ordinary Laplacian diagonal, negative off-diagonal weights on edges (j,j+1), and positive off-diagonal weight on the wrap edge (n-1,0). In the ordered wedge basis e_x wedge e_y (x<y), the generator A wedge I + I wedge A is exactly H. Non-wrap moves do not reorder the two coordinates. Every allowed wrap move reorders them once, cancelling the positive off-diagonal sign. Diagonals agree. This proves the identity entrywise, including adjacent-pair killing through the retained diagonal.

Let C be the ordinary weighted Laplacian on the 2n-cycle with repeated weights. For T=[I;-I], CT=TA. Consequently exp(-tC)T=T exp(-tA), and exp(-tA) is the upper-left n-by-n block of exp(-tC) minus its upper-right block. Each signed row has l1 norm at most one. A substochastic nonnegative approximation to the cover heat matrix has the same bound after this subtraction, and the signed row l1 error is at most the cover row error.

For x<y the survival probability is the sum over u<v of the determinant of rows x,y and columns u,v of exp(-tA). Equivalently S_xy=p_x^T K p_y, where K_uv=sign(v-u). If both approximate rows have l1 norm <=1 and individual row error <=epsilon, the bilinear error is <=2epsilon, by telescoping the two factors and using max|K_uv|=1. Compute the signed bilinear value before clipping its error interval to [0,1]. No total positivity of rounded matrices is assumed. The positive-cover integer enclosure therefore certifies cycle pair survivals using 2n one-particle states. An executed end-to-end cycle averaging certificate has not yet been produced.

## Restricted branching obstruction
On the unit-weight star with center 0 and leaves 1,2,3 consider the pair-state loop
(1,2),(0,2),(2,3),(0,3),(1,3),(0,1),(1,2).
The ordinary one-particle wedge generator and physical killed-pair generator have relative edge-sign product -1 around this loop: the paths exchange the two labels without collision. Every physical tree edge occurs twice, so changing fixed one-particle edge signs cannot change that product. General reversible phases likewise cancel across the paired opposite traversals. A pair-basis gauge also telescopes around the loop. Therefore this fixed one-particle edge-gauge exterior representation cannot reproduce the physical pair generator on this star. This is not an obstruction to other algorithms, larger state representations, or graph-specific methods.

Original check_cycle.py verifies exact integer generator/intertwiner identities for n=3,...,12, the star loop, and separate floating heat diagnostics. checks.json records results. Floating diagnostics are not the proof.
