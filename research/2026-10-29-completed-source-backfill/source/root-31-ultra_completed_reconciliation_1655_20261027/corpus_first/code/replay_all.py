"""Offline reconstruction of all decisive computations in dependency order."""
import os,subprocess,sys,time,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
scripts=['compile_classical.py','direct_polytope.py','instrument_rank_check.py',
 'product_closure_test.py','product_witness_search.py','product_threshold_search.py',
 'exact_product_counterexample.py','repair_frame.py','exact_repair_kernel.py',
 'kernel_robustness.py','circuit_replay.py','werner_unraveling.py','verify_unraveling_full.py']
records=[];start=time.monotonic()
for script in scripts:
 t=time.monotonic();print('Running',script,flush=True)
 p=subprocess.run([sys.executable,'-B',str(BASE/'code'/script)],env=env,capture_output=True,text=True)
 (BASE/'results'/(script.removesuffix('.py')+'.log')).write_text(p.stdout+p.stderr)
 record=dict(script=script,exit_code=p.returncode,seconds=time.monotonic()-t)
 records.append(record);print(json.dumps(record),flush=True)
 if p.returncode:
  print(p.stdout+p.stderr);raise SystemExit(p.returncode)
result=dict(passed=True,python=sys.executable,checks=records,elapsed_seconds=time.monotonic()-start,
 meaning='Implementation and exact finite identities replayed. Independent audit, historical novelty and physical validation are separate claims.')
(BASE/'results'/'REPLAY_ALL.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(passed=True,checks=len(records),elapsed_seconds=result['elapsed_seconds'])),flush=True)
