# Positive reference-filter score at every unfiltered qutrit-reset seed

Status: independently PASS; see `qutrit_reset_unfiltered_score_independent_audit.md`. Exact companion certificate freshly replayed successfully. This is an infinitesimal theorem, NOT finite reference-filter monotonicity.

Let d>0,A>=0 be any3 by3 reset matrix, and

X=3d Phi3+I3 tensor A.

For a positive semidefinite reference perturbation P, set Z_epsilon=(I3+epsilon P)^(1/2). Then

(d/depsilon) D[(I3 tensor Z_epsilon)X(I3 tensor Z_epsilon)] at0 >=0.

It is strictly positive for P!=0 and A!=0. At A=0 the derivative is0 for every P. The filter direction need not commute with A.

## Actual gradient and covariance

The derivative is Tr(PQ), with

Q=Tr_input[XlogX-2(NX)log(NX)]+RlogR-(log3)R,
R=Tr_input X.

This is acquired directly by differentiating congruences; zero eigenvalues cause no off-support logarithmic derivative because the congruence preserves rank. The expression uses the continuous function xlogx. A matched physical/reference unitary diagonalizes A while preserving Phi3. Matched diagonal phase covariance then makes Q diagonal in that eigenbasis. It suffices to prove all its diagonal entries positive.

For A=diag(a1,a2,a3), the exact source block formula and rational kernel are in `qutrit_reset_anchored_reference_score_interface.md`:

Qi=d integral_0^infinity s/(ai+s)^2 g_i(d/(a1+s),d/(a2+s),d/(a3+s)) ds.

The acquired one-crossing kernel is either positive throughout or has one negative-to-positive crossing along this decreasing path.

## Reduction to singular diagonal reset

`qutrit_reset_reference_score_spectral_floor_reduction.md` proves that any negative coordinate at a faithful A forces a strictly more negative coordinate after subtracting lambda_min(A)I. More strongly, along an added floor b the coordinate is positive above its crossing and concave below it. Thus nonnegative singular boundary scores pay every faithful score. Strict positive singular boundary scores pay strict positivity; if the boundary reset is zero, the positive crossing-endpoint value gives strict positivity for every b>0.

Only two singular faces remain, up to relabeling:

1. Distinguished eigenvalue zero: A=diag(0,b,c).
2. One companion eigenvalue zero: A=diag(a,b,0), a,b>0. Endpoints a=0 or b=0 are separately paid by the distinguished-zero or axisymmetric receivers.

## Distinguished-zero face

`qutrit_reset_zero_own_noise_reference_score_theorem.md` proves nonnegativity, strict for b+c>0, by a pointwise resolvent compensation. With h(z)=z/[(s+1)(s+1+z)], v=s/(b+s),w=s/(c+s), the exact score is the integral of

h(v+w)-h(v/(2-v))-h(w/(2-w))+2h(1)-h(2).

Since h is increasing and concave, J(x,y)=h(x)+h(y)-h(x+y) increases in each argument. Also v/(2-v)<=v<=1 and similarly for w. Therefore the displayed integrand is at least J(1,1)-J(v,w)>=0, strictly away from the pure endpoint. The companion exact polynomial certificate is optional corroboration.

## Companion-zero face

Scale d to1 and suppose a,b>0. Its kernel is negative at s=0 and positive at s=1; it has a unique crossing theta in(0,1). Put

v=(1-theta)/theta, u=b/theta, w=a/theta, z=s/theta.

The crossing equation is the quadratic F=A(u,w)v^2+C(u,w)(2v-u)=0, with A,C strictly positive polynomials. Its positive root satisfies

2u/(u+4)<=v<=u/2.

Let q(s)=s g_i/(a+s)^2 and q0(z)=4(z-1)/[(z+1)(z+3)(3z+1)]. The baseline q0 has integral0, negative below1 and positive above1. Define the removable ratio R(z)=q(theta z)/(q0(z)/theta).

The self-contained exact certificate `qutrit_reset_companion_zero_ratio_certificate.py` reacquires R from the actual kernel. Its derivative numerator, reduced by the quadratic root equation using exact polynomial pseudo-division, equals(z-1)^2 times a polynomial linear in v, divided by a positive power of A. Substituting the lower root bound in its positive-v monomials and the upper bound in its negative-v monomials gives a lower polynomial; multiplying byu+4 yields4066 monomials with nonnegative coefficients. Thus R'(z)>=0. For a,b>0 the lower polynomial is strictly positive at z>0, so R is strictly increasing.

Consequently

Qi=integral_0^infinity [R(z)-R(1)]q0(z) dz>0.

This is an actual signed-integral payment, not a conclusion from single crossing alone. The ratio is finite at infinity; its singularity at1 is removable by the same actual crossing equation. Baseline and source integrals converge. The case b=0 was independently received in `qutrit_reset_axis_reference_score_theorem.md`; the case a=0 belongs to the first face.

## Consequences and limits

Q is positive definite whenever A!=0 and zero at A=0. This includes noncommuting positive reference-filter tangents because Tr(PQ)>0 for every nonzero P>=0. Homogeneity gives TrQ=D(X), furnishing another proof of the already received unfiltered qutrit-reset whole value.

It does NOT imply the finite inequality D[(I tensor Z)X(I tensor Z*)]>=lambda_min(Z*Z)D(X), nor any accepted-only GLS comparison. After a finite filter the seed is no longer maximally entangled and the acquired unfiltered score theorem cannot be reapplied. Reference-axis convexity is itself false: see `anchored_reference_axis_convexity_obstruction.md`.
