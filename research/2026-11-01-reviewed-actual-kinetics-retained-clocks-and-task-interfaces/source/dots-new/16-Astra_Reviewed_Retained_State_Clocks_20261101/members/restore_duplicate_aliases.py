from pathlib import Path,PurePosixPath
import json,hashlib
p=Path(__file__).resolve().parent
a=json.loads((p/'DUPLICATE_ALIASES.json').read_text())
for n,r in a.items():
 q=PurePosixPath(n);s=PurePosixPath(r['canonical'])
 assert not q.is_absolute() and '..'not in q.parts and not s.is_absolute() and '..'not in s.parts
 b=(p/r['canonical']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 out=p/n;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==b
 else:out.write_bytes(b)
print('Restored and verified',len(a),'duplicate aliases')
