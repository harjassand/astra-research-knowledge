# Joint compatibility: exact dual-kernel sampling

A complete exact sampler and a rank-budgeted conditioning theorem were derived and tested. For `F(x)y=g(x)` with affine `F`, arbitrary efficiently evaluable `g`, and a verified collective matrix-rank bound `R>=m+1`, the algorithm outputs a uniform sample from **all** joint solutions in fewer than three expected trials. Pure bilinear constant-target systems need `R>=m` for fewer than four trials.

A raw-matrix acquisition rule based on Moore interpolation supplies the rank certificate for an exposed linearized-polynomial class. It is classical rank-metric structure, not a newly solved general certification problem. An exact hidden-basis example preserves intrinsic minimum rank 4 but reduces this acquisition rule's bound to 1. A fully coupled diagonal restriction can make a high-rank system unsatisfiable, so unrestricted composition remains open.

No historic capability or novelty claim is made. The prior pivot-chart idea was identified as an established LLD argument and is retained only as a screened branch.

- `DUAL_KERNEL_COMPATIBILITY.md`: full input model, law, cost, closure, native acquisition, and boundaries
- `PIVOT_CHART_SCREEN.md`: screened deterministic chart mechanism and coordinate trap
- `PRIMARY_SOURCES.md`: targeted baseline check
- `verify_dual_kernel.py`: executable exact checks
- `EXACT_RESULTS.json`: full matrices, coefficients, transformations, probability checks, and counterexamples

Reproduce with Python 3: `python verify_dual_kernel.py`.

A subsequent native-envelope gate is in `AFFINE_ENVELOPE_GATE.md`: affine rank-stratification can need exponentially many pieces, even on independent diagonal matrices. A stronger bound rules out polynomial-overhead arbitrary polynomial-size positive mixtures of uniform affine laws on that family. Independent product sampling succeeds there, so this is a representation-specific obstruction, not an intrinsic hardness claim.

`run_native_sampler.py` additionally executes the actual sampler after raw-matrix certificate acquisition, without enumerating coefficient vectors or assignments. In the retained 16-by-16, six-constraint binary test, all 200 outputs passed every joint equation, using 252 trials. This smoke test is separate from the exhaustive exact-law proofs.
