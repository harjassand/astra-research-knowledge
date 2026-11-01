# Strict mean increase needs only a short FIXED-amplitude pulse

This strengthens and simplifies the finite-rate limit argument in
TIME_DEPENDENT_MIXING_CAN_STRICTLY_INCREASE_MEAN.md (SHA-256
c6d797b8a9a8d6ac9ca9ed4bff8afa52a9d0f4120cb291bcca8bd71874361484).
All its definitions A,C,m,v and u(t) are unchanged. Select a sufficiently
small positive calendar time t so that u_1(t)>u_0(t).

Fix ANY finite R>0, for example R=1. Apply A+RC for duration epsilon starting
at t, and A otherwise. Let J(epsilon) be total mean lifetime from m. Exact
splitting of the occupation integral gives

    J(epsilon)=int_0^t <1,u(s)>_m ds
      +int_0^epsilon <1,exp[-s(A+RC)]u(t)>_m ds
      +<v,exp[-epsilon(A+RC)]u(t)>_m.

Finite-dimensional differentiation at epsilon=0, together with Av=1, gives

    J'(0)=<1,u(t)>_m-<v,(A+RC)u(t)>_m
         =-R<v,Cu(t)>_m
         =R(v_0-v_1)(u_1(t)-u_0(t))/3>0.

Thus J(epsilon)>J(0)=Q for all sufficiently small positive epsilon. The pulse
amplitude R remains FIXED and finite; no arbitrarily strong processing,
instantaneous permutation, intervention limit, source observation, or state
feedback is needed. The reference killed chain and full reference Q also stay
fixed. The extra form RC is nonnegative, reversible, common-measure preserving,
and annihilates h=1_D on both sides at every time.

This is a strict-increase boundary, not an unbounded-ratio counterexample.
The nonautonomous constant-four principle and sharp near-clock limit remain
unchallenged. The rare-gadget near-clock embedding described in README.md
scales this positive first variation by eta and preserves all receiving.

Status: exact local first-variation proof; independent review pending.
