from pathlib import Path
import json,hashlib,zipfile
root=Path(__file__).resolve().parents[3];b=root/'work/physical-cooling-thermal-service-20261107';out=root/'outputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[p for p in b.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.venv','__pycache__','.git']) and p.name!='.DS_Store']
for name in ['PHYSICAL_COOLING_THERMAL_SERVICE_RESEARCH_DOSSIER.md','PHYSICAL_COOLING_THERMAL_SERVICE_THEOREM_LEDGER.json','PHYSICAL_COOLING_THERMAL_SERVICE_VALIDATION.json']:
 paths.append(out/name)
for pin in json.loads((b/'sources/INITIAL_SOURCE_PINS.json').read_text()):
 if 'original' in pin:paths.append(root/pin['original'])
old=out/'PROTECTED_QUANTUM_PROCESSING_RESEARCH_RECORD.zip'
if old.exists():paths.append(old)
paths=sorted(set(paths));records=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths]
manifest=out/'PHYSICAL_COOLING_THERMAL_SERVICE_RECORD_MANIFEST.json'
manifest.write_text(json.dumps({'date':'2026-11-07','scope':'Research evidence; no priority or physical-validation certification','files':records},indent=2)+'\n')
paths.append(manifest)
archive=out/'PHYSICAL_COOLING_THERMAL_SERVICE_RESEARCH_RECORD.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,str(p.relative_to(root)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for r in records:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
receipt={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive),'entries':len(paths),'roundtrip_hashes':'PASS','manifest_sha256':sha(manifest)}
(out/'PHYSICAL_COOLING_THERMAL_SERVICE_ARCHIVE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
