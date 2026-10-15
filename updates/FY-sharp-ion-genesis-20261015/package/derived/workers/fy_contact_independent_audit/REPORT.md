# Independent contact and projection audit

15 October 2026. Status: **PASS_INTERNAL_MATHEMATICAL_AUDIT**.
External correctness, formal verification, and historical originality
remain UNKNOWN.

For every finite real t!=0, write n=1+t2, L=tw-j+v and
F=alpha H+kL2+ell v(j-2L/n)+m v2 at the contact
R=(t,1) tensor e1. Some finite alpha gives global ROC iff some finite
alpha gives all-background QC iff

* k=ell=0 and m>=0; or
* 2m>|ell| and
  Delta=k n2(2m-ell)(2m+ell)-ell2[t2(2m+ell)+3(2m-ell)]>0.

The forced determinant support is lambda=3ell. Every non-convex singular
weak boundary has an actual rank-one acoustic zero with nonzero background
derivative, independent of alpha. The ell=0 square-only boundary and the
ell!=0 determinant boundary are both treated. The trace-free t=0 sharp
examples are explicitly preserved.

This theorem was reconstructed before reading the constructor's new proof.
The subsequent proof and implementation comparison found no mathematical
defect. The independently checked supplementary cost family requires
alpha>=1/(32eta)+13/80+47eta/200 and has a sufficient alpha of order 1/eta.

With the pinned N872 shear and N873 parallel-contact existence theorems
as inherited premises, the exhaustive contact normalization and independent
strict-conformal completion proof yield equality of the full existential
H projections: pi_H(ROC intersect V)=pi_H(QC intersect V) for the full
nine-dimensional invariant space V. The quotient has dimension eight.
This does not decide QC at the originally supplied alpha or the positive
sharp fixed-alpha J_r question.

The analytic test contract is every bounded planar Lipschitz domain, every
real affine background, and every vector W0^(1,4) perturbation, plus the
periodic analogue. Each completion uses one finite coefficient independent
of all those tests.

Artifacts:

* `INDEPENDENT_DERIVATION.md`: independent theorem and all boundary proofs.
* `STRICT_CONFORMAL_COMPLETION.md`: direct strict branch with sufficient
  coefficient 25144M2/delta+(9391/4)M.
* `FULL_PROJECTION_AUDIT.md`: constructor comparison, exact inheritance,
  normalization, full composition, and coefficient-cost addendum.
* `verify_independent.py` and `EXACT_IDENTITIES.json`: 31 passing exact
  identity groups, supporting the separately written universal proofs.
* `AUDIT_RECEIPT.json`: input and final artifact hashes and reading scope.

No protected checkout, source, or Git content was modified.
