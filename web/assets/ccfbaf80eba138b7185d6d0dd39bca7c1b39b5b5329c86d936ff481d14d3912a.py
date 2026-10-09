"""Run the exposed finite replay while leaving every origin file unchanged."""
from contextlib import redirect_stdout
from pathlib import Path
import hashlib
import io
import json
import runpy

OWN = Path(__file__).resolve().parent
ORIGIN = OWN.parents[1] / "root_cycle05"
source = ORIGIN / "replay_antisymmetric.py"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "ca0711e0c8692a92894bed0c0f138aa807220fb3606bc41d2cbb9b015ddd2fca"
buffer = io.StringIO()
with redirect_stdout(buffer):
    runpy.run_path(str(source), run_name="__main__")
raw = buffer.getvalue()
assert json.loads(raw) == json.loads((ORIGIN / "ANTISYMMETRIC_REPLAY.json").read_text())
(OWN / "EXPOSED_ANTISYMMETRIC_REPLAY.json").write_text(raw)
print(raw, end="")
print(json.dumps({"matches_frozen_origin_result": True,
                  "result_sha256": hashlib.sha256(raw.encode()).hexdigest()}))
