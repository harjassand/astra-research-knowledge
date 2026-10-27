# Fixed-degree nonlinear blocks with acquired quadratic response orbits

This extends the root cubic construction to every fixed degree d>=3. It
uses established multilinear centroid decomposition, the root's proved
orbit-clustering representation lemma, and the same conditional local-phase
theorem. It is not a generic dense polynomial solver or a new centroid
algorithm.

## Theorem

The input is an explicit Boolean ANF p on n independent variables, of degree
at most a fixed d>=3. Suppose an unknown invertible affine change x=A z+a
makes

    p(Az+a) = sum_j F_j(z[V_j]) + q_B(z),

where the V_j are the primitive components of the radical-free top
d-linear additive derivative, each has size b in the uniform case, and
each F_j has degree at most d. No coordinates, partition or local functions
are supplied. Away from the diagonal blocks, suppose the quadratic polar
matrix has the form

    B_ij = L_i K_(tau(i),tau(j)) L_j^T + S_ij,

where L_i is invertible b by b, tau has at most c types, K is symmetric,
and E=sum_(i<j) rank(S_ij). The matrices, types, gauges, errors and error
locations are not supplied.

The compiler produces an exact invertible coordinate map, an explicit
block-local degree-at-most-d foreground, a symmetric matrix C of rank at
most bc, and an alternating exact residual S' satisfying

    transformed quadratic polar = off(C) + S',
    unordered scalar edges in S' <= 15 b^2 (2E+n).

It checks that all nonquadratic terms are block-local, and rejects when
this structural requirement fails. Its identities remain exact for every
accepted input; the witness only guarantees the complexity parameters.

Top-polar acquisition is deterministic polynomial time and space for fixed
d. Orbit acquisition takes 2^(b^2) poly(n) time and polynomial space.
The explicit input has at most sum_(j=0)^d binom(n,j) binary ANF coefficients,
or a sparse term-list encoding. All full-ANF substitutions have polynomial
cost in this description for fixed d. The algorithm does not acquire the
representation by evaluating the 2^n-point truth table.

The foreground has O_d(n b^(d-1)) monomials, each of locality at most d.
Conditional on the root local-phase theorem, exact summation has cost

    poly_d(L+n) [ 2^(b^2) poly(n)
                 + 2^(bc + F_d(n, O_d(n b^(d-1)+b^2(E+n)))) ],

with polynomial space. Here F_d is the guarded local-phase exponent in
the root manuscript; F_d(n,u)=o(n) when log(2+u/n)=o(log n). Thus

    b=n^(o(1)),  bc=o(n),  E=n^(1+o(1))

suffices for original-input subexponential time. The exact zero count is
(2^n+sum_x(-1)^p(x))/2. The acquired affine bijection preserves all n
independent inputs. The root refinement reconstruction proves the required
exact Gaussian-integer arithmetic and power-of-two divisions.

## Proof of primitive coordinate acquisition

Let T be the d-fold additive derivative of p. It is a symmetric alternating
d-linear tensor. On distinct indices its coefficient equals that of the
corresponding degree-d ANF monomial, so it is obtained directly from the
explicit input. Compute the kernel of the contraction map

    v -> T(v, -, ..., -)

by binary linear algebra. This theorem rejects if that radical is nonzero.
The center consists of matrices H satisfying

    T(Hv_1,v_2,...,v_d) = T(v_1,Hv_2,...,v_d)
                       = ... = T(v_1,...,Hv_d).

These are O_d(n^d) homogeneous binary linear equations in n^2 unknowns.
Symmetry lets the implementation enforce the first two slots for all
indices and unordered tails, which enforces every pair of slots.

Commutativity uses three slots. If H,J are in the center, then

    T(HJx,y,z,...) = T(Jx,Hy,z,...)
                   = T(x,Hy,Jz,...)
                   = T(Hx,y,Jz,...)
                   = T(JHx,y,z,...).

Zero radical implies HJ=JH. Products, sums, and the identity stay in the
center. It is therefore a commutative binary algebra.

In characteristic two the map H->H^2-H is linear on a commutative algebra.
Its kernel is exactly the vector space of central idempotents. Compute a
basis e_1,...,e_s of this kernel. Starting from I, refine each current
projector P into Pe_i and P(I-e_i), discarding zero terms. The projectors
commute, stay idempotent, remain pairwise orthogonal, and sum to I.
The final images cannot split further: every basis idempotent acts as zero
or identity on each image, so every idempotent does so.

An idempotent in the center splits T as the direct sum of its image and
kernel. Conversely, the projection onto a direct summand belongs to the
center. Thus these images are exactly the primitive tensor components.
Choosing bases gives the coordinate change by deterministic polynomial
linear algebra. This is the established center/idempotent mechanism from
the multilinear-form and hidden-trilinear prior work identified in
HIDDEN_CUBIC_COMPARATORS.md.

## Proof of lower-degree and quadratic compatibility

Transform the full Boolean ANF. Check every monomial of degrees 3,...,d:
all its variables must belong to one primitive block. This check is
essential: top-degree direct-sum structure does not imply locality of all
lower nonlinear degrees. A crossed cubic below a quartic top form is a
concrete counterexample.

Any acquired primitive basis differs from a hidden primitive basis by a
permutation and independent invertible maps within blocks. Translations
also decompose into block translations. The F_j therefore stay block-local
and of degree at most d. Their new lower-degree terms stay inside their
blocks.

Off the diagonal blocks, the quadratic matrix transforms by invertible
left and right gauges. This preserves each rank(S_ij) and absorbs the basis
ambiguity into L_i. Arbitrary within-block corrections contribute at most
n directed rank error. The root orbit lemma therefore applies with hidden
error at most 2E+n, yielding rank bc and at most 15b^2(2E+n) residual edges.

There are O_d(b^d) possible ANF monomials per block and n/b blocks. Hence
the foreground has O_d(n b^(d-1)) fixed-locality monomials. Preserve S'
exactly. The root symmetric quadratic refinement and streamed Walsh
expansion replace C by at most 2^(bc) weighted local-phase sums with
additional unary factors. This proves the stated count and cost.

## Unequal blocks and budget selection

Rows of different sizes can be clustered separately. Rectangular column
blocks retain sum-rank isometry. With c_b types at size b and beta=max b,
the output rank is at most sum_b b c_b, the residual bound is
15 beta^2(2E+n), and the foreground has O_d(n beta^(d-1)) terms. The
sufficient subexponential regime is beta=n^(o(1)), sum_b b c_b=o(n),
E=n^(1+o(1)). The validator below only implements uniform blocks.

For uniform blocks a supplied c is unnecessary: compute distances once,
run polynomial local search for each possible c, and select the exact
certificate with the best explicitly computed counting bound. This adds
a polynomial factor without evaluating every candidate phase sum. For
unequal blocks, naive enumeration of all budget tuples would be excessive;
the root subsequently implemented a weighted budget dynamic program to
choose among the size-wise certificates. That additional implementation
is maintained in the root files, not duplicated here.

## Executed checks

`fixed_degree_orbit_checks.py` implements the generic top-polar equations,
radical test, center, linear idempotent kernel, primitive splitting,
full-ANF change, and crossed-lower-degree rejection. It imports the root
orbit acquisition and exact finite reconstruction.

Five densely affine-disguised fixtures were executed: degrees 4,4,4,5,6
on 8,8,12,10,12 variables. All 9,728 pointwise coordinate identities and
all five original/latent/acquired exact sums agreed. The three degree-four
fixtures executed complete orbit acquisition and Gaussian-Walsh
reconstruction, yielding -12, 12, -40. The degree-five/six fixtures tested
primitive acquisition, locality and exact count preservation without their
more costly GL enumeration. A quartic-top instance with a crossed cubic
lower term correctly rejected.

Results are saved in `fixed_degree_orbit_results.json`. The finite sum
backend is exhaustive. No asymptotic replacement-form engine was executed,
and no practical speed claim is made.
