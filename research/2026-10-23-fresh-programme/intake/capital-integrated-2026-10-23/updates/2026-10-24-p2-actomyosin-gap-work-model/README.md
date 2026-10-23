# P2 actomyosin gap-controlled work model — 24 October 2026

This completed computational benchmark uses an explicit three-state actomyosin crossbridge model with fixed chemical affinity, geometric binding access, competing target sites, reverse reactions, and forces derived consistently from the state energies. It is a model prediction; the inspected muscle experiments support the relevance of distinct radial responses but do not calibrate this calculation.

## Calculated prediction

For a counterclockwise 1 nm by 1 nm square at fixed registry, total work changes from `+0.17333 pN nm` at centre `(x,h)=(10,14) nm` to `−1.36843 pN nm` at `(10,16) nm`. Axial-only work is positive at both gaps; including transverse-gap work reverses the total at 16 nm. After uniform registry averaging, predicted work per motor is `+0.0409348 pN nm` at mean gap 14 nm and `−0.0934483 pN nm` at 16 nm, while mean axial force remains contractile in both cases.

The calculation corrects an inspected source force term that produced about `1.56 pN nm` passive loop work with the strong state frozen. Deriving both force components from the same energy removes that loop work. It includes the confinement force implied by the steric head-access cutoff, completes the reverse-reaction cycle at fixed affinity, and normalizes the competition among periodic binding sites using the full shared-free-state stationary population. These checks concern the stated model and are not experimental uncertainty estimates or a fitted whole-muscle model.

## Physical boundary: no acquired scaffold operation

The geometry assumes two independently controlled relative translations and a defined motor-base reference frame. The cited DNA-origami thick-filament mimic has 40 nm pivoting connectors and observed angle variation; it does not identify the loaded deformation-transfer map. MAESTRO provides multidirectional loading through separately assembled configurations, but its measurements do not demonstrate two independently cycled displacement ports or a continuously fueled junction. The finite-handle argument is conditional on force-growth, rate-regularity, irreducibility and tail assumptions; it gives no attainable stiffness threshold or attachment chemistry.

Thus the completed result is a fixed-affinity, geometry-based work prediction for a conventional gap-controlled active-traction operation. No scaffold operation, calibrated transfer map, molecular realization, new materials capability, practical advantage or historical novelty is acquired. The exact completed source text and rendered HTML are retained in [the manifest](source_manifest.json).
