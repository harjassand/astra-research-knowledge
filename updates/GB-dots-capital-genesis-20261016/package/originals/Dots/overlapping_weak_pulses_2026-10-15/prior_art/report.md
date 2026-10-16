# Continuous shared-bath noise: prior-art comparison

Research date: 2026-10-15. Primary papers inspected directly via arXiv full-text PDF/HTML. This report distinguishes published threshold results from recent preprints and from deductions specific to the present project. No theorem below is claimed to prove the current asynchronous local-memory theorem.

## Bottom line

There are two genuine alternatives to an atomic error premise, but neither is a black-box proof of the desired completion-time conditional bound:

1. Prove a **coherent fault-path norm bound** for the physical continuous Hamiltonian and redo the fault-tolerance combinatorics in amplitude norm.
2. Implement **whole-interval independent conjugations** with a compatible global time partition, or a genuinely continuous pointwise-covariant control scheme, and use the particular global error statement that scheme proves.

The shared bath itself is not an obstruction to Hamiltonian threshold theorems. The missing implication is from continuous interleaved interactions to causal, local, completion-time CP error instruments with uniformly small conditional bad weights.

## 1. Aliferis–Gottesman–Preskill (AGP)

Primary: [Quantum accuracy threshold for concatenated distance-3 codes](https://arxiv.org/pdf/quant-ph/0504218), particularly §11.1, pp. 47–48, Eqs. (53)–(59), and Theorem 6 / Eq. (76), pp. 52–53.

Their Hamiltonian is H_S + H_B + sum_a H_SB,a. Each term's system support is the qubits of an ideal circuit location during that time step; H_B is arbitrary. Time-resolved fault expansions give ||E(I_r)|| ≤ η^r, η = λ_0 t_0, for the **sum** of all paths faulty on a specified r-location set, with other locations unrestricted. Theorem 6 requires fault-tolerant gadgets satisfying exRec-Cor and η below a constant. Eq. (76) bounds output distribution error linearly in the norm of the bad amplitude. The text explicitly distinguishes amplitude η from stochastic probability η². Their overlapping exRecs are combinatorial gadgets in a circuit; this does not identify arbitrarily interleaving physical operations with completion-time stochastic atoms. Fresh ancillas or reset capability remain necessary.

### Import assessment (our deduction)

This is the most defensible starting point for a different proof architecture. One must exhibit the relevant time-resolved locations for each realized schedule, establish their noise support and norm bounds uniformly in the schedule, then prove the local correction mechanism's fault-path combinatorics. An existing probability proof cannot be retained merely by replacing its bad-event parameter with η². The labels in the coherent expansion are not classical observations with a filtration.

## 2. Aharonov–Kitaev–Preskill (AKP)

Primary: [Fault-tolerant quantum computation with long-range correlated noise](https://arxiv.org/pdf/quant-ph/0510231), Eqs. (4)–(9), (16)–(24), pp. 1–4.

The noise may include always-on H_ij acting on arbitrary pairs of system qubits and the bath. The sufficient parameter is η = t_0 max_i sum_j ||H_ij||, uniformly in time. Pair contractions account for one Hamiltonian insertion damaging two simultaneous locations. Their local amplitude strength is ε = exp(1+1/(2e)) sqrt(2η) for gates of at most two qubits, Eq. (24). Algebraic spatial decay faster than r^{-D} makes the per-site sum converge in D dimensions. No restriction on H_B is required. The analysis permits constructive interference of bad paths.

### Import assessment (our deduction)

A common bath need not be geometrically local. Conversely, a bound on each of many direct pair couplings is insufficient without summability. The square-root degradation is a warning against counting each affected location as an independently small event. Nothing in this result establishes an event-by-event conditional bad-character bound for overlapping local windows.

## 3. Preskill's many-body generalization

Primary: [Sufficient condition on noise correlations for scalable quantum computing](https://arxiv.org/pdf/1207.6131), §2, Theorem 1, Eqs. (4)–(7); conclusions §4.

For k-body H_SB terms with arbitrary bath action, Theorem 1 bounds effective fault-path strength in terms of suitably summable norm weights and sufficiently rapid decay in k. Gates act on at most m qubits, and t_0 bounds location duration. Theorem 1's hypothesis is tilde-η_1^(k) ≤ f_k α^k, and conclusion ε ≤ 2mα exp(sum_k g_k/(2k!)), with g_k defined in Eq. (7). The argument sums perturbation theory to all orders. Bath dynamics are unrestricted; initialization and entropy removal are explicit physical requirements.

This supplies a language for higher-support error terms, not a classicalization theorem.

## 4. Discrete randomized compiling

Primary: Wallman–Emerson, [Noise tailoring for scalable quantum computation via randomized compiling](https://arxiv.org/pdf/1512.01098), Theorems 1–2 and discussion p. 7.

Theorem 1 yields stochastic Pauli noise with independent twirls per round and gate-independent easy-gate noise. Hard-gate errors may be gate-dependent. Theorem 2 controls a deviation for gate-dependent easy-gate errors. The paper explicitly leaves long-memory non-Markovian robustness open. Its cycles and easy/hard gate partition are substantive implementation assumptions, not merely notation.

Primary: Winick et al., [Concepts and conditions for error suppression through randomized compiling](https://arxiv.org/pdf/2212.07500), §III.B–C, Theorem 3, Eqs. (2)–(5).

This subsequent paper introduces a persistent ancillary environment. Theorem 3 extends Pauli tailoring when easy-gate errors are gate-independent. Its term “local stochastic Pauli” refers to a subsystem Pauli-noise description with environment-dependent coefficients; the displayed theorem does not state a spatial subset domination parameter. Section III.C gives adversarial non-Markovian failures when gate-dependent errors leak the twirl to the environment. Thus independence of the current randomizer from the effective joint noise is indispensable.

### Import assessment (our deduction)

For correlated system–bath inputs, the safe object is the full joint CP instrument, not a formula that applies scalar environment-dependent probabilities to an unchanged reduced system state. In general bath-selective Kraus operators steer a correlated system. For example, a Bell-diagonal classical correlation can be measured on the bath to change the conditional system state even if the system Kraus factor is identity. This does not invalidate Pauli-history representations with appropriate initialization and joint evolution; it invalidates casually discarding the joint state during their use.

## 5. Directly relevant continuous-process RC preprint

Primary: He Wang, [Continuous-Process Randomized Compilation for Quantum Process Tensors](https://arxiv.org/html/2610.01521v1), posted October 1, 2026; inspected actual full text, including Proposition 3, Theorem 1, and Appendix J. This is a recent preprint, not an independently verified threshold theorem.

Proposition 3 assumes factorized, frame-independent initialization, independent conjugation of each **whole interval**, and operation slots only at interval boundaries. Eq. (22) gives positive joint history weights with persistent bath memory. Appendix J.2 conditions on Poisson refresh schedules; arbitrary prescribed cuts are not independent slots. Theorem 1 instead bounds full adaptive-record TV by min{1,4∫dt∫ds g(t)g(s)b(s,t)}, requiring autonomous control independent of records, centered bounded coupling, mixing, and pointwise-covariant instruments. There is no bath reset or local completion-order conditional-small-error theorem. Finite-duration endpoint compensation alone is explicitly insufficient. For exact character diagonalization, the required partition is sequential whole intervals, not independently crossing local operation windows.

## 6. Autonomous and asynchronous correction

Primary: Shtanko et al., [Bounds on Autonomous Quantum Error Correction](https://arxiv.org/pdf/2308.16233), published Quantum 9, 1804 (2025); §1, Theorems 1–4.

The model begins with Markovian Lindblad noise, Eq. (2). Theorem 1 assumes recovery properties in Eqs. (6), (8), (9), including strict error reduction, and bounds logical error using correction strength and an error-generator norm. Global-decoder and Poisson-noise specializations are separate assumptions. These do not supply a persistent-bath finite-gate reduction.

Primary: Dünnweber–Styliaris–Trivedi, [Quantum Memory and Autonomous Computation in Two Dimensions](https://arxiv.org/html/2601.20818v3), September 25, 2026 revision. Version distinction matters: v1 asserted a continuous-time mapping using local CPTP Poisson updates and local unitary noise jumps. The current v3 establishes the discrete QCA result rigorously, while presenting the continuous-time implementation as an outline whose proof is deferred. Consequently the older v1 assertion must not be imported as a currently established continuous-time threshold. Neither version supplies the persistent shared-bath, overlapping finite-duration reduction required here.

Primary: Drechsler–Oreg–Aharonov, [Autonomous Quantum Memories from Classical Stochastic Processes](https://arxiv.org/html/2610.05589v1), October 2026 preprint, §§1.5–1.6 and formal results thereafter.

The asynchronous correspondence concerns syndrome-based Lindbladians and continuous-time classical Markov processes. Its 4D Toom applications prove memory under local Pauli noise for synchronous and Floquet constructions. The Floquet lift uses global reset/read/execute phases; a fully time-independent lift remains open in that work. It does not cover continuous non-Markovian Hamiltonian noise during overlapping finite gates.

Primary: Midha–Abanin, [Local autonomous inference machines for quantum LDPC codes](https://arxiv.org/html/2609.38139v1), September 2026 preprint, main theorem and supplementary Theorem 9.

Its rigorous repetition-code result is a discrete inference machine with p_th = 1/2 and mean clearing time O(log d), based on initial noise and a BP mapping. Continuous inference thresholds for broader codes are studied numerically. This is not a finite-duration shared-bath threshold result.

## 7. Exact logical distinctions needed in the present theorem (our deductions)

### Conditional domination is strictly stronger than subset domination

Let two bad labels satisfy Pr(B_1=B_2=1)=q², Pr(B_1=B_2=0)=1-q². Then every specified subset S obeys Pr(all S bad)≤q^{|S|} for 0≤q≤1, but Pr(B_2=1 | B_1=1)=1. Therefore even a correct local-stochastic subset theorem cannot simply be cited for the stronger chronological conditional statement. An amplitude bound is further removed: it is not automatically a probability measure at all.

### What the atomic premise buys

An atomic joint CP instrument with a bad subinstrument satisfying B_bad^*(I)≤qI immediately gives conditional bad probability≤q for every incoming normalized joint state, including a bath carrying the entire past. Its product composition supplies an honest filtration. The missing operation in crossing-window dynamics is precisely such a causal composition by local completion events. A final Fourier/character decomposition over all controls can be positive without being causally composable in completion order.

### A possible replacement route, not an established result

A revised theorem could aim only at weighted subset bounds, connected-cluster bounds, or coherent norm bounds. The decoder proof must then be checked for whether it ever conditions on previously revealed labels. If it needs only a union bound over specified witness sets, subset domination may suffice. If the proof adaptively reveals history and applies a one-step hazard bound, it needs redesign.

For overlapping Poisson-start windows, a cluster route would have to quantify the distribution of overlap components, the support growth of interaction-picture errors, and the fault weight of a whole component. Simply coloring windows after the fact is not enough: interacting components can retain bath memory, and Poisson schedules have no deterministic bound on overlap count. A valid theorem could use probabilistic cluster tails rather than a uniform overlap cap, but that is additional mathematics.

## Recommended citation-safe conclusion

“Continuous Hamiltonian fault-tolerance theorems already tolerate a persistent shared bath under local or summably nonlocal bounded couplings. Their quantitative hypothesis is a norm bound on coherent sums of fault paths. Existing randomized-compiling and autonomous-memory results considered here do not identify arbitrary overlapping finite-duration correction windows with completion-time CP instruments having uniformly small conditional character probabilities. Consequently the atomic premise cannot be removed by a direct citation; one must change the implementation assumptions or establish a different fault-path/cluster bound and adapt the decoder proof.”

## 8. Follow-up: private-coordinate Hamiltonian subset lemma

The following replacement lemma is a project derivation, not attributed to a paper:

H_g(t)=H_0(t)+sum_i V_{i,g_i}(t), with independent private frame coordinates g_i, real-coupling unitary interpolations, and a_i=∫sup_g ||V_{i,g}(t)||dt. Let Q_i=I−E_{g_i} in frame L². Deleting selected couplings gives a multivariate anchored finite-difference formula. Because every boundary with z_i=0 is independent of g_i, Q_S removes those boundaries. Mixed Duhamel derivatives have norm at most product_i a_i: order permutations partition the integration cube and all interspersed real-z propagators are unitary. Applying the commuting L² contractions Q_i and Parseval to U_g|ψ⟩ then bounds the total Fourier-Kraus weight whose selected coordinates are all nontrivial by product_i a_i², uniformly in |ψ⟩.

A targeted literature search did not locate this exact statement for overlapping privately randomized pulse windows. This is not evidence of novelty. Its ingredients are conventional perturbative marked-insertion estimates and Fourier orthogonality. State and prove it explicitly rather than attributing the combined claim to AGP or discrete RC.

### Required qualifications

- **Deletion stability:** At z_i=0, every remaining part of the dilation must be independent of g_i. This includes H_0, other couplings, instruments, the initial state, the schedule, ancilla preparation, and terminal readout. Frame-covariant implementation may establish this after a suitable representation change; it is not automatic in laboratory coordinates.
- **Noise-state independence of sampling:** The private coordinates must be sampled independently of the incoming state and of the other noise/controller variables retained in the conditioning. An exogenous schedule can be conditioned on, but conditioning on future measurement information can change the sampling law.
- **The labels are Fourier coordinates:** Positive Fourier-Kraus weights form a valid decomposition of the random-unitary averaged channel, but a nontrivial coordinate need not already be a correctable local completion-time Pauli error. The remaining proof must establish a syndrome/support or witness-set bridge for these global Kraus branches.
- **No conditional consequence:** The bound is for specified subsets under the original ensemble. It does not imply a small bad-label probability after arbitrary previous-label postselection.
- **Locality costs remain:** The analytic norm estimate need not require geometric locality; the decoder theorem certainly needs a relation between a coordinate's Hamiltonian support and how its faults propagate.
- **Boundedness/regularity:** The finite-dimensional bounded-Hamiltonian version is straightforward. Unbounded bath generators require a well-defined common propagator and an interaction-picture bounded perturbation argument, not a formal Dyson expansion alone.

The rare-condition crossing-window examples are compatible with this candidate lemma: subset smallness can coexist with conditional probability close to one.
