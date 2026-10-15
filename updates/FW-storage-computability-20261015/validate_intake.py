#!/usr/bin/env python3
"""Verify this intake's provenance, portable references and three own exact replays."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PACKAGE=HERE/'package'
SEED='8ff1d6489f8e917f72bb776b59e25759148b0c6a'
BASE='33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d'
def digest(b):return hashlib.sha256(b).hexdigest()
def git_bytes(rev,path):return subprocess.check_output(['git','show',rev+':'+path],cwd=ROOT)
def rows(data):return [json.loads(x) for x in data.decode().splitlines() if x.strip()]
manifest=json.loads((PACKAGE/'TRANSFER_MANIFEST.json').read_text())
assert manifest['archive_sha256']=='1a9d0397ece268afc78b5df3726ace53ebff0c90a88c4a60b1952522bca70301'
assert manifest['archive_bytes']==78519
for f in manifest['files']:
 b=git_bytes(SEED,str((PACKAGE/f['path']).relative_to(ROOT)))
 assert len(b)==f['bytes'] and digest(b)==f['sha256'],f['path']
assert len(manifest['files'])==23 and sum(f['bytes'] for f in manifest['files'])==182122
# Every final artifact is hashed independently of the original transfer manifest.
final=json.loads((HERE/'INTEGRATED_MANIFEST.json').read_text())
for f in final['files']:
 b=(ROOT/f['path']).read_bytes();assert digest(b)==f['sha256'],f['path']
for p in PACKAGE.rglob('*'):
 if not p.is_file():continue
 s=p.read_text()
 assert not re.search(r'/Users/|/workspace/|/mnt/data/|sandbox:',s),str(p)
 if p.suffix=='.md':
  for target in re.findall(r'(?<![\w_])\[[^\[\]\n]+\]\(([^)]+)\)',s):
   if '://' not in target:
    assert (p.parent/target.split('#')[0]).resolve().is_file(),(p,target)
for ref in json.loads((HERE/'EVIDENCE_REFS.json').read_text())['evidence']:
 p=ROOT/ref['path'];assert digest(p.read_bytes())==ref['sha256']
 assert 1<=ref['lines'][0]<=ref['lines'][1]<=len(p.read_text().splitlines())
# Preserve all prior ledger records and gates; only two reciprocal notices change.
for path,key in [('indexes/claims.jsonl','id'),('indexes/source_metadata.jsonl','source_id'),('frontier/OPEN_PROOF_GATES.jsonl','gate_id'),('agent/SEMANTIC_NOTICES.jsonl','notice_id')]:
 before=rows(git_bytes(BASE,path));after=rows((ROOT/path).read_bytes())
 assert after[:len(before)]==before,path
before=rows(git_bytes(BASE,'frontier/CURRENT_CLAIM_STATUS.jsonl'));after={x['card_id']:x for x in rows((ROOT/'frontier/CURRENT_CLAIM_STATUS.jsonl').read_bytes())}
for old in before:
 new=after[old['card_id']]
 if old['card_id'].split('-')[0] in ('N850','N860'):
  assert {k:v for k,v in old.items() if k!='material_updates'}=={k:v for k,v in new.items() if k!='material_updates'}
  assert new['material_updates'][:-1]==old['material_updates']
 else:assert new==old,old['card_id']
# Execute only the three authorized original standard-library scripts, in a copy.
results=[]
with tempfile.TemporaryDirectory(prefix='astra-storage-replay-') as tmp:
 dest=Path(tmp)/'package';shutil.copytree(PACKAGE,dest)
 for script,receipt in [('heat_certificate/replay.py','heat_certificate/receipt.json'),('heat_certificate/coercivity_replay.py','heat_certificate/coercivity_receipt.json'),('storage_spatial/verify_resource_bounds.py','storage_spatial/resource_receipt.json')]:
  supplied=json.loads((PACKAGE/receipt).read_text())
  proc=subprocess.run([sys.executable,str(dest/script)],cwd=tmp,capture_output=True,text=True,check=True)
  actual=json.loads((dest/receipt).read_text());assert actual==supplied,receipt
  results.append(dict(script=script,receipt=receipt,receipt_sha256=digest((dest/receipt).read_bytes()),matches_supplied_receipt=True,result=json.loads(proc.stdout)))
print(json.dumps(dict(status='PASS',seed_files_verified=23,seed_bytes=182122,prior_records_preserved=True,portable_links=True,replays=results,scientific_validation='Exact finite replay and integration integrity only; not external mathematical validation or storage-value execution.'),indent=2))
