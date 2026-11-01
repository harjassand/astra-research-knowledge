"""Read-only verification of audit payloads and the four original source files."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser()
p.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parent.parent)
a=p.parse_args(); root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_SHA256.json').read_text())
def verify(path,entry):
    data=path.read_bytes()
    assert len(data)==entry['bytes'],str(path)
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],str(path)
for name,entry in manifest['audit_payloads'].items(): verify(root/name,entry)
for name,entry in manifest['original_source_bindings'].items(): verify(a.source_dir/name,entry)
print(json.dumps({'status':'PASS_READ_ONLY_BINDINGS','audit_payloads':len(manifest['audit_payloads']), 'original_source_files':len(manifest['original_source_bindings'])},sort_keys=True))
