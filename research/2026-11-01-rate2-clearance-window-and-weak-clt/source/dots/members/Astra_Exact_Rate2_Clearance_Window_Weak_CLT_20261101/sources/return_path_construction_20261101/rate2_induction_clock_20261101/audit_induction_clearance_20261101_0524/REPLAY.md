# Replay, source layout, and numerical gate

This is a mathematical audit, not a production numerical receiver. Original author files and earlier audits are immutable.

- `python verify_saved_audit.py` performs read-only hash/byte readback of the audit payloads, eight original component files, and all pinned original dependency files. For relocation, supply `--workspace-root /path/to/extracted/root`; the original sibling directory names recorded in INPUT_BINDINGS.json must be retained.
- COPY the audit directory before rerunning tests. `python independent_induction_checks.py` requires the already installed SymPy and Python standard library. It imports no author code and writes deterministic adjacent JSON files.
- The exact copied author layout is `author_replay/rate2_induction_clock_20261101/`, with the exact dependency siblings needed by its source-binding checker. Run both `check_corrected_clock.py` and `check_clearance_continuation.py` there in a copy. Compare their JSON reports byte-for-byte with `inputs/`.
- Do not run historical `check_history_v0/independent_induction_checks.py` as an accepted check: it is the preserved audit-harness float-division overflow, not the final exact implementation.
- Dependency-readback reports are HASH VERIFICATIONS, not new replays of the accepted scalar solver or prior theorem checks. The original full gates remain controlling; snapshotting selected proof/receipt files does not invent their omitted runtime artifacts.

No frozen code evaluates or admits the UNEVALUATED interior c(epsilon), n0(epsilon). A numerical finite-N consumer must acquire these or refuse; replaying these algebra checks does not acquire them. No floating probability or practical-cost claim is made.
