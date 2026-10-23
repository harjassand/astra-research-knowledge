from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
fail=[]
for entry in manifest['payloads']:
 p=root/entry['path']
 if not p.is_file():
  fail.append({'path':entry['path'],'reason':'missing'});continue
 data=p.read_bytes()
 if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
  fail.append({'path':entry['path'],'reason':'identity mismatch'})
result={'status':'PASS' if not fail else 'FAIL','checked_payloads':len(manifest['payloads']),'failures':fail,'scope':'Payload identity only; no mathematical proof or physical operation is certified, and no original scientific calculation is executed.'}
print(json.dumps(result,indent=2))
sys.exit(bool(fail))
