"""Check the immutable delivered source inventory before replay changes receipts."""
from pathlib import Path
import hashlib,json

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST.json').read_text())
for item in manifest['files']:
    path=root/item['path']
    data=path.read_bytes()
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
        raise SystemExit('MISMATCH: '+item['path'])
print('PASS:',len(manifest['files']),'delivered files match exact sizes and SHA256 values')
