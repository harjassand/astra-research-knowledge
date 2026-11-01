#!/usr/bin/env python3
"""One ordinary fresh replay of the frozen coarse pipeline; no fine solve."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
REL=Path('boundary_clearance_kernel_root_20261101/coarse_cold_algorithm_20261101')
SRC=ROOT/REL
FREEZE='a6e1638f31b6d8055c2e158e4bdbabc0256b2a6c43cf49ea564ce4c1c69b4114'
blob=(SRC/'AUTHOR_FREEZE.json').read_bytes();assert hashlib.sha256(blob).hexdigest()==FREEZE
freeze=json.loads(blob)
checked=[]
for name,item in freeze['files'].items():
    data=(SRC/name).read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'];checked.append(str(REL/name))
for name,item in freeze['old_files_preserved'].items():
    data=(ROOT/name).read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'];checked.append(name)
manifest=json.loads((SRC/'COLD_SOURCE_BINDINGS.json').read_text())
DEST=HERE/'REPLAY_ROOT'
assert not DEST.exists(),'one-run review replay refuses to overwrite prior run'
for row in manifest['files']:
    data=(ROOT/row['path']).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    out=DEST/row['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
for name in ('coarse_clock.py','independent_coarse_verify.py','coarse_windows.py','run_cold.py','COLD_SOURCE_BINDINGS.json'):
    out=DEST/REL/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((SRC/name).read_bytes())
start=time.monotonic_ns()
with (HERE/'FROZEN_PIPELINE_REPLAY.stdout').open('wb') as log:
    proc=subprocess.run([sys.executable,str(DEST/REL/'run_cold.py')],stdout=log,stderr=subprocess.STDOUT)
elapsed=time.monotonic_ns()-start
assert proc.returncode==0,proc.returncode
old=json.loads((SRC/'COARSE_CERTIFICATE.json').read_text());new=json.loads((DEST/REL/'COARSE_CERTIFICATE.json').read_text())
for obj in (old,new):obj.pop('wall_nanoseconds_nonproof')
assert old==new
for name in ('INDEPENDENT_COARSE_CHECK.json','COARSE_WINDOWS.json'):
    assert (SRC/name).read_bytes()==(DEST/REL/name).read_bytes(),name
# Author source preservation is checked again after replay.
for name,item in freeze['files'].items():assert hashlib.sha256((SRC/name).read_bytes()).hexdigest()==item['sha256']
out={'status':'PASS_FRESH_FROZEN_COARSE_PIPELINE_REPLAY','author_freeze_sha256':FREEZE,
     'source_files_verified':len(checked),'runtime_manifest_files':len(manifest['files']),
     'new_review_scalar_passes':3,'new_review_consumer_runs':1,'failed_review_runs':0,
     'fine_scalar_solves':0,'author_files_preserved':True,
     'reference_elapsed_ns_nonproof':elapsed,
     'comparison':'All certificate fields exactly agree except omitted nonproof wall-time field; independent verification and both-window outputs byte-identical.',
     'cost_scope':'This review replay is additional disclosed research work, not an extra mandatory prospective phase or a measured bit bound.'}
(HERE/'FROZEN_PIPELINE_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
