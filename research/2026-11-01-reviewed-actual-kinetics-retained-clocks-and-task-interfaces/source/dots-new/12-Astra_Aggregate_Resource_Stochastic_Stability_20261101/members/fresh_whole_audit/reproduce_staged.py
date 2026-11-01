"""Strict source-bound relocation replay. No write to frozen inputs."""
from pathlib import Path
import tempfile,shutil,subprocess,json,os,hashlib,time,sys
ROOT=Path(__file__).resolve().parent
binding=json.loads((ROOT/'INPUT_BINDING.json').read_text());source=Path(binding['source'])
stage=Path(tempfile.mkdtemp(prefix='aggregate_resource_staged_',dir='/tmp'));src=stage/'source';src.mkdir();audit=stage/'audit';audit.mkdir()
for name,meta in binding['verified_files'].items():
 data=(source/name).read_bytes();assert len(data)==meta['bytes']and hashlib.sha256(data).hexdigest()==meta['sha256'];dest=src/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
for name in ('independent_aggregate_receiver.py','exercise_independent.py','graph_domain_controls.py','nested_fractional_controls.py'):shutil.copy2(ROOT/name,audit/name)
shutil.copytree(ROOT/'retained_independent',audit/'retained_independent')
rows=[]
for script,refs in [('exercise_independent.py',('INDEPENDENT_RESULTS.json',)),('graph_domain_controls.py',('GRAPH_DOMAIN_RESULTS.json',)),('nested_fractional_controls.py',('NESTED_FRACTIONAL_RESULTS.json','MAIN_NESTED_AST.json'))]:
 start=time.monotonic();p=subprocess.run([sys.executable,str(audit/script)],cwd=audit,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',AGGREGATE_SOURCE_DIR=str(src)),capture_output=True)
 (ROOT/('staged_'+script+'.stdout')).write_bytes(p.stdout);(ROOT/('staged_'+script+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==0 and not p.stderr,(script,p.returncode,p.stderr)
 for ref in refs:assert (audit/ref).read_bytes()==(ROOT/ref).read_bytes(),ref
 rows.append(dict(script=script,exit_code=0,byte_identical=list(refs),seconds=time.monotonic()-start));print('PASS',script,flush=True)
# Recheck the source after complete replay, including binding members.
for name,meta in binding['verified_files'].items():
 data=(source/name).read_bytes();assert len(data)==meta['bytes']and hashlib.sha256(data).hexdigest()==meta['sha256']
res=dict(status='PASS_RELOCATED_INDEPENDENT_REPLAY',frozen_source_unchanged=True,bound_source_files=len(binding['verified_files']),rows=rows,staging_directory=str(stage))
(ROOT/'STAGED_REPLAY.json').write_text(json.dumps(res,indent=2)+'\n')
