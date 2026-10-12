"""Regenerate the rational witness, verify it, evaluate bounds, and run tests."""
from pathlib import Path
import os,subprocess,sys,time,json
ROOT=Path(__file__).parent
start=time.perf_counter();env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1'
records=[]
for name in ('build_flow.py','verify_module.py','certificate_bounds.py','selftest.py'):
    t=time.perf_counter()
    result=subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,env=env,
                          text=True,capture_output=True,check=True)
    (ROOT/(name.removesuffix('.py')+'_reproduction_log.txt')).write_text(result.stdout+result.stderr)
    records.append({'script':name,'seconds':time.perf_counter()-t})
out={'steps':records,'total_seconds':time.perf_counter()-start}
(ROOT/'reproduction_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
