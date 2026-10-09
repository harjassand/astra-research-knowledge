"""Verify an explicitly pinned manifest and its complete file inventory."""
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
assert len(sys.argv)==2,"Pass the externally reported immutable MANIFEST.json SHA256."
raw=(HERE/"MANIFEST.json").read_bytes()
assert hashlib.sha256(raw).hexdigest()==sys.argv[1],"Manifest does not match reported freeze."
m=json.loads(raw)
listed=set()
for item in m["files"]:
    rel=item["path"]
    assert rel not in listed and rel!="MANIFEST.json"
    listed.add(rel)
    data=(HERE/rel).read_bytes()
    assert len(data)==item["bytes"] and hashlib.sha256(data).hexdigest()==item["sha256"],rel
actual={str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file() and p.name!="MANIFEST.json"}
assert actual==listed,("Unclassified/missing files",sorted(actual-listed),sorted(listed-actual))
for item in m["preservation_anchors"]:
    data=Path(item["absolute_path"]).read_bytes()
    assert hashlib.sha256(data).hexdigest()==item["sha256"],item["absolute_path"]
print(json.dumps({"status":"PASS_READ_ONLY_INTEGRITY","classified_files":len(listed),
                  "preservation_anchors":len(m["preservation_anchors"]),"unclassified_files":0}))
