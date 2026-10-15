"""Acquire the report's exact public Git blob; check identity without solving OPF."""
from pathlib import Path
import urllib.request, json, base64, hashlib, datetime, re
ROOT=Path(__file__).resolve().parent
PIN='9b5c0548be7dd4baaa01a8b6359a81d8ec2faf3f'
URL='https://api.github.com/repos/power-grid-lib/pglib-opf/git/blobs/'+PIN
req=urllib.request.Request(URL,headers={'User-Agent':'Astra-exact-reciprocal-audit','Accept':'application/vnd.github+json'})
with urllib.request.urlopen(req,timeout=30) as r:
    body=r.read()
    status=r.status
data=json.loads(body)
assert data['encoding']=='base64'
content=base64.b64decode(data['content'])
actual=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
assert actual==PIN and data['sha']==PIN
first=next(line for line in content.decode().splitlines() if line.startswith('function '))
name=re.search(r'=\s*(\w+)',first).group(1)+'.m'
(ROOT/name).write_bytes(content)
receipt={'url':URL,'http_status':status,'acquired_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'git_blob_sha1_expected':PIN,'git_blob_sha1_actual':actual,'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content),'filename_from_function':name,'first_line':first,'scope':'Exact file identity only. No OPF solve or source package recovery.'}
(ROOT/'PGLIB_ACQUISITION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
