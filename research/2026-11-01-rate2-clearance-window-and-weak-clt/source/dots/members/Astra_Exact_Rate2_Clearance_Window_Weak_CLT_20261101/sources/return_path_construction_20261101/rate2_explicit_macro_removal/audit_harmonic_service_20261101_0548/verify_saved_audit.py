"""Read-only verification of this audit and its four original source bindings."""
from pathlib import Path
import argparse,hashlib,json
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,default=root.parent);a=p.parse_args()
m=json.loads((root/'AUDIT_SHA256.json').read_text())
def check(p,e):
 b=p.read_bytes();assert len(b)==e['bytes'],str(p);assert hashlib.sha256(b).hexdigest()==e['sha256'],str(p)
for n,e in m['audit_payloads'].items():check(root/n,e)
for n,e in m['original_source_bindings'].items():check(a.source_dir/n,e)
print(json.dumps({'status':'PASS_READ_ONLY_BINDINGS','audit_payloads':len(m['audit_payloads']),'original_source_files':len(m['original_source_bindings'])},sort_keys=True))
