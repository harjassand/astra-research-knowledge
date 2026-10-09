"""Read-only integrity checks. The manifest is never regenerated or edited."""
from pathlib import Path
import argparse
import hashlib
import json

parser=argparse.ArgumentParser()
parser.add_argument("--expected-manifest-sha256",required=True)
args=parser.parse_args()
here=Path(__file__).resolve().parent
manifest_bytes=(here/"MANIFEST.json").read_bytes()
manifest_hash=hashlib.sha256(manifest_bytes).hexdigest()
assert manifest_hash==args.expected_manifest_sha256
manifest=json.loads(manifest_bytes)
for entry in manifest["files"]:
    path=here/entry["path"]
    content=path.read_bytes()
    assert len(content)==entry["bytes"],str(path)
    assert hashlib.sha256(content).hexdigest()==entry["sha256"],str(path)
assert manifest["origin_proof_sha256"]=="6a82f6f18ba0861f2954254c454ecd786032a24b15222e6a7fdc24285de7657d"
for entry in manifest["preservation_anchors"]:
    path=Path(entry["absolute_path"])
    assert hashlib.sha256(path.read_bytes()).hexdigest()==entry["sha256"],str(path)
print(json.dumps({"status":"PASS_READ_ONLY_INTEGRITY","manifest_sha256":manifest_hash,"frozen_entries":len(manifest["files"]),"preservation_anchors":len(manifest["preservation_anchors"]),"writes":0}))
