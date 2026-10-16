# Control genesis: exact minimax value, source-relative extension, and limits

Author: gc_peak_genesis. Date: 2026-10-16. Final status: **FROZEN**. Analytic claims are internally derived and independently matrix-checked where stated; external correctness, exact historical priority, and physical implementation remain UNKNOWN.

## Decision

The incoming fixed-J peak-cap optimizer reconstructs correctly. More consequentially, the certificate is uniformly sharp to leading order for **actual endpoint error inside the exact ideal generator model**, and fixed private fair-refresh slots have an **exact singleton robust minimax operation** for a known time-varying envelope. This does not establish a new DD protocol. A missing profile bound is decisive: a total-action-only adversary can concentrate its interaction inside one uncontrolled gap and erase every claimed count improvement.

No canonical, worktree, or supplied-input files were edited. This worker wrote only in its own directory. It spawned no agents and executed no supplied author scripts.

## Exact results

1. **Peak-cap reconstruction.** For duration T, action a=JT, intensity cap L, and integrated intensity Λ, the exact certificate minimum is the supplied endpoint-atom/floor formula when Λ≤LT≤Λ+2, and 2a²/(Λ+2) when LT≥Λ+2. A global positive-kernel/potential proof handles arbitrary plateaus. Both regimes have an explicit finite attaining rate schedule. See [PEAK_AND_POISSON_MINIMAX.md](PEAK_AND_POISSON_MINIMAX.md), Section 1.

2. **New actual-error minimax sharpness.** For every deterministic rate schedule and any known envelope j(t), a permitted physical qubit H(t)=j(t)X has p=E sin²S and C=E S², with S=∫jξ and |S|≤a. Consequently κ(a)C≤p≤C for a<π, κ(a)=sinc²a. Combining this concrete lower witness with the source's universal upper effect gives κ(a)C*≤inf_control sup_allowed_H p≤C*. The incoming optimizer is asymptotically minimax for actual endpoint error as a→0. This is a new proved lower bound within this mathematical model; it is not a measured device floor. Sections 2–3 give the proof and necessary ideal resource cost.

3. **Exact fixed-slot singleton minimax.** N internal fair-toggle refresh opportunities represent N complete virtual pinches and N+1 gaps. For prescribed gap actions a_k, the worst-case actual endpoint error over the exact source uncertainty class is

       Q=1−∏_k cos²(min(a_k,π/2)).

   A subspace-angle survival bound proves the upper; a finite sink bath attains it and also fits the additive private-sign Fourier model. Over slot placements with known envelope j, equal-action gaps globally minimize this to

       Q_N*=1−cos^(2(N+1))(min(a/(N+1),π/2)).

   The lower witness can make odd Walsh weight equal actual final physical memory-parity error. In general, the theorem's receiving interface remains an odd-Walsh effect unless physical support/covariance is separately proved. See [FIXED_REFRESH_MINIMAX.md](FIXED_REFRESH_MINIMAX.md), Sections 1–4.

4. **Coupled selected-subset control.** For any coupled deterministic rate-admissibility class, the sharp source product certificate bounds the robust actual all-selected endpoint minimax within the schedule-uniform factor ∏κ(a_i), when all action bounds are small enough that no factor is capped. In the aggregate cap-inactive regime LΣT≥ΛΣ+2r, the exact product optimum is

       (∏a_i²)[2r/(ΛΣ+2r)]^r,

   attained by equal integrated exposure Λ_i=ΛΣ/r and synchronized endpoint-hold schedules. This rule optimizes the all-selected product objective. The coupled cap-active global problem is explicitly left open. For fixed refresh slots with a total integer budget, the leading product certificate is minimized by balanced slot counts. Neither result optimizes a sum of marginal errors.

5. **Unknown-profile gate.** If only total action a is known and no pointwise envelope is supplied, every finite latent rate cap has minimax certificate a². The actual ideal-model robust error supremum is sin²(min(a,π/2)); arbitrarily narrow admissible pulses approach it. Fixed deterministic slots are defeated by placing the pulse inside one gap. This is a countermodel to discarding the fixed-J/profile premise, not to the original theorem.

## Strongest equally informed incumbent and paid counts

The fixed-slot random pulse-or-identity operation is already explicit in [Santos–Viola 2005](https://arxiv.org/html/quant-ph/0511121), and the broader random-DD control and bath model is in [Viola–Knill 2005](https://arxiv.org/html/quant-ph/0511120). [Wang v2, 2026](https://arxiv.org/html/2610.01521v2) supplies fixed refresh, persistent environment treatment, and the finite-duration covariance obligation. Exact source-relative new content here is the stated uniform minimax theorem, witness and sharp resource comparison; exhaustive novelty is UNKNOWN. See [PRIMARY_PRIOR.md](PRIMARY_PRIOR.md).

N fixed independent fair-toggle opportunities use at most N and on average N/2 **interior actual involution flips**. A telegraph implementation with mean n physical flips has latent complete-pinch budget Λ=2n. At N=2n, fixed slots have certificate a²/(2n+1), while the best unconstrained Poisson certificate is a²/(n+1); the peak cap can only worsen the latter. For 0<a≤π/4 and N≥1, the exact fixed-slot robust error is strictly below the Poisson robust minimax lower bound. This upgrades the within-model comparison beyond upper-certificate constants.

Initial private seed/frame, terminal inverse, every coordinate's full support, randomness/control acquisition, reset, finite ramps, and reservation time must still be charged. The latent identity λ=2γ never turns into twice as many actual telegraph pulses. If exact physical full pinches are instead the acquired primitive, deterministic versus Poisson **measurement** counts are a separate comparison. Public deterministic DD can be defeated under arbitrary time dependence known only by an envelope; with a known constant commuting interaction, spin echo cancels it exactly and is a better informed incumbent.

## Independent verification

`python3 check.py` uses NumPy 2.5.3 only and writes [CHECK_RESULTS.json](CHECK_RESULTS.json). It executes newly authored code, never the supplied scripts. All checks passed:

- Peak energy formulas, regime boundaries, admissible attaining schedules, and 360 random feasible rate profiles.
- 160 literal master-equation qubit instances with nonuniform j and λ, verifying the new uniform physical-error sandwich.
- Explicit sink-bath endpoint effect matrices attaining the exact minimax, including a saturated gap, and exhaustive fair-toggle Walsh averaging agreeing with the physical endpoint effect.
- A noncommuting two-selected-seed/shared-qubit-bath model where direct Walsh averaging equals the virtual fixed-pinch effect to 5.1×10^−18 and respects the sharp product certificate.
- 1,600 partition diagnostics for equal-action optimality, integer slot-allocation enumeration, strict robust incumbent comparisons, and concentrated-profile countermodels.

The analytic proofs establish uniform and global claims. These finite checks establish only the displayed identities/examples and may catch algebraic or implementation mistakes. Default and bundled Python environments lacked SciPy; the final authored check uses available NumPy and needs no install.

## Remaining gates

No full physical dephasing dilation, finite-width/private-controller support theorem, microscopic generator, useful memory threshold, or hardware data were acquired. A final inverse alone does not prove correctness throughout a finite operation. The original additive selected-sign independence, pointwise ideal covariance, whole reservation, complete support/common decoder, and ramp/noise model are still required. The finite-action shared-bath joint upper ∏Q_i and the coupled peak-active product optimizer are not proved here. Every such open obligation is retained rather than promoted from the singleton theorem.

Source bytes/pins and inspected primary URLs are recorded in INPUT_RECEIPTS.json and SOURCE_URLS.json. FROZEN_MANIFEST.json records this worker's final artifact hashes; hashing is an integrity receipt only.
