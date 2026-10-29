# Reproduction

From this directory, with Python3, NumPy and SymPy installed:

```sh
python independent_checks.py
```

This writes `INDEPENDENT_CHECKS.json`. It reads but does not modify `source_snapshot/exact_schedule.json`.

The author scripts can be replayed without touching the frozen snapshots:

```sh
mkdir -p author_replay
cp source_snapshot/*.py author_replay/
python author_replay/check_history_bounds.py
python author_replay/check_dense_transitions.py
python author_replay/exact_schedule.py
```

Compare the three generated JSON files against the same filenames in `source_snapshot/`. Exact JSON equality was verified in this review. These computations are rational/symbolic or floating matrix diagnostics, not physical quantum executions. The proof and acceptance scope are in `REVIEW.md`; `REVIEW_RECEIPT.json` binds the accepted sources and evidence by SHA256.
