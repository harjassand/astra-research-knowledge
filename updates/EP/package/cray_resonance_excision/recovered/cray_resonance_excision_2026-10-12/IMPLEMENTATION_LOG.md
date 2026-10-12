# Implementation and failure log

The retained primary benchmark files were generated during this investigation with one BLAS thread. The seeded fixtures are independent of the sampling streams and comparator calculations. See `run_benchmarks.py` for all seeds and parameters.

The main implementation uses an acquired fixed-point Gaussian proposal. It samples an approximating spectral reference and separately reports its mathematical floor-bias bound. It does not secretly claim that clipping is an exact contour operation. Normalisation and phase use the real-cycle Gaussian branch; a principal scalar square root of a determinant is not substituted.

### Retained negative evidence

1. Transfer quadrature with 192 points on the 16-site chain was under-resolved. Orders 320 and 512 agree, and all three outputs are retained.
2. The transfer and Wick comparators beat the independent estimator on the matched chain. The Wick result has no proven remainder, while neither transfer nor the floating estimator is interval-certified.
3. The coefficient gate becomes uninformative at moderate oscillatory gaps. The entire parameter sweep is retained.
4. The heat degree-two bound is informative near small h but about 7.55 at h=.1. An inexpensive local formula is not uniformly accurate merely because it behaves well at a singular limit.
5. The first algebra-diagnostic run attempted to sum symbolic Boolean atoms and failed. Converting each exact Boolean to an integer fixed the counting operation; no scientific inequality was changed. The final 200 assertions passed.
6. Small scalar pivots can be artificial: the coupled 2x2 determinant remains nonzero. A separate genuine determinant-zero experiment was added rather than treating the scalar-pivot example as a sign-problem solution.

### Unimplemented requirements

Outward-rounded gate evaluation; certified finite-bit Gaussian sampling; interval matrix factorisation; a global accumulated arithmetic error budget; exact tensor/contour baselines on ordinary-coupling 2D/3D inputs; an affordable many-block integration rule; a global residual phase theorem.

The result JSONs are numerical diagnostics and measurements. Checksums establish byte integrity, not scientific correctness. No physical experiment was performed.
