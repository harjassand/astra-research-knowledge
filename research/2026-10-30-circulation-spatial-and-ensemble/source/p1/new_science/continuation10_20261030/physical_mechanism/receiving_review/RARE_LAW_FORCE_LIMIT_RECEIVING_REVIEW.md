# Receiving review: rare law, ordinary law, force limits and the nonlinear evaluator

30 October 2026. Actual-file review by the existing physical-mechanism role. No extra agents or numerical fixtures were used. The root inputs were not edited.

## 1. Pinned inputs and verdict

The exact versions read and copied into this directory are:

* `RARE_LAW_TYPICAL_LAW_AND_FORCE_LIMITS.md`, SHA256 **`1a36eeda2df4523e25778f11ce71404ab2ee58a6e6d4b11c7c1125d4d8d50f13`**.
* `NONLINEAR_CIRCULATION_OPERATION_AND_PATH_LAW.md`, SHA256 **`53db4609d6b9a127c2898988a2f50684f4de7643d05c2156af516c19802a0c20`**.

**The explicit one-ring force-limit result is correct at its stated native-only force port.** I reconstructed the finite-N likelihood score, the controlled-law derivative, the rare-coupling moment estimate, canonical variance and current central limit, and both orders of limits. The coexistence of unchanged ordinary finite-N trajectory laws to superpolynomial accuracy with changed speed-N tails is also correct; no equality of rate functions follows from this total-variation bound.

The nonlinear path-map/evaluator scope is sound for a fixed supplied evaluator with globally bounded derivatives and the stated certified timing/precision interface. One optional extension needs sharper wording: the parenthetical allowance of an merely “exponentially tight domain” is not by itself enough for a **superexponential** equivalence theorem. Section 6 below gives the precise correction. It does not affect the global-derivative hypotheses or the explicit rational examples.

This review accepts the mathematical consequence at its declared ports. It does not certify manufactured sensors, synchronization, pulse accuracy, total work, or historical priority. The full native exclusion LDP is a separate supplied theorem; I checked the use of its contraction and the displayed projection algebra, not every external finite-energy recovery argument again.

## 2. The exact finite-N score has the stated factor

Write `delta_i=eta_i-eta_(i+1)` and let `A(eta)=sum_i delta_i^2`. An active bond exchange has native rate

\[
q_F(\eta,\eta^i)=D\exp\{F\delta_i/(2N)\}.
\]

At zero field the derivative of the jump-log-rate sum is `B/(2N)`. The derivative of the total escape-rate term is

\[
\frac{D}{2N}\sum_i\delta_i=0
\]

pointwise on the periodic ring, not merely after equilibrium averaging. The initial canonical law does not depend on `F`. Hence the native path score is exactly

\[
S_N=B(N^2T)/(2N).
\tag{R1}
\]

The controller observes only physical data, not the external parameter. Conditional on a complete native path, its auxiliary primitive randomness, sensors and causal policy have no explicit `F` dependence at this stated port. Therefore the joint law factorizes into the parameter-dependent native path law and a parameter-independent conditional apparatus kernel. Differentiating a fixed functional of this joint record gives

\[
\frac{d}{dF}\left.\frac{\mathbb E_F C_N}{N^2}\right|_{F=0}
=\frac{\mathbb E_0[C_NB]}{2N^3}.
\tag{R2}
\]

The switching threshold is a discontinuous functional of a realized path, but it is the **same** functional under every `F`. It is not differentiated as an explicit parameter-dependent function. At each finite `N`, bounded hop intensities on compact force intervals and Poisson count domination justify differentiation of the expectation. There is no missing derivative of the threshold policy or auxiliary rate law.

This calculation would change if the force also acted on auxiliary carriers, altered the measurement law other than through the native path, or were explicitly supplied to the controller. The root text correctly excludes these alternatives and explicitly warns against reusing (R2) at the two-lane force port.

## 3. Rare coupling is sufficient for the moment comparison

Construct the controlled and force-off auxiliary processes from the same primitive clocks, with the same native path and pre-arm observations. Let `E_N` denote first arming, including false arming caused by a certified observation failure. The two actual auxiliary paths agree on `E_N^c`. The unforced estimate is

\[
\Pr(E_N)\le C e^{-c\log^2 N}+p_N,
\]

where `p_N` is superexponential at speed `N`. This does not condition the native process on its rare trigger.

All total native and auxiliary hop counts on time `N^2T` have moments bounded by powers of `N`. A deliberately loose bound suffices: with `R_N<N`, the fourth moments of `A`, `A^0` and `B` are at most `C N^12`. Thus Hölder and Cauchy–Schwarz give, for example,

\[
|\mathbb E[(A-A^0)B]|
\le C N^6\Pr(E_N)^{1/2}.
\tag{R3}
\]

After division by `N^3`, this tends to zero faster than any inverse power. No small conditional work estimate or independence of the **controlled** auxiliary current from the native current was assumed.

The zero-drive comparison `A^0` is independent of `B` under Section 7's expressly independent initial state and primitive clocks, and is centered. Hence `E[A^0B]=0`. This identifies precisely which independence is used. An arbitrary retained correlated initial record must not silently replace Section 7's canonical, independent experiment; the broader tracking theorem and this explicit susceptibility calculation have distinct initial-law premises.

The same polynomial-moment/superexponential-bad-event argument establishes convergence of the mean normalized current under a fixed load. Mere convergence in probability would not suffice, but the root supplies the required moment bound.

## 4. Canonical mean, central limit and the two limits

The uniform canonical law is stationary for the homogeneous asymmetric ring at every constant `F`: in each configuration the numbers of `10` and `01` bonds are equal, so incoming and outgoing weighted rates balance. Therefore the actual native mean drift is

\[
2D N\chi_N\sinh(F/(2N)),\qquad
\chi_N=\frac{n_N(N-n_N)}{N(N-1)}.
\tag{R4}
\]

The root's mean formula and limit `D m(1-m)FT` are correct.

At zero field `B` is a martingale with bracket `D int A(eta_s) ds`. Canonical averaging gives `E A=2N chi_N`, so

\[
\mathbb E B(N^2T)^2=2D N^3\chi_NT.
\tag{R5}
\]

The canonical activity has variance `O(N)`: overlapping local terms contribute `O(N)`, and disjoint canonical occupation covariances are `O(1/N)` each. Stationarity and Cauchy–Schwarz in time therefore bound

\[
\operatorname{Var}\left[N^{-3}D\int_0^{N^2T}A(\eta_s)ds\right]
=O(1/N).
\tag{R6}
\]

No relaxation-rate or mixing estimate is required for this bound. Monotonicity of the bracket and a finite-grid argument give its uniform-in-time convergence; the rescaled jumps vanish. The martingale functional central limit has variance parameter `2D m(1-m)`. The zero-drive auxiliary martingale has normalized quadratic variation `O(R_N/N)`, hence disappears at scale `N^(3/2)`. Total-variation coupling transfers the same central-limit law to the armed physical current.

Equations (R2)–(R5) establish

\[
\lim_N\mathcal J'_N(0)=D m(1-m)T.
\]

For every **fixed** finite macroscopic field, auxiliary inward capacity `K_N` eventually dominates the native `O(|F|)` drift. Tracking plus the moment bound gives `lim_N mathcal J_N(F)=0`. The derivative of this limiting zero function is zero. The two noncommuting limits in the root box are therefore correct.

The claimed small-force boundary layer also follows: if `|F_N|=o(log N/sqrt(N))`, the compensator drift accumulated over `N^2T` is `o(b_N)`, uniformly over the native state. The remaining bounded-jump martingale obeys the same maximal estimate. Arming remains superpolynomially rare in this regime. A fixed nonzero `F` eventually leaves it.

This is a singular sequence of active finite-horizon protocols. It is not a counterexample to finite-system linear response, equilibrium FDT, or a theorem equating differentiable limiting cumulant curvature and central-limit noise under appropriate uniform assumptions. The root states these distinctions correctly.

## 5. Ordinary paths, rare laws and physical work

The common-record coupling is adequate for the claimed total-variation bound, including native and auxiliary trajectories, delayed observations, applied-force logs and timing. A shadow evaluator can run in the reference. The fixed protocol description is conditioned on; it is not a random data field falsely declared equal. All physical paths agree until first arming. Consequently every measurable statistic, including an `N`-dependent rescaling, inherits a distributional TV bound. This does not by itself bound unbounded moments; the root correctly handles the moment comparison separately.

Polynomially many genuinely independent passive trials have vanishing distinguishing power by the product-TV union bound. Inspection of the controller program, active force probing, or exponentially long/repeated experiments are different information interfaces, and are not excluded. Arbitrary hidden-parameter mixtures do not become independent product trials without their corresponding conditional setup.

There is no conflict between this TV bound and the changed LDP. The error `exp[-c log^2 N]` is **larger** than `exp[-c'N]` for large `N`. Thus it permits changes to an entire speed-N rare-event family. The trigger lies above the central-limit scale and below the macroscopic scale. Calling the result a separation of these scales is accurate; claiming unchanged rare laws from the small TV distance, or changed central-limit noise from the constrained limiting action, would be incorrect. The root does neither.

The physical force-work calculation for the hop supplier is exact: at each carrier, the two conditional rates have the same prefactor and opposite affinity factors, so the conditional expected work rate is `2c_l F_l sinh(F_l/2)`. It is nonnegative even when `c_l` is unknown. A real thermal-heat identification needs the extra local-detailed-balance/internal-energy premise; the root limits the statement to force work and preserves that distinction.

The finite-cell formula retains the momentum and force-switching term, and matches the independently reconstructed expression in `FINITE_CELL_FORCE_WORK_UNDER_DELAYED_COMMANDS.md`. Its exact synchronized pulse schedule, delayed force filtration and fresh unread input are indispensable. Spatially asynchronous pulse errors are not covered by that algebra.

The sustained-load lower bound is a correct Jensen bound at the calibrated affinity-only port. It must not be applied after arbitrary future rare-event conditioning, as the root explicitly says. Sensing, synchronization, computation, communication, availability of distributed drive, initial preparation and the mechanical supplier's continuing thermal replacements remain outside the vanishing mean carrier-work statement.

## 6. Nonlinear evaluator and one required scope sharpening

The target construction is correct under the global assumptions. For a bounded native jump `delta B`,

\[
\Delta Z_N=(D_h\phi-I)\Delta B+O(N^{-2}|\Delta B|^2).
\]

The first term has bounded drift because the **total** native drift is bounded. The summed Taylor remainder has drift `O(1/N)`, and explicit time dependence contributes bounded `partial_t phi`. Thus the actual nonlinear target remains a bounded-drift source with bounded jumps and `O(N)` intensity. No derivative of unknown microscopic rates is estimated.

The root explicitly requires a real evaluator for the selected function. The rational examples are implementable with `O(log N)` precision and polynomial-in-log-N arithmetic on a polynomially bounded counter range. Such a counter range has superexponentially reliable overflow protection under bounded intensities. This complexity statement must remain attached to the **explicit rational examples**; arbitrary supplied smooth functions can require a different program or resource budget. It would help to start the relevant sentence with “For these explicit examples”.

**Scope correction requested.** The sentence allowing derivative bounds merely “on a warranted exponentially tight domain if its failure is accounted for” should say one of:

1. a domain with a **superexponentially small** whole-horizon exit probability; or
2. an exhaustion by domains with exit exponents tending to infinity, with the stopped derivative/evaluator/tracking estimates proved on each domain before taking that exhaustion limit.

A single exit estimate `exp(-cN)` with fixed `c` is not enough to preserve a conclusion whose logarithm divided by `N` must tend to minus infinity. “Failure accounted for” could otherwise mean only adding this finite-exponent event and would weaken the theorem. The stated globally bounded derivative theorem and all listed examples require no change.

The conservation-based path map and retained auxiliary current are appropriate: the actual auxiliary mass is deterministically `o(N)`, its nonconstant current is determined by its density endpoints, and its constant component is supplied by tracking. In one dimension this yields the asserted complete spatial-path operation. The main theorem is explicitly conditional on an actual native LDP; bounded drift/activity alone does not manufacture one. For the two-ring linear projection, minimizing over the native preimage `(j_1+u,j_2-u)` gives the displayed quadratic subtraction with denominator `r_1+r_2`; its sign and factor `1/4` are correct.

## 7. Primary-predecessor and consequence scope

I had already read the actual primary texts of Brandes 2010, Wagner et al. 2017, Fricke et al. 2011 and Brandes 2015 while constructing the ordinary comparison. They preempt any new-current-governor, sampled-feedback, freezing, or autonomous-charge-mismatch principle. The root credits the current-governor and finite-window precedents, and narrows its proposed addition to the real dilute-flow interface and complete physical path-law conjunction. That is the appropriate claim to assess.

Likewise, the response order-of-limits phenomenon is proved here by a concrete physical protocol; it is not a claim that noncommuting limits or rare-event control are new general mathematics. No priority inference follows from the absence of a located exact matching apparatus. No practical or total-cost superiority has been established.

**Receiving conclusion:** accept the force-limit/rare-law theorem at the pinned stated interfaces and initial laws. Accept the globally bounded-derivative nonlinear evaluator/path-map scope. Sharpen the optional localized-domain clause as above before treating that extension as accepted. No further fixture is needed to resolve these analytic points.
