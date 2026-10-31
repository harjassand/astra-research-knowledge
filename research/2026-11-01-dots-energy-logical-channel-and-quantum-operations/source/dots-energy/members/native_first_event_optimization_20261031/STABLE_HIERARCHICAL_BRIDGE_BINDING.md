# Stable hierarchical bridge acquisition: no inner endpoint floor

Status: candidate receiving improvement to the separately checked elementary two-state source. It changes neither the physical process nor the sharp first-event proposal. It exploits the particular virtual history: ONE alternating P/Q chain and identical QQ insertions inside each fast residence. It is not a claim for independently colored many-mode paths.

## 1. A continuous proposal for conditional same-endpoint events

Use the exact first-event laws in ELEMENTARY_TWO_STATE_BRIDGE_SOURCE.md: rates a,b>0, v=a+b, event remaining time x=t-u with density proportional to e^{a x}(1-e^{-v x}). Set x0=min(t,1/v) and Delta=t-x0.

If Delta=0, propose x=x0 sqrt(U), accept e^{a(x-x0)} R(vx), where R(z)=(1-e^{-z})/min(1,z), R(0)=1. If Delta>0, select a lower or upper proposal with the UNNORMALIZED positive weights

    L=(1/2)e^{-a Delta},
    H=(1-e^{-a Delta})/(a/v).

For the lower proposal use x=x0 sqrt(U) and acceptance e^{a(x-x0)}R(vx). For the upper proposal draw x=t-X, with X a truncated Exp(a) on [0,Delta], and accept R(vx). Do not renormalize components separately after acceptance. When Delta=0 take lower probability one, upper zero; the displayed weight formula extends continuously to this limit.

Proof: a common positive scalar e^{a t}/v times L is the integral of the lower envelope v x e^{a x0} on [0,x0], and the same scalar times H is the integral of e^{a x} on [x0,t]. The stated acceptance factors divide the target by those envelopes. For t<=1/v the lower envelope alone gives the same result. On every proposal, a x0<=1 and R(vx)>=1-e^{-1}, so acceptance is at least e^{-1}(1-e^{-1})>1/5. Use the same cap Rcap=ceil(log[100(K+1)/eta]/log(5/4))+1 as the elementary source; zero on overflow, with no endpoint rejection.

Evaluate H as v Delta exprel(-a Delta), not by dividing rounded tiny differences. All exponentials are nonpositive; R is continuous and globally 1/2-Lipschitz. The mixture remains well conditioned as Delta tends to zero. Coherent capped acquisition retains every seed and the first accepted proposal flag until inner unprepare.

## 2. Direct shared-uniform stability, including rare endpoints

The important output of a virtual first event is the remaining time x. For every proposal component, x is 1-Lipschitz as a function of input t under the same underlying uniform:

* Lower x=min(t,1/v)sqrt(U).
* Upper x=t-Q_Exp(a,Delta)(U); the truncated exponential quantile has derivative in its upper endpoint in [0,1].
* For opposite endpoints, component1 gives x=t-Q_Exp(a,t)(U), component2 gives x=Q_Exp(b,t)(U), both with derivative in [0,1].

The no-event atom A_i=e^{-a t}/Pii(t) has |A_i'|<=a<=v: differentiate its logarithm and use Pii=(b+a e^{-v t})/v.

For opposite endpoints the first component weight is w(t)=(1-e^{-a t})/(1-e^{-v t}). Write alpha=a/v and z=v t. Then w is the probability of U<=alpha under density proportional to e^{-z U} on [0,1]. Its z derivative is minus Cov(1_{U<=alpha},U); bounded-variable covariance has absolute value at most1/4. Thus |w'|<=v/4, including the t=0 limiting value alpha. This is a cancellation specific to the exact two-state bridge, not an assumed generic conditioning bound.

For t>1/v the lower proposal probability is

    p_L=(a/2)/(a/2+v(e^{a Delta}-1)).

This formula is used only to prove the bound, not evaluated with a positive huge exponential. Differentiation gives |p_L'|<=2v: its value relative to the derivative at Delta0 is y/[1+(2v/a)(y-1)]²<=1 for y=e^{a Delta}>=1. Below the split p_L=1, so the bound holds globally. Conditional on choosing the same component, its proposed x changes by at most |dt|. Lower acceptance changes by at most (2a+v/2)|dt|<=3v|dt|; upper acceptance changes by at most v|dt|/2. Therefore, coupling the SAME fresh mixture/proposal/acceptance uniforms for Rcap attempts, the discrete outcome (atom, accepted-index, or overflow) differs with probability at most

    (1+6 Rcap) v |dt|.

On the matching accepted-index event, the remaining times differ by at most |dt|. The source cap and this bound are WORST-CASE capped operations, not an expected-runtime shortcut.

This avoids both inverse endpoint probabilities and inverse remaining durations. A rare same-endpoint EVENT is sampled only after its Bernoulli flag, but the conditional sampler has constant acceptance; no division by that flag probability enters runtime or stability.

## 3. Zero internal durations are harmless limits

Finite rounding may make a remaining duration zero. Define the extended conditional source at t=0 as follows: identical endpoints give no event; opposite endpoints give exactly one zero-time sector flip and then stop. This is the continuous t-down-to-zero limit of the conditional bridge's word/time law. It is not an assertion that a classical CTMC has a positive-probability jump at zero time. The original endpoint coefficient Eij(0) is zero for opposite endpoints; for an internally rounded residual duration the extension supplies the correct limiting word rather than discarding a potentially important branch.

All zero intervals are retained in the operator word. The acquired Q kernel has F(0)=Q/2 and its previously priced factor2, so zero-duration products agree with the source-projector limit. Same-endpoint event probability tends to zero; its unused conditional-event sampler can use any fixed zero-duration convention. Rates a,b are positive under the retained positive coupling/high-rate source premise; separately certified zero-coupling/rate cases remain the received explicit branches.

## 4. Stable recursion and QQ placement: no near-tie exclusion

Fix a cap K on TOTAL off-diagonal and QQ insertions. Use a dyadic remaining-time grid of mesh h and approximate each elementary quantile to error at most h/10 before monotone rounding into [0,current remaining time]. Round the returned remaining time, not a separately reconstructed sequence of elapsed increments. Because the exact accepted remaining-time map is 1-Lipschitz, after j matched transitions its error is O(j h), not 2^j h. The summed probability of a discrete mismatch is O((Rcap+1)v K² h), plus explicitly allocated finite-uniform/threshold errors.

Each fast residence is bounded by consecutive ordered off-diagonal event times. Its duration changes by O(Kh). Add its QQ count using the received finite Poisson CDF scan with mean 2c times that residence. Poisson laws admit TV coupling at most the absolute change in their means; indeed shared quantile coupling is monotone and its mean count difference bounds the mismatch probability. Over all residences the additional error is O(c K²h). Finite CDF approximation is charged separately; overflow selects zero exactly.

Given matching QQ counts, use the same relative uniforms inside the corresponding fast residence and sort them ONLY within that residence. Sorting real coordinates is 1-Lipschitz in maximum coordinate error. All these QQ insertions apply the SAME operator QKQ and the same phase -i, so exchanging labels of equal/nearby QQ marks has no semantic effect. The sequence of residences and their bordering off-diagonal operators is already known. Place them in that hierarchical order, retaining the boundary operators even when rounded times coincide. This prevents a QQ mark from being numerically moved to another sector or across a differently typed off-diagonal event.

Thus no global anti-concentration or minimum-spacing cut is needed for this one-chain word. Ties produce zero nonnegative interval lengths with a fixed correct ordering. This argument must NOT be applied to different independent colors with noncommuting operators, for which the earlier cross-color order issue remains real.

With matching discrete events, all absolute times differ by O(Kh). The word operator error is bounded by

    O([Hs+mu(alpha_H+1)](K+1)²h),

using the received differentiable exact fast kernels and interval simulations; their numerical approximations are uniformly close to those functions. Choose, conservatively,

    h <= min(1,
      eta/[10^5(1+(Rcap+1)v+2c)(K+1)²],
      beta/[10^5(1+Hs+mu(alpha_H+1))(K+1)²]).

All constant factors above have ample room in 10^5. Elementary source errors receive a separate eta/100 budget, and the aggregate virtual overflow remains the previously proved weighted tail, not a new conditional tail claim.

## 5. Finite uniforms and arithmetic are paid

There are O((K+1)(Rcap+1)) proposal/comparison operations, plus the received finite Poisson scans/sorts. Use a proposal-time accuracy

    h_prop<=min(h/100,eta/[10^5(1+v)(K+1)(Rcap+1)]).

Fresh Bernoulli uniforms allow direct conditional threshold-strip bounds, not a union over hypothetical inverse-CDF midpoints. For every inverse-log or square-root proposal coordinate exclude endpoint strips of width

    sigma_in=eta/[10^5(K+1)(Rcap+1)].

Select zero if any of the capped proposal coordinates lies in such a strip, even an unused proposal if convenient. Their TOTAL removed mass is O(eta/10^5), charged linearly to the averaged inner block, not asserted to approximate the coherent source state at that same error. On the remaining interval the truncated-exponential inverse has uniform derivative <=tau_max/sigma_in and the square-root proposal derivative <=tau_max/(2sqrt(sigma_in))<=tau_max/sigma_in. Thus a sufficient finite-uniform budget is

    2^{-B}<=eta h_prop/[10^6 max(1,tau_max)(K+1)(Rcap+1)].

This makes proposal-time perturbations deterministic away from the charged strips. Small finite-grid ambiguity at a strip boundary is charged with the same fresh-uniform threshold bound. All inverse-log arguments stay bounded away from zero by a supplied dyadic scale; evaluate log/sqrt to absolute time error h_prop/10 with explicitly increased arithmetic bits. Threshold computations have absolute tolerance <=eta/[10^5(K+1)(Rcap+1)]. Proposal-time rounding changes acceptance by at most 2v h_prop and is included in this budget. If actual finite arithmetic uses more operations, subdivide by its actual capped count; do not equate K with a gate count.

Evaluate the no-event flag with positive denominator b+a e^{-v t}; opposite mixture weights with expm1/exprel; lower/upper weights with nonpositive exponentials and v Delta exprel(-a Delta). As t approaches zero use the analytic continuous values and certified Taylor bounds. Grid-positive times are at least h, and large negative exponents are clipped at the allocated absolute tolerance. Required bit lengths are polynomial in log(1/h), log(1/eta), log(1+a+b), supplied rate/input lengths, and log K. No minimum endpoint probability is an input to this source's precision budget.

The physical OUTER three-exponential proposal, its common-uniform embedding, short-remaining-window handling, derivative bound Lout, and private counter-augmented continuation remain exactly the checked sharp assembly. The outer source may retain its conservative strip/time floor. Removing inner p0/zeta/pz is justified only by Sections2–4 here, not by an assertion that such floors never matter.

## 6. Cost and scope

This acquires each capped virtual history using O(K Rcap) elementary conditional proposals and the existing O(K²) conservative Poisson-CDF/sort work, rather than O(K J) bisection steps with J depending on inverse endpoint floors. Rcap=O(log(K/eta)), and all elementary functions/controlled arithmetic are paid. It is not a claim that their reversible gate cost is one or that every inner loop can be measured early.

The exact scalar E coefficients, positive outer normalization and aggregate z=2 word cap are unchanged. Therefore this addendum can feed the same complete-isometry proof after its source error allocation is included. It does not change the physical count/window cap, source preparation, jump stack, H0 action, or fast-kernel algorithm. A separate ledger must show the revised arithmetic/precision proxies before claiming any numerical resource improvement. No practical crossover, novelty, or implemented quantum backend is inferred.
