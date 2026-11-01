# Receiving consequence of the independently accepted global Foster inequality

This is an ordinary countable-state CTMC argument for the exact rate-2 model, not another network construction or a runtime certificate.

Let lambda=1/60000 and take the finite unevaluated Nstar earned in the analytic receipt. Since the head {N<Nstar} is finite and all rates/actual successor values are finite, define
 K=max(0,max_{N<Nstar}[LW+lambda W]).
Then globally LW<=-lambda W+K. K exists but has not been evaluated.

Nonexplosion, irreducibility and finite-horizon integrability were established in the analytic receipt. In particular N_s<=N_0+I_s for unit Poisson immigration, W<=21.05 r^N exp((3N/200)^(1/3)), and rates grow at most quadratically in N. Localized integrating-factor Dynkin and dominated convergence therefore give
 E_x W(X_t)<=e^(-lambda t)W(x)+(K/lambda)(1-e^(-lambda t)).

Let mu_T=(1/T) integral_0^T Law_x(X_t)dt. Its W moment is <=W(x)/(lambda T)+K/lambda. Since W>=3999r^N/4000 and each N sublevel is finite, these measures are tight as T tends to infinity. A subsequence converges in total variation on the countable state space to a probability pi. For each s>=0,
 ||mu_T P_s-mu_T||_TV<=2s/T.
Contraction of total variation by the transition kernel implies pi P_s=pi. Fatou applied to finite partial sums gives pi(W)<=K/lambda, without subtracting infinite stationary generator terms.

Consequently
 pi[r^N] <= (4000/3999) K/lambda < infinity,
 r=1000001/1000000.
Equivalently, the invariant law has a nonzero exponential moment at theta=log(1000001/1000000). This theta is explicit; the finite constant involving K is not evaluated. No assertion about every theta>0 is made.

Irreducibility makes the invariant probability unique and the chain positive recurrent. In this model even pi of the exit rate is finite: the rate is bounded by1+N+11N^2, whose pi expectation follows from the exponential moment. Thus ordinary CTMC recurrence receiving has no hidden infinite-exit-rate issue.

This consequence is contingent precisely on the independently accepted global proof and exact stated model. It does not upgrade the earlier merely local linear-clip components, supply an algorithm for acquiring Nstar, or authorize extrapolation to other rates or architectures.
