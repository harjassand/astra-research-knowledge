# Astra P2: finite coherent information and actual receiver operations

Research continuation, 29 October 2026 Australia/Brisbane. Preceding `p2_measurement` and `p2_mediator` proofs, executable evidence, actual reviews and failed comparisons are preserved. Independent reviews in this directory identify the accepted files and their dependencies. Internal acceptance is not external peer review or a priority claim.

## Completed scientific advance

The opening was to ask which **bounded source interactions** must remain quantum. A finite source alphabet need not preserve all the continuous generators of its environment. For the projective-unitary families treated here, information divides into a finite matrix factor that must remain coherent, commuting information that can become an actual record, and multiplicity that can be retired.

This has become a finite circuit construction. The binary compiler takes an arrival schedule, transfers its required matrix factors into finite qubits, records the relevant phases with a finite actual instrument, and retires the other quantum systems. It proves a complete corrected-operation guarantee against the **same actual receiver acting on the common input**. The supplied interface consists of controlled access to the actual source-relative unitaries and finite ancillary control/readout. No ideal modular subsystem-extraction oracle is used.

The robustness extension treats actual nearly anticommuting unitaries and controls the disturbance caused by the noncommuting phase-measurement sequence. It gives a finite-error separation from every classical-memory receiver in the stated all-input, phase-feedback class, including irrational Weyl phases sufficiently near anticommutation. Actual Weyl operators are never replaced by supposedly norm-close rational ones.

A further completed construction connects the protected receiver register to the source operation's noise: the same prefix algebra fixes the source phase-error patterns of memory Pauli faults. Under an explicitly supplied state-independent Pauli fault law, their net character gives an exact complete-record error, with finite compiler error added separately. See Section 7.

## 1. Causal algebra and finite compilation

An acquired dilation has ordered branches V_x=product_i V_i^x_i, with V_i=tensor_t U_i,t and binary source labels x. A known diagonal source target G includes the actual cocycle. Suppose batch generators have projective commutation matrices C_t over the prime field F_p. Let B_t=sum_(s<=t) C_s. If B_T=0, the exact theorem gives the simultaneous causal quantum-memory dimension

\[
D_t=p^{\operatorname{rank}_{\mathbb F_p}(B_t)/2}.
\]

The upper construction and lower bound allow arbitrary normal receiver processing, classical adaptation, and arbitrary original source/environment/reference correlations. They permit record-dependent source phase correction and exclude an additional source coupling or an uncounted quantum system crossing the arrival cut. Exact unitary responses force a multiplicative-domain representation through the retained register. This is not a rule for compressing arbitrary nonunitary observables.

For p=2, the finite compiler estimates the commuting squares with actual sine-window phase instruments, reduces their signs by binary symplectic elimination, extracts one qubit per anticommuting pair, measures the remaining commuting binary factors, and retires the old field and memory. Its actual circuit is exactly isometric even though the phase-normalized generators need not be involutions.

If L_t is the number of generator occurrences in the symplectic word basis, w_t the largest admitted source-word weight, and M_t the power-of-two phase resolution, the sufficient complete-instrument bound is

\[
\epsilon_{\rm complete}\leq\min\!\left(1,
\sum_t w_t(2L_t+1)\frac{2\sin[\pi/(2M_t)]}{\sqrt2}\right),
\quad L_t\leq n^2.
\]

It supports every binary rank schedule with B_T=0 in one compatible receiver, retaining rank(B_t)/2 qubits after each cut. Uniformity applies to every pre-cut history, with the current actual phase outcomes still summed. Arbitrary postselection on a bad current phase outcome does not inherit the bound. Phase records subsequently serve only as controls.

`compile_receiver.py` emits the symplectic words, execution order, cocycle and normalization phases, retained Pauli frames, actual record masks, feedback, and a rational error/query ledger. The default four-arrival example has memory schedule 1,2,1,0 qubits. At requested allowance 1/100 the general recipe certifies 495/50176 and counts 1,048,560 controlled field queries and 248 record bits. This is a conservative construction cost, not a physical lower bound. The specialized two-generator circuit gives a much better allowance when applicable.

See [the compiler proof](FINITE_PROJECTIVE_COMPILER.md), [the executable compiler](compile_receiver.py), [the emitted example](COMPILED_EXAMPLE.json), and [the executed evidence](projective_compiler_checks.json). The independent proof review is `reviews/compiler/INDEPENDENT_REVIEW.md`; emitted operational metadata has its own separate review.

## 2. A separation that survives imperfect algebra

For actual U,V with ||UV+VU||<=eta, estimate U^2 and then V^2 in that order. With r_M=2sin(pi/(2M)) and K=M-2, the extracted-qubit defects obey

\[
\delta_U=r_M+(6K+1+1/\sqrt2)\eta,\qquad
\delta_V=r_M/\sqrt2+2K\eta.
\]

The K eta terms include the later phase instrument's disturbance of the earlier estimate. For two arrivals, eta_1,eta_2<=10^-5 and M=128 give

\[
\epsilon_{\rm quantum}<127863/1225000<0.10438.
\]

Every receiver retaining no quantum system across the cut, with arbitrary classical records and later processing under the same phase-feedback/all-input contract, has

\[
\epsilon_{\rm classical}\geq(2-10^{-5})/16>0.124999.
\]

These disjoint upper and lower intervals establish a resource separation in actual complete-instrument performance. The upper is not an attained optimum. Exact anticommutation gives the smaller sufficient bound 2r_M(1+1/sqrt2), approximately 0.0837953 at M=128.

One qubit crosses the arrival cut. The explicit binary schedule uses 1,020 controlled field queries and 30 actual record bits. A separate predicate schedule uses 1,012 queries plus predicate gates/workspace. The field remains available throughout extraction; the source must remain coherent through feedback. Reset of measured registers uses retained records and does not erase entropy for free.

At fixed nonzero eta the sufficient bound scales as 1/M+M eta; M of order eta^(-1/2) gives an O(sqrt eta) allowance. These are construction statements, not physical noise limits. Small physical displacement miscalibration still needs the appropriate moment/control contract.

See [the exact circuit](extractor_circuit/FINITE_QUBIT_EXTRACTOR.md), [the robust extension](robust_extractor/NEAR_ANTICOMMUTING_EXTRACTOR.md), and their actual independent reviews in `reviews/extractor` and `reviews/robust_extractor`.

## 3. Exact operation metrics and source-only reuse

This tranche also replaces several proxy comparisons by operation-level statements. For a controlled branch V_a, actual receiver POVM M(dy), and phase feedback c_a(y), define

\[
T_{ab}=V_b^*\left[\int c_a(y)c_b(y)^*M(dy)\right]V_a.
\]

The source marginal is one fixed Schur channel for every correlated source/environment/reference input exactly when T_ab=D_ab I. Finite **operator** responses suffice; tests on selected input states do not establish that equality. An exact detector-relocation identity supplies a constructive realization without physically coupling the source to the comparison detector.

For the specified Gaussian receiver,

\[
D_{ab}=\exp[-(a-b)^TN(a-b)/2+i a^T\Omega b].
\]

The phase sign is positive in this convention. For a real correlation matrix D, the actual source half-diamond distance from identity is

\[
\epsilon_{\rm source}=1-\min_{p\in\Delta}p^TDp.
\]

This is a finite convex program with exact KKT witnesses in the examples. The two previously compared fixed covariance paths reverse their actual-error ranking as the noise strength changes. This is not a global receiver-path optimization result.

Complete-record error remains a distinct objective. For a fixed known preparation, a positive record Gram measure exactly describes the source and actual record when the discarded bath has no future contact. Rank-one polar recovery is source-diamond optimal over all record-conditional CPTP source recoveries for the fixed rank-one instrument. A simple family has full-record error equal to the square root of its source-only error. The full-record optimality claim is only over the proved diagonal-phase class; no all-CPTP full-record optimum is asserted.

If every call satisfies the all-correlated-input scalar-response identity, arbitrary adaptive source-only gates, measurements, references and public source histories compose exactly as the known channels, while the private bath remains correlated and unreset. This removes a bath-renewal requirement at that boundary. Fresh independent detector supply remains necessary for the stated realization. Raw receiver records, public receiver success flags and returning retired modes require a larger proved interface. Exact counterexamples preserve both record leakage and the failure caused by reusing a detector that was assumed fresh.

See [finite response and composition](FINITE_RESPONSE_AND_REUSABLE_SERVICE.md), [the corrected channel](operation_metric/EXACT_CORRECTED_CHANNEL.md), [the full Gaussian record](operation_metric/GAUSSIAN_RAW_RECORD.md), and [record Gram/recovery](recovery_challenge/RECORD_GRAM_AND_RECOVERY.md).

## 4. Strong comparisons and physical scope

A suitable retained oscillator and final commuting quadrature measurement can be simpler than the finite non-Gaussian extractor. For a known prepared vacuum, local heterodyne plus polar half-gain feedback halves the relevant noise covariance in the worked comparison. Its preparation promise is narrower than the universal unknown-field interface. Neither comparator is weakened to manufacture an advantage.

The new contribution is the bridge from finite source-relative operators to a complete-record causal circuit and an actual operation separation. Symplectic reduction, sine phase states, SWAP extraction, rational rotation algebras, modular subsystems and environment-assisted correction are established ingredients. No priority claim is made for them.

The explicit controlled-displacement Hamiltonian identifies a coherent ancilla/field interface, but it does not acquire it experimentally. The read trapped-ion modular-measurement implementation uses fluorescence whose bright branch disturbs the oscillator, with heralded continuation; it is not evidence for the deterministic repeated readout used here. Source coupling, collection, calibration, source storage, field energy, query time, loss, memory errors and reuse remain essential physical channels and resource costs. A finite retained Hilbert dimension neither bounds field energy nor compresses dumped energy reversibly into a qubit.

If a physical receiver differs from the specified circuit by a valid complete-channel allowance eta_R, comparison with the same physical receiver's common-input baseline generally pays 2 eta_R. Source-interaction and source-feedback errors add separately. This is distinct from the analytic compiler approximation, floating diagnostic residuals, actual physical noise and total workload error. No scalable fault-tolerant computing or device advantage has been established by this package.

## 5. Evidence, corrections and sources

| Component | Actual independent review |
|---|---|
| Finite response and reusable source interface | `reviews/reusable_service/INDEPENDENT_REVIEW.md` |
| Actual Schur error and Gaussian record | `reviews/operation_metric/INDEPENDENT_REVIEW.md` |
| Record Gram and source recovery | `reviews/record_gram/INDEPENDENT_REVIEW.md` |
| Finite algebra and classical-memory converse | `reviews/algebra/INDEPENDENT_REVIEW.md` |
| Explicit finite two-generator circuit | `reviews/extractor/INDEPENDENT_REVIEW.md` |
| Imperfect anticommutation | `reviews/robust_extractor/INDEPENDENT_REVIEW.md` |
| General binary compiler theorem and checks | `reviews/compiler/INDEPENDENT_REVIEW.md` |
| Executable schedule metadata and causal costs | `reviews/schedule_compiler/INDEPENDENT_METADATA_REVIEW.md` |
| Memory-fault character and exact operation error | `reviews/memory_faults/INDEPENDENT_REVIEW.md` |
| Coherent-memory source and complete-record metrics | `reviews/coherent_memory_extension/INDEPENDENT_REVIEW.md` |

Review receipts pin the actual versions. Independent replay and separate algebra/instrument checks are distinguished; an author does not independently validate their own dependency. The compiler author checks 1,199 binary forms, 92 exact source words, and four whole finite-record instrument families. Its reviewer independently checks 1,099 forms, 651 nonreal inverse phases, 96 source-word transfers and a compatible dense-basis rank walk. Floating finite-dimensional diagnostics remain separate from exact rational/cyclotomic identities and from the infinite-dimensional analytic proof.

Two theorem scope clarifications were incorporated before acceptance: G is diagonal in the controlled source basis, and uniformity is per pre-cut history with the current record summed. The phase records are only used as controls after their actual measurement. The executable recipe's separate review found omitted normalization-phase metadata and a need to state controlled old-frame phases explicitly; the corrected recipe includes both. Its earlier incomplete output is preserved under `history/schedule_compiler_initial` as a failed operational interface, not a current circuit.

The current Astra U1004 and U1023 governing sources/corrections, and the finite-algebra ancestry, are saved with their actual read scopes. The accepted quantum-channel undecidability foundations were not reopened. Root's primary reading ledger is `sources/ROOT_PRIMARY_READING.json`; module source ledgers preserve narrower author/reviewer access scopes. Root later read the relevant full Sorella 2610.23264v2 passages after a contributor's retrieval failed. That resolves the local access gap for the algebraic ancestry, without importing its singlet-preparation calculation or physical synthesis.

Close conventional phase-estimation constructions include Babbush 1805.03662 and Najafi–Costa–Berry 2303.12503. Their efficient preparation/streaming methods can improve subroutines; equivalence to this exact zero-edge instrument has not been certified and is not assumed. The root compiler proof records the specific source passages read.

`robust_extractor/GENERAL_P_SCOPED_NOTE.md` is an unreviewed qudit extension note. It is preserved for future work and excluded from the completed claims. Earlier Gaussian comparison failures, corrected parity alternative, visibility-start cost, startup/supply assumptions and model-versus-device distinctions remain intact in the predecessor packages.

## 6. What is now possible

The completed machinery can classify the exact coherent information required by the stated finite interactions, compile a compatible finite receiver for a whole binary arrival schedule, and compare its complete operation against a strong classical-memory class. It can also test when private bath memory disappears from the source-only interface and compute the actual source error for an important corrected-channel family.

The next substantive frontier is to make such interfaces useful under restricted coupling, loss and control cost, or to establish a comparably constructive general theorem for imperfect multigenerator relations. The present sufficient query count is not a reason to refine a cutoff automatically. The choice should be driven by which physical or informational obstruction the operation must remove. No execution continues merely because these files are saved.

## 7. The memory-fault interface: coherence and error propagation share an algebra

At cut t, for a memory Pauli Q define chi_t(Q)_i by Q P_i=(-1)^chi_i P_i Q. For the rank-minimal register,

\[
\operatorname{Im}\chi_t=\operatorname{Im}B_t,
\qquad\chi_t\text{ is injective on memory Pauli labels modulo phase}.
\]

Thus the prefix matrix determines both the required coherent dimension and the possible source phase-error patterns. Small memory does not imply local source noise: the exact example maps one retained-qubit Y fault to a six-source-qubit Z pattern.

For an exogenous classical joint Pauli-fault path f, independent of the initial source/field/reference but allowed arbitrary time correlations, the corrected complete instrument has the exact form

\[
\mathcal I=\sum_f p_f(\operatorname{Ad}_{Z^{\chi(f)}}\otimes\mathcal R_f),
\quad\chi(f)=\bigoplus_t\chi_t(Q_t).
\]

Each R_f is the same actual common-input receiver with that path, including every actual record. The comparison is sum_f p_f(id tensor R_f). Its complete half-diamond error is exactly

\[
1-\Pr[\chi(f)=0].
\]

The upper bound follows pathwise; source |+>^tensor n makes the nonzero characters orthogonal and saturates it even after discarding records. With finite compiler allowance epsilon_c, actual error lies within epsilon_c of this value, clipped to [0,1]. It is the performance of the prescribed correction, not an optimum over additional fault-aware recovery. Acquired syndrome correction can be incorporated through its residual character law.

This is an operational interface to conventional logical-memory protection, subject to that protection supplying the state-independent logical Pauli/syndrome law and its costs. It does not turn a general coherent error into a mixture. The executed counterexample E=(4I-3iZ)/5 gives actual error 3/5 on a stated input, while a false Pauli replacement predicts 9/25. A correlated fault example also shows exact cancellation: actual error 1/4 despite probability 1/2 of at least one nontrivial fault.

The proof is [MEMORY_FAULT_INTERFACE.md](MEMORY_FAULT_INTERFACE.md); [memory_fault_checks.py](memory_fault_checks.py) and its JSON preserve exact rational evidence. It passed independent review at these stated assumptions. The reviewer used a different three-arrival receiver, verifying 512 row-operator identities over all two-cut Pauli paths and direct complete-record correlated-fault calculations. This extension preserves the distinction between a supplied noise law, an approximation allowance, and total physical/workload error.

### The stronger coherent-record challenge, separately constructed and reviewed

The same coherent fault (4I-3iZ)/5 has exact universal source-only error 3/5 and exact universal complete-record error 24/25 under the wide joint-input contract. The source-only value is the norm of the map from joint source/environment input to the source; it does not assert one field-independent source channel.

The complete-record maximum is attained by a source basis state and common field (Phi+ + i Phi-)/sqrt(2). The actual and noisy common-input receiver give the two Phi records probabilities (1/50,49/50) and (49/50,1/50). The source is unchanged. Thus the record alone has distance 24/25. A matching all-input upper bound follows from the relative-unitary spectrum {1,(7+24i)/25,(7-24i)/25}. For the source-only metric, the off-diagonal difference is Tr_E[(exp(-2i theta Q)-I)rho_01]; complete trace-norm duality gives upper sin(theta)=3/5, saturated by the original source-superposition/Q-eigenstate witness.

The [complete-record extension](reviews/memory_faults/COHERENT_RECORD_EXTENSION.md) was authored during independent challenge. The [source-only proof](COHERENT_SOURCE_METRIC.md) was constructed separately by root. Both passed a further independent review with sixteen exact Kraus identities, 256 marginal matrix-unit identities, the complete record probabilities and analytic norm certificates. That review is distinct from the extension author's review of the original memory-fault theorem. No self-review or retroactive upgrade of the original input-specific witness is claimed.

This exact comparison establishes why a coherent memory fault cannot be replaced by its diagonal Pauli mixture without controlling the missing cross terms and actual record. Additional acquired calibration or recovery operations could change the protocol; these metrics are not recovery optima.
