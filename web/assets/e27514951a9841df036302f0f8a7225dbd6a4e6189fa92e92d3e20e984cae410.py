"""Verify capture integrity only; this is not a mathematical proof checker."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import time
import zipfile

root = Path(__file__).resolve().parents[3]
out = root / "outputs/round6"
start = time.monotonic()
manifest = json.loads((out / "SNAPSHOT_MANIFEST.json").read_text())
archive = out / "ROUND6_EVIDENCE.zip"
errors = []
digest = hashlib.file_digest(archive.open("rb"), "sha256").hexdigest()
if digest != manifest["archive_sha256"]:
    errors.append("archive hash")
if archive.stat().st_size != manifest["archive_bytes"]:
    errors.append("archive size")
with zipfile.ZipFile(archive) as z:
    embedded = json.loads(z.read("SNAPSHOT_MANIFEST.json"))
    if embedded["files"] != manifest["files"]:
        errors.append("embedded file manifest differs")
    names = z.namelist()
    expected = [f["path"] for f in manifest["files"]] + ["SNAPSHOT_MANIFEST.json"]
    if sorted(names) != sorted(expected) or len(names) != len(set(names)):
        errors.append("archive entry set")
    for f in manifest["files"]:
        data = z.read(f["path"])  # also checks the entry CRC
        if len(data) != f["bytes"] or hashlib.sha256(data).hexdigest() != f["sha256"]:
            errors.append(f["path"])
tree = ast.parse((root / "work/cycle6/control/snapshot.py").read_text())
selected = next(ast.literal_eval(n.value) for n in tree.body
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
                and t.id == "selected" for t in n.targets))
for name, relative in selected.items():
    source, dest = root / "work/cycle6" / relative, out / name
    if not source.exists() or not dest.exists():
        errors.append("missing selected proof: " + name)
    elif source.read_bytes() != dest.read_bytes():
        errors.append("selected alias differs: " + name)
cards = json.loads((out / "RESEARCH_RESULT_CARDS.json").read_text())["cards"]
references = []
for card in cards:
    for key in ("proofs", "evidence"):
        for name in card.get(key, []):
            references.append(name)
            if not (out / name).is_file():
                errors.append("missing card reference: " + name)
receipt = {
    "status": "PASS" if not errors else "FAIL",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "ZIP CRC, all captured SHA256 hashes, embedded manifest, selected proof aliases and card references; NOT proof validity or external validation",
    "archive_sha256": digest,
    "archive_bytes": archive.stat().st_size,
    "captured_files": len(manifest["files"]),
    "selected_proofs": len(selected),
    "card_references": len(references),
    "seconds": time.monotonic() - start,
    "errors": errors,
}
(out / "ARCHIVE_VERIFICATION.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
raise SystemExit(bool(errors))
