# Algebra audit: acquired cubic blocks and quadratic response orbits

27 October 2026. The acquisition and exact identities below are unconditional.
The subexponential phase-counting consequence is conditional on the pinned
OpenAI manuscript and the previously established local phase compiler. The
centroid, metric local-search, and quadratic Gauss ingredients are prior
machinery, not newly claimed components.

## 1. Hidden model and the charged error quantity

Let the acquired primitive cubic blocks have dimensions b_a, with sum n and
maximum Delta. In some unknown block bases, suppose the off-block quadratic polar
matrix is

    B_(a,j) = L_a K_(tau(a),tau(j)) L_j^T + S_(a,j),    a != j,

where L_a is invertible of dimension b_a. Blocks sharing a hidden type have the
same dimension. The quotient K is symmetric; its total dimension is

    r = sum_d d*c_d,

where c_d is the hidden number of types of dimension d. The within-block
quadratic terms and local cubic polynomials are arbitrary. No labels, gauges,
quotient, corruption support, or type profile are supplied to the compiler.

Use the invariant error measure

    E = sum_(a<j) rank(S_(a,j)).

If the hidden corruption has M scalar off-diagonal edges, then E <= M. If it
occupies M_B nonzero block pairs, then E <= Delta*M_B. Define an ideal symmetric
full matrix using the quotient also on each diagonal block; its diagonal is
free. Replacing each actual diagonal block costs at most b_a in rank. Thus the
sum of row-block errors is bounded by

    T <= 2E+n.

This explicitly pays for arbitrary local quadratic terms.

## 2. The orbit metric is admissible

For two d-by-n row blocks X,Y, partitioned into d-by-b_j column blocks, put

    d_d(X,Y) = sum_j rank(X_j-Y_j),
    orbit_d([X],[Y]) = min_(G in GL_d(F2)) d_d(GX,Y).

The rank triangle inequality makes d_d a metric. Simultaneous invertible left
multiplication is an isometry. Minimizing over this finite isometry group is
therefore a metric on the orbits, or a pseudometric on raw rows. Symmetry uses
G inverse; the triangle inequality composes two gauges. Distance zero means
exactly equality of orbits, including zero and rank-deficient row blocks.

Independent invertible right transformations on the column blocks are also
isometries, because rank((X_j-Y_j)H_j)=rank(X_j-Y_j). This is why the compiler
uses rank distance before it knows the gauges. Scalar Hamming distance does
not have this invariance.

For hidden type t, the row vector with column blocks
K_(t,tau(j)) L_j^T is a common center after left normalization. The total
distance to these ideal centers is at most T. The centers need not be observed
rows. Within each hidden cluster, choose the observed row closest to its ideal
center. The triangle inequality shows that the total distance to this observed
center is at most twice the original cluster cost. Hence the optimum using
c_d observed centers in dimension d is at most 2T_d, where sum_d T_d <= T.

An exact one-swap local optimum has cost at most five times the metric k-median
optimum, by Arya et al. The compiler therefore obtains, separately for each
dimension and center budget,

    kappa_d(c_d) <= 10T_d

whenever c_d equals a promised profile's budget. Zero-distance duplicates do
not invalidate the theorem; one can quotient by zero-distance classes or use
its same triangle-inequality proof. Unoccupied facilities may be discarded
after local search, leaving at most c_d occupied classes.

Each distance is an integer between zero and n. A strictly improving swap
lowers the objective by at least one, and that objective is at most N_d*n.
Thus exact local search uses polynomially many swaps. All pairwise distances
can be found in 2^{O(Delta^2)} poly(n) time, by enumerating GL_d, and polynomial
space by streaming its elements. For fixed Delta this preprocessing is polynomial.

Primary source for the five-approximation component: Arya, Garg, Khandekar,
Meyerson, Munagala and Pandit, Local Search Heuristics for k-Median and Facility
Location Problems, SIAM J. Comput. 33 (2004), 544--562,
https://doi.org/10.1137/S0097539702416402 . An author-hosted version is
https://theory.stanford.edu/~kamesh/lsearch.pdf . This is an established
ingredient; the present construction concerns its exact representation
interface, not a new local-search approximation theorem.

## 3. The unknown heterogeneous type profile is acquired by dynamic programming

For every present dimension d, run local search for c=1,...,N_d on the cached
orbit distance matrix and retain its objective kappa_d(c) and a reconstructible
center witness. For each rank budget R, compute

    F(R) = min sum_d kappa_d(c_d),
           subject to sum_d d*c_d <= R and 1 <= c_d <= N_d.

This is an ordinary integer resource-allocation dynamic program. After adding
dimension d, its transition for used budget s considers the options c with
d*c<=s and adds kappa_d(c). Minimizing over s<=R gives the budget-at-most
version. Infeasible states are left infeasible. The lower bound one is imposed
only for dimensions that occur; there is no center choice for absent sizes.

If an unknown promised profile has weighted rank at most R, it is a feasible
choice. Consequently the chosen profile satisfies

    kappa_R = F(R) <= 10 sum_d T_d <= 10(2E+n).

The DP neither needs nor estimates E. It uses computed exact metric objectives.
All objectives are nonnegative integers of size O(log n) bits, bounded by n^2.
There are at most O(n^2) states and backpointers. The straightforward number of
candidate transitions is O(n*sum_d N_d)=O(n^2). Storing all distance matrices
is polynomial; even keeping one d-by-d aligning gauge for each ordered pair
uses sum_d d^2 N_d^2 <= n^2 binary entries, apart from indexing overhead.
Storing all local-center lists is also polynomial.

After reconstructing one profile for R, align and round as below. The budget R
itself need not be supplied: inspect all R up to n, retain the actual valid
certificate with the smallest explicit counting bound, then perform the count.
This adds only a polynomial factor and preserves polynomial workspace. There
is no need to enumerate exponentially many type profiles.

## 4. Simultaneous alignment and the exact 3A rounding lemma

Let s(a) be the selected observed center for row block a, and G_a a minimizing
left gauge. Apply the same gauge system on both sides:

    B' = G B G^T,        G = blockdiag(G_a).

Define C_(a,j)=B_(s(a),j) G_j^T. Within every acquired row class, C is row
constant coordinate by coordinate. The common right transformation is an
isometry, so sum_(a,j) rank(B'_(a,j)-C_(a,j)) = kappa_R. A nonzero rectangular
block contains at most Delta^2 nonzero entries and has rank at least one. Therefore

    A := Hamming(B',C) <= Delta^2 kappa_R.

The following proof does not assume C is symmetric. Treat scalar coordinates
having the same acquired block class and within-block index as one coordinate
class. In every row, replace C's entries on each column-coordinate class by
their majority, with a consistent tie rule. Call the result P(C). This is a
minimum-Hamming projection onto column-class-constant matrices. Since C was
row-class constant, P(C) is row-class constant as well.

Now C^T is column-class constant, and B' is symmetric. Hence

    Hamming(C,P(C)) <= Hamming(C,C^T)
                      <= Hamming(C,B')+Hamming(B',C^T) = 2A.

Thus Hamming(B',P(C)) <= 3A. Finally round B' itself by majority on each pair
of coordinate classes; call this D'. Symmetry of B' and consistent ties make
D' symmetric. This is a best blockconstant approximation, even when compared
with nonsymmetric blockconstant candidates. It follows that

    Hamming(B',D') <= Hamming(B',P(C)) <= 3A.

The diagonal of D' is free. A one there must not be erased prematurely: the
exact Z4 quadratic refinement handles it, and setting it to zero can destroy
the low-rank factorization.

Let H be the coordinate-class incidence matrix and K' the rounded quotient.
Then D'=H K' H^T and rank(D') <= sum_d d*c_d <= R. The exact residual is
S'=B'-off(D'). Off-diagonal errors occur twice in directed Hamming distance,
and consequently

    edges(S') <= (3/2)A <= 15 Delta^2(2E+n).

The compiler constructs and validates every matrix, gauge, label, and residual
entry. There is no rank-times-error product in this acquisition guarantee.

## 5. Compatibility with raw cubic acquisition and exact observables

For a radical-free third derivative, the established centroid construction
finds its primitive cubic direct-sum subspaces from the raw coefficients. An
unknown global invertible affine input change preserves these intrinsic
subspaces up to permutation and independent block bases. Translation of a
cubic summand adds only lower-degree terms inside its block; translation of a
cross-block quadratic adds only unary and constant terms.

After choosing the orbit gauges, substitute the entire Boolean polynomial.
Congruencing its quadratic matrix alone misses lower-degree terms created by
transforming a cubic. The tested root implementation performs full ANF
substitution, subtracts the congruenced quadratic polynomial, and checks that
the foreground remains block local. Its use of gauge_rows as the substitution
column list implements x=G^T y, exactly matching G B G^T.

The existing exact quadratic refinement and Fourier reconstruction stream at
most 2^R characters. The remaining phase consists of the actual sparse
quadratic residual, local transformed cubic terms, and unary fourth roots of
unity. The local foreground has at most O(sum_a b_a^3) <= O(n Delta^2) monomials.
Inner cyclotomic coordinates must be reconstructed exactly before division by
the Fourier normalization. No extra independent inputs or coordinate deletions
are introduced by this compiler.

For an explicit certificate with actual rank r', residual edge count M', and
local foreground monomial count m_F, the total bound is

    2^{O(Delta^2)} poly(L+n) + poly(L+n) 2^{r' + F_phase(n,M'+m_F+O(n))}.

The implementation may use the quotient dimension R rather than r' without
invalidating its bound. The worst-case model guarantee gives M' and m_F at
most O(Delta^2(E+n)). Thus Delta=n^{o(1)}, R=o(n), and E<=n^{1+o(1)} suffice for
subexponential time in the original input count n and polynomial space. A more
input-sensitive certificate may succeed outside these sufficient conditions.

## 6. What is and is not separated from the previous guarantee

For fixed Delta, the model guarantee no longer requires R*E=o(n^2). For example,
R on the order of n/loglog n and E on the order of n*log n are allowed, while
their product is not o(n^2). This is a strict improvement of the charged
guarantee on this hidden-orbit family over plugging those same parameters into
the previous general low-rank-plus-sparse acquisition theorem.

It is not yet a proof that every such instance lacks another lower-rank or
lower-error certificate satisfying the earlier theorem. Excluding all
alternative certificates requires a separate rigidity argument. The orbit-type
model is also more restrictive than an arbitrary low-rank matrix: rank r alone
allows exponentially many different row orbits. This family restriction is
explicit; the useful labels and gauges are nevertheless acquired from raw
data, not supplied as an extra oracle.

## Executed uniform-interface audit

The companion orbit_rounding_audit.py imports and exercises the actual root
implementation while independently generating unknown-gauge corrupted
quotient instances, computing optimal data-center subsets, and implementing
majority projection. It passed:

- 27 block-matrix compiler fixtures, 3,645 metric triangle checks and 693
  independent two-sided gauge isometries;
- 27 comparisons with exact optimal observed-center subsets;
- 50,248 majority-rounding and triangle-bound cases;
- 3 all-zero cases with unoccupied requested facilities;
- 3 raw globally affine-disguised cubic ANFs, 4,672 pointwise coordinate
  equalities, and 3 exact Gaussian-Walsh reconstructions.

These are exact finite checks; the asymptotic phase engine was not executed.
The heterogeneous implementation was then independently exercised by
heterogeneous_orbit_audit.py. Twelve generated mixed-size hidden-profile models
were compared against exact globally budgeted observed-medoid optima; another
model was checked at all four feasible budgets. Fourteen malformed inputs were
rejected. Two new raw affine-disguised ANFs acquired blocks [5,3,3] and [3,6,3].
All 6,144 pointwise coordinate identities and both exact Gaussian-Walsh
reconstructions passed, giving original signed sums -80 and 64. The respective
JSON files contain the complete executed outputs.

## 7. Mathematical audit of exact classification on the acquired summaries

Let the d columns of the acquired incidence matrix H be disjoint nonempty
coordinate classes A_1,...,A_d whose union is [n], so D'=H K H^T. Define

    s_a(y) = sum_(i in A_a) y_i mod 4.

The entire dense quadratic sign depends only on s. Indeed,

    q_off(D')(y)
       = sum_a K_aa binom(s_a,2)
         +sum_(a<b) K_ab (s_a mod 2)(s_b mod 2)  (mod 2).

The formula is independent of the representatives chosen for s_a modulo four:
binom(w+4,2)-binom(w,2)=4w+6 is even. Let h_K(s) be the sign of this quadratic
function. Put F(y)=(-1)^(foreground(y)+q_(S')(y)), including any constant term
in the foreground. Define the residual signed class mass

    H_res(s) = sum_(y:s(y)=s) F(y).

For each chi in (Z/4Z)^d, let

    T_chi = sum_y F(y) i^[sum_a chi_a sum_(j in A_a) y_j].

Character orthogonality gives the exact transform

    H_res(s) = 4^(-d) sum_chi i^(-chi dot s) T_chi.

The Fourier signs are therefore as written: a positive character in the inner
sum and a negative character in reconstruction. Each inner phase needs only
the existing local cubic/quadratic foreground plus unary order-four phases;
the dense quotient does not reappear as local factors.

The original label imbalance in summary class s is

    J(s) = # {y:s(y)=s,p(y)=0} - # {y:s(y)=s,p(y)=1}
         = h_K(s) H_res(s).

Its unsigned population is known independently:

    N(s) = product_a sum_(0<=w<=|A_a|, w=s_a mod 4) binom(|A_a|,w).

This factorization uses the disjoint partition property of the acquired
indicator columns. The d in this statement is the number of scalar coordinate
classes, not just rank(D'). A later compact low-rank basis need not have this
partition property and cannot be substituted silently in the population
formula.

The best Boolean classifier restricted to these summaries predicts zero when
J(s)>=0 and one when J(s)<0, with any convention on empty or tied classes.
Its exact minimum number of uniform-input mistakes is

    sum_s (N(s)-abs(H_res(s)))/2.

The summands are integers because H_res(s) has the same parity as N(s).
For any specified Boolean predictor h(s), its exact mistakes are

    sum_s [N(s)-(-1)^h(s) J(s)]/2.

Thus a single reconstructed table supports arbitrary subsequent predictors on
the same summaries. This is exact optimal classification *within the acquired
summary representation*, given the raw program/polynomial that defines the
labels. It is not global representation optimization, a PAC learning theorem,
or an assertion that examples alone suffice to acquire the representation.

For a polynomial-workspace implementation, stream the 4^d output summaries;
for each one recompute the 4^d inner character sums sequentially. The cost is
at most 2^(4d+F_phase(n,m)) poly(L+n), where m is the residual plus local
foreground size. This permits d=o(n). It writes 4^d output records; polynomial
workspace excludes this unavoidable streamed output. A finite implementation
that instead caches all Fourier values must state its additional 4^d storage.

Each T_chi is a Gaussian integer with O(n)-bit coordinates. After exact inner
reconstruction, the outer numerator has O(n+2d) bits and is divided exactly by
4^d. Its imaginary coordinate is zero. The mod-four binomial population
counts and their products have O(n) bits and are computable in polynomial time
per summary. No uncharged precision or division step is needed.

This section is a mathematical audit of the parent's proposed extension; its
executed learning checks, if any, belong to the parent's accompanying program.
