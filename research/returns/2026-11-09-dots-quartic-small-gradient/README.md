# Original quartic small gradient stability

## Conclusion

This archive contains a checked mathematical contribution, not a solution of global quasiconvexity.

For the original unmodified J_r and every r>0, every affine mean has a positive, mean-dependent gradient-supremum radius on which the Jensen inequality holds. The previously difficult full-rank degenerate contacts are included, without restricting the normal component of the compatible perturbation.

The correct term is **Morrey weak quasiconvexity**, or **small-gradient Jensen stability**. Some preserved source filenames use “local quasiconvexity”; that does not mean the stronger existence of a nearby globally quasiconvex extension.

## Why this is worth keeping

The proof eliminates an infinitesimal instability at each fixed mean of the original family and identifies the compatible-gradient estimate that pays the fourth-order angular degeneracy. Its contact-line reserve also applies to a concrete quartic that takes negative values at some matrices.

This is useful proof capital for the original question, with an independently reconstructed all-r acoustic classification and reusable analytic lemma. Its importance is bounded: N806 already supplied much of the contact geometry and harmonic-analysis architecture. No claim of historical novelty or a major advance on Morrey's problem is made.

## Read in this order

1. VALUE_AND_LIMITS.md gives the candid assessment.
2. ASSUMPTIONS_AND_DEPENDENCIES.md states the exact density and theorem contracts.
3. proofs/LOCAL_QC_DEGENERATE_CONTACT.md gives the original-J_r proof.
4. reviews/INDEPENDENT_REVIEW.md independently derives the acoustic classification and checks the full proof.
5. proofs/TYPE_II_SMALL_GRADIENT_LEMMA.md gives the abstract implication with a positive quartic reserve.
6. proofs/CONTACT_LINE_RESERVE.md removes that global positivity requirement at a specified nonzero contact.
7. The two matching review files check those extensions separately.
8. PRIOR_AND_UNCERTAINTY.md compares the strongest prior and records what remains open.

The original-J_r result and the concrete noncoercive contact have complete stated analytic arguments in this archive. Coverage of every nonzero mean of the entire left-SO(2) quartic cone is **conditional on N806's complete algebraic classification**. This archive does not represent that classification as independently re-proved.

## What this does not establish

- Global quasiconvexity of original J_r.
- A radius uniform over all normalized or moving means.
- Arbitrary-amplitude quasiconvexity at zero for a general noncoercive quartic.
- Agreement near a mean with a globally quasiconvex extension.
- An evaluated numerical radius, a finite-bit implementation for arbitrary real inputs, or a practical application.
- Historical novelty.

The source's reported full J_1 positive control was not reconstructed and is not used.

## Integrity and review scope

The mathematical bodies of the proofs and reviews are preserved. Administrative coordination wording has been neutralized in a few delivery copies. PROVENANCE.json records every original and delivered hash and each affected line; no formula, assumption, proof step, numerical constant, or uncertainty qualification was changed. Historical “review pending” statements remain in frozen sources; the final dispositions are in reviews/ and summarized above.

Reviews were independent analytic reconstructions after receipt of the arguments, not blind rediscovery, external peer review, or proof-assistant verification. No scientific computation was performed for these positive results.

From this directory run:

    python3 verify_manifest.py

This checks archive integrity only. It does not prove the mathematics. No third-party Python dependency or network access is required.
