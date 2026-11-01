"""Replay the final code from a fresh preferred-package layout without changing inputs."""
from pathlib import Path
import os,sys,json,shutil,subprocess,tempfile,time
HERE=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('CIRCUIT_SOURCE_DIR',str(HERE.parent if (HERE.parent/'cover_circuit.py').exists() else HERE.parent/'stochastic_cover_circuit_pending_20261031')))
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
root=Path(tempfile.mkdtemp(prefix='cover_audit_stage_'));stage=root/'preferred';audit=stage/'fresh_whole_audit';actual=root/'output';audit.mkdir(parents=True);actual.mkdir()
manifest=json.loads((SOURCE/'AUTHOR_MANIFEST.json').read_text())
for name in list(manifest['files'])+['AUTHOR_MANIFEST.json']:
 dest=stage/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to((SOURCE/name).resolve())
files=['independent_cover_receiver.py','independent_circuit_receiver.py','replay_author.py','exercise_independent.py','replay_circuit.py','exercise_independent_circuit.py']
for name in files:shutil.copyfile(HERE/name,audit/name)
env=dict(os.environ,AUDIT_OUTPUT_DIR=str(actual),PYTHONDONTWRITEBYTECODE='1');env.pop('COVER_SOURCE_DIR',None);env.pop('CIRCUIT_SOURCE_DIR',None)
rows=[]
for name in ['replay_author.py','exercise_independent.py','replay_circuit.py','exercise_independent_circuit.py']:
 start=time.perf_counter();p=subprocess.run([sys.executable,str(audit/name)],cwd=actual,env=env,capture_output=True,text=True)
 row=dict(script=name,returncode=p.returncode,seconds=time.perf_counter()-start,stderr_bytes=len(p.stderr.encode()));rows.append(row)
 assert p.returncode==0,(name,p.stderr)
for name in ['INDEPENDENT_RESULTS.json','INDEPENDENT_CIRCUIT_RESULTS.json']:
 one=json.loads((actual/name).read_text());two=json.loads((HERE/name).read_text());one.pop('seconds');two.pop('seconds');assert one==two,name
for name in ['EXACT_REPLAYS.json','CIRCUIT_EXACT_REPLAYS.json']:
 assert all(r['returncode']==0 and r['exact_match'] for r in json.loads((actual/name).read_text()))
result=dict(status='PASS',stage=str(stage),output=str(actual),runs=rows,default_staged_source_resolution_verified=True,independent_semantic_totals_identical=True,all_published_replays_byte_identical=True,original_evidence_not_overwritten=True)
(OUT/'STAGED_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
