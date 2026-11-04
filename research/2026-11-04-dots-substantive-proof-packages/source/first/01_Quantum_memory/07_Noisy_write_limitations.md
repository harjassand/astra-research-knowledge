# Unary noisy terminal WRITE: physical release contract and exact remaining gate

2026-11-03. Independent construction/audit. Sources: `UNARY_FULL_WRITE_HOST_AND_COMPOSITION_AUDIT.md`, `RING_TERMINAL_HANDOFF_LEMMA_20261103.md`, and `physical_memory_handover_20261102/{CONSTRUCTOR_RESULT,ROOT_AVERAGE_OUTPUT_THERMAL_BASIN}.md`. The new ideal preparation is accepted subject to its stated analytic audits. No new circuit-level threshold for the recursive code is presumed.

## Verdict first

The all-sector thermal ancilla and interacting syndrome sampler remove the earlier IDEAL isolated-memory preparation obstruction. A constant-rate noisy terminal release remains a different theorem. Below is an explicit physical-noise output class and reference-safe short-HOLD interface. Neither that interface nor ordinary fault-tolerant simulation proves exponentially long passive HOLD. The exact unresolved gate is a time-uniform nonstationary basin for this output class, or a physically implemented Gibbs-subpreserving terminal channel. No access denial occurred.

## 1. Target and physical controls

Write the ideal thermal logical encoding as

 W(rho_LR) = U [sum_sigma mu(sigma) (V_sigma tensor I_R) rho_LR (V_sigma^dagger tensor I_R) tensor tau_sigma] U^dagger.

Here V_sigma is the same decoder-frame embedding used in the storage proof; tau_sigma is the complete, all-number-sector conditional clock Gibbs state, not a one-particle truncation. U is the bounded-depth bounded-spread prefix Clifford at fixed K and degree. The classical sample is independent of the unknown logical/reference input. On maximally mixed logical input, W(I/d_L) is the isolated-memory Gibbs state rho_beta. This does not include an inaccessible correlated bath.

Specify a local stochastic circuit model: preparations, gates, measurements and each bounded-time idle are locations; for every set F of locations, Pr[F are faulty] <= p^|F|. Faults may be chosen from local Pauli channels for the concrete release construction. Independent depolarizing faults are a special case. A fixed-rate Markovian bath during a gate is an additional noise source, not a reason to omit idle locations. If converting its generator to circuit-level noise, provide the local-norm/rate assumption and charge gate duration.

The ideal polynomial preparation may be simulated in an active FT architecture with local routing, reset, measurements and protected classical control. Its internal channel error can be reduced to delta_int with threshold overhead PROVIDED that architecture's noise model and threshold apply. Outputting n bare qubits is not covered by the statement that its internal logical circuit is accurate. A concrete output interface must specify the final decoders/release gadgets. Disjoint block release can avoid cross-output spread, but needs n blocks, their geometry, their ancillas and their durations counted; it is not constant-density n-qubit hardware for free. The prior macroscopic CSS teleportation alternative avoids n independent blocks, but still needs an actual repeated-measurement threshold and thermal-clock output interface.

For a bounded-depth final physical Clifford release circuit, each fault affects at most b output registers and each output register has at most a possible fault ancestors. Its residual support therefore obeys

 Pr[S subset residual support] <= [a p^(1/b)]^|S|.

This follows by assigning each required output site to an ancestor fault, then applying the location local-stochastic bound. It is not applicable to the entire polynomial-depth thermofield circuit without an FT analysis. The physical noise acts on DATA AND CLOCKS. A fault-free final interval or noiseless clock release must not be silently granted.

## 2. Honest full-output contract

A sufficient release contract, in half-diamond convention, is

 (1/2)||W_phys - N_out o W||_diamond <= delta_int,

where N_out is an input-independent local stochastic physical Pauli channel with bounded parameter p_out. A slightly more general, adequate contract permits sigma-dependent Pauli laws nu_sigma, provided their support tails are uniformly bounded conditional on every sampled sigma. Merely conditioning the circuit on success does not establish either contract. One can instead use a subnormalized good-history channel and charge the bad channel's total mass, while proving the joint sparse-support bounds without renormalization.

Conjugating an output Pauli through U gives a bounded-support data Pauli times a clock Pauli. Bounded spread/incidence converts p_out to p_D <= C p_out^(1/b_U). Clock faults generally change tau_sigma and its correlations. They do not spoil the immediate data decoder when the data Pauli is correctable: on each correctable branch the logical/reference state factors from the remaining syndrome/clock state. Thus the construction preserves arbitrary reference entanglement without assuming the noisy clock state is thermal.

For a static admission estimate one needs the actual code theorem: a sparse thermal syndrome law, plus bounded-support local-stochastic data errors, stays in the correct decoder frame except with probability f_n. If mu has local-stochastic check parameter q_th and each data site changes at most h checks, a conservative error-syndrome parameter is q_err <= C' p_D^(1/h). Uniform conditional sparsity permits a joint covering bound q_th+q_err. Using the existing any-local-stochastic decoder-instability theorem at O(n) canonical single-site prefixes then gives the corresponding poly(n) exp[-c n^eta] admission error when its threshold hypotheses hold. This is conditional on the actual theorem's constants and its applicability to mu; bounded check weight alone is not that theorem.

The resulting immediate decoded half-diamond error is at most delta_int+f_n. It does NOT show W_phys is globally close to W, or that its average output is Gibbs dominated with a useful constant.

## 3. Short passive HOLD with actual bounded-rate Davies noise

Assume exactly the sectorized Pauli-Davies bath contract of the ring handoff lemma, including the Lamb-shift restriction. A physical channel has data footprint at most r; each data qubit meets at most c channels; each channel's total hazard is bounded by Gamma. The Bohr components retain their data Pauli label even though they are not spatially local on clocks. No-jump evolution acts trivially on bare logical multiplicities inside a fixed syndrome.

Independent dominating Poisson clocks give the bath support parameter

 p_B(t) = c [1-exp(-Gamma t)]^(1/r).

The clocks can be sampled independently of initial syndrome and terminal faults; actual acceptances may depend on the full state. This yields a terminal-plus-bath support parameter p_D+p_B(t). Apply the static threshold/witness argument to that enlarged support, with the initial thermal syndrome included. This proves a positive bounded handoff interval if

 q_th + C' [p_D+p_B(t)]^(1/h) < q_*,

where q_* is the actual admitted decoder-witness threshold. Uniform constants can be very unfavorable. Ancillas may now be arbitrarily far from Gibbs; the short-time bound uses upper jump rates, not their temperature or equilibration. This result is reference-safe, by branchwise Pauli correction and the bad-history probability bound.

It is restricted to this Davies contract. It is not a theorem for the more general exact joint Hamiltonian bath with arbitrary allowed V. For that model use the actual joint stationary state and its own bad-projector estimate.

## 4. Why the ideal thermal preparation does not finish long HOLD

The stationary storage theorem starts from the thermal logical encoding. Terminal N_out changes this state. At constant p_out, typical residual error weight is extensive. Global trace-distance closeness to W cannot be obtained from an internal FT error estimate alone.

Even classical product states show the operator-domination obstruction sharply. Let rho = diag(1-a,a)^tensor n, with 0<a<1/2, and independently flip each site with probability p>0. The output is diag(1-b,b)^tensor n, b=a+p(1-2a)>a. Any inequality N(rho)<=kappa rho requires

 kappa >= (b/a)^n.

Thus arbitrarily small constant stochastic p can require exponential-in-volume domination. This is a counterexample to a generic deduction from local stochasticity, not evidence that the actual unary memory necessarily fails. Multiplying a stationary rare-bad estimate exp[-c n^eta] by this kappa loses the advertised protection when eta<1.

Short-time support accumulation also cannot be iterated passively. A hypothetical decoder used in a proof does not physically reset defects; the state after the interval is not a new sampled thermal state. Repeated actual recovery is an active memory protocol.

A sufficient long-HOLD theorem is, for this specified N_out and actual storage channel S_t,

 sup_(rho_LR) D[(Dec tensor id_R) S_t N_out W(rho_LR), rho_LR] <= epsilon_n(t)

uniformly through the advertised lifetime. One route controls the evolving dangerous-cluster distribution; another proves the average-output domination N_out(rho_beta)<=kappa_n rho_beta with log kappa_n below the barrier exponent, together with initial admission. Neither follows from the ideal polynomial loader.

There IS an instructive restricted positive case: if the only release noise is an exact Gibbs-preserving Davies evolution for a short duration, then N_out(rho_beta)=rho_beta, and short-time logical admission plus the applicable stationary theorem can propagate the result. But replacing generic noisy local gate release by that exact thermal channel is a new hardware/noise restriction. The preceding physical output gates are still faulty, and obtaining the exact Gibbs state before that interval is the disputed operation. This special case does not close the generic writer.

Alternatively, allowing every physical location's fault probability to shrink as delta/G for G charged WRITE locations makes the no-fault union bound <=delta. Then ideal-channel composition gives long-HOLD error delta+epsilon_ideal(t). This is a genuine vanishing-noise construction, not a fixed-positive-rate threshold theorem; reaching that rate on final bare carriers requires an explicit physical service.

## 5. Strongest fair alternatives

The active comparator gets the loader's same local controls, routing volume, measurements, resets, cooling, gate rates, classical hardware and interaction-switching capability. It can keep its protected output encoded and perform repeated recovery rather than expose n terminal carriers. The same FT architecture used to justify delta_int is therefore an immediate baseline; one cannot grant its threshold to WRITE but deny it to active HOLD. A specified local concatenated architecture with p_(j+1)<=A p_j^2 and space factor B per level has space polylog(T/epsilon), with exponent log_2 B before additional local-routing costs. At T=exp(c n^eta), this is polynomial in n; there is no generic exponent advantage from stretched-exponential passive lifetime alone.

The native resonant-clock comparator already has ideal overwrite/Gibbs-subpreserving admission in its admitted scope and broader perturbative storage statements, but also lacks a complete noisy physical writer under generic terminal faults. The unary candidate's new ideal positive polynomial loader is substantive progress relative to the older conditional-clock obstruction. It is not a noisy device advantage until this release/basin gate is solved.

The possible passive benefit remains avoiding repeated control/reset work during HOLD. Quantify that against the active comparator's integrated operations/entropy export and the passive device's actual refrigeration/coupling costs, not just its preparation circuit or absence of externally commanded gates.

## Conclusion

Earned: explicit thermal logical target, reference-safe local stochastic release class including clock faults, a conditional static threshold admission bound, and a bounded-time passive handoff bound under the specified Davies model. Not earned: the release gadget's whole-circuit threshold at the claimed hardware density, a useful Gibbs-domination estimate for generic terminal faults, or long nonstationary passive retention. The blocker is mathematical and physical, not an unavailable tool, permission denial, or impossibility theorem.
