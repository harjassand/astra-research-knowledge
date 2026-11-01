# Robust kinetics source-bound theorem receipt

**PASS, theorem-only, with no source correction required.**

- Main theorem: `LOCALIZED_DENSITY_ENVELOPE_CANDIDATE.md`, SHA-256 `cb68b2f121f89e2553b4f6330dee2b60ae185309b715491fe4ec487cac7b5366`.
- Separate generic note: `GENERAL_ENVELOPE_CONSERVATIVITY_NOTE.md`, SHA-256 `7a30632dc9f42e5eaaa8a16c0e26ce93cd72ff8611fd9faca929d23cc053bbfc`.
- Author manifest: SHA-256 `ee3dd448fccfe85cf42742b681c8a72cf41aff7ecb2b5787868fc44f7c5f2663`, 5735 bytes; all 18 file and 13 dependency byte bindings independently match. Manifest binding is not code acceptance.

## Accepted proof

1. Actual nonfactorized fixed-member constant-mobility diffusion is global, reversible and has finite Gibbs mass. The declared full **actual-member** Gibbs|A initialization is retained.
2. Nominal **upper-density source** currents can be priced against the **lower density** to bound actual inverse forms. This comparison is independently derived, not inherited from the unreviewed root sketch.
3. All homogeneous squared-density/mixture prices, the strict `e<kappa` premise, the exact localized slab resistance, and complete non-slab/S/tail costs are valid. No false pointwise density-ratio or actual-source substitution occurs.
4. Actual mean lower/upper bounds, the independent cross-source join, and the conservative mass-lower-bound spectral reference `k0=C0/M_b` are sound. The latter is checked directly rather than treating M_b as the actual mass.
5. The localized asymptotic condition is exactly `e<7 kappa²/(16+23 kappa)`; it suppresses both non-slab and separate-S costs. Whole-domain dominated convergence gives the stated O(e/kappa) limiting sufficient defect. This is not a finite-tolerance or actual-error identity.
6. The generic C2 global-envelope note is valid for its finite constant SPD block mobility. The finite-mass form cutoff, local-domain identification with the **minimal** SDE, and positive-time density/Markov argument together establish every-start nonexplosion, not merely a formal conservative operator or an almost-everywhere law.

`DERIVATION_REVIEW.md` contains the complete challenge, including core/infinity details, positive homotopy cross terms, unknown normalizer cancellation, actual initial-law distinctions and the unbounded-mobility Brownian/atan counterexample.

## Checks and preservation

**1,095 independent exact assertions passed**, without importing candidate code. A first symbolic check lacked the strict parameter assumption needed to choose a radical branch; its failure and original script are preserved. The corrected check verifies the squared rational identity under positivity established in the proof and admitted fixtures. This was not a source defect.

All frozen inputs are unchanged; snapshots, input hashes, exact results, freeze-binding results and the new receipt are covered by `AUDIT_SHA256.json`. No prior artifact was overwritten.

## Exclusions

No executable, finite numerical interval/KS value, budget, hardware, empirical model calibration or physical preparation accepted. The actual-member full Gibbs|A law remains a premise. The generic smooth-envelope theorem does not enlarge the concrete fixed-atom parser or acquire global inequalities from finite local probes. State-dependent/unbounded/cross mobility and nonreversibility remain outside the generic note. No relative extreme-tail, exponential-moment, arbitrary-start hitting-law, finite-bit mean-stability, asymptotic finite-accuracy or historical-priority conclusion is accepted.
