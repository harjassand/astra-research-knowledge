# Native autonomous realization gate: thermal energy selection is conditional; finite-clock compilation is not yet admitted

Independent physical-interface assessment, 2026-11-01. Read the shared Tanner controller, TANNER_WITNESS_PHYSICAL_COST_AUDIT.md, and JOINED_TANNER_MEMORY_DRAFT.md. No hardware actions. Result: no native finite-noisy implementation has been established. There is a concrete autonomous thermal mechanism IF its Hamiltonian and local couplings are physically earned; the missing premise cannot be replaced by a pulse/adiabatic-elimination error bound proportional to total time.

## 1. What the existing theorem actually requires

The joined theorem starts with the time-independent correction generator Σ_v κ(Φ_v−id), with joint-syndrome-conditioned witness corrections, plus small admitted local perturbations on its data/witness system. It permits coherent witness errors. It does NOT include physical controller progress registers, temporary syndrome ancillas, locks, meter states, reset devices or propagation delays as a proved enlarged system.

Replacing Φ_v by a finite circuit is not merely changing a numerical constant. It introduces intermediate states and nonzero durations in which overlapping controllers or physical errors can change the sampled predicate. A correction downhill for an earlier snapshot need not be downhill when applied. This stale-snapshot issue exists even if every elementary circuit gate is perfect.

The warm real-meter mechanism previously checked supplies self-adjoint selected measurement branches. Its matched quadrature waveform requires a phase/timing reference, and conditional witness feedback is a separate operation. It therefore does NOT supply an autonomous Φ_v implementation. Its thermal width, discrimination/separation, coupling, bandwidth, readout and reset costs also prevent treating a warm meter as a sharp high-success projector for free.

## 2. A concrete autonomous thermal alternative, at the exact model level

Suppose one physically realizes the commuting Hamiltonian

H_sys=E W

on the actual data/witness system, and couples a fixed local witness-flip operator T to a stationary thermal reservoir through a TIME-INDEPENDENT interaction. In a Davies-type energy-resolved Markov model, decompose

T=Σ_Δ T Π_Δ,

where Π_Δ selects local labels with W(after T)−W(before T)=Δ. Because W is a bounded-incidence sum of commuting local terms and T has bounded support, these energy-difference projectors depend only on a bounded neighborhood. They do not require a global syndrome measurement. The bath's frequency selectivity then produces the conditional jumps as energy-selection rules, rather than an external controller evaluating a truth table.

For a Hermitian flip T=T†, thermal detailed balance relates the uphill and reverse downhill rates by a Boltzmann factor exp(−β E Δ), Δ>0, subject to the actual bath spectral factors. A finite temperature does not eliminate uphill events, but those events can be charged as local dissipative noise; pure reset is not conceptually necessary.

One can propose all of a fixed finite list of allowed local witness flips instead of choosing a perfect minimum move. Let A be the number of proposals offered at a location, and normalize the TOTAL attempt rate there to κ_0. If every available strictly downhill move has rate at least κ_eff>0, for example κ_eff=κ_0 r_min/A under a normalized spectral model, the previously proved extensive move count gives

L_down^* e^(aW) ≤ −κ_eff (1−e^(−a)) W e^(aW)/K.

If the total uphill offer rate is bounded by C n κ_0 exp(−βE), and any offered move changes W by at most b, then

L_up^* e^(aW) ≤ C n κ_0 exp(−βE) (e^(ab)−1) e^(aW).

Zero-energy transitions commute with this potential. Thus a finite βE can make this explicit uphill load fit the same local drift budget, provided the actual constants and move support are paid. An exponentially large fixed proposal list reduces κ_eff or demands more hardware; it is not assigned exponential free rate. This is an actual autonomous thermal MECHANISM at the stipulated generator/Hamiltonian level, not a practical implementation or a new thermodynamics result.

## 3. Why this does not yet earn native hardware

First, W is an O(Δ²)-body function of stabilizer and witness operators. Its Hamiltonian terms are not a collection of supplied native two-/three-body couplings. Replacing ideal conditioned projectors by an unpriced exact W Hamiltonian only relocates the hard step. Likewise the mismatch witness move can flip O(Δ²) bits at once. A bath coupling directly to that flip is still a many-body interaction, not a native local single-bit thermal transition. Single-bit flips cannot be substituted unless an extensive downhill theorem is proved for that altered move set; local energy barriers in the move implementation matter.

Second, the energy-resolved Davies generator is itself a controlled weak-coupling/secular model. Here W is integer valued and a local move changes it by a bounded integer, so the relevant Bohr frequencies form a fixed finite set: the generic objection about exponentially dense many-body spectral gaps is NOT the obstruction in this specific construction. A finite microscopic reservoir and finite coupling do not automatically generate it exactly for exponentially long times. A theorem comparing actual and effective dynamics by O(ε T) is insufficient. The actual bath/controller must be included in the admitted local dynamics or a time-uniform LOCAL stability/weighted-generator principle must be established. Thermal-rate heuristics alone do not establish that principle.

Third, finite mediator gadgets used to synthesize W add their own excitation sectors, errors and noise. A low-energy effective Hamiltonian approximation is not an enlarged-system memory theorem. One must exhibit an actual potential W_tilde and protected subsystem on all relevant mediator states, with restoring drift and boundary/holonomy control under their real finite-temperature dynamics. Small leakage probability per gadget cannot simply be multiplied by an exponentially long storage time and still called a fixed-parameter construction.

These are missing construction/proof obligations, not physical no-go statements. Large fixed energies/rate ratios may be allowed by a mathematical model; the source's catastrophic sufficient constants are not used here as impossibility evidence.

## 4. What an autonomous finite circuit would have to prove instead

An alternative is a finite-state local controller which extracts the commuting syndrome, computes the finite truth table, flips witnesses, uncomputes and thermally resets. A biased stochastic clock/chemical cycle can replace an externally prescribed gate sequence in principle, with finite reverse/error rates. However the complete implementation must explicitly address:

* Intermediate syndrome extraction can temporarily correlate data and apparatus. Resetting an interrupted extraction may induce a bounded-support data channel, not merely a classical flag error.
* Overlapping operations can make predicates stale; local arbitration, revalidation or a progress-aware Lyapunov proof must charge this.
* Faulty locks/progress states can suppress correction availability. A mean successful-cycle rate is not the pointwise extensive drift assumption of the joined theorem.
* Reverse steps, false reset, and unfinished computations must be included with actual rates. Declaring the program or clock perfectly cyclic is a cleaner-controller assumption.
* A fault must remain confined to a bounded support, or a quantitative decaying-tail interaction bound must replace the current fixed-support alphabet.

The exact needed positive admission would be either:

(A) an operator drift inequality for a physically specified enlarged W_tilde and full microscopic Markov generator, plus a flat protected low-potential component; or

(B) a proved local comparison theorem converting the native controller into ideal correction plus bounded local perturbations with constants independent of system size AND storage time, including its internal memory and overlapping use.

Neither has been supplied. A circuit's worst-case finite-run diamond error, a clean-clock dilation, or a bare adiabatic-elimination theorem does not imply A or B.

## 5. A concrete discriminating test, before scaling claims

For one physically specified finite local-code instance and its bounded-overlap controller neighborhood, enumerate the actual controller states and native allowed interactions. Include reset/excitation states and neighboring-controller progress. Test the candidate weighted drift inequality on those states, NOT only on a correctly initialized idle apparatus. In particular test:

1. Many violated compatibility blocks with all local controllers in allowed busy/reset states: where is restoring drift stored?
2. A snapshot measured just before a neighboring valid update changes its predicate.
3. A single progress/lock fault followed by continued operation: can it block repairs or apply unchecked flips indefinitely?
4. Finite-temperature uphill/gadget excitations, with no perfect preparation assumption.

A counterexample to the proposed enlarged inequality identifies the missing operation directly. Passing a finite neighborhood inequality would be a useful component; it still requires an overlap/composition proof for the lattice and a valid finite code. No such numerical test is claimed to have been run here.

## Final boundary

The conditional thermal energy-selection construction explains how an autonomous finite-temperature mechanism COULD replace explicit measurement/feedback without a global clock. At present it assumes native H=EW and the required bounded-support flip couplings, precisely the physical resources not yet earned. Finite noisy circuit alternatives still lack a joint apparatus-inclusive drift/admission theorem. Therefore the native realization gate remains OPEN, and the abstract Tanner memory theorem must retain its explicit ideal-channel scope.

An ordinary active qLDPC implementation receives identical interactions, reservoirs, mediator circuits, reset power, interconnects and rate budgets. No hardware advantage or cleaner-controller distinction is established. A narrow primary-literature check of the Davies weak-coupling premise was made. The primary research article “Efficient quantum thermal simulation,” https://www.nature.com/articles/s41586-025-09583-x , explicitly distinguishes Bohr-frequency-resolved Davies jumps and their secular/weak-coupling construction; E. B. Davies, “Markovian master equations. III,” https://numdam.org/item/AIHPB_1975__11_3_265_0/ , is a primary mathematical source in that series. The general dense-spectrum criticism in the former is not imported into this integer-W model. No denied/stopped source was accessed.
