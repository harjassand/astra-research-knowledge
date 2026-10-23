# Sharper operator bound transferred from the preserved forest calculation

This is a proof consequence of the completed star-four construction and an
explicitly recovered earlier owner proof. It changes no observation, output,
input, coloring, finite witness or measured run. The saved receiving records
retain their valid squared bound 2. Their unchanged canonical least-squares
decoder actually has the stronger uniform operator bound below. The Frobenius
output bound remains sqrt(2).

**Theorem.** For any finite triangle-free support supplied with any proper star
coloring, the canonical least-squares coordinate decoder satisfies

    ||Dhat-D||op <= sqrt(3/2) ||E||F.

The diagonal is arbitrary, all original coordinate actions are observed, and
each query row has norm one. The claim is independent of graph size, degree,
number of colors and action-noise distribution. It is not claimed sharp for
this decoder on every graph or historically new.

## Proof

First choose a direct exact left inverse T. Read the diagonal in each vertex's
own-color action cell. In every bichromatic star, read each edge from its leaf's
action cell in the center's color. For a single-edge component choose either
endpoint. These action cells are isolated and distinct: a selected leaf has
exactly one neighbor of that color, different color pairs use different cells,
and properness separates the diagonal. T ignores the other action cells and
copies each edge coefficient symmetrically. Thus T is an exact left inverse on
every supported symmetric matrix, with the stated free diagonal.

For unit z, put w_i=z_i^2. The squared norm of the scalar linear functional
E -> z^T T(E) z, measured against the full Frobenius input norm, is exactly

    Q_G(w)=sum_i w_i^2 + 4 sum_{ij in E(G)} w_i w_j,
    w_i>=0, sum_i w_i=1.

This is the same isolated-read identity used in the preserved Cycle2 forest
proof. Its mass-shifting argument requires only that cliques have order at
most two, so it applies to every triangle-free graph. If two positive-weight
vertices are nonadjacent, keep their sum fixed and vary their two weights.
Q is a convex quadratic along that interval: their mutual edge is absent,
their two squared terms have positive quadratic coefficient, and all other
incident contributions are linear. One endpoint of the interval does not
decrease Q and removes a positive-weight vertex. Repeating finitely often
concentrates the weight on a clique. In a triangle-free graph that support has
at most two vertices. Its value is either 1 or

    a^2+b^2+4ab=1+2ab<=3/2,  a+b=1.

Consequently, using symmetry of the output,

    ||T||_(F->op)^2
     =sup_(||z||=1) || E -> z^T T(E) z ||^2 <=3/2.

Now let L map supported symmetric matrices to their complete coordinate action
block, and let Pi be the orthogonal projection in Frobenius action space onto
range(L). Star coloring makes L injective, and the canonical least-squares
inverse R is L^{-1} Pi. Since T is an exact left inverse on range(L),

    R=T Pi.

Pi is a contraction in the original Frobenius noise norm. Hence
||R||_(F->op)<=||T||_(F->op)<=sqrt(3/2). Applied to Y=LD+E, RY-D=RE, proving
the theorem. This comparison does not change the actual saved LS output to
the direct decoder T, and it does not require extra observations. QED.

The same proof pays a floating supported projected-action residual by
sqrt(3/2)||R_num||F, in addition to sqrt(3/2)||E||F. The independent residual,
action acquisition, assembly and D deltaX allowances remain necessary.

## Receiving consequence and source boundary

Every graph in the completed grammar is triangle-free and its constructed
coloring is star. The theorem therefore gives the stronger operator squared
bound 3/2 on all of them, including the same three exact receiving operations.
No new numerical experiment is needed to make this all-noise argument.
The old saved squared bound 2 remains a true, weaker certificate and the
Frobenius-output squared bound is still 2. The archived action data and timings
were not rewritten to suggest a second run.

The old direct forest theorem, including its sharper sqrt(3/2) operator bound,
was recovered from native Cycle2 ZIP 10,829,134 bytes, SHA256
2afd976929a3290da49f710a5cd5bce428a6f3d28a33b3130f3675f44c43b953.
The exact selected PROOF.md and member/hash receipt are in
`sources/cycle2_selected/`. Sections 1-2 were read. No earlier calculation was
rerun. The receiving use of that capital is the transfer of its quadratic
bound to triangle-free star recovery, followed by the action-projection
identity for the unchanged new LS decoder. This supplies a mathematical
consequence; it does not establish a causal research-amplification claim.

Costs of this read, reasoning and focused proof review are unmetered and remain
unknown. Internal proof and inherited attribution are separate from historical
priority, external acceptance or application performance.
