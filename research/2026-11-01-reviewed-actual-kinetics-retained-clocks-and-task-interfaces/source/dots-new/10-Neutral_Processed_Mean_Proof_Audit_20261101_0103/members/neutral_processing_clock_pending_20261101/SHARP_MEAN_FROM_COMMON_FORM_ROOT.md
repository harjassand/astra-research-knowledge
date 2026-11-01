# Root corollary: tight controlled mean from the received reference tail

Status: NEW conditional derivation, independent review pending. Depends on the separate common-form proof, not on uniform CDF accuracy alone.

Receive actual killed propagation with the two chronological common-form energy and sub-Markov premises of COMMON_FORM_UNIFORM_MEAN_ROOT.md. Write

 Href(t)=<1_D,exp(-tA)1_D>, Q_D=integral_0^infinity Href(t)dt,
 G(t)=2/t^2 integral_0^t s Href(s)ds.

The common-form theorem gives Hactual(t)=<1_D,P_0,t1_D><=G(t/2). For initial Gibbs|A of unnormalized mass M, actual survival S_a(t)<=Hactual(t)/M by positivity.

Also receive uniform absolute Gibbs|A survival approximations

 |S_a(t)-exp(-kt)|<=delta_a,
 |S_ref(t)-exp(-kt)|<=delta_r,

and Q_D<=Qupper with qbar=k Qupper/M>=1. The latter follows in the intended current construction from Qupper=B_total and k=C0/M, giving qbar=1+epsilon. All symbols refer to the SAME reference measure/model; no change of generator or initialization is free.

Tonelli gives the exact reference-envelope tail identity

 (1/M) integral_L^infinity G(t/2)dt
 =4Q_D/M -(4/M) integral_0^(L/2) (1-2s/L)Href(s)ds.

Positivity gives Href(s)>=M S_ref(s)>=M(exp(-ks)-delta_r). With ell=kL>0 this yields

 k integral_L^infinity S_a(t)dt
 <=4(qbar-1)+8(1-exp(-ell/2))/ell+delta_r*ell.

The bound is valid even where exp(-ks)-delta_r is negative; replacing it by zero can only sharpen the calculation. No subtraction of infinite quantities occurs because Q_D is finite by the received full-current bound.

Integrate the actual CDF bound on [0,L] and combine:

 1-exp(-ell)-delta_a*ell <= k E_A tau
 <=1-exp(-ell)+4(qbar-1)
   +8(1-exp(-ell/2))/ell+(delta_a+delta_r)*ell.

The lower bound can be clipped at0; the upper can be intersected with the separate4qbar bound. These are deterministic mathematical bounds, not numerical code receipts.

If Dsum=delta_a+delta_r>0, choose ell=sqrt(8/Dsum) to obtain the simpler safe upper

 k E_A tau <=1+4(qbar-1)+2sqrt(8 Dsum).

For 0<delta_a<1, ell=log(1/delta_a) gives lower

 k E_A tau >=1-delta_a[1+log(1/delta_a)].

When qbar->1 and both uniform survival errors vanish, controlled means therefore converge to1/k uniformly over all received protocols, even with no global mixing gap. No assertion of finite second/exponential moments follows. If delta_a=0 the actual survival is exactly exp(-kt), and its mean is exactly1/k; no limiting optimization is necessary.

This repairs no prior false claim: the earlier warning was specifically that absolute CDF error alone does not control an unbounded mean. The new information is the entire reference common-form tail envelope with an independently bounded full-source inverse form. Initial preparation error merely in total variation still does not control unbounded means; the actual stated initialization/common-form domination must remain earned.
