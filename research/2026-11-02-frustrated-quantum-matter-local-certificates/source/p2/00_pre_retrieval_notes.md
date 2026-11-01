# Independent pre-retrieval construction — 2026-11-02 (Brisbane)

## North star and currently unavailable capability
Give *rigorous, useful* thermodynamic-limit phase/energy comparisons for genuinely frustrated, strongly entangled 2D local quantum Hamiltonians from finite computational and experimental resources, including no assumed gap or sign-free Monte Carlo. A reliable density interval or phase-order certificate would affect material design and understanding of quantum matter; the generic problem is computationally intractable at sufficient precision.

## Admissible operations
Specified k-local bounded Hermitian interactions; exact or certified finite-patch diagonalization; local reduced density matrix (RDM) optimization/SDP; physical state preparation or variational tensor networks as upper bounds; interval arithmetic for numerical rigor; lattice symmetries. No exact thermodynamic state oracle, no presumed correlation length, no physically free nonlocal probe.

## Positive construction before reading Astra or papers
Write H=sum_x h_x on an infinite translation-invariant square lattice. For LxL open patch Hamiltonian H_L, a translated, normalized average of H_L gives H exactly (each x-edge lies in L(L-1) translated patches). Therefore the local operator bound H_L >= E_L I gives e_infty >= E_L/[L(L-1)] for nearest-neighbor equal-strength interactions, with the finite-volume thermodynamic justification on tori divisible by L. Upper bound e_infty <= (E_L + 2JL)/L^2 from tensor products of optimal open-patch ground states; 2L cross-tiling edges per L² sites and |<h>|<=J. A more informative lower bound might replace single-patch E_L with a compatible, translation-invariant patch-RDM hierarchy, and upper bounds with state constructions. Both are genuine global bounds with an O(1/L) surface uncertainty, not a scalable 2D breakthrough.

## Decisive obstruction
Local marginals optimized separately do not generally admit one common infinite-system quantum state (quantum marginal/extension problem). Enforcing global entanglement compatibility without exponentially large patches is the unearned operation. Even exact finite patches can leave bounds too far apart near competing quantum phases. A method that merely hides this operation as 'consistent boundary' or assumes a gap has not solved it.

## Initial candidate research mechanism
Use a dual local-operator decomposition providing a *verifiable sum-of-squares witness* that translates/tiles into an infinite-lattice energy-density lower bound, paired with a constructive upper state. Seek an automatically learned/optimized finite-support witness that recognizes frustration and cancels seam errors. This is provisional. Before claiming novelty, compare directly with Anderson cluster bounds, noncommutative polynomial/quantum marginal SDP hierarchies, quantum bootstrap and PEPS/DMRG. If it cannot improve the strong alternative at equal patch size/budget, switch problem or obtain an irreducible new invariant.

## Falsifiers
- Local-witness bound no stronger than optimized existing cluster RDM-SDP at same support/cost.
- A purported globally realizable patch family fails an extension example.
- Certified interval does not discriminate competing 2D phases before exponential resource growth.
- Numerical SDP lower values are quoted as certified without dual feasibility/residual checks.

Source cutoff: none consulted before this note.
