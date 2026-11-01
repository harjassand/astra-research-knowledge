"""Fresh-output preflight for the NEW recovered source version."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent;OUT=Path(os.environ['AUTHOR_OUTPUT_DIR']).resolve();OUT.mkdir(parents=True,exist_ok=True)
assert OUT!=ROOT and not any(OUT.iterdir()),'empty external output directory required'
m=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
for n,w in m['files'].items():
 b=(ROOT/n).read_bytes();assert len(b)==w['bytes']and hashlib.sha256(b).hexdigest()==w['sha256'],n
sys.path.insert(0,str(ROOT));import arm_backbone as B
raw=B.fixture();c=B.construct(raw,2);rows=[]
for ref,b in [('arm_backbone_certificate.json',(B.G.canonical(c)+'\n').encode()),('arm_backbone_expression.json',(B.G.canonical(B.certificate_expressions(raw,c))+'\n').encode())]:
 assert b==(ROOT/ref).read_bytes();(OUT/ref).write_bytes(b);rows.append(dict(reference=ref,byte_identical=True,sha256=hashlib.sha256(b).hexdigest()))
for script,ref in [('test_components.py','component_results.json'),('test_raw_and_production.py','raw_production_results.json'),('test_symbolic_and_parameters.py','symbolic_parameter_results.json')]:
 start=time.monotonic();p=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=1200)
 (OUT/(script+'.stdout')).write_bytes(p.stdout);(OUT/(script+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==0 and not p.stderr and p.stdout==(ROOT/ref).read_bytes(),(script,p.returncode,p.stderr)
 rows.append(dict(script=script,reference=ref,byte_identical=True,sha256=hashlib.sha256(p.stdout).hexdigest(),seconds=time.monotonic()-start));print('PASS',script,flush=True)
for n,w in m['files'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==w['sha256'],n
(OUT/'AUTHOR_PREFLIGHT.json').write_text(json.dumps(dict(status='PASS_NEW_RECOVERED_AUTHOR_PREFLIGHT',historical_source_identity_claimed=False,independent_whole_acceptance=False,rows=rows),indent=2)+'\n')
