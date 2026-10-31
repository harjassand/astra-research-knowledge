# Elementary bounded-work source for a two-state bridge

Status: separate candidate acquisition improvement. It replaces the recursive inverse-CDF implementation, not the exact bridge law or any physical source model. All quantum uses retain random seeds coherently, select zero on cap failures, and unprepare only the inner virtual-word seed after SELECT. Rejection here is a capped reversible source routine, not postselection of the physical quantum state.

## 1. Exact first-event distributions

Consider a continuous-time two-state chain with positive outgoing rates a=q_i and b=q_j, v=a+b, starting in i over duration t>0. The endpoint is supplied. Standard transition probabilities are

    P_ij(t)=a(1-e^{-v t})/v,
    P_ii(t)=(b+a e^{-v t})/v.

If the endpoint is j, a first event is compulsory. Its density is

    a e^{-a u} P_jj(t-u)/P_ij(t), 0<u<t.

This is EXACTLY the positive mixture

    w1=(1-e^{-a t})/(1-e^{-v t}),
    w2=e^{-a t}(1-e^{-b t})/(1-e^{-v t}),
    w1+w2=1,

of (1) a truncated Exp(a) time u, and (2) a reflected truncated Exp(b) time u=t-X. The formula follows by expanding P_jj(t-u)=[a+b e^{-v(t-u)}]/v. No endpoint rejection or tiny event-probability normalization is used in sampling.

If the endpoint is i, first select the no-event atom

    A_i(t)=e^{-a t}/P_ii(t).

On its complement, the remaining time x=t-u after the first event has conditional density proportional to

    F(x)=e^{a x}(1-e^{-v x}), 0<x<t.

The small probability of this complement is used only as a Bernoulli threshold. It is NEVER a rejection acceptance denominator or a runtime factor.

After an actual first event change state to j, retain the supplied endpoint, and recursively apply the same construction to remaining time t-u. Stop at the no-event atom or virtual cap. This reproduces the usual conditional CTMC bridge exactly before numerical/cap errors.

## 2. Constant-acceptance sampler for the same-endpoint event

When v t>=1, propose x from the increasing truncated exponential with rate a on [0,t], i.e. x=t-X where X is truncated Exp(a). Accept with probability 1-e^{-v x}. Its mean acceptance is at least the corresponding uniform average, since the proposal stochastically dominates uniform:

    1-(1-e^{-v t})/(v t)>=e^{-1}>1/3.

When v t<1, propose x=t sqrt(U), density 2x/t². Accept with probability

    exp[a(x-t)] * (1-e^{-v x})/(v x),

where the ratio at zero is one. Both factors are <=1. The accepted density is proportional to e^{a x}(1-e^{-v x}). Uniformly on this regime the acceptance is at least e^{-1}(1-e^{-1})>1/5.

No exact comparison against a transcendental boundary is needed. Compute v t to certified absolute accuracy 1/40. If its approximation is <=1 use the square-root proposal; otherwise use the increasing-exponential proposal. The former then has v t<=21/20, the latter v t>=19/20. On the former, the uniform acceptance lower bound is e^{-21/20}(1-e^{-21/20})/(21/20)>1/5; for example the elementary rational Taylor bounds 17/50<e^{-21/20}<9/25 imply this inequality. On the latter the uniform-average bound is >1/3, using e^{-19/20}>e^{-1}>11/30. Thus 1/5 is a common certified lower bound with overlap.

Use independent uniforms for every proposal and acceptance. With K recursive events, cap proposals per conditional event at

    R=ceil(log[100(K+1)/eta]/log(5/4))+1.

Failure probability is <=eta/[100(K+1)] per invocation. On failure choose the ZERO selected word and do not resample globally or renormalize the surviving words. This gives total additional conditional removed mass <=eta/100. A reversible fixed-R loop stores the first accepted index and retains all seed words until the final inner unprepare. Its operation count is O(KR), not the expected number of proposals. Expected acceptance does not grant free variable-time coherent execution.

## 3. Duration conditioning without inverse endpoint powers

The exact first-event kernel has a stronger duration-TV bound than the generic formula with inverse endpoint probabilities. On t,t' >=t_min>0,

    TV(K_t,K_t') <=32(v+1/t_min)|t-t'|.

No-event outputs are a common FLAG rather than an asserted equality of distinct physical timestamps. Event outputs include the first-event time u and flipped state. This statement concerns the internal virtual source kernel.

Proof for opposite endpoints: w1' has absolute value at most v+2/t_min, by 1/(1-e^{-z})<=1+1/z and z/(e^z-1)<=1. A truncated decreasing exponential changes in TV by at most |dt|/t_min; the increasing truncated exponential by at most (v+1/t_min)|dt|, since the distributions are restrictions of the same positive exponential density on nested intervals. Combining mixture weights and both components gives a bound smaller than 8(v+1/t_min)|dt|.

For equal endpoints, |A_i'|<=2v because |P_ii'|/P_ii<=v. Conditional on an event, x has density F(x)/Z(t) on [0,t], with F independent of t and increasing. Concavity gives (1-e^{-v x})/(1-e^{-v t})>=x/t, so

    Z(t)/F(t)>=integral_0^t (x/t)e^{-a(t-x)} dx,
    F(t)/Z(t)<=a+2/t.

For the second inequality put z=a t and use
(z-1+e^{-z})(z+2)>=z², whose difference z-2+(z+2)e^{-z} is nonnegative because its derivative is 1-(z+1)e^{-z}>=0. The a=0 limiting expression agrees.

Changing the truncation endpoint changes this x-distribution in TV by at most (a+2/t_min)|dt|. Passing to u=t-x adds a translation; a monotone probability density on its interval has translation-TV at most its maximum density times the translation. Thus the u-distribution changes by at most 2(a+2/t_min)|dt|. Combine this with the no-event atom to obtain the stated conservative constant32. If a proof step crosses the numerical proposal-regime boundary, use this exact kernel bound: both proposal schemes target the SAME law, so no cross-regime seed coupling is required.

## 4. Finite-bit acquisition and errors

Truncated Exp(q) is sampled by

    X=-log1p[-U(1-e^{-q t})]/q,

with stable expm1 and uniform limiting formula when q t is sufficiently small at the requested absolute tolerance. The increasing exponential is reflected. All exponent arguments used directly are nonpositive. The square-root proposal is elementary. The function (1-e^{-z})/z is evaluated by expm1/Taylor with its value1 at zero. The Bernoulli atom uses the positive denominator b+a e^{-v t}; mixture weights use expm1, or the equivalent rate ratio times exprel ratio. These are finite arithmetic operations whose bit complexity is polynomial in input lengths and requested bits, not in q t. Certified clipping of exponentially small terms is charged.

For rounding a uniform to a B-bit midpoint, any monotone quantile in an interval of length <=tau_max obeys E|Q(U)-Q(U_B)|<=tau_max 2^{-B}. Markov's inequality therefore bounds the probability of a time discrepancy >h_time by tau_max 2^{-B}/h_time, without a density lower bound. Use separate independent uniform coordinates for component choices, proposals, and acceptance tests. Each acceptance/comparison threshold is independent of its fresh test uniform conditional on preceding proposals. Hence an absolute threshold error zeta_p and finite uniform grid contribute at most 2zeta_p+2^{-B} bad probability PER executed comparison; there is no union over 2^J hypothetical bisection midpoints.

Choose the elementary proposal-time tolerance

    h_prop<=min(h_time/10,eta/[10000(1+v)(K+1)(R+1)]).

Acceptance functions have proposal-coordinate derivative at most a+v<=2v (the exprel ratio derivative has magnitude at most1/2), so this also pays acceptance changes induced by rounding a proposal. Allocate each of the O((K+1)(R+1)) source operations bad probability <=eta/[1000(K+1)(R+1)]. Thus a sufficient uniform precision satisfies

    2^{-B} <= eta*h_prop/[1000 tau_max (K+1)(R+1)],

with a separate absolute threshold tolerance <=eta/[1000(K+1)(R+1)]. Actual finite arithmetic budgets are subdivided by the real primitive count. Very small a,b,t cost logarithmic bits; there is no rejection depending on the endpoint probability. Positive-rate and t=0 branches are explicit: t=0 allows only identical endpoints. Zero-rate degeneracies may be handled directly or excluded by the positive supplied source premise, as in the received compiler.

For recursive duration perturbations, replace the old Lker=16(1+qrate)²/pz² by

    Lker,new=32(v+2/zeta)

on retained remaining times >=zeta/2. The accumulated mismatch remains O((Lker,new+2c) K² h_time), including the separate QQ Poisson source; allocate h_time accordingly. Keep the old GLOBAL near-boundary/cross-event tie cut and its endpoint floor p0 if desired. This addendum removes neither that cut nor the physical outer-time/common-uniform proof. It only improves the acquired conditional source and its duration-conditioning bound.

All cap failures select zero in the positive word block. The whole aggregate word-tail lemma, actual complete-isometry amplification, jump-stack output, and physical count/private-clock assembly remain separate received results. The new per-source numerical error is added to the same beta budget. This is standard elementary conditional CTMC sampling used as an explicit acquired routine, not a new stochastic process, a physical simulator implementation, or a demonstrated speedup.
