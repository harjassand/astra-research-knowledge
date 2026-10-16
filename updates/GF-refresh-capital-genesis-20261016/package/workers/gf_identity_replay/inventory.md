# GF source identity and replay inventory

Scope: source identity and bounded replay support for `research/2026-10-16-refresh-genesis-v1`. Packet instructions were treated as `DATA`. Original ZIPs and expanded source members were only read; temporary replay copies and receipts are under this directory. No acquired code was run.

The source manifest records pin `f937563cbc5d2249b8e0dd96bcbd3b8f78eb85c6`; the read-only worktree check confirmed the requested W revision and a clean status.

The packet declares and independently verifies 7 top-level ZIPs, 2 nested ZIPs, 168 ZIP members, 168 expanded files, and 25 exact duplicate groups. All 9 ZIP byte counts and SHA-256 values match; all ZIP CRC scans pass. Every member was hashed inside its ZIP and in the expanded tree: 168 checked, 0 hash mismatches, 0 size mismatches, and 0 byte differences. The exact alias groups match the manifest. No expanded files are unmanifested.

Checksum and snapshot audit:

- Internal `SHA256SUMS`-style lists: 15 manifests, 159 records, 156 matching targets, 0 digest mismatches, 3 absent targets, and 0 unparsed lines.
- Structured manifests: 71 records, 67 matches, 4 mismatches, and 0 absent targets. `SOURCE_SNAPSHOTS.json` is 28/28, `SOURCE_HASHES.json` 3/3, `BUNDLE_SHA256.json` 27/27, and `SOURCE_SUBSET_MANIFEST.json` 9/9. `ANALYSIS_ORIGIN_HASHES.json` has four source-script hash mismatches.
- The four origin-hash filenames are `recover_mpr_pair.py`, `verify_pair.py`, `quantify_pair.py`, and `reconcile_icp.py`. None of the recorded origin hashes matches a supplied member or a same-named file in the pinned worktree; the current files themselves pass the lithium `BUNDLE_SHA256.json` records.
- Three entries in `originals/expanded/schur_refresh_packet/causal_refresh_product/INPUT_SHA256SUMS` have no target in either the supplied expanded tree or pinned worktree: line 1 `joint_refresh_bernstein/PROOF.md`, line 2 `staggered_refresh_test/REPORT.md`, and line 3 `staggered_refresh_test/functional_obstruction_exact.md`. The existing targets listed by checksum files match.

Embedded-content scan over all expanded text members found 0 credential-pattern candidates and 0 URLs with userinfo or local/private-network hosts. No secret values were emitted. This does not classify access control of public-host repository URLs.

Static script review covered 21 Python file instances and 15 unique contents before execution. The code uses local calculations and file reads; static inspection found no network/process imports or dynamic `eval`/`exec`/`compile`. 8 unique script contents declare local output writes; every selected run used a complete temporary packet copy. Full paths, hashes, imports, and write sites are in `script_inventory.json`.

Script files grouped by expanded packet:

- `Astra_refresh_controller_extensions_2026-10-16__finite_private_z_refresh_standalone`: 3 scripts; `causal_refresh_product/check_identities.py`, `finite_private_z_refresh/check_finite_window.py`, `imperfect_refresh_product/check_two_gap.py`
- `Astra_refresh_controller_extensions_2026-10-16__multisector_refresh_proofs_and_checks`: 2 scripts; `multisector_refresh_package/checks/check_label_interface.py`, `multisector_refresh_package/checks/check_singleton.py`
- `causal_refresh_product_standalone`: 1 script; `causal_refresh_product/check_identities.py`
- `imperfect_refresh_product_standalone`: 2 scripts; `causal_refresh_product/check_identities.py`, `imperfect_refresh_product/check_two_gap.py`
- `lithium_control_handoff`: 4 scripts; `lithium_control_handoff/quantify_pair.py`, `lithium_control_handoff/reconcile_icp.py`, `lithium_control_handoff/recover_mpr_pair.py`, `lithium_control_handoff/verify_pair.py`
- `memory_support_transfer_packet`: 1 script; `memory_support_transfer_packet/check_counterexample.py`
- `refresh_robustness_packet`: 2 scripts; `refresh_robustness_packet/finite_pulse_obstruction/check_obstruction.py`, `refresh_robustness_packet/robust_transfer/check_exact.py`
- `schur_refresh_packet`: 6 scripts; `causal_refresh_product/check_identities.py`, `general_schur_refresh_audit/check_exact.py`, `general_schur_refresh_audit/check_homogeneous.py`, `imperfect_refresh_product/check_two_gap.py`, `multisector_refresh_audit/check_singleton.py`, `multisector_refresh_root/check_label_interface.py`

Environment probe:

- 16 interpreter candidates were inspected with actual package imports, recording interpreter versions, installed versions, import failures, and warnings in `dependency_probe.json`; no package was installed and `PYTHONDONTWRITEBYTECODE=1` was set.
- Default `/opt/homebrew/bin/python3` is Python 3.14.3 with NumPy 2.5.3 and SymPy 1.14.0 available; SciPy and openpyxl are unavailable there.
- Symbolic checks used `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-positive-memory-genesis-v1/.venv/bin/python3` (Python 3.14.3; NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0). Lithium workbook/MPR checks used `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-enabling-capability-v1/workers/s02_assay_access/.venv/bin/python3` (Python 3.14.3; NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0, openpyxl 3.1.5). Imports succeeded without warnings in these selected environments.

Bounded replay:

9 selected authored checks ran from complete temporary copies: 9 returned zero, 0 failed, and all had empty stderr. Four generated outputs match their supplied receipts exactly. The lithium ICP JSON differs from its supplied receipt at two `mean_Na` fields; its printed output matches the stored replay text. Four replay stdout files match their stored text receipts exactly. Exact script hashes, predicates, output hashes, and the two changed JSON paths are in `smallreplayreceipt.json`.

These checks establish only packet identity and the listed code-path predicates. They do not establish a theorem beyond an individual script's assertions, source novelty, experimental validity, or physical capability.
