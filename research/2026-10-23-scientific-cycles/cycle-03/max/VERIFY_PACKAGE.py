"""Verify this selected return's exact payload bytes. No scientific execution."""
from pathlib import Path
import hashlib,json

root=Path(__file__).resolve().parent
rows=json.loads((root/'MANIFEST.json').read_text())['files']
listed={r['path'] for r in rows}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'}
assert listed==actual, {'missing':sorted(listed-actual),'unlisted':sorted(actual-listed)}
for r in rows:
    b=(root/r['path']).read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
print(json.dumps({'PASS':True,'payload_files':len(rows),'scope':'Transport only; no scientific acceptance.'}))
