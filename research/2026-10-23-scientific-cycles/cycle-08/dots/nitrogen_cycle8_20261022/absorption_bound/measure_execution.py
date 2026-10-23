"""Run only the new bound check from /tmp, with explicit resource ceilings."""
import os, resource, subprocess, time, json
from pathlib import Path
root=Path(__file__).resolve().parent
limit=2*1024**3

def cap_address_space():
 resource.setrlimit(resource.RLIMIT_AS,(limit,limit))

env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
t0=time.perf_counter()
status='completed'
with (root/'execution.log').open('w') as log:
 try:
  p=subprocess.run(['python',str(root/'check_bound.py')],cwd='/tmp',env=env,stdout=log,stderr=subprocess.STDOUT,timeout=30,preexec_fn=cap_address_space)
  rc=p.returncode
 except subprocess.TimeoutExpired:
  status='wall_timeout';rc=None
elapsed=time.perf_counter()-t0
r=resource.getrusage(resource.RUSAGE_CHILDREN)
report=dict(status=status,exit_status=rc,elapsed_wall_s=elapsed,peak_RSS_KiB=r.ru_maxrss,user_cpu_s=r.ru_utime,system_cpu_s=r.ru_stime,limits=dict(address_space_bytes=limit,wall_s=30),working_directory='/tmp',script='check_bound.py',measurement='Python subprocess timeout; child RLIMIT_AS; resource.getrusage(RUSAGE_CHILDREN), Linux peak RSS in KiB',earlier_measurement_attempt='External /usr/bin/time unavailable; no numerical program executed in that failed measurement attempt.')
(root/'resource_measurement.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if rc!=0: raise SystemExit(1)
