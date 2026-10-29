# Exact two-body-qudit quantum-recovery cell with a certified noisy reset tail
Date: 2026-10-29. This is a finite correction module, not a scalable fault-tolerant architecture.

## Concrete channel, not a Kraus oracle
Use the [[5,1,3]] code with stabilizer generators
XZZXI, IXZZX, XIXZZ, ZXIXZ.
Five external data qubits surround one hub. The hub contains four syndrome bits and a 30-position clock, hence dimension 16×30=480. It can be placed in a bounded-size 2D patch with five finite-range hub–leaf couplings. No interaction connects two leaves or three physical sites.

The gate sequence is explicit:
1. For each of four generators, apply H to its hub syndrome bit, four hub-controlled single-data Pauli gates for its nonidentity entries, then H to that syndrome bit (24 gates total).
2. For each of five data qubits, apply a Pauli chosen by the four hub syndrome bits: the unique single-qubit Pauli with that nonzero syndrome, or identity (five further gates).

These are hub-only or hub+one-data-qubit gates. The finite family is H, controlled-X, controlled-Z, and syndrome-conditioned single-qubit Pauli. No arbitrary many-body update oracle is used. The syndrome-conditioned gate is an explicit operation within the finite hub and one leaf, not an elementary two-qubit gate after binary hub encoding.

For t=0,...,28, let U_t be the corresponding unitary on data+syndrome and set

H=Σ_t g [U_t⊗|t+1><t| + U_t†⊗|t><t+1|].

Clock and syndromes are in the same physical hub, so each summand is at most two-body in the qudit convention. Its norm is g; all rates and dimensions are fixed independently of device size and runtime.

The only intended dissipative jumps are hub-local,

L_s=√κ |clock0, syndrome0000><clock29, syndrome s|, s=0,...,15.

No externally timed gates or reset triggers occur. Starting hub-ready, the first terminal emission applies exactly the usual recovery Kraus map, and the hub is exactly ready again. Finite g,κ changes only the random waiting time, not that emitted recovery map.

## Exact history argument and full-space regeneration
Let G_t=U_{t−1}...U_0, with G_0=I. The unitary gauge Σ_t G_t⊗|t><t| transforms the full propagation Hamiltonian to I_(data+syndrome)⊗g A_path. Summing L_s†L_s gives κ I_syndrome⊗|29><29|, also gauge-invariant.

Consequently the entire no-terminal-emission evolution, even from an arbitrary corrupted, reference-entangled hub/data state, is unitarily equivalent to the scalar path no-jump operator

A=−ig A_path−(κ/2)|29><29|.

Every eigenvalue of A has negative real part. Indeed a zero-real-part eigenvector would have zero terminal component from the dissipation identity; the path recurrence then forces all components to vanish. Thus the hub eventually emits and resets from every initial state, with exponential waiting tail. The data channel generated from a dirty hub may be erroneous, but all data damage is confined to this fixed five-qubit module; the hub memory is erased at the terminal jump.

## Exact rational finite-parameter certificate
At g=κ=1 and path dimension30, define P as the positive solution of
A†P+PA=−I.
It equals ∫_0^∞ e^{A†t}e^{At}dt, so Tr(Pρ_clock) is the mean first-terminal-emission time. `path_clock_certificate.py` reconstructs rational P=Q/4 and verifies the equation EXACTLY using SymPy integer matrices (B=2A, B†Q+QB=−8I). The certificate is included as JSON.

TrP=24335/4,
<0|P|0>=149/4.

For every initial state, mean reset time≤||P||≤TrP. Thus for
T=2 TrP=24335/2,
P(reset occurs by T)≥1/2.
The bound is conservative; numerical ||P||≈1858.72 gives better, but not relied-on, constants.

## Imperfect reset / additional local noise
Let N be an additional trace-preserving local Markov generator on this fixed module, including thermal upward jumps and local coherent Hamiltonian errors, with ||N||_diamond≤δ. The clean and noisy 'no designated terminal reset' evolutions are CP trace-nonincreasing subchannels. Duhamel and contraction give their diamond distance at time T at most δT, for arbitrary inputs and retained reference systems. Therefore, when

δ≤1/(4T)=1/48670,

there is a designated reset by T with probability at least1/4, uniformly in the incoming dirty state. Repeating conditional intervals yields

P(no designated reset in mT)≤(3/4)^m.

This is a runtime/volume-independent LOCAL regeneration guarantee. The perturbation bound is for the fixed module, not a global generator norm over N modules. Under overall frequency scale Ω, multiply g,κ,δ by Ω and divide T by Ω. Bounded local system–bath Hamiltonian perturbations can be handled by the same joint-space Duhamel estimate when their norm budget is uniform; no bath reset is assumed.

For thermal reverse jumps L_s† with upward rate κ_up, their generator norm budget is at most 2×16κ_up. Other spurious hub transitions and data noise must be included too. The small numerical bound is not presented as an experimentally competitive threshold.

## Verification
`five_qubit_recovery_test.py` explicitly constructs all 29 gates and all sixteen Kraus operators. It checks trace preservation and the error-correction identities for I and X,Y,Z on each of the five data qubits. Maximum residuals: history isometry5.1e−15, TP9.5e−15, recovery7.4e−16. Exact structure, rather than floating-point numbers, supplies the proof.

`two_body_correction_cell.py` supplies a smaller bit-flip-only example: three data qubits, two syndrome bits, eight clock positions, 32-level hub, seven gates. Its full 256-dimensional H/jump intertwining checks give zero residuals.

## Boundaries of the result
A fault in the central hub may corrupt all five data qubits. Therefore this recovery circuit is not internally fault-tolerant and does not by itself preserve a logical qubit indefinitely. It must be treated as one bounded-support noisy gadget inside a genuinely fault-tolerant larger architecture. Overlapping modules cannot run freely on shared data; the two-site lease construction addresses two-site primitives, but robust scheduling of a whole multiqubit recovery cell remains an additional composition step. No spectral approximation/global O(Nt) error has been used here; equally, no global data-fault threshold has been proved.

The 480-level hub is finite but demanding hardware. Compiling it into elementary qubits while keeping only two-qubit interactions is NOT provided. One-body engineered reset requires a powered/non-equilibrium entropy sink, finite-temperature reverse noise, and cooling throughput; it is not an equilibrium free-energy miracle.
