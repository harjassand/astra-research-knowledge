# Independent receiving review: eight-CNOT Bell-label encoder
2026-10-29. Accepted at ideal analytic-control scope. This separate review binds the root derivation and independently executed netlist; the earlier QR review remains unchanged.

## Exact construction
The logical-zero label branch becomes 11 after the initial two X gates. Neither negative-controlled rotation changes it; the two Z phases cancel. The logical-one branch becomes 01 in (a,b) notation, then sqrt(2/3)|00>+|01>/sqrt3, then (|00>+|01>+|10>)/sqrt3, then (|00>-|01>-|10>)/sqrt3. The two CNOTs coherently duplicate computational labels, not arbitrary unknown quantum states. This is an entangling isometry, not forbidden cloning. Pair Bell transforms produce exactly the two specified singlet columns. Linear extension covers entanglement with arbitrary external systems.

The root local pair-ket convention and the program's global q3 q2 q1 q0 convention are consistent for these states: reversing both local pairs changes each antisymmetric Bell vector's sign, which cancels in its tensor square. The direct exact global-matrix check below avoids relying on this observation alone.

For the controlled rotation decomposition, with the control zero between its conjugating X gates, the two target rotations cancel. With control one, the product is X Ry(-theta/2) X Ry(theta/2)=Ry(theta), using X Ry(a) X=Ry(-a). Thus each negative-controlled rotation costs exactly two CNOTs and four one-qubit gates in the emitted construction. Two such gates, two coherent-copy CNOTs and two Bell-transform CNOTs give eight total; the emitted one-qubit count is fourteen. No work ancilla is used.

## Independent exact symbolic check
check_exact.py independently replaces every emitted gate by an exact SymPy radical matrix, using
c1=sqrt((1+1/sqrt3)/2), s1=sqrt((1-1/sqrt3)/2)
for the first half-angle and c2=sqrt(2+sqrt2)/2, s2=sqrt(2-sqrt2)/2 for the second. It multiplies the full chronological 16-by-16 gate sequence and verifies both target columns exactly. Every individual factor is verified exactly unitary, proving the entire product unitary. Gatewise proof avoids relying on a large nested-radical expression being reduced to a particular normal form by a simplifier.

The canonical reset Kraus family is constructed from this exact full inverse. Its K†K sum equals UU†=I, and its full Choi matrix equals the desired E† code term plus the leakage-reset block (I-EE†)^T. This supplies an exact algebraic check beyond the source's floating tests. The floating program matrix differs from the independently computed exact ideal matrix by approximately 8.6e-16 in Frobenius norm; that comparison is a numerical consistency check, not an interval-certified physical bound.

## Decoder and supersession
Apply the inverse circuit, measure the three nonlogical signal registers, retain the logical output if all are zero and otherwise reset it to the declared fixed state; discard the measurement record. This gives D(X)=E†XE+Tr[(I-EE†)X]tau, including its correct reference-memory extension. Plain inverse-and-discard is not interchangeable with this operation. Because the reset-completed channel depends only on E, changing the full unitary completion from the older QR route does not change the canonical channel used by the prior source-memory construction.

The accepted efficient cost is eight CNOTs and fourteen single-qubit gates per direction, four qubits and no fifth work qubit. Encode-plus-inverse costs sixteen CNOTs and twenty-eight singles before measurement/reset and other costs. This supersedes the valid but unoptimized 500-CNOT/1032-single QR implementation as the supplied best cost for this particular target. It does not establish global gate optimality. A supplied local frame adds four single-qubit rotations per direction. Routing, calibration, preparation, measurement/reset, storage, finite gate-set approximation and fault tolerance remain explicit requirements.

Both matching and conventional logical guards may use this encoder. The construction closes the ideal structured-family isometry/interface obligation, not a general unknown-noise promise. QR, controlled rotations, Bell transforms and computational-label CNOT entangling are established quantum circuit machinery; no historical novelty is claimed.

## Bound source versions and evidence
The accompanying receipt hashes ROOT_ANALYTIC_DERIVATION_v1.md, README.md, check_bell_encoder.py, received helper, stored circuit and results. exact_checks.json records the separate symbolic check. The source's 100 entangled-input decoder tests are supporting floating evidence; the exact review relies on the explicit channel identity rather than interpreting those examples as an exhaustive experimental certification.
