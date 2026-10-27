# Hidden cubic coordinates: exact comparators and two method barriers

27 October 2026. This note supports the continuation combining acquired
cubic blocks with the acquired symmetric low-rank/sparse quadratic
representation. The asymptotic phase engine remains conditional on the
pinned OpenAI manuscript. The algebraic barriers below are unconditional
apart from their explicitly cited established slice-rank theorem.

## 1. Direct prior art: recovering hidden blocks is already established

Bläser, Gullans, Hangleiter, Liu and Qiao, *Verifiable quantum advantage
based on polynomials with planted structures*, arXiv:2609.39918v1,
Appendix A, explicitly recovers a hidden block-diagonal trilinear tensor
through its centroid and idempotents. Section 1.6 says this defeats the
hidden product/block cubic forrelation proposal discussed there. The
appendix allows independent transformations in the three tensor modes;
the symmetric cubic application requires the same-coordinate version.

Primary source, Appendix A and relevant introduction actually read:
<https://arxiv.org/html/2609.39918v1>.

Huang, Lu, Ye and Zhang, *Centers of Multilinear Forms and Applications*,
arXiv:2110.07915, establishes commutativity for nondegenerate multilinear
forms and the center's connection to direct-sum decompositions. This is
the earlier structural ancestry, not a new component of the present work.
<https://arxiv.org/abs/2110.07915>.

Consequently the defensible new target is a compiler that first acquires
the hidden nonlinear coordinates and then handles unknown, globally
coupled quadratic interactions which obstruct multiplication of block
counts. A theorem for independently countable hidden blocks alone would
repackage a prior solution. Sparse-plus-small-rank quadratic coupling can
be dense and have linear cut rank; preserving its acquisition guarantee
under the ambiguity in the recovered block coordinates is the relevant
additional requirement.

The same Bläser et al. paper evaluates a cubic with an h-dimensional
independent space in polynomial space and O(2^(n-h) poly(n)) time by
enumerating a complementary affine coordinate set and doing quadratic
Gauss sums. Its planted-space recovery algorithm has a distributional
promise. A raw direct sum of disjoint cubic triples already provides an
independent space of dimension 2n/3 after the blocks are recovered, even
with an arbitrary quadratic perturbation. Thus 2^(n/3) poly(n), not 2^n,
is an essential equally informed comparator for that family.

## 2. Exact barrier to every affine quadratic-leaf partition

Let n=3t and

    p(x) = sum_{j=0}^{t-1} x_{3j} x_{3j+1} x_{3j+2} + q(x),

where q has degree at most two over F_2. Arbitrary invertible affine
changes of all n coordinates are permitted. Let T be p's third additive
derivative, a constant alternating trilinear form.

**Proposition.** Every affine subspace on which p restricts to a
polynomial of degree at most two has dimension at most 2n/3. This bound
is attained. Every cover, and therefore every partition, of F_2^n by
such affine subspaces has at least 2^(n/3) members.

**Proof.** The tensor T is the direct sum of t three-dimensional volume
forms. A volume tensor is the Levi-Civita tensor (minus equals plus in
characteristic two). It has ordinary slice rank three. Gowers's direct
sum theorem therefore gives slice_rank(T)=3t=n. The cited paper both
proves direct-sum additivity (Theorem 2) and explicitly discusses the
Levi-Civita tensor and its direct sums on pages 2–3.

If a+W is an affine subspace on which p has degree at most two, then
T restricted to W×W×W is zero. Write c=codim(W). Choose a basis of W
and extend it to V=F_2^n. Every nonzero coefficient of T has at least
one coordinate among the c complement directions. Assign each such
coefficient to its first complement mode. This expresses T using at
most c slices in each of its three modes, so slice_rank(T) <= 3c.
Consequently c>=n/3. The direct sum of the first two coordinate axes
in every triple attains dimension 2n/3. Neither adding q nor affine
scrambling changes this argument. Finally every allowed affine leaf
has at most 2^(2n/3) points. A cover of 2^n points needs at least
2^(n/3) leaves. QED.

Primary proof dependency:
W. T. Gowers, *The slice rank of a direct sum*, arXiv:2105.08394v2,
Theorem 2 and the following Levi-Civita example, pages 2–3:
<https://arxiv.org/pdf/2105.08394>.

This includes adaptive choice of the affine leaf spaces: choosing a
different coordinate system at each branch does not evade the counting
argument. It is not a lower bound on all algorithms, weighted signed
decompositions, tensor contractions, or the replacement-form method.
For q=0 the product structure makes counting trivial despite the leaf
barrier. An expander sparse perturbation together with the dense
low-rank coupling is what makes the parent's stronger family relevant.

## 3. Full stabilizer nullity is another distinct obstruction

For any Boolean cubic p, consider its normalized phase state

    |p> = 2^(-n/2) sum_x (-1)^p(x) |x>.

**Proposition.** If the third polar tensor of p has zero radical, this
state has no nonidentity Pauli stabilizer, and its stabilizer nullity is n.

**Proof.** If X^a Z^b stabilizes the state up to a scalar phase, then
p(x+a)+p(x)+b·x is constant. Applying two additive derivatives gives
T(a,u,v)=0 for every u,v. Zero radical implies a=0. Full support then
forces b=0. The signed identity is the only remaining possibility. QED.

In particular this holds for the disjoint-triple family, all its affine
disguises, and every quadratic perturbation. If a state can be written
as a Clifford image of |phi_k> tensor |0>^(n-k), the dormant factors
provide at least n-k independent Pauli stabilizers. Hence the family
requires k=n in every such exact representation.

Clifft, Chase and Labib, arXiv:2604.27058v2, uses exactly this kind of
Clifford frame plus active virtual state vector. Its exponential cost
is controlled by the peak active dimension, which can be small in
measured near-Clifford workloads but cannot be sublinear for the
unmeasured phase states above. This is a comparison of representation
parameters, not an executed runtime comparison or a lower bound against
stabilizer-rank methods.
<https://arxiv.org/html/2604.27058v2>.

## 4. Another comparator: mixed rank-width/stabilizer methods

De Colnet, Geerts, Hai, Laarman, Lee and Pérez,
*Quadratic Sums-of-Powers for Fixed-Parameter Tractable Quantum-Circuit
Simulation*, arXiv:2605.29944v2, gives an exact amplitude dynamic program
using O(4^k poly(n)) arithmetic operations on a supplied rank
decomposition of width k. Its stabilizer-rank optimization chooses
between discharging local magic and paying cut ranks; some mixed
families are polynomial even though each separate parameter is large.

This result should be considered whenever claiming a benefit merely
from combining locally simple nonlinear phases and low-rank interfaces.
The present dense low-rank-plus-expander family has a different source
of advantage: globally small rank does not prevent sparse expander
errors from having linear cut rank at balanced original-coordinate cuts.
No assertion is made here about the best rank-width after arbitrary
nonlocal circuit rewriting.

Primary abstract, formulation, and stated exact bounds read:
<https://arxiv.org/html/2605.29944v2>.

## 5. Coordinate stability and a necessary lower-degree correction

Suppose in one hidden block basis the quadratic polar matrix is

    B = off(D) + S,   D=D^T, rank(D)<=r,   e(S)<=M,

where blocks have size at most beta. Any two decompositions into the
same primitive nondegenerate cubic components differ by blockwise
invertible transformations and a permutation of blocks. Let T be such
a transformation, after matching the block order.

The polar matrix of q_B(Ty) is

    T^T B T = T^T D T + T^T diag(D) T + T^T S T.

The first term has rank at most r. The second is block diagonal and
has at most sum_j binom(beta_j,2) <= n(beta-1)/2 off-diagonal entries.
Each original sparse edge contributes at most beta^2 new unordered
pairs, so the last term has at most beta^2 M edges. Cancellations can
only reduce these counts. Cubic local tables and translations also
contribute only block-local lower-degree terms in a blockwise change.

Thus a safe ordinary matrix-acquisition budget is

    M* <= beta^2 M + O(n beta).

One must not delete arbitrary within-block quadratic entries before
low-rank acquisition: deleting those entries can change the rank by
Theta(n). A free block-diagonal completion procedure could improve
this bookkeeping, but the scalar-diagonal Kogan argument does not
automatically generalize to arbitrary blocks. In F_2 a nonzero scalar
equals one; an invertible matrix block need not equal any fixed identity.

Also the full Boolean ANF must be transformed. Cubic monomials under
linear substitution generate lower-degree terms after x_i^2=x_i.
Transforming only the raw quadratic coefficient matrix is invalid.

### A row-type bound is not a block-coordinate invariant

Rank survives the ambiguity in primitive block bases. A small number
of distinct rows need not. Here is an explicit family with three-bit
blocks. For each pair 1<=i<j<=c, put one block with row labels
(e_i,e_j,0) in F_2^c. Let U collect these labels and D=U U^T. There are
n=3 binom(c,2) coordinates, rank(D)=c, and exactly c+1 distinct rows.
Within each block replace the first coordinate direction by the sum
of the first and second. The new labels are (e_i+e_j,e_j,0). The
congruent matrix has the same rank c but now binom(c,2)+c distinct
rows, which is Theta(n). The three-variable volume tensor is
preserved by this invertible within-block change.

Thus even c=Theta(sqrt(n)) can become linearly many row types under
the allowable recovered-basis ambiguity. Any row-type compiler should
be used with an a posteriori observed budget or a separately proved
coordinate-stability guarantee; c=o(n) in an unspecified hidden basis
does not suffice. In general a crude safe bound is the number of
sums of at most beta old row types.

## 6. Executions

`hidden_cubic_coordinate_checks.py` executed 36 block-coordinate
stability identities, with rank preservation and the edge-count bound;
all 36 had a nonzero diagonal-induced local correction. It executed
36 dense affine full-ANF roundtrips and nine exact count comparisons.
Transforming only the quadratic coefficients failed in every one of
the 36 roundtrips; ten raw quadratic coefficient matrices had full
rank even though the latent polynomial had no quadratic terms.
The same program checked the row-type counterfamily for c=4,8,16,
including a 360-coordinate example with 17 original row types and
136 transformed row types, while rank stayed 16.

`independent_space_barrier_checks.py` exhaustively enumerated all
subspaces at the first forbidden dimension: one for n=3, 63 for n=6,
and 43,435 for n=9. None was independent. Each dimension 2n/3 witness
was also checked. These finite checks accompany, rather than replace,
the all-dimension slice-rank proof.

The same validator tested nine phase states on n=3,6,9 with zero or
random dense quadratic perturbations. It exhausted all 1,752 possible
X-shifts across the fixtures and derived the unique candidate Z-mask
for each affine derivative; only the identity survived in every case.

No asymptotic replacement-form counter was executed here, and no
practical speed or historical first-priority claim is established.
