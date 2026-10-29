# Explicit local-control circuit for a learned qubit-flag receiver

2026-10-29 UTC. Circuit-model construction/check, awaiting independent review. This is conventional Naimark dilation and gate decomposition executed on the NEW certified learned effects, not a new universality theorem, new hardware, or an advantage claim.

## Circuit and certificate

Input: at most4 rational qubit effects E_a>=0 summing exactly to identity, with associated actual Pauli correction labels. Numerical square roots/QR propose an8-dimensional unitary with first two columns formed from stacked sqrt(E_a). The unitary acts on the named accessible flag qubit plus TWO freshly prepared, trusted zero ancillas; it never accesses retained environment memory. Input ancilla00 means initial columns0,1. Output ancilla bits1,2 give outcome a; flag bit0 is discarded and the corresponding data-Pauli correction is applied.

The proposal is decomposed into28 SU(2) two-level rotations and8 basis phases. Each gate is replaced by an EXACT rational unitary, using stereographic rational parametrization of the unit3-sphere or unit circle. The gate identities are checked algebraically. Products are evaluated exactly in Gaussian rationals. The resulting actual effects E'_a are computed from the corresponding two-row blocks of the first two unitary columns, not inferred from QR accuracy. For each a, an integer-square-root bracket bounds ||E'_a-E_a||_F. Thus the complete averaged measure/Pauli-correct channel, on arbitrary data/flag/reference input, has half-diamond error at most

(1/2) sum_a ||E'_a-E_a||_op <= (1/2) sum_a ||E'_a-E_a||_F.

No numerical optimizer or QR status is acceptance evidence. The three sampled pruned receiver examples have exact upper bounds between1.1134e-15 and2.4206e-15 in this rational two-level gate model.

## No arbitrary-POVM or multi-controlled-unitary oracle

`compile_controlled_primitives_v2.py` expands two-level operations along a3-bit Gray path into addressed two-controlled one-qubit gates, treating negative controls explicitly. It verifies the entire compiled unitary equals the rational two-level circuit EXACTLY. Each of the three examples needs68 such controlled primitives.

`compile_local_controls_v3.py` removes the remaining multi-control abstraction. A CC-U is expanded through V^2=U into three controlled-V/Vdag gates and two CNOTs. A controlled one-qubit unitary is expanded using a global phase on the control and the standard A-X-B-X-C factorization with ABC=I. Negative controls use explicit X gates. Single-qubit factors are again rational-unitary approximations; their exact products are compared with the target controlled primitive by a rational Frobenius norm upper bound. Telescoping between exact unitary factors bounds the total additional operator error by the sum of those primitive residual bounds.

Each recorded receiver circuit uses544 CNOTs and1,384 single-qubit gates (1,928 local gates total), on three qubits. These are deliberately straightforward, unoptimized constructions, not a good claim of minimal practical cost. Including all rational local-gate approximation residuals, the three correction-channel half-diamond upper bounds are7.682e-13,8.631e-13,8.599e-13. Files retain every local gate's exact rational matrix, control/target index, correction label, and error bound. No environment reconstruction occurs.

## Remaining physical interfaces and budget

A device must provide a named addressable flag qubit, two trusted resettable ancillas, and calibrated CNOT/single-qubit control on those three qubits. Specifying rational matrix entries is a finite classical gate command, not proof that a device implements it. Let delta_CX and delta_1 bound the actual channel half-diamond error of each named primitive under the relevant memory/history conditions. Ancilla preparation, two-bit readout, data storage during the flag circuit, and selected Pauli corrections require separate error bounds. A safe one-use budget is

nu <= nu_exact_synthesis +544 delta_CX +1384 delta_1 +epsilon_prep +epsilon_readout +epsilon_storage +epsilon_Pauli +epsilon_private_coins.

This expression assumes those are valid worst-case composable bounds on the executed device/instrument, not independent scalar infidelity numbers. Correlated gate noise is not excused by counting gates. Pulse durations, energy, leakage and calibration have NOT been measured; flag/data coherence must survive the whole circuit. Compiler work can occur before the source call because its receiver is predictable from earlier records. Any unavoidable waiting/control noise must be included in the actual instrument or storage budget.

The code tests only the three sampled pruned terminal receiver instances, not a newly executed entire online physical trajectory. Ideal pruning with its private branch discarded preserves the label-output instrument in expectation; gate approximation used on every evaluation round could accumulate occupation error and needs a per-round bound or a direct robust analysis. Existing source records remain their original floating/unpruned simulations. These circuit certificates do NOT turn them into hardware experiments or establish high-fidelity service. A successful per-instance certificate supplies a finite controllable receiver description; generic all-input synthesis/runtime guarantees and a useful end-to-end physical error rate remain open.
