# Exact tests of three Gaussian reconstruction routes

27 October 2026. These are unconditional algebraic statements about specified
reconstruction architectures. They do **not** prove that dense quadratic phases
with local nonlinear perturbations lack subexponential algorithms.

The unresolved target remains

\[
Z=\sum_{x\in\{0,1\}^n}(-1)^{q_B(x)}\prod_{j=1}^m(-1)^{p_j(x)},
\]

with arbitrary raw alternating binary matrix \(B\), fixed locality for every
\(p_j\), and \(m=n^{1+o(1)}\). Pure quadratic sums are easy; the existing local
phase compiler is fast without arbitrary dense \(B\). None of the three repairs
examined below closes that gap.

## 1. Moving the replacement construction to finite fields loses linear reconstruction

The rational source construction gains its power from two simultaneous facts:
replacement factors separate at nonzero interpolation nodes, and their total sum
is a bounded-degree polynomial in the interpolation parameter. Finite-field
linear replacements would preserve binary Gaussian phases, but additive
characters do not inherit the second property.

Here is a precise obstruction, including arbitrary per-node observations of
Hasse jets, not merely the character value at the node.

**Theorem.** Let \(F=\mathbb F_{2^e}\), \(D\ge1\), and write
\(p_c(T)=\sum_{i=0}^D c_iT^i\) for \(c\in F^{D+1}\). Put
\(\psi(a)=(-1)^{\operatorname{Tr}_{F/\mathbb F_2}(a)}\). For every nonzero
\(t\in F\), choose an integer \(1\le J_t\le D\), and let

\[
\mathcal J_t(c)=(p_c(t),p_c^{[1]}(t),\ldots,p_c^{[J_t-1]}(t)),
\]

where brackets denote Hasse derivatives. There are no complex-valued functions
\(F_t:F^{J_t}\to\mathbb C\) for which

\[
\psi(p_c(0))=\sum_{t\ne0}F_t(\mathcal J_t(c))
\quad\text{for every }c\in F^{D+1}.
\]

Any subset of nonzero nodes is also covered by the assertion.

**Proof.** For each fixed node \(t\), the polynomial
\((T-t)^{J_t}\) lies in the kernel of \(\mathcal J_t\), but its value at zero
is nonzero. Multiplying it by a field scalar gives an element of this kernel
whose value at zero has absolute trace one. Translation by that coefficient
vector pairs the elements of every jet fiber with opposite values of
\(\psi(p_c(0))\). Consequently, for every function \(F_t\),

\[
\sum_c\psi(p_c(0))F_t(\mathcal J_t(c))=0.
\]

Multiplying the proposed representation by \(\psi(p_c(0))\) and summing over
\(c\) would therefore give \(|F|^{D+1}=0\), a contradiction. \(\square\)

Equivalently, the characters of the coefficient space form an orthogonal basis.
The target character lies outside the character subspace of every incomplete
nonzero-node jet. Taking an arbitrary linear combination of these subspaces does
not manufacture that missing character.

**An indistinguishable-pair formulation.** Let the two coefficient populations be

\[
C_\epsilon=\{c:\operatorname{Tr}(c_0)=\epsilon\},\qquad \epsilon\in\{0,1\}.
\]

Each has size \(|F|^{D+1}/2\). At every permitted node and jet length, their
complete jet histograms agree, so they agree for the sum of **any** function of
that node's jet. Nevertheless their target character sums are respectively
\(+|F|^{D+1}/2\) and \(-|F|^{D+1}/2\). These populations have affine
parametrizations by \(e(D+1)-1\) independent Boolean bits; the example does not
require an arbitrary input table.

This rules out a direct finite-field replacement of source Proposition 3.4's
linear Hermite reconstruction. It does not rule out joint observations coupling
several nodes. Such joint observations are exactly an additional task: summing
each node separately loses their correlations. With all \(D+1\) jets at one
node, one can recover the whole polynomial, but the theorem deliberately makes
no claim in that full-information regime.

Nor does this theorem rule out a carefully costed p-adic lift. A p-adic lift must
provide a new bounded representation and account for its precision and
dimension; finite-field phase preservation alone does not establish one.

### Sharp threshold for joint observations

The same argument proves a stronger and sharp statement. An observation may be
an arbitrary joint function of jets at several distinct nonzero nodes. If its
total number of Hasse coordinates is
\(J=\sum_{t\in A}J_t\le D\), the polynomial

\[
\prod_{t\in A}(T-t)^{J_t}
\]

has degree at most \(D\), lies in that joint jet kernel, and has nonzero value
at zero. Scalar multiplication again supplies a kernel translation that flips
the target character. Therefore every such deficient joint observation has
zero correlation with the target character. An arbitrary linear combination
of deficient joint observations, even with different node sets and jet lengths,
cannot recover the target. The two populations \(C_0,C_1\) have identical full
joint jet histograms for every one of them.

Conversely, any joint jet specification at distinct nodes with total length
\(D+1\) determines a degree-at-most-\(D\) polynomial uniquely, by Hermite
interpolation over the field. Thus \(D+1\) is the exact threshold for this
observation model. A proposed finite-field repair has to compute at least one
correlation at that threshold; simply collecting more observations below it
does not suffice. This is an information statement about the stated oracle
model, not a bound on algorithms that inspect and use the raw input in other
ways.

## 2. Groupwise Fourier transformation preserves the dense Gaussian interface

Let \(B\) be a nonsingular alternating \(n\times n\) binary matrix, with
\(n\) even, and define \(q_B(x)=\sum_{i<j}B_{ij}x_ix_j\). Set

\[
G_B(a)=\sum_x(-1)^{q_B(x)+a^Tx},\qquad
\gamma_B=G_B(0)\in\{\pm2^{n/2}\}.
\]

Completing the square with \(y=B^{-1}a\) gives

\[
G_B(a)=\gamma_B(-1)^{q_B(B^{-1}a)}.
\]

The quadratic function \(a\mapsto q_B(B^{-1}a)\) has polar matrix \(B^{-1}\).
It may have unary terms when written in a standard upper-triangular convention;
the displayed expression retains them automatically.

For a coordinate partition \([n]=\bigsqcup_g S_g\), let \(f_g\) be arbitrary
functions on the Boolean assignments to \(S_g\), and let
\(\widehat f_g(a_g)=\sum_{x_g}f_g(x_g)(-1)^{a_g^Tx_g}\). Exact Fourier
inversion gives

\[
\sum_x(-1)^{q_B(x)}\prod_g f_g(x_g)
=2^{-n}\gamma_B\sum_a(-1)^{q_B(B^{-1}a)}
\prod_g\widehat f_g(a_g).
\]

The local tables can be transformed cheaply when each group is small. The
remaining sum, however, has precisely the same kind of dense Gaussian coupling.
Indeed, for every coordinate cut \(S\sqcup T=[n]\),

\[
\operatorname{rank}_{\mathbb F_2}(B^{-1})_{S,T}
=\operatorname{rank}_{\mathbb F_2}B_{S,T}.
\]

One direct proof compares kernels. For a vector \(y\) supported on \(T\),
\((B^{-1}y)_S=0\) exactly when \(z=B^{-1}y\) is supported on \(T\) and
\(B_{S,T}z_T=0\). The map \(z\mapsto Bz\) is a bijection between these two
kernels, which therefore have equal dimensions. Both cross blocks have \(|T|\)
columns, giving equal ranks.

Consequently, groupwise Fourier transformation cannot reduce the cross-rank
cost of the universal separated-group interface. It moves the coupling from
\(B\) to \(B^{-1}\). This is a restricted failure of one proposed repair,
not a hardness result for the particular local functions.

## 3. Exact Gaussian moments do not permit sublinear perturbation order uniformly

For a set \(U\) of coordinates fixed to one, the Gaussian moment

\[
M_B(U)=\sum_{x:x_i=1\ (i\in U)}(-1)^{q_B(x)}
\]

is either zero or has absolute value
\(2^{n-|U|-\operatorname{rank}(B_{U^c,U^c})/2}\). The remaining unary terms
can make it zero; the formula for nonzero magnitude is exact.

For cubic monomials \(p_j(x)=x^{S_j}\), expand

\[
H(V)=\sum_x(-1)^{q_B(x)}\prod_j(1-2Vx^{S_j}).
\]

A selection of \(t\) factors contributes
\((-2)^tM_B(\bigcup S_j)\). Its 2-adic valuation, when nonzero, is at least

\[
t+\left\lceil\frac{\max(0,n-3t)}2\right\rceil.
\]

This bound need not grow with \(t\). There is a simple exact family in which
every high perturbation order remains necessary for exact reconstruction:
take \(n=3m\), independent triples \((a_j,b_j,c_j)\),
\(q_B=\sum_j a_jb_j\), and cubic factors \(a_jb_jc_j\). A single triple
gives

\[
\sum_{a,b,c}(-1)^{ab}(1-2Vabc)=4+2V.
\]

Hence

\[
H(V)=(4+2V)^m,\qquad [V^t]H(V)=\binom mt2^{2m-t},\qquad H(1)=6^m.
\]

The top coefficient has valuation exactly \(m\), and every nonempty omitted
tail is positive and smaller than \(2^{n+2}\). Thus truncating at any order
below \(m=\Theta(n)\) changes even the residue modulo the standard exact-count
precision \(2^{n+2}\). This family itself is easy by its visible block product;
it proves only that exact Gaussian evaluation of each moment does not justify
a general sublinear-order truncation.

## 4. A rank obstruction to polynomial deformation of the quadratic matrix

There is also a direct constraint on deforming the dense matrix itself while
retaining low polynomial degree.

**Lemma.** Let \(C(T)\) be an \(a\times a\) polynomial matrix over any field,
with entry degrees at most \(R\), and suppose \(\det C(0)\ne0\). At distinct
nonzero nodes \(t_1,\ldots,t_Q\), put \(k_j=\operatorname{rank}C(t_j)\).
Then

\[
\sum_{j=1}^Q(a-k_j)\le aR.
\]

**Proof.** Constant invertible row operations at node \(t_j\) make at least
\(a-k_j\) rows of \(C(t_j)\) zero. Every entry of these rows in the transformed
polynomial matrix is divisible by \(T-t_j\); multilinearity makes its
determinant divisible by \((T-t_j)^{a-k_j}\). Distinct-node divisibilities
multiply, while \(\deg\det C\le aR\) and the determinant is nonzero.
\(\square\)

For a fixed balanced cut with nonsingular original cross matrix, making every
deformed cross matrix have rank \(o(n)\) therefore requires
\(R/Q\ge1-o(1)\). This is incompatible with the vanishing degree-to-node ratio
needed by the source reconstruction. The lemma covers a **fixed** cut; it does
not by itself cover changing cuts together with low-rank shared-summary terms.

A weaker summary-free statement does allow the partition to change. Suppose
the original matrix has \(E\) nonzero off-diagonal unordered entries. Every
nonzero original entry is a nonzero polynomial and remains nonzero at at least
\(Q-R\) nodes. If at every node the deformed matrix is block diagonal with
blocks of size at most \(s\), then it has at most \(n(s-1)/2\) nonzero unordered
entries. Thus

\[
E(Q-R)\le Qn(s-1)/2.
\]

For \(E=\Theta(n^2)\) and \(s=o(n)\), this again forces
\(R/Q\ge1-o(1)\). A small-rank shared term can be dense, so this entry-count
argument must not be extended silently to the general summary architecture.

## Executed finite checks

The companion `gaussian_reconstruction_checks.py` uses exact integer and finite
field arithmetic. It checks the full finite-field jet histograms of the two
indistinguishable coefficient populations; complete Walsh transforms and all
coordinate cross-ranks for nonsingular Gaussian examples; exact weighted group
duality; Gaussian moment magnitudes; and all coefficients of the block
perturbation family. Its JSON is the direct output of execution. These are
mechanism checks, not practical performance measurements.

The executed run passed 57 complete single-node jet histogram equalities, 189
deficient joint-jet histogram equalities, 3 full-threshold injectivity checks,
4,850 character observations, 10,912 Gaussian Walsh entries, 10,832 cross-rank
equalities, 40 weighted group Fourier identities, 1,024 Gaussian moment checks,
and 15 exact failures of prematurely truncated perturbation tails.

## Primary sources consulted for alternatives

The underlying Gaussian duality and quadratic character calculus are classical;
no priority claim is made for them. The governing construction is OpenAI,
*The Exponential Time Hypothesis is False* (25 October 2026), Definition 3.1,
Lemma 3.2, Proposition 3.4 and Section 4, at the user's pinned commit:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf

For p-adic alternatives, Lauder and Wan, *Counting points on varieties over
finite fields of small characteristic*, especially Sections 4--6, explicitly
construct additive characters through splitting functions and compute traces of
finite precision operators. Their polynomial-time statement fixes the geometric
dimension; their displayed complexity has exponential dependence on a growing
number of variables. It does not already settle the present original-input
frontier:
https://library.slmath.org/books/Book44/files/18lauder.pdf

Sperber and Voight, *Computing zeta functions of nondegenerate hypersurfaces with
few monomials*, Theorems A and B, tracks monomial count, lattice volume, and a
cohomological matrix. Its stated algorithms impose nondegeneracy and include
dimension-dependent powers; Theorems A and B also state odd-characteristic
restrictions. They cannot be invoked as an uncharged Boolean Gaussian
reconstruction step:
https://jvoight.github.io/articles/sparse-dwork-073025.pdf

The first three failures leave a clear remaining requirement: a successful
generic Gaussian extension needs a way to preserve correlations among the
manufactured easier instances, or a different exact algebra whose representation
dimension and precision are both subexponential. Independent per-node Gaussian
answers and local Fourier transforms do not supply that requirement.
