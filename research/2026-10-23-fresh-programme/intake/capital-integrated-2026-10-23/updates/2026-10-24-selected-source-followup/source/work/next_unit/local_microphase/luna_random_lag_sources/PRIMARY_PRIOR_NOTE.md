# Local screened-elasticity / equilibrium microphase: bounded primary-source check

## Finding

The closest decisive comparator is Qiang, Luo & Zwicker, “Nonlocal Elasticity Yields Equilibrium Patterns in Phase Separating Systems,” *Physical Review X* 14, 021009 (2024), DOI [10.1103/PhysRevX.14.021009](https://doi.org/10.1103/PhysRevX.14.021009). It already establishes the broad target mechanism: nonlocal elasticity with a structural length scale can stabilize equilibrium mesoscopic patterns in an elastic phase-separating gel; ordinary local elasticity cannot. Its main model uses a Gaussian convolution of strain with kernel `g_ξ(X) = √(2/(πξ²)) exp(−2X²/ξ²)`. In the SI, a generic quadratic displacement energy is rewritten as a sum/integral of finite-separation spring energies, with springs joining material points `X, X′` and energy proportional to `[u(X)−u(X′)]²`; an explicit Gaussian-chain network model gives the same bilocal form for endpoints `X ± γ/2`. The article and SI therefore directly own the nonlocal-elasticity explanation and a physical network-level finite-separation-spring ancestry.

They do **not** present the exact proposed local auxiliary-field realization `∫[C(u_x−αφ)²/2 + Dv_x²/2 + K(u−v)²/2] dx` or its exact screened rational multiplier `A_el(k) = E₀/(1 + ξ²k²)`. Qiang et al. choose a Gaussian kernel with Fourier multiplier `E exp(−k²ξ_QZ²/8)`; the rational kernel has a `k⁻²` high-wavenumber tail and is not equal to that Gaussian. The two models share a positive, scale-dependent elastic penalty and the same broad equilibrium pattern-selection mechanism; the parent’s exact two-network Hamiltonian is a distinct local realization/parameterization of that mechanism. This is a mechanism-boundary statement, not a novelty or priority conclusion.

## Closest cited experimental predecessor

Alig et al., “Irreversible frustrated spinodal decomposition in simultaneous interpenetrating polymer networks: Small-angle x-ray scattering,” *Physical Review B* 53, 11481 (1996), DOI [10.1103/PhysRevB.53.11481](https://doi.org/10.1103/PhysRevB.53.11481), is the direct IPN antecedent cited by Qiang et al. It derives a hydrodynamic-limit structure factor for spinodal decomposition frustrated by growing topological restraints and compares it with SAXS from simultaneously cross-linked poly(carbonate-urethane)/poly(methyl methacrylate) IPNs. The reported frozen-fluctuation length is about 2 nm for one-glass-transition samples and 15–35 nm for two-glass-transition samples. This is real-material evidence for topology-frustrated/frozen composition structure, but the published abstract does not describe an equilibrium screened-repulsion Hamiltonian or the specific local two-network elimination. It is not the same exact mechanism as the proposed local model.

## Acquired material operation in the strongest comparator

The PRX article describes the experiment it explains: equilibrate a relaxed PDMS gel by soaking it in oil at high temperature for tens of hours, then cool it; the sample develops bicontinuous oil/gel structure with arrested scale roughly 1–10 μm, dependent on gel stiffness, reversible on reheating and reported independent of cooling rate. This establishes an actual gel/oil microphase-separation operation and pattern readout. It does not establish fabrication or validation of the proposed `u,v` two-network architecture or its rational screened kernel.

## Source boundary

- Qiang et al., official APS article: https://journals.aps.org/prx/abstract/10.1103/PhysRevX.14.021009
- Qiang et al., official APS Supplemental Material, especially Sec. III, Eqs. S27–S33: https://journals.aps.org/prx/supplemental/10.1103/PhysRevX.14.021009/ps_em_sm.pdf
- Alig et al., official APS abstract: https://journals.aps.org/prb/abstract/10.1103/PhysRevB.53.11481

The APS Alig page exposes the abstract; detailed claims here are intentionally restricted to that abstract. No novelty claim is inferred from the absence of the exact auxiliary-field model in this bounded source check.
