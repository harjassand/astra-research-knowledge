# Geometric mechanism investigation: closed without a discovery claim

Date: 2026-10-10.

No genuinely new dimension-free mechanism or finite-cost universal sampler survived this pass. The proposed inverse-conditional-variance chord inequality remains unproved. Its Gaussian tests are exact, its sharp constant-one version fails on a disk, and cube padding retains the full ordinary Poincare obstruction. Treating inverse short-chord compensation as a free clock change is invalid: the stationary mean event rate is already infinite on a square.

## Read first

- `CANDIDATES_AND_SCOPE.md`: initial mechanisms, exact obligation, current KLS status and stopping boundary
- `EXACT_OBSTRUCTIONS.md`: complete elementary proofs, including the isotropic simplex and random-scan two-block ball examples
- `normalized_chord_tests/normalized_chord_analysis.md`: anisotropic Gaussian proof, exact disk counterexample, general padding theorem and precise clock limitation
- `PRIMARY_SOURCE_CHECK.md`: four targeted primary sources with submission/revision dates; no audit or independent validation of recent KLS claims

## Reproduce

From this directory:

    python verify_native_obstructions.py
    python normalized_chord_tests/ball_exact_tests.py

Dependencies present at verification: NumPy 2.3.5, SymPy 1.14.0, and SciPy. The first script verifies exact symbolic identities and records seeded Monte Carlo cross-checks; simulations are not the proofs. The second computes exact rational disk moments and floating-point polynomial-subspace eigenvalues.

`normalized_chord_tests/product_exponential_test.py` and its output preserve an exploratory calculation that was unstable in some regimes. They are explicitly excluded from all conclusions; the rigorous padding theorem replaces that exploratory route.

## Two important scope distinctions

1. The ball example uses random scan, \(P=(P_X+P_Y)/2\), not a deterministic alternating sweep.
2. Infinite stationary expected rate does not itself prove pathwise explosion or failure of the analytic Dirichlet form. It blocks an automatic finite-expected-work sampling claim.

The SHA-256 inventory covers all substantive files. No paid computation, publication, push, external contact or physical experiment was performed.
