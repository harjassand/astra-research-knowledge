# Audit of the reusable thermal-register process theorem

The theorem in ../reusable_register_opening.md is valid under its explicit Pauli-resolved bath and syndrome-preserving active-control contract. Adaptive stopping and syndrome-conditioned controls do not invalidate its unconditional complete-record bound. The following clarifications make the exact scope transparent.

## 1. A fixed intrinsic-time trajectory is enough

Sample at time zero a complete labeled autonomous syndrome trajectory on intrinsic passive time [0,T]. This means the jump times and labels of the specified Pauli-resolved generator, including any jumps that leave the syndrome unchanged. Initial syndrome law is pi. This trajectory can equivalently be exposed progressively as the campaign runs.

The actual and ideal campaign use the same trajectory. Active instruments preserve the syndrome, and the bath is isolated while they run, so they merely pause its traversal. Their outcomes and chosen holding durations may depend on arbitrary retained records, including syndrome observations and logical measurement results. Every compatible campaign traverses a stopped prefix of this trajectory, of length tau<=T. A bad logical jump during that prefix is therefore contained in the event that the fixed trajectory has a bad jump somewhere in [0,T]. No stationarity at a stopping time, and no bound on a posterior hazard conditional on a rare report, is required.

Stationarity on the fixed intrinsic interval gives

    E_pi N_bad(T) = integral_0^T E_pi b(S_t) dt = T sum_s pi(s)b(s).

Markov's inequality gives the stated first-bad probability bound. This remains true even if the stopping rule would preferentially spend its allowed time on branches with a dangerous observed syndrome: it cannot skip uncharged intrinsic evolution or restart the syndrome.

## 2. Arbitrary logical references and retained records

For each fixed trajectory with no bad logical jump, actual and ideal passive evolution coincide on the entire logical/reference system. A logical Pauli proportional to identity is harmless; the definition of b(s) must use nonidentity **modulo global phase**. Between bad jumps, the no-jump operator is syndrome-scalar by the stated bath contract.

The same instruments then generate the same full quantum state and the same retained classical records on these good trajectories, even for arbitrary logical/reference entanglement and arbitrary adaptive logical instruments. Bad trajectories contribute trace distance at most their probability. This proves the complete-record comparison, not merely a bound on a final logical marginal.

The joint initial state must be block diagonal in syndrome:

    sum_s p(s) |s><s| tensor rho_LR^(s).

The conditional states rho_LR^(s) may be arbitrary, and the sampled syndrome can be retained as a classical report. A coherent purification across distinct syndrome sectors is not covered by this classical trajectory argument merely because its reduced memory syndrome distribution equals pi. This is compatible with P1's classical-syndrome loader and arbitrary references of the unknown logical input.

Coupling p to pi once with the same conditional preparation kernel rho_LR^(s) gives the initialization cost TV(p,pi) once. An equivalent proof applies trace-distance contractivity to the full adaptive experiment as one channel.

## 3. Active errors and timing scope

The sum of uniform diamond-norm implementation errors is legitimate even if an actual faulty instrument changes syndrome or leaks it. First compare the entire faulty campaign to the ideal-instrument campaign by a channel hybrid; later evolution is contractive and the ideal campaign alone needs stationary intrinsic-time analysis. Use a finite indexed call budget or a uniform bound on the accumulated per-call error budget along every branch.

The uniformity is over **classically scheduled** compatible adaptive campaigns. Coherent quantum control of whether or how fast the bath acts would require a new generator/interface theorem. Likewise a general correlated Davies generator whose jump operators coherently combine different Pauli/syndrome changes is not automatically in the present contract. The stated Pauli-resolved Lindblad representation with syndrome-scalar no-jump evolution is sufficient and directly supplies the claimed autonomous process.

If several independent blocks have separate passive clocks and pathwise caps T_i, the same construction gives a union bound sum_i T_i lambda_i, even if operations entangle their logical registers or schedule their clocks adaptively. Product Gibbs starting law supplies independent stationary bath trajectories; independence is stronger than necessary for the marginal union bound.

## 4. Conditioning is not free

The final trace-distance guarantee is unconditional and includes the syndrome reports, acceptance flags and stopping records. It does not imply that every rare record-conditioned branch has the same error bound. If a user postselects an event of ideal probability a, a conditional guarantee can incur a factor of order 1/a. For example, a stationary dangerous syndrome of probability p can have order-one conditional failure when the campaign is run only on that reported branch, while the unconditional failure is still only order p.

## 5. Useful endpoint

The frame-preserving interface genuinely reuses the thermal background. Measuring syndrome, applying its decoder frame, decoding to ports, performing any logical instrument (including swap-in of a fresh unknown input), re-encoding and restoring the same frame returns the same syndrome. The bath-isolated active interval can be costly, and its error budget, ancilla reset, metrology, routing, port protection, refrigeration and total spacetime remain charged. None of these costs needs a new thermal syndrome sample merely because the logical contents changed.

Thus the new conclusion is a reusable ideal-register process with one initial thermal acquisition and a total intrinsic exposure budget. It is stronger than separately composing single-storage theorems while repeatedly charging fresh preparation error, and it remains within the stated physical class.
