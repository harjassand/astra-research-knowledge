# Connection test before construction

**Date:** 2 November 2026, Brisbane. **Target source:** original square-lattice spin-1/2 J1-J2 Hamiltonian, alpha=J2/J1=1/2. **Prior preserved state:** producer-workspace/astra_phase_research_20261102.zip and unchanged baseline archive SHA256 `a339c1e31c60c27b0dfb77c13c725e19f04f8486a847e24e5f84ee2fe67e5a21`.

## Initial target and why it did not transfer

The previous question was field-selected spontaneous valence-bond ordering for alpha=1/2, not an interval around the ground energy. The earlier defect-gated and orthogonal-RK constructions fail to connect to the original exchange model. A finite-field energy secant is only an upper approximation to the right derivative at zero. Without uniform near-zero curvature control, narrowing independent absolute energy envelopes at one field does not certify the order parameter. The published structured NC polynomial hierarchy is a strong existing direct observable method; larger local moments alone are not a new organizing principle.

## Changed actual physical assertion

Ask a question of the original model that is not contingent on an unearned phase-transfer condition: whether its ground and low-temperature Gibbs states can be represented by mixtures of independent clusters of at most five spins. This is a model-relevant assertion about multipartite quantum correlations, distinct from and logically weaker than phase identification. It can be falsified through the *actual* Hamiltonian energy if a rigorous k-producible energy lower bound is obtained.

## Source-to-mechanism connection, derived before work on the certificate

At alpha=1/2 the square-lattice exchanges obey an exact classical square completion, equivalent to exchange-Fourier lower eigenvalue -2 J1. A state which is a product of quantum blocks has classical expectations between blocks and genuine quantum covariances only inside the blocks. This identity reduces its *actual physical energy* to finite block functionals, retaining all real Heisenberg interactions, with no orthogonal dimer assumption or recovered global marginals. Each functional has a negative quadratic term in local spin magnetizations. Replacing that scalar quadratic by the expectation of a fixed two-replica operator is exact on pure block states; positivity of the exchange-shift matrix extends it to mixed states. If finite spectral lower bounds hold for all connected physical interaction motifs of size <= k, they certify an energy floor for all k-producible states in arbitrarily large systems.

This creates a direct input/output bridge: physical H and a small-block *integer* dual bound -> physically meaningful entanglement depth, with no unknown susceptibility or many-body gap. This assertion was selected as the tractable, connected alternative; it must not be presented as a resolution of VBS, N\'eel, gaplessness or topological order.

## Mechanism failures and comparisons established during construction

- The exact 2-producible threshold -3/8 is sharp at alpha=1/2, so it cannot exclude 3-producible states or determine a phase.
- A two-copy operator bound with threshold -9/20 per spin **fails** on the four-site square (negative exact Bareiss pivot, physical interpretation: the *relaxation* can be entangled between its two virtual copies). The weaker -91/200 threshold passes all 1--5-site motifs.
- The two-copy spectral technique is an outer relaxation: its lowest eigenvector need not be a product of identical copies. A lower eigenvalue from the relaxation is not a physical ground-state energy; it becomes useful only after the precise product-state inequality is proved.
- Enumeration of 6-site motifs and a 12-qubit exact witness was not completed; numerical reconnaissance does not certify entanglement depth seven. No large-scale solver or gap oracle is implicit.
- Older energy-entanglement witnesses, symmetric-extensions/replica bounds and structured NC polynomial SDPs are established antecedents; comparative novelty/priority and advantage have not been established.
