# Single-crossing resolvent rank collapse at a PSD minimum

This is an algebraic stationary-rank lemma. It needs neither convexity of the objective nor a claim that an indefinite congruence preserves an integrated inertia bound.

Let Q>=0 have support P, let R be any rectangular matrix, let kappa>0 and t>0. Suppose its positive-support stationary equation is

 kappa P=P [integral_0^infinity (Q+sI)^{-1} R W_s R*(Q+sI)^{-1} ds] P,

where the integral converges on the positive support and W_s is Hermitian with

 W_s<=0 for 0<s<t,   W_s>=0 for s>t.

Then rank Q<=rank R.

## Proof

If rank Q>rank R, choose nonzero u in range P with R*u=0. The vector (Q+tI)u also lies in range P. Multiply the stationary equation on the right by Q+tI and sandwich with u. The left side is

 kappa <u,(Q+tI)u>>0.

Put a_s=R*(Q+sI)^{-1}u. The resolvent identity and R*u=0 give

 R*(Q+sI)^{-1}(Q+tI)u=(t-s)a_s.

Thus the right side is

 integral_0^infinity (t-s) a_s* W_s a_s ds<=0,

a contradiction. This proves the rank bound.

The same proof works if W_s depends on the current Q, as long as its common Loewner sign threshold is valid at that stationary point. Coercivity/existence of a minimum must be supplied by the application. The lemma does NOT apply when only individual eigenvalues of W_s change sign at different thresholds, or when the common threshold is inferred from an unproved commutation.

## Proven application

The rank-one-main balanced WH3 bath functional has R=d, t=h/2, and scalar W_s=(a_s-1/2)/[(1+a_s r_s)(1+r_s/2)], a_s=2s/(h+2s), r_s=d*(Q+sI)^{-1}d. It follows that every minimizing bath has rank at most one. The complete coercive value argument is in `rank_one_main_arbitrary_bath_entropy_theorem.md`.

The short proof above was supplied by the SIC-partition worker after the scalar Cauchy-ratio proof had established the rank-one application independently.
