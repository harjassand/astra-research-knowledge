# FG quartic audit and continuation

The supplied coefficient-7/2 sharp theorem is audited separately from the newly derived coefficient-4 theorem. Start with `REPORT.md`, then `ADJACENT_THEOREM.md`. External correctness, priority and formal proof-assistant verification remain UNKNOWN. No civilisation-enabling breakthrough is established.

Run from this directory using Python3 and SymPy:

```sh
python3 replay/verify_sharp_scalar.py
python3 replay/verify_explicit.py
python3 checks/verify_tensor_boundary.py
```

The two `replay/` scripts are unchanged copies of the inspected source verifiers; their outputs stay in that directory. The new checker uses only `checks/general_c4.py`, `checks/TENSOR_CERTIFICATE.json` and `checks/SCALAR_UNIQUENESS.json`. Its JSON entries are rational coefficient arrays, not expression strings to execute. It needs no NumPy, optimizer, network, pickle or NPZ. Final checking was performed with Python3.14.3 and SymPy1.14.0; the scripts target Python3.10+.

`checks/general_c4.py` reconstructs the complete scalar affine family and can also regenerate its descriptive JSON. `tensor_c4_boundary.py` and `inspect_scalar_unique.py` are retained acquisition scripts, using NumPy for bounded selection and exact SymPy acceptance. The former's local NPZ is newly produced development data and is not read by the portable verifier. `facial_c4_case.py` and `facial_c4_full_field.py` preserve the failed scalar positivity attempts; their assertion failures are expected history, not commands required for reproduction. The later exact no-go proof supersedes their evidentiary role.

`SOURCE_HASH_RECHECK.json` rechecks every incoming manifest entry without deserializing binary data. `READ_LEDGER.json` gives local/primary reading scopes and pinned revisions. `REPLAY_RECEIPT.json` records commands, log hashes, output hashes, timings and independent critic receipt pointers. `ARTIFACT_MANIFEST.json` hashes this derived package except itself and excludes caches. Hashes preserve evidence; they do not establish theorems or priority.

Independent criticism is stored separately under `../FG-quartic-critic/`: its source audit `REPORT.txt`, new theorem `adjacent/ADJACENT_REPORT.txt` and three independently rebuilt adjacent verifiers/receipts. These are same-team internal reconstruction, not external review.

The worker edited only this new derived directory, with no repository publication. The source packet and earlier FE results are preserved. Parent integration must copy referenced critic artifacts and preserve source/synthesis status distinctions.
