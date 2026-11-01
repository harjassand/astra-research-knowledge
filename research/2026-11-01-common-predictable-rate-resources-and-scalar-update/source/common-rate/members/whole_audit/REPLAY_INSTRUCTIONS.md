# Relocation and immutable replay

This audit tree is relocatable as a complete directory. Its scripts resolve paths
relative to `__file__`; there are no network dependencies or installed packages.
Use standard Python 3 with assertions enabled, not `python -O`.

Read-only verification in the preserved audit directory:

    PYTHONDONTWRITEBYTECODE=1 python verify_saved_audit.py

For independent replay, first copy the entire audit directory to a **new working
directory**. Do not overwrite the immutable released results. Within that copy:

    PYTHONDONTWRITEBYTECODE=1 python independent_arithmetic.py v2
    PYTHONDONTWRITEBYTECODE=1 python independent_controls.py v2
    PYTHONDONTWRITEBYTECODE=1 python independent_repair.py
    PYTHONDONTWRITEBYTECODE=1 python final_supplement.py

These scripts use `replay_v2/`, `frozen_v1/` and `frozen_v2/` at the retained relative
paths. Their output timing fields may differ. The arithmetic/control v1 replays
and `api_v1_diagnostic.py` are historical evidence; running them is not a v1 whole
acceptance. The initial failed arithmetic reference is also historical, not a
passing entrypoint.

The current author source package is separately relocatable as a directory. In a
fresh copied/extracted author v2 directory, the four actual source entrypoints are:

    PYTHONDONTWRITEBYTECODE=1 python check_common_box.py
    PYTHONDONTWRITEBYTECODE=1 python check_box_large_tiers.py
    PYTHONDONTWRITEBYTECODE=1 python check_scalar_extremes.py
    PYTHONDONTWRITEBYTECODE=1 python check_v2_receiving.py

They write reports beside themselves. Preserve original/frozen copies and run
only in a dedicated reproduction tree. No path override is needed. Their results
were byte-identical in this audit.

The complete audit allowlist is every key in `AUDIT_SHA256.json.files`, plus
`AUDIT_SHA256.json` itself. Include the complete allowlist if claiming a
self-contained replayable audit. A receipt-only package must instead explicitly
say that full audit artifacts are separate. Python bytecode/cache files are not
part of the manifest. `freeze_audit.py` is a maintainer-side sealing record: it
expects both original sibling source directories and is not a recipient replay
entrypoint. `verify_saved_audit.py` needs only this complete audit tree.
