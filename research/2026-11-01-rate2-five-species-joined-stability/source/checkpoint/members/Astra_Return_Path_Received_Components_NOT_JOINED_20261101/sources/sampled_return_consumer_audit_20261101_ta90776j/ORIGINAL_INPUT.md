# Conditional consumer: paid activation blocks imply a stationary exponential moment

Status: ordinary probabilistic component, newly written for this investigation; not yet independently reviewed. The rate2 network has NOT earned the block hypothesis below. This note isolates what its constructor must supply and charges the entire holding interval. No novelty claim.

Let X be an irreducible nonexplosive countable-state continuous-time Markov chain with integer total population n(X). Assume every finite population sublevel is finite. On one probability space, population satisfies n(X_t)<=n(X_0)+I_t, where I is a rate-lambda Poisson immigration counting process. No independence between I and a success event is assumed.

For each initial state x select a deterministic block duration d(x), with d(x)>=d0>0 and d(x)<=D(1+n(x)^a), where 0<a<1. This is a state-dependent sampling schedule, not a reset or an intervention. Assume there are c>0, p<infinity, delta in (0,1), and n0 such that uniformly over every x with n=n(x)>=n0,

 P_x[n(X_d)>(1-delta)n] <= p exp(-c n^a).                     (H)

The duration and hypothesis must cover activation, crossing the interface, actual removal, continuing immigration and all adverse channels. A statement only for a special initial ray is not (H).

Claim: for some theta>0 the sampled chain has a geometric Foster drift with V(x)=exp(theta n(x)); its occupation measure induces an invariant probability for X, with a positive exponential population moment.

Proof. Split success and failure B. Success contributes at most exp(theta(1-delta)n). By Cauchy--Schwarz, immigration domination, and the EXACT Poisson moment generating function, the failure contribution is at most

 exp(theta n) sqrt(p) exp[-c n^a/2 + lambda d(x)(exp(2theta)-1)/2].

Choose theta>0 so lambda D(exp(2theta)-1)<c (if lambda=0 this constraint is empty). The bracket relative to V tends to zero as n tends to infinity. Thus QV<=rho V+b 1_C for a finite C and rho<1, with Q(x,.)=P_{d(x)}(x,.). The finite-C bound is finite by Poisson domination and the bounded finite set of durations. Standard countable-state Foster recurrence gives an invariant law nu of Q with nu(V)<infinity. Q is irreducible: any finite positive-rate CTMC path can occur within any positive duration, followed by holding at its endpoint. Aperiodicity is also available from positive no-jump probability, but is unnecessary here.

Let h=nu(d). It is positive and finite since d0<=d<=D(1+n^a) and nu(V)<infinity. Define

 pi(f)=h^(-1) sum_x nu(x) E_x integral_0^{d(x)} f(X_t) dt.

This is an invariant probability of the original continuous-time chain, not just of its sampled kernel. For bounded f and fixed s, the Markov property inside the interval gives the difference of the integrals over [d,d+s] and [0,s]. The strong Markov property at the sampling time and nu Q=nu cancel those expectations. All integrals involved are absolutely integrable since f is bounded and h<infinity. Hence pi(P_s f)=pi(f).

For any 0<eta<theta, Poisson domination yields

 E_x integral_0^d exp(eta n(X_t)) dt
 <= d exp[eta n + lambda(exp(eta)-1)d]
 <= K_eta exp(theta n)

for a finite K_eta, because a<1. Therefore pi(exp(eta n))<infinity. Irreducibility gives uniqueness and positive recurrence of the actual chain.

Scope and costs. This is a conditional construction, not a way to obtain H for free. It requires uniform actual blocks for every sufficiently large state, not merely the hardest corner. The cost D may be huge; the allowed theta shrinks with D/c. A polynomial failure probability is insufficient for this argument. Exponential failure exp(-c n^a) pays exponential immigration growth over O(n^a) time, with an explicitly smaller theta. The sampled drift cannot be converted into a pointwise continuous-time drift for a bounded multiple of exp(theta n); that would contradict the previously established delayed-return obstruction. The intervening occupation measure is essential. The full source state and physical elapsed time persist.
