# Root shifted-barrier well current with the old paid well ceiling

Status: NEW theorem candidate, independent review pending. This is an explicit reconstruction of the changed current, not a silent transfer of the old source.

Use exactly the received original quartic/constant-SPD model and notation in WELL_REDISTRIBUTION_CURRENT.md. Set b=1/2, v*=1+kappa, v_b=1+9kappa/16. Choose ANY barrier density parameter a0 in[v_b,v*]. In A set a(y)=max(v(y),a0); in S set a=a0. Let J(y)=int_-infinity^y q(t)1_A(t)dt and

 j_y=J*pi_a,
 j_z=q F_v where v<a0, F_v=-(z/4)int_v^a0 pi_s/s ds,
 j_z=-J v' z pi_v/(4v) where v>=a0,
 j_z=0 in S.

The old pointwise homogeneous continuity identities now give div j=rho1_A for this NEW current. Normal y-flux matches at v=a0 and y=-b, so no interface delta source arises. The transverse component may jump without contributing to y-normal divergence. Its exact slab price is beta M^2 R_a with

 R_a=int_-b^b [a0^2/(2a0-v(y))]^alpha dy.

The denominator is >=2v_b-v*=1+kappa/8>0. I claim the entire OLD E_rest ceiling in the accepted well theorem remains a valid well price for this changed current. Here is the needed separate proof.

The changeover on the outer well side is x_a=sqrt(1+sqrt((a0-1)/kappa)). Since a0>=v_b and a0<=v*,

 sqrt(7/4)<=x_a<=sqrt(2), in particular x_a>5/4.

1. Homotopy transverse cost. Its support length x_a-b<1, integration endpoint a0<=v*, and a0-v<=kappa. The same Cauchy/moment bound is dominated by K*kappa^2*G1^alpha, where G1=v*^2/(2v*-1). Monotonicity of s^2/(2s-v) for s>=v, followed by the same decreasing-in-v bound, proves this domination. No new fiber norm is assumed.

2. Near-well longitudinal cost. On x in[b,1+delta], delta=1/alpha<=1/4, the old inequality v(x)<=v_b<=a0 makes the current's density parameter constant. Since a^2/(2a-v) increases in a whenever a>=v, its price is bounded by the old M^2(1+delta-b)Gb^alpha, Gb=v*^2/(2v*-v_b).

3. Remaining constant-density interval. On x in[1+delta,x_a], the length is<1/2 and v<=a0. The old cumulative mass estimate J(-x)<=v^(1-alpha)/[(alpha-1)v'] and v'>=8kappa delta applies. Monotonicity in a0<=v* and v>=1 bounds this longitudinal price by the old v*^2 G1^alpha/[128kappa^2(alpha-1)^2 delta^2].

4. Conditional far tail. For x>=x_a the current is the ordinary conditional-dilation current, with global correction<=Dmax. Its old pointwise integrable ceiling is valid wherever x>1. Because x_a>5/4, extending the integral down to5/4 is still conservative, giving (1+Dmax)/[16kappa^2(alpha-1)^2]. This explicitly charges the newly conditional band below sqrt(2), rather than ignoring it.

Thus, with the SAME explicit E_rest from the old accepted theorem,

 Q_A<=beta[M^2 R_a+E_rest].

Reflecting the left current at y=0 as in the separately accepted global odd construction gives

 Q_(1A-1B)<=beta[M^2 R_a+2E_rest].

Both are finite actual source energies on the original generator. No angular sampler, unknown normalizer evaluation, new physical mobility, or optimal current oracle is supplied. Subsequent energy-sensitive trial/residual joins must use their own newly received source and Dirichlet costs.

The proposed a0=v*(1-1/(2alpha)) is admitted whenever alpha>=8v*/(7kappa), in addition to alpha>=4. That condition must be checked, not assumed at small kappa. This note gives a finite exact current bound; it does NOT receive the formal asymptotic cancellation or the numerical primal integral.
