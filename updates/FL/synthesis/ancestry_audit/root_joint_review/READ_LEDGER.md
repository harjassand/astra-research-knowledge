# Read ledger and manifest scope

This directory is the **post-isolation review** requested after the initial FL-ancestry audit was frozen. The original frozen audit and its initial manifest remain in place and were not edited. No other FL worker output was opened for this follow-up.

The sole target source read was:

- `work/FL-root/JOINT_ANCESTRY_OPERATION.md`
  - 150 lines, 13,086 bytes
  - SHA-256 at review start: `9dbe8f423d560afa9f3bf726f50d3396789489c36a0d3573f19515cd459f9607`
  - Read via `sed` and `nl -ba` for the complete mathematical and scope review.

After this review was saved, root reported that the reviewed draft had been preserved at `work/FL-root/history/JOINT_ANCESTRY_DRAFT_01.md` and that the main proof was amended. I verified the preserved draft's SHA-256 and byte count against the review-start values; they match exactly. The review and manifest are pinned to that byte-identical historical copy. The amended main proof was not read or audited in this follow-up.

No producer script for that note was supplied in this follow-up; the checker here was recreated independently. It uses only Python's standard library and is not represented as a producer-script replay. No source or capital files were edited. This report applies to the historical draft hash above, not to later edits at the main target path.

Generated review artifacts in this directory:

- `REVIEW.md`: proof review, constants, assumptions, and counterexample.
- `review_checks.py`: independent finite-state and exact-rational checker.
- `check_results.json`: captured checker output, including exact rational results.
- `MANIFEST.sha256`: hashes for the generated files and the byte-identical preserved historical target; this file intentionally does not hash itself.

Validation command:

```text
python3 -m py_compile work/FL-ancestry-audit/root_joint_review/review_checks.py
python3 work/FL-ancestry-audit/root_joint_review/review_checks.py
```

The four-point path-enumeration and pointwise cut checks use floating point with stated tolerances. Generator relations, P/R distributions and transform differences, and the finite time/history counterexample arithmetic use exact rational checks. None of these computations validates isotope chemistry, instrument calibration, producer provenance, external novelty, or physical performance.
