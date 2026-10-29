# Explicit four-spin encoder and canonical reset decoder — 2026-10-29

## What changed

The four-spin singlet encoder is now an explicit one-qubit/CNOT circuit rather than an assumed supplied isometry. This is an ideal-control interface closure, not an optimized circuit, fault-tolerant implementation, new synthesis algorithm or advantage for one guard family. The construction benefits matching and conventional full-logical tests equally.

Run `OPENBLAS_NUM_THREADS=1 python compiler.py` (Python and NumPy). `circuit.npz` contains the chronological gate list, isometry and completed physical unitary; `results.json` records checks and counts. All residuals are floating checks of analytically specified circuit identities, not rigorous directed-rounded error certificates. Hardware error and finite universal-gate-set synthesis remain additional obligations.

## Physical states, bit order and completion

Use computational ket order `q3 q2 q1 q0`. The logical input is q0, with q1,q2,q3 initially zero; q4 is a clean work qubit. Thus input columns 0 and 1 carry the logical qubit. The output columns are

ψ0=(|0101>−|0110>−|1001>+|1010>)/2,

ψ1=(|0011>+|1100>−(|0101>+|0110>+|1001>+|1010>)/2)/√3.

They are orthonormal and annihilated by all three total-spin generators, so span the full four-spin singlet. Pairing for ψ0 is (q3,q2),(q1,q0).

Thin QR eliminates the lower entries of column 0 then column 1 using 2×2 Givens rotations. The matrix `[conj(x),conj(y);−y,x]/sqrt(|x|²+|y|²)` maps `(x,y)` to `(r,0)`. The inverse reversed sequence defines a complete 16×16 unitary U whose first two columns are ψ0,ψ1. There are nine nontrivial two-level gates; no arbitrary orthogonal completion is silently supplied.

Each two-level gate is addressed along a bit-flip Gray path. Adjacent addressed swaps move the first endpoint to the penultimate vertex; the desired final adjacent gate is applied; swaps are undone. This gives 25 addressed three-controlled one-qubit primitives.

For each primitive, open controls are conjugated by X. Compute the AND of two controls into q4 with an exact six-CNOT Toffoli. Apply CC-U controlled on q4 and the third control, then uncompute. For V²=U, CC-U uses controlled V, CNOT, controlled V†, CNOT, controlled V in the conventional order. Each controlled unitary uses two CNOTs, Euler one-qubit rotations and the control phase accounting for det(U). The explicit Toffoli uses H,T,T† and six CNOTs. Thus each addressed primitive costs exactly 20 CNOTs in this unoptimized construction.

## Counts and controls

One encoder: **500 CNOTs and 1032 one-qubit gates**. Inverse decoder: the same, before measurements/reset. One encode/decode pair therefore costs 1000 CNOTs and 2064 one-qubit gates. Peak local circuit footprint: **five qubits**, four signal plus one restored clean work qubit; the work qubit is not sent through the four-spin source port. Sequential reuse is possible after restoration; fully parallel blocks need their own work qubits. Counts assume required two-qubit connectivity and do not include routing, storage, preparation or readout cost.

Learned local-frame rotations can be appended after this encoder and inverses before this decoder, when the learned frame is a tensor product of four supplied one-qubit unitaries. Their acquisition, precision and four additional one-qubit gates per direction must be charged separately. This file does not assume an arbitrary learned 16×16 unitary is free.

## Canonical complete decoder, not just code-subspace inverse

Plain U† followed by discarding q1,q2,q3 is CPTP and recovers the code, but generally differs on leakage from the canonical reset completion used in the earlier source-memory maps. To implement that completion, apply U†; measure q1,q2,q3 in the computational basis. If all zero, retain q0; otherwise reset q0 to |0>. Discard the syndrome record. A reset can be implemented by computational measurement of q0 and conditional X, so no postselection is required. The resulting channel is exactly

D(ρ)=E†ρE+|0><0| Tr[(I−EE†)ρ].

The Kraus operators are E† and |0><2a+l|U† for a=1,...,7 and l=0,1. Their squared sum is I16. This identity also holds with an arbitrary entangled reference or memory: the leakage contribution retains the appropriate partial-trace reference state, not a scalar replacement of the whole joint state. Code inputs entangled with reference are recovered exactly. Decoder readout/reset must itself be trusted or independently error-budgeted.

## Executed checks and limits

The actual 32×32 compiled circuit is applied to all 16 clean-work physical input columns. Its action agrees with U with Frobenius residual 5.03e−14, work restoration residual 7.16e−15, and whole-circuit unitarity residual 1.41e−13. Thirty random full physical inverse-circuit tests and thirty logical/reference coherent recovery tests pass. Twenty arbitrary entangled physical/reference inputs verify the canonical leakage-reset channel; TP residual is below 6e−16. Total-spin annihilation was checked directly.

These tests check more than the two target columns and therefore cover source outputs outside the code before decoding. Mathematical exactness belongs to the ideal QR/Gray-path/control identities; stored floating matrices and tests establish numerical implementation consistency, not laboratory performance. No gate optimality, fault-tolerance threshold or scalable practical advantage is claimed.

## Dependencies and prior art

This is a standalone NumPy program. The three-qubit addressed-control approach in recovered Astra `certified_qubit_projection_20261029/compile_controlled_primitives_v2.py` and `compile_local_controls_v3.py` informed the implementation, but their hard-coded three-qubit programs are not imported or modified.

Standard controlled-unitary decompositions and universal one-qubit/CNOT synthesis: Barenco et al., *Elementary gates for quantum computation*, Phys. Rev. A 52,3457 (1995), https://arxiv.org/abs/quant-ph/9503016 (primary paper inspected). QR/Givens and Gray-path reduction are established machinery, not new algorithms. The governing new content is the explicitly executed four-spin circuit and its complete leakage-reset interface.
