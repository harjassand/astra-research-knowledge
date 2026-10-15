# Direction-rigidity worker: frozen continuation

Date: 2026-10-15. Worker: /root/nonlocal_compensation, third-wave output owned by direction_rigidity. Mathematical originality UNKNOWN. All source files and the repository were read only; no commit, upload or publication was performed.

## Completed core

SCALAR_EULER_SCHUR_COUNTERMODEL.md is the frozen full-elimination theorem and proof. It supplies a left-SO(2)-invariant globally rank-one convex quartic G and a genuine global first-row scalar minimizer on the affine-periodic rectangle [0,8 pi] x [0,1], with both scalar Hessian blocks uniformly elliptic, for which the actual reduced energy is strictly midpoint nonconvex. The compatible perturbation keeps every quartic term. Its exact energy decrease is less than -1/200000. This disproves a universal nonnegative Schur conclusion from scalar Euler, full acoustic rank-one convexity and the two positive scalar blocks.

This is not a negative quasiconvexity test. The unperturbed affine Jensen gap is 575/384; the entire explicit two-zone trial family has gap at least 62387/41664 for every period and scale. A whole-cell scalar-stress residual further proves that the fully row-minimized two selected endpoints have gap at least 527/384. Thus the countermodel proves failure of reduced convexity while retaining a positive global comparison at these endpoints. Its base is first-row stationary but not full-vector stationary, so it does not contradict the incoming many-center radial/full-Euler equivalence.

Core files, immutable after the initial freeze:

- SCALAR_EULER_SCHUR_COUNTERMODEL.md
- verify_scalar_schur_countermodel.py
- exact_countermodel_checks.json

The exact checker passed seven groups; the analytic optimality, nonconvexity, all-scale positive bound, and full endpoint minimization bound are proved in the report. The hash manifest preserves the original frozen hashes.

## Completed separate prior-transfer investigation

ISOTROPIC_TRANSFER_OBSTRUCTION.md proves that G is outside the coefficient-closed positive cone generated jointly by every right-GL transform of every left-and-right-SO(2)-invariant rank-one convex homogeneous quartic, every right-GL transform of the specified Fstar, and arbitrary homogeneous polyconvex quartics with no symmetry requirement.

The new step classifies the target acoustic-zero face of the full transformed isotropic family: every atom on that face is explicitly a convex fourth power plus a nonnegative determinant square. A strictly positive acoustic trace normalizes the entire nine-dimensional ROC cone; closed parameter bounds give a compact isotropic family. Weighted acoustic-null concentration, combined with the prior lifted finite Jensen functional, excludes coefficient-limit positive sums. Singular right-transform limits and degenerate isotropic generators are included.

The Fstar-only positive-cone exclusion was already proved in pinned repository updates/FO/synthesis/profile_prior/cone_followup/REPORT.md. It is credited as prior work. Bruno--Pasqualotto Theorem 2 establishes quasiconvexity of the isotropic generator class; that theorem is not a new result here and is not needed for the exclusion proof itself. This investigation blocks positive transfer and does not settle G quasiconvexity.

Separate files:

- ISOTROPIC_TRANSFER_OBSTRUCTION.md
- verify_isotropic_transfer.py
- exact_isotropic_transfer_checks.json

The standalone exact checker passes eight groups, including the prior Fstar strict acoustic Gram and the target G rank-six Gram. These algebra checks support the supplied analytic compactness proof; they are not a finite search extrapolation.

## Explicit unresolved obligation

Prove a nonconvex global comparison for the fully scalar-minimized energy at every affine-periodic second component, or construct one exact continuous compatible field whose affine Jensen gap is negative. Requiring the reduced energy to be convex or its Schur Hessian to be globally nonnegative is invalid by the frozen core theorem. Positive synthesis from the stated isotropic/Fstar/polyconvex generators is also excluded. A new heat/closed-form certificate is outside both obstructions and could still prove G quasiconvexity.

No more search along the frozen two-zone construction is warranted: the all-scale trial bound and actual endpoint-minimum bound quantify its positive gap. No general negative compatible witness, universal lower bound, or full quartic Morrey implication has been obtained.

## Review status and provenance

Complete proofs were sent to the parent and /root/adversarial_proof_review. At this checkpoint, any internal-review conclusion should be recorded separately and must not be represented as external mathematical or priority review. A correction, if required, should be appended in a new file rather than silently altering the frozen core.

Repository pin: b7cada92d2eb304578be5ed974f1e44b10a89928 at /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015.

Source hashes, file sizes and measured replay costs are in MANIFEST.json and REPLAY_RECEIPT.json. Computation used local exact SymPy arithmetic; no optimization service, data acquisition or physical experiment was used. Pure inference time, aggregate tokens and bit-operation count were not independently metered.
