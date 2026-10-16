"""Create-only scientific preservation; no Git action and no historical overwrite."""
from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path(__file__).resolve().parents[1];W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016');U=W/'updates/GE-endpoint-exterior-genesis-20261016';D=U/'package/derived';assert not D.exists()
excluded=[];copied=[]
for base in ['root','workers']:
 for p in sorted((R/base).rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(R);parts=rel.parts
  if any(x in {'__pycache__','acquired_excluded_from_publication','sources','acquired_full_texts','third_party_full_texts'} or x.startswith('overlay-stage-') for x in parts) or p.suffix.lower() in {'.pyc','.pdf','.png','.epub'}:
   excluded.append({'path':rel.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'reason':'Third-party acquisition, rendered fulltext/cache, or unpublished metadata stage; preserved through provenance only.'});continue
  if p.is_symlink():raise RuntimeError('No symlink publication: '+str(p))
  target=D/rel;target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();raw=p.read_bytes();target.write_bytes(raw);assert target.read_bytes()==raw
  copied.append({'path':target.relative_to(W).as_posix(),'source':rel.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
for name in ['REPORT.md','CONTINUATION_HANDOFF.md']:
 raw=(R/'root'/name).read_bytes();target=U/name;assert not target.exists();target.write_bytes(raw);copied.append({'path':target.relative_to(W).as_posix(),'source':'root/'+name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
manifest={'schema':'astra.ge-scientific-payload.v1','source_pin':'adb0a306e9bfdc33b9fbd105efb58baed0cc021e','source_preservation_commit':subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip(),'files':copied,'excluded':excluded,'scope':'Byte preservation and explicit publication selection only; mathematical correctness, historical novelty and capability remain separate.'}
(U/'SCIENTIFIC_PAYLOAD_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'files':len(copied),'bytes':sum(x['bytes'] for x in copied),'excluded_files':len(excluded),'dest':str(D)}))
