#!/usr/bin/env python3
"""Replay selected finite evidence in disposable copies, leaving published bytes unchanged.
Requires NumPy, SciPy, SymPy. This is not analytic proof or physical certification.
"""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; DERIVED=HERE.parent; PACKAGE=DERIVED.parent
SCRIPTS=[
 'root/check_radius_crossover.py',
 'workers/gb_reverse_genesis/checks/verify_exact.py',
 'workers/gb_reverse_adversary/check_exact.py',
 'workers/gb_finite_rate_genesis/check.py',
 'workers/gb_memory_audit/check_interfaces.py',
 'workers/gb_memory_audit/check_poisson_pinch.py',
 'workers/gb_memory_audit/check_exposure_optimum.py',
 'workers/gb_kinetic_genesis/check_total_count_obstruction.py',
 'workers/gb_kinetic_audit/independent_exact_audit.py',
 'workers/gb_empirical_quantum/exact_interface_tests.py',
 'workers/gb_empirical_quantum/cp_floor_tests.py',
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 if args.output.exists():raise SystemExit('Refuse overwrite of output')
 manifest=json.loads((PACKAGE.parent/'SELECTED_DERIVED_MANIFEST.json').read_text())
 for row in manifest['files']:
  p=PACKAGE.parent/row['path'];assert sha(p)==row['sha256']
 before={str(p.relative_to(PACKAGE)):sha(p) for p in PACKAGE.rglob('*') if p.is_file()}
 results=[]
 with tempfile.TemporaryDirectory(prefix='astra-gb-public-') as td:
  temp=Path(td)/'derived';shutil.copytree(DERIVED,temp)
  dots=str(PACKAGE/'originals/Dots')
  env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
  for rel in SCRIPTS:
   p=temp/rel;raw=p.read_text();adapted=raw.replace('/Users/harjas/Downloads/Dots',dots)
   if adapted!=raw:p.write_text(adapted)
   run=subprocess.run([sys.executable,str(p)],cwd=p.parent,env=env,text=True,capture_output=True,timeout=120)
   results.append({'script':rel,'published_script_sha256':sha(DERIVED/rel),'ephemeral_script_sha256':sha(p),'path_relocation':'Only literal /Users/harjas/Downloads/Dots prefix relocated to this checkout originals/Dots' if adapted!=raw else None,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
 after={str(p.relative_to(PACKAGE)):sha(p) for p in PACKAGE.rglob('*') if p.is_file()}
 assert before==after
 result={'schema':'astra.gb-public-finite-replay.v1','python':sys.version,'scripts':results,'passed':sum(x['exit_code']==0 for x in results),'attempted':len(results),'published_package_unchanged':True,'scope':'Finite exact/numerical checks only; no original Willow runner, reserved-outcome analysis, model fitting, device validation or novelty certification.'}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k!='scripts'}))
 if result['passed']!=result['attempted']:raise SystemExit(1)
if __name__=='__main__':main()
