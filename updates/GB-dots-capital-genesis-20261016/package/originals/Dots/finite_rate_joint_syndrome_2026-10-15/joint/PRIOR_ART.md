# Prior-art check: dephasing-induced joint endpoint subset bounds

Date: 2026-10-15. Bounded primary-source literature check; no Willow data, numerical experiments, model fitting, or author code execution.

## Bottom line

I did not locate a primary theorem stating this exact combination: arbitrary persistent shared quantum bath, independent parity-dephasing generators, single-parity-flipping bounded Hamiltonian terms, and a **product bound on the actual joint endpoint parity-flip probability/effect for every selected subset**, with factors of order J_i² T / γ_i and no bath-dimension, bath-speed, or total-system coupling prefactor. This is a search result, not a novelty determination or validation of the candidate theorem.

The closest antecedents cover different parts:

1. **AGP local non-Markovian noise:** already gives all-specified-location product bounds with unrestricted shared bath, but on coherent fault-path amplitudes, without the claimed dephasing improvement.
2. **Dominy et al. weak-measurement Zeno analysis:** already supplies commuting-stabilizer character grading, generator-resolved attenuation, and Dyson/norm majorization. Its stated performance theorem is global trace distance.
3. **Viola–Knill random decoupling:** already derives bath-independent quadratic-in-coupling error-probability suppression by averaging paired Dyson expansions. Its theorem is global and assumes finite-time independence of controls rather than Poisson telegraph correlations.
4. **Kolesnik telegraph moments:** the candidate's exact hyperbolic scalar factor is a known moment-generating function. That scalar resummation is not new.

Thus the narrow contribution to check is the **local selected-endpoint product comparison**, including retaining locality under noncommuting bath couplings and obtaining an effect bound uniform over initial states in the sector. Neither “Zeno suppression,” “shared bath without independent errors,” “parity grading,” nor the cosh/sinh formula alone supports novelty.

## Exact target used for comparison

The supplied candidate concerns commuting Hermitian involutions Z_i, a specified initial joint sector, arbitrary finite bath/reference, and H(t)=H_0(t)+Σ_i V_i(t), with H_0 commuting with all selected Z_i. Each V_i flips its own selected parity and preserves the others, with norm at most J_i. Independent Markov dephasing has generator Σ_i γ_i(Ad Z_i−I). The proposed actual endpoint event bound is

P(all selected i flip at T) ≤ ∏_i q_i(T),

q_i(T) = {exp(−γ_i T)[cosh(d_i T)+(γ_i/d_i)sinh(d_i T)]−1}/2,

d_i²=γ_i²+4J_i²,

with q_i≤[exp(2J_i²T/γ_i)−1]/2 for γ_i>0.

This report does not verify the proof. The claim is about endpoint parities, not all historical faults, arbitrary physical-error support, or a quantum-memory threshold.

## Closest sources and exact comparisons

### A. Aliferis, Gottesman, Preskill: subset products with unrestricted shared bath

[Quantum accuracy threshold for concatenated distance-3 codes, quant-ph/0504218v3](https://arxiv.org/pdf/quant-ph/0504218), §11.1, Eqs.53–59, pp.47–48.

Their Hamiltonian model has arbitrary bath Hamiltonian and local system–bath terms bounded by λ_0. For any r specified coarse-grained circuit locations, the norm of the sum of all fault paths faulty at those locations, unrestricted elsewhere, obeys ||E(I_r)||≤(λ_0 t_0)^r. The text explicitly permits the same bath to persist and mediate spatial/temporal correlations; unlike the earlier Terhal–Burkard result, no bath-locality assumption is needed. It also discusses noncommuting bath actions.

**Comparison:** this is the nearest established *all-subsets interface*. It bounds amplitudes of expansion-defined faults, not the proposed measured endpoint events. No γ-dependent improvement is established there. One cannot simply square an amplitude bound and call every coherent fault-path event a classical probability. Conversely, the candidate's single-parity-change assumption is structurally narrower than general local circuit noise. Reference: [Terhal–Burkard antecedent](https://arxiv.org/abs/quant-ph/0402104).

### B. Dominy, Paz-Silva, Rezakhani, Lidar: closest proof algebra

[Analysis of the quantum Zeno effect for quantum control and computation, arXiv:1207.5880v2](https://arxiv.org/pdf/1207.5880), J. Phys. A 46,075306 (2013). See Theorem1 Eqs.11–14; Lemmas3–7; Eqs.38–42.

The model has time-dependent system–bath Hamiltonian, stabilizer-commuting ideal dynamics, and detectable interaction terms. It studies repeated nonselective weak measurements of the full stabilizer group or its generators. The operator algebra is graded by stabilizer characters. Lemma7 retains the exact factor ζ^c, where c counts generators anticommuting with an operator. The proof then expands the dynamics in a graded Dyson series and bounds norms. The main theorem controls global reduced-state trace distance with aggregate interaction norm and other global constants; its generator-protocol bound uses a worst-case attenuation substitution.

**Comparison:** strong proof-method prior, including the generator-resolved damping that a local comparison would exploit. The stated theorem does not retain a product over selected final parity flips or remove all dependence on the commuting Hamiltonian norm. Taking a continuous weak-measurement limit alone does not supply the missing joint-event conclusion. Earlier announcement: [Paz-Silva et al., arXiv:1104.5507](https://arxiv.org/abs/1104.5507).

### C. Viola–Knill: quadratic suppression from averaged Dyson pairs

[Random decoupling schemes for quantum dynamical control and error suppression, quant-ph/0511120](https://arxiv.org/pdf/quant-ph/0511120), PRL94,060502 (2005), Theorems1–2 and Appendix Eqs.7–13.

Theorem2 gives worst-case averaged pure-state error probability O(T Δt λ²) for bounded system–environment interaction norm λ. A bath rotating frame removes its internal dynamics. The Appendix expands both propagators, uses random-control averaging to eliminate isolated time insertions, and bounds the remaining integration regions. Time-dependent Hamiltonians are allowed. Controls must be uniform on the relevant group and independent at times separated by more than Δt.

**Comparison:** very close conceptual precedent for bath-independent quadratic probability suppression through randomization and Dyson pairing. It treats a global error probability, not every local endpoint subset. Poisson telegraph processes retain exponentially decaying correlations at all separations, so their assumptions do not directly identify Δt=1/γ. An extension must establish the telegraph moment integrals and local factorization rather than import the theorem unchanged.

### D. Kolesnik: the exact scalar expression is established

[Moment analysis of the telegraph random process](https://www.math.md/en/publications/basm/issues/y2012-n1/11070/), Bul. Acad. Științe Repub. Mold. Mat.,2012,no.1,90–107. [Primary full text](https://www.math.md/files/basm/y2012-n1/y2012-n1-%28pp90-107%29.pdf); [Math-Net record](https://www.mathnet.ru/eng/basm304). §5, Theorem4, Eq.25.

For symmetric integrated telegraph motion with switching rate λ and speed c, the moment-generating function has the exp(−λt)[cosh(t√(λ²+c²s²))+λ/√(λ²+c²s²)sinh(t√(λ²+c²s²))] form. Kolesnik's Eq.25 uses z=s² for its even-moment generating series.

**Comparison (direct substitution):** take λ=γ, c=1, s=2J. The candidate q is one-half of this function minus one. Equivalently q=E[sinh²(JX(T))] for symmetric integrated unit-speed telegraph X. This identifies the positive scalar majorant, not the noncommutative quantum bound that it is supposed to dominate. Search-indexed full text exposed the theorem; direct PDF opening intermittently returned gateway errors.

### E. General strong-damping bounds and randomized-Zeno unification

[Burgarth et al., Generalized Adiabatic Theorem and Strong-Coupling Limits](https://arxiv.org/pdf/1807.02036), Quantum3,152 (2019), Theorem2 Eqs.3.10–3.13 and Corollary1: general finite-dimensional GKLS dynamics approaches its projected Zeno dynamics with O(1/γ) error on compact time intervals, with explicit norm/resolvent bounds. **Comparison:** rigorous and general, but global. Restricting such an estimate to a subset does not turn O(1/γ) into the required O(γ^−|S|) product.

[Hahn, Burgarth, Yuasa, Unification of Random Dynamical Decoupling and the Quantum Zeno Effect](https://arxiv.org/html/2112.04242v3), NJP24,063027 (2022), §2.2 Eq.2.24 and §3: averaging independent group kicks yields a repeated projected evolution; global Zeno convergence bounds give quantitative random-decoupling control. **Comparison:** the stochastic-control/Zeno connection is established, but this paper does not state the candidate local joint-event product.

[Ng, Lidar, Preskill, Combining dynamical decoupling with fault-tolerant quantum computation](https://arxiv.org/abs/0911.3202), PRA84,012305 (2011): derives effective protected-gate noise-strength bounds and threshold consequences under Hamiltonian noise with limited spatial correlations; performance depends on bath dynamics/norm or correlation spectrum. **Comparison:** essential precedent for the intended eventual composition, but not this bath-speed-independent endpoint statement.

## What remains to establish before any novelty or threshold claim

- Prove the actual sector-compressed Heisenberg effect inequality P_initial E_T*(P_selected-flipped) P_initial ≤ (∏q_i) P_initial, or show rigorously that a probability bound uniform over all bath/reference states yields it.
- Preserve the selected-index requirement in every expansion term. An operator-character label of a density matrix is not itself a population-sector label.
- Explicitly separate independence of engineered dephasing clocks from independence of physical errors; the latter is not assumed or implied.
- Explain why arbitrary selected-parity-preserving dynamics can be absorbed without worsening the bound, including other interactions and unselected dephasing. A term flipping two selected parities violates the proposed single-label structure.
- Establish whatever temporal conditioning/composition a memory application requires. A single-interval initial-sector endpoint result is not automatically a spacetime fault-support model; undetected logical motion can commute with all selected checks.
- Compare novelty at the intersection of A–D, especially whether retaining the grading in B and applying the paired-expansion technique in C is a direct existing corollary. This bounded search cannot resolve that intellectual-priority question.

Search scope: targeted queries around local/non-Markovian fault products, weak-measurement stabilizer Zeno bounds, random dynamical decoupling, strong-damping bounds, and the explicit telegraph moment formula. No exact matching theorem found among the primary results inspected.
