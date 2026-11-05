# The model and the complete certificate chain

The theorem concerns a two-dimensional subspace of `Sym^n(C²)` encoding one arbitrary logical qubit, with exact correction of arbitrary errors supported on at most two physical qubits. Equivalently, its rank-two projector detects every physical Pauli operator of weight at most four. No real-amplitude, parity, time-reversal, stabilizer or support ansatz is imposed. The [technical model](package/TECHNICAL_MODEL.md) and [second independent review](package/audit_second/INDEPENDENT_REVIEW.md) explain why taking real parts of relaxed moment blocks does not restrict the underlying arbitrary complex codes.

| Length | Source argument | Evidence boundary |
|---|---|---|
| n < 9 | Quantum Singleton exclusion | An elementary bound; stronger general-code shadow bounds were already known |
| n = 9,…,17 | Exact rational intrinsic MacWilliams LP separators | [Exact LP certificates](package/exact_lp_certificates.json), [independent checker](package/audit_independent/check_certificates.py); the lower bound of 18 is prior art |
| n = 18 | Three-copy moment, permutation, lifted Knill–Laflamme, PPT and complement necessary conditions; rigorous dual contradiction | [Corrected witness](package/audit_residual/dual_witness_corrected.json), [interval certificate](package/audit_residual/interval_certificate.json), [verifier source](package/audit_residual/verify_interval_dual.py) |
| n = 19 | Independent exact algebraic reconstruction of the published construction | [Positive construction guide](package/audit_positive19/README.md), [certificate](package/audit_positive19/positive19_certificate.json), [exact replay source](package/audit_positive19/replay_certificate.py) |

The scalar LP with shadow inequalities is still feasible at 18: [an exact rational feasible point](package/exact_feasible18.json) is preserved. That relaxation's feasibility is not a physical code. The three-copy exclusion uses necessary conditions, so their certified infeasibility suffices for the no-go claim without claiming the relaxation characterizes all codes. Both symmetric and standard S3 multiplicity sectors are retained; the alternating sector vanishes for a rank-two projector. The relaxation is not restricted to the totally symmetric three-copy sector.

The source verifier uses exact rational factorial Racah coefficients and 192-bit outward-rounded integer intervals, with positive dual matrices defined by exact dyadic factor products and residual penalties bounded using trace identities and Gram lower bounds. The recorded strict contradiction margin is greater than `0.0000690847`; the full rational bound is in the certificate. Floating solver status or approximate eigenvalues alone are not the proof.

The governing final witness is `audit_residual/dual_witness_corrected.json`, SHA-256 `0fec2978c5c7141ea7d119fce811c237dbb817a819c494041d8802bfa1ebdbd9`. The source reports that an exported free equality multiplier had the opposite orientation from the verifier convention. Its sign was corrected once, without changing the physical constraints, PSD multipliers or numerical solve. [The independent audit](package/audit_residual/AUDIT.md) records that correction. Earlier raw witnesses, failed/inaccurate runs and diagnostic logs remain historical evidence, rather than final certificate status.

The positive control independently reconstructs the known Aydin–Alekseyev–Barg code: exact root existence and uniqueness, all 50 reduced Knill–Laflamme identities and a nonzero five-site witness giving distance exactly five. The [symmetric-19 review](package/symmetric19_audit/INDEPENDENT_REVIEW.md) and numerical lifted/PPT checks supplement that algebraic construction. The numerical sanity checks do not replace its exact existence proof, and the construction is not claimed as new.

[Review and priority limits](prior-art-costs-and-review.md) · [Return overview](README.md)
