# Astra: deterministic computation for a published thermal-avalanche model

Research handoff, 15 October 2026.

## Capability

Compute a fixed-disorder mean lifetime and rigorous early-failure upper bounds for the thermal-creep fiber-bundle model of Hiemer, Moretti, Zapperi and Zaiser, including initial and subsequent instantaneous mechanical avalanches. The calculation avoids enumeration of all failed-fiber subsets.

This is a conditional computational result for a published theoretical model. The strength fixtures are specified synthetic realizations. No measured material calibration, time conversion to seconds, or validated engineering reliability claim is supplied.

## Evidence

An exact common-clock construction gives a static order-statistic lifetime formula. A positive count-boundary dynamic program evaluates the relevant internal-time population probabilities in O(n²) arithmetic operations.

For 400 fibers, f0=.125 and T=.05, integer arithmetic certifies a mean lifetime between 858.3703837983501 and 862.676217625171 model-time units, an interval of about 0.502% relative width. The measured certificate kernel took 6.28 seconds. Inputs are exact binary64 strengths from the specified NumPy seed, interpreted as rationals; force and temperature are stated exact rational values. The prototype stores O(n²) mechanics, although the probability recurrence itself uses O(n) workspace.

For a separate published parameter pair f0=.15, T=.1, with the specified 400-fiber realization, the failure probability by dimensionless time .1 is at most 1.14594e-110. This is an upper bound, NOT an estimate or a matching two-sided interval for the actual probability. An independently reconstructed 1024-bit positive DP verifies the bound. The source-aware pure-birth comparator gives the weaker upper bound 4.48222e-86.

A hypothetical ±.01 coordinatewise strength box still yields a uniform upper bound of 1.58996e-103 at the same deadline. This uncertainty box is illustrative, not measured. Both thermal rates and avalanche thresholds change together in this calculation.

## What changed from the earlier construction

The published model immediately removes overloaded fibers. Omitting those avalanches changes the event being computed and can materially shift lifetimes. The earlier complete-failure importance-sampling certificate does not automatically transfer.

The corrected representation retains that operation exactly. It also allows classical radial conditioning to reduce variance by about 2.4–2.8 times in the tested early-failure examples. Those variance observations are floating-point diagnostics and do not certify extremely rare tail probabilities.

## Closest prior work and novelty boundary

The model, kinetic Monte Carlo, static bundle reliability, Poisson-binomial boundary recursions, minimal cuts, uniformization and Gamma/Dirichlet conditioning are established machinery. The contribution developed here is the explicit avalanche-aware clock representation, its shared boundary computation, and complete fixed-input certificates. Historical novelty and superiority over every specialized method remain unestablished.

Primary model: https://arxiv.org/abs/2508.13367
Author source: https://github.com/ComplexityBiosystems/fiber-bundle
Simulation archive metadata: https://doi.org/10.5281/zenodo.16413747

The 42 GB archive contains simulations, not physical experiments, and was not downloaded. The report explains two apparent printed-equation inconsistencies resolved using the mutually consistent rate equation and implementation; the certificate uses that explicitly specified model.

## Missing operation and plausible consequence

The computation now supplies deterministic risk certificates for this model, including regimes inaccessible to ordinary direct sampling. It does not supply the exact rare-tail probability, spatially localized load transfer, matrix-creep memory, or experimentally justified microscopic rates. Those are separate scientific gates.

A plausible use is checking whether a specified model satisfies a very small risk budget without requiring observed failures. A real engineering decision would additionally require calibrated material data and model discrepancy bounds.

## Decisive next tests

- Reproduce the integer certificates and check the order-statistic/common-clock proof.
- Compare additional source parameter/strength realizations and specialized competing bounds.
- Acquire measured creep data and determine whether the model's constitutive, independence and load-sharing assumptions are defensible. Do not turn specimen-level lifetime fits into elementary fiber hazards without an identification argument.

## Files and replay

- failure_source_benchmark/ASSESSMENT.md: source qualifications, exact clock and static proof, radial transfer and honest execution provenance.
- avalanche_boundary_dp/DERIVATION.md: shared boundary PMF proof.
- avalanche_boundary_dp/LARGE_CERTIFICATE.md: integer exponential/DP/integration error proof and compile/run commands.
- avalanche_rare_bound/REPORT.md: one-level tail bound, informed comparator and hypothetical strength uncertainty.
- avalanche_independent_audit/REPORT.md and RARE_AUDIT.md: exact replay and separate arithmetic checks, with scope limits.
- avalanche_independent_audit/rare_integer_check.py: standalone rare-bound verification.

Only source scripts and data are distributed; compile the C++ certificate locally using the documented command. Dependencies are Python, NumPy, SciPy and mpmath for the indicated supplementary scripts, plus a C++17 compiler for the integer mean certificate. No script installs dependencies. Saved integer numerator/denominator fields, rather than displayed decimal rounding, define exact endpoints.

No canonical Astra records were changed and no external outreach or spending occurred.

## Separately acquired measured evidence

The measured_creep folder contains 303 published Kevlar/epoxy composite-strand lifetimes at three loads, transcribed from Robinson's 1992 NASA-archived report reproducing LLNL/Glaser observations. It includes observed-hour CSVs, numeric-table images, independent analysis code and provenance. The original report is linked in the assessment rather than repackaged.

Endpoint cohort means differ by 52.23 times. Conditional on comparable cohorts, a two-point power-law interpretation gives effective specimen exponent 47.16; this is not a microscopic fiber hazard exponent. The third cohort does not distinguish that law from linear-stress activation at the available precision. The exploratory lifetime-shape tests do not establish a multiplicity-adjusted rejection of exponential specimen lifetimes.

Temperature, loading/proof history, batches and exclusion logs remain incomplete. These measured observations therefore do not validate or calibrate the computational avalanche fixture above. They provide an external evidence base and expose the remaining identification problem.
