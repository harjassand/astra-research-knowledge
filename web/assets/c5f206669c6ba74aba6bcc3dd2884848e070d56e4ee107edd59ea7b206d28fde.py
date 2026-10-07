"""Package new research artifacts, not raw downloaded literature or the prior repo."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
for name in ['research_index.json', 'research_index.txt']:
    shutil.copy2(ROOT / 'work/verification' / name, OUT / name)

selected = []
omitted = []
for p in sorted((ROOT / 'work').rglob('*')):
    if not p.is_file() or p.is_symlink():
        continue
    rel = p.relative_to(ROOT)
    if 'astra-research-knowledge' in rel.parts or '__pycache__' in rel.parts:
        continue
    direct_report = p.suffix == '.md' and p.parent in [ROOT/'work/scouts',ROOT/'work/deep',ROOT/'work/expansion']
    code_or_receipt = p.suffix in {'.py','.json'}
    entry = rel.as_posix() == 'work/RESEARCH_BRIEF.txt'
    index = p.parent == ROOT/'work/verification' and p.name == 'research_index.txt'
    if direct_report or code_or_receipt or entry or index:
        selected.append(p)
    else:
        data=p.read_bytes()
        omitted.append({'path':rel.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})

provenance={
    'prior_repository':{'url':'https://github.com/harjassand/astra-research-knowledge','commit':'1c5743f427b2200d7a1ba188063e5c07053a5744','included':False},
    'scope':'Raw literature/source snapshots omitted from deliverable; reports and provenance JSON retain primary URLs and exact source IDs. Original workspace retains raw files.',
    'omitted_workspace_files':omitted
}
(OUT/'SOURCE_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
output_names=['START_HERE.txt','RESEARCH_STATE.json','RESULT_CARDS.txt','REPRODUCE.txt','research_report.tex','research_index.txt','research_index.json','SOURCE_PROVENANCE.json']
selected.extend(OUT/name for name in output_names)
selected=sorted(set(selected))
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in selected)
(OUT/'MANIFEST.sha256').write_text(manifest)
archive=OUT/'frontier_research_evidence.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in selected:
        z.write(p,p.relative_to(ROOT).as_posix())
    z.write(OUT/'MANIFEST.sha256','outputs/MANIFEST.sha256')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for line in manifest.splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256(z.read(name)).hexdigest()==digest, name
    report_count=sum(name.startswith(('work/scouts/','work/deep/','work/expansion/')) and name.count('/')==2 and name.endswith('.md') for name in z.namelist())
    assert report_count==37, report_count
receipt={
    'archive':archive.name,'bytes':archive.stat().st_size,
    'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
    'members':len(selected)+1,'direct_research_reports':report_count,
    'crc_check':'PASS','manifest_hash_check':'PASS',
    'scope':'Artifact integrity only; not mathematical proof, novelty or external certification.'
}
(OUT/'PACKAGING_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
