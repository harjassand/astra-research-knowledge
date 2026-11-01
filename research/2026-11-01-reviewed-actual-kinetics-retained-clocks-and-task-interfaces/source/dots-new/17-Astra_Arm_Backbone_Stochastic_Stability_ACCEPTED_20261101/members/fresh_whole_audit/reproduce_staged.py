"""Relocated replay of only the frozen new binding and independent audit inputs."""
from pathlib import Path
import tempfile,hashlib,json,shutil,subprocess,os,sys,time
ROOT=Path(__file__).resolve().parent;b=json.loads((ROOT/'INPUT_BINDING.json').read_text());source=Path(b['source']);stage=Path(tempfile.mkdtemp(prefix='recovered_backbone_audit_',dir='/tmp'));src=stage/'source';audit=stage/'audit';src.mkdir();audit.mkdir()
for name,meta in b['files'].items():
 raw=(source/name).read_bytes();assert len(raw)==meta['bytes']and hashlib.sha256(raw).hexdigest()==meta['sha256'];p=src/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
for name in('independent_backbone.py','fixtures.py','check_components.py','check_raw.py','check_receiving.py'):shutil.copy2(ROOT/name,audit/name)
shutil.copytree(ROOT/'retained',audit/'retained');rows=[]
for script,refs in [('check_components.py',['COMPONENT_RESULTS.json']),('check_raw.py',['RAW_RESULTS.json']),('check_receiving.py',['RECEIVING_RESULTS.json','MAIN_DAG.json'])]:
 t=time.monotonic();p=subprocess.run([sys.executable,str(audit/script)],cwd=audit,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',BACKBONE_SOURCE_DIR=str(src)),capture_output=True)
 (ROOT/('staged_'+script+'.stdout')).write_bytes(p.stdout);(ROOT/('staged_'+script+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==0 and not p.stderr,(script,p.returncode,p.stderr)
 for ref in refs:assert (ROOT/ref).read_bytes()==(audit/ref).read_bytes(),ref
 rows.append(dict(script=script,results_byte_identical=refs,elapsed_seconds=time.monotonic()-t));print('PASS',script,flush=True)
for name,meta in b['files'].items():assert hashlib.sha256((source/name).read_bytes()).hexdigest()==meta['sha256'],name
(ROOT/'STAGED_REPLAY.json').write_text(json.dumps(dict(status='PASS_NEW_BINDING_RELOCATED_REPLAY',source_files=158,frozen_source_unchanged=True,source_dir=str(source),stage_dir=str(stage),rows=rows),indent=2)+'\n')
