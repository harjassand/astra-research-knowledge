"""Restore exact-byte duplicate dependencies in a writable extracted copy.
No network, no imports of research code, and no overwriting of different bytes.
"""
import pathlib,json,hashlib,shutil
root=pathlib.Path(__file__).resolve().parent
for row in json.loads((root/'ALIASES.json').read_text()):
 src=(root/row['copy_from']).resolve();dst=(root/row['path']).resolve()
 assert src.is_relative_to(root) and dst.is_relative_to(root)
 assert hashlib.sha256(src.read_bytes()).hexdigest()==row['sha256']
 if dst.exists():assert hashlib.sha256(dst.read_bytes()).hexdigest()==row['sha256'];continue
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
print('Exact-byte dependency aliases restored.')
