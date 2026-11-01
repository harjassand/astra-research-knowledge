"""Read-only payload, original-source, and exact theorem-dependency verifier."""
from pathlib import Path
import argparse,hashlib,json
parser=argparse.ArgumentParser()
parser.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parent.parent)
a=parser.parse_args();root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_SHA256.json').read_text())
def check(path,entry):
    data=path.read_bytes()
    assert len(data)==entry['bytes'],str(path)
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],str(path)
for name,entry in manifest['audit_payloads'].items():check(root/name,entry)
for name,entry in manifest['original_source_bindings'].items():check(a.source_dir/name,entry)
for name,entry in manifest['dependency_bindings'].items():check(a.source_dir/name,entry)
print(json.dumps({'status':'PASS_READ_ONLY_BINDINGS','audit_payloads':len(manifest['audit_payloads']),'original_source_files':len(manifest['original_source_bindings']),'dependency_files':len(manifest['dependency_bindings'])},sort_keys=True))
