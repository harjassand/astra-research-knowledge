#!/usr/bin/env python3
"""Verify delivered bytes; optionally replay only the NEW frozen diagnostic."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("--run-new-diagnostic",action="store_true")
args=parser.parse_args()
manifest=json.loads((ROOT/"MANIFEST.json").read_text())
for item in manifest["files"]:
    path=ROOT/item["path"]
    body=path.read_bytes()
    assert len(body)==item["bytes"],item["path"]
    assert hashlib.sha256(body).hexdigest()==item["sha256"],item["path"]
original=ROOT/"sources/Astra_Amplification_Cycle10_PRO3_20261023.zip"
body=original.read_bytes()
assert len(body)==3508928
assert hashlib.sha256(body).hexdigest()=="55afc9d70013d8cc0332d6a03c51901876533d908412448d7d81b2b6f393e1c1"
print(json.dumps({"payload_hashes_checked":len(manifest["files"]),
                  "predecessor_exact":True,"old_science_rerun":False}))
if args.run_new_diagnostic:
    fixture=ROOT/"contributors/tagged_path_check"
    with tempfile.TemporaryDirectory(prefix="astra_cycle11_check_") as td:
        copy=Path(td)/"tagged_path_check"
        shutil.copytree(fixture,copy)
        subprocess.run([sys.executable,"-I",str(copy/"replay.py")],check=True)
        assert (copy/"RESULT.json").read_bytes()==(fixture/"RESULT.json").read_bytes()
        print(json.dumps({"new_diagnostic_matches_frozen_result":True,
                          "delivered_inputs_modified":False}))
