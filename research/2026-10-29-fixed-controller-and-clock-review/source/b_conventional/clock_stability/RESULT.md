# Result: a parameter-qualified local stability transfer

The remaining physical-local perturbation gate has an analytical closing
route, beyond the earlier endpoint-gap/path result. The construction is
fully written in `PROOF.md`; it introduces no finite controls or new code
level and leaves all frozen clock sources unchanged.

For the source-qualified spatial RX/RZ family, choose a sufficiently small
positive constant

    lambda<=min(lambda_*,rho/2,1/(2 Cmart)),
    Delta=1/(4lambda^L), L=8.

Both constants remain independent of system size. For each such fixed
choice, sufficiently weak arbitrary bounded-range physical Hermitian
perturbations leave the logical ground band and a uniform positive gap.
The splitting is bounded by N times a rapidly decaying function of a
positive power of source distance. No bare-check symmetry is required of
the physical perturbation.

The proof uses two constructive missing interfaces:

1. Exact common spectral flow within each conserved syndrome maps its
   unique clock ground state to vacuum. A CP martingale then decomposes
   the remaining weak terms into local Hermitian vacuum-annihilating
   terms. Allocating part of the large clock penalty makes an EXACT
   frustration-free comparison interaction. Its local projectors are the
   bare-code-plus-clock-vacuum projectors, with uniform local gap >=3/4.
2. A polynomial-radius buffer is sufficient in the ordinary FF BHM
   argument: a globally block-diagonal quasilocal term can be localized
   against those enlarged projectors with cost proportional to
   sum_r |B_F(r)| tail(r). Polynomial F and rapid spatial tails make this
   finite. This pays the actual check-soundness consequence without
   claiming strict spatial TQO-2 or a support-volume spectral-flow norm.

The literal old compiled lambda_* has NOT been compared numerically with
the new Cmart gate. A smaller constant may be required, with an even
larger penalty. The theorem is not a practical threshold, two-body-qubit
conversion, finite-temperature lifetime, or hardware qualification.
It also does not cover arbitrary nonspatial k-local perturbations.

Ordinary spectral flow, quasi-local map estimates, positive local comparison
and the BHM strategy are explicitly credited in `PRIOR_AND_COST.md`.
Priority is UNKNOWN; no computational or physical advantage is asserted.

Internal intake: root WHOLE-read the governing proof, both new elementary
lemmas, the primary-filter/sectorwise scope, unmerged marked-hop energy
tail, and the explicit quasilocal-initial-term radius summation in Section8a.
Its analytical verdict is ACCEPTED at the parameter-qualified mathematical
scope. This is a completed substantive internal review, not an acceptance
of an unexecuted numerical clock threshold or a physical implementation.
