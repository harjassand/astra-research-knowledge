"""Replay selected finite diagnostics in a temporary copy; this is not proof validation."""
from pathlib import Path
import json,sys,shutil,tempfile,subprocess,time,hashlib,argparse
base=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--integrity-only',action='store_true')
args=parser.parse_args()
manifest=json.loads((base/'MANIFEST.json').read_text())
errors=[]
for entry in manifest['files']:
 p=base/entry['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:errors.append(entry['path'])
if errors:raise SystemExit('Integrity failures: '+repr(errors))
print('Archive file hashes match. This does not validate the mathematical claims.')
if args.integrity_only:raise SystemExit(0)
plan=json.loads((base/'work/REPLAY_PLAN.json').read_text())
results=[]
with tempfile.TemporaryDirectory(prefix='astra-research-replay-') as tmp:
 tmp=Path(tmp);shutil.copytree(base/'work',tmp/'work')
 for job in plan['checks']:
  started=time.monotonic()
  try:
   run=subprocess.run([sys.executable,job['script']],cwd=tmp,capture_output=True,text=True,timeout=job.get('timeout_seconds',180))
   row={'script':job['script'],'exit_code':run.returncode,'elapsed_seconds':time.monotonic()-started,'stdout_tail':run.stdout[-3000:],'stderr_tail':run.stderr[-3000:]}
  except subprocess.TimeoutExpired as e:
   row={'script':job['script'],'exit_code':None,'elapsed_seconds':time.monotonic()-started,'error':'timeout'}
  results.append(row);print(('PASS' if row.get('exit_code')==0 else 'FAIL')+' '+job['script'])
 result={'scope':'Independent rerun of selected finite diagnostics; not analytic proof, formal verification or novelty certification.','python':sys.version,'results':results}
 Path('REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
if any(x.get('exit_code')!=0 for x in results):raise SystemExit(1)
print('Selected finite diagnostics completed. REPLAY_RESULTS.json was written in the calling directory.')
