"""Reproduce the package without internet or any upstream code dependency."""
from pathlib import Path
import subprocess,sys,os,json,platform,time,resource,hashlib
BASE=Path(__file__).resolve().parents[1]
os.environ['OPENBLAS_NUM_THREADS']='1'; os.environ['OMP_NUM_THREADS']='1'
start=time.perf_counter()
logs=[]
for script in ['compact_model.py','continuum_certificate.py','feasible_witnesses.py','probe_protocols.py']:
 result=subprocess.run([sys.executable,str(BASE/'code'/script)],cwd=BASE,text=True,capture_output=True,check=True,env=os.environ)
 logs.append('### '+script+'\n'+result.stdout+result.stderr)
# The protocol certificates use no mass correction and hence no extra frequencies.
sys.path.insert(0,str(BASE/'code'))
from continuum_certificate import verify
probes=json.loads((BASE/'results/probe_protocols.json').read_text()); out=[]
for p in probes:
 for key in ['lower','upper']:
  v=verify(p['certificate_input'],key,0.,30.); v['protocol']=p['name']; out.append(v)
  if not v['pass']:raise RuntimeError(f"Protocol continuum check failed: {p['name']}, {key}, {v}")
(BASE/'results/probe_protocol_certificates.json').write_text(json.dumps(out,indent=2))
certs=json.loads((BASE/'results/continuum_certificates.json').read_text())
assert all(c['pass'] for c in certs)
# Input checks and algebraic audit tests are independent of optimizer status.
subprocess.run([sys.executable,str(BASE/'code'/'tests.py')],cwd=BASE,check=True,env=os.environ)
import numpy,scipy,mpmath
rr=resource.getrusage(resource.RUSAGE_CHILDREN)
metadata={'date':'2026-10-15','python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,'scipy':scipy.__version__,'mpmath':mpmath.__version__,'end_to_end_seconds':time.perf_counter()-start,'child_user_cpu_seconds':rr.ru_utime,'child_system_cpu_seconds':rr.ru_stime,'largest_child_maxrss_KiB_linux':rr.ru_maxrss,'blas_threads_requested':1,'hardware':'container CPU; not a benchmark against another package','gpu_used':False,'external_code_executed':False,'network_required_for_replay':False,'input_sha256':hashlib.sha256((BASE/'data/cell_001_eis.csv').read_bytes()).hexdigest()}
(BASE/'results/runtime.json').write_text(json.dumps(metadata,indent=2))
(BASE/'results/replay.log').write_text('\n'.join(logs)+'\n'+json.dumps(metadata,indent=2)+'\nALL_CHECKS_PASS\n')
print(json.dumps(metadata,indent=2))
print('ALL_CHECKS_PASS: 4 continuum duals, 4 exact-feasible witnesses, 6 sparse-protocol duals, and unit checks.')
