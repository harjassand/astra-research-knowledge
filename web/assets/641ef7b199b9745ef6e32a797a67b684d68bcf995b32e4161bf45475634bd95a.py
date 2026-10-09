"""Replay the exposed fixed exact control without modifying its directory."""
from pathlib import Path
import hashlib
import json

OWN = Path(__file__).resolve().parent
ORIGIN = OWN.parents[1] / "variance_monogamy_sol" / "cycle03_graph"
SOURCE = ORIGIN / "replay_k222_exact.py"
raw = SOURCE.read_text()
assert hashlib.sha256(raw.encode()).hexdigest() == "ab8c3db7ad9fed699dfd0fe91f63e4831ec7db4f475f250f8d9dcd6b06d72757"
old = "(ROOT/'K222_REPLAY_RESULT.json').write_text"
new = "(Path(" + repr(str(OWN / "EXPOSED_K222_REPLAY_RESULT.json")) + ")).write_text"
assert raw.count(old) == 1
namespace = {"__file__": str(SOURCE), "__name__": "__main__"}
exec(compile(raw.replace(old, new), str(SOURCE), "exec"), namespace)
original = (ORIGIN / "K222_REPLAY_RESULT.json").read_bytes()
replayed = (OWN / "EXPOSED_K222_REPLAY_RESULT.json").read_bytes()
assert replayed == original
print(json.dumps({"origin_unchanged": True, "replay_matches_origin_byte_for_byte": True,
                  "result_sha256": hashlib.sha256(replayed).hexdigest()}))
