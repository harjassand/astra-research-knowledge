# Independent substantive review: planar quartic PC/SOS-PC gap

Reviewer: independent_opening_6,2026-10-27, existing same model/context.
No producer/root verification module was imported.

**Decision: ACCEPTED at the stated mathematical scope.** No substantive
counterargument survived the primary-definition, all-degree, global-lift,
zero-increment, or35-dimensional perturbation checks. This is an internal
mathematical review, not a claim of world priority, external publication,
physical capability, or a solution of the planar Morrey problem.

The literal energy is

    F=u²+v²+3w²+(113/10)q²+4q(u-v),
    u=a²+c², v=b²+d², w=ab+cd, q=ad-bc.

The accepted conclusion is: F is globally polyconvex with a finite-valued
convex lift, has the displayed quantitative quasiconvex support, and fails
SOS polyconvexity under primary2604.11124v1 Definition2.5 for every
real polynomial selector of arbitrary finite degree. The same distinction
holds for all real homogeneous quartic perturbations in the closed
35-coefficient sup box of radius1/616000.

## 1. Governing primary definition

I read the live arXiv record and primaryv1 Definition2.5, Proposition2.3,
Theorem2.3 and Remark2.1:
[Fantuzzi–Henrion–Kružík–Murali–Weis](https://arxiv.org/html/2604.11124v1).
The record lists onlyv1, submitted13April2026.

Definition2.5 requires one polynomial supporting-minor map q(Y) and a
single residual SOS jointly in both matrices. It explicitly permits
arbitrarily large selector degree. The planar2-by-2 quartic case is
expressly open in Remark2.1. The reviewed result addresses that definition,
rather than only the previously known failure of an SOS-convex polynomial
lift. More permissive nonpolynomial/rational selectors or separately chosen
pointwise-in-base SOS decompositions are not excluded by this review.

Column-major versus row-major order is a harmless permutation of the four
entry minors. The determinant cofactor in the reviewed row-major convention
is(d,-c,-b,a), not the adjugate's row-major vector.

## 2. Every polynomial selector, not a fixed-degree SDP

Write a hypothetical selector as(V(A),k(A)). The jointly SOS residual

    H(B)-H(A)-V(A):(B-A)-k(A)(detB-detA)

vanishes when B=A. For each fixed A, its global nonnegativity and
differentiability force its B derivative there to vanish. Thus

    V(A)=DH(A)-k(A)cofA.

After the invertible linear change B=A+X, the only freedom is

    B_H(A,X)-k(A)detX.

For a homogeneous quartic H, the Bregman term has joint degree4.
If a highest homogeneous component k_j has j>2, choose A with k_j(A)neq0
and choose X with determinant of its sign. Joint scaling(tA,tX) then makes
the leading term -t^(j+2)k_j(A)detX negative for large t. If a lowest
component has j<2, the same choice makes the leading small-t term negative.
All variables range over all real matrices, so no determinant-domain
restriction obstructs these choices. Therefore k is homogeneous quadratic
or zero. This argument applies to arbitrary real coefficients.

The resulting residual is a homogeneous quartic. In a finite SOS, the
highest and lowest nonzero homogeneous square components cannot cancel
each other. Every summand is therefore homogeneous quadratic. At X=0,
their squared sum is identically0, forcing every summand to vanish there.
The pure A_iA_j monomials are absent, leaving exactly

    A_i X_j (16),       X_i X_j, i<=j (10).

All ten quadratic selector monomials A_iA_j, i<=j, are unrestricted.
Thus the26-feature moment dual is complete for Definition2.5, not just
one guessed degree or symmetry ansatz. Increasing selector degree cannot
escape the separator.

## 3. Positive support, cancellation, and a finite global lift

The positive certificate is an identity for |X|²P(A,X). Its strict Gram
margin and the feature norm imply, for Xneq0,

    P(A,X)>=|A|²|X|²/400+|X|⁴/1200.

Division is used only there. At X=0, P(A,0)=0 by its literal definition,
and the required inequality is0>=0. No SOS cancellation is asserted:
positivity after division does not make the unmultiplied P SOS.

Let kappa be the supplied quadratic and

    ell_A(B,t)=F(A)+(DF(A)-kappa(A)cofA):(B-A)
                         +kappa(A)(t-detA).

The exact determinant expansion gives ell_A(B,detB)<=F(B), with equality
at A=B. Hence G(B,t)=sup_A ell_A(B,t) is convex and equals F on the full
minor graph.

There is no hidden +infinity off that graph. For any(B,t), choose a real
matrix Y with detY=t-detB. The average of the two graph points
(B+Y,det(B+Y)) and(B-Y,det(B-Y)) is(B,t). Every affine ell_A at(B,t) is
therefore bounded above by the same finite number
[F(B+Y)+F(B-Y)]/2. A=0 gives the finite lower bound0.
Thus G is real-valued everywhere. This independently proves the finite
lift without needing a polynomial convex lift or a compact A search.

The alternative coercivity proof is also correct: P(A,-A)
=3F(A)-kappa(A)detA>=|A|⁴/300. In ell_A(B,t), all other A terms have
degree at most3, so its supremum is finite and attained.

For zero-boundary W1,4 or periodic potentials, the gradient mean and
determinant mean vanish. The determinant identity passes by strong W1,4
approximation, so integration of the global support gives the claimed
quantitative quasiconvex inequality. There is no finite-bandwidth,
small-amplitude, or tested-gradient restriction.

## 4. Independent literal exact algebra

independent_symbolic.py builds F, derivatives, determinant and Bregman
polynomials through SymPy exact algebra from the displayed formula. It
reads only the two JSON certificates, with SHA256:

* positive60 matrix:
  a7b53759b9ba5576a099ef36b9ffce96c266478a5fbc5594a8b156d5f1576e32;
* negative26 functional:
  768f5564a0e9ed66524d3d908626ec4f52f4a24634c4eb3daf50034314d32c19.

The replay independently passed:

* exact positive polynomial identity in all eight variables;
* all60 positive LDL pivots and full reconstruction of R-I/200;
* reconstruction of the negative moment matrix from the functional;
* all26 positive LDL pivots and full reconstruction;
* all ten unrestricted selector annihilators, exactly0;
* literal Bregman pairing -39/125000;
* all35 ordinary quartic monomial Bregmans and sensitivity69749/25000;
* full658-monomial coverage by products of the60 features;
* determinant/cofactor, Euler, and X=-A identities.

The negative implication uses a real PSD Gram S:
L(Z^T S Z)=tr(SM)>=0. Since M is positive definite and every quadratic
selector term is annihilated, the strict negative Bregman pairing is a
contradiction. It rules out real SOS coefficients, not only rational ones.

The replay took approximately0.53seconds; SYMBOLIC_RESULT.json contains the
actual receipt. Finite coefficient verification supplies the certificate
facts; Sections2–3 supply the all-degree and global quantifiers.

## 5. Full35-dimensional perturbation

A unit ordinary homogeneous quartic monomial has Bregman coefficient l1
norm2^4-1-4=11. Multiplication by |X|² gives norm44. Across35 independent
coefficients bounded by epsilon, the total bound is1540epsilon.

Every resulting A²X⁴,AX⁵,X⁶ monomial is a product of two60-feature
monomials. A chosen off-diagonal entry and its transpose receive half the
coefficient; a diagonal receives the whole coefficient. Different target
monomials cannot collide in one entry because one entry has one exponent
sum. Hence a symmetric Gram correction exists with entry l1 norm at most
1540epsilon, which bounds its operator norm.

At epsilon=1/616000, this is1/400. Since R-I/200 is positive definite,
the perturbed Gram remains strictly above I/400. Keeping the same kappa
gives the halved positive/QC constants for every real perturbation in
the closed box. No rotational symmetry is used.

The worst negative pairing is exactly bounded by

    -39/125000+(1/616000)*(69749/25000)
       =-4735051/15400000000 <0.

The same fixed moment matrix and all ten annihilators therefore exclude
every polynomial selector throughout that entire box. Uniform strict
margins also give an open neighborhood containing the closed box.
The claim is35-dimensional **homogeneous quartics** in coefficient sup norm,
not the full70-dimensional space of polynomials of degree at most4.

## 6. Hierarchy challenge and a useful strengthening

I separately whole-read the parent HIERARCHY_PROOF and governing
1904.00206v1 Thm1.1, Lemmas2.2–2.3 and the sphere step in Section4.
The source authors are Trung Hoa Dinh, Minh Toan Ho, and Cong Trinh Le.
[Primary source](https://arxiv.org/html/1904.00206v1).

Its conditional completeness statement passes:

* Global a|A|²|X|²+b|X|⁴ support, with a,b>0, homogenizes the affine
  A quadratic to a5-by-5 matrix bounded below by diag(aI,b) on the X sphere.
* The matrix module for both signs of1-|X|² is Archimedean. Scherer–Hol
  gives matrix SOS modulo that sphere ideal.
* Averaging a row f with f(-X)D, D=diag(-I4,1), and splitting with factors
  1/2 correctly preserves the averaged square sum. One row type has odd
  first four entries/even last; the other has reversed parity.
* Multiplying a reversed row by all four X_i preserves its square sum on
  the sphere and switches its parity.
* Odd k gives integral nonnegative powers when homogenizing the first
  entries to degree k and last entry to k+1.
* The resulting global square sum is
  |X|^(2k-2)P(A,X), so r=k-1. The identity extends polynomially to X=0.

This needs global strict support with a supplied quadratic selector.
It does not establish that all PC quartics have such a selector, cover
weak supports, or give a degree/bit/time bound.

RATIONAL_STRICT_COROLLARY.md proves an additional implementation fact:
for rational H with an existing strict real quadratic support, some level
has a rational quadratic selector and a **positive-definite** rational Gram.
The argument subtracts a small strict diagonal reserve, applies the same
weighted matrix proof, then uses density in a rational affine solution space.
This is a derived known-machinery corollary, not claimed a new hierarchy;
the parent has reported incorporating it into the pinned hierarchy snapshot.
No quantitative degree, bit, or search-time conclusion is added.
