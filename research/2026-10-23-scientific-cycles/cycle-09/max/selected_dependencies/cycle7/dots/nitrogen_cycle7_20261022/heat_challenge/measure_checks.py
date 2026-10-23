"""Measure each check in a fresh wrapper process; Linux ru_maxrss is KiB."""
import json,resource,subprocess,sys,time
from pathlib import Path
p=Path(__file__).parent
name=sys.argv[1]
t0=time.perf_counter()
r=subprocess.run([sys.executable,str(p/name)],capture_output=True,text=True)
elapsed=time.perf_counter()-t0
u=resource.getrusage(resource.RUSAGE_CHILDREN)
(p/(Path(name).stem+'_output.txt')).write_text(r.stdout+r.stderr)
result={'command':[sys.executable,name],'exit_code':r.returncode,'elapsed_seconds':elapsed,'user_cpu_seconds':u.ru_utime,'system_cpu_seconds':u.ru_stime,'max_resident_set_KiB':u.ru_maxrss,'scope':'One fresh Python child execution; excludes web lookup, reasoning, source retrieval, other workers and tool overhead.'}
(p/(Path(name).stem+'_resources.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
if r.returncode: print(r.stderr)
raise SystemExit(r.returncode)
