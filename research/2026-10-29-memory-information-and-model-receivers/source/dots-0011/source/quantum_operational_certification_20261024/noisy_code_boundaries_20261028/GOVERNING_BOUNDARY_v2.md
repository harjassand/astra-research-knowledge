# Explicit noisy input and output boundaries for the five-qubit pipeline

28 October 2026. Author construction pending independent review. This is an explicit implementation of standard stabilizer encoding and syndrome recovery, not a new quantum code, threshold or generic fault-tolerant input-injection theorem.

## What is removed

Earlier bulk propagation starts with an ideal code isometry and ends with ideal minimum-weight syndrome recovery followed by logical decoding. Here one arbitrary input qubit enters on physical site 0. Four local reset/preparations supply the remaining sites. An explicit finite Clifford circuit encodes it, the previously acquired native inverse and actual clocked flagged controller operate, and an explicit inverse Clifford circuit plus four destructive syndrome measurements and a conditional physical Pauli return a single physical qubit. No ideal logical operation is inserted at either boundary.

Single-qubit external input preparations and output Pauli tests remain trusted for any proposed six-state experiment. The constructed channel itself is defined for arbitrary input including an inaccessible entangled reference; testing it with those six states requires no entangled preparation. A calibrated bound on external tester error must be added to any experimental confidence claim.

## Circuit synthesis and convention

The stabilizers are XZZXI, IXZZX, XIXZZ, ZXIXZ; logical normalizers are XXXXX and ZZZZZ. Canonical |0L> is normalized code projection of |00000>, and |1L>=XXXXX|0L>. The program performs direct Clifford conjugation of the four stabilizers plus logical Z. Previously reduced rows are multiplied out. Local H/S gates turn a selected Pauli row into Z operators, and CX gates eliminate all but its designated pivot. A final single-qubit phase adjustment aligns both canonical code columns. Row multiplication changes the generator basis, not the code.

The returned decoder network, in execution order, is:

H3, H0, CX(2,1), CX(3,1), CX(0,1), H3, H4, CX(3,2), CX(4,2), H4, CX(4,3), CX(0,3), H0, CX(0,4), X0.

The encoder is its reversed adjoint sequence. Each direction has 8 CX, 6 H and 1 X. Its ideal duration is 23 reference units with one-qubit gates taking 1 and CX taking 2. The complete canonical code map is checked in all four input Pauli coordinates, not only |0>.

A bare inverse Clifford and discard would not reproduce the previous ideal recovery. For each of the 16 weight-zero/one representatives E_a, the program derives the unique four-bit syndrome s and single-qubit Pauli P_s such that U_dec E_a Enc = |syndrome s> tensored with P_s on the logical input, up to phase and the tensor order. It then measures the four syndrome qubits and applies P_s on the remaining physical qubit. The 16 syndrome sectors are mutually orthogonal rank-two spaces and exhaust the 32-dimensional physical space. Consequently this measurement/feedback circuit equals the old complete recovery on every physical operator, including entangled reference inputs, in the ideal limit. The lookup is calculated from the actual circuit rather than assuming its syndrome basis equals the original generator labels.

## Complete boundary noise and time model

All additional operations use the same declared dimensionless local control model as the clocked construction:

- Each of four sequential |0> preparations lasts 2, with a Y rotation of angle eta. Input site 0 and already prepared sites dephase throughout; not-yet-prepared sites do not hold information.
- Each H, X or other single-qubit Clifford is followed by an X rotation eta. Each CX is followed by ZZ rotation eta. All five live data qubits dephase throughout each gate interval, including gate supports.
- After inverse decoding, each syndrome readout lasts 4. Every still-live qubit dephases during that interval. A Y basis misalignment eta is applied to the measured qubit before its Z projection, matching the prior readout convention. The qubit is then retired.
- A single common classical feedback interval lasts 1 after all four records are available. The physical output dephases then and during a final 1-unit correction window. Nonidentity lookup corrections have post-Pauli X rotation eta; identity lookup branches still wait for the window. Classical record processing is otherwise trusted.

Total additional boundary time is 8 + 23 + 23 + 16 + 1 + 1 = **72**. There are 30 Clifford gates, four preparations, four syndrome measurements and at most one conditional Pauli correction. This excludes external acquisition preparation/readout time, which must be paid separately. Native-use and bulk EC counts are unchanged. Native phases continue to be the separate effective channel model and exclude background by its declared assumption; no microscopic physical mechanism establishing that exclusion is claimed.

The output is physical site 0 after the actual noisy syndrome process. Tracing other sites is ordinary discard, not a recovery oracle. The full physical state, including leakage out of the code, is carried through every native and EC operation before this terminal circuit.

## Scope and comparison

This addresses an omitted implementation boundary in the finite model. It does not make arbitrary unknown input injection fault tolerant: an early error on the unencoded input is generally a logical error. Likewise final decoder/control errors can be first order. Longer protected bulk evolution cannot erase those endpoint costs. Strong conventional stabilizer implementations can run exactly this circuit, so no algorithmic or hardware advantage over equal-resource conventional coding is claimed. Comparison with a one-carrier channel must charge its elapsed-time contract and declare extra qubits/control resources explicitly.

`boundary_channel_v1.py` is a preserved failed preliminary version: its raw Pauli coordinates were misnormalized, caught by the zero-noise code-entry assertion before any result output. Version 2 fixes the factor of two and adds actual terminal syndrome correction. No result from version 1 is used.

All numerical evaluations use floating arithmetic, not outward-rounded diamond certificates or hardware measurements. Existing learned frames are inherited from the prior acquisition; no fresh calibration claim is made here.
