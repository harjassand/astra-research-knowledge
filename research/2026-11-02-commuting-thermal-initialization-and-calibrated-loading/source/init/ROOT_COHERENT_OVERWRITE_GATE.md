# Root construction: coherent decoded overwrite and the physical loading gate

1 November 2026. Conditional circuit construction, not a physical loading theorem.

## Target and fixed interface
The delivered thermal-memory theorem starts from the actual joint interacting Gibbs state rho_MB and overwrites a decoded memory logical qubit. Generic bath and memory interactions mean that measuring stabilizer syndrome can change this state. A syndrome-measure-and-correct procedure cannot simply be substituted.

Let stabilizer sectors be P_s, and choose a fixed Pauli decoder R_s. For each bare logical Pauli L_mu, the decoded full-space logical Pauli has the form
Q_mu = L_mu sum_s f_mu(s) P_s, where f_mu(s) in {+1,-1}.
The f_mu are the commutation signs between R_s and L_mu. The Q_mu form an exact qubit Pauli algebra, even outside the good sector, because they are conjugates under the fixed decoder isomorphism.

## Coherent circuit existence
With clean temporary ancillas, extract stabilizer eigenvalues COHERENTLY:
U_syn: |psi_s>|0> -> |psi_s>|s>.
Compute f_mu(s) reversibly, implement its phase controlled by an external control bit, apply controlled bare L_mu, then uncompute f and all syndrome workspace. Bare logical Paulis commute with stabilizers, so the uncomputation returns workspace to zero. The induced memory operation is exactly controlled Q_mu on every superposition of syndrome sectors, and acts as identity on the environment. It therefore does not dephase a generic interacting Gibbs state.

Controlled Q_X and controlled Q_Z, together with physical operations on a supplied qubit, generate a SWAP between that qubit and the DECODED logical subsystem. In the decoder frame this is SWAP_input,L tensor I_GB. Discarding the old logical output leaves rho_input tensor Tr_L(rho_MB), including for inputs entangled with an external reference. This exactly realizes the ideal overwrite channel while retaining the actual bath-gauge marginal. No microscopic knowledge of V is used.

This is a finite circuit existence statement. It does not grant efficient coherent decoding, geometrically local depth, fault tolerance on an unknown thermal gauge state, zero waiting exposure, or clean ancillas at zero physical cost.

## Error accounting: do not multiply preparation error by storage time
Let the ideal loaded state map E and implemented map E_tilde differ in reference-safe trace norm by delta uniformly over logical input, including the actual bath background. Any common storage channel and final decoder contract this difference. Hence endpoint error <= delta + ideal_storage_bound + decoder_implementation_error. An initial background approximation in full joint trace norm eta contributes at most eta after ideal overwrite and subsequent channels. Fixed target endpoint accuracy does NOT demand an exponentially small preparation trace distance merely because storage duration is exponential.

However, global trace closeness is much stronger than local-observable convergence. An extensive bath cannot be replaced by finitely many locally accurate marginals without a separate locality/response argument. Fault tolerance of the logical input alone does not establish closeness of the post-loading thermal gauge-bath state.

## Decisive open gate
Implement the coherent logical SWAP at finite physical noise while preserving a thermally admissible gauge-bath background, OR prove a weaker post-loading admissibility condition sufficient for long storage. Every clean ancilla/reset, entropy export, control strength, gate duration and waiting interaction must be charged.

The storage model by itself does not provide reset or thermalization. In particular V=0 with a zero bath Hamiltonian is allowed; unitary dynamics alone cannot universally create an actual Gibbs state from arbitrary initial states. Adding a thermalization/reset service changes the operational resource model and must be supplied equally to the active baseline.

A raw unknown unencoded input additionally has a physical injection error floor under faults before redundancy is created. Compare the same input interface, or use an already protected input. No size-scaling endpoint theorem may silently erase this floor.
