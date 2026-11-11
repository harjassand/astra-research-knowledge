UNIFORM ENDPOINT NEGATIVE SUBLEVELS AND AN EXACT GENERATING-HESSIAN INTERFACE
ROOT mathematical derivation, 11 November 2026

1. Original contract and accepted new input

For k>1/3, ell=3k-1,n=k+1, column norms u,v and determinant j, retain
  J_k(F)=ell(ku-v+2j)^2/(8n)+ell uv/4+j^2
        =j^2+ell Q_k(F).
The full question is the original integral inequality at EVERY affine mean,
EVERY actual periodic W^(1,4) vector gradient and EVERY k>1/3, or an actual
compatible negative original gap. No change of source measure is free.

P1_28DA6F_FULL_FINAL_20261111.md proves, for 1/3<=k<=1,
  |F|^4/336 <= Q_k(F) <= 7|F|^4/16,
  |Q_hat_ell(F)-Q_hat_epsilon(F)|
     <=13|ell-epsilon||F|^4/96,
where Q_hat_ell=Q_{(1+ell)/3}. These are bounds on the quartic CORRECTION itself.
It also supplies the exact conditional potential-law variance and the actual
conditional lower-endpoint value limit. Neither gives a universal original
sign or control over first rows varying with ell by itself.

2. A uniform necessary condition for ALL negative tests approaching the endpoint

Let F=A+Dphi be any actual admitted field, with negative original gap, and
1/3<k<=1. The determinant null-Lagrangian gives int j=det A=d. Hence
  Delta J_k = int(j-d)^2 + ell[int Q_k(F)-Q_k(A)].
In particular A!=0, and negativity implies BOTH
  int Q_k(F)<Q_k(A),
  int(j-d)^2 < ell Q_k(A).
Using the accepted correction coercivity, not just coercivity of J_k, yields
the uniform all-field estimates
  int |F|^4 <147 |A|^4,
  ||j-d||_2^2 <(7/16)ell |A|^4.                         (1)
There is no inverse-ell blow-up in the first estimate. It covers changing
frequencies, changing first rows and concentration patterns, not just a fixed
conditional cell problem. By quartic homogeneity any negative test can be
normalized to |A|=1.

At that normalization the correction Lipschitz estimate further gives
  int Q_0(F)-Q_0(A)
    < (481/24)ell - ||j-d||_2^2/ell.                    (2)
Here Q_0 means Q_{1/3}, and 481/24=(13/96)(147+1).

For an actual negative sequence with ell_i down to zero and |A_i|=1, take a
subsequence A_i->A. Poincare and (1) bound the mean-zero potentials in W^(1,4).
They have a weak W^(1,4) limit and a strong C^(0,alpha) limit for each alpha<1/2.
The distributional determinant identity, combining strong potentials with weak
gradients, identifies det(A+Dphi) as the strong L2 limit of the determinants.
Thus the ACTUAL weak-limit gradient has constant determinant det A.

The unresolved point must not be suppressed: Q_0 is not known to be weakly
lower semicontinuous for these full vector gradients. Therefore this compactness
does NOT transfer the inequality in (2) to the weak limit, exclude concentrations
or prove an endpoint neighborhood. Even equality in a limiting constrained
comparison would leave higher-order negative gaps possible. No uniform endpoint
theorem, epsilon-regularity or finite search cutoff follows from (1)--(2).

3. Every periodic scalar Hessian gives an actual constant-determinant map

Let W(theta,y) be a smooth real periodic scalar function and suppose
  q=1+W_{theta y}>=q0>0.
Use the actual source coordinate change
  x=theta+W_y(theta,y),  x2=y.
It is a global torus diffeomorphism, since its derivative with respect to theta
is q>0 and its winding in theta is one. Define in the ORIGINAL source variables
  Psi(x,y)=(theta(x,y), y+W_theta(theta(x,y),y)).
Write a=W_{theta theta}, b=W_{yy}, c=W_{theta y}, q=1+c. Direct differentiation
gives the exact matrix
  D Psi=L(D^2 W),
  L(a,b,c)=q^{-1} [[1,-b],[a,q^2-ab]],
  det L=1.                                               (3)
Psi-id is periodic and the actual source Jacobian is dx dy=q dtheta dy.
For EVERY constant real matrix A, F=A D Psi is an actual compatible gradient
with affine mean A and constant determinant det A. In particular,
  int_original Q_0(F)=int_(theta,y) K_A(D^2 W),
  K_A(M)=(1+M12) Q_0(A L(M)),
  K_A(0)=Q_0(A).                                         (4)
All integrals here use the specified unit torus and its actual measure.

This is larger than the two independent-profile partial-Legendre branch.
There is no wave equation or separability assumption on W. Conversely, after
the given left SO(2) normalization of an invertible mean to rows (s,0),(b1,b2),
this parameterization exhausts smooth constant-total-determinant completions
whose normalized first potential U has U_x1>0 and UNIFORM circle law.

For that converse, invert U to x=X(theta,y). Uniform circle law says
  int_0^1 X_theta(theta,y)dy=1.
Consequently the y-mean of X-theta is constant. Remove the harmless constant
source translation and write X=theta+W_y with W periodic. Constant determinant
then gives, in mixed coordinates,
  v(X(theta,y),y)=b1 theta+b2[y+W_theta(theta,y)]+p(theta),
with p periodic. Its constant is irrelevant; after fixing it to have zero mean,
the remaining p can be absorbed in W by adding a periodic function h(theta)
with h'=p/b2. This leaves W_y unchanged and proves the converse.

The converse does not cover folded first potentials, degenerating monotonicity,
nonuniform circle laws, singular affine means or arbitrary determinant
fluctuations. Formula (3) itself is valid for any A, including singular A.

4. The transformed density is Hessian rank-one convex, not already quasiconvex

Let M=[[a,c],[c,b]], q=1+c>0. Along the scalar-Hessian rank-one direction
xi tensor xi, with xi=(xi1,xi2), put q_t=q+t xi1 xi2. Then
  L(M+t xi tensor xi)-L(M)
    =t/[q q_t] C tensor R,
  C=(-xi2, q xi1-a xi2),
  R=(xi1, q xi2-b xi1).                                 (5)
The vectors C,R are constant along that line. In particular, the L-images lie
on one ordinary rank-one matrix line and q_t L(M+t xi tensor xi) is affine in t.
The perspective of a convex scalar function is convex. Applied to the accepted
rank-one convexity of J_k, this proves convexity of
  t -> q_t J_k(A L(M+t xi tensor xi))
throughout q_t>0. Since det(A L)=det A, its determinant-square part is the
AFFINE function q_t(det A)^2. Subtract that part and divide by ell>0, then let
k down to 1/3. Thus K_A in (4) is rank-one convex along all scalar Hessian
directions xi tensor xi.

This is not a scalar first-gradient convexity assertion. The central new form
of the remaining constant-determinant comparison is
  int K_A(D^2 W) >= K_A(0),  for all periodic W with 1+W12>0.    (6)
Rank-one convexity in (5) does not prove this Hessian Jensen inequality.
Ordinary scalar Jensen, independent-profile averaging and the Burkholder
projection theorem cannot simply be inserted for (6). No claim that all
Hessian gradient measures are laminates is made.

5. A strictly negative transformed test gives a paid original negative

Suppose an ACTUAL W with q>=q0 and an actual A satisfy
  int K_A(D^2 W)-Q_0(A) <= -eta <0.
Put E=int_original |A D Psi|^4+|A|^4. The accepted correction Lipschitz estimate
implies that every positive rational
  ell < min(1,48 eta/(13 E))
gives, at the admitted k=(1+ell)/3,
  int_original J_k(A D Psi)-J_k(A) <= -ell eta/2 <0.          (7)
One may replace E by any paid explicit upper bound. This retains the original
measure, compatibility, affine mean and total determinant exactly. It is an
actual reduction from a Hessian test to the FULL original negative endpoint,
not an abstract measure or certificate-jet negative.

A universal positive theorem for (6) alone would be narrower: it would settle
this smooth monotone constant-determinant correction class, not arbitrary k,
folds, varying-ell competitors, relaxed limits or determinant fluctuations.

6. Finite realization and computation; no PDE/optimization oracle

For rational A and rational finite Fourier W, use rational upper bounds on derivatives through
order three, computed from its coefficient sums and 2pi<7. Suppose q>=q0>0 has
a supplied or finitely certified rational lower bound. Define a rational
  B>=2+|A|_1+q0^{-1}+sum_(1<=|alpha|<=3)||D^alpha W||_infinity.
The explicit formulas give |A L|_1<=8 B^4 and, for each coordinate j,
|partial_j(A L)|_1<=16 B^6. For example,
  C_B=2^40 B^32
is a safe common bound for the integrand q Q_0(A L), its first derivatives and
the fourth-moment integrand q|A L|^4 and its first derivatives.

A square grid with side count >=8 C_B/zeta, rational interval evaluations at
nodes of width <=zeta/4 and the first-derivative Riemann bound enclose each
integral to prescribed error zeta. Trigonometric interval values use finite
Taylor polynomials after rational pi enclosure and paid argument reduction.
Division uses q>=q0; no exact-real primitive is assumed. If q is positive but
its floor was not supplied, successive grids and the derivative bound certify
a positive rational floor after finitely many stages. No termination is claimed
for a W whose q is nonpositive somewhere.

The original compatible map is defined by the unique monotone equation for
theta in (3). Pointwise bisection has a derivative floor q0. The displayed
derivative bounds pay uniform errors in the inverse and D Psi. Smooth periodic
approximation can therefore realize the same original W^(1,4) map or a finite
Fourier approximation with its gap error explicitly bounded. Grid node count,
precision, bisections and approximation errors are finite charged functions of
the listed input and derivative bounds; no polynomial efficiency in binary
input alone is asserted or required. No negative W, energy grid or PDE solve
was executed here.

Finite diagnostic actually executed: four exact rational choices of a,b,c,
xi,t, including a vanishing q derivative, checked det L=1, rank-one matrix
increments and the complete increment identity (5) with standard-library
Fraction arithmetic. All identities held exactly. This finite check is not
an energy computation or a substitute for the displayed all-input derivation.

7. Source boundary and relation to the actual returned obstruction

ROOT refreshed arXiv:2609.28311v2 Theorem1, Corollary2 and Lemmas3--4, including
the actual compatible projection and null-determinant proof, at
https://arxiv.org/html/2609.28311v2
Its all-affine-mean periodic VECTOR-gradient Burkholder theorem is accepted at
that scope. It does not identify the anisotropic K_A in (4), supply (6), erase
the Hessian constraint or pay a sharp shared original-energy budget here.
Equations (1)--(7) are derived directly from the original density and the new
returned correction estimates, not imported from an unavailable proof file.

The returned twisted area-preserving example proves that the actual conditional
radial work can be negative on part of a path although its complete original
gap is positive. Thus pointwise nonnegative radial flux is unavailable. The
uniform negative-sublevel estimate and the generating-Hessian representation
do not assume that false sign. Neither they nor the fixed-first-row endpoint
limit close the original all-k/all-means/all-gradients question.
