# Independent constructor: reachable thermal-memory loading

Date: 2026-11-01. Derived from target and factual obstruction, without inspecting parent files or preferred construction. Later reconciled with parent's matching coherent-Pauli construction.

## Result first
A global decoder unitary is unnecessary for an IDEAL overwrite. Coherent syndrome extraction, reversible decoder-sign evaluation, three controlled decoded Paulis, and full uncomputation implement an exact logical SWAP while preserving the gauge/environment marginal. This establishes circuit existence, not a noisy reachable loading theorem. Neither efficient actual interacting-Gibbs preparation nor a gauge-preserving fault-tolerant implementation follows from standard fault tolerance.

## Algebraic construction
Write physical memory as a decoder-defined subsystem L tensor G, with inaccessible environment E. Let P_s be stabilizer syndrome projectors and let the chosen Pauli decoder correction be R_s. Decoded Pauli Q_mu has form sum_s chi_mu(s) P_s bar_mu, where chi_mu(s) is the commutation sign between R_s and the bare logical Pauli bar_mu.

A clean syndrome register coherently records s, reversible computation evaluates chi_X and chi_Z, and controlled bare logical Paulis with controlled sign phases implement controlled Q_X and Q_Z. No syndrome measurement is needed. The syndrome registers may remain throughout the logical SWAP because logical operations preserve each syndrome subspace, and are then fully uncomputed. SWAP(A,L) = CNOT(A,L) CNOT(L,A) CNOT(A,L); CNOT(L,A) is H_A controlled-Q_Z(A) H_A. Thus no measurement/readout is required ideally. After tracing the outgoing A, arbitrary input rho_A replaces L and the original GE marginal is unchanged, even when LGE is correlated and has syndrome coherences. The outgoing A carries the old logical correlations.

A measured-syndrome shortcut is NOT valid for generic interacting Gibbs states: it dephases syndrome coherences. For a commuting Gibbs state this objection disappears, but thermal syndrome sampling still requires a real preparation algorithm.

## Resource ledger
- m syndrome bits plus reversible decoder workspace W_dec must be coherently clean initially. This is O(m+W_dec), not supplied automatically by a finite-temperature bounded-dimensional spin environment.
- Bare stabilizer checks have constant-depth coherent extraction only when check weight, geometric range, overlap degree, and ancillary placement have bounded constants. Enormous code constants must remain explicit.
- Reversible decoder complexity and physical communication must be charged. A polynomial decoder permits a polynomial circuit and local routing with polynomial overhead, not automatically practical depth. A merely mathematically defined minimum-weight decoder need not be efficient.
- Controlled logical Pauli strings require distributing a coherent control or transporting it; bounded-strength local gates impose a propagation cost. Cat-state preparation is a cost, not a free global control.
- Ideal uncomputation avoids readout and reset; fault-tolerant correction during the circuit needs usable low-entropy ancillas and entropy export/reset or a finite supply adequate for the run.
- The actual always-on H0, environmental dynamics, and weak coupling operate during the entire routed circuit. Compiling abstract gates does not suppress them. Cancellation/control of known H0 and control errors must be budgeted; the environment cannot silently be frozen.

## Exact remaining barrier
Ordinary FT can simulate a circuit on PROTECTED inputs, including inputs entangled with references. But the memory is already an extensive unknown interacting mixed physical state, not an FT-encoded input. Encoding every physical input spin into a second FT code entails N noisy boundary interfaces and ultimately an N-spin output interface. A bound O(N eta) in full-state distance is not small at fixed physical noise. Protecting only L does not protect GE. An arbitrary constant-density residual local error on G need not be globally close to the actual Gibbs marginal. Therefore a blanket appeal to threshold theorems is insufficient.

Two sufficient missing results would close the circuit issue:
1. A joint-state implementation bound ||E_phys(rho_A tensor rho_GE_actual)-E_ideal(rho_A tensor rho_GE_actual)||_1 <= delta uniformly over reference-entangled inputs, with a local noisy implementation and explicit resources; or
2. A strengthened storage theorem for the actual noisy loading output class: e.g. an explicitly controlled local-noise thickening of the ideal Gibbs-overwrite ensemble, not just exact Gibbs initialization.

For (1), CPTP contraction means delta adds ONCE to endpoint error. It need not be exponentially small in storage duration. This does not itself give an implementable circuit. A crude Gibbs-density domination bound can scale exponentially in N times residual error density, so is generally useless when the protected barrier is subextensive. A local-noise basin theorem is the more plausible useful extension.

## Same-resource active comparison
The established rigorous baseline is geometrically local concatenated-code FT combined with local Hamiltonian/non-Markovian noise threshold machinery, rather than a nonlocal qLDPC circuit with free classical/global communication. Local bounded spin couplings fit suitable Hamiltonian-noise hypotheses only after checking interaction support, strength times gate duration, gate schedule, and reset assumptions. Bounded environment dimension is not a limitation for these results; weak local coupling is the relevant parameter.

Active FT does not require preparation of the interacting Gibbs state or preservation of an unknown thermal gauge marginal. It does require repeated control and fresh/reset ancillas. If those are allowed to make the passive loader work, they must also be allowed to the active comparator. Conversely, if only a finite closed spin system with no usable resets is permitted, unlimited active threshold operation is not established merely by citing standard theorems. Compare the same ancilla inventory, control norm, local geometry, reset access, wall-clock loading/reading delay, and endpoint error.

An arbitrary single unencoded unknown input has an unavoidable noisy injection boundary: a physical input error before redundancy is established is indistinguishable from a changed input. Thus neither competitor achieves endpoint error tending to zero at fixed uncontrolled input-interface error merely by increasing memory size. Use epsilon_total = epsilon_injection + epsilon_load + epsilon_store + epsilon_read, or supply a protected input and explicitly charge its creation. This is an adversarial-noise observation, not a claim that every physical input has a positive lower bound under all noise channels.

## Primary references checked
- Gottesman, *Fault-Tolerant Quantum Computation with Local Gates*, https://arxiv.org/abs/quant-ph/9903099 : explicit local concatenated constructions, nearest-neighbor in 2D/3D; polylogarithmic overhead. Existence threshold, not optimized constants.
- Terhal and Burkard, *Fault-Tolerant Quantum Computation For Local Non-Markovian Noise*, https://arxiv.org/abs/quant-ph/0402104 : Hamiltonian noise strength measured through gate duration times coupling spectral width.
- Aharonov, Kitaev, Preskill, *Fault-tolerant quantum computation with long-range correlated noise*, https://arxiv.org/abs/quant-ph/0510231 : weak pair interactions with environment, spatial decay faster than inverse distance to power D.
- Aliferis, Gottesman, Preskill, *Quantum accuracy threshold for concatenated distance-3 codes*, https://arxiv.org/abs/quant-ph/0504218 : threshold proof including generalized local non-Markovian analysis. Numerical stochastic threshold is not transferable unchanged to this physical noise model.
- Koenig and Pastawski, *Generating topological order: no speedup by dissipation*, https://arxiv.org/abs/1310.1037 : local preparation/encoding lower bounds, including linear diameter scaling for toric-code examples. Not a universal lower bound for arbitrary finite-temperature logical overwrite from a preexisting thermal state.
- Svore, DiVincenzo, Terhal, *Noise Threshold for a Fault-Tolerant Two-Dimensional Lattice Architecture*, https://arxiv.org/abs/quant-ph/0604090 : explicit noisy SWAP routing and 2D architecture, with model-dependent stochastic constants.

## Access log
Opening https://www.nature.com/articles/srep08975 failed with a non-retryable redirect to idp.nature.com authorization. Did not retry, bypass, or fetch alternate versions after that failure. Search snippets had reported an unknown-input encoding limitation, but the reasoning above is independent and does not rely on inaccessible full text. Other listed arXiv abstract pages were accessible; no external contact or publication occurred.
