# Code-conditioned return experiments: paid preparation removes dilution, not complexity

Root conditional physical/interface construction, 2026-11-01. This note does not claim a laboratory implementation, logical-gate advantage, or independently reviewed multiseed extension.

## Actual scalar experiment

Let P be an actual code projector of rank d_C, and F_i Hermitian logical Pauli operators supported on that code, F_i²=P, with physical operator norm1. Normalize the full physical Hilbert-Schmidt inner product by <A,B>=Tr(A B)/d_C. Then ||F_i||=1 even though the code is a small fraction of the physical Hilbert space.

For a traceless F_i, suppose the experiment can actually prepare the two normalized logical eigensembles rho_±=(P±F_i)/d_C. Choose s=±1 uniformly, prepare rho_s, execute the desired operation, and measure a final logical Pauli F_j, assigning value0 to code-space failure. The signed report s*o lies in[-1,1] and has mean

 E[s o]=Tr[F_j T(F_i)]/d_C.

For F_i=P, simply prepare P/d_C and use s=+1. A report0 may be converted to an unbiased binary report by an independent fair coin; this is paid randomization, not conditioning on successful outcomes.

This avoids the O(d_C/d_physical) dilution of a whole-register infinite-temperature trace by CHANGING AND PAYING preparation. It does not infer code-conditioned performance from the old maxmixed signal. Encoding, ancilla initialization, mixture generation, final code/logical measurement, calibration, discarded attempts and systematic preparation/readout bias remain costs. If these cannot be supplied to the required bias accuracy, this source is not earned.

## Actual adjoints without reversing dissipation

Suppose each selected measurement operation has a CP map T_a(X)=sum_r K_(a,r) X K_(a,r), with every K_(a,r) Hermitian and sum_r K_(a,r)²<=I. Such a map is self-adjoint in the normalized Hilbert-Schmidt inner product and is a contraction there: the standard Schwarz inequality for subunital CP maps gives ||T_a X||_2²<=Tr T_a(X*X)<=Tr X*X. The trace inequality uses the same sum K²<=I. For a single projector or positive weak-measurement branch this is immediate.

A physically implemented selected branch must include its failure probability. On a failed specified outcome the episode returns0, rather than resampling free successes. Reversing the chronological list of these ACTUAL self-adjoint primitives supplies the Hilbert-Schmidt adjoint of a word. This is not an inverse of the noisy channel. Generic coherent errors, uncontrolled Hamiltonians, arbitrary Kraus operators and feedback do not inherit this identity.

Consequently cross-seed Gram entries

 <T_u F_i,T_v F_j>=<F_i,T_u* T_v F_j>

can be acquired by a signed F_j preparation, the actual concatenated return word v followed by u in reverse order, and a final F_i measurement. All preparations and branch failures are charged. The experiment does not need to reveal hidden operator coordinates.

## A conditional complete logical-gate report

For the code-to-code trace-nonincreasing channel E, define R_ji=Tr[F_j E(F_i)]/d_C. For a known target logical Clifford U, write U F_i U*=s_i F_(pi(i)). Then the entanglement fidelity relative to U, INCLUDING loss of code probability, is

 F_e(E,U)=(1/d_C²) sum_i s_i R_(pi(i),i).

This identity uses the complete d_C² logical Pauli basis, including identity. It is not inferred from one scalar autocorrelation. For non-Clifford targets the corresponding known Pauli transfer coefficients must be acquired/computed and their coefficient/sampling costs charged. A high scalar fidelity alone is not an unqualified worst-case logical-error certificate.

## What an acquired predictor would additionally need

The currently audited acquisition theorem starts from one seed and returns its autocorrelation. Applying its nonlinear projection construction to R_ji requires an explicitly extended source contract with all the above cross-seed experiments, initial dictionary containing the paid seeds, and a width promise over their joint reachable family. The Duhamel product argument then uses seed i for the forward model and seed j for the reverse-adjoint model. The initial seed count enters the determinant budget and all source/job counts. This extension is algebraically plausible but is not silently included in the existing same-seed receipt.

The scientific task could be comparing many physically allowed measurement-only logical-gate words. This still does not earn an efficient optimizer over all words, adaptive feedback policies, inexpensive code preparation, high success probability, a low-dimensional joint reachable family, or a practical advantage over retaining logical tomography / predictive-state / direct adaptive-racing methods with the same information and controls.

If the actual jumps are merely Pauli-string dephasing, each Pauli observable is a common eigenoperator and the scalar problem collapses to per-primitive attenuation calibration. If a low-rank model follows from a fully known small operator algebra, ordinary algebraic propagation receives that information too. The remaining potentially substantive case is experimentally available but unknown intermediate leakage/geometry whose useful reusable structure can be acquired economically. No such regime is established by this note.
