# Replay and relocation

This is a mathematical proof audit, not a production numerical receiver.

1. Run `python verify_saved_audit.py` for read-only audit and four-file original-source hash/byte verification.
2. COPY this entire audit directory before rerunning either check script, because they write adjacent deterministic JSON output.
3. In the copy, run `python independent_harmonic_checks.py`. It uses Python standard library plus the already installed SymPy, imports no author code, and uses exact rational/symbolic arithmetic. Compare both generated JSON files byte-for-byte with the saved ones.
4. Run `python author_replay/check_harmonic_service.py` in the copy. Its CHECK_RESULTS.json must match inputs/CHECK_RESULTS.json exactly. Author checks are not counted as independent checks.

The verifier defaults to the original source directory one level above this audit. For relocation use `--source-dir /path/to/rate2_explicit_macro_removal`. No other theorem or scalar source is required by this service's proof. Replacement consumer joins have their own receipts and are not implied here.

`check_history_v0` preserves an incomplete audit-harness run with an inexact integer-division expression. It is not an accepted checker. The final exact implementation and full rerun control.

Do not edit originals, replace historical bytes, or regenerate a manifest over modified payloads and call it the same acceptance. The manifest SHA is an external immutable binding.
