# Independent audit of root's entanglement-breaking amplification

## Receipt
The amplification argument closes the gap between a polynomially small attack probability and a fixed-error lifetime counterexample, **subject to the explicit single-logical-qubit / Pauli-trajectory scope and isolation conditions below**. The earlier rare-branch construction by itself does not establish a constant-error lifetime bound.

## 1. Exact gate model on all workspace branches
Every completed primitive must be a permutation of classical syndrome/bath labels, accompanied by a logical Pauli, not merely an arbitrary K-conserving unitary. This property holds for the proposed controlled Pauli case swaps, diagonal-energy predicates, bath exchanges, and SWAP routing.

For an off-diagonal Hermitian involution S supported on a local pair of equal-K subspaces, let Q=S² be its support projector. Then h=Q−S commutes with K and exp[−i(π/2)h]=(I−Q)+S. Thus it implements the exact swap, with no relative i phase. Q is a local diagonal syndrome/bath projector. Norm ≤2 is bounded. This avoids reliance on simultaneous sums of overlapping cases; apply each admitted case gate sequentially. On a valid unary input the cases are disjoint. Outside that sector their sequential composition remains a permutation/Pauli trajectory, even when correctness fails.

An input block |sigma><sigma|⊗rho_logical, with diagonal initial bath labels, therefore becomes a mixture of states with classical sigma and bath labels and Pauli-conjugated rho_logical. The output classical trajectory depends only on the input classical labels, never on the logical state. The statement includes bad battery/scratch branches. No syndrome coherence is generated at completed primitive boundaries. Intermediate pulse superpositions cause no problem because no overlapping unaccounted operation is applied then.

## 2. Uniform good-branch approximation
Condition on the designated initial clean unary/scratch branch. Its probability p_n depends only on the fresh attempt bath/workspace, independent of memory and reference. Fresh reservoir groups are independent at first use. Uniform refill mixing bounds boundary failure by delta_n for every initial syndrome and every conditional prior successful trajectory.

Because successful path histories implement the same complete logical Pauli and return to the original syndrome, tracing out the attempt bath gives exactly Ad_X on those histories. Failed histories have total probability ≤delta_n. Thus the reference-safe trace-norm channel error is ≤2delta_n on the syndrome-diagonal class (there is no need to replace it by sqrt(delta_n)). This uses classical failure histories; the exact-permutation gates above guarantee them.

A fresh independent zero-energy maximally mixed bit r controls **every code-contact gate AND each flag reset**. At r=0 the memory path is skipped; at r=1 it runs. Refill can occur on both values. After tracing away r and all attempt resources, the good channel is within O(delta_n) of E=(id+Ad_X)/2.

## 3. Why the p_n factor is valid
The physical attempt decomposes as Phi=p_n Phi_good+(1−p_n)Phi_bad by its initial workspace label. Define the comparison channel Psi=p_n E+(1−p_n)Phi_bad. Both preserve the required input class, and ||Phi−Psi||≤p_n O(delta_n) on that class with arbitrary reference. Telescoping M compositions gives O(M p_n delta_n), not O(M delta_n). With M=ceil(log(4)/p_n), this is O(delta_n). Consequently there is no circular demand delta_n≪p_n.

## 4. Entanglement-breaking scope
For a single logical qubit with classical syndrome, E is X-basis dephasing and is entanglement breaking across memory/reference. Every subsequent memory-only CPTP map preserves separability. The ideal mixture's probability that no E occurred is (1−p_n)^M≤1/4. After any memory-only decoder, Bell fidelity is at most 1/2+(1/2)(1−p_n)^M≤5/8; the actual process adds O(delta_n).

**Multiple-logical caveat:** dephasing one logical qubit is NOT entanglement breaking on the unrestricted full logical Hilbert space. For a code with additional logical qubits, start the target qubit Bell-entangled with the reference, with all other logical factors initially independent of that reference, conditional on syndrome. The primitive trajectory restriction implies only tensor-product logical Paulis are applied; there is no logical SWAP, controlled logical gate, or logical-dependent predicate. Therefore no target-reference entanglement can transfer to other logical factors. Dephasing the target still makes the whole memory/reference state separable on this narrower preserved class. Alternatively, dephase every logical qubit using independent fresh random bits. One of these restrictions must appear explicitly in the theorem.

## 5. Physical isolation is essential
E is a statement about **memory after discarding the attempt's bath**. The joint memory+bath state may retain the entanglement in its r record, so calling that joint state separable would be false. Future code contacts must only access new workspace/reservoir identities; no old r, scratch, spent bath, or history record is allowed to return through a memory-coupled port.

Equal-gap SWAP routing can pass through physical sites that previously stored records only if state identities are tracked: restore the transport permutation or maintain a rigorous logical-to-physical map. Run routing with code contact disabled. The intended fresh state, not an old record displaced into a carrier, must be the state at every later active code-contact port. Bath-only rearrangement of old records is harmless; later recontact with memory is not.

This is constructible with dedicated banks/ports and polynomial routing volume/time. It must be part of the schedule, rather than inferred merely from the phrase 'fresh bath'. The ever-present drift K does not couple the bath records back to memory.

## 6. Resource and claim boundary
M is polynomial in n for each fixed noise rate. Each attempt uses O(log n)+O(m(q)) selected low-entropy bits; crucially these are not all simultaneously postselected across the M attempts. Each independent bank merely has probability p_n of being good. Total physical bath size, control pulses, and time are still polynomial, with fixed gap/body/range/strength bounds.

The cleanest counterexample uses no preparation noise on memory, and common fixed nonzero noise on a constant-density resource bath. This fits an independent heterogeneous noise class with per-site rates bounded above by q. It does not, without an additional initial-state estimate, prove the version requiring exactly the same nonzero rate on every memory spin.

The result is for explicitly driven, exactly K-conserving controls and admitted energy-resolved local code contacts. No autonomous/static extension or generic native-two-body realization is proved.
