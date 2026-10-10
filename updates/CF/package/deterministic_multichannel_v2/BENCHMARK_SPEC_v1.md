# Bounded native three-channel benchmark specification

Frozen 2026-10-09. Do not launch the endpoint benchmark until the focused proof check resolves the mathematical contract. This is a specification, not a results file.

## Exact target and inputs

Use the irreducible rational quadratic family in verify_three_channel_scaling.py. Each method receives the same explicit rational coefficient matrices, rational Omega, interval [0,1], initial matrix I_3, and tolerance 2^(-s). Return the complete 3-by-3 endpoint matrix, including coherent relative and global phases. No phase alignment, population-only scoring, or relaxed observable substitution is permitted.

Parameterize eta=2^(-B) and Omega=2^(3B+f). The three independent rows of experiments are:

- Frequency: B=3, s=20, f in {-2,0,2,4}. Only Omega changes.
- Precision: B=3, f=0, s in {12,20,28,36}. Only requested accuracy changes.
- Coalescence: f=0, s=20, B in {2,4,8,16}. This follows the adversarial fixed-transition-strength scaling. It is reported separately because frequency and geometry change together.

Deduplicate shared rows. Run a prerequisite row B=2,f=0,s=12 before the sweeps. All coefficients remain exact rationals in the manifest. Every solver may use the known family rescaling; no method gets an uncharged connection matrix or precomputed transition amplitude.

## Candidate modes

1. Certified mode: interval/ball propagation of coefficient, root, projector-jet, scalar-phase, local truncation, endpoint conversion, and product errors. A complete analytic or interval certificate must bound the global operator error by 2^(-s).
2. Exploratory mode: high-precision numerical realization of the same normal form. It can establish observed contraction, numerical endpoint agreement and acquisition counts. It must be labeled uncertified and is not allowed to satisfy the certified success condition.

Use local measured enclosures/residuals to avoid literal enormous worst-case constants if they are rigorous; otherwise retain the theorem's conservative fallback. A floating-point residual sampled at nodes is insufficient to bound a continuum residual or certify the final matrix.

## Baselines

A. A high-order adaptive exponential/Magnus implementation for the same matrix IVP, with working precision and error control charged. A stiff/Runge–Kutta implementation may be included as an additional diagnostic but is not the only baseline.

B. A current phase-function systems baseline, ideally Hu–Bremer 2025, including cyclic-vector selection/scalarization, conditioning repairs and sufficient working precision for the same operator tolerance. The verified public FreqInd package solves scalar second-order equations; it cannot stand in for this irreducible third-order scalarized problem. A native reconstruction is admissible only after checking it on the published system examples and verifying its numerical behavior. No external contact is authorized to obtain unavailable source.

C. A high-precision Taylor/certified D-finite reference where affordable. If the reference is merely a tighter floating-point solve, disagreement is informative but agreement is not a rigorous certificate.

No conclusion of superiority over optimized frequency-independent methods is allowed while B is unavailable or not valid on the target. A comparison of candidate A alone is reported precisely as such.

## Accounting and limits

Primary metric: cold-start wall time and total native work per successfully certified endpoint. Include coefficient conversion, discriminant/root acquisition, eigenvalue/projector work, all jet stages, phase quadrature/argument reduction, block propagation, certificate construction, and endpoint products. Record failed/rejected local panels too. Do not time only the final matrix multiplication.

Also record: maximum working bits, H/derivative/eigensystem calls, root refinements, panel count, cluster sizes, maximal normal-form order, Taylor order, scalar phase evaluations, all certificate contributions, resident-memory high-water mark, and output hashes. Reuse/caching is a secondary amortized metric with its setup and reuse count stated. Allow equivalent caching and family rescaling to every method.

For this first included-compute pass, cap each executed solver row at 30 seconds and the whole pass at 180 seconds of native solver time. A capped row is censored, not a mathematical lower bound or a completed failure proof. The purpose is to decide whether a modest implementation is worth pursuing, not to acquire a publication-scale benchmark. Do not increase these limits silently or launch external jobs.

## Acceptance and fallback

A certified success requires a global bound <=2^(-s), not just apparent unitarity or agreement with another discretization. Compare total costs only among equal-contract successes. Preserve every uncensored output, every error budget and every missing/censored row.

If reliable interval arithmetic cannot be implemented within the available native scope, stop the certified sweep and preserve the mathematical construction plus clearly marked exploratory results. Do not relabel numerical sanity checks as rigorous endpoint certificates. If the phase baseline remains unavailable, retain the stronger-baseline comparison as an explicit open gate rather than announcing practical superiority.

## Reproducible manifest

Run make_benchmark_manifest.py to regenerate benchmark_manifest.json. It specifies the exact rational coefficient list and independent sweep labels. Solver adapters must accept this list rather than substitute an analytically solved surrogate. No benchmark has run as part of generating the manifest.
