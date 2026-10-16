"""Offline, read-only packet replay. Only newly authored audit scripts execute."""
from pathlib import Path
import json,hashlib,tempfile,shutil,subprocess,sys,time,os
P=Path(__file__).resolve().parent
manifest=json.loads((P/'MANIFEST_SHA256.json').read_text())
def verify():
 for name,h in manifest.items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h,name
verify();start=time.monotonic();steps=[]
with tempfile.TemporaryDirectory(prefix='measured-randomizer-replay-') as temp:
 Q=Path(temp)/'packet';shutil.copytree(P,Q);env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
 for script in ['validate_counts.py','independent_audit.py']:
  r=subprocess.run([sys.executable,str(Q/script)],cwd=Q,env=env,capture_output=True,text=True,timeout=60)
  assert r.returncode==0,(script,r.stdout,r.stderr)
  steps.append({'script':script,'exit_code':r.returncode});print('PASS '+script)
 for name in ['contract_validation.json','direct_count_examples.csv','all_pure_power_return_counts.csv','all_pure_power_return_summary.csv','pure_power_selection_validation.json','independent_audit_results.json']:
  assert (P/name).read_bytes()==(Q/name).read_bytes(),('Replay mismatch',name)
 for name,h in manifest.items():
  assert hashlib.sha256((Q/name).read_bytes()).hexdigest()==h,('Unexpected mutation',name)
verify();print(json.dumps({'status':'PASS','manifest_files':len(manifest),'reproduced_outputs':6,'comparison':'exact bytes','originals_and_packet_unchanged':True,'author_code_executed':False,'new_fits_or_tests':False,'steps':steps,'elapsed_seconds':round(time.monotonic()-start,4),'python':sys.version},indent=2))
