# Robust rare conductance from acquired radial envelopes

Status: new construction, independent review pending. Earlier freezes are unchanged.
The engine is ordinary unnormalized Dirichlet comparison, not a novelty claim.

## 1. Task and information reduction

Predict k_F=cap_mu,M(A,B)/mu(A) for A={y<=-1/2}, B={y>=1/2}, a full-fiber
reversible diffusion with unit longitudinal mobility, fixed finite SPD transverse
M, zero cross mobility and noise covariance2 diag(1,M)/beta. Actual physical
membership is not inferred from potential data. This is equilibrium conductance,
not an arbitrary-start first-passage time or a projected Markov model.

Let U=sum_d U_d be a nonnegative-component polynomial with degrees2<=d<=p and an
acquired coercive component. The TRUE F need not equal U(s(y)z), or have a known
partition. Suppose acquired scalar functions l,u>0 satisfy, globally,

    U(l(y)z) <= F(y,z) <= U(u(y)z).                    (E)

Uniform angular coefficient rescaling belongs inside the SAME anchor U, not in
the error. We do not assume U's partition, angular distribution, mixing time,
convexity, committor, or microscopic kinetic matrix has been reconstructed.
For the actual raw grammar below all premises are verified, not oracle supplied.

## 2. Unnormalized comparison: keep the slab and basin separate

Write C_F=inf_h beta^-1 integral_slab [h_y^2+grad_z h^T M grad_z h]e^-betaF dy dz
and M_F=int_A e^-betaF. Then k_F=C_F/M_F: the GLOBAL partition cancels.
Only the slab potential affects C_F. Basin mass requires the entire left tail.
Pointwise density ordering gives

    C_U(u.) <= C_F <= C_U(l.),
    Z_U MA(u) <= M_F <= Z_U MA(l),

where Z_U=int e^-betaU and MA(r)=int_A r(y)^-m dy.
This follows by comparing the Dirichlet integrand for every admissible function,
then taking infima. It does not require any kinetic approximation.

For r=l, scalar trial profiles give C_U(l.)<=Z_U/[beta R0(l)],
R0(l)=int_slab l(y)^m dy. For r=u, choose u0>=max_slab u and define

    Rplus(u)=int_slab [u0^(2p)/(2u0^p-u(y)^p)]^(m/p)dy.

The earlier spatial-dilation Jensen argument applies with center reference u0:
for r=u/u0<=1, nonnegative components imply
2U(u0z)-U(u(y)z)>=U(u0(2-r^p)^(1/p)z).
Fixed-fiber Cauchy and Jensen give C_U(u.)>=Z_U/[beta Rplus(u)].
The reference need not be an attained maximum. Therefore

    1/[beta MA(l) Rplus(u)] <= k_F
       <=1/[beta MA(u) R0(l)].                       (R)

The SAME unknown Z_U cancels exactly in BOTH bounds. We do not compare normalized
capacities while forgetting their normalizer. No exact conditional distribution of
F itself is required. The common scalar envelopes, not full internal information,
are sufficient for this task. Numerical receiving must enclose FOUR scalar
integrals and separately check the requested TOTAL interval width.

## 3. Strong ordinary global comparisons are retained

For a global density ratio e^-b<=e^-beta(F-F0)<=e^-a, unnormalized capacity and
basin mass imply e^-(b-a) k_F0<=k_F<=e^(b-a) k_F0. Constant energy offsets cancel;
this is the elementary bounded-density/Holley–Stroock style comparison, not ours
to claim as novel. Unbounded polynomial energy perturbations often have no finite
additive oscillation, even when the radial envelopes below are tight.

For pure homogeneous U of degree p, a multiplicative energy envelope
c_-F0<=F<=c_+F0 gives the ordinary partition penalty(c_+/c_-)^(m/p) per endpoint.
These penalties multiply the nominal STRUCTURAL family outer endpoints, not an
asserted equality for the actual fixed-M rate under uniform energy scaling.
Uniformly rescaling a fiber energy can change its actual committor and, after a
coordinate change, the effective transverse mobility. Its family-level prediction
still belongs inside the previously accepted common outer bracket.
For positive mixed degrees with d_min<=d<=p, spatial scaling gives, for c>=1,

    c^(-m/d_min) Z_U(beta) <= Z_U(beta*c)
                              <=c^(-m/p) Z_U(beta).

For c<=1 reverse the corresponding scaling directions. Thus the coarser exponent
m/d_min gives an ordinary multiplicative-energy penalty. It remains available.
A global radial envelope l=a s,u=b s specializes(R) to the nominal bounds times
(a/b)^m below and(b/a)^m above. It is sound, but may charge error in regions that
carry negligible resistance or basin mass. The localized integrals in(R) retain
that information rather than declaring a worst-case sufficient bound necessary.

## 4. The dilation defect and what it loses

For nominal s define R=F_y-(s'/s)z.grad_zF. Along w=s(y)z held fixed,

    d/dy F(y,w/s(y))=R(y,w/s(y)).

If |R|<=eta(y)F and F>0, Gronwall bounds this transformed energy relative to an
anchor by exp(+/-int eta). Zero-energy points follow by the corresponding linear
inequality/continuity. A finite global integral gives an energy envelope; the
ordinary comparison above then applies. One may validate this componentwise for
nonnegative atoms, but there is no global positivity oracle for arbitrary F.

The unsigned integral forgets cancellation: a defect may return to zero at the
barrier, wells and tails despite nonzero total variation. The direct radial
profile inequalities in(E) can retain this information. Neither a uniform angular
rescaling (R=0) nor a harmless anchor reparameterization is charged as macro error.
Small Euclidean rotations are NOT automatically small defects for sharp angular
energies: for U=(lambda z1^2+z2^2)/2, a rotation through theta changes the value on
the soft axis by the ratio lambda*sin(theta)^2+cos(theta)^2. Arbitrarily tiny
nonzero theta gives unbounded relative error as lambda grows. Conditioning or an
actual envelope is required; generic rotated inputs may be UNKNOWN here.

## 5. Two localized envelope shapes, not exactly factorized true models

Let t=y^2, s=1+kappa(1-t)^2 and

    e_sensitive=t/(1+t)^2,
    e_flat=t(t-1)^2/(1+t)^4.

Both are nonnegative, smooth and vanish at y=0 and infinity. Their suprema are
1/4 and1/16 respectively; write v=t/(1+t)^2, then e_flat=v(1-4v).
Set l=s(1-delta e), u=s(1+delta e),
0<=delta<=kappa/[2(1+kappa)]. Both remain positive. They decrease on[0,1] and
increase on[1,infinity), so u0=s(0) is a valid slab reference. Here are sufficient
uniform derivative bounds, not a sampled sign test:

For e_sensitive, e_t=(1-t)/(1+t)^3, so
u_t=(t-1)[2kappa(1+delta e)-delta s/(1+t)^3].
Use s<=s0(1+t)^2 and delta<=kappa/(2s0); the bracket is positive.
l_t has the corresponding PLUS second term and is positive in its bracket.

For e_flat, e_t=-(t-1)(t^2-6t+1)/(1+t)^5. Since
|t^2-6t+1|<=2(1+t)^2, the common bracket for either l or u is at least
2kappa(1-delta/4)-2delta s0>0. Thus the asserted monotonic intervals are earned.
No high-dimensional monotonicity or convexity of F is assumed.

The actual grammar permits different univariate coefficient profiles for EVERY
nonnegative quadratic/quartic atom. It validates inequalities against these
l,u; it does not require each profile to have the nominal shape, or F to have any
exact spatial dilation. Unknown angular structure can therefore vary with y.

## 6. Complete raw acquisition and bounded polynomial positivity certificates

Input is the COMPLETE rational potential F=N(x)/(1+x_axis^2)^16. The denominator
is part of the exact program syntax, not an implicit tail truncation. The numerator
is an expanded rational sparse polynomial in physical coordinates, total degree
at most52. Its positive pure quadratic part identifies the unique absent y axis;
this must match the denominator's declared axis. No basis is supplied for free.

Group numerator coefficients by their transverse monomial phi_j: positive pure
quadratics, pure quartics, or square-square quartics. Each macro coefficient N_j(t)
has degree at most16+2d_j, d_j=2 or4, and N_j(0)>0. All transverse quadratic axes
must be present. From the first quadratic profile's leading/base ratio acquire
r=kappa/(1+kappa) by an EXACT rational square root, require0<r<1, and set
kappa=r/(1-r). This is a sufficient finder; non-square proposals can be UNKNOWN.
No fit alone admits the model. Set c_j=N_j(0)/s0^d_j and U=sum c_j phi_j.
The coefficients are read to validate this anchor; no partition or angular solver
is used or returned. Positive quadratic c_j acquire U>=q_min||z||^2.

Write B_+/-=(1+t)^4 +/-delta E(t), with E=t(1+t)^2 or t(t-1)^2.
For EVERY profile verify globally on t>=0 the two polynomial inequalities

    s^d B_-^d (1+t)^(16-4d) <= N_j(t)/c_j
         <=s^d B_+^d (1+t)^(16-4d).                   (V)

They are exactly(E) multiplied by the strictly positive common denominator.
Each certificate uses rational Bernstein subdivision on the projective interval
x=t/(1+t) in[0,1]. For P(t)=sum a_k t^k of degree D, the transformed polynomial
(1-x)^D P(x/(1-x)) has Bernstein coefficients a_k/binom(D,k). Nonnegative
coefficients on every covering dyadic subinterval certify P>=0. de Casteljau
subdivision is exact rational arithmetic; strict node/depth/operand budgets may
return UNKNOWN on a true inequality. No arbitrary polynomial-positivity oracle,
complete SOS search or hidden sample grid is assumed. Identical NORMALIZED
profiles can share proofs, but every raw coefficient and exponent is still read,
validated, hashed, and bound. This respects irrelevant uniform atom rescalings.

## 7. Actual global diffusion and infinite tails are earned

The received value envelope implies finite Gibbs mass, since l>=c s with c>0,
and U has quadratic coercivity. For T>1,

    int_T^infinity l^-m <= (1-delta sup e)^-m
       kappa^-m(1-T^-2)^(-2m) T^(1-4m)/(4m-1).

For u>=s the same tail without the first factor suffices. The left basin equals
the right tail only because this grammar has even y dependence. These are full
infinite tails, not finite-box substitute dynamics.

The actual rational profile is a_j=N_j/(1+t)^16>0. Let
h=min(1/8,kappa/2)*(1-delta sup e)>0. The inequality
s>=min(1/8,kappa/2)(1+t)^2 follows from(1+t)^2<=2(t-1)^2+8.
By(V), N_j>=c_j h^d_j(1+t)^(16+2d_j).
If L_j is the sum of absolute coefficients of N_j/c_j and D_j its degree, then
|2t N'_j/N_j|<=2D_j L_j/h^d_j. Hence

    y a'_j/(d_j a_j) >=-[2D_j L_j/h^d_j+32]/d_j.

Acquire K=1+max_j of the right-hand positive bound. Since each atom is nonnegative,
z.grad_zF=sum_j d_j a_j phi_j, the Lyapunov function
V=1+y^2+K z^T M^-1 z has LV<=2(1+Km)/beta. Thus the actual smooth rational SDE is
nonexplosive for every finite constant SPD M. K may be large; its exact algebra is
paid but it does not enter the conductance width. No actual inverse M is computed.

## 8. Sensitivity is real, while a global error floor is not

A separate exact asymptotic obstruction is given in SENSITIVITY_CANDIDATE.md.
Even with an arbitrarily small fixed sensitive-profile perturbation, actual full
rates can change by exp(Theta(m*delta)). Thus sub1% prediction requires charging
relevant geometric accuracy. In contrast, e_flat vanishes at the barrier and
basin concentration points. Its resistance/mass penalties have finite limits as
m grows. Our finite exact integral receiver, not this asymptotic statement, must
establish any numerical requested width. No empirical parameter accuracy or
physical calibration is supplied by mathematical admission.
