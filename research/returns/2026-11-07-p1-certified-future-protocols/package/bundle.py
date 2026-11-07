from pathlib import Path
import json,hashlib,zipfile

ROOT=Path(__file__).resolve().parent
WORK=ROOT.parent
old=WORK/'Certified_collective_state_selection_2026-11-07.zip'
old_hash='791c2b69d5c2245e7ae5ce961b80b57a10be9ffbc213dae9b40d44d1aa8e85b1'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert old.is_file() and sha(old)==old_hash
assert old.stat().st_size==12403656
with zipfile.ZipFile(old) as z:assert z.testzip() is None
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json')
manifest={
 'title':'Certified causal protocols from finite experiments',
 'date':'2026-11-07',
 'scientific_scope':'Complete mathematical acquisition-to-parity-game operation with a robustness gap; executed repeated-service safety game; no physical experiment or historical-priority claim',
 'predecessor':{'name':old.name,'bytes':old.stat().st_size,'sha256':old_hash,'preservation':'included unchanged'},
 'astra_pin':'fa4bf6724037a9a52addb4d26607cea2d6164ea8',
 'source_holds':'N1683 and all predecessor holds preserved; no new worker or live-peer transfer',
 'files':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]
}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
out=WORK/'Certified_all_future_protocols_2026-11-07.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files+[ROOT/'MANIFEST.json']:z.write(p,'causal_games/'+str(p.relative_to(ROOT)))
    z.write(old,'predecessors/'+old.name)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert hashlib.sha256(z.read('predecessors/'+old.name)).hexdigest()==old_hash
    members=len(z.namelist())
print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'members':members,'sha256':sha(out),'predecessor_unchanged':True},indent=2))
