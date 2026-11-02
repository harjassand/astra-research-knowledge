# Usable passive quantum memory: independent interface direction

Date: 2026-11-02. This direction was derived before consulting the parent's preferred files. The supplied storage theorem is treated as an earned premise, not independently re-proved here.

## Result first

The most useful next theorem is **noisy quotient-equilibrium loading plus an entanglement-preserving physical interface**. Full Gibbs mixing is unnecessarily strong; merely preparing the code ground state is generally insufficient. The precise intermediate target is the joint syndrome–environment state after erasing the decoded logical subsystem. The ideal overwrite already erases that logical subsystem, so logical-sector mixing can be omitted exactly.

This is a reduction and research program, not a demonstrated usable memory. Its unresolved gate is constructive preparation with actual environmental correlations and a physically realizable decoder/overwrite channel under fixed noise.

## Mechanism

Let S be the memory and E its actual finite local-spin environment. Let Ω_SE be the Gibbs state of the actual same Hamiltonian used in the storage theorem. Suppose the theorem's ideal overwrite uses a reversible subsystem identification D:S→L⊗A (or a specified reversible extension). Define

    Q(σ_SE) = Tr_L[(D⊗I_E) σ_SE (D†⊗I_E)].

Given an external logical input ρ_LR, with arbitrary inaccessible reference R, its ideal write is

    W_ρ(σ_SE) = (D†⊗I_ER)[ρ_LR ⊗ Q(σ_SE)](D⊗I_ER).

The logical subsystem previously held by S is swapped into a disposable ancilla, not measured in a way that destroys A–E correlations. Therefore

    ½||W_ρ(σ)-W_ρ(Ω)||₁ = ½||Q(σ)-Q(Ω)||₁ = δ_Q.

An isometry gives equality; general physical postprocessing gives the sufficient inequality. This formula requires that the supplied ideal overwrite really has this subsystem form. If not, use its actual overwrite channel to define the corresponding preparation equivalence relation instead of assuming one.

Under the same storage channel, contractivity gives the service bound

    ε_service(t) ≤ δ_Q + ε_write + ε_store(t) + ε_read,

where endpoint errors are reference-preserving channel errors, and ε_store is whatever reference-sensitive guarantee the storage theorem actually supplies. If the theorem supplies only unreferenced state fidelity, the conversion to an entanglement-preserving channel guarantee must be established explicitly (for a fixed number of logical qubits, dimension factors can be kept explicit).

No term δ_Q exp(t) is introduced. A one-time initialization error need not be exponentially small in the storage duration.

## Physical architecture

1. A noisy local loader prepares σ_SE whose Q-distance or a weaker theorem-proven admissible-basin error is bounded. It may equilibrate syndrome variables within logical sectors, without needing to mix logical sectors.
2. A temporary fault-tolerant access station implements D, a logical swap/teleportation, and D†, or a more direct equivalent write map. Fault-tolerant components are allowed, but their resets, time, ancillas, noise assumptions, and geometry are counted.
3. All control turns off for storage under the actual fixed Hamiltonian. Any change made to enable access must end in the theorem's storage Hamiltonian, with switch-induced error budgeted.
4. A noisy fault-tolerant extraction station delivers an encoded logical qubit to a conventional processor or an appropriate logical measurement. Quantum READ is not merely a classical bit readout.

A compiler correct only on a clean code subspace does not suffice for a thermal input. Its map must preserve the required syndrome–environment correlations, or the loading proof must put the state inside the compiler's certified domain. Nor can a standard threshold theorem be invoked without checking its assumptions on residual always-on interactions, initial correlations, reset quality and locality.

## Decisive tests

A. Exhibit the ideal overwrite's subsystem or channel structure and prove the above quotient reduction.
B. Construct a local noisy loader with explicit size dependence, success probability, entropy export, environmental access assumptions, and δ_Q. Full global trace-distance Gibbs preparation is sufficient but not necessary.
C. If direct δ_Q control is too strong, prove a preparation-basin extension of the storage theorem in an operational norm that directly bounds failure. Local-observable matching alone is not enough for a global logical guarantee.
D. Compile WRITE and READ with reference-sensitive error and physical costs. A teleportation label alone does not furnish a thermal logical Bell-pair resource or physical logical measurements.
E. Compute the end-to-end feasible region and compare its Pareto frontier with active fault-tolerant storage using the same resource assumptions.

## Strongest resource-matched alternative

An optimized active FT memory, including concatenated, topological or other suitable architectures, may also use the candidate Hamiltonian as a physical device and may use passive bias between correction rounds. Give both architectures the same physical noise floor, local dimensions, connectivity, coupling/drive strength, reset and measurement quality, cooling/entropy service, footprint, and available parallelism. Optimize code, correction schedule, and interfaces for each. FT is both a legitimate interface component and a serious competitor; comparing against uncorrected qubits is not informative.

Resource output should be a vector rather than a favorable scalar: total physical systems/volume, end-to-end latency, retained logical qubits, reference-sensitive error, reset count/entropy exported, control duty cycle, cooling power and integrated energy. Count initialization and final extraction. The environment, shielding and control apparatus cannot be declared free for one architecture and charged to the other.

For a fixed target service error η, a candidate must exhibit n, loader time τ_load, access time τ_access, and storage horizon T with δ_Q+ε_write+ε_store(T)+ε_read≤η. Its practical opportunity is long idle duty cycles where startup/access costs amortize, provided static cooling and isolation do not dominate. A nominal inequality E_load+E_access+P_passive T < E_active,start+P_active T is only a bookkeeping crossover after each term is derived for optimized, equally reliable implementations; it is not evidence on its own.

## Important limits

- Fast mixing within a logical sector is a conjectured mechanism, not a consequence of a slow logical transition rate. Kinetic trapping may exist within sectors.
- A system-only preparation generally cannot manufacture arbitrary required bath correlations. The loader must either access an adequate physical bath process or use a robustness theorem accepting the actual correlations it creates.
- The physical environment may be finite in the theorem, whereas a laboratory refrigerator is an additional system. Include its coupling during loading and remove or account for it during storage.
- Reliable repeated service does not follow from the single-use bound. A cycle can change the syndrome/environment state. Reuse requires reloading or a proved invariant admissible basin/renewal guarantee.
- A stretched-exponential lifetime with extreme constants can fail to intersect the resource-feasible region at any useful size.

## Stronger question if the loader fails

Which correlated low-energy preparation basin can be reached in polynomial physical time under fixed local noise and finite-rate entropy export, and does the same-Hamiltonian storage bound hold uniformly on it? A successful basin theorem plus one local preparation algorithm would compound into reliable quantum capability more directly than further improving a lifetime theorem with inaccessible initialization.
