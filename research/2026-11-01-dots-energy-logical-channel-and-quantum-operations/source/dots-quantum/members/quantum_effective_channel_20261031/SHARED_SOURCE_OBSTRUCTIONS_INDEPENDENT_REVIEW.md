# Independent review: two shared-source local-fault obstructions

Verdict: scoped mathematical PASS. Neither example contradicts the accepted global-sign logical-channel theorem, nor establishes a lower bound against all recovery/control methods.

Fully read on 2026-10-31:

* SHARED_BATH_LOCAL_SIGN_OBSTRUCTION.md, SHA-256 bc6bd89df7942a8cc60ffdea2b4b8ce5a0eda3b34dac4f3d8fac4732f6f965c0.
* SHARED_SOURCE_LOCAL_FAULT_OBSTRUCTION.md, SHA-256 d33354f4fc64eddaf8119d5d8743dc368d0c2c759cffe3afb6b8e91e28a889cd.

## Stationary telegraph example

Conditional on the common integrated phase W, independent private per-site signs average each local unitary into the dephasing mixture with probability sin^2 W. The full averaged channel is therefore a positive mixture of product Pauli channels, and a specified k-site inclusion probability is exactly E sin^{2k} W. This is a channel-identifiable Pauli coefficient, not an arbitrary jump unraveling.

For exactly one rate-lambda telegraph flip, the unnormalized flip-time density is lambda exp(−lambda t) on (0,t). Including both stationary initial signs and the change of variables W=+/−sqrt(gamma lambda)(2u−t) gives precisely lambda exp(−lambda t)/(2sqrt(gamma lambda)) on the stated phase interval. No missing factor of two occurs.

Let a=sqrt(gamma lambda)t−pi/2>0. A sufficient integer support threshold is k>=max(1,ceil(1/(4a^2))); endpoints at the support boundary have zero Lebesgue measure and do not affect the integral. On |v|<=1/(2sqrt(k)), cos(v)>=1−1/(8k), and Bernoulli's inequality gives cos(v)^{2k}>=3/4. Multiplying by the interval length 1/sqrt(k) proves exactly the source's lower coefficient 3lambda exp(−lambda t)/(8sqrt(gamma lambda)). It eventually exceeds every p_eff^k with fixed p_eff<1. The coefficient may be exceedingly small; the conclusion is asymptotic in device size at fixed physical parameters, not a claimed practically sized fault floor.

The no-flip atom at phases pi/2 modulo pi gives the stronger constant lower bound exp(−lambda t), as stated. The fixed-N multiple-epoch extension is separately proved for the Gaussian common-field model: after local-sign averaging, the single-site error probability is (1−product cos(2W_j))/2. A small cube around (pi/2,0,...,0) has positive density, volume proportional to k^{-N/2}, and conditional k-site inclusion probability bounded below by a positive constant. This Gaussian statement does not claim a uniform finite-telegraph-rate/many-epoch limit or a result when N grows with k.

The distinction between averaging generators and averaging finite-time channels is load-bearing and correct. Independent local signs generally change each branch's effective Gram matrix; averaging exp(tL_sign) is not exp(t average L_sign). A single global sign leaves the quadratic target unchanged branchwise, which is why the accepted global-sign theorem is unaffected.

## One excited damping source

For L=sqrt(2)|0><1|, H=|1><1|, the source population decays at rate 2lambda and G†H=−2H. The interaction H tensor sum xi_i Z_i commutes with the source energy, cannot excite a dark source, and causes no energy injection. Starting excited, there is at most one physical jump, whose waiting time is Exp(2lambda) independently of the system state.

At T=pi/(2sqrt(lambda)), the no-jump event has probability exp(−pi sqrt(lambda)). Its system unitary is a product of Z_i up to irrelevant phases, for every sign choice. Earlier jump times give product rotations stopped at that time; independent-sign averaging yields positive product dephasing mixtures. Hence the all-n-Z Pauli coefficient is at least the no-jump probability. Choosing n>log(q)/log(p) violates any asserted n-independent local-stochastic parameter p<1.

This example explicitly has warm initial energy E0=1 and global interaction norm b=n. It neither satisfies a cold-input premise nor escapes the global-norm costs of the accepted logical bounds. A small number of source jumps or zero injection alone does not control the weight of faults caused by an unbounded shared fanout.

## Boundary of the conclusion

Both results identify a missing high-order spatial/probabilistic premise in a proposed many-qubit inference. They do not rule out bounded-degree sources, independently refreshed local reservoirs, schedules whose resources scale with the requested support/error, recovery tailored to correlated faults, or additional acquired cluster/tail bounds. No source/sign leakage is required for either obstruction. No computational hardness, experimental relevance threshold, or novelty claim is inferred.
