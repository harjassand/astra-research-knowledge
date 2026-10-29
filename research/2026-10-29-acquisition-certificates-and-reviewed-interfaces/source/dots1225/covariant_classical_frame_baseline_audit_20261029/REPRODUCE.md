# Reproduction

With Python3 and NumPy:

```sh
python independent_checks.py
```

This writes `INDEPENDENT_CHECKS.json` without modifying any source snapshots.

Author replay:

```sh
mkdir -p author_replay
cp source_snapshot/*.py author_replay/
python author_replay/check_covariant_estimator.py
python author_replay/check_quadrature.py
```

Compare both generated JSON files with the snapshot versions. Ignore only the estimator's `seconds` field; all other fields matched in this review. `REVIEW_RECEIPT.json` binds the accepted source versions, finite-interface addendum, proofs, code and results by SHA256. The review's analytical bounds are not inferred from the finite diagnostics.
