# Thermal-core capacity and sparse-current certificate

## Result
For the actual periodic heatbath Ising graph with soft source on the acquired thermal core and majority-spin target, this package derives an explicit finite capacity lower bound proportional to the FULL core normalizer, rather than the exponentially less representative allminus weight. A corollary bounds actual entrance current through all nonwinding critical components with at most cR plus spins, without extensive bulk-normalizer loss.

This is a reusable partial result, not the full North Star, not a full mean-transition predictor, and not a sharp capacity estimate. The argument uses established Thomson, Peierls and canonical-flow methods. Broad scientific novelty has NOT been established.

## Read in this order
1. `THERMAL_CORE_CAPACITY_LOWER.md`: complete capacity construction and proof.
2. `SPARSE_ENTRANCE_CURRENT_CERTIFICATE.md`: support counting and exact thermal erasure. Use the next file for the combined normalization.
3. `BULK_FREE_SPARSE_CURRENT_COROLLARY.md`: final combined finite certificate and prior-art comparison.
4. `PRIOR_ART.md`: checked source links and exact comparison.

## Explicit restrictions
- θ≥4, φ=θ/R, actual source clock κ>0.
- Source core parameter r obeys 1≤r, r+2≤R/3, r<L/4. The +2 conservatively pays lattice box-width conventions.
- The sparse-family bound additionally needs the acquired M5/core error bound u_r<1 and M<floor(5R²)+1.
- The sparse violating component is nonwinding with an embedded filled domain. Dense compact, rough, and merging entrances with more than M plus spins remain unhandled.
- The result is a flow/energy certificate, not a claim that these paths are typical physical trajectories or a fast physical growth theorem.

## Tests and exact evaluation
All scripts require only Python standard libraries.

```
python thermal_capacity_flow_test.py
python rational_sparse_certificate.py
python sparse_current_thermal_normalization.py
```

The first checks exact rational divergence and energy accounting on an explicitly defined small test core. It is a flow-algebra diagnostic, not verification of the governing large-volume hypotheses. The second proves scalar constant bounds and coarse finite current-fraction consequences by EXACT rational arithmetic, integer square roots and elementary exponential-series inequalities. It does not independently prove the contour/flow theorem. The third gives convenient floating evaluations and rejects examples violating the explicit core-size condition.

For θ4,L8R,κ1,M10R, the exact scalar certificate gives at R20,r4 current fraction≤exp(−1130), and at R1000,r6≤exp(−68842), conditional on the proved geometric/source interfaces. κ1 is illustrative; the formula retains κ and must use the actual chosen clock.

## Review status
Internally derived with explicit proofs, source checks, and executed exact tests. This package is NOT an independent scientific audit or external validation. Independent verification is still required before treating it as an established research result. Held source material was not opened. No generic theorem may be substituted for the explicit assumptions above.
