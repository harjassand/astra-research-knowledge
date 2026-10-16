"""Offline replay. Requires an existing Python with NumPy and SciPy; installs nothing."""
from pathlib import Path
import os,sys,tempfile,subprocess,shutil,json,math,time,resource,re
ROOT=Path(__file__).resolve().parent
SKIP={'cpu_seconds','max_rss_KiB','peak_RSS_KiB','reserved_rows_read'}
def compare(a,b,path=''):
 if isinstance(a,dict):
  assert set(a)==set(b),(path,'keys')
  for k in a:
   if k not in SKIP:compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),path
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif isinstance(a,(int,float)):
  assert math.isclose(a,b,rel_tol=1e-8,abs_tol=2e-13),(path,a,b)
 else:assert a==b,(path,a,b)
checks=[('tracked_control/check_direct_fourier.py','direct_fourier_verification.txt'),('tracked_control/check_bridge.py','exact_matrix_check.json'),('single/check.py','checks.json'),('single/serial_check.py','serial_checks.json'),('joint/group_check.py','group_checks.json'),('independent/grouped_independent_check.py','grouped_independent_check.json'),('independent/check_endpoint_subset.py','endpoint_subset_verification.txt'),('scope/check_zero_syndrome_logical.py','zero_syndrome_verification.txt')]
if '--search' in sys.argv: checks += [('joint/search.py','search_result.json'),('joint/check_majorant.py','majorant_checks.json')]
start=time.monotonic();cpu0=resource.getrusage(resource.RUSAGE_CHILDREN);records=[]
with tempfile.TemporaryDirectory(prefix='joint_syndrome_replay_') as td:
 for rel,expected in checks:
  src=ROOT/rel;work=Path(td)/src.parent.name;work.mkdir(exist_ok=True);shutil.copy2(src,work/src.name)
  env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
  p=subprocess.run([sys.executable,str(work/src.name)],cwd=work,env=env,text=True,capture_output=True,timeout=60)
  assert p.returncode==0,(rel,p.stdout,p.stderr)
  saved=src.with_name(expected)
  if expected.endswith('.json'):compare(json.loads(saved.read_text()),json.loads((work/expected).read_text()))
  else:
   assert 'PASS' in p.stdout
   nums=lambda s:[float(v) for v in re.findall(r'(?<![A-Za-z_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?',s)]
   compare(nums(saved.read_text()),nums(p.stdout),rel+' stdout numerical values')
  records.append({'script':rel,'saved_result':str(saved.relative_to(ROOT)),'status':'PASS'})
cpu1=resource.getrusage(resource.RUSAGE_CHILDREN)
result={'status':'PASS','checks':records,'search_replayed':'--search' in sys.argv,'wall_seconds':time.monotonic()-start,'child_CPU_seconds':cpu1.ru_utime+cpu1.ru_stime-cpu0.ru_utime-cpu0.ru_stime,'network_used':False,'software_installed':False}
print(json.dumps(result,indent=2))
if '--record' in sys.argv:(ROOT/'REPLAY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
