# Independent review: physical flagged five-qubit storage gadget

28 October 2026. **PASS at the explicit single-gadget and one-cycle decoded scope.** Governing argument: `flagged_five_qubit_storage_round_20261028.md`; binding receipt identifies exact versions. Reviewed primary Chao–Reichardt arXiv:1705.02329v1 §II/Fig.2 via https://arxiv.org/html/1705.02329v1#S2. This is an instantiation of their known construction, not a new fault-tolerant code or method.

## Independent reconstruction

The reviewer wrote `flagged_five_qubit_independent_check_20261028.py` without importing author routines. It uses seven-tuples of local Pauli labels, a separately constructed stabilizer group, independently generated gate schedules and projective Clifford propagation. It independently constructs flag correction tables and compares every recorded branch/output with the author's machine-readable evidence, modulo stabilizers. Checks completed:

- 16 identity/weight-one input cases with no gadget fault: exact correction.
- 1,024 arbitrary Pauli input cases with no fault: agreement with the ideal full-syndrome weight-one recovery's logical action.
- 1,528 clean-input single-Pauli-fault cases: all outputs in the common weight-one-correctable space, and all 1,528 adaptive records agree.
- Four flag tables of eight entries, with no same-syndrome inequivalent code-action collision.
- Resource recount: 106 locations per flagged check, 73 per unflagged check; correction weight at most three; conservative longest-branch bounds 737 locations and 111 serial slots.

The initial communicated count 1,312 was superseded by explicit ancilla-idle accounting. The bound/review here applies to the current 1,528-case, 424-clean-path-location model. All 15 two-qubit post-CX Pauli faults, all post-H/preparation single-qubit faults, separate measurement/readout flips and every unused-qubit serial idle are included. Native |+> preparation/X measurement and trusted classical control are explicit assumptions. Extra gates to compile those native operations would require additional locations.

## Physical program and adaptive reachability

The inspected version executes conditional single-qubit Pauli corrections, rather than leaving an unapplied classical Pauli frame. This matters before subsequent initially unknown non-Pauli noise. Correction gates and their idle locations are fault-injectable in the author program. They, and unflagged rescan operations, are not reached on the ideal clean-input trajectory; reaching them already consumes the unique fault. Excluding a first fault there from the clean-input single-fault list is therefore correct. This does not assert robustness to an existing input error plus a new gadget fault.

For a fault-free weight-one input, the fresh unflagged pass and physical correction are reached and independently checked. The first two flag tables agree modulo stabilizer with the paper's explicit choices; the other two are independently checked for the specified ascending-support order. Conditional branching terminates after at most four flagged checks, four fresh unflagged checks, and at most three single-qubit corrections. Flag precedence and the fresh complete pass are material.

## Coherent errors, spectators and records

Projective Pauli propagation suffices for the load-bearing span assertion, not because errors are stochastic Paulis. Every residual branch maps the code into span{E C: weight(E)<=1}, with one common ideal recovery. Distinct weight-one representatives have different syndromes. Same-syndrome representatives differ only by code stabilizers, hence by a scalar on the code, not a logical operation. Thus all pairwise Knill–Laflamme products are scalar. Expanding an arbitrary admitted local faulty Kraus operator gives a linear combination in this same common correctable space; phases change coefficients, not membership.

After the common ideal recovery, every branch Kraus operator is a scalar times logical identity. Consequently arbitrary untouched reference/spectator correlations are preserved, and the joint record/error environment has no dependence on the logical input within this specified local-CPTP model. This conclusion does not silently include an initially correlated uncontrolled bath, leakage or nonlocal faults. The actual gadget output may retain a correctable syndrome; the common ideal recovery is a proof/decoded metric interface, not an uncharged physical reset. Measurement/readout fault reduction is valid here because a sole fault first occurring at a terminal measurement sees a clean encoded trajectory; general controller corruption is not included.

## First-order one-cycle cancellation

The governing one-cycle corollary is valid under its local interleaving premise: every isolated receiver/native fault reaches this gadget on at most one data qubit. A sole gadget fault on ideal encoded input is removed by the final ideal decoder; a sole receiver fault is removed by the fault-free gadget. Therefore every singleton actual-minus-ideal term vanishes in the decoded logical channel. Submultiplicativity and the triangle inequality bound the higher-order expansion by product_i(1+epsilon_i)-1-sum_i epsilon_i, with epsilon_i the full diamond differences. Half-diamond budgets require the stated factor two.

The adaptive circuit must be represented as the declared bounded controlled/padded local-instrument circuit: per-slot bounds are uniform over its reachable classical branches and idle alternatives, with trusted controller registers not arbitrarily corrupted. The 737-location count is a maximum serial-branch budget, not a claim that unrelated branch operations all occur simultaneously. No bound for shared-memory noise follows from reduced marginal bounds alone. These are prerequisites to applying the perturbative formula, not observed hardware properties.

## Negative control and limits

An independent outside-premise counterexample starts with input error XIIII and inserts X on data qubit 1 during the first preparation's idle. The gadget returns residual XXIZI, a nontrivial logical error after its chosen recovery. This is two events, not a failure of the proved one-event conditions. It concretely blocks promotion to simultaneous input-error-plus-fault correction or a naive independent decoded-round product.

Accepted: the specified standard gadget's one-event correction conditions, arbitrary-local-Kraus span extension under the model, and conditional one-cycle first-order cancellation with ideal final decoding. Not accepted or established: a repeated-storage/exRec theorem, global threshold, hardware achievement, fault-tolerant unknown-state injection, unqualified controller robustness, arbitrary bath-memory protection, or new-code novelty. The earlier undecomposed native-parity enumeration is separate evidence; this receipt binds the explicit H/CX/H physical implementation only.
