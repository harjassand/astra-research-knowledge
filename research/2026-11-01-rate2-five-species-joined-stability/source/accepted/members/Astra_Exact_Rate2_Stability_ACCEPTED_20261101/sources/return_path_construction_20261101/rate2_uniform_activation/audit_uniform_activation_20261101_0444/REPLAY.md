# Replay and relocation

This is a proof-component audit, not a production stochastic or numerical API.

- `python verify_saved_audit.py` performs read-only audit/source/dependency hash verification.
- COPY the audit directory before replaying either checker: they write adjacent deterministic reports.
- In the copy, `python independent_activation_checks.py` uses only the Python standard library. Its two JSON outputs should be byte-identical to the saved ones. There are no timing fields.
- In the copy, `python author_replay/check_activation.py` requires SymPy (already present for the actual audit run). Compare its CHECK_RESULTS.json byte-for-byte with inputs/CHECK_RESULTS.json. Those author counts are not independent-audit counts.
- The verifier defaults to the original activation source directory one level above this audit. For a relocated extracted package, pass `--source-dir /path/to/rate2_uniform_activation`; the accepted initial-growth directory and its exact audit gate must be its sibling at the recorded layout.

The manifest binds all audit payloads, the four original activation source files, and the four exact original initial-growth dependency/gate files. The saved dependency_readback.stdout also records the full accepted initial-growth gate's 19-payload/4-source readback. Package the full earlier gate if independent replay of that gate is desired; this audit does not fabricate missing historical payloads from a receipt alone.

Do not regenerate the manifest over modified files and represent that as the same acceptance. The final manifest SHA is the external immutable binding. No source or previous archive is to be edited.
