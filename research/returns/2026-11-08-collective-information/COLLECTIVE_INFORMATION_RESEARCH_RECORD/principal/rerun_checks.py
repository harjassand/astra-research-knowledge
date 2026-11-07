from pathlib import Path
import subprocess, sys, os, json, hashlib, datetime, concurrent.futures

root=Path(__file__).resolve().parents[1]
d=root/'verification-rerun'
scripts=json.loads((d/'CHECK_SUITE.json').read_text())['scripts']
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')

def one(name):
    p=d/name
    start=datetime.datetime.now(datetime.timezone.utc)
    z=subprocess.run([sys.executable,str(p)],cwd=d,env=env,capture_output=True,text=True,timeout=600)
    log=p.with_suffix('.rerun.log');log.write_text(z.stdout+'\nSTDERR:\n'+z.stderr)
    return dict(script=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),exit_code=z.returncode,start_utc=start.isoformat(),seconds=(datetime.datetime.now(datetime.timezone.utc)-start).total_seconds(),log=str(log.relative_to(d)),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(one,scripts))
out={'synthetic_only':True,'physical_experiments':0,'all_pass':all(x['exit_code']==0 for x in results),'results':results}
(d/'RERUN_REPORT.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
if not out['all_pass']:sys.exit(1)
