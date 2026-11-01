# Fresh recovered-backbone whole audit

Scoped PASS for the **new** f900821b source binding, not the lost c6061f53 source.
Read `WHOLE_PROOF_CODE_AUDIT.md` and `FINAL_AUDIT_MANIFEST.json` for scope/evidence.
All 158 bound files remain unchanged. Giant mass/global/stationary powers remain
unexpanded; source-process, novelty and general-WR clearance are not claimed.

Main independent files:
- `independent_backbone.py`: raw/constant/full receipt and executable DAG receiver.
- `fixtures.py`, `check_components.py`, `check_raw.py`, `check_receiving.py`.
- `COMPONENT_RESULTS.json`, `RAW_RESULTS.json`, `RECEIVING_RESULTS.json`.
- `MAIN_DAG.json`, `INPUT_BINDING.json`, `STAGED_REPLAY.json`.
- `retained/`: four exact, separately authored previous primitive files.
- `author_replay/`: current source receipt/DAG and three author-suite replays.

Use assertions-enabled Python, never -O. From a fresh audit copy:

```
PYTHONDONTWRITEBYTECODE=1 python check_components.py
PYTHONDONTWRITEBYTECODE=1 python check_raw.py
PYTHONDONTWRITEBYTECODE=1 python check_receiving.py
PYTHONDONTWRITEBYTECODE=1 python reproduce_staged.py
```

Set BACKBONE_SOURCE_DIR to a verified relocated source for the first three.
They write only beside themselves, not into source. `reproduce_staged.py` copies
only the 158 bound inputs and exact independent code/dependencies into fresh /tmp
staging, runs all three suites, compares result/AST bytes and rechecks frozen
source hashes. Fresh timings are measurements, not required historical matches.

The dense custom P4 fixture explicitly uses a 300,000 core-loop budget; default
100,000 honestly refuses its 102,755 steps. Synthetic heads/widths and actual-K
local cones are never presented as numerical global Foster states.
