# Frozen independent free-port glue audit

Verdict: scoped mathematical, constructor and independent-receiver PASS.
Read `WHOLE_PROOF_CODE_AUDIT.md` for the full proof, exact raw boundary, costs,
actual execution evidence, source-access quarantine and excluded claims.

Strict staging: copy only the relative files listed in `ARTIFACT_ALLOWLIST.json`.
`FINAL_AUDIT_MANIFEST.json` hashes every other allowlisted file. Do not overwrite
any evidence. The source manifest is separately bound in `SOURCE_BINDINGS.json`.
No multi-target exploration or unreviewed finite-layer note is included.

From a copy of this directory, assertions-enabled Python with
`PYTHONDONTWRITEBYTECODE=1` runs:

- `replay_author.py`
- `exercise_independent.py`
- `graph_and_switch_controls.py`
- `wire_and_dependency_controls.py`

Set `AUDIT_OUTPUT_DIR` to a fresh writable absolute directory. Optionally set
`GLUE_SOURCE_DIR` to the original 29-file candidate. Default resolution supports
this directory staged as that source package's `fresh_whole_audit/`.
`reproduce_staged.py` makes a fresh local temporary package and runs all four,
comparing mathematical outputs while excluding variable elapsed times.

The independent receiver imports only the two byte-identical earlier independent
primitives under `prior_independent/`, never the candidate implementation. Driver
imports of candidate code are for comparisons only. Exhaustive cover enumeration
occurs solely in charged small graph controls, not production receiving.

The actual astronomical head and complete phi=1 global tail were not executed.
Synthetic cutoff widths test only the cross-generator lemma. The whole ordinary
proof establishes the unbounded global join; cost claims remain conditional on
explicit state/certificate bits. A mathematical PASS does not clear the retained
historical source-access violation.
