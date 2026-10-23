from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
for row in m['files']:
 p=(root/row['path']).resolve()
 assert p.is_relative_to(root.resolve()), row['path']
 assert p.stat().st_size==row['bytes'], row['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'], row['path']
print(json.dumps({'status':'PASS','checked_files':len(m['files']),'scope':'Integrity only; no new science or certification.'}))
