# Physical opportunity checkpoint — 2026-10-24

The owned result is a constructive global optimum for finite-temperature harmonic ballistic heat transport in a passive periodic single-backbone material. Mission-level physical capability is NOT_ACHIEVED. Historical novelty and real material advantage remain UNKNOWN.

## Governing statement and positive construction

PHONON_OPTIMUM.md is the stable governing proof (SHA256 99f7440adef09397b338b81d3f4b4f5803b51796331edfa3d851778766089959).

For any finite connected internal network of positive masses/springs attached to one scalar backbone coordinate, with one adjacent-cell backbone spring K, total cell mass M, and backbone mass m>=m_min>0, the full acoustic-and-optical pass-band indicator obeys a trace moment and a regularized logarithmic moment. A scalar dual therefore certifies a complete spectrum globally, while admitting arbitrary internal topology, additional resonators, arbitrary internal stiffness, dark modes, and reallocation of mass onto a heavier backbone.

At theta=k_B T/hbar=1/2 choose
m_min=m=1,
M=3.3387164232022783,
K=3.7866316437609973.
A single side mass2.3387164232022783 attached by internal spring2.8019347878118195 realizes bands
[0,1] union [2,4.259874009292292].
It is globally optimal within the stated passive class.

The full Bose-weighted conductance integral is1.133319342823405, versus1.440176577374174 for the equally massive rigid chain at the identical K: a numerical21.3069% reduction in this exact ideal model. Strict benefit is analytically certified; an exact rational Riemann certificate also gives difference>0.29034279485998. The current optimum is an explicit finite primitive rather than an unverified numerical search.

At high temperature its larger total bandwidth makes it worse than the rigid chain. As T tends to zero, both have the same leading single-channel quantum. This is useful thermal spectral redistribution in a finite quantum window, with the compensating optical band fully charged.

## Actual checks and independent review

phonon_optimum.py / phonon_optimum.json reconstruct the matrices, both spectral moments, complete bands, root and conductance numbers.
phonon_dual_exact_certificate.py / .json use exact Fraction exponential bounds to prove every required sign and a strictly positive conductance difference.

The owned analytic argument supplies the all-frequency root count and global optimum. Numeric frequency samples are diagnostics. Root independently reconstructed the proof; passive_lag then completed a whole independent mathematical review and reported PASS, including four bounded support readbacks, exact rational endpoint checks and nonstar/dark-mode challenges. These are internal reviews, not external certification.

The permitted supports checked sources, exact mechanics/spectra, scalar dual and finite-T quadrature. The finite internal-connector inertia model is a separate completed model check, not a premise or replacement for the exact point-mass/spring theorem. All three bands are included for midpoint connector masses from1% to80% of the side-mass budget; the tested family retains approximately18.7–21.2% lower ideal conductance than the rigid comparator. REALIZATION_CHECKS.md states its exact scope and the separate physical frequency/specific-modulus limits.

## Physical operations and strongest boundaries

Passive local-resonance thermal control is established prior art, including nanophononic modeling and experiments. The specific contribution under examination is the two-moment full-spectrum optimization and explicitly attained global finite-T optimum at a positive backbone-mass lower bound. See sources_support/PHONON_SOURCES.md and the narrow optimum-prior addendum when complete.

SERIAL_CHAIN_COMPARATOR.md separately proves that every purely serial positive scalar mass/spring chain with the same total mass and static series stiffness has intrinsic conductance at least the rigid-chain value at every temperature. Thus ordinary serial dimerization and mass redistribution do not reproduce the positive pendant-resonator benefit.

The theorem does not optimize all materials. Multiple independent intercell bonds, nonlocal intercell topology, nonlinearity, disorder/localization, lossy contacts and full3D transport are different comparator classes and may improve on this primitive. Diffusive conductivity, unchanged electronic power factor, cheap manufacture and civilisation-scale consequence are not established.

A real continuum spring has mass, finite specific modulus and internal modes. For a rod of length a, E/rho imposes mass>=K a^2/(E/rho). The construction fixes positive m_min and finite ratios, but physical connector mass, strength and anharmonicity still need an actual realization. No apparatus, specimen, measurement, purchase, outreach or public disclosure occurred.

## Why the first fracture construction was not promoted

FIRST_CONSTRUCTION.md preceded all support exposure. A literal reciprocal spring/bistable cell does shield a different threatened port and closes its complete load/preload energy ledger. cell_comparison.py/json then apply conventional-spring and flexure-travel failure limits. The delayed-snap and favorable preselected branches of the identical material model reach the same final state and fail at the same force5.389568535390918. The delayed state adds2.25 units of ordinary hysteretic absorption. Since snapping/transformation toughening is also primary prior art, the work pivoted to the positive phonon optimum rather than promoting a relabeled fracture operation.

The capital checkout remained read-only at e606bfc587c76bdcae8b8fa3ec33e721efa2fbac. No formal goal, automation, pool expansion or producer packaging was created.

