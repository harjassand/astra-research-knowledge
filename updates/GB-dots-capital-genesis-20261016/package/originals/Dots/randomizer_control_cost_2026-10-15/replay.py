"""Portable offline replay: two suites; no installations or network operations."""
from pathlib import Path
import sys,os,json,math,tempfile,subprocess,shutil,time,resource,re
ROOT=Path(__file__).resolve().parent
SUITES=[('control_cost/check_control_cost.py','checks.json'),('reference/check_direct_fourier.py','direct_fourier_verification.txt')]
def compare(a,b,path=''):
 if isinstance(a,dict):
  assert set(a)==set(b),(path,'keys')
  for k in a:compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),(path,'length')
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif isinstance(a,(int,float)):
  assert math.isclose(a,b,rel_tol=1e-8,abs_tol=3e-13),(path,a,b)
 else:assert a==b,(path,a,b)
start=time.monotonic();cpu0=resource.getrusage(resource.RUSAGE_CHILDREN);records=[]
with tempfile.TemporaryDirectory(prefix='control_cost_replay_') as td:
 for rel,expected in SUITES:
  src=ROOT/rel;work=Path(td)/src.parent.name;work.mkdir(exist_ok=True);shutil.copy2(src,work/src.name)
  env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
  p=subprocess.run([sys.executable,str(work/src.name)],cwd=work,env=env,text=True,capture_output=True,timeout=60)
  assert p.returncode==0,(rel,p.stdout,p.stderr)
  saved=src.with_name(expected)
  if expected.endswith('.json'):compare(json.loads(saved.read_text()),json.loads((work/expected).read_text()),rel)
  else:
   assert 'PASS' in p.stdout
   nums=lambda s:[float(v) for v in re.findall(r'(?<![A-Za-z_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?',s)]
   compare(nums(saved.read_text()),nums(p.stdout),rel+' printed values')
  records.append({'script':rel,'saved_result':str(saved.relative_to(ROOT)),'status':'PASS'})
cpu1=resource.getrusage(resource.RUSAGE_CHILDREN)
result={'status':'PASS','suite_count':len(records),'suites':records,'wall_seconds':time.monotonic()-start,'child_CPU_seconds':cpu1.ru_utime+cpu1.ru_stime-cpu0.ru_utime-cpu0.ru_stime,'network_used':False,'software_installed':False}
print(json.dumps(result,indent=2))
if '--record' in sys.argv:(ROOT/'REPLAY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
