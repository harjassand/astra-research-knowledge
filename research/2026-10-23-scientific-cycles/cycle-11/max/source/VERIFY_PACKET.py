"""Verify this delivered packet's payload identities. No scientific execution.

The external archive SHA256 and private source identity bind the delivered copy.
An editable internal manifest alone is not an authenticity certificate.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
seen = set()
failures = []
total = 0
for item in manifest["files"]:
    name = item["path"]
    rel = PurePosixPath(name)
    if rel.is_absolute() or ".." in rel.parts or name in seen:
        failures.append({"path": name, "error": "unsafe_or_duplicate_path"})
        continue
    seen.add(name)
    path = ROOT.joinpath(*rel.parts)
    if path.is_symlink() or not path.is_file():
        failures.append({"path": name, "error": "missing_or_nonregular_file"})
        continue
    data = path.read_bytes()
    total += len(data)
    if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
        failures.append({"path": name, "error": "identity_mismatch"})
actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
unexpected = sorted(actual - seen - {"MANIFEST.json"})
if unexpected:
    failures.append({"error": "unlisted_files", "paths": unexpected})
result = {
    "status": "PASS" if not failures else "FAIL",
    "checked_files": len(seen),
    "payload_bytes": total,
    "failures": failures,
    "scope": "Packet identity only. No owner science, proof certification, novelty or acceptance check.",
}
print(json.dumps(result, indent=2))
sys.exit(bool(failures))
