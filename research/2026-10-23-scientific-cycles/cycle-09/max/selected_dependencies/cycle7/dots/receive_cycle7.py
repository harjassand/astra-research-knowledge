"""Relocated finite Cycle7 calculations; no historical scientific replay."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,hashlib,resource,time,os,platform
base=Path(__file__).resolve().parent
manifest=base/'SHA256SUMS'
def verify():
 for line in manifest.read_text().splitlines():
  h,n=line.split('  ',1)
  assert hashlib.sha256((base/n).read_bytes()).hexdigest()==h,n
verify()
assert hashlib.sha256((base/'preserved/Astra_Amplification_Cycle6_DOTS_20261022.zip').read_bytes()).hexdigest()=='965c841f9f2f9a7021477beae5cbc2d510c647d621a235005fe4b6a62ea6d26e'
steps=['heat_challenge/verify_thermo_bounds.py','heat_challenge/check_ledger.py','parent_checks/exact_heat_check.py','oxidation_operation/conditioner_bound.py','conditioning_independent/independent_check.py']
start=time.perf_counter();runs=[]
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
 resource.setrlimit(resource.RLIMIT_CPU,(25,25))
with tempfile.TemporaryDirectory(prefix='dots_cycle7_receive_') as tmp:
 dst=Path(tmp)/'nitrogen_cycle7_20261022';shutil.copytree(base/'nitrogen_cycle7_20261022',dst)
 for step in steps:
  t=time.perf_counter();r=subprocess.run([sys.executable,str(dst/step)],cwd=tmp,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},preexec_fn=limits,capture_output=True,text=True,timeout=30)
  runs.append({'entrypoint':step,'exit_code':r.returncode,'elapsed_s':time.perf_counter()-t,'stdout':r.stdout,'stderr':r.stderr})
  if r.returncode:break
 # Scientific assertions inside scripts and independent direct-X comparison all run in the fresh copy.
 out={'status':'passed' if len(runs)==5 and all(r['exit_code']==0 for r in runs) else 'failed','scope':'Only new finite Cycle7 derivations/calculations; not physical validation','runs':runs,'elapsed_s':time.perf_counter()-start,'peak_RSS_self_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'peak_RSS_children_KiB_Linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'python':platform.python_version(),'address_limit_GiB':2,'wall_limit_per_child_s':30,'total_research_cost':'unknown'}
verify()
(base/'RELOCATION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2))
assert out['status']=='passed'
