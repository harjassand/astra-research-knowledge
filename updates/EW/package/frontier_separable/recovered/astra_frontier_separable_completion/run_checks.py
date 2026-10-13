"""Run current standalone checks in a separate output directory.
This does not rerun prior packet discovery or claim an external proof audit.
"""
import subprocess,os,json,time,sys
from pathlib import Path
if not __debug__:raise RuntimeError('Run without Python -O.')
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'recheck';OUT.mkdir(exist_ok=True)
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
commands=[['separable_repair.py'],['tt_completion.py'],['multiscale_repair.py'],
          ['gap_algebra.py'],['structural_tests.py'],
          ['pressure_certificate.py','--verify',str(ROOT/'pressure_L10K6_witness.json')],
          ['compact_pressure_baseline.py'],['nonlocal_transport_trial.py']]
records=[]
for args in commands:
    start=time.perf_counter()
    p=subprocess.run([sys.executable,str(ROOT/args[0])]+args[1:],cwd=OUT,env=env,capture_output=True,text=True,timeout=120)
    (OUT/(args[0]+'.stdout.txt')).write_text(p.stdout)
    (OUT/(args[0]+'.stderr.txt')).write_text(p.stderr)
    row=dict(script=args[0],returncode=p.returncode,seconds_including_imports=time.perf_counter()-start)
    records.append(row);print(row,flush=True)
    if p.returncode:raise RuntimeError(p.stderr)
(ROOT/'reproduction_status.json').write_text(json.dumps(dict(all_passed=True,runs=records,scope='Same-author reruns, not independent proof validation'),indent=2))
