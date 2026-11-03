# Root construction check: full-fiber unitary moves cannot supply the interface

2026-11-02. This is a scoped elementary obstruction, not a no-go for the interface.

For a finite free slab with finite fermion Fock space and a fixed rotor configuration phi, write the combined axial charge as

Q(phi) = Q_slab + K(phi) + s(phi) I.

Here s is the scalar rotor self-linking charge, and K is the decoration pairing number operator of §3.3, arXiv2601.04304v2. The Majoranas are perfectly paired on a closed geometry. Every pairing K has the same full-Fock spectrum, up to a configuration-independent convention for its constant; in particular its trace is independent of phi. Q_slab is independent of phi. The slab and decoration occupy separate fermion factors.

A candidate local rotor hopping |phi'><phi| tensor U, with U a unitary on the complete finite fermion fiber, is exactly axial invariant only if

Q(phi') U = U Q(phi).

Taking traces after conjugation implies s(phi') = s(phi). Consequently a self-linking-changing move cannot be a full-fiber conditional unitary. This remains true even without any locality restriction on U. Adding finitely many ancillary charged fermions independent of phi does not repair the trace mismatch. This argument concerns the full finite Fock fiber, not a selected low-energy subspace or an unbounded charge reservoir.

This rejects a tempting proof shortcut: build controlled unitary fermion swaps for every rotor move and claim the kinetic Hamiltonian is a conjugated product rotor Laplacian with unchanged gap. The swap cannot meet the exact charge condition on the full fiber for a charge-changing move.

What IS allowed is a partial charge-transfer operator T satisfying Q(phi') T = T Q(phi). Its kernel is unavoidable for a finite charge ladder shifted by nonzero amount. A schematic fermion annihilation operator supplies precisely such a partial map, but does not itself identify a local slab mode or prove its matrix element on the actual correlated ground states. Combined odd operators can make the complete transfer even.

A viable construction must prove that these kernels never obstruct the relevant low-energy motion, and control the resulting configuration-dependent hopping amplitudes and loop phases. Equivalently it could use an explicitly charged unbounded reservoir, but then symmetry, rotor domain, normalizable ground state and resource costs must be supplied. The trace check does not forbid a uniformly gapped low-energy interface and should not be presented as doing so.

Primary definitions inspected: https://arxiv.org/html/2601.04304v2, equations 73–76. The trace argument is root's elementary deduction, not a claimed new general theorem.
