"""Verify all payload bytes in this extracted checkpoint."""
import hashlib
import json
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parent
m=json.loads((root/"MANIFEST.json").read_text())
for row in m["files"]:
    p=root/row["path"]
    assert p.is_file(),row["path"]
    b=p.read_bytes()
    assert len(b)==row["bytes"],row["path"]
    assert hashlib.sha256(b).hexdigest()==row["sha256"],row["path"]
old=root/"sources/Astra_Restore_PRO3_20261021.zip"
assert old.stat().st_size==258287
assert hashlib.sha256(old.read_bytes()).hexdigest()=="761fcf179a6f127d288e8ee5e901ff0f219cc594160dd471cadffbee8c2836c3"
with zipfile.ZipFile(old) as z:
    assert z.testzip() is None
print(json.dumps({"status":"PASS","payload_files":len(m["files"]),
                  "unchanged_previous_source":True}))
