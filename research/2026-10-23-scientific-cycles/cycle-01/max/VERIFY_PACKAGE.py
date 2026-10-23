"""Verify this private return's file bytes; no scientific execution."""
from pathlib import Path
import hashlib, json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
rows=manifest['files']
bad=[]
for r in rows:
    p=root/r['path']
    if not p.is_file():
        bad.append(r['path']+':missing'); continue
    b=p.read_bytes()
    if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
        bad.append(r['path']+':digest')
assert not bad,bad
print(json.dumps({'PASS':True,'payload_files':len(rows),
 'scope':'Transport identities only; no scientific calculation or acceptance.'}))
