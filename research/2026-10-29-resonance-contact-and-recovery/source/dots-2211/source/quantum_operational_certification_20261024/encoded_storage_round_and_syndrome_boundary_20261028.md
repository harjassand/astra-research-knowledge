# Encoded storage is a cleaner next interface than a free fault-tolerant input encoder

28 October 2026. Candidate operational consequence and explicit implementation boundary. This does not receive a fault-tolerant syndrome gadget or a completed processor.

## 1. Return to the known code space, without reinjecting the unknown payload

With the five-qubit encoder isometry C and standard decoder Kraus R_a=Cdagger F_a dagger, define encoded-recovery Kraus

    Q_a=C R_a=P_C F_a dagger.

They satisfy sum_a Q_a dagger Q_a=I and output the fixed code space. They are the ordinary operation 'measure the four stabilizers, apply the syndrome Pauli correction', rather than an instruction to decode an unknown qubit and reencode it physically after every cycle.

The learned-frame/QEC theorem immediately gives the same reference-complete error bound for Q composed native noise on a KNOWN encoded input: postcomposing its logical-output comparison by the isometry C preserves the diamond norm. Encoded storage can therefore be the workload. The initial unknown-qubit injection/encoding error and final decoding/readout error remain one-off debits, not magically quadratic quantities.

For T rounds using the same frozen learned frame, the record-retaining route supplies a per-good-record channel guarantee, not merely a one-use averaged-program identity. Under an actual round-by-round native product/local-CPTP contract and the required stable frame/support promises, an ordinary hybrid gives at most the sum of the logical round bounds, plus one calibration-failure probability, initial/final debits, and the sum of actual syndrome/control/storage implementation allowances. Ideal encoded recovery returns each reference trajectory to the code space, which licenses the next logical round. Arbitrary coherent bath correlations or hardware memory that violate the per-round contract are not covered.

This finite-round statement does NOT inherit the faster retired-independent-program one-cycle rate merely by reusing its program. That averaging needs its separate reuse analysis.

## 2. A single unflagged syndrome fault can remain first order

For the first stabilizer g0=X0 Z1 Z2 X3, consider the standard ancilla-|+> controlled-Pauli measurement: controlled-X0, controlled-Z1, controlled-Z2, controlled-X3, then ancilla X readout. An ancilla X fault immediately after the first two controlled gates propagates through the remaining controlled gates as

    X_ancilla tensor Z2 X3.

The ancilla X readout does not reveal this X fault. On a clean code input the induced data error is IIZXI, which commutes with g0. Perfect later measurements of the other three stabilizers give syndrome(0,1,0,0). The standard minimum-weight correction is IIIIZ. Their product is a nontrivial logical X, up to a stabilizer and global phase.

Thus one physical ancilla fault with probability h can cause logical error of order h in this unflagged measurement circuit. The native-channel quadratic theorem is not a proof that a real syndrome circuit is fault tolerant. A flag/verified-ancilla or other explicit fault-tolerant gadget, with its own control assumptions and acquisition costs, is a genuine next obligation.

The accompanying exact Pauli/syndrome check preserves this rejected shortcut. It does not claim all syndrome implementations fail or that standard fault-tolerant gadgets are unavailable.

## 3. What remains physically meaningful

One-off O(p) input injection and final decoding do not negate a protected storage rate O(p²) per cycle when comparing sufficiently long storage intervals, provided the actual syndrome/control error budget supports that rate. Conversely a per-cycle O(p) unflagged syndrome fault can dominate it. Reporting should separate initial quality, recurring memory error, and final readout; compressing all three into a nominal quadratic code claim would conceal the decisive physical operation.

## Primary-source identification

After constructing the hook check, the actual primary paper Chao–Reichardt, Quantum error correction with only two extra qubits, arXiv:1705.02329v1, SectionII and Figure2(b)–(d), was inspected: https://arxiv.org/pdf/1705.02329 . It already gives the SAME IIZXI hook and resulting IIZXZ logical-X failure, and supplies a two-ancilla flagged correction procedure. Thus this boundary is a reproduced standard failure, not a new Astra discovery. The relevant next step is to instantiate and check that known flag circuit and its adaptive recovery/measurement/reset interface in the acquired-frame architecture. Merely citing its existence is not a completed implementation here.
