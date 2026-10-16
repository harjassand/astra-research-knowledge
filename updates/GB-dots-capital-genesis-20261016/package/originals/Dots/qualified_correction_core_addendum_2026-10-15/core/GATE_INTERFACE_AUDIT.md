# Independent audit: qualified noisy Clifford cores and gadget grouping

Date: 2026-10-15. Separate extension; not part of the previously frozen finite-pulse packet.

## Verdict

PASS for the revised GATE_INTERFACE_AND_OBSTRUCTION.md under its explicit fixed-noisy-core, exact-wrapper, full-support Pauli-frame, protected-record, fixed-slot, and common-dilation assumptions. These hypotheses qualify the stated quantum gate errors and yield gadget subset strength sum_e a_e². They do not qualify measurement/reset/classical-controller errors, noisy wrappers, arbitrary recompilation, or generic gate-dependent noise inferred from reduced fidelity.

The protected-record qualification was added during this audit and is essential. Finite-dimensional joint bath/dilation scope is certified here; no new unbounded-bath extension is claimed.

## 1. Fixed-core compiler identity

Let the ideal core be Clifford C and let the same physical noisy core be C W for every private frame T. Apply T before it and C T† C† afterward. The physical operation is exactly

(C T† C†)(C W)T=C T† W T.

The ideal operation is C, and the output wrapper is a Pauli because C is Clifford. No independent noise assumption follows from this identity: W must really be the same joint memory-bath operator for every T, or the stronger time-dependent common-Hamiltonian premise must be verified. Shared bath state correlations are allowed; explicit dependence of the physical core Hamiltonian on the selected frame is not.

For a finite-duration ideal path C(t), use local coordinates D(t)=C(t)T. In the transformed generator, the derivative term cancels the ideal drive and leaves

T† [C(t)† V_lab(t) C(t)] T.

The bracket is seed-independent, has the same operator norm, and remains on the same gate memory support. Bath-only evolution is unchanged. Remote operations commute with D(t) only because their memory supports are disjoint from the clean gate's full support. Simultaneous clean gates may share the bath, but their ideal moving frames act on disjoint memory supports. At gate boundaries the output wrapper restores the fixed ideal C.

This is one joint moving-coordinate calculation, not a factorization of the full shared-bath propagator into independent noisy gate channels. Within each gate, move only memory Pauli factors to its endpoint and preserve every bath factor's chronological order.

## 2. Full-Pauli characters and zero-character correctness

The Pauli group modulo phase has one distinct conjugation character for every memory Pauli on the full gate support. Thus a Dyson monomial's character fixes its net memory Pauli P_e, up to phase. Trivial character implies P_e=I on all of that gate's data and ancillas. In physical endpoint coordinates a nontrivial P_e is transported by C_e to another Pauli.

The distinction from stabilizer-only twirling matters: there is no residual nontrivial stabilizer polynomial in the gate's zero character. Zero-character terms can retain arbitrary chronological bath/auxiliary coefficients, but their gate-memory action is exactly the intended ideal gate. Full ancilla coverage is necessary; twirling data alone could leave zero-character ancilla errors that change the extracted syndrome.

Intervening later gates in the same gadget are not crossed when grouping a gate's memory factors. Remote memory operations crossed within its own clean slot are disjoint. Hence the grouping preserves support and bath order under the stated reservation assumptions.

## 3. Protected records are load-bearing

An arbitrary operator on an unqualified bath subsystem may change that subsystem. Consequently a trusted stored syndrome bit cannot simply be placed in the mutable bath and then read by later ideal feedforward. An identity-on-gate-memory error can flip that record, survive entirely in the zero gate character, and cause wrong feedforward.

The revised note correctly separates protected genuine classical registers from the arbitrary bath. They may be written only by the specified ideal measurement/lookup operations. Error terms and bath-only dynamics cannot flip or coherently mix their values. Record-controlled coefficients are block-diagonal in their actual record basis. The records are stable during a controlled gate slot.

Use fixed padded gate slots and fixed enclosing supports, with uniform action bounds over all genuine branches. The same controlled dilation must exist under every coupling deletion/interpolation. This handles branch selection without freezing observed outcomes or pretending that a separately calibrated family of normalized branches proves a joint moment bound. A branch selecting identity still occupies its padded slot; any physical noise in that slot must be included or explicitly absent.

If a controlled endpoint Clifford differs by genuine record, its Pauli transport can be resolved branchwise in the actual record expansion. The zero-character memory action remains ideal, and nonzero branches are charged as whole-gadget faults. No final global Fourier label becomes available to the physical controller.

## 4. All-zero versus failed gadgets

If every qualified gate of a clean completed gadget has trivial character, each quantum gate has its intended memory factor. The exact preparation, ideal measurement, protected lookup, and conditional Pauli operations therefore yield the intended refined syndrome correction on each actual physical record. Bath filters and correlations can remain; the good branch need not be CPTP or a common memory-independent bath channel on arbitrary inputs.

If any qualified gate has nontrivial character, charge the entire gadget's bounded reserved support and time interval. This includes altered data/ancilla states, wrong genuine measurement outcomes, consequent wrong feedforward, and the possibility that the intended correction is effectively missing. There is no proved reduction to one post-correction local error.

For the support proof, expand every such bad gadget's physical operations in local memory Paulis with auxiliary coefficients at their actual times. The existing arbitrary-bad-gadget/skipped-correction certificate must include these operations. Their Fourier-record maps may be trace-decreasing and coherent sums; positivity of a classical Pauli trajectory is unnecessary. A universal common decoder must correct every admitted term.

The ideal target may be the stabilizer-refined correction already audited separately. Its orbit transitions agree with the original sweep although its full-input channel differs on coarse-branch coherences.

## 5. Gadget subset moments

For a fixed exogenous schedule and fixed unselected bad/pending seeds, let E_b be the fixed finite gate-slot set of clean completed gadget b. These sets are disjoint for distinct gadgets. The qualified global character lemma gives the full-input effect bound

effect(chi_e nonzero for every e in S) <= product_(e in S) a_e² I.

Endogenous physical outcomes are summed at the effect level. For B_b={some e in E_b has nonzero character}, the indicator of intersection_(b in J) B_b is bounded by the sum over selecting one e_b in each E_b. Applying the gate bound to each disjoint selection gives

effect(intersection_(b in J) B_b) <= product_(b in J) [sum_(e in E_b) a_e²] I.

There is no independence assumption and no hidden conditional probability estimate. With at most m gates and uniform action a, the gadget parameter is at most m a². The constant-number qualification must include every noisy slot claimed covered by the theorem.

Only fully completed and actually unframed qualified gates are selected. Pending/dirty gadget prefixes remain arbitrary charged operations. The classical module must use the resulting whole-gadget local-stochastic subset moments, full support/duration, and skipped-start/conflict/pending flags; an earlier birth-only or independent-mark theorem cannot be substituted silently.

## 6. Decoder and channel conclusion

For one input-independent support-good predicate, every decoded expansion term has scalar logical action under the fixed decoder. Summing its ordered bath coefficients gives Kraus I_logical tensor B. The good subchannel is therefore Id_logical tensor Lambda_g with Lambda_g CP and trace-nonincreasing.

Once the separate classical probability argument bounds the bad effect uniformly on all joint inputs, the established bath-defect completion yields the 2 epsilon joint-input diamond estimate. Initial bath/reference entanglement is allowed. Normalizing a good or fixed-measurement branch would not justify this step.

## 7. Counterexample and exact checks

The covarying-drive counterexample is correct. If frame g changes the actual core to g C E g† and wrappers undo g, the final logical operation is always C E. The overrotation is entirely zero-character. This violates the required error-conjugation premise, not the global moment estimate; nonzero-character moments are trivially zero. It does not show that the fixed-core compiler fails.

Reran ../checks/core/check_gate_obstructions.py successfully. It checks the covarying-drive failure, coarse/fine channel difference, positive fixed-core Pauli character identity, and mutable-record obstruction.

Added ../checks/core/check_fixed_core_independent.py. It uses a fixed endpoint Hadamard with a nontrivial intermediate ideal path and two noncommuting joint bath-error segments. For all four frames it verifies the exact physical compiler identity. The Fourier coefficients factor as C P tensor B_P, including K_0=C tensor B_0. Exact Kraus completeness and the stated bad-effect upper bound pass. This supplements the general common-dilation proof, rather than establishing its physical premises.

## Final boundaries

Still ideal or separately qualified: wrappers, initialization/reset, detectors and faithful outcome transmission/storage, classical lookup, timing, frame privacy, and the complete branch-independent/padded compiler structure. Strong support isolation and gatewise bath independence of intended controls are retained. No general noisy correction-controller theorem or hardware claim is certified.
