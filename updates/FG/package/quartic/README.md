# Exact sharp anisotropic quartic theorem

Start with `ASTRA_SHARP_QUARTIC_THEOREM.md`.

The main result is the sharp quasiconvexity/rank-one-convexity threshold for

    F_l = u^2 + v^2 + 4w^2 + (7/2)q^2 + l q(u+v).

The endpoint is the unique root in (2.95,2.96) of

    48 L^6 - 2545 L^4 + 29712 L^2 - 97344 = 0.

This settles the specified one-parameter family, including the previously unresolved l=-29/10 example. It does not settle all left-SO(2) quartics or planar Morrey. Historical novelty and external review are not established.

## Verification

The main verifier is standalone and uses exact arithmetic:

    python verify_sharp_scalar.py

It requires SymPy. The recorded run used Python 3.13.5 and SymPy 1.14.0. No optimizer, network, pickle snapshot, or certificate-input file is needed. The script checks the algebraic endpoint, a positive four-by-four block and zero Schur complement, the full universal polynomial identity for compatible jets, the compact geometric primitive, and the exact rank-one obstruction beyond the endpoint.

For a redundant rational certificate at l=-29/10:

    python verify_explicit.py

The analytic heat-flow and Stokes argument connecting these identities to all compatible gradient oscillations is in the proof note. The proof has not been formalized in a proof assistant.

## Contents

- Main note, standalone verifiers, exact certificate data, and run logs are at the package root.
- `exploration/` preserves exploratory scripts and numerical/symbolic snapshots. Numerical feasibility or infeasibility residuals there are not proof. The final sharp certificate is scalar-only; the earlier tensor certificate is redundant for this slice.
- The exploration scripts may have dependencies on each other, NumPy, SciPy, and saved local state. They are not prerequisites for checking the theorem.
- Pickle snapshots are trusted local research data. Do not load pickle data from an untrusted source. The standalone exact verifiers do not load pickle files.
- `MANIFEST.json` records SHA-256 hashes of all other package files.

The prior heat/exact-form framework is credited to Bruno and Pasqualotto, arXiv:2608.06367v1. No third-party manuscripts are included. No GitHub repository write was performed.
