#!/usr/bin/env python3
"""Replay the kinetic packet in an isolated output copy, without source mutation."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source-dir", required=True, type=Path)
parser.add_argument("--output-dir", required=True, type=Path)
args = parser.parse_args()
source = args.source_dir.resolve()
output = args.output_dir.resolve()
if output == source or source in output.parents:
    raise SystemExit("Output directory must be outside the immutable source packet.")
output.mkdir(parents=True, exist_ok=True)
manifest = json.loads((source / "MANIFEST.json").read_text())
hashes = []
for name, entry in manifest.items():
    data = (source / name).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    hashes.append({"path": name, "sha256": digest,
                   "sha256_ok": digest == entry["sha256"],
                   "size_ok": len(data) == entry["bytes"]})
if not all(x["sha256_ok"] and x["size_ok"] for x in hashes):
    raise SystemExit("Source integrity check failed.")
shutil.copy2(source / "verify.py", output / "verify.py")
run = subprocess.run([sys.executable, str(output / "verify.py")], cwd=output,
                     capture_output=True, text=True, check=False)
(output / "run_log.json").write_text(run.stdout)
(output / "stderr.txt").write_text(run.stderr)
receipt = {"scope": "Producer diagnostic replay only; no independent universal theorem or novelty validation.",
           "python_version": sys.version, "returncode": run.returncode, "source_hashes": hashes}
if run.returncode == 0:
    produced = (output / "results.json").read_bytes()
    original = (source / "results.json").read_bytes()
    receipt.update({"bytes_match": produced == original,
                    "semantic_match": json.loads(produced) == json.loads(original),
                    "output_sha256": hashlib.sha256(produced).hexdigest()})
(output / "REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({k: receipt[k] for k in ["scope", "returncode", "bytes_match", "semantic_match"] if k in receipt}, indent=2))
if run.returncode:
    raise SystemExit(run.returncode)
