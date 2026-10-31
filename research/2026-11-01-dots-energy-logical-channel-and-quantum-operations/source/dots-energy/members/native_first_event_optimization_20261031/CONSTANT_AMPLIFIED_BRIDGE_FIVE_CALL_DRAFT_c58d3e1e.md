# Constant-degree coherent preparation of the conditional bridge source

Status: candidate improvement to the stable hierarchical bridge. Ordinary exact-amplitude amplification is used as a paid component. This is NOT physical postselection, an expected-time quantum routine, or an assumed probability oracle. It leaves the exact bridge and physical first-event instrument unchanged.

## 1. Acquired proposal and its explicit acceptance

Receive the unified continuous envelope in STABLE_HIERARCHICAL_BRIDGE_BINDING.md. For a same-endpoint conditional EVENT, rates a,b>0, v=a+b, and remaining duration t, the target x-density is proportional to e^{a x}(1-e^{-v x}). The proposal has component labels retained privately and pointwise acceptance at least1/5.

Its TOTAL scalar acceptance P(t) is explicitly computable. Define

    Zbar(t)=v[(1-e^{-a t})/a-e^{-a t}(1-e^{-b t})/b].

For t<=1/v,

    P(t)=2 Zbar(t)/(v² t²).

For t>1/v, set Delta=t-1/v,

    L=(1/2)e^{-a Delta}, H=v Delta exprel(-a Delta),
    P(t)=Zbar(t)/(L+H).

These formulas are the integral of the target divided by the proposal-envelope integral. They follow from integral e^{a x}(1-e^{-v x})dx=(e^{a t}-1)/a-(1-e^{-b t})/b, after multiplying by v e^{-a t}. No positive exponential e^{a t} is evaluated. At t=0 use the limit P=1.

The mathematical lower bound P>=1/5, not a statistical estimate, supplies the conditioning. Compute P to a certified absolute tolerance and clip its numerical representative inside [1/6,1] with the clipping error charged. The small-t expression has cancellation but is not a precision oracle: grid-positive t>=h, so evaluating its numerator to absolute error O(t² v² delta) adds only O(log(1/h)+input bits) guard bits. Alternatively use its Taylor expansion for v t<=1. On the other branch L+H>=1/2 and all exponentials are nonpositive; stable expm1/exprel and clipping of tiny exponentials give polynomial finite arithmetic. All rates and times are supplied/acquired finite-bit quantities, not unknown means.

## 2. Five-call preparation, uniformly on a coherent time register

Let U_prop(t) coherently prepare the proposal's component/uniform seed and rotate a success flag with probability equal to the pointwise acceptance. Retain the seed; uncompute temporary arithmetic. Its good vector has norm sqrt(P(t)) and positive amplitudes equal to proposal amplitudes times square-root acceptance. The induced x-law conditional on that flag is exactly the desired target. Multiple components producing the same x remain orthogonal source coordinates; their squared weights, not amplitudes, sum.

Set theta=pi/10 and attenuate the good flag by

    c(t)=sin(theta)/sqrt(P(t)).

Since P>=1/5, c<0.7. This is a controlled scalar rotation obtained from the explicit preceding arithmetic. The resulting success amplitude is the SAME sin(theta) for every time/rate input. Two ordinary oblivious Grover iterations, with clean-input and success-flag reflections, give sin(5theta)=1. This uses exactly five calls to the attenuated proposal unitary or its inverse, plus fixed reflections. Choose the conventional sign so the success amplitude is positive; no branch-dependent phase is allowed. The normalized accepted vector is preserved.

The time/rate registers are NOT measured and are unchanged by the preparation. Consequently this is a source isometry on an arbitrary superposition of those registers, not an amplitude-amplification argument valid only for one classical parameter. The probability P is acquired by bounded arithmetic, not by amplitude estimation. There is no retry and no rejection cap R in the quantum execution cost.

The initial no-event atom and opposite-endpoint two-exponential mixture remain the elementary preparations. Only the same-endpoint event branch needs this constant-degree routine. A controlled five-call implementation bounds all branches without expected-time accounting. The entire path PREP and its inverse are available; the positive word average is obtained by PREP† SELECT PREP. Physical jump/color/time registers of the OUTER instrument are unaffected.

## 3. Finite-grid and synthesis robustness

Let the finite proposal discretization, endpoint-strip removal, acceptance arithmetic, and mixture arithmetic change its total acceptance to P_disc, with |P_disc-P|<=delta_s. For fixed retained parameter registers the finite accepted vector has some direction phi_disc. Attenuation using the approximate P changes its success amplitude from sin(theta) by O(delta_s), uniformly because P>=1/5. The same two-projector calculation used in sharp OAA shows that five-call amplification has coherent failure O(delta_s) and accepted amplitude1-O(delta_s²), with direction phi_disc. Numerical controlled rotations and reflections receive their actual operator-norm synthesis budgets; constant degree makes their telescoping bound constant, not an unpriced ideal phase operation.

The pushforward accepted distribution of x differs from the exact target by O(delta_s) in total variation plus the explicitly coupled time discretization, because normalization divides by P>=1/5. Strip removal is charged to this averaged distribution. We do NOT claim that deleting mass delta_s approximates the coherent source vector in norm delta_s; a vector comparison would cost sqrt(delta_s). It is enough here to bound the selected-word average, while the actual finite unitary is synthesized in operator norm. SELECT is the zero contraction on a residual internal preparation-failure flag; its missing weight is O(delta_s²). This flag remains coherent until the whole inner unprepare, so no physical postselection is introduced.

For sequential source preparation all earlier seeds and flags remain. On the good flags the amplitudes multiply the normalized conditional finite distributions. On bad flags SELECT is zero. Therefore conditional-distribution errors add over at most K stages by the ordinary sequential coupling bound; the O(delta_s) failure-norm estimate is also a conservative bound if used instead. Actual PREP/PREP† circuit synthesis errors add by a capped unitary hybrid, independently of the classical word-average estimate.

An explicit conservative allocation is delta_s=eta/[10^6(K+1)²]. The scalar P, component probabilities and acceptance evaluations receive absolute error at most delta_s/100, or squared tolerances where square-root PREP rotations require them. Use actual primitive-call counts for the final synthesis tolerance, not K alone. All elementary logs, exponentials, inverse roots, and Hadamards/reflections on the B-bit seed registers are counted operations. No lookup table over all times or all source states is assumed.

## 4. Stable duration coupling without a quantum rejection loop

The exact accepted law can still be ANALYZED using the unified classical rejection sampler with independent uniforms. Until either of two coupled samplers accepts or their discrete choices disagree, the per-proposal mismatch probability is <=5v |dt| and continuation probability <=4/5. Summing this geometric analysis bound gives <=25v|dt|. Including the initial atom and the opposite-endpoint mixture gives a safe total <=64v|dt|, while on matching accepted indices the remaining times are 1-Lipschitz. This is a proof coupling, not the implemented quantum runtime; the implementation uses five proposal calls.

Thus matched recursive remaining-time errors grow additively. QQ counts have the same O(c K² h) perturbation, and hierarchical placement/sorting preserves operator order with zero intervals allowed. The t=0 limiting bridge remains: empty for same endpoints; one instantaneous required flip for opposite endpoints; QQ count zero. There is no inner endpoint-probability or near-tie floor.

One sufficient grid tolerance is

    h<=min(1,
      eta/[10^6(1+64v+2c)(K+1)²],
      beta/[10^6(1+Hs+mu(alpha_H+1))(K+1)²]).

For the at most O(K) amplified proposal seeds choose

    sigma_in=delta_s/100,
    h_prop<=min(h/100,delta_s/[100(1+v)]),
    2^{-B}<=sigma_in*h_prop/[100 max(1,tau_max)].

Outside the charged uniform strips, inverse-exponential and square-root quantile derivatives are at most tau_max/sigma_in. Hence finite uniforms and arithmetic change proposal times by at most O(h_prop), and acceptance changes by O(v h_prop). Since acceptance is uniformly positive, square-root acceptance rotations are uniformly conditioned; tiny component probabilities use squared absolute probability budgets. The total strip and discretization contribution fits O(K delta_s)<=eta/100. Relative QQ uniforms need only the same or finer grid. Finite Poisson scans keep the existing allocated absolute CDF errors and zero overflow.

All outer-time and physical-clock bounds are inherited unchanged from the checked sharp first-event assembly. The new finite source error occupies its existing inner mean-block budget; aggregate word cutoff, count cap and physical short-window rules do not change. The underlying quantum source/jump state is never reset by this preparation.

## 5. Resource meaning and exclusions

Per path PREP the worst-case conditional-proposal call count is at most5K, with paid scalar P arithmetic, instead of K*Rcap rejection attempts. PREP† doubles that bound. Poisson scans and relative-coordinate sorting remain polynomial in K; their counts are separate. The exact first-event amplification degree, number of calls, and fast-kernel slot cap do not change.

This is ordinary amplitude amplification applied where the scalar acceptance is explicitly acquired and bounded below. It does not create a constant-cost arithmetic primitive, an optimal state-preparation oracle, or a demonstrated advantage over ordinary dense/effective simulation. A new resource ledger may report the proposal-call proxy10 S d_A K, but must not call that a gate count or omit the analytic acceptance computation and actual kernel gates.
