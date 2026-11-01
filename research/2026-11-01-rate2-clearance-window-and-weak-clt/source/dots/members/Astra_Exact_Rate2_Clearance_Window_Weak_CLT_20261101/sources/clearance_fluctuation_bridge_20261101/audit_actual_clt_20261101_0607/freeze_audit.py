from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
out=here/'AUDIT_SHA256.json'
if out.exists():raise SystemExit('Refusing to overwrite an existing audit freeze')
files=[]
for p in sorted(here.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p.name=='FINAL_VERIFICATION.json':continue
 data=p.read_bytes();files.append({'path':str(p.relative_to(here)),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
out.write_text(json.dumps({'status':'INDEPENDENT_ACTUAL_WEAK_CLT_PASS','source_sha256':'4b09204361aee3b35adceaa148fcbca560c1b07d53720c803f36f82f5d60138a','author_freeze_sha256':'fd48100bccba41d7df3cc777fe96a717f74746bf0c52354aec0cba8dda11a022','files':files},indent=2)+'\n')
print(json.dumps({'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':len(files)},indent=2))
