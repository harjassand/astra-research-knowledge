"""Read-only audit/source/dependency binding verifier."""
from pathlib import Path
import argparse,hashlib,json
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--workspace-root',type=Path,default=root.parents[2]);args=p.parse_args()
x=json.loads((root/'AUDIT_SHA256.json').read_text())
def check(p,e):
 b=p.read_bytes();assert len(b)==e['bytes'],str(p);assert hashlib.sha256(b).hexdigest()==e['sha256'],str(p)
for n,e in x['audit_payloads'].items():check(root/n,e)
for n,e in x['original_source_bindings'].items():check(args.workspace_root/n,e)
for n,e in x['dependency_bindings'].items():check(args.workspace_root/n,e)
print(json.dumps({'status':'PASS_READ_ONLY_BINDINGS','audit_payloads':len(x['audit_payloads']),'original_source_files':len(x['original_source_bindings']),'dependency_files':len(x['dependency_bindings'])},sort_keys=True))
