# Repeated measured cells: bounded primary-source comparison

Checked 2026-10-15. Scope: the supplied DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md; no data analysis. This is a literature comparison, not an independent proof audit or a novelty certification.

## Bottom line

Repeated error detection giving quadratic short-cell leakage and an inverse-measurement-count total error is established quantum-Zeno error prevention. The closest rigorous ingredients are **Dominy et al.'s finite-M stabilizer-measurement bound** and **AGP's all-selected-location shared-bath fault-amplitude bound**. Neither inspected statement is the proposed actual retained-record effect inequality

    F_C <= (product over c in C of a_c^2) I,
    F_R <= (product over i in R of sum_l a_(i,l)^2) I.

The defensible distinction is the precise conditional composition: protected syndrome-difference records, deletion nullness uniform in other perturbations, crossing clean parents, and a whole-footprint support certificate. The operation, Zeno scaling, and arbitrary-shared-bath amplitude-product technique should all be credited as existing. A bounded search cannot establish that their combination is novel.

## Closest primary results

### 1. AGP: strongest all-subset/shared-bath comparison

Aliferis, Gottesman, Preskill, *Quantum accuracy threshold for concatenated distance-3 codes*, [arXiv quant-ph/0504218v3](https://arxiv.org/pdf/quant-ph/0504218), 21 October 2005, §11.1, pp.47–49, Eqs.(53)–(59).

For r specified coarse-grained locations, the coherent sum E(I_r) of fault paths with faults at every selected location and unrestricted behavior elsewhere obeys ||E(I_r)|| <= (lambda_0 t_0)^r. The bath is shared, persistent, and has arbitrary internal Hamiltonian; simultaneous couplings may have noncommuting bath actions. This is already the crucial uniform selected-location product architecture. Their discussion explicitly separates coherent fault amplitudes from recorded stochastic faults. Measurements also enter their noisy-location model.

**Exact comparison:** the source does not directly identify a protected detection event with E(I_r), nor state the measured-cell squared-effect bound or parent-cell OR factorization. Squaring a generic fault-path bound is unjustified without the event-annihilation argument. Conversely, once that argument is supplied, this looks closely related to an application/refinement of the established fault-path method, rather than a fundamentally new shared-bath suppression principle.

### 2. Dominy et al.: rigorous repeated stabilizer measurement and finite-M rate

Dominy, Paz-Silva, Rezakhani, Lidar, *Analysis of the quantum Zeno effect for quantum control and computation*, [arXiv:1207.5880v2](https://arxiv.org/pdf/1207.5880), 26 March 2013, J. Phys. A 46,075306; Theorem1, Eqs.(11)–(14), and generator protocol Eq.(9). Earlier protocol: [arXiv:1104.5507](https://arxiv.org/abs/1104.5507), PRL108,080501 (2012).

They analyze M equally spaced weak stabilizer-group or generator measurements under a time-dependent system-bath Hamiltonian. The interaction errors are code-detectable; the remaining Hamiltonian commutes with the stabilizer. Theorem1 bounds global reduced-state trace distance, with leading O(1/M) term; Eq.(14) gives the projective-measurement limit. Constants involve aggregate interaction norm, commuting Hamiltonian norm, and group-size factors. Outcomes need not be observed; measurements are instantaneous.

**Exact comparison:** strong primary precedent for both mechanism and finite-M control. The stated theorem does not bound arbitrary selected detector-record effects, retain per-cell local actions, or yield a lattice-uniform local-stochastic parent distribution. Its Hamiltonian-term detectability is weaker than the corollary's whole-footprint centralizer certificate.

### 3. Early error prevention: explicit quadratic detection probability

Erez, Aharonov, Reznik, Vaidman, *Correcting quantum errors with the Zeno effect*, PRA69,062315 (2004); preprint titled *Quantum Error Correction in the Zeno Regime*, [quant-ph/0309162](https://arxiv.org/pdf/quant-ph/0309162), §2 Eqs.(2)–(4),(9), footnote2. Their common-environment Hamiltonian is a sum of single-qubit Pauli couplings with bath operators. A two-ancilla encoding makes first-order noise orthogonal to the favorable ancilla outcome, whose probability is 1−O(epsilon²). The presentation assumes initially factorized system/environment and explicitly acknowledges higher-order errors even after a favorable outcome. §3 also gives two-time disturbance checks.

Earlier: Vaidman, Goldenberg, Wiesner, [*Error prevention scheme with four particles*](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.54.R1745), PRA54,R1745 (1996), already proposes Zeno-based encoded-state protection.

**Exact comparison:** neither inspected result supplies the desired finite-action all-selected-cell CP-effect theorem. In particular, a favorable syndrome alone does not guarantee absence of higher-order logical error.

### 4. Continuous QEC: useful rate and resource comparison

Oreshkov and Brun, [*Continuous quantum error correction for non-Markovian decoherence*](https://arxiv.org/pdf/0705.2342), PRA76,022318 (2007), §IV Eqs.(43)–(47). Their code models use independent baths per qubit; Hamiltonian-driven Zeno behavior yields outside-code weight scaling as inverse correction-rate squared, contrasted with inverse-rate behavior for Markovian noise. The discussion addresses evolving bath states and code-space correlations, but does not prove the requested shared-bath spatial/subset effect bound. Eq.(47) relates correction rate to ancilla coupling strength and interaction time, making the control-resource tradeoff explicit.

## What must remain explicit in the proposed composition

These are checks of the supplied interface, not claims made by the cited papers:

- The observed flag is a change relative to the cell's actual entering syndrome. Shared boundary outcomes are allowed because all retained predicates commute.
- Nullness must hold as an input-operator identity for every setting of the other interpolations. A small averaged one-cell failure probability is insufficient.
- The parent event counts any intermediate change, including paths returning to their original final syndrome. Endpoint syndrome alone would lose those paths.
- The whole accumulated footprint must satisfy Pauli(A_i) intersect Centralizer(G_i) subset phase times S_code. Detectability of each Hamiltonian term separately cannot replace it: products can be undetected logical operators.
- No normalized chronological postselection is needed for the proposed joint-effect proof; do not infer a small conditional hazard given arbitrary rare histories.
- Exact measurements, protected records, exact correction, and full detector/data reservation are assumptions. Total operation duration and conflict geometry can grow with M even though the weak-noise action majorant falls as J² tau_noise²/M.

## Suggested characterization

“A scheduled-memory composition of standard projective Zeno error detection, using a uniform retained-record joint-effect estimate related to shared-bath fault-path bounds.” This accurately describes the current evidence while leaving priority of the exact composition unresolved.
