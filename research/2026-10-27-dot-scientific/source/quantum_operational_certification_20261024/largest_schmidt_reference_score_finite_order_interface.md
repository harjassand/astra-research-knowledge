# Largest-coordinate score as a finite commuting-filter target

Status: exact source/interface and conditional reduction, not a sign theorem. No diagnostic is used as payment.

For positive Schmidt weights h=(r,u,v) and diagonal reset B=diag(a,b,c)>=0, let

X=P_(sqrt(r)00+sqrt(u)11+sqrt(v)22)+I3 tensor B.

The distinguished REFERENCE-filter score Q0 differentiates congruence by diag(sqrt(1+epsilon),1,1); this scales BOTH r and a. It is not a derivative changing only the pure main weight unless a=0.

Exact source blocks yield

Q0=(f(H))00+3f(a+r/3)-2(f(O01))00-2(f(O02))00,
H=diag(a,b,c)+sqrt(h)sqrt(h)*,
O0j=diag(a,bj)+(1/2)[sqrt(r),sqrt(hj)]^T[sqrt(r),sqrt(hj)].

Sherman-Morrison receives the exact rational integral

Q0=r integral_0^infinity s/(a+s)^2
 g1(r/(a+s),u/(b+s),v/(c+s)) ds.

The function g1 is the same received scalar one-crossing kernel. Since all three arguments decrease, the kernel is either positive throughout or has one negative-to-positive crossing. Adding a common ACTUAL reset floor b0 to(a,b,c) translates the integral and gives the same second-derivative concavity reduction as in `qutrit_reset_reference_score_spectral_floor_reduction.md`. Thus any negative score reduces to a singular reset, with h fixed.

## Sufficient target

Prove Q0>=0 whenever r>=max(u,v), for arbitrary a,b,c>=0.

The own-noise-zero face is already received by the clean-Schmidt compensated derivative: its pure score

r log[4r(r+u+v)/(3(r+u)(r+v))]

is nonnegative for a largest r, since r^2+r(u+v)-3uv>=0. The remaining companion-zero face a,b>0,c=0 is unpaid. Endpoint u or v tending0 is permitted by continuity, but no sign claim is inferred there.

## Why this receives a finite commuting anchored comparison

Start with X0=3d Phi3+I3 tensor A and a positive reference filter K>=I satisfying[A,K]=0. In their common eigenbasis the filtered source has Schmidt weights h_i=d k_i and reset weights b_i=a_i k_i. If the target above holds, lowering a largest k_i while keeping k_i>=the other weights cannot increase the deficit. Lower it to the next largest level, then continue lowering the tied maximum coordinates until all k_i=1. Each partial derivative has the target sign because its reference weight is maximal; along the actual path the corresponding reset weight scales too, exactly as required by Q0. Integrating gives D(X_K)>=D(X0).

After factoring out lambda_min(K), this would prove D(X_K)>=lambda_min(K)D(X0) for every positive K commuting with A. It would NOT receive noncommuting A,K, arbitrary reference-score positivity, or generic reference-channel monotonicity.

## Narrower finite one-axis subproblem

For K=diag(R,1,1), R>=1, the source parameters are(r,u,v)=(R,1,1), actual reset(a,b,c)=(R a0,b,c). On a companion-zero face the pure baseline is

q_R(s)=2R(R+3)(s-1)/[(R+3s)(R+s+2)(R+2s+1)],

with integral R log[4R(R+2)/(3(R+1)^2)]>=0. A monotone ratio to its crossing-rescaled copy would suffice, just as in the received R=1 companion-zero certificate. The R=1 quadratic crossing brackets must NOT be imported unchanged: for general R the own crossing argument may be arbitrarily large, and the old lower root bracket2u/(u+4) fails in that limit; only the weaker geometric lower bound u/(u+2) is immediately available.

## Obstruction already preserved

Ordinary reference-axis convexity is false even for scalar positive reset: `anchored_reference_axis_convexity_obstruction.md` gives a strictly positive logarithmic coefficient at large filter weight. Hence positive unfiltered tangent cannot be integrated by a generic convexity assertion.
