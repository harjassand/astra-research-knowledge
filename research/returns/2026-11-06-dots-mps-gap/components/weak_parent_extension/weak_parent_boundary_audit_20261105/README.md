# Weak-parent boundary audit: findings and scope

2026-11-05. Internal research deliverable, separate from the preserved proper-parent candidate. No external verification, general completeness theorem, or novelty claim.

## Version 2: conditional GNS identification

The added `STRICT_PRODUCT_REPRESENTATIVE.md` independently proves that the entire fixed-block criterion has the positive range-k representative b=B_k/(k-1), with a strict product open kernel, exact original periodic Hamiltonians, and exact original infinite dynamics. The normalization and boundary counting are checked explicitly. The original open Hamiltonians and finite-level LTI SDPs are **not** identified.

The separate provisional proper-parent periodic/GNS candidate explicitly allows finite interaction range and therefore applies to this representative with D=1. **Conditional on accepting that candidate**, the original-h LTI limit is also the product-state GNS gap for the fixed-block class, including native noncritical PVBS. Its unchanged proof is included as `dependencies/PROPER_PARENT_GNS_CANDIDATE.md`, with source hash in `UPDATE_PROVENANCE.json`. This is not a new independent or externally verified GNS theorem claim.

`PRIORITY_AND_GNS_AUDIT.md` is included unchanged. Its opening sentence about being outside a frozen manifest refers to the earlier version; it is included in this version's manifest. The earlier proof notes remain scoped as originally written; this addendum supplies the conditional GNS interpretation without silently broadening them. Novelty remains unresolved, and all general weak-parent limitations remain in place.

## What survived the adversarial test

1. **A real obstruction to an overbroad proof.** A fully explicit qutrit interaction has unique product bulk, periodic gap exactly 1/5, but an exponentially closing open gap. A weak-parent extension cannot simply assume the uniform open gap used in the proper-parent proof. See `COBOUNDARY_REPAIR.md`, Section 3.
2. **A direct repair for a meaningful class.** If a fixed block of the interaction becomes strictly vacuum-coercive after an onsite coboundary, full local translation invariance bounds endpoint occupations. Resetting only the two endpoint sites gives unrestricted LTI convergence at rate O(n^(-1/2)), without a trace bound or any original open gap. The class includes the adversarial qutrit example and all native finite-species noncritical PVBS models. See `COBOUNDARY_REPAIR.md` and `NATIVE_PVBS_EXTENSION.md`.
3. **An independent boundary-mode construction.** For one-species PVBS, a two-buffer asymmetric channel preserves the inner-cut mode and erases only the outer mode. The entire local-code estimate is explicit, including arbitrary references. It also covers kernel-equivalent deformations and finite tensor-product layers. A naïve reset of both long buffers fails. See `PVBS_EXTENSION.md`.

No counterexample to full unrestricted LTI convergence was found. General gapped weak parents without either a verified boundary repair or the stated coboundary condition remain unresolved here. Periodically gapless examples alone cannot refute convergence: the elementary dual lower bound and periodic upper bounds squeeze the hierarchy to zero whenever the periodic liminf gap is zero.

## Evidence and review

- Exact `Fraction` check of the qutrit projector and positive-square decomposition proving the periodic 1/5 gap.
- Six entire-core operator checks of the endpoint-reset estimate, including arbitrary complex positive vacuum-annihilating interactions.
- Twenty-four whole-code asymmetric-repair checks, twenty finite open spectra, and three complete Kraus-family checks with reset branches.
- Independent full open/periodic qutrit spectra for lengths 3 through 7 and exact trial-energy comparisons.
- Five native multispecies shifted-kernel checks, including repeated anisotropies and random exchange phases.
- A second internal reviewer checked the coefficient identities, sharper boundary-cost constant, source phase conventions, and both proof notes without finding a remaining algebraic gap in the stated unrestricted nearest-neighbor scope. See `LITERATURE_AND_SECOND_REVIEW.md`.
- Three added full-operator representative checks cover normalization on nine rings, exact open boundary weights, local derivation equality, and a case where the shifted two-site term is indefinite although B_3 is positive.

Floating checks are corroboration, not certified SDP solves or substitutes for the algebra. The PVBS spectra and boundary phenomenon are prior art. The qutrit periodic gap is already certified by an elementary onsite potential, so this does not claim a better physical gap estimate or a new high-consequence scientific capability.

## Reproduction

Requires Python, NumPy, and SciPy. Tested with Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. No data downloads are required. Each script resolves its own output directory and can be run from any working directory:

    OPENBLAS_NUM_THREADS=1 python check_pvbs_repair.py
    OPENBLAS_NUM_THREADS=1 python check_coboundary_reset.py
    OPENBLAS_NUM_THREADS=1 python check_boundary_gap_counterexample.py
    OPENBLAS_NUM_THREADS=1 python check_native_pvbs_coboundary.py
    OPENBLAS_NUM_THREADS=1 python check_block_representative.py

They regenerate the corresponding JSON results. The full qutrit spectrum test is the largest computation (a 2187-dimensional dense Hermitian matrix at N=7); it is not needed for the exact symbolic proof. Reproduction changes the elapsed-time field in `pvbs_repair_results.json`, so keep frozen results or run a copy if preserving their hash matters.

`SHA256SUMS` hashes every frozen artifact, including the separately attributed dependency. Run `python verify_packet.py` for manifest verification or `python verify_packet.py --run-tests` to replay all five checks in a temporary copy without changing the frozen results. The previous proper-parent package and the v1 weak-parent ZIP were not edited or replaced.
