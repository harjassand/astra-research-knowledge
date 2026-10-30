# Independent scoped audit: covariant continuous noise and finite dephasing

2026-10-29 UTC. Source bytes are pinned in `SOURCE_SHA256.txt`, and copies of both lead files and the cited spacetime theorem are retained here. Original files were not edited.

## Verdict and exact scope

No mathematical failure found in the covariant continuous-noise extension or the stated finite-rate disagreement damping/local-source resolvent estimates, under their explicit locality, distance, norm, covariance, and well-defined-dynamics assumptions. The memory conclusion remains conditional on D0/D1 of the cited ideal atomic SSF theorem. This audit does not certify those deterministic contracts afresh, an actual noisy transactional compiler, generic off-charge Hamiltonian/dissipative noise, or an all-orders excursion expansion.

A precision caveat is recorded below: the autonomous resolvent identity must not be read as an instantaneous-generator inverse identity for a time-dependent base. Its propagator estimates do extend as stated.

## 1. Fixed-charge jump factorization, including degenerate codes

Expand a joint data/bath operator supported on data set Z in the finite data-Pauli basis, with arbitrary bath-operator coefficients. Stabilizer conjugation multiplies each data Pauli by its syndrome character. A character eigenoperator therefore contains only Paulis with that character.

For K_Z,a choose any nonzero Pauli component E_Z,a. For every other component P, E_Z,a† P has zero syndrome and remains supported on Z; the support is at most s, not 2s. Since s<d, it cannot be a nontrivial logical Pauli. It is a stabilizer up to phase. This handles code degeneracy correctly: low-weight stabilizers are allowed, and do not invalidate the factorization. Consequently E†K is a sum of stabilizers with bath coefficients. On each full syndrome sector it is identity on the logical factor times a bath operator. The selected E remains supported on Z, so counting its support by s is legitimate.

This factorization is algebraic, not a Pauli twirl or measurement. Syndrome-dependent signs and scalar phases are absorbed into bath coefficients. It remains valid with a common retained bath and arbitrary correlations accumulated during preceding events.

## 2. Zero-charge no-jump action

K_Z,a†K_Z,a has zero character and support Z. The same is true of R_Z after summing a, and of the declared h_Z,0. Every Pauli coefficient is therefore a stabilizer up to phase by s<d. On EVERY syndrome sector, not only codespace, these terms act trivially on the logical factor. Sums, time ordering, and unrestricted bath-only evolution preserve that property. The non-Hermitian no-count propagator need not be trace preserving and need not have small norm or short duration; its syndrome-controlled bath action is nevertheless logically benign.

Starting from the specified encoded input and factored bath, a fixed physical charge-jump/atomic-feedback record can be represented by a serial Pauli error path with bath coefficients. No uncounted Pauli error support is generated during no-jump periods. The required statement would fail for a generic zero-syndrome LOGICAL term of support at least d, or for a nonzero-charge Hamiltonian; neither is permitted here.

## 3. State-dependent count moments and independent hub schedules

The jump intensity bound uses the JOINT operator inequality R_Z≤epsilon_Z I, not a reduced-data bound. Tilting a positive quantum trajectory instrument by x^{N}, x≥1, adds (x-1) times the selected jump gains. The ordinary Lindbladian has zero trace derivative; the added contribution is at most (x-1) sum_Z epsilon_Z times the tilted trace. Gronwall supplies the claimed positive exponential count moment uniformly over input, reference, and retained bath.

Conditioning on a complete independent exogenous ideal hub clock schedule fixes intervention times only. At those times the complete ideal intervention, including summation over measurement outcomes, is CPTP and preserves the tilted trace. The same scalar differential estimate applies between them. It is important not to condition on an outcome/syndrome record here; the text does not do so. A state-dependent jump process is not identified with independent Poisson event times.

For each fixed certificate W and window label, the no-ring majorant is a function of this clock schedule. Multiplying the uniform conditional count bound by its nonnegative moment and averaging gives the same joint bound as the cited spacetime argument. This is exactly the joint interface its terminal-density union bound needs. Bounded incidence translates sum epsilon_Z into the fixed-volume count budget. No union over separate quantum residual distributions is introduced.

## 4. Transfer to D0/D1 and quantum output

Given D0/D1, every charge-jump history has local Pauli bad-event support bounded by the declared primitive support. The same first-bad-block and connected spacetime certificate argument therefore applies. The geometric bad event depends on actual jump support/time and ideal hub-clock records, not a normalized quantum branch. Uniform count tails bound its CP subinstrument effect even though jump occurrence probabilities can depend on the joint state.

On a good geometric record, all compatible Pauli histories are restored by the same final decoder. Their syndrome/bath coefficients are logical-identity, so the decoded good CP map is a scalar a times id_L for the specified fixed initial bath. The scalar is independent of logical input. The bad subinstrument is CP with norm at most p_bad; trace preservation gives its complementary trace. Thus the displayed 2p_bad decoded diamond bound follows. This uses the common-decoder correctable-span property and the initial factorization assumption; a mere marginal Pauli failure probability would not suffice.

## 5. Redundant-check Fourier projectors and exact damping

The relevant Fourier group is the actual finite stabilizer conjugation group. Redundant generator labels restrict the admissible disagreement vectors; they do not create independent sectors. On an admissible character delta, the Fourier sum has coefficients of absolute value 1/|G|, so its diamond norm is at most one by the triangle inequality for unitary channels. P_0 is CP syndrome dephasing; nonzero P_delta need not be positive, and the proof correctly does not require positivity.

Atomic feedback Kraus operators F_a Pi_a are character eigenoperators. Their CP maps, including recorded versions, commute with stabilizer conjugation. The engineered generator sums the ACTUAL check conjugations, so its eigenvalue on sector delta is -2 kappa times the number of actual checks with delta_j=1, including redundant checks that were physically included. Commutation and CPTP diamond contraction then give the exact sector damping bound, without SSF mixing, uniqueness of a stationary state, or a logical gap.

A small independent exact-algebra test with three checks ZZI, IZZ, ZIZ=S1S2 checked 256 matrix-unit/projector comparisons. Fourier projectors agree with syndrome-block projectors, inadmissible sectors are empty, and damping counts three actual checks rather than independent rank two. PASS; this is only a redundancy-algebra regression.

## 6. Uniform local-source resolvent

A superoperator supported on s data qubits can be expanded with left and right data Paulis and bath superoperators. Acting on P_0, its charge is the character of the product of those Paulis. There are at most 4^s possible products, including identity; hence at most 4^s-1 nonzero charges. This avoids a global count of syndrome sectors. Each projected source has diamond norm at most ||V_Z||, and each nonzero charge decays at least e^{-2 kappa t}. Integration gives (4^s-1)||V_Z||/(2 kappa), uniformly in system size.

For the autonomous base, differentiation under the convergent local-source integral gives L_base R_off V_ZP_0=-Q V_ZP_0. This is an actual source-restricted inverse, not a bound on an arbitrary extensive source or a claim that the full response remains spatially local. The document correctly reserves spatial quasi-locality for an additional argument.

**Time-dependent precision:** A covariant time-dependent CPTP base still preserves charges, factors the scalar dephasing attenuation, and satisfies the same propagator and integrated-response norm bounds. One must not identify that causal response with an inverse of an instantaneous generator: L_base(t) R=-Q does not generally follow when L_base varies with time. The text's explicit extension of displayed bounds (1)–(2) is sound under the propagator reading. The autonomous inverse identity remains autonomous.

## 7. Diagonal resummation and remaining off-charge problem

Character projection keeps data support Z. Summing K_a†K_a gives exactly the stabilizer twirl of K†K, so its joint norm is at most ||K||²; no 4^s jump-rate penalty is needed. The character-diagonal dissipator plus zero-charge Hamiltonian is a genuine covariant Lindbladian and has the same P_0-to-P_0 action as the original local noise. It is therefore an allowed covariant base for both the damping estimates and the continuous covariant-noise theorem.

Cross-character dissipator terms and nonzero-charge Hamiltonians change the disagreement sector, so P_delta V_off P_delta=0. The second-order return kernel has the stated damping/integral bound. Disjoint check neighborhoods cannot create and remove the same nonzero character, so their second-order return vanishes. These facts do NOT bound all returning charge walks, establish a convergent linked-cluster expansion, or justify replacing a signed finite-memory kernel by a positive epsilon²/kappa jump rate. No such unsupported acceptance is made.

## Preserved limitations and blockers

No tool or permission block occurred. No source failure was repaired or hidden. This audit accepts only the explicitly covariant continuous-noise extension of the ideal atomic conditional theorem and the finite-rate local-source estimates. D0/D1, physical controller covariance during partial gates, engineered-dephasing implementation errors, spatial quasi-locality, and the all-orders off-charge problem retain their separate proof obligations.
