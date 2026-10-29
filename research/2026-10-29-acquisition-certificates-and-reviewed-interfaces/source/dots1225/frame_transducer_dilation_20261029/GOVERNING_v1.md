# Explicit known-unitary realization of the frame transducer
2026-10-29. Author construction; receiving review pending. Purpose: remove an implicit arbitrary-Kraus-operation oracle, not claim an efficient hardware implementation.

## Exact dilation
The accepted four-program transducer is K=(4/sqrt3)T, T=J(MM^T)^(-1)M, mapping two nine-dimensional R programs to four four-dimensional quaternion programs. Embed its81 input coordinates into8 physical qubits at indices16a+b, a,b=0,...,8; the256 output coordinates are already8 qubits. Set all invalid input columns to zero. Thus padded K is256x256. The accepted exact polynomial/projector certificate establishes eigenvalues of A=K†K in{0,1/3,2/3,1}. Let P_lambda be its Lagrange spectral projectors, including the padded zero subspace.

Define
 D=P_0+sqrt(2/3)P_(1/3)+sqrt(1/3)P_(2/3),
 E=I+sum_(lambda>0) [(sqrt(1-lambda)-1)/lambda] K P_lambda K†.
Then D²=I-K†K, E²=I-KK†, and EK=KD. Consequently
 U=[[K,E],[D,-K†]]
is a512x512 unitary. A ninth flag qubit initialized0 gives K on flag outcome0 and D on outcome1. This realizes the EXACT accepted success Kraus map, with a legitimate paid failure branch, including entangled references. It uses no unknown-source inverse. All coefficients are explicitly determined real algebraic numbers. The spectral identities, not floating diagonalization, govern correctness.

## Finite elementary compilation bound
QR elimination compiles any known512x512 unitary into at most512*511/2=130816 two-level unitaries plus512 computational-basis phases. A two-level operation on two9-bit strings can be realized with a Gray path: at most8 adjacent basis transpositions, one controlled one-qubit operation, and the inverse path. This is at most17 eight-controlled one-qubit operations. A basis phase needs one such operation. Hence at most G=2224384 eight-controlled one-qubit operations suffice.

Compute the AND of eight positive controls into seven clean work qubits with seven Toffolis, apply a one-controlled U, and uncompute. Negative controls add at most16 single-qubit X gates. A one-controlled U uses two CNOTs and four arbitrary one-qubit gates (the usual A-X-B-X-C decomposition plus a phase on the control). For a self-contained conservative Toffoli bound, choose V²=X: controlled-V(b,c), CNOT(a,b), controlled-V†(b,c), CNOT(a,b), controlled-V(a,c) implements Toffoli, since its target exponent is b-(a xor b)+a. Thus each Toffoli costs at most8 CNOTs and12 arbitrary one-qubit gates by the same controlled-U decomposition.

An eight-controlled gate therefore costs at most114 CNOTs and188 arbitrary one-qubit gates, including negative-control flips. Overall the deliberately loose bounds are114G CNOTs and188G single-qubit gates, with16 qubits total (8 program qubits,1 outcome flag,7 clean AND work qubits). Routing, readout/reset, storage lifetime and fault-tolerance costs are extra. This enormous generic bound is not a claim of practicality. The constants do not grow with target approximation precision, but synthesis precision/cost of the single-qubit gates does.

If each compiled elementary unitary is approximated to operator-norm error at most zeta/L for a circuit of L gates, telescoping bounds the full unitary error by zeta and half-diamond instrument error by at most zeta before conditioning. Conditioning on a rare success can amplify this error and must be charged by the enclosing protocol. No exact finite Clifford+T realization or certified hardware timing is claimed. Standard decomposition background: Barenco et al., *Elementary gates for quantum computation*, arXiv:quant-ph/9503016; the explicit algebra above fixes the conservative counts used here.

## Executed diagnostic
`check_dilation.py` builds the padded K, polynomial spectral projectors, E,D,U, and executes a double-precision QR decomposition. It obtains78822 nontrivial two-level rotations, orthogonality residual1.82e-15 and QR residual1.56e-15. These numbers are a CPU diagnostic, not the exact proof or native circuit execution. Floating skips at1e-16 are not used to lower the governing130816 worst-case bound. The original accepted transducer certificate is unchanged.
