from pathlib import Path
import hashlib,tempfile,shutil,subprocess,sys,os,resource,time,json,platform
b=Path(__file__).resolve().parent
manifest=b/'SHA256SUMS'
def verify():
 for l in manifest.read_text().splitlines():
  h,n=l.split('  ',1);assert hashlib.sha256((b/n).read_bytes()).hexdigest()==h,n
verify()
assert hashlib.sha256((b/'preserved/Astra_Amplification_Cycle7_DOTS_20261022.zip').read_bytes()).hexdigest()=='36dad04ccb00458636d690d4bbc2bb8de35c67ca97dbaa02e6785b31ccbf2712'
steps=['absorption_bound/check_bound.py','pilot_reconstruction/reconstruct.py','pilot_reconstruction/feedback_check.py','pilot_reconstruction/check_absorption_independently.py']
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3));resource.setrlimit(resource.RLIMIT_CPU,(25,25))
t=time.perf_counter();runs=[]
with tempfile.TemporaryDirectory(prefix='dots_cycle8_receive_') as tmp:
 p=Path(tmp)/'nitrogen_cycle8_20261022';shutil.copytree(b/'nitrogen_cycle8_20261022',p)
 for step in steps:
  start=time.perf_counter();r=subprocess.run([sys.executable,str(p/step)],cwd=tmp,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},preexec_fn=limits,capture_output=True,text=True,timeout=30)
  runs.append({'entrypoint':step,'exit_code':r.returncode,'elapsed_s':time.perf_counter()-start,'stdout':r.stdout,'stderr':r.stderr})
  if r.returncode:break
verify()
import scipy,mpmath
out={'status':'passed' if len(runs)==4 and all(r['exit_code']==0 for r in runs) else 'failed','scope':'Only new finite Cycle8 calculations, not physical admission, old science or evaluator replay','runs':runs,'elapsed_s':time.perf_counter()-t,'peak_RSS_self_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'peak_RSS_children_KiB_Linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'python':platform.python_version(),'scipy':scipy.__version__,'mpmath':mpmath.__version__,'address_limit_GiB':2,'wall_limit_per_child_s':30,'total_research_cost':'unknown'}
(b/'RELOCATION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='runs'},indent=2));assert out['status']=='passed'
