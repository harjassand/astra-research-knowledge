"""Verify two immutable extractions; assemble/replay only in fresh /tmp."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
assert len(sys.argv)==2,'supply the exact accepted aggregate extraction directory'
BASE=Path(sys.argv[1]).resolve();sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text());dep=json.loads((ROOT/'DEPENDENCY_BINDING.json').read_text())['members']
for n,w in m['members'].items():
 b=(ROOT/n).read_bytes();assert len(b)==w['bytes']and sha(b)==w['sha256'],n
for n,w in dep.items():
 rel=n.removeprefix('frozen_aggregate/');b=(BASE/rel).read_bytes();assert len(b)==w['bytes']and sha(b)==w['sha256'],n
rows=[]
with tempfile.TemporaryDirectory(prefix='astra_accepted_backbone_',dir='/tmp')as td:
 dst=Path(td)/'source';dst.mkdir()
 for n in m['strict_allowlist']:
  p=dst/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/n).read_bytes())
 for n in dep:
  p=dst/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((BASE/n.removeprefix('frozen_aggregate/')).read_bytes())
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','BACKBONE_SOURCE_DIR':str(dst)}
 ao=Path(td)/'author_output';ao.mkdir()
 p=subprocess.run([sys.executable,str(dst/'replay_author.py')],cwd=dst,capture_output=True,check=True,timeout=1200,env={**env,'AUTHOR_OUTPUT_DIR':str(ao)});assert not p.stderr,p.stderr
 ar=json.loads((ao/'AUTHOR_PREFLIGHT.json').read_text());assert len(ar['rows'])==5 and all(z['byte_identical']for z in ar['rows']);rows.append(dict(script='replay_author.py',five_outputs_byte_identical=True))
 for script,refs in [('check_components.py',['COMPONENT_RESULTS.json']),('check_raw.py',['RAW_RESULTS.json']),('check_receiving.py',['RECEIVING_RESULTS.json','MAIN_DAG.json'])]:
  p=subprocess.run([sys.executable,str(dst/'fresh_whole_audit'/script)],cwd=dst,capture_output=True,check=True,timeout=1200,env=env);assert not p.stderr,(script,p.stderr)
  for ref in refs:assert(dst/'fresh_whole_audit'/ref).read_bytes()==(ROOT/'fresh_whole_audit'/ref).read_bytes(),(script,ref)
  rows.append(dict(script=script,byte_identical=refs))
for n,w in m['members'].items():assert sha((ROOT/n).read_bytes())==w['sha256'],n
for n,w in dep.items():assert sha((BASE/n.removeprefix('frozen_aggregate/')).read_bytes())==w['sha256'],n
print(json.dumps(dict(status='PASS_EXTRACTED_ACCEPTED_EXTENSION_REPLAY',required_base_members=142,new_audit_members=48,rows=rows,originals_unchanged=True,no_upload=True),indent=2))
