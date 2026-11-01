from pathlib import Path,PurePosixPath
import json,hashlib
root=Path(__file__).resolve().parent
aliases=json.loads((root/'DUPLICATE_ALIASES.json').read_text())
for name,item in aliases.items():
 for s in [name,item['canonical']]:
  q=PurePosixPath(s);assert not q.is_absolute() and '..'not in q.parts
  resolved=(root/s).resolve();assert resolved==root or root in resolved.parents
 b=(root/item['canonical']).read_bytes()
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
 out=root/name;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert not out.is_symlink() and out.read_bytes()==b
 else:out.write_bytes(b)
print('Restored and verified',len(aliases),'duplicate aliases')
