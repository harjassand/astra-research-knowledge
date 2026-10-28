"""Package this completed research boundary without changing predecessor artifacts."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'Astra_P2_Continuum_Instrument_20261028.zip'
items=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p.name=='MANIFEST.json': continue
 items.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={'date':'2026-10-28','package':'Astra P2 continuum instrument successor','files':items,
 'scope':'All listed artifacts are preserved at their stated scientific and review scopes; manifest itself excluded from self-hashing.'}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for entry in items: z.write(ROOT/entry['path'],arcname='Astra_P2_Continuum_Instrument/'+entry['path'])
 z.write(ROOT/'MANIFEST.json',arcname='Astra_P2_Continuum_Instrument/MANIFEST.json')
with zipfile.ZipFile(OUT) as z:
 for entry in items:
  assert hashlib.sha256(z.read('Astra_P2_Continuum_Instrument/'+entry['path'])).hexdigest()==entry['sha256'],entry['path']
print(json.dumps({'archive':str(OUT),'members':len(items)+1,'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
