# Decisive local-transfer test, independent of the first hopping ansatz

Root derivation, 2026-11-02. Standard purification duality used as a constructive diagnostic; not a novelty claim or interface proof.

Let psi and psi' be normalized endpoint fermion ground states, including BOTH the complete finite free slab and the decoration. The rotor configurations differ by one permitted local reconnection. Split the fermion modes into a bounded neighborhood R of the move and its complement E. Use a fixed graded tensor-product convention; the final physical operator is even.

Define X_R = Tr_E |psi><psi'|. Then

  a_R = max_{||O_R|| <= 1} |<psi'|O_R|psi>|
      = ||X_R||_1
      = F(rho_E, rho'_E),

where F is root fidelity, not its square. First equality to the trace norm is trace/operator-norm duality. The last equality is Uhlmann purification duality. If X=V|X|, O=V† attains the maximum on its support and extends to a contraction. This is an explicit optimal finite-patch transfer, rather than guessing a single creation operator. For a fixed-size patch its matrix can be acquired from the actual endpoint states; acquiring those states is still charged.

Symmetry qualification: choose R large enough to contain all changed pairing edges and closed under the two endpoint Majorana pairings. The charge decompositions must then actually take the form Q(phi)=Q_R+Q_E and Q(phi')=Q'_R+Q_E, including the scalar self-linking difference in a local term. This common exterior generator is to be checked, not assumed for an arbitrary bipartition. For endpoint total charges equal, average O as

  O_bar = integral_0^{2pi} exp(it Q'_R) O exp(-it Q_R) dt/(2pi).

When these define the relevant periodic representation, O_bar is an intertwiner, its norm is at most one, and its endpoint matrix element is unchanged. More generally include the phase selecting the endpoint charge difference. Vector symmetry needs a DIFFERENT check: it translates the fixed rotor configurations, so the individual fibers are not vector-charge eigenstates. One must construct an equivariant family T(phi'+alpha,phi+alpha)=V(alpha)T(phi',phi)V(alpha)^dagger (with the correct microscopic action), or prove that averaging the whole kernel preserves the required amplitudes. Averaging a single fixed-fiber O over vector symmetry is not justified by the axial argument. Equal total fermion parity allows parity-even projection without reducing this matrix element. The rotor shift times O_bar is then the corresponding invariant local move.

This does not contradict ROOT_CHARGED_MOVE_OBSTRUCTION.md: O_bar is a contraction/partial map and need not be invertible on the full fermion fiber.

What this test can establish:
- If a particular single-fermion hopping amplitude is small but a_R stays bounded, the ansatz failed, not every local mechanism.
- If a_R tends to zero with increasing slab size for every fixed patch, NO bounded-norm operator on that patch couples the endpoint ground states at first order with a uniform amplitude.
- If a_R is bounded below, an isolated two-sector degeneracy with identical energies has a first-order split 2g a_R; leakage into other sectors requires a separately proved gap and perturbative error, and cannot be ignored.

What it cannot establish:
- A finite-patch anticrossing does not give a thermodynamic gap, uniqueness, no topological order, or a rotor truncation theorem.
- Endpoint states may include the desired far-boundary chiral modes; a fixed sector/boundary condition is needed, and their finite-size gap must not be used as an interface gap.
- Uniform exterior fidelity for one move does not establish phase consistency for overlapping moves. Their products around loops remain part of the actual Hamiltonian problem.

Useful next numerical quantity is a_R versus slab width, lateral volume, patch radius and reconnection geometry, computed using all occupied slab orbitals. For Gaussian endpoints the exterior states are fermionic Gaussian and their fidelity is obtainable from covariance matrices; exact small-patch Fock computations can cross-check conventions. A declaration that only the crossing orbital matters is insufficient.

## Further locality qualification

The optimization is pointwise in the COMPLETE endpoint rotor configurations. Although O_R acts on a bounded set of fermion modes, its coefficients obtained from endpoint ground states may depend on rotors arbitrarily far away. Thus pointwise optimal local fermion support is not by itself a bounded-range joint rotor–fermion Hamiltonian. A physical construction needs one coefficient rule depending only on a fixed rotor neighborhood, working uniformly over all allowed exterior configurations. An obstruction from a_R -> 0 remains valid; a positive a_R only removes one necessary local-access barrier. Uniform compatibility across exterior configurations is an additional decisive test.
