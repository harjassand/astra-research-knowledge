# nonlinear_qc continuation and handoff

Date: 15 October 2026. Source repository pin:
`b7cada92d2eb304578be5ed974f1e44b10a89928`.

## Achieved internally

The particular retained non-polyconvex quartic G is quasiconvex at every affine
background, including all nonlinear compatible perturbations. The result is
not restricted to a prescribed phase, a scalar component solve or finitely
many Fourier modes.

Load-bearing files:

1. `G_EXACT_HEAT_CERTIFICATE.json`, SHA-256
   `4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000`.
   Exact diffusion diag(4897/5000,5103/5000); rational full closed quadratic
   two-form; rational PSD 24x24 Gram factored through a rational 24x18 basis
   and a positive definite 18x18 reduced Gram. All 18 exact LDL pivots positive.
2. `verify_G_heat.py`: standalone verifier, no acquisition helper or numerical
   candidate import. Seven exact groups passed, including the complete
   compatible-jet polynomial identity, closedness and global primitive.
3. `G_QUASICONVEXITY_PROOF.md`: complete analytic anisotropic-heat proof, including
   zero correction integral, all affine backgrounds, the zero-time/infinite-time
   limits, W0^(1,4) density and periodic version. Also gives exact nonpolyconvexity
   and the absence of a strict subtraction margin.
4. `SOFT_COMPENSATION_COROLLARY.md`: closes the previously unresolved compatible
   cubic-plus-quartic sign for this G. If P=<v_xx^2>,
   T=<v_xy(9v_xx^2+4v_xy^2)> and D=<K(v_xx,v_xy,v_yy)>, then
   D>=0 and T^2<=(8748/5) P D. The full v_yy dependence is retained.

Root independently checked the portable certificate with a separate
Fraction-based implementation and reconstructed the analytic heat implication.
The `adversarial_proof_review` worker separately checked the certificate and
reconstructed the all-background W0^(1,4) proof from the JSON without reading
the authored proof first; its reported verdict found no critical gap. These
are independent same-team checks, not external mathematical validation.

Final audit artifacts read in full:
`../adversarial_operation/G_HEAT_REVIEW.md` reconstructs the certificate,
nonpolyconvexity and complete analytic all-background proof; and
`../adversarial_operation/ORBIT_AND_SOFT_REVIEW.md`, Sections 1-2, reconstructs
the full soft-action consequence and the entire isotropic orbit separator.
Both report no critical gap in these exact scopes. Root also independently
reconstructed the isotropic compact-face proof. Snapshot hashes and precise
review boundaries are recorded in `REVIEW_RECEIPTS.json`.

## Comparison with prior generators

`DM_ORBIT_SEPARATOR.md` proves G is outside the coefficientwise closed positive
input-GL2 orbit cone of all Dacorogna-Marcellini energies in their rank-one-convex
range plus arbitrary homogeneous polyconvex quartics.

`ISOTROPIC_ORBIT_SEPARATOR.md` strengthens this to the entire both-left-and-right
rotational homogeneous quartic class. The compactification uses the exact
necessary bounds a>=0, |b|<=4a, c>=-8a+3|b| for
F=a|A|^4+b|A|^2 det A+c(det A)^2, and the polyconvex decomposition at c>=4a.
The shear-null generator pullbacks are convex, including the |b|=4a endpoint.
Bounded orbit mass and G's exact negative lifted-barycenter law separate the
closed positive cone. No numerical conic infeasibility premise is used.

`verify_orbit_and_soft.py` passed five exact finite groups. Compactness and
the analytic cone separation have their complete proof in the notes and are
not certified merely by the checker. The initial algebra check corrected an
intermediate diagonal-curvature coefficient to 16a, yielding the stronger bound
c>=-8a+3|b|; no incorrect coefficient remains in the final proof.

## Discovery record, dispensable for proof

`search_complex_diffusion.py` explored the complete homogeneous-quadratic closed
two-form space with bilinear Gram certificates and positive real input diffusion,
also permitting a rotating target-diffusion term. Exact acoustic zeros supplied
an initial three-dimensional Gram null span. A rational candidate face from a
numerical dual exposure reduced the Gram to dimension 18. The positive reduced
margin then allowed exact affine rationalization.

The accepted certificate has zero rotating diffusion. The exploration is not
claimed as invention of the general heat/exact-form method. The necessity of
the heuristic extra null restriction is not a proof premise; the final rational
identity and PSD factor stand alone.

The `.npz` candidates and numerical search JSON files are acquisition history
only. `acquire_exact_G_heat.py` uses rounded numerical entries exclusively to
select free variables of an exact affine solution, then accepts only exact
closedness, exact identity, positive diffusion and positive LDL pivots. No
floating eigenvalue or rounded singular Gram certifies the theorem.

## What remains open

* Quasiconvexity of the entire nine-coefficient left-SO(2)-invariant rank-one-convex
  quartic cone and the general planar Morrey implication.
* Historical novelty and external specialist review of the specific G result
  and orbit-separation applications.
* Any quantitative global Jensen gap beyond the proved nonnegative gap.

G has an exact acoustic zero at (I,e12), so G-epsilon|A|^4 fails rank-one convexity
for every epsilon>0. Do not import the strict Fstar margin or its strong-critical
storage consequences without new hypotheses.

The previous fixed-phase and reduced-functional nonconvexity obstructions remain
valid. Quasiconvexity of G does not imply convexity of its phase or Cartesian
reduced values at nonaffine data. No negative compatible G witness exists under
the theorem's hypotheses; the finite negative nonpolyconvexity law is not a
gradient law.

## Verification commands

    python3 verify_G_heat.py
    python3 verify_orbit_and_soft.py

No search rerun is needed for verification. All outputs are confined to this
worker directory. No source bytes, repository file or old research artifact
were modified; no commit or external scientific promotion was performed.

Final status: complete and frozen for parent integration. No more search or
proof expansion is running. The manifest pins the finished proof and discovery
history separately from the same-team review snapshots.
