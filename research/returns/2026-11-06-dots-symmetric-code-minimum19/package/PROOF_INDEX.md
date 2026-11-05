# Proof and replay index

Certified result: the least length of a rank-two qubit quantum code contained entirely in the fully symmetric subspace, with distance at least five, is 19. The computational certificates and both independent adversarial analytic reviews pass.

This is a minimum-resource theorem for a specified code family. It is not a claim about unrestricted qubit codes, practical memory lifetime, circuit-level thresholds, implementation cost, or a new physical experiment.

## Read first

- TECHNICAL_MODEL.md: physical definition, necessary conditions, proof architecture, resources and source links.
- LITERATURE_PRIORITY_AUDIT.md: final priority assessment. The n>=18 lower bound and19-qubit construction were already known; the proposed new advance is the unrestricted n=18 exclusion, hence exact minimum19. This supersedes preliminary priority comments in early audit logs.
- audit_residual/AUDIT.md: independent mathematical and interval verification, including correction of an exported equality-multiplier orientation.
- audit_second/INDEPENDENT_REVIEW.md: separate analytic derivation, arbitrary-complex full-product-basis checks, and fresh exact interval replay.
- symmetric19_audit/INDEPENDENT_REVIEW.md: separate exact-rational reconstruction of the known19-qubit code.
- audit_positive19/README.md: exact algebraic specification of the published 19-qubit code and the independent verification of its error-correction capability.

## One-command replay

Run `python REPLAY.py` from the extracted package. It checks all lower-bound certificates and the exact19-qubit positive construction, and exits unsuccessfully if a required strict inequality fails. Verification uses NumPy and SymPy, not CVXPY or an optimizer.

## Lower bound

1. Quantum Singleton supplies an elementary exclusion for n<9. This is not claimed as the strongest general-code bound: Rains shadow enumerators already imply n>=11.
2. Exact rational LP duals replay the known intrinsic lower bound excluding n=9,...,17 (Okada already tabulated the corresponding numerical bound). Run:
   `python audit_independent/check_certificates.py`
3. At n=18, the scalar LP plus shadow inequalities remains feasible. `exact_feasible18.json` is an exact rational witness, so the decisive new check is genuinely stronger than that incumbent bound.
4. The three-copy PPT/complement witness excludes n=18. Run from this directory:
   `python audit_residual/verify_interval_dual.py audit_residual/dual_witness_corrected.json`
   Expected status: CERTIFIED EXCLUSION; exact positive margin lower bound whose decimal display is 6.908479009717404e-5.
   This replay uses exact rational factorial Racah coefficients and 192-bit outward-rounded integer intervals. The positive matrices are defined by exact dyadic factor products. No optimizer is used in verification.

## Upper bound

Run:
`python audit_positive19/replay_certificate.py`

Expected: exact rational proof of root existence and uniqueness, all 50 reduced Knill–Laflamme identities, and a nonzero five-site witness proving distance exactly five. The code is credited to Aydin, Alekseyev and Barg, Quantum 8, 1321 (2024), Section7 (codeword ansatzEq31, coefficient systemEq32), https://doi.org/10.22331/q-2024-04-30-1321. The exact root certificate here is an independent reconstruction from their reported example.

## Reproducibility and evidence boundaries

- `requirements.txt` records the isolated construction environment. The no-go verifier needs NumPy; the exact LP checker uses SymPy. The positive-control replay uses only the Python standard library.
- Construction scripts and successful, inaccurate, failed, and sign-corrected logs are retained for provenance. Do not interpret an early failed or inaccurate optimizer status as the proof.
- The final corrected no-go witness SHA256 is 0fec2978c5c7141ea7d119fce811c237dbb817a819c494041d8802bfa1ebdbd9.
- Numerical checks on the actual 19-qubit code independently confirm the lifted/PPT map. They are sanity checks; the algebraic root and rational identities provide its rigorous existence/error-correction certificate.
- Current literature searches found no explicit previous unrestricted minimal-19 proof. Search coverage is not exhaustive; novelty remains a bounded claim pending broader scholarly review.
- General SDP bounds and intrinsic MacWilliams bounds are prior art. The result here is a certified application closing this specific case, not invention of those frameworks.

## Integrity and replay outputs

Check the package manifest or local SHA256SUMS before replay. Some verification scripts regenerate receipt JSON with a fresh elapsed-time field; those generated receipt hashes may therefore change on replay. The frozen witness and verifier source hashes identify the mathematical input and checking program. Keep an untouched package copy if comparing all original file hashes.
