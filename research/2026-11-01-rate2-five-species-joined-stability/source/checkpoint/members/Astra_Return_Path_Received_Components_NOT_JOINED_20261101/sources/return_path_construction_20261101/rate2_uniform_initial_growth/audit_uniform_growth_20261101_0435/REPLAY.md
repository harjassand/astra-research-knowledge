# Replay and immutability

This audit is a mathematical component review, not a production numerical receiver. No external packages are required; Python standard library only. The independent checker does not import author code.

1. Run `python verify_saved_audit.py` in the saved audit directory for read-only payload and original-source readback.
2. COPY this entire directory to a fresh path before any replay. Both checker scripts write their own adjacent JSON result.
3. In that copy, run `python independent_initial_growth_checks.py`. Compare its INDEPENDENT_CHECK_RESULTS.json with the saved file; the result is deterministic and has no timing field.
4. In the copy, run `python author_replay/check_initial_growth.py`. Compare author_replay/CHECK_RESULTS.json with inputs/CHECK_RESULTS.json. The report must match exactly; author counts are not independent-audit counts.

The read-only verifier defaults to the original source directory one level above this audit. For a relocated extracted package, use `python verify_saved_audit.py --source-dir /path/to/rate2_uniform_initial_growth`. Only the four named original files are read; no broad directory traversal or trusted cache is used. Historical checker output and original snapshots remain exact.

Do not regenerate AUDIT_SHA256.json over a changed artifact and call it the same acceptance. The final manifest hash is an external binding. No permission to edit originals or any other accepted archive is conveyed.
