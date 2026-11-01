# Ordinary stopped-martingale receiver for a paid timing window

Status: conditional ordinary probability component, not yet independently reviewed and not yet a finite-N certificate for the rate2 chain. The actual clock observable, derivative acquisition and all admission probabilities must be supplied separately.

Let X be the actual process, T>0 a declared time scale, q an acquired observable, and tau an actual target hitting time. Fix a deterministic horizon d and an admission exit sigma_adm. Stop at sigma=tau wedge sigma_adm wedge d. Every one-step target used in q and its jump bounds must be included. Suppose an actual Dynkin martingale satisfies

 q(X_{t wedge sigma})-q(X_0)=-(t wedge sigma)/T+integral_0^{t wedge sigma} R(X_s) ds+M_t.

Assume, for the stopped process itself (NOT after conditioning on a favorable event),

 |M jumps|<=j, predictable quadratic variation <M>_d<=v,
 integral_0^sigma |R(X_s)| ds<=r,
 q>=-c on the full stopped domain,
 q(X_tau)<=b_tail+c at target exits,
 q(X_0) in[q_lo,q_hi].

All constants are supplied valid bounds, with c,b_tail,r,v,j>=0. If bounds are enforced by additional stopping rules, those are included in sigma_adm and their first-exit probability must be charged. In particular a bracket/residual budget cannot be treated as a conditional martingale theorem.

Let delta_M in(0,1), L=log(2/delta_M), and

 m=jL/3+sqrt(2vL+(jL/3)^2).

The two-sided bounded-jump Freedman bound gives probability at most delta_M that sup_(t<=d)|M_t| exceeds m. If an explicit upper approximation to m is used, its numerical error and bit cost are paid.

Suppose the actual admission failure probability obeys

 P(sigma_adm<=min(tau,d))<=delta_adm,

so a simultaneous adverse exit is explicitly included as failure, including at the deterministic deadline. Choose d/T>q_hi+c+r+m. On the event of no admission failure and |M|<=m, tau>d would imply at t=d

 d/T=q(X_0)-q(X_d)+integral R+M_d<=q_hi+c+r+m,

a contradiction. Hence tau<=d on that event, and the actual target time obeys

 T max(0,q_lo-b_tail-c-r-m) <=tau<=T(q_hi+c+r+m)

with probability at least1-delta_adm-delta_M.

This proves a timing window without assuming its target is reached beforehand. If the target is only an intermediate level, this is NOT a clearance-time theorem. To extend the upper bound, a separately received actual continuation must show clearance occurs within d_rem after tau, uniformly over its actual exit states, with conditional failure at most delta_rem. To extend the lower bound, earlier clearance must be excluded or its probability paid. No reset, independent restart, frozen-fiber distribution, or new source preparation is permitted by this receiver.

A finite-N computational claim additionally requires acquiring q, its pointwise derivative/residual/bracket bounds and all admission constants from the provided model; reporting every failed refinement; and comparing total cost with ordinary SSA, tau-leap/multiscale and finite killed-chain computation under the same accuracy/information. This receiver alone supplies none of those operations and is not a new generic martingale theorem.
