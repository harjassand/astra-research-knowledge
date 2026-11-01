from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'MANIFEST.json').read_text())
for rel,row in m['files'].items():
 data=(p/rel).read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],rel
print(json.dumps({'status':'PASS','verified_payload_files':len(m['files']),'scope':'checkpoint integrity only'}))
