# Acquiring repeated quadratic fibers and replacing a field scan by eight moments

## Result and implementation boundary

Let q=2^d with 3 not dividing d, let b=2s+1>=5, and let A=F_q[t]/(t^e).
The contact compiler acquires its coefficient algebra, homogeneous cubic,
center, and compatible binary quotient quadratic from the original Boolean
description. This note supplies an additional polynomial-time residue
certificate. The certificate manufactures coordinates in which the residue
cubic is

    H_0=gamma sum_(i=1)^s [X_i^3+X_iY_i^2+Y_i^3
                          +Z(X_iY_i+a_iX_i^2+b_iY_i^2)] + tau Z^3,

where gamma is nonzero and every a_i,b_i belongs to F_2. The coordinates
and the decomposition into pairs are computed; they are not inputs.
Arbitrary higher nilpotent cubic coefficients are permitted. The quadratic
weight can have arbitrary binary rank and use the quotient A/t^h provided
3h<=e+1.

For this acquired class, exact counting is deterministic polynomial time
uniformly in the original n=bde input bits and explicit description size,
at every depth e. A conservative field-terminal cost is soft-O(d^31) time
and soft-O(d^20) storage, plus polynomial acquisition and integer arithmetic.
These large fixed exponents come from an established fixed-variable
point-count algorithm. They are a complexity theorem, not a speed claim.

Implemented and executed here: the complete extra residue acquisition,
exact coefficient identity checks, eight joint Gaussian states and their
moment reconstruction, an independent 49-moment reference reconstruction,
small-field moment-expansion oracles, and a raw
36-bit acquisition regression through the root compiler. The general
Lauder--Wan point-count backend is not implemented. The executable reference
terminal explicitly enumerates q field values and labels that cost. The
`moment_terminal_eight` interface requires a supplied exact moment backend and
never silently substitutes a field scan.

## 1. Acquire a contact chart and center its transverse critical point

Acquire the unique line spanned by ell from the kernel of
alpha -> alpha wedge T_0. Verify the contact identity and a nondegenerate
alternating form Omega on ker ell. This is the polynomial linear-algebra
construction in `HIGHER_RANK_STATIONARY_AUDIT.md`.

In any resulting chart (x,z), with z=ell and m=b-1, write

    H_0(x,z)=G_3(x)+z Q_2(x)+z^2 L_1(x)+c z^3.

The third form of G_3 vanishes, so its formal gradient is M x^[2]. Here
M is acquired directly from its square-times-linear coefficients; the map
from those coefficients to M is one-to-one, including the x_i^3 diagonal
terms. The polar matrix of Q_2 is Omega. The affine chart gradient is

    M x^[2]+Omega x+L.

Solve this binary affine linear system and require binary kernel dimension
zero. Let a be its unique solution. The change x -> x+a z eliminates the
z^2 L_1 term. It leaves G_3 and Omega unchanged and replaces c by the
acquired value tau=H_0(a,1). The centered polynomial is G_3+zQ_2+tau z^3.
If tau=0 its one affine stationary point is a projective critical ray; if
tau is nonzero there is no projective critical ray in this chart. The
later certificate makes M invertible, excluding the missing hyperplane.

## 2. Semilinear descent manufactures the binary structure

Let sigma denote coordinatewise squaring, and form the semilinear map

    S=Omega^(-1) M sigma.

Compute the F_q-linear matrix K=S^d by d semilinear compositions. Require

    K^2+K+I=0.

Choose r in {1,2} with rd=1 modulo3 and put

    D=K^r,             F=D^(-1)S.

The maps D and S commute, D^2+D+I=0, and F^d=I. Acquire the binary fixed
space U=Fix(F) by another linear solve. Check that it has binary dimension
m and that its computed basis is an F_q-basis of the transverse space.
These checks are part of the certificate, so its soundness does not
require a black-box descent theorem.

Restrict Omega to this binary basis. Require all its entries to be either
zero or one common nonzero field scalar gamma. Thus Omega/gamma is an
acquired binary symplectic form on U. Compute D on U and check that its
entries lie in F_2 and that it preserves this symplectic form. Each step
is polynomial in b and d and uses no field-element enumeration.

Now manufacture D-invariant symplectic planes. The binary quadratic
function v -> (Omega/gamma)(v,Dv) has polar form Omega/gamma, because
D^(-1)=D+I. It therefore has a vector v of value one. One can find such
a vector among a basis and its pairwise sums. The span of v,Dv is a
nondegenerate two-plane; its orthogonal complement is D-invariant. Repeat
on the complement. In the resulting basis, every block has

    Omega/gamma = [[0,1],[1,0]],       D=[[0,1],[1,1]].

Since the basis lies in Fix(F), the semilinear map S has coefficient D.
Therefore M=Omega D and every G_3 block is exactly

    gamma (X^3+XY^2+Y^3).

The remaining quadratic Q_2 has the known polar matrix. Read its square
coefficients in this basis and require that they too belong to gamma F_2.
Finally verify the complete ordinary polynomial identity displayed at the
start. The final check certifies all coefficients, not just sample values.

The rotation (X,Y)->(Y,X+Y) preserves the binary cubic above. On square
types it acts by

    (a,b) -> (b,1+a+b).

It cycles (0,0),(0,1),(1,0) and fixes (1,1). Thus every manufactured pair
has one of just two counting types: plus, with Q=XY, and minus, with
Q=XY+X^2+Y^2. Let their acquired multiplicities be s_+,s_-, respectively.

## 3. Completeness for the advertised family under hidden field coordinates

Start with a polynomial of the displayed two-type form. Apply an arbitrary
invertible field coordinate change, and multiply the entire polynomial by
a nonzero field scalar. Once the contact line and its unique affine root
are acquired, the centered old and new coordinates have the relation

    w_old=R w,              z_old=t z,

for an invertible R and nonzero t. Write D_0 for the direct sum of the
order-three blocks and let the original coefficient scale be gamma_0.
Then

    S=t^(-1) R^(-1) D_0 sigma R,
    K=R^(-1)D_0^d R,
    D=R^(-1)D_0 R,
    F=t^(-1)R^(-1)sigma R.

Consequently Fix(F)=R^(-1)t F_2^m. The acquired form on this space has
the common scalar gamma_0 t^3. All certificate conditions hold. The
symplectic D-invariant planes may differ from the planted pairs, but they
are computed and the complete ordinary polynomial identity still holds.
In particular Q_2 retains binary normalized coefficients. This proves
completeness under arbitrary field coordinates, radial normalization,
and phase scaling; a planted decomposition is unnecessary.

The additional raw binary affine disguise is handled by the root's
centroid, coefficient, and center acquisition. The degree restriction
d>=3 of that raw fitter remains in force. It is compatible with this
subfamily's requirement 3 not dividing d.

## 4. Every pair Gaussian has at most seven values

For a fixed field parameter z, define

    A_+(z)=sum_(x,y in F_q) (-1)^Tr(gamma [x^3+xy^2+y^3+zxy]),
    A_-(z)=sum_(x,y in F_q) (-1)^Tr(gamma [x^3+xy^2+y^3
                                        +z(xy+x^2+y^2)]).

These are binary quadratic Gaussians in 2d bits. Their polar matrices are
identical, because the extra square terms are binary-linear. A vector
(x,y) lies in the common binary polar kernel precisely when

    gamma x^2+(gamma x)^(q/2)+gamma y^2+gamma z y=0,
    (gamma x)^(q/2)+gamma y^2+(gamma y)^(q/2)+gamma z x=0.

Squaring and dividing by gamma gives the ordinary quartic system

    gamma x^4+x+gamma y^4+gamma z^2 y^2=0,
    x+gamma y^4+y+gamma z^2 x^2=0.

The ordinary Jacobian is [[1,0],[1,1]], invertible in characteristic two.
Every geometric solution is isolated and simple, and Bezout bounds their
number by 16. The binary kernel therefore has dimension at most four.
The polar rank is even, so the nullity is one of 0,2,4. A quadratic
character sum with this nullity is either zero or plus/minus
2^((2d+nullity)/2). Thus both A_+ and A_- belong to the fixed alphabet

    V={0,q,-q,2q,-2q,4q,-4q}.

This bound is uniform in d, z, gamma, and the number of repeated pairs.

## 5. Order-three symmetry reduces the joint table to eight states

The minus-pair polynomial is invariant under C:(x,y)->(y,x+y), an
ordinary polynomial identity over every F_q. This map has C^2+C+I=0.
The associated binary quadratic and its polar form are C-invariant.
Consequently the binary radical R is C-stable. The quadratic restricted
to R is linear, and a C-invariant linear functional must be zero because
C+I is invertible. Thus A_- never vanishes.

The quadratic descends to a nondegenerate binary quadratic on the quotient
by R. For any vector v in this quotient,

    Q_-(v)=Q_-(v+Cv)=B(v,Cv),

where C-invariance was used to cancel Q_-(v)+Q_-(Cv). A vector with
B(v,Cv)=1 spans, together with Cv, a C-invariant nondegenerate plane.
The quadratic has value one on both basis vectors of that plane, so the
plane is anisotropic and its Gaussian sign is negative. Its orthogonal
complement is C-invariant. Decomposing successively shows that, if the
binary radical has dimension k,

    A_-(z)=(-1)^(d-k/2) q 2^(k/2),        k in {0,2,4}.

A_+ has the same polar matrix. For k=0 it is nonzero with magnitude q;
for k=2 or4 it is zero or has the same magnitude as A_-. Put
epsilon=(-1)^d. There are therefore only eight possible joint states:

    ( -q, epsilon q), (q, epsilon q),
    ( -2q,-2epsilon q), (0,-2epsilon q), (2q,-2epsilon q),
    ( -4q, 4epsilon q), (0, 4epsilon q), (4q, 4epsilon q).

The code checks this sharper palette independently of the earlier
seven-value marginal bound.

### Exact reconstruction from eight moments

The full field sum is

    S_1=sum_z (-1)^Tr(tau z^3) A_+(z)^(s_+) A_-(z)^(s_-).

For each of these eight nodes (u,v), define the signed multiplicity

    C_(u,v)=sum_(z:A_+(z)=u,A_-(z)=v) (-1)^Tr(tau z^3).

It may be negative when tau is nonzero. Use the eight moments

    M_(i,j)=sum_z (-1)^Tr(tau z^3) A_+(z)^i A_-(z)^j,
             (i,j) in {(0,0),(0,1),(0,2),
                        (1,0),(1,1),(1,2),(2,0),(2,1)}.

Here is an explicit invertibility argument. The three moments with i=0
recover the total signed mass at each of the three distinct v-levels by
a 3-by-3 Vandermonde system. The three moments with i=1 recover the signed
u-sum at each v-level in exactly the same way. At the first level u^2=q^2,
so its signed u^2-sum is already known. Subtract that contribution from
the two i=2 moments; a 2-by-2 Vandermonde system gives the u^2-sums at the
other two levels. At each level, total mass, u-sum, and u^2-sum uniquely
determine the masses at its two or three allowed u-values.

Equivalently, invert the fixed 8-by-8 evaluation matrix of these monomials
on the eight nodes. After reconstructing C, compute

    S_1=sum_(u,v) C_(u,v) u^(s_+) v^(s_-).

The convention0^0=1 is used throughout. Each moment has O(d) bits,
because its indices are bounded. Rational reconstruction uses only fixed
matrix dimensions and O(d)-bit operands. The final powers and sum have
O(bd) output bits and are computed by ordinary exact integer arithmetic.
There is no unit-cost assumption for exponentially large integers.

An independent reference in the code reconstructs the full 7-by-7 table
from all 49 rectangular moments with 0<=i,j<=6 and verifies that it agrees
with this eight-state reconstruction. The extra reference moments are
used for validation, not needed by the polynomial theorem.

## 6. The eight moments are fixed-variable exact point counts

Expand each A_+^i A_-^j using i+j independent pair copies. Its moment is
the character sum of

    P_(i,j)=tau z^3 + gamma sum_(ell=1)^(i+j)
                [x_ell^3+x_ell y_ell^2+y_ell^3
                 +z(x_ell y_ell+epsilon_ell(x_ell^2+y_ell^2))],

where epsilon=0 for the first i copies and1 for the last j. This is an
ordinary cubic in 2(i+j)+1<=7 field variables, irrespective of b. Add an
Artin--Schreier coordinate w and count

    w^2+w+P_(i,j)=0.

For each assignment to the original variables, this equation has
1+(-1)^Tr(P_(i,j)) solutions. Therefore

    M_(i,j)=#V_(i,j)(F_q)-q^(2(i+j)+1).

The hypersurface has degree at most three in at most eight variables. The
deterministic algorithm of Lauder--Wan therefore computes each moment in
polynomial time in d, uniformly in b. Their conservative bound for fixed
characteristic, degree, and variable count n_0 is soft-O(d^(3n_0+7)) time
and soft-O(d^(2n_0+4)) storage. With n_0<=8 this gives the stated d^31
and d^20 bounds. There are at most eight calls; M_(0,0) is itself a binary
quadratic Gaussian and can be computed directly.

Primary source: Alan G. B. Lauder and Daqing Wan, *Counting points on
varieties over finite fields of small characteristic*, Theorem1,
Proposition36 and the quantitative statement in the introduction,
https://arxiv.org/pdf/math/0612147. The algorithm permits singular
varieties and assumes the finite field is supplied by an irreducible
polynomial. Here that presentation is acquired by the existing compiler.

## 7. Why this removes the remaining depth-one obstruction for this class

The contact gradient of one pair at z=1 is

    X^2+Y^2+Y=0,             Y^2+X=0.

It has only the zero solution when3 does not divide d, since any nonzero
Y would satisfy the irreducible binary cubic Y^3+Y+1=0. The coefficient
matrix M has invertible 2-by-2 blocks, so there are no missed projective
critical points at z=0. The entire residue therefore has either one
critical ray (tau=0) or none (tau nonzero), independently of b and of the
square types.

At ring depths e>=2 the previously proved transverse Gaussian and
origin descent process at most this one ray, while permitting arbitrary
higher nilpotent cubic coefficients and allowed quotient quadratics.
Whenever the recursion reaches depth one, the terminal above applies to
the same residue. Thus every depth is polynomial for the certified
subfamily, with all original input variables counted and all arithmetic
costs charged. The generic unbounded-rank class still has the #P-hard
growing-kernel obstruction proved in the companion audit.

## 8. Executed evidence and the limit of that evidence

`acquired_pair_terminal.py` contains the complete residue certificate,
ordinary polynomial transformations, exact eight-state reconstruction,
explicit Gaussian-fiber reference backend, and exact-moment interface.

`acquired_pair_terminal_checks.py` executes six disguised counting cases,
including both quadratic types, nonzero radial cubics, arbitrary field
coordinate mixing, and nontrivial phase scaling. Its independent complete
finite-field truth oracles cover 2,114,720 assignments. Twenty independent
small-field expanded moments cover 6,624 assignments and verify the
Artin--Schreier conversion. Five larger acquisition-only cases reach 77
binary residue coordinates and recover the coefficient identity without
field enumeration. A non-binary square coefficient is correctly rejected
by the additional template gate even though it retains contact geometry.

`raw_pair_terminal_regression.py` starts from the existing 36-bit raw
Boolean ANF, reruns centroid/coefficient/center acquisition, and then
acquires this pair certificate without a supplied field-block basis.
Its moment backend is explicitly a test-only replay of moments from the
16-element reference field scan. The saved result distinguishes this from
a generic fixed-variable point-count execution.

The finite-value Gaussian/moment method has established ancestry. For
example, Jinquan Luo's *On Binary Cyclic Codes with Five Nonzero Weights*,
Sections2--3, uses binary quadratic-form ranks and moment identities to
recover exponential-sum distributions:
https://arxiv.org/html/0904.2237v1. Neither this note nor the tests establish
historical priority for that method. The contribution under examination
is the particular manufactured semilinear/block certificate, its use to
keep point-count dimension independent of unbounded module rank, and its
composition with the raw chain-ring compiler. A broader novelty assessment
remains separate from the proved identities and executed regressions.

There is an even closer classical connection for odd d. In F_(q^2), let
omega^2+omega+1=0 and write u=x+omega y. Then u^q=x+omega^2 y,

    x^3+xy^2+y^3=omega^2 u^3+omega (u^q)^3,
    x^2+xy+y^2=u^(q+1),
    x+y=Tr_(q^2/q)(omega u).

Thus A_-(z) is the generalized Kasami sum with norm coefficient gamma z
and cubic coefficient gamma omega^2. A_+(z) is the corresponding sum with
the added linear coefficient omega(gamma z)^(q/2). This is an explicit
algebraic identification of our pair kernels with established objects.
The pertinent primary paper is Jinquan Luo, Yuansheng Tang and Hongyu
Wang, *Cyclic Codes and Sequences: the Generalized Kasami Case*, equations
(3)--(4) and Lemma3, https://arxiv.org/pdf/0902.4510. It studies value
distributions of those quadratic exponential sums over their parameter
families. The present terminal requires a joint distribution along the
specific linked parameter line, with weight (-1)^Tr(tau z^3), and the
manufactured decomposition described above. This source strengthens the
ancestry qualification; the additional compiler is not presented as the
discovery of the pair exponential sums.
