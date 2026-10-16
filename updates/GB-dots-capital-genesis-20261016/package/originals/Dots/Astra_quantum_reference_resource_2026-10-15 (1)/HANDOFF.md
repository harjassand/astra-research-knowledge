# Quantum reference dimension resource law

Research handoff • 15 October 2026

## Capability established

This package determines exactly how the dimension of an untouched quantum reference changes a classical symmetric channel’s conditional standard-Petz/RLD distinguishability. For m classical symbols, symmetry parameter lambda, and reference dimension at most r, the sharp coefficient is

eta_(m,r) = lambda²/[lambda+((1-lambda)/m)(k+1)/k], with k=min(r,m-1).

Equivalently, an m-symbol erasure measurement with reveal probability q dominates that symmetric measurement in reference-assisted standard Petz-D2 order exactly when q >= eta_(m,r). Unequal reference marginals are allowed. Separable classical-quantum states suffice: the examples require noncommuting reference blocks, with no entanglement requirement.

For m=4 and lambda=1/2, the thresholds are 1/3 for scalar references, 4/11 for a qubit reference, and 3/8 once the reference dimension reaches three. The reference advantage saturates at dimension m-1. THEOREM.md states and proves the result, including faithful approximants and exact-dimension extensions.

## Evidence and confidence

Status: internally proved, with an independent internal reconstruction of the inequalities and an exact symbolic sharpness example. External expert review and historical priority remain open.

The general proof combines a rank-sensitive projection inequality, a zero-sum inverse inequality, a spectral Jensen bound, and a Hermitian simplex-frame construction. The accompanying exact checks establish:

- The projection identity and the m=4, r=2 sharp limit 4/11.
- Global ordinary-order polynomial identities for a ternary example.
- A rational, faithful ternary/qubit counterexample, even after common input noise makes every channel effect strictly positive. Its source-minus-target Q2 difference is exactly -5193535897517/810667132432430.

The scripts use exact symbolic arithmetic. Floating-point decimals in the fixture are convenience displays, not proof inputs. These tests are reproducible consistency and witness checks; they do not replace the general mathematical proof.

## Closest prior work

The ordinary scalar formula is credited to Gu and Polyanskiy, Appendix A, Proposition 40, Eq. (231), in [Non-linear Log-Sobolev Inequalities for the Potts Semigroup and Applications to Reconstruction Problems](https://people.lids.mit.edu/yp/homepage/data/nlsi_potts.pdf). Reconstructing that scalar result is not claimed as new.

The conditional-erasure framework is directly related to [Hirche, George, Nuradha and Wilde](https://arxiv.org/html/2608.27171v1). A focused comparison with this and related primary sources did not establish a predecessor for the exact finite-reference formula. That is a limited search outcome, not evidence of first discovery. Existing Volcic machinery is not claimed as new.

## Missing operational step

A sharp conditional Petz/RLD order coefficient does not itself establish a measured-estimation advantage, a capacity improvement, or an experimental protocol with quantified noise tolerance. An operational task needs its own loss function, allowed receiver, optimality proof, and resource accounting. OPERATIONAL_APPENDIX.md separately supplies an internally exact-certified binary-estimation example with an optimal receiver. This does not identify its SLD/MMSE objective with the Petz/RLD coefficient. The recommended compact example includes a certified 1% reference-depolarization model with receivers calibrated for that known noise. Experimental implementation, calibration costs, and broader hardware robustness remain open.

## Plausible consequence

The theorem provides an exact benchmark for dimension-limited quantum side information in a concrete family of classical-channel comparisons. It can guide tests of whether a proposed comparison remains valid when a small quantum memory is retained. Any stronger operational or technological consequence requires a separate argument; this is not a civilization-scale breakthrough claim.

## Decisive next test

Obtain an external expert check of the rank-sensitive lemma, faithful sharpness construction, and prior-work boundary. For an operational extension, externally review the separate exact binary-estimation certificate and test preparation/calibration costs and robustness beyond the specified 1% depolarization model, then compare its dimension dependence with this theorem without identifying the two objectives.

## Reproduce

Use Python 3 with SymPy installed. From any working directory, run:

python /path/to/unpacked/archive/verify_all.py

The runner checks SHA-256 hashes and runs five exact scripts. The scripts locate fixtures relative to their own file paths and never rewrite them. No network access, source PDFs, external accounts, or original research workspace is needed. See CHECKS.md for the exact certificate and test boundaries, and AUDIT.md for the independent mathematical reconstruction. SHA256SUMS covers all package files except itself.
