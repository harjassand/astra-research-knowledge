#!/usr/bin/env python3
"""Read-only validation of source and package SHA bindings."""
from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
root=here.parent
checks=[]
for manifest,base,key in [(here/'SOURCE_BINDINGS.json',root,'files'),(here/'AUTHOR_FREEZE.json',here,'files')]:
    payload=json.loads(manifest.read_text())
    for entry in payload[key]:
        path=base/entry['path'];data=path.read_bytes()
        ok=hashlib.sha256(data).hexdigest()==entry['sha256'] and len(data)==entry['bytes']
        checks.append({'path':str(path.relative_to(root)),'passed':ok})
        if not ok:raise AssertionError(str(path))
print(json.dumps({'status':'PASS_SHA_AND_SIZE_BINDINGS','checked_files':len(checks),'checks':checks},indent=2))
