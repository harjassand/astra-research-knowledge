# Methods, residual accounting, and execution costs

## 1. Euclidean conservation-enriched diagnostic

Starting from the exact initial delta, eleven approximate Arnoldi directions were generated using the full frozen first-hit operator, two-pass modified Gram–Schmidt, and adaptive TT rounding. The local relative Frobenius target was 10⁻¹⁰, subject to a per-vector rank cap of 16. The normalized full-grid constant and a separate overflow basis span the augmented mass co-kernel. A generalized Galerkin system was solved by degree-32 endpoint-inclusive Chebyshev collocation.

The rank cap was reached early. It applies to individual trial vectors, not the whole trajectory: the uncompressed summed grid representation has bond ranks [129, 168, 168, 168, 168, 168, 129]. The largest discarded unnormalized local 2-norm was 680.434; this was not treated as a certificate.

The grid's normalized constant has mass 163⁴ = 705,911,761. The Galerkin Gram condition was 1.00033, but the augmented dense time system reported reciprocal condition about 2.22 × 10⁻¹⁷. A separately scaled evaluation of the same reduced ODE reproduced the collocation endpoint to about 4.05 × 10⁻¹⁶ in reduced coordinates, identifying the observed wrong tail as spatial projection rather than time-solver failure.

Total mass was 1 + 1.47 × 10⁻¹⁶ under an 80-digit contraction, yet the uniform component carried 0.06443567 grid mass and overflow was 0.00456538. The exact balanced witness proves actual augmented-state error at least 0.1380019503.

## 2. Geometrically weighted follow-up

This documented follow-up used μᵢ(n) = 2⁻|n−50|/(3 − 2⁻⁵⁰ − 2⁻¹¹²), the similarity transform q = Dμ¹ᐟ² y, and the transformed mass representer √μ. Local reaction similarity ratios are at most √2 and diffusion ratios at most 2. Target freezing commutes with the diagonal transform. The initial whitened norm is approximately 81.

Twelve localized directions plus the product invariant direction were retained. Adaptive per-vector ranks were allowed up to 32; the summed trajectory bonds are [143, 314, 315, 315, 315, 314, 143]. The weighted Gram condition was 4.58942. The largest discarded local unnormalized 2-norm was 286.518. The stored physical bases and coefficients were explicitly rescaled, and full physical defects were evaluated after that conversion.

The full floating residual triangle diagnostic is 0.270841235943, consisting of spatial 0.270841235943 and temporal 3.60009 × 10⁻¹³. The final Krylov column contributes 0.1590791473; other spatial defects remain material. The cap tail drops to 3.27 × 10⁻³⁵, but the invariant direction still supplies excessive probability outside the localized cube. The exact balanced witness proves actual augmented-state error at least 1.509585413 × 10⁻⁴.

Grid weighted 2-norm plus absolute overflow dominates physical augmented 1-norm in exact arithmetic. A single combined augmented 2-norm with weights (μ, 1) instead needs a √2 factor. No unit-factor augmented inequality is assumed. Weight normalization and all upper diagnostic contractions remain floating rather than outward enclosed.

## 3. Reduced-only constrained structural follow-up

After the first two results, a documented structural test removed the broad rank-one trial direction and reused the same twelve localized physical basis vectors, unchanged. There was no new Arnoldi enrichment, rank increase, weight change, or physical/time-model change.

In the stored whitened coordinates, the constrained least-squares generator was

C = M⁻¹K − M⁻¹m (mᵀM⁻¹K + fᵀ)/(mᵀM⁻¹m).

The physical overflow derivative was separately fixed to fᵀa. The saved physical bases are literally supported on counts 39 through 61, so their cap-overflow flux is exactly zero. This does not suppress any physical transition; full operator leakage into counts 38 and 62 is retained in the independent residual.

The same degree-32 anchored time representation gives exact delta initialization at basis index 0. The Gram condition is 1.00006, the constraint denominator is 0.412397, and the floating mass-row norm falls from 14499.7583 to 4.91 × 10⁻¹². Export scaling uses a = S y, Cphysical = S C S⁻¹ with the original S.

The structural tail defect is eliminated exactly. Nevertheless the all-50 coordinate, evaluated with every full-generator predecessor, proves integrated residual at least 1.491853365 × 10⁻⁵. This already exceeds the entire 10⁻⁹ interior budget. The duplicate full residual QR was therefore not computed. No actual target-error or full-state-error lower bound is claimed for this third candidate.

## Continuous trajectory and full residual accounting

Every export defines the exact dyadic-coefficient polynomial

yⱼ(t) = initialⱼ + Σₖ₌₁³² cⱼₖ [Tₖ(2t/h − 1) − (−1)ᵏ].

This anchored definition makes initialization exact. There is only one slab, hence no join. The independent verifier constructs its constant shifts with exact rational arithmetic, rather than relying on floating endpoint cancellation.

For the first two candidates, each full physical spatial defect Eⱼ = A Bⱼ − B Cⱼ was evaluated as an uncompressed TT sum, including target freezing and the physical overflow residual. The complete residual identity is

R(t) = B[y′(t) − C y(t)] − Σⱼ Eⱼ yⱼ(t).

The upper diagnostic applies triangle inequalities to all columns and integrates absolute coefficient polynomials. It is not a diagonal Gram calculation or a projected residual. The weighted follow-up streams one residual core at a time and uses QR without singular-value truncation. Before use, this routine matched three full first-candidate residual columns to at most 5 × 10⁻¹⁶ relative difference. A near-canceling dense test lost 2.82 × 10⁻⁸ relative precision, explicitly demonstrating the lack of an enclosure guarantee.

All rounding, basis-conversion and polynomial-integration effects are reflected in the saved candidate and independent exact rejection tests. The floating upper diagnostics have no outward arithmetic-radius term and therefore cannot pass the rigorous gate. The verifier instead retains signed temporal polynomial terms, exact decimal model rates, directed TT contractions, physical boundary terms, and exact initialization. A lower bound from one separating functional or coordinate suffices to reject; it does not claim to enumerate the full norm.

## Resources and provenance

| Stage | Elapsed time | Peak RSS | Hard memory cap |
|---|---:|---:|---:|
| First candidate and complete residual diagnostic | 60.052 s | 1,274,188 KiB | 2 GiB |
| Read-only high-precision/scaled-ODE audit | 2.407 s | 260,748 KiB | 2 GiB |
| Streaming-QR validation | 5.765 s | 382,048 KiB | 2 GiB |
| Weighted candidate and complete residual diagnostic | 314.760 s | 1,319,156 KiB | 2 GiB |
| Reduced-only constrained candidate | 0.642 s | 171,064 KiB | 2 GiB |
| Third independent coordinate rejection | About 4.5 s | 89,232 KiB | 512 MiB |

Each candidate run had a 900-second timeout and single-threaded BLAS. The first complete residual stored at most 563,101,104 bytes of fused cores, with peak bond 296. The weighted streaming calculation used at most 377,504,088 bytes for a current core, with peak residual bond 571. No cap was exceeded. Exact verifier runtime/RSS details are retained in the certificates.

No acquired MATLAB program was executed, no package was installed, and no shared original was modified. The initial attempt to launch `/usr/bin/time` failed before numerical execution because that binary was absent; successful runs used internal elapsed/RSS logging.

These finite trial-space failures do not show that conservation itself is harmful or that full adaptive AMEn must fail. Conservation as a test constraint removes the documented Riesz-trial tail pollution, but positivity, conditioning, rank adequacy and small full residual remain separate requirements. No calculation advanced beyond h = 0.0001.
