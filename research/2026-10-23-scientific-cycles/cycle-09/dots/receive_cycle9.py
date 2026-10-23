"""Finite new calculations in a temporary relocated copy; no network or predecessor replay."""
from pathlib import Path
import tempfile,shutil,subprocess,os,sys,time,json,resource,hashlib
p=Path(__file__).resolve().parent
manifest=p/'SHA256SUMS'
if manifest.exists():
 for line in manifest.read_text().splitlines():
  h,n=line.split('  ',1);assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
jobs=['native_reconstruction/reconstruct_dataset.py','native_reconstruction/profile_finite_record.py','native_reconstruction/material_bounds.py','native_reconstruction/baseline_sensitivity.py','tracer_independent/calculate_bounds.py','tracer_independent/check_native_receipt.py']
def limits():resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,)*2)
start=time.perf_counter();receipt=[]
with tempfile.TemporaryDirectory(prefix='dots_cycle9_') as d:
 dst=Path(d)/'work';shutil.copytree(p/'nitrogen_cycle9_20261022',dst)
 for j in jobs:
  t=time.perf_counter();r=subprocess.run([sys.executable,str(dst/j)],cwd=dst,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,timeout=30,preexec_fn=limits)
  receipt.append({'entrypoint':j,'exit_code':r.returncode,'wall_s':time.perf_counter()-t,'stdout':r.stdout,'stderr':r.stderr})
  if r.returncode:break
out={'all_pass':len(receipt)==len(jobs) and all(x['exit_code']==0 for x in receipt),'total_receiving_wall_s':time.perf_counter()-start,'children_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'per_child_address_space_limit_bytes':2*1024**3,'per_child_wall_limit_s':30,'scope':'New finite replay, not experiment, old trajectory, discovery-cost estimate or physical qualification','jobs':receipt}
print(json.dumps({k:v for k,v in out.items() if k!='jobs'},indent=2));sys.exit(0 if out['all_pass'] else 1)
