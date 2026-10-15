# Full invariant finite-H completion projection

15 October 2026. Independent coverage and analytic audit by
`fy_global_projection_audit`. The full-space gluing is the root's synthesis;
the generic-angle classification is credited to `fy_contact_angle_genesis`,
with a separate equation-first reconstruction by `fy_contact_independent_audit`.
The classical strict branch and the two inherited contact strata retain their
original attribution. This proof is internally audited, externally unreviewed,
and not formally verified. Historical priority remains UNKNOWN.

## Exact statement

Let V be the real nine-dimensional vector space of real homogeneous quartics
on real 2 by 2 matrices invariant under left SO(2). Write

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
\mathcal C A=(a-d,b+c),\qquad
H(A)=|\mathcal C A|^4=(|A|^2-2\det A)^2.
\]

The matrix norm is Frobenius. Let R be the cone of globally rank-one-convex
members of V, and let Q be its all-background quasiconvex cone. The QC contract
is every bounded planar Lipschitz domain Omega, every B in R^(2x2), and every
phi in W_0^(1,4)(Omega;R^2), with inequality

\[
\int_\Omega [F(B+D\phi)-F(B)]\ge0. \tag{1}
\]

Let pi be quotient by span{H}. Then

\[
\boxed{\pi(R)=\pi(Q).} \tag{2}
\]

Equivalently, for every G in V, existence of one finite real alpha making
G+alpha H rank-one convex is equivalent to existence of one finite real beta
making G+beta H satisfy (1). The completed coefficient may depend on G but
is independent of B, Omega and phi. The periodic version holds as well.

Moreover, for every prescribed nu>0, beta can be increased so that the left
side of (1) is at least

\[
\frac{4\nu}{1875}\int_\Omega |D\phi|^4. \tag{3}
\]

This does not equate the two coefficients, identify their least values, or
prove QC of a representative at its original coefficient.

## 1. Necessary acoustic condition and the conformal dichotomy

For a smooth finite polynomial integrand, QC implies the Legendre-Hadamard
inequality. One direct argument differentiates (1) twice at zero amplitude,
giving a nonnegative integrated constant-coefficient quadratic form.
Testing with (1/k) eta(x) p sin(k q.x), where eta is a fixed smooth compact
cutoff, and letting k tend to infinity isolates
D^2F(B)[p tensor q,p tensor q]. Thus this quantity is nonnegative at every B.
For C^2 functions this is equivalent to convexity on every rank-one line,
because it is exactly the second derivative along each such line. Therefore
pi(Q) is contained in pi(R).

For the other inclusion, suppose F=G+alpha_0 H is ROC for one finite alpha_0.
The first three derivatives of H vanish on the conformal plane, in particular
at I. Consequently

\[
q_G(R):=D^2G(I)[R,R]=D^2F(I)[R,R]\ge0
\quad(\operatorname{rank}R=1). \tag{4}
\]

The set of rank-one matrices of Frobenius norm one is compact. There are
exactly two possibilities: its minimum mu for q_G is positive, or that
minimum is zero and attained by a nonzero rank-one R. The origin's automatic
quartic contact is irrelevant to this dichotomy.

Every nonzero conformal matrix is sQ_theta with s>0 and Q_theta in SO(2).
Left invariance and homogeneity imply

\[
D^2G(sQ_\theta)[R,R]
=s^2D^2G(I)[Q_\theta^TR,Q_\theta^TR]. \tag{5}
\]

Hence strict positivity at I gives strict positivity at all nonzero
conformal backgrounds. Conversely, any failure of conformal strictness
already gives a rank-one zero at the invertible background I. No
classification of contacts at singular or nonconformal backgrounds is
needed for the proof.

## 2. Strict branch: exact classical hypotheses

If mu>0 in (4), equation (5) gives

\[
D^2G(U)[R,R]\ge d|U|^2|R|^2,
\qquad d=\mu/2>0, \tag{6}
\]

for every conformal U and rank-one R. The factor 1/2 is required because
|I|^2=2.

Decompose A=U+V orthogonally into its conformal and anticonformal parts.
For the quadratic dependence of D^2G(A)[R,R] on A, finite-dimensional
compactness provides a finite M such that its mixed polarization has
absolute value at most M|U||V||R|^2 and its V-quadratic part is at least
-M|V|^2|R|^2. Thus

\[
D^2G(U+V)[R,R]\ge
\left[\frac d2|U|^2-
\left(M+\frac{2M^2}{d}\right)|V|^2\right]|R|^2. \tag{7}
\]

For rank-one R, |CR|^2=|R|^2 and |CA|^2=2|V|^2. Direct differentiation gives

\[
D^2H(A)[R,R]=4|CA|^2|R|^2+8(CA.CR)^2
\ge8|V|^2|R|^2. \tag{8}
\]

Choose a finite

\[
c\ge\frac{M+2M^2/d+d/2}{8}.
\]

Then R_0=G+cH satisfies the global strict LH inequality

\[
D^2R_0(A)[R,R]\ge(d/2)|A|^2|R|^2. \tag{9}
\]

The original publisher PDF of Iwaniec-Kristensen (2005), printed pp.77-80,
was downloaded and visually inspected in this audit. Its Theorem 3.1 applies
to a C^3, positively p-homogeneous R_0 with p>3 and the global strict LH
bound. Here p=4 and R_0 is a polynomial, so the regularity and homogeneity
requirements hold everywhere, including zero. Its perturbation P must have
a uniform integrated p-gap. Their Lemma 4.1 gives this for powers of a linear
map whose kernel contains no nonzero rank-one matrix. Set that map to
sqrt(2) times the Frobenius-orthogonal anticonformal projection, so P=H
exactly. This also fits the source lemma's equal-domain/equal-codomain
linear-map convention. Its kernel is the conformal plane, whose nonzero
members have positive determinant and rank two.

Thus H has a uniform integrated fourth-power gap e_H>0, and Theorem 3.1
gives QC of R_0+tH for all sufficiently large finite t. At p=4 the source's
displayed sufficient value is

\[
t\ge\frac{T_3^2}{2\delta e_H},\qquad
\delta=d/2,\quad
T_3=\sup_{|A|=1}\|D^3R_0(A)\|.
\]

This supplies a finite QC completion of G. It is a classical consequence,
not new completion machinery. The primary proof supplies compact smooth
tests at every affine background; Section 6 below gives the receiving
Sobolev and periodic extensions.

Source: [Iwaniec-Kristensen, A construction of quasiconvex functions](https://www.rivmat.unipr.it/fulltext/2005-4s/pdf/03.pdf), Theorem 3.1 and Lemma 4.1.

## 3. Nonstrict branch: exhaustive H-preserving normalization

Let R=a tensor b be a nonzero rank-one zero of (4). Absorb |b| into a and
choose O in SO(2) with Ob=e1. Define

\[
\widetilde G(A)=G(O^T A O),\qquad
\widetilde R=O R O^T=(r,s)\otimes e_1. \tag{10}
\]

Then I is fixed, the contact persists, and nonzero rescaling of the direction
preserves the zero. There are exactly three cases:

* s=0: the contact is a nonzero multiple of e11.
* s is nonzero and r=0: the contact is a multiple of e21; conjugation by the
  quarter-turn J sends e21 to -e12.
* rs is nonzero: division by s gives R_t=(t,1) tensor e1 for one finite real
  t=r/s different from zero.

No limiting passage t to infinity is used for the first case, and the second
case is explicitly separated from t=0 in the generic theorem.

For any O in O(2), orthogonal conjugation preserves the Frobenius norm and
determinant, so it preserves H. It also preserves left-SO(2) invariance:
O^T Q_theta O is again in SO(2), even for det O=-1. Rank-one directions are
preserved. The QC transport follows from the explicit change of variables

\[
\widetilde\Omega=O\Omega,\qquad
\widetilde\phi(y)=O\phi(O^T y),\qquad
\widetilde B=OBO^T.
\]

Then D tilde_phi(y)=O Dphi(O^Ty) O^T and
tilde_G(tilde_B+D tilde_phi)=G(B+Dphi). Area, Frobenius norm, zero trace and
W^(1,4) membership are preserved. Applying the inverse orthogonal matrix
proves equivalence in both directions. Reflections are therefore permitted,
although SO(2) alone suffices for exhaustive coverage.

In particular, if a generic-angle report uses the row direction
e1 tensor (t,1), the symmetric reflection

\[
U_t=\frac1{\sqrt{1+t^2}}
\begin{pmatrix}t&1\\1&-t\end{pmatrix}
\]

sends it by conjugation to R_t. This is an orthogonal change of both target
and domain coordinates; no transposition invariance of quasiconvexity is
assumed. Its conjugation map has rational entries for rational t because
the two square-root factors combine to the denominator 1+t^2.

## 4. Contact stationarity and the three exact receiving theorems

For an ROC quartic, the polynomial

\[
h_F(B,p,q)=\tfrac12D^2F(B)[p\otimes q,p\otimes q]
\]

is nonnegative for every B,p,q. At any zero every first derivative vanishes.
This uses ROC together with contact equality. Equality alone would not
justify any of the four-dimensional span claims. Since D^3H(I)=0, replacing
F by its H-projected representative does not change these stationary
conditions.

The independent script differentiates the full nine-coefficient invariant
polynomial, without importing producer code, and reconstructs the entire
stationary space in each case. The generic rank-five minor is

\[
-24t(1+t^2)^3(t^2+3),
\]

which has no nonzero real root. Four independent kernel generators then
give the asserted span; the exceptional cases are checked separately.

For e12, the stationary span is

\[
\operatorname{span}\{H,u^2,j^2,uj\},
\quad u=a^2+c^2,\quad j=\det A.
\]

The inherited entire shear projection, N872, states that
alpha H+beta u^2+gamma j^2+delta uj has a finite ROC completion exactly when
it has a finite all-background QC completion. Its exact alternatives are
delta=0, beta,gamma>=0, or delta different from zero, gamma>0,
6 beta gamma-delta^2+delta gamma>=0 and 2 beta+delta>0. This includes the
positive-delta sufficiently large completion. No unchanged sharp coefficient
is inferred from that existence statement.

For e11, the stationary span is

\[
\operatorname{span}\{H,w^2,vj,v^2\},
\quad v=b^2+d^2,\quad w=ab+cd.
\]

Pinned N873 proves finite ROC/QC completion equivalent to k=ell=0,m>=0,
or k>0, ell+2m>0, 2km-k ell-ell^2>0 in
alpha H+k w^2+ell vj+m v^2. Its all-background analytic contract is exactly
(1), including the singular affine backgrounds.

For R_t with finite t different from zero, put

\[
n=1+t^2,\quad L_t=tw-j+v,\quad B_t=v(j-2L_t/n).
\]

The new generic classification gives the stationary span
{H,L_t^2,B_t,v^2}. For
alpha H+k L_t^2+ell B_t+m v^2 it proves finite ROC/QC completion equivalent
to k=ell=0,m>=0, or

\[
m>|\ell|/2,\qquad
\Delta=k n^2(2m-\ell)(2m+\ell)
-\ell^2[t^2(2m+\ell)+3(2m-\ell)]>0. \tag{11}
\]

The finished constructor report and independent equation-first derivation
were read in full. Section 5 records the analytic audit that admits this
lemma. Thus the three cases in (10) each provide one finite QC completion
of tilde_G. Orthogonal transport gives a finite QC completion of G and
proves (2).

## 5. Audit of the generic lemma's load-bearing analytic steps

The exact determinant support is

\[
Q(X)=\tfrac12D^2G(I)[X,X]-3\ell\det X
=kx^2+\frac{2\ell}{n}(tb-3d)x
 +(2m-\ell)b^2+3(2m+\ell)d^2,
\quad x=-a+t(b+c)+d. \tag{12}
\]

The coordinate map X to (x,b,d) has kernel span{R_t}. For all triples with
td-b different from zero, choosing
c=(xd-tbd-d^2)/(td-b) and a=t(b+c)+d-x realizes that triple by a rank-one
X. This is a dense set of triples, so the acoustic condition at I forces
Q to be PSD on the full three-dimensional coordinate space. Its matrix is

\[
C=\begin{pmatrix}
k&\ell t/n&-3\ell/n\\
\ell t/n&2m-\ell&0\\
-3\ell/n&0&3(2m+\ell)
\end{pmatrix},\qquad \det C=3\Delta/n^2. \tag{13}
\]

For ell nonzero, t nonzero, PSD requires 2m-ell>0 and 2m+ell>0: the two
off-diagonal entries rule out zero diagonal entries. Schur complementation
then gives Delta>=0. At Delta=0, set A0=2m-ell, B0=2m+ell. The displayed
second rank-one kernel direction in the constructor has x=1 and is
independent of R_t. Its background acoustic derivative is

\[
\frac{\ell^3t}{A_0^3B_0^2n^3}(-4tP,S,S,4tP),
\]

where P=mB0^2t^2+A0^2(2ell+m) and
S=B0^3t^4+2(4m-3ell)A0B0t^2+3A0^3. For ell>0, P>0. For ell<0, all
three coefficients of S as a polynomial in t^2 are positive, so S>0.
The prefactor is nonzero. Hence the derivative never vanishes in the
allowed boundary region. The independent script reconstructs all four
entries from the differentiated quartic rather than importing the result.

For each finite alpha, displacement of the background opposite this
nonzero derivative makes the acoustic polynomial negative for sufficiently
small positive displacement. H has zero cubic derivative at I, so it
cannot remove the nonzero linear term. This is a genuine ROC obstruction,
uniform over the quantifier 'each finite alpha', with a displacement allowed
to depend on alpha.

For ell=0, PSD gives k,m>=0. If k=0, mv^2 is ordinarily convex. If k,m>0,
C is positive definite. The remaining k>0,m=0 case has the rank-one zero
Z0=(1,-t) tensor e2 and background derivative 2kn(-1,t,t,1), which is
nonzero and is excluded by the same argument. These cases exhaust all
weak possibilities; no semidefinite boundary is silently discarded.

Under (11), Q has rank three and kernel exactly span{R_t}. Contact
stationarity gives D^3G(I)[R_t,R_t,E]=0 for every E. By polarization on
this one-dimensional kernel, the full two-kernel-vector flatness predicate
of GENERAL_FLAT_COMPLETION holds. Its supplied slope is forced here to be
lambda=3ell; a PSD support must annihilate the contact in its polar form.

The inherited flat compiler expands the whole quartic Taylor remainder at
B=sI+E, where E is anticonformal after a target rotation. It integrates away
the constant determinant multiplier and controls the remaining mixed and
cubic terms by kernel flatness and Young inequalities. There is no
unbounded-order remainder and no uniform ellipticity assumption on the
kernel. Its finite threshold is

\[
\alpha_*=401296M^2/\kappa+(9391/4)M,
\]

where M bounds the symmetric four-linear tensor and kappa>0 bounds Q on
its Frobenius-orthogonal kernel complement. The absolute sum of expanded
quartic coefficients is a valid M. At rational t,k,ell,m, the four-entry
matrix is rational, and e3/e2 of its positive spectrum is a positive
exact lower bound. It does not require numerical eigenvalue separation.

The analytic mechanism covers every affine B, including B=0 and singular
B, because every matrix has the stated conformal/anticonformal decomposition.
The operator bound used by the inherited numerical constants is the
nonsharp complex L4 Beurling bound sqrt(24); no contemporary sharp claim
is needed. The pinned independent audit of GENERAL_FLAT_COMPLETION was
read, and the threshold arithmetic and H gap identities were checked here.

## 6. Sobolev, periodic, and reserve quantifiers

For smooth compact tests, every completion theorem above holds at all
backgrounds. Extending a smooth zero-boundary test by zero gives its
whole-plane version. Strong W^(1,4) approximation proves (1) for the stated
zero-trace Sobolev space: quartic polynomial integrals are continuous under
that convergence, with B fixed. The coefficient remains independent of B
because the smooth inequality was already uniform over backgrounds.

For a smooth periodic perturbation, tile an expanding square and multiply
by a cutoff that is one in the interior and vanishes in a fixed-width outer
strip. The strip area is O(N) against O(N^2) bulk area, and all quantities
there are uniformly bounded. Dividing the zero-boundary inequality by bulk
area and taking N to infinity gives the periodic inequality. Smooth
periodic approximation then gives the W^(1,4) periodic version. Mean-zero
values are unnecessary; periodic gradients already have zero mean and the
cutoff error is negligible.

Finally, for x,h in R^2,

\[
|x+h|^4-|x|^4-4|x|^2x.h-|h|^4/3
=2(|x|^2|h|^2-(x.h)^2)+6(x.h+|h|^2/3)^2\ge0.
\]

Together with the inherited finite Cauchy-Riemann gradient bound
integral|Dphi|^4 <= (625/4) integral|C Dphi|^4, it gives the H gap
4/1875 times integral|Dphi|^4. An additional nu H therefore gives (3).
It is added after one completed representative has been obtained; no
positive uniform gap is deduced for an unchanged sharp representative.

## Computational and scientific boundary

The proof is existential for arbitrary real coefficients. The rational
generic-contact compiler has polynomial fixed-dimensional bit work when
t and the coefficients are supplied exactly. It does not itself find a
contact, supply an exact zero from approximate data, or guarantee rational
contact coordinates for every rational full-space polynomial. Such costs
must not be inherited from the stratum compiler without a separate
acquisition/elimination argument.

The result is equality of the full H projections, with eventual QC
completion. It leaves fixed-alpha ROC versus QC, sharp positive J_r,
ordinary PC, sharp completion thresholds, external correctness, formal
verification and historical originality unresolved.
