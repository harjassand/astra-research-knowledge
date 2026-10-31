# Robust reusable operator knowledge — frozen local checkpoint

31 October 2026. This package contains 38 verbatim scientific source files,
three separate source-bound review receipts, reproducible code/results, and
new packaging metadata. It is local only: no publication, upload or external
delivery was performed. Original research files and older archives are unchanged.

## Result and significance

For repeated scalar evaluations of operator words, the package proves and
implements an acquired, task-sensitive representation with a uniform
two-sided residual certificate. Its exact common-contraction bound is

    |error| <= ||b|| ||c|| e_in e_out S_l(alpha),
    S_l(alpha) = sum_(j=0)^(l-2) (l-1-j) alpha^j.

The imperfect-observation extension does not infer exact common stationarity
from data. It separates stochastic observation uncertainty from an acquired
center-family geometry, explicitly stabilizes the small replay and pays its
bias, then executes a certified bounded-integer backend. A capped mixed-norm
bound remains sound even when the learned geometry is not invariant.

A sparse observation frontend selects probes using a paid Bellman upper
envelope, discovers labels, preserves possible unseen-transition mass and
charges all training/validation samples. On one simultaneous confidence event,
the admitted model covers arbitrarily many later adaptive words within its
specified horizon. This concerns the same realized word, not equivalence of
different state-feedback policies.

These are proved ingredients that ordinary retained Krylov, range or spectral
methods can implement. Giving such methods the certificate does not erase
the ingredient's contribution. But quadratic primal/dual output accuracy,
stable reduction and model-based exploration have strong prior antecedents.
`PRIOR_AND_CONTRIBUTION_MAP.md` distinguishes actual prior matches, the precise
formulations derived here and historically unresolved scope. It is a separate
author analysis, not a novelty certification by the reviewers.

**A consequential new computational advantage after all costs remains
unestablished.** Neither a new learner nor historical novelty is claimed.

## Strong comparisons and informative failures

* Ordinary retained methods using the same certificate reduce a 12-state
  imperfect-observation fixture to ranks 4, 5 and 6. All tune their own smallest
  admitted replay precision. All lose after acquisition on the 40-query batch.
* A stronger separately reviewed mixing comparator defeats even that batch's
  apparent online rank advantage. An acquired minorization and checked drift
  admit a constant answer for every length 16--30, with full-center fallback
  for shorter words. All 40 long-word tests use **zero matvecs**. This is a
  fixture failure, not a refutation of the two-sided or mixed-norm theorem.
* The sparse frontier starts with initial label 17 in a billion-label universe
  and acquires seven center states through 84 row updates. It charges
  **15,778,976 logical iid draws**, not merely the fast runtime of aggregate
  multinomial simulation. Its observation bound is 3/32. The composed total
  bound is 0.0938263 at horizon 12 and tolerance 0.1.
* The composed replay stays **full rank seven**. Ordinary retained sparse
  center evaluation already has that graph and is a strong cheaper alternative.
* Full-entry statistical acquisition can dwarf online savings. A deliberately
  conservative sufficient Hoeffding budget at the interval fixture's
  parameters is approximately 4.74 trillion transitions; this is a calculated
  upper budget, not an executed experiment or an optimality claim.
* A routing-tree lower bound requires Omega(K log(1/delta)/epsilon) samples
  for uniformly successful admission even when the null task is identically
  zero. Small task rank alone therefore does not imply cheap acquisition;
  lazy admission for only requested tasks remains a legitimate strong baseline.

Read `finite_observation/COSTS_AND_FAILURES.md` alongside the later
`MIXING_BASELINE.md`; the former's timing table is not the final strongest
comparison. Construction, per-candidate verification, coefficient/state bits,
retained payloads, unsuccessful acquisitions and observation counts are
separated. Acquisition wall time includes exact arithmetic, but individual
peak intermediate bit operations are not fully instrumented.

## Review map — no blanket review claim

All science is under `science/robust_operator_reuse_20261031/`.

1. `INDEPENDENT_FOUNDATIONAL_REVIEW.md` binds the exact-input proofs, code and
   results. SHA-256:
   `99002fc47fd05426c3a2fa070150026bac53d72e6b5541ead2c52e28d2107e2e`.
   It reran 167 author assertions and passed 150 additional independent checks.
2. `finite_observation/INDEPENDENT_REVIEW.md` separately binds the imperfect-
   observation, sparse-frontier and composition sources. SHA-256:
   `a44d83e191b360e2ef7222a3ce5a145f4fe6ab023fd4f17a7c81db2b4d3db6c0`.
   It reran 501, 4,124 and 35 author checks and passed 415 additional checks.
3. `finite_observation/MIXING_BASELINE_INDEPENDENT_REVIEW.md` is a later,
   separate review, NOT coverage retroactively supplied by the second receipt.
   SHA-256:
   `da29db6666b3496f254d4da3756710d8687d7dceb09178b197351187c61bb5c6`.
   It reran the 240-check mixing comparator.

Contextual cost and prior-analysis notes and this package wrapper are not
claimed independently reviewed. Original author proof headers are preserved;
the exact source-bound receipts determine their later review status.

The finite code imports exact helpers from the included `learn.py` and strict
matrix decoding from the included `verify.py`. Those dependencies are retained
with their original hashes, not silently copied into a different implementation.

## Receiving scope

True row-stochasticity is the generative model class; no code authenticates
real-world model truth or that deterministic enclosures contain physical truth.
Statistical validity requires nonanticipating row/support/batch-size selection
and fresh conditionally iid validation. A transcript verifier checks algebra,
not timing/provenance, and is not a confidence-sequence validator for optional
stopping. The emitted acquisition fixes its design before validation.

The sparse executable's `risk/2` is for terminal task range width at most one.
The general proof multiplies by `osc(b)`; a wider-range task cannot omit that
factor. Horizons, tolerances, task vectors, coefficient rounding, replay
rounding and observation contracts must retain their stated bindings. No
unbounded-horizon, drifting-law or unrestricted new-observable guarantee follows.

## Verify and reproduce without changing frozen files

From this package directory:

```
sha256sum -c SHA256SUMS
python -B REPRODUCE.py
```

`REPRODUCE.py` creates a temporary copy before running anything, including the
independent exact script that writes beside its own copied source. It never
updates these frozen files. It prints invariant test counts, and checks the
current saved certificates using included dependencies. NumPy 2.3.5 and SymPy
1.14.0 were already available; no software installation was performed.

`ALLOWLIST.txt` names the 38 verbatim scientific originals; `MANIFEST.json`
records their bytes and SHA-256 values. `SHA256SUMS` covers those and the new
package metadata except itself. `VALIDATION_REPORT.json` records this packaging
run's reproduction and source/archive preservation checks. ZIP CRC, clean
extraction and every manifest entry were checked locally.

Caches, duplicate logs, preliminary `initial_trial.json`, old subset manifests,
old archives and unrelated administrative/private files are excluded. Primary
research links are in the preserved proofs and prior-contribution note.
