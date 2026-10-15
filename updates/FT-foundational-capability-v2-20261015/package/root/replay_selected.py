"""Bounded copy-first model/calculus replay; no physical validation."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib, json, platform, shutil, subprocess, sys, tempfile, time

source=Path(__file__).resolve().parents[1]
dest=Path(tempfile.mkdtemp(prefix='astra-genesis2-replay-'))/'campaign'
omitted={'sources','replays','__pycache__','.DS_Store'}
shutil.copytree(source,dest,ignore=lambda path,names:[n for n in names if n in omitted or n.endswith(('.pdf','.png','.jpg','.pyc'))])
specs=['root/check_dependent_kernel.py','root/pauli_variance_check.py',
       'workers/physical_invention/screening_calculations.py',
       'workers/scientific_operation/check_scalar_acquisition.py',
       'workers/scientific_operation/check_high_order_obstruction.py']
logs=source/'replays'; logs.mkdir(exist_ok=True)
def run(rel):
    start=time.perf_counter()
    try:
        proc=subprocess.run([sys.executable,'-B',str(dest/rel)],cwd=(dest/rel).parent,capture_output=True,text=True,timeout=180)
        code,out,err=proc.returncode,proc.stdout,proc.stderr
    except subprocess.TimeoutExpired as exc:
        code,out,err=None,exc.stdout or '',exc.stderr or ''
        if isinstance(out,bytes): out=out.decode(errors='replace')
        if isinstance(err,bytes): err=err.decode(errors='replace')
    stem=rel.replace('/','__').removesuffix('.py')
    op=logs/(stem+'.stdout.txt'); ep=logs/(stem+'.stderr.txt')
    op.write_text(out); ep.write_text(err)
    return {'script':rel,'sha256':hashlib.sha256((source/rel).read_bytes()).hexdigest(),
            'exit_code':code,'status':'PASS' if code==0 else 'FAIL_OR_TIMEOUT',
            'elapsed_wall_seconds':time.perf_counter()-start,
            'stdout':str(op.relative_to(source)),'stderr':str(ep.relative_to(source))}
start=time.perf_counter()
with ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,specs))
receipt={'schema':'astra.genesis2.copy-first-replays.v1','python':sys.executable,
         'python_version':sys.version,'platform':platform.platform(),'subprocess_slots':3,
         'disposable_copy':str(dest),'elapsed_wall_seconds':time.perf_counter()-start,
         'results':results,'all_passed':all(r['exit_code']==0 for r in results),
         'model_tokens':None,'inference_seconds':None,'inference_energy_joules':None,
         'scope':'bounded exact/symbolic/synthetic/numerical checks; no general proof, novelty, formal, physical or complete-cost validation'}
path=source/'root/REPLAY_RECEIPTS.json'; path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'receipt':str(path),'all_passed':receipt['all_passed'],
                  'elapsed_wall_seconds':receipt['elapsed_wall_seconds'],'results':results},indent=2))
if not receipt['all_passed']: raise SystemExit(1)
