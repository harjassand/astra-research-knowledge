# Tailored monotone defect flags for the actual one-body-reset compiler
2026-10-30. Structural derivation; not yet a complete dressed-barrier theorem.

For deterministic syndrome-measure/Pauli-update SSF, choose one Kraus operator K_s=U_{F_s}P_s per complete local consulted syndrome. Orthogonality P_sP_t=0 gives
K_s K_t^dagger=0 for s!=t,
E_h=V_h V_h^dagger=sum_s U_{F_s}P_sU_{F_s}^dagger tensor |s><s|.
Hence E_h is diagonal in commuting syndrome projectors and physical excited labels. Define
C_h=Q_h-G_h E_h,
G_h=product_{j~h}P_j (ready auxiliary projectors).
This positive projector flags either a dark excited component OR any occupied box having an occupied neighbor. It differs crucially from a bare dark-label flag.

The C_h commute with all data syndrome projectors, all auxiliary occupancy projectors, and one another. On any occupancy sector, a box with an occupied neighbor has C_h=Q_h=I on that occupied local sector; remaining isolated occupied boxes have disjoint data supports, so their E_h commute. Clean Hamiltonian terms commute with C_h: the drive creates/removes only the good Stinespring excitation when every neighbor is ready, and all adjacent drives are blocked when h is occupied.

Every physical one-body reset clears its own C_h and cannot create a C_j that was zero. If resetting an illegal occupied pair exposes a neighbor's dark component, that neighbor's C_j was ALREADY one because of the illegal edge. Thus the apparent dark-label branching is not growth of these combined flags. This is a sectorwise statement and can be written C_j L_hs (I-C_j)=0 for each jump, with local cases checked using occupancy and good-range invariance. It must not be confused with arbitrary Kraus-complement projectors commuting in illegal sectors.

A syndrome/label-monomial unitary completion for the gauge should be chosen explicitly: on each local syndrome orbit, map the source pair (s,excited_reference_label) to (s+sigma(F_s),label_s) using the appropriate Pauli isometry, then extend this injective finite matching to a permutation of the remaining syndrome/label pairs. Pauli equivalence gives equal-dimensional syndrome subspaces within each orbit. This normalizes the joint commuting syndrome/label algebra. Its guarded finite-depth product also does so.
With this completion, conjugated individual reset Kraus operators are partial monomial maps on the joint syndrome/label sectors. Therefore their adjoints preserve diagonal observables; no generic bad/bad interference needs to be assumed away for the RAW diagonal observable. The CP-dressed clock observable has off-diagonal clock components, so this structural fact alone does not settle its drift.

## Augmented animal idea
Add a fixed number R of unary tokens for every occupied C_h to an enlarged bounded-degree animal graph. Choose R larger than the bounded number of syndrome bits that any dirty reset can create. A dirty reset removes its own R tokens, creates no C flags, and changes only boundedly many data checks; it has a strictly positive net defect decrease. Good resets retain the SSF decrement. Complete changed patches to bounded cliques, and the same full-animal per-move charging can make every reset monotone in an augmented potential. This is an actual candidate mechanism for paying dirty DATA corruption, unlike mean defect damping.

Unresolved: the finite-clock CP dressing must be extended to this augmented observable and the actual conditional reset maps. Those maps act on neighbor labels in the gauge and no longer factor as a_h tensor a fixed data-only Phi_h on every sector. The signed commutator proof for the direct fresh-K model cannot be imported without checking these extra local terms and their domination by the dirty-reset decrement. Also the monomial gauge completion and all source-sector inclusions should be written as exact local operator identities before claiming the full physical theorem.

## Explicit full-Hilbert monomial completion (root construction)
The abstract finite matching can be replaced by an explicit local unitary. Encode the excited labels in an m-bit register, with reference label 0 and m the number of consulted syndrome bits. Let Pi_s be the complete local syndrome projectors (zero on impossible labels), and let F_s be the chosen Pauli correction, set to identity on unused/impossible labels. On the excited DATA+label space define
U_exc=[sum_s F_s tensor |s><s|][sum_s Pi_s tensor X_label^s].
The second factor coherently XORs the current syndrome into the label register and is unitary on the entire space; the first is a controlled Pauli unitary. On label0 it produces sum_s F_s Pi_s|psi> tensor |s>, exactly the bundled Stinespring isometry. On arbitrary dirty labels it remains a monomial map of global syndrome/auxiliary-label sectors. Extend as identity on ready and guard by all neighboring auxiliaries ready. This gives the required local monomial gauge without an abstract completion oracle. The local resource cost is exponential in the fixed read-footprint size, but independent of system volume.
