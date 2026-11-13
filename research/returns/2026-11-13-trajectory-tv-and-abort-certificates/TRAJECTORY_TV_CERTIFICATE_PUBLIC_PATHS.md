# Rigorous error accounting for a truncated trajectory MPS sampler

This is standard trace-distance/channel-contractivity machinery applied to the actual chronological sampler, not a new theorem about low entanglement or efficient 2D simulation.

## Required conventions

The input is exact. Every noise/category coin and classical measurement record is retained. Each physical or framed operation is the correct quantum instrument conditioned on the preceding classical record. Measurement probabilities are computed from the current APPROXIMATE normalized state, then the matching normalized postmeasurement branch is used. This is the approximate simulator's legitimate instrument; it is not postselection on a fixed desired record.

Every compression is a normalized Schmidt truncation: in canonical gauge, discard squared Schmidt weight w relative to the state immediately before THIS compression, and renormalize the retained state. Then its pure-state trace distance is exactly sqrt(w). Counting a raw discarded singular-value norm from noncanonical tensors without checking state normalization is NOT sufficient.

If a nonlocal gate is implemented by several swaps, MPO applications, or split steps, charge EACH compression, including internal routing steps. Exact swaps and exact gauge changes cost zero approximation error but still cost runtime. Floating arithmetic and approximate gate-synthesis errors need separate bounds.

## Joint classical-quantum proof, including conditioning

Use trace distance D(ρ,σ)=||ρ−σ||_1/2. Store the entire classical record in an orthogonal register. Let ρ_j be the exact joint record/state after j instruments and σ_j the approximate simulator's joint state. The next physical instrument, including outcome-dependent classical control, is a single CPTP map E_j on this joint state. Therefore

D(E_j ρ_j,E_j σ_j) <= D(ρ_j,σ_j).

Immediately after this exact instrument on the simulator ensemble, let branch h have probability p_h and normalized state |ψ_h>. Replace it by its compressed |φ_h>. The resulting joint distance is

Σ_h p_h D(ψ_h,φ_h) = Σ_h p_h sqrt(w_h).

The triangle inequality gives a recurrence. Iterating across all compressions, and finally measuring output bits/discarding the record, gives

TV(P_exact,P_MPS) <= E_simulator[Σ_j sqrt(w_j)].

This expectation is over the approximate simulator's OWN records, including its Born outcomes and sampled noise flags. There is NO inverse-small-measurement-probability penalty. Conditional state error on an individually rare branch can grow; the global record-weighted inequality already pays the branch probability. Arbitrarily postselecting a particular record would be a different task and is not covered by the same unconditional bound.

The same proof covers frame-MPS: diagonal-frame reset measurement and subsequent recorded local Z feedforward form a CPTP instrument. Classical controls may correlate different quantum components; preserving the whole record makes the argument valid. Changing the physical ensemble or discarding record-dependent phases is not an approximation covered by this accounting.

## An implementable deterministic error certificate

Maintain B=Σ sqrt(w_j) along each sampled trajectory. If the implementation guarantees B<=δ on EVERY trajectory, then the final full-output TV error is <=δ (plus separately bounded numerical/gate error). One simple policy with at mostL remaining compression steps is to choose the smallest bond rank whose normalized discarded weight is <=(δ/L)^2 at each step. Adaptive reallocations of the remaining budget are allowed if their total never exceedsδ.

This may require exponentially large bond ranks. A bounded error budget is NOT a polynomial-runtime proof.

## Bond caps and aborts

If rankχ is capped, abort BEFORE a compression would exceed the remaining error budget. Return a fixed fallback output, not a newly resampled successful trajectory. In analysis, replace the abort by exact simulation of the remaining quantum process. This hypothetical continuation has accumulated compression budget <=δ, so differs from the physical process by at mostδ. Replacing its abort continuations by the fallback changes output law by at most the approximate simulator's abort probability α. Hence

TV(P_exact,P_capped) <= δ + α + numerical_error.

The exact simulator need not be run on abort; it is only the coupling argument. A finite observed abort rate is NOT an upper bound on α. One can report a separately stated binomial confidence upper bound, or prove α analytically. For zero aborts inN independent trials, the one-sided confidence1−η upper bound is1−η^(1/N), approximately log(1/η)/N. Do not silently identify no observed aborts with zero bias.

If the sampler already aborts for an auxiliary-graph cap with proven probabilityα_graph, include that term too (or use one bound for the union). Do not reject/resample either kind of bad trajectory.

## Comparing direct versus frame MPS fairly

Use the same physical circuit, noise flags, target full-output TV budget, numerical precision, and rank cap. Each representation needs its own cumulative discarded-weight certificate. Record actual SVD count, maximum/mean bond rank, wall time, maximum live storage, abort count, and cumulative B. The frame may require fewer quantum operations but larger dressed-gate supports; charge every resulting routing/MPO compression. Direct and frame approximate measurements can yield different outcomes even with coupled uniforms, so trajectory agreement is not a proof of equal error.

For small systems, compare all output probabilities or independent dense trajectories as implementation checks. For large systems, report ONLY the proven δ+α guarantee and measured resources. Neither small-state agreement nor average low observed bond rank proves an asymptotic scalable phase.

## Checked implementation-specific SVD bound

Inspection of frame_mps/mps_sampler.py confirms canonical-center QR motion precedes each two-site SVD. A routed pair at distance d uses2d−1 SVDs, at most2n−3. At degree4 each dressed rare has at most7 incident ZZ edges, applied forward and backward, plus one Q: at most15 routed pair gates. Thus J_frame<=15M(2n−3). Direct physical simulation uses at most D plus Q per pair slot, giving J_direct<=2M(2n−3). Measurements and gauge QR moves do not truncate.

Equal per-SVD tolerance does not mean equal global truncation bounds: the frame bound is7.5 times the direct bound. For identical targetδ one may use tolerance δ/J separately. Alternatively compare both under the larger common certifiedδ while acknowledging the direct implementation is being run more accurately than necessary. Abort-rate uncertainty still dominates the reported finite strict-cap tests.

## Why conditional-trajectory error is not a certificate

Let |ψ>=sqrt(1-w)|00>+sqrt(w)|11>, compressed to|00>, so local trace error is sqrt(w). Measure the first qubit in a basis containing |m>=sqrt(w)|0>+sqrt(1-w)|1>. On outcome m the exact remaining qubit is|+>, while the compressed remaining qubit is|0>: their conditional Z-output TV is1/2 regardless of how small w is. The event has probability2w(1-w) versus w. The full joint classical output TV is only w. Therefore a large conditional discrepancy need not violate the global certificate, and observing small conditional discrepancies cannot establish that certificate either.

## Established primary machinery

- G. Vidal, Efficient Classical Simulation of Slightly Entangled Quantum Computations, Physical Review Letters91,147902(2003), DOI10.1103/PhysRevLett.91.147902, arXiv quant-ph/0301063: entanglement-limited pure-state simulation.
- J. Dalibard,Y. Castin,K. Mølmer, Wave-function approach to dissipative processes in quantum optics, Physical Review Letters68,580–583(1992), DOI10.1103/PhysRevLett.68.580: stochastic pure-state open-system trajectories.

Primary publisher/archive records were checked during this pass. Combining conventional trajectory simulation with MPS is not presented as a new primitive. The research-specific question is whether this circuit's exact frame and noise produce a useful certified rank distribution; no such general theorem is supplied here.

## Stronger practical budget: condition on presampled physical flags

The fixed15M(2n−3) bound is needlessly strict for rare gates. All physical reset/rare flags are sampled before quantum outcomes. Moreover, the known-basis STATUS (not its bit value) is determined by those flags: initially known, both targets become unknown after Q, reset endpoints become known. Thus the entire list of two-site gates surviving known-basis phase reduction can be counted before simulation, for any chosen static ordering. The ordering may depend on these flags but not unobserved Born outcomes.

Use the actual deterministic count J(flags,order), set local amplitude allowance δ/J, and keep strict rank caps. Every individual flags realization then has total truncation budget<=δ, so averaging preserves the same full-output guarantee. For the original SWAP-routing backend, a two-site call at distance d costs2d−1 SVDs. A validated nonlocal bond2-MPO backend that truncates each traversed bond once costs d SVDs; this must be checked against its actual implementation. trajectory_budget.py computes these counts from a weighted two-site operation graph.

An additional exact frame simplification removes the endpoint-internal ZZ edge from forward/backward conjugation: [Z_u Z_v,X_u X_v]=0. Only edges crossing from one target to a neighboring control are needed. This reduces gate/SVD count, not approximation accuracy.

For a fair strong baseline, give direct physical MPS the same ordering optimization, nonlocal gate implementation, trajectory-conditioned δ budget, rank cap, and outcome handling. Improvements that vanish under this baseline should be reported as implementation improvements, not a new simulation regime.

## Abort estimation usable with optional stopping

abort_confidence.py constructs one-sided Clopper–Pearson-style upper limits on an immutable sampler's abort probability. SciPy only proposes an endpoint on a rational grid; exact INTEGER binomial-CDF arithmetic verifies the endpoint. At predetermined sample-count checkpoint j, spend confidence error eta/[j(j+1)]. The total across all fixed checkpoints is at mosteta, so choosing when to stop among them preserves coverage. For arbitrarily data-adaptive check times, spend eta/[n(n+1)] at sample count n instead; this unions over EVERY possible n. Do not assign the j-th spending amount to an adaptively chosen sample size without this correction. Distinct compared sampler configurations additionally require allocated confidence budgets or fresh independently evaluated final candidates.

Freeze the complete algorithm (ordering rule, chi, tolerance policy, circuit parameters) before using new independent holdout seeds. Tuning on the same trajectories and then quoting their bound is invalid. Confidence is statistical, not an absolute all-randomness proof, and must be stated explicitly.

Examples at fixed99% confidence: zero aborts in30 trials only implies alpha<=.142305; zero in1000 implies <=.004595; zero in5000 implies <=.000921. The full-output bound is δ plus this upper bound, with99% confidence, plus any independently controlled numerical error. Small pilot samples cannot establish tiny TV error.
