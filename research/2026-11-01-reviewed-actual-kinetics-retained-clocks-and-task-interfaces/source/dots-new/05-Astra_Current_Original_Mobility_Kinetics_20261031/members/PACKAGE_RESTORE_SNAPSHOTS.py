from pathlib import Path,PurePosixPath
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'PACKAGE_ALIASES.json').read_text())
for name,v in m['aliases'].items():
 p=PurePosixPath(name);q=PurePosixPath(v['canonical'])
 assert not p.is_absolute()and '..'not in p.parts and not q.is_absolute()and '..'not in q.parts
 b=(root/q).read_bytes();assert len(b)==v['bytes']and hashlib.sha256(b).hexdigest()==v['sha256']
 dest=root/p;assert not dest.is_symlink()
 if dest.exists():assert dest.read_bytes()==b
 else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
print('Restored exact duplicate paths:',len(m['aliases']))
