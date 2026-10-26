# Separately labelled post-review batch-coverage repair

The frozen checker accepted an empty results list and a duplicated valid result row while omitting another input. Both failures were reproduced against the unchanged original; raw outputs and corrupt batches are preserved in `regression_results.json` and `original_failure_evidence/`. `original_check_results.py.txt` preserves its source bytes.

`check_results.py` is a repaired copy. Before retaining the original exact per-row certificate/witness checks, it requires a nonempty input batch with unique string IDs, unique result IDs, and exactly equal input/result ID sets. Unknown, missing and duplicate results are rejected; identical or conflicting duplicate input IDs are rejected rather than silently overwritten. Valid result order may differ from input order.

`test_batch_coverage.py` executed ten regressions: valid, valid reordered, empty, omitted, duplicate-with-omission, unknown, duplicate identical input, duplicate conflicting input, invalid certificate/output bound, and invalid channel. All passed. The original two defects reproduced, and the frozen original checker hash matched before and after. No phase1/stage2 source was edited, no researcher was added, and no scientific trial was run.

This fixes checker integration coverage only. It does not alter the frozen policy outcomes, retrospectively count as treatment success, or establish a new scientific result. The original defect remains part of the record; the previously produced per-row certificates were not found false by this repair.

Replay:

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 /Users/harjas/Documents/ChatGPT/coordination/work/astra-method-redesign-20261026/experiments/channel_case/teams/T74/post_review/test_batch_coverage.py
```

Use the repaired checker with the same two input/output arguments as the original.
