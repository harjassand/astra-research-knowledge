# Bounded reproduction

The frozen artifacts are a receipt of this run. To reproduce generated outputs, first copy this worker directory to a new directory and run there. The scripts retain absolute paths to the supplied input packets. No supplied packet is modified by these scripts. Preserve the original frozen receipt because later shared-worktree HEAD and runtime metadata may change.

New exact interface operation (Python standard library):

```sh
python3 exact_interface_tests.py
```

New independent central-chi and isolated-qubit compiler checks (NumPy required):

```sh
python3 cp_floor_tests.py
```

Source payload verification and aggregate JSON comparison (standard library; requires the saved aggregate output and initial Git commit):

```sh
python3 verify_sources.py
```

The archived matched-memory `replay_analysis.py` is read-only, sets `sys.dont_write_bytecode`, and writes its receipt to stdout. The randomizer `replay.py` makes a disposable copy before generating its derived outputs. Their exact command paths and exit codes are in `CHECK_RECEIPT.json`; logs are preserved beside this document. No new simulator trajectory was launched.

Autonomous `evaluate.py`, `model.py`, `check_ideal_recovery.py` and the two specified unit modules were inspected for input and write behavior before execution. They print results only and were run with `PYTHONDONTWRITEBYTECODE=1`. Author `Extended_data_Fig6.py` was read as source, never imported or executed.

The complete Willow statistical replay and the complete autonomous optimization suite were not run. SciPy is absent from the inspected default and bundled Python environments. No dependency installation or replacement statistical implementation was attempted.

To verify this worker's frozen bytes without rerunning any scientific code:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json
p = Path('.')
m = json.loads((p/'FROZEN_MANIFEST.json').read_text())
for name, d in m['files'].items():
    assert hashlib.sha256((p/name).read_bytes()).hexdigest() == d['sha256'], name
print('PASS: frozen worker bytes')
PY
```
