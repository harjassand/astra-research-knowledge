"""Own checks only; no author simulation imports or network calls."""
from pathlib import Path
import subprocess,sys,hashlib,time,os
p=Path(__file__).parent
for l in (p/'SHA256SUMS').read_text().splitlines():
 h,f=l.split('  ',1); assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h,f
t=time.monotonic()
cmds=[('autonomous_correction_evaluator',['-m','unittest','test_check_chi.py','test_evaluate.py']),('autonomous_fit_audit',['audit.py']),('autonomous_fit_audit',['-m','unittest','test_audit.py']),('autonomous_echo_comparator',['model.py']),('autonomous_echo_comparator',['check_ideal_recovery.py']),('optimal_spin_recovery',['check.py']),('faulty_measurement_cp_bridge',['check_cp_coin_bridge.py'])]
env=dict(os.environ,OPENBLAS_NUM_THREADS='1')
for d,args in cmds:
 r=subprocess.run([sys.executable]+args,cwd=p/d,capture_output=True,text=True,env=env)
 if r.returncode:print(r.stdout,r.stderr);raise SystemExit(r.returncode)
 print('PASS',d,' '.join(args),flush=True)
print('PASS',len(cmds),'suites; seconds',round(time.monotonic()-t,3))
