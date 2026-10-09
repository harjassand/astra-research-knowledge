"""Verify final byte inventory. This is not mathematical proof verification."""
from pathlib import Path
import hashlib
import json

manifest=Path(__file__).with_name('final_integrity_manifest_v1.json')
data=json.loads(manifest.read_text())
root=manifest.parent.parent.parent
errors=[]
for item in data['files']:
    path=root/item['path']
    if not path.is_file():
        errors.append(f"missing: {item['path']}")
        continue
    content=path.read_bytes()
    if len(content)!=item['bytes'] or hashlib.sha256(content).hexdigest()!=item['sha256']:
        errors.append(f"changed: {item['path']}")
if errors:
    raise SystemExit('\n'.join(errors))
print(f"PASS: {len(data['files'])} preserved file hashes; byte integrity only")
