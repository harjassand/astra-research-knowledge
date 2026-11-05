# LTI exact value counterexamples

5 November 2026

This standalone packet proves an exact obstruction to gap-value convergence of the finite-cutoff H-squared/LTI hierarchy. The original Rai Eq. (17) has value **1 at every finite level** for the Ising projector chain, while its periodic gap is **2**. An explicitly defined rectangular analogue has the same plateau for the toric code. Matching primal and dual witnesses establish the values analytically.

**Only exact-value convergence fails in these examples. Positive-gap detection does not fail.** No novelty, priority, external peer review, or improvement over existing numerical gap bounds is claimed. The periodic and specified vacuum-GNS gaps are standard. No SDP was solved.

## Read the packet

1. PROOF.md gives the precise original 1D program, the complete Ising proof, a general separated-defect lemma, the explicit rectangular toric program and proof, and all scope qualifications.
2. SOURCE_SCOPE.md records the exact Rai equation and periodic-gap convention, source locations, prior-art boundaries, and source provenance.
3. audits/toric_local/REPORT.md gives one independent internal audit, including an explicit positive toric finite-window operator and a support lemma proving full local translation invariance.
4. audits/ising_and_toric/INDEPENDENT_REVIEW.md gives a second independent internal audit, including direct Ising and toric witnesses, spectral normalization, primary-source checks, and exact finite-dimensional tests.
5. REPRODUCED_CHECKS.json records the packaging rerun. MANIFEST.sha256.json records the packet file hashes. verify.py checks the manifest and reproduces both computational audits in temporary directories.

The two original audit reports and scripts are copied byte-for-byte. The second audit uses the alternative grouping

    h_r = Q^A_(r+(1,1)) + Q^B_r,

whose support is a 2-by-2 cell patch. The main proof and first audit use

    h_r = Q^A_r + Q^B_r,

whose support fits a 3-by-3 cell patch. These groupings have the same global toric Hamiltonian, but their finite-window generators are not identified term by term. Both independently have the exact plateau 1. The common stabilizer-window checks concern every contained generator; the main proof uses windows large enough to contain every requested h_r.

## Reproduce the checks

Requirements: Python 3.10 or later and NumPy. Packaging was tested with Python 3.12.14 and NumPy 2.3.5. There are no network calls, optimization solvers, proprietary data, external repository paths, or trained models.

From the extracted packet directory, run:

    python verify.py

The verifier first checks all recorded file hashes, then copies each audit to a fresh temporary directory and runs its script there. It compares the first script's exact text output and the second script's complete JSON result with the recorded originals, ignoring only elapsed runtime. It leaves the packet unchanged and prints a JSON verification report. To save that report outside the packet, use:

    python verify.py --report /path/to/verification.json

The scripts can also be run directly:

    python audits/toric_local/check_lti.py
    python audits/ising_and_toric/check_explicit_witnesses.py

The second direct command rewrites its adjacent results.json, including a new runtime. Use the verifier if preserving the recorded manifest is important.

## What is actually tested

- Exact Ising full marginal equality, local normalization, and zero distinct-pair products for n=3 through 12.
- Three translation-averaged Ising torus witnesses.
- Exact toric Pauli-coefficient equalities for all translated subrectangles in five windows through 3-by-4 and 4-by-3 cells.
- A separate full opposite-face Pauli-expansion audit through 4-by-4 cells, with boundary-subgroup rank checks through 5-by-7 and 8-by-6 cells.
- An actual 256-dimensional integer density numerator, checked by an exact projector polynomial.
- Three toric torus syndrome constructions with exact rank, nonempty syndrome space, defect separation, and normalization checks.

The finite checks use integer and rational arithmetic for the claims they test; NumPy supplies integer arrays and matrix multiplication. They are sanity checks of the analytic all-level constructions, not a numerical extrapolation or a certified SDP computation. Their cost is far below storing or solving the full higher-level SDP, so they are not an SDP scalability benchmark.

## Integrity and boundaries

The packet is self-contained for reading the proofs and running the checks. Online primary sources are linked rather than republished in full. A clean extraction was tested without relying on files in the original workspace. The separately scoped proper-MPS, strict-product, and finite-depth-circuit candidates are not included, modified, or invalidated by this packet.

The missing operation in a proposed universal value-completeness extension is now explicit: a fixed-distance H-squared truncation loses the cross energy of arbitrarily separated defect pairs. Full LTI constraints cannot recover terms that the truncation discarded, even when the witness is the restriction of a genuine larger-system state. A different method would need additional information; this packet does not claim to supply it.
