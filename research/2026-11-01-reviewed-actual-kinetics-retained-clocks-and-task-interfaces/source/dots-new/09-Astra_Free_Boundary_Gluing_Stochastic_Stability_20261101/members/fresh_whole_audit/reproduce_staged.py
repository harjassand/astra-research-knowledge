from pathlib import Path
import tempfile,os,shutil,subprocess,json,sys,time,hashlib
HERE=Path(__file__).resolve().parent;SOURCE=Path(os.environ.get('GLUE_SOURCE_DIR',HERE.parent if (HERE.parent/'free_port_glue.py').is_file() else HERE.parent/'stochastic_free_port_glue_pending_20261031')).resolve();OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',HERE)).resolve();OUT.mkdir(parents=True,exist_ok=True)
stage=Path(tempfile.mkdtemp(prefix='free_port_glue_audit_stage_'));base=stage/'preferred';audit=base/'fresh_whole_audit';output=stage/'output';audit.mkdir(parents=True);output.mkdir()
manifest=json.loads((SOURCE/'AUTHOR_MANIFEST.json').read_text())
for name in list(manifest['files'])+['AUTHOR_MANIFEST.json']:
 dest=base/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE/name,dest)
files=['independent_glue_receiver.py','replay_author.py','exercise_independent.py','graph_and_switch_controls.py','wire_and_dependency_controls.py','prior_independent/independent_cover_receiver.py','prior_independent/independent_circuit_receiver.py']
for name in files:
 dest=audit/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HERE/name,dest)
 assert dest.read_bytes()==(HERE/name).read_bytes()
rows=[]
env=dict(os.environ,AUDIT_OUTPUT_DIR=str(output),PYTHONDONTWRITEBYTECODE='1');env.pop('GLUE_SOURCE_DIR',None)
for script in ['replay_author.py','exercise_independent.py','graph_and_switch_controls.py','wire_and_dependency_controls.py']:
 begin=time.monotonic();run=subprocess.run([sys.executable,str(audit/script)],capture_output=True,env=env,cwd=stage)
 (OUT/('staged_'+script+'.stdout.txt')).write_bytes(run.stdout);(OUT/('staged_'+script+'.stderr.txt')).write_bytes(run.stderr)
 assert run.returncode==0 and not run.stderr,(script,run.returncode,run.stderr)
 rows.append(dict(script=script,seconds=time.monotonic()-begin,returncode=run.returncode));print(script,'PASS',flush=True)
def normalized(v):
 if isinstance(v,dict):return {k:normalized(x)for k,x in v.items()if k!='seconds'}
 if isinstance(v,list):return [normalized(x)for x in v]
 return v
for name in ['SOURCE_BINDINGS.json','AUTHOR_REPLAY.json','INDEPENDENT_RESULTS.json','GRAPH_RESULTS.json','WIRE_DEPENDENCY_RESULTS.json']:
 assert normalized(json.loads((output/name).read_text()))==normalized(json.loads((HERE/name).read_text())),name
result=dict(status='PASS_STAGED_REPLAY',stage=str(stage),output=str(output),copied_code_files={name:hashlib.sha256((audit/name).read_bytes()).hexdigest()for name in files},entrypoints=rows,mathematical_results_identical=True,author_three_published_outputs_byte_identical=True,original_evidence_not_overwritten=True)
(OUT/'STAGED_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
