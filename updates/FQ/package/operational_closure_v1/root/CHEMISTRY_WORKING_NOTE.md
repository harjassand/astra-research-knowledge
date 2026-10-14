# Aggregate-activity safety certificate — root working derivation

Status: internal conditional mathematics; physical acquisition and novelty UNKNOWN.

Consider unknown hidden reversible elementary mass-action pairs with reactants alpha_r, products beta_r, jump s_r=beta_r-alpha_r. Each pair is individually balanced at a measured positive baseline c, with one-way flux w_r>0. The visible designed subsystem is separately stationary at c. Unknown support is allowed; individual hidden detailed balance is an essential independent assumption, stronger than observed stationarity. Let Q=2 sum_r w_r s_r s_r^T be the hidden subsystem instantaneous jump covariance in consistent concentration/volume units. Shift c'=c exp(h) at fixed temperature and unchanged rates/gates. Acquire a bound |alpha_r dot h|,|beta_r dot h|<=M for every hidden pair, e.g. from a genuinely justified molecularity bound and the displacement.

Then F_H(c')=sum_r w_r (exp(alpha_r dot h)-exp(beta_r dot h))s_r. The mean-value theorem and weighted Cauchy give, for any output vector z,

|z dot F_H(c')| <= exp(M)/2 sqrt[(z^T Q z)(h^T Q h)].

Moreover -h dot F_H(c') lies between exp(-M) h^T Q h/2 and exp(M) h^T Q h/2. Therefore Q_h=0 iff every active hidden pair remains individually balanced at c', iff the hidden net drift at c' vanishes (last equivalence uses the nonnegative dissipation projection). Positive covariance prevents cancellation of zero-net hidden exchange.

This does not infer Q from noisy long-time concentration covariance, and does not grant reaction-resolved observation. Total covariance can conservatively replace hidden Q if visible terms are positive semidefinite and both projected bounds are used. Independent upper confidence bounds on projected Q values propagate monotonically. Subtraction of noisy visible covariances requires a certified PSD enclosure; naive subtraction is invalid. Finite sample nonobservation never proves exact Q_h=0.

Failure without individual detailed balance: a driven cycle can have zero baseline species drift while a concentration shift preserves every affinity but changes reaction speeds differently, yielding nonzero target drift even with Q_h=0. Invisible catalytic species and unmeasured coordinates can likewise invalidate a projected certificate. Drift residual is not a stability/steady-state error bound without an acquired contraction/resolvent margin. A direct target drift challenge may be cheaper and requires weaker assumptions, so it is a mandatory competitor.

Physical idea: measure a task-aligned scalar chemical jump activity to expose a dormant exchange before a large relocation. Actual molecule-count bandwidth, reporter fidelity, transport terms, units, baseline balance, degree bound and physical target preparation are open. This is not an established chemical capability.
