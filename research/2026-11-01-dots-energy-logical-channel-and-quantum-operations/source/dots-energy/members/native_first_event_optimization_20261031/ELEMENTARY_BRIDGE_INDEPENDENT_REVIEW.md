# Independent local acquisition review: elementary two-state bridge

31 October 2026. PASS as an explicit positive-rate, bounded-work virtual source routine and a sharper exact duration-TV estimate. It does not automatically amend the frozen complete assembly or its ledger.

I read the entire `ELEMENTARY_TWO_STATE_BRIDGE_SOURCE.md` and verified SHA-256 `3c52477dd77f523f986fa4cf32d6169ed313d5009084dd047e49f0a7e5261fb0`.

## 1. Exact laws and bounded rejection

For opposite endpoints the first-event density expands as

 [a exp(-a u) + b exp(-v t + b u)]/[1-exp(-v t)].

The first term is exactly w1 times a decreasing truncated Exp(a) density; the second is w2 times the reflected truncated Exp(b) density. Their weights add to one. No endpoint acceptance test is required.

For equal endpoints the no-event atom is exp(-a t)/P_ii(t). On the complement, changing variables to remaining time x=t-u gives a density proportional to exp(a x)(1-exp(-v x)). This complement is chosen by a fresh Bernoulli test, not used as a rejection normalization or runtime multiplier.

The increasing-exponential proposal accepts with probability 1-exp(-v x). Its stochastic dominance over uniform gives the displayed acceptance lower bound. For the square-root proposal, multiplying density 2x/t^2 by exp(a(x-t))(1-exp(-v x))/(v x) gives exactly the required target up to a scalar. The factors are bounded by one. The overlap-regime lower bounds remain above 1/5: on v t <=21/20 the product bound uses exp(-21/20)(1-exp(-21/20))/(21/20); on v t >=19/20 the uniform average exceeds 1/3. The stated rational exponential estimates are sufficient. A certified regime approximation therefore introduces no exact-boundary decision oracle.

Capping R independent proposals with the stated logarithmic bound gives failure at most eta/[100(K+1)] per invocation. The selected zero contraction on failure is crucial. The output is a subnormalized approximation of the conditional word mean, not a claim that the finite sampler never fails. Fixed reversible loops retaining all proposal seeds and the first accepted index have O(KR) work; the constant expected acceptance does not supply free coherent variable-time execution.

As a diagnostic only, 100 independently selected positive rate/time triples verified the opposite-endpoint mixture identity to relative floating error below 2e-15. The analytic calculation and uniform acceptance bound, not numerical sampling, establish correctness.

## 2. Duration-TV estimate

Opposite-endpoint mixture weights and the two normalized exponential restrictions have the stated derivative bounds. In particular a decreasing truncated exponential has endpoint mass density at most 1/t, and an increasing one at most its rate plus 1/t. Their combination fits well within the conservative constant 32.

For equal endpoints, the logarithmic derivative of the no-event atom is bounded by 2v. Let F(x)=exp(a x)(1-exp(-v x)) and Z(t)=integral_0^t F. Concavity of 1-exp(-v x) gives the lower bound on Z/F(t). The identity

 (z-1+exp(-z))(z+2)-z^2 = z-2+(z+2)exp(-z) >= 0

follows by differentiating and using exp(z)>=1+z. It yields F(t)/Z(t)<=a+2/t, including the continuous a=0 limit. Normalized restriction to nested intervals changes in TV by the integrated endpoint density. Translating from x to u adds at most the maximum density times the translation, since F/Z is monotone on its finite support. Combining this with the atom proves the stated 32(v+1/t_min)|t-t'| bound.

The no-event output must be a common flag for this TV statement; distinct deterministic terminal timestamps would have mutually singular atom locations. The source explicitly uses the correct flag convention. Likewise, crossing the numerical proposal-regime boundary is harmless for this exact kernel comparison because both proposal routines target the same conditional law. No continuity of their raw random-seed maps across that boundary is assumed.

## 3. Finite precision and recursion

All proposal formulas use nonpositive exponential arguments or stable limiting expressions. Small positive rates, durations and denominators enter the required bit precision; they do not generate endpoint-dependent rejection loops. The premise supplies positive encoded/refinable rates, while zero-rate and zero-time cases are explicitly excluded or handled separately rather than divided through.

Midpoint rounding of a uniform under any monotone bounded-range quantile has mean time displacement at most the range times the grid width. The proposed Markov bound therefore controls large displacement without an inverse-density lower bound. Fresh independent uniforms for mixture choices and acceptance tests ensure that threshold errors can be charged conditionally on the preceding proposal. No union over hypothetical inverse-CDF bisection trees is needed in this routine.

The acceptance-coordinate derivative is bounded by a+v (and hence by 2v); the expm1 ratio has a finite derivative at zero. The displayed h_prop and per-operation bad-probability budgets thus cover proposal rounding, decision errors and the K-by-R recursion. Actual arithmetic primitives still need their stated subdivisions. Coupling exact kernels in TV for changed remaining durations is a proof device, not an additional oracle that must be executed.

Using the inherited global retained-duration floor zeta/2 gives Lker,new=32(v+2/zeta). Summing at most K recursion errors and O(K h_time) accumulated duration perturbations yields the stated O((Lker,new+2c)K^2 h_time) contribution, including the separate QQ insertion process. The global tie/order cutoff and original endpoint floor are still paid; removing pz^-2 from this one Lipschitz estimate does not remove all rate/endpoint precision costs.

Coherent inner seeds are unprepared only after the selected word is applied, and numerical/cap failures select zero in the positive operator block. Consequently probability couplings bound the selected mean operator error. This is not a claim of small state-vector error between every pair of coherent seed preparations. The outer physical Kraus coordinates and their L2 timing comparison remain the separately received assembly, not a consequence of this local TV lemma.

## 4. Binding boundary

No load-bearing correction is required. The routine earns an actual bounded-work replacement for the internal two-state bridge sampler and a better duration-conditioning constant. Its use in a complete simulator must explicitly reallocate the source errors and instantiate the new finite source work and precisions. The previous sharp ledger, whole compiler, physical count, private-clock and output guarantees are not silently revised by this local receipt. No new stochastic identity, physical implementation, practical crossover or advantage is asserted.
