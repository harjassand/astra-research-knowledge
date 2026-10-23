"""Frozen payload identity only. No science execution, network, or extraction."""
from pathlib import Path
import hashlib,json,sys

def verify(root):
    root=Path(root).resolve()
    manifest=json.loads((root/'MANIFEST.json').read_text())
    failures=[];total=0
    for row in manifest['files']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            failures.append(dict(path=row['path'],reason='unsafe path'));continue
        path=root/rel
        if not path.is_file() or path.is_symlink():
            failures.append(dict(path=row['path'],reason='missing/nonregular'));continue
        data=path.read_bytes();total+=len(data)
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            failures.append(dict(path=row['path'],reason='byte identity'))
    expected={r['path'] for r in manifest['files']}|{'MANIFEST.json'}
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    for p in sorted(actual-expected):failures.append(dict(path=p,reason='unmanifested payload'))
    return dict(status='PASS' if not failures else 'FAIL',checked_files=len(manifest['files']),
                payload_bytes=total,failures=failures,
                scope='Frozen payload identity only; no scientific proof, novelty or acceptance claim.')

if __name__=='__main__':
    result=verify(Path(__file__).resolve().parent)
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['status']=='PASS' else 1)
