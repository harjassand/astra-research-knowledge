# After-evidence assessment: exact preparation target, missing physical gate

## Evidence consulted

- robust_native_memory_20261101/ROOT_ROBUST_NATIVE_MEMORY_JOIN.md and native_history_holder_lemma.md.
- native_thermal_interactions_20261101/ROOT_NATIVE_THERMAL_MEMORY_JOIN.md.
- filtered_code_preparation_20261101/ROOT_FILTERED_THERMAL_ENCODER_JOIN.md.
- quantum_thermal_phase_20261101/FIXED_SYSTEM_MKS_REPAIR.md.
- quantum_noise_release_20261101/EXACT_COMPLEX_POLE_BARRIER.md, README_BOUNDARIES_DELIVERY.md, INDEPENDENT_CONSTRUCTOR.md.

The quotient identity in the independent direction is an elementary reduction, not a claimed new general theorem or breakthrough. The supplied native theorem already identifies the retained gauge/clock/bath marginal and is reference-safe.

## Sharper conclusion

An ideal native Gibbs-source algorithm would be valuable, but is not the physical loading gate. Running it inside a conventional fault-tolerant computer and releasing N unencoded carriers through fixed-rate local noise can produce an extensive joint-state disturbance. The present stationary-reference proof does not certify that disturbance for long storage. Its failure to certify is not a no-go for ordinary benign release noise.

The strongest positive construction presently justified by the supplied evidence remains ideal preparation in an admitted baseline class plus exact-H equilibrium storage. I have not obtained a local noisy native quotient-thermalizer, and should not promote a plan into that result.

## A concrete, larger admissible basin: stationary warm starts

A useful exact sufficient criterion avoids full trace-distance Gibbs preparation. Let Ω be stationary under H, P the bad projector, and p=Tr(PΩ). Suppose a prepared input/reference joint state Γ_RSE has physical marginal

    Γ_SE ≤ K Ω_SE.

Then for all t, Γ_SE(t)≤KΩ_SE and Tr[P Γ_SE(t)]≤Kp. Since each logical commutator is supported on P on both sides, the existing derivative consumer gives an error of order

    ε_initial-decoding + C v n T K p.

The estimate is reference-safe: bound logical-Pauli/reference-observable derivative pairings by the norm of the commutator times Tr(PΓ_SE(t)), then apply the same fixed-logical-dimension norm conversion used by the supplied theorem. No assumption that Γ_RSE itself is product or dominated by Ω tensor an independent reference is necessary.

If exact Ω domination is inconvenient, assume Γ_SE≤K Ω_bar, where Ω_bar is the logical twirl and ||Ω_bar-Ω||₁=δ_tw. Stationarity and contractivity give Tr[P Γ_SE(t)]≤K(p+δ_tw), hence the same conclusion with that replacement. The ideal overwrite has K=2 against Ω_bar.

Thus K may grow as exp(o(n^η)) while preserving a reduced stretched-exponential storage exponent. The real loading target could be sub-barrier max-relative-entropy overhead, not globally accurate Gibbs preparation. This is a sufficient condition; low mean energy, low relative-entropy density, or local-marginal agreement do not imply it. A generic fixed-rate local release channel can have an extensive log K, so it does not pass automatically.

## Most focused constructive experiment/theorem

Use an explicitly accessible finite engineered bath during loading. Seek a local dissipative loader whose invariant state is the actual joint Gibbs state, or whose output has the above warm-start envelope after logical overwrite, and prove mixing only modulo the logical subsystem. Require a microscopic physical implementation with fixed noisy reset resources, bounded control strength, and charged entropy export. The loader may turn off before the exact-H storage interval.

A successful proof must address three different facts, none implied by the others:

1. The Gibbs target is a fixed point of the actual imperfect loading process.
2. The gauge/clock/bath quotient mixes in polynomial or exp(polylog N) physical time, despite potentially slow logical-sector mixing.
3. A WRITE of an unknown entangled input either preserves that stationary envelope or adds only an admissible one-time error.

A designed Davies/Gibbs sampler may be a useful mathematical loading model, but its energy resolution, local implementation, resets and stationary-state sensitivity must be charged. The no-Davies claim is about storage; it does not ban a properly justified engineered loading process. Generic noisy resets cannot be declared Gibbs preserving by nomenclature.

## Why READ is a different and easier gate

At READ there is no later exponentially long idle interval. A plausible direct closure combines the actual Gibbs syndrome witness bound with a local-stochastic terminal-fault bound: fixed-depth U† increases fault support only by fixed factors; error correction / logical teleportation can then extract to a conventional FT processor. This needs an actual terminal extraction construction and witness robustness to combined thermal syndromes and circuit faults. It does not require the post-read gauge/bath state to be stationary.

The analogous decoder-threshold argument does not close WRITE, because correcting the logical effect of immediate faults leaves an altered gauge/bath state for the later hold.

## Relationship to the parent's native-path proposal

Trading explicit commuting check strength against native induced J0 while turning off clock hopping could provide a uniformly protected analysis/preparation path. Direct finite-patch mixed-source/rod calculations of local reduced density matrices could avoid a circular marginal oracle for block Petz gates. Both are worthwhile ideal-source gates; they still need a physical terminal-release argument or a directly stationary loading implementation. The known complex-pole example forbids rescuing this by assuming a volume-uniform jointly analytic inverse-noise operator logarithm.

## Stopping condition and judgment

The constructive research gate is closed only by an explicit physical loader/write map with a proved quotient-distance or warm-start-envelope bound under a specified fixed-noise model, followed by a read extractor and a matched resource comparison. Neither an ideal circuit nor a numerical finite-size fidelity plot establishes this gate. No end-to-end usable passive advantage has been earned in this pass. The warm-start criterion and separate terminal-read gate make the next question testable without falsely demanding exponentially accurate initialization.
