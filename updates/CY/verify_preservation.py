#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2]
r=json.loads((ROOT/'updates/CY/INTEGRITY.json').read_text()); p=ROOT/r['source_root']
actual={x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file()}
if actual!=set(r['source_files']): raise SystemExit('expanded source membership mismatch')
for rel,m in r['source_files'].items():
 b=(p/rel).read_bytes()
 if len(b)!=m['bytes'] or hashlib.sha256(b).hexdigest()!=m['sha256'] or len(b.decode('utf8').splitlines())!=m['lines']: raise SystemExit('expanded source mismatch: '+rel)
zpath=ROOT/r['bundle']['path']; b=zpath.read_bytes()
if len(b)!=r['bundle']['bytes'] or hashlib.sha256(b).hexdigest()!=r['bundle']['sha256']: raise SystemExit('bundle hash/size mismatch')
with zipfile.ZipFile(zpath) as z:
 if z.testzip() is not None: raise SystemExit('bundle CRC error')
 manifest=json.loads(z.read('landmark_capability/MANIFEST.json'))
 for x in manifest['files']:
  b=z.read('landmark_capability/'+x['path'])
  if hashlib.sha256(b).hexdigest()!=x['sha256'] or len(b)!=x['bytes'] or b!=(p/x['path']).read_bytes(): raise SystemExit('bundle/extraction mismatch: '+x['path'])
print(json.dumps({'intake_id':'CY','expanded_files':len(actual),'result':'PASS','research_code_executed':False},indent=2))
