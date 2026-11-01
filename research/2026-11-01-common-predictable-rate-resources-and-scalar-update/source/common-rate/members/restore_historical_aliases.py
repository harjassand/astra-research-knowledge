"""Restore exact historical duplicate paths; never overwrite a conflict."""
from pathlib import Path
import json,hashlib

def safe(root,name):
    if type(name)is not str or not name or Path(name).is_absolute() or '..' in Path(name).parts:raise ValueError('unsafe relative path')
    p=root/name
    if not p.resolve().is_relative_to(root.resolve()):raise ValueError('path escapes package')
    return p

def check(path,record):
    if not path.is_file() or path.is_symlink():raise ValueError('missing/nonregular bound file: '+str(path))
    b=path.read_bytes()
    if len(b)!=record['bytes'] or hashlib.sha256(b).hexdigest()!=record['sha256']:raise ValueError('bound bytes mismatch: '+str(path))
    return b

def verify_payload(root):
    m=json.loads((root/'PAYLOAD_MANIFEST.json').read_text())
    for name,record in m['files'].items():check(safe(root,name),record)
    return len(m['files'])

def restore(root):
    root=Path(root).resolve();verify_payload(root)
    aliases=json.loads((root/'ALIAS_MAP.json').read_text())['aliases']
    for target,record in aliases.items():
        b=check(safe(root,record['source']),record);dest=safe(root,target)
        if dest.exists():check(dest,record)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            with dest.open('xb') as f:f.write(b)
    logical=json.loads((root/'LOGICAL_BINDINGS.json').read_text())['files']
    for name,record in logical.items():check(safe(root,name),record)
    return {'restored_aliases':len(aliases),'verified_logical_paths':len(logical)}

if __name__=='__main__':print(json.dumps(restore(Path(__file__).resolve().parent),sort_keys=True))
