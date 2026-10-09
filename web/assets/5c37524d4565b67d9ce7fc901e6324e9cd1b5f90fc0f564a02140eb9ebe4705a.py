from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
rows=json.loads((root/'FILE_MANIFEST.json').read_text())
expected={r['path'] for r in rows}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='FILE_MANIFEST.json' and '__pycache__' not in p.parts}
if expected!=actual:
    raise RuntimeError('File inventory mismatch: '+str(expected.symmetric_difference(actual)))
for row in rows:
    p=root/row['path']
    if p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
        raise RuntimeError('Digest mismatch: '+row['path'])
print('PASS: '+str(len(rows))+' files; present artifact integrity only, not proof validation')
