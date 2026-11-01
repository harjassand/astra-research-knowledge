"""Replay only into a fresh explicitly supplied output directory."""
from pathlib import Path
import hashlib,json,subprocess,os,sys,time
ROOT=Path(__file__).resolve().parent
OUT=Path(os.environ['AUTHOR_OUTPUT_DIR']).resolve();OUT.mkdir(parents=True,exist_ok=True)
assert OUT!=ROOT and not any(OUT.iterdir()),'fresh external output required'
manifest=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
for name,item in manifest['files'].items():
 p=ROOT/name;data=p.read_bytes();assert len(data)==item['bytes']and hashlib.sha256(data).hexdigest()==item['sha256'],name
rows=[]
for script,reference in [('aggregate_mass.py','tail_plan.json'),('demo_symbolic.py','aggregate_symbolic_demo.json'),('check_aggregate_mass.py','aggregate_mass_results.json'),('structural_controls.py','structural_results.json')]:
 start=time.monotonic();p=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (OUT/(script+'.stdout')).write_bytes(p.stdout);(OUT/(script+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==0 and not p.stderr and p.stdout==(ROOT/reference).read_bytes(),(script,p.returncode,p.stderr)
 rows.append(dict(script=script,reference=reference,byte_identical=True,sha256=hashlib.sha256(p.stdout).hexdigest(),seconds=time.monotonic()-start))
 print('PASS',script,flush=True)
(OUT/'AUTHOR_REPLAY.json').write_text(json.dumps(dict(status='PASS_AUTHOR_SOURCE_REPLAY',rows=rows),indent=2)+'\n')
