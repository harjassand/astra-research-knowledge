"""Require the reported manifest hash; verify all files without writing."""
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
assert len(sys.argv)==2,"Supply the externally reported manifest SHA256."
data=(HERE/"MANIFEST.json").read_bytes()
assert hashlib.sha256(data).hexdigest()==sys.argv[1]
m=json.loads(data)
listed=set()
for row in m["files"]:
    assert row["path"] not in listed
    listed.add(row["path"])
    b=(HERE/row["path"]).read_bytes()
    assert len(b)==row["bytes"] and hashlib.sha256(b).hexdigest()==row["sha256"],row["path"]
actual={str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file() and p.name!="MANIFEST.json"}
assert actual==listed,(sorted(actual-listed),sorted(listed-actual))
for row in m["preservation_anchors"]:
    assert hashlib.sha256(Path(row["absolute_path"]).read_bytes()).hexdigest()==row["sha256"],row["absolute_path"]
print(json.dumps({"status":"PASS_READ_ONLY_INTEGRITY","classified_files":len(listed),
                  "preservation_anchors":len(m["preservation_anchors"]),"unclassified_files":0}))
