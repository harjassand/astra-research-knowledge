#!/usr/bin/env python3
"""Read-only preservation check. No writes, regeneration, chmod, or repair."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[3]
EXPECTED={
 "MANIFEST.json":"24832b92178c023dc90dbe40fe3cf567050d3468662fea0e80b06e76c8be8864",
 "POST_EXPOSURE_MANIFEST_20261009.json":"b33167475a8d9c6d3e945a543b35069768298ef2abbab4ee2c92f85d4d44e85f",
 "PRESERVATION_REPAIR_RECEIPT.json":"fef48310f775d1c5a16149a54450045f3c9c3dadf1428892fd9c38a2c5f85a40"
}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name,expected in EXPECTED.items():
 assert digest(ROOT/name)==expected,(name,digest(ROOT/name))
original=json.loads((ROOT/"MANIFEST.json").read_text())
post=json.loads((ROOT/"POST_EXPOSURE_MANIFEST_20261009.json").read_text())
current=json.loads((ROOT/"POST_REPAIR_MANIFEST_20261009.json").read_text())
assert len(original["files"])==19
assert len(post["files"])==21
assert original["authorized_review_receipts"]==[]
assert len(post["authorized_review_receipts"])==2
for name,manifest in [("original",original),("post_exposure",post),("post_repair",current)]:
 for item in manifest["files"]:
  path=ROOT/item["path"]
  assert path.stat().st_size==item["bytes"],(name,item["path"],"size")
  assert digest(path)==item["sha256"],(name,item["path"],"hash")
for path,sha in original["preserved_cycle06_hashes"].items():
 assert digest(ROOT.parent/"cycle06_record_transfer"/path)==sha,path
for review in post["authorized_review_receipts"]:
 assert digest(WORKSPACE/review["path"])==review["sha256"],review["path"]
print(json.dumps({
 "integrity":"PASS_READ_ONLY",
 "original_manifest_sha256":digest(ROOT/"MANIFEST.json"),
 "preserved_post_exposure_sha256":digest(ROOT/"POST_EXPOSURE_MANIFEST_20261009.json"),
 "post_repair_manifest_sha256":digest(ROOT/"POST_REPAIR_MANIFEST_20261009.json"),
 "original_entries":19,"post_exposure_entries":21,
 "post_repair_entries":len(current["files"]),
 "origin_proof_report_hashes":len(original["frozen_origin_hashes"]),
 "preserved_old_proofs":len(original["preserved_cycle06_hashes"]),
 "writes":0
}))

