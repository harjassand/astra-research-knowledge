# Original errors and separate reviewer diagnostics

The neutral packets and `owned_Q52`/`owned_Q17` are unchanged. No repairs to original proofs or code were made.

1. **Q52 aggregate source-call undercount.** `archive_science/main/CONSTRUCTION.txt:75` adds only 240,000 for `check_four_query_correction.py`. The script's lines 249–250 also execute 1,000 paired samples, two samplers with four source calls each. Instrumenting every call gives 248,000 for the complete script. Conditional on the stated historical two-block cosine subtotal, the three-experiment total is 1,435,552; including the separately stated null-event check gives 1,435,556. The four-call cap per generated sample and the law bounds are unaffected. The frozen 60,000-sample block report is accurate for that block.

2. **Source-dependent verification work is additional.** The cosine residual certificate uses analytic h, h', K/Hermite coefficients and the known mean in post-fit verification. Those resources are disclosed by the return and accepted for this fixture. They do not become legal arbitrary-source queries by being charged, and four runtime calls are not the full acquisition cost. REVIEW.md accounts for their grids, arithmetic and coefficients explicitly. This is a scope boundary, not a newly found proof error.

3. **Refit variation is preserved.** A fresh unmodified run changes seven dyadic coefficient numerators, by at most 2.42861286636753e−17 in coefficient value. `refit_coefficient_differences.json` preserves the exact differences. The original frozen coefficient file was used for the successful exact certificate. No substitution or repair occurred.

4. **Reviewer-owned numerical failures are not packet failures.** The first independent nonconstant weak-identity test used an over-tight GH192 tolerance; the GH residual converged slowly for this rational integrand. A later NumPy GH384 attempt overflowed its weights. `logs/independent_first_failure.txt` preserves those observations. Integrating the Z polynomial exactly and using independent adaptive G integration resolved the check. These changes affect only the reviewer check, not the packet implementation or mathematics. Initial missing SciPy was resolved by installing it in `review_native/deps`.

No other substantive mathematical error was found in the claims accepted at the exact scopes described in REVIEW.md. This does not accept a general query compiler, unrestricted recursive class closure, generic unknown-CP learner, novelty claim or efficiency advantage.
