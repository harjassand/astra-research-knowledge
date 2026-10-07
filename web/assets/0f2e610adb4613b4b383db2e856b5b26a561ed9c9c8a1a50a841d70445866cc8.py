"""Package scientific artifacts, excluding environments and the entire prior corpus."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
SKIP_DIRS = {'.git', '.venv', 'venv', 'uv-cache', 'node_modules', '__pycache__', '.cache'}
SKIP_FILES = {'.DS_Store'}
files = set()

def add_tree(relative):
    for current, dirs, names in os.walk(ROOT / relative):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not (Path(current)/d).is_symlink()]
        for name in names:
            p = Path(current)/name
            if name not in SKIP_FILES and not p.is_symlink() and p.suffix not in {'.pyc','.pyo'}:
                files.add(p.relative_to(ROOT).as_posix())

for d in ['work/agents','work/sources','work/state','work/root_certificate_replay','work/root_final_certificate_replay']:
    add_tree(d)
for p in (ROOT/'work').iterdir():
    if p.is_file() and not p.is_symlink():
        files.add(p.relative_to(ROOT).as_posix())
for name in ['00_START_HERE.txt','01_CORE.txt','AGENTS.md','EXPORT_SCOPE.txt','UPDATE_PROTOCOL.txt','README.md']:
    files.add('work/astra/'+name)
for p in OUT.iterdir():
    if p.is_file() and p.name not in {'research_evidence.zip','research_evidence_manifest.json','research_evidence.sha256'}:
        files.add(p.relative_to(ROOT).as_posix())

required = ['work/agents/quantum_coding/nonnegative_gbs_audit.md',
            'work/agents/reaction_control_prior/FINAL_REVIEW.md',
            'outputs/RESEARCH_STATE.txt','outputs/RESEARCH_INDEX.json']
for p in required:
    assert p in files and (ROOT/p).is_file(), p
rows=[]
for name in sorted(files):
    data=(ROOT/name).read_bytes()
    rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
manifest={
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Scientific snapshot. Hashes and CRCs verify integrity, not correctness or priority.',
 'source_pins':{'astra':'2aa99b272ec720af587cf6cd6fb1822e15433ce1',
                'openai_math':'adc7f1241b42e322a6451854ab7e4b4c146bf78a'},
 'exclusions':['runtime environments and dependency caches','Git internals','full Astra corpus clone','user memory files'],
 'files':rows}
manifest_data=(json.dumps(manifest,indent=2)+'\n').encode()
(OUT/'research_evidence_manifest.json').write_bytes(manifest_data)
archive=OUT/'research_evidence.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for row in rows:
        data=(ROOT/row['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['sha256'], 'File changed during snapshot: '+row['path']
        z.writestr(row['path'],data)
    z.writestr('MANIFEST.json',manifest_data)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(OUT/'research_evidence.sha256').write_text(digest+'  research_evidence.zip\n')
print(json.dumps({'files':len(rows),'source_bytes':sum(r['bytes'] for r in rows),
                  'archive_bytes':archive.stat().st_size,'sha256':digest}))
