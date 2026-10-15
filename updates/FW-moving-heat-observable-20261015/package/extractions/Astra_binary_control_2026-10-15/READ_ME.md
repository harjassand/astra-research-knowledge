# Astra binary-control research: constructions, limits, and baseline

15 October 2026. Mathematical and synthetic evidence only. No hardware validation or historical-priority claim. No canonical repository changes.

## Decision

Do not promote the fixed two-anchor schedule as an experimentally efficient acquisition method. Its exact identifiability result survives, but a stronger same-budget random-design baseline performed better under noise on every one of twelve paired synthetic ground truths. Continue only where a new operation addresses global branch selection or measured acquisition conditioning.

## Exact constructions

1. **Polynomial exact binary query count.** A bounded-degree function-field argument shows the full binary response map can generically be recovered from O(m² log m) exact readings. Offline symbolic selection/reconstruction can be exponential or worse. This removes a query-interface obstruction, not the computational or physical precision obstruction. See binary_control_acquisition, including a complete degree-lemma proof check.

2. **One versus two anchors.** One-anchor low-support calibration generically fails for m>=5. Two anchors give generic local identifiability with O(m²) settings; an exact modular 20-by-20 minor and overlap argument establish this for all m>=5. Local identifiability is not globally unique or computationally easy recovery.

3. **Conditional constructive recovery.** Given an acquired anchor scaffold, each other directed pair is recovered by a 3-by-3 linear solve. A constant-block exhaustive algebraic procedure plus checkable branch-compatibility conditions supplies a conditional global prediction certificate. No nontrivial complete passing instance or generic pass theorem has been established. A separate exact rational known-three-anchor attachment example is exhaustively solved, including excluded poles. It does not acquire the unknown seed.

4. **Prediction certification.** A shifted diagonal-stability margin bounds all-subset prediction from a verified model enclosure, including binary normalized matrices whose zero diagonal makes the previous unshifted condition unnecessarily restrictive. This does not acquire the enclosure.

Exact construction outputs use compact matrix/algebraic-circuit representations. A full scalar algebraic minimal polynomial can require much larger representation; polynomial arithmetic counts are not unconditional polynomial bit-time prediction. Weighted-transpose ambiguity preserves the response map, not every physical state constraint.

## Decisive baseline check

The final comparison jointly fits raw baseline, singleton weights and matrix couplings, avoiding frozen calibration-noise bias. It uses identical setting budgets, four readings per setting with raw Gaussian standard deviation 0.001, twelve initializations, twelve physically admissible synthetic ground truths (m=5 through 10, two seeds each), and training-loss-only selection.

Median full-table RMSE:
- Two-anchor: 0.006522924
- Equal-count random: 0.000759163

Random has lower error on the identical full response table in all twelve paired cases. Both designs' selected fits converge and have small training residuals. This is evidence within a small constructed ensemble, not a universal comparison or hardware result. Every table entry is synthetic; exhaustive validation has exponential size and is explicitly charged separately from acquisition. See binary_fitting_baseline/joint_raw_fit/REPORT.md, which supersedes the initial noisy comparison. All source, raw synthetic data, fits, budgets and per-subset errors are included.

## Closest prior result and missing operation

2026 read-once determinant / principal-minor learning is polynomial-time under a stronger oracle. Binary scalar measurements supply linked ratios, not the needed minors or arbitrary field evaluations. An exact two-control ambiguity prevents simply assuming original denominator minors can be recovered. Existing experimentally demonstrated inverse-model fitting is the practical baseline. Sources and exact oracle differences are in binary_learning_prior_art/PRIOR_ART.md.

The unresolved new operation is efficient, globally valid and noise-accounted reconstruction from binary scalar readings that improves the actual experimental task. The present work does not establish that capability.

## Reproduction

Each directory contains its own report and scripts. Only locally written source and data are packaged, not executable binaries or downloaded author software. Python NumPy/SciPy/SymPy requirements are described in the reports. The exact modular witness, pair solve, attachment elimination and independent scaffold checks can be replayed separately from the numerical benchmark. Audit reports include proof arguments and receipts; their labels alone are not independent scientific validation.
