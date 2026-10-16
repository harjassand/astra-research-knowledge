#!/usr/bin/env python3
"""Bounded replay of authored checks on a temporary publication-package copy.

Does not execute acquisitions or source scripts, install packages, or write to
the supplied package. Measured subprocess CPU is local execution, not inference.
"""
from pathlib import Path
import argparse,hashlib,json,resource,shutil,subprocess,tempfile,time
CHECKS=['root/singleton_schur.py','workers/gf_causal_adversary/exact_checks.py','workers/gf_causal_adversary/adaptive_independent_checks.py','workers/gf_causal_genesis/check_new_results.py','workers/gf_schur_genesis/check_exact.py','workers/gf_robust_adversary/tests/check_math.py','workers/gf_memory_genesis/check_memory_genesis.py','workers/gf_physical_adversary/check_claims.py','workers/gf_lithium_genesis/check_conservation.py']
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--package',type=Path,required=True);a.add_argument('--python',type=Path,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args()
 package=args.package.resolve();out=args.output.resolve();assert not out.is_relative_to(package) and not out.exists()
 original={p.relative_to(package).as_posix():sha(p.read_bytes()) for p in package.rglob('*') if p.is_file()}
 prep=time.perf_counter();rows=[]
 with tempfile.TemporaryDirectory(prefix='gf-public-authored-replay-') as folder:
  copy=Path(folder)/'package';shutil.copytree(package,copy);prep=time.perf_counter()-prep
  env=subprocess.run([str(args.python),'-c','import sys,numpy,sympy,openpyxl,json; print(json.dumps({"python":sys.version,"numpy":numpy.__version__,"sympy":sympy.__version__,"openpyxl":openpyxl.__version__}))'],capture_output=True,text=True,check=True,timeout=10)
  for name in CHECKS:
   p=copy/name;assert p.is_file();script=p.read_bytes();before=resource.getrusage(resource.RUSAGE_CHILDREN);t=time.perf_counter()
   x=subprocess.run([str(args.python),'-B',str(p)],cwd=copy,capture_output=True,timeout=45)
   after=resource.getrusage(resource.RUSAGE_CHILDREN)
   row={'script':name,'script_sha256':sha(script),'returncode':x.returncode,'wall_seconds':time.perf_counter()-t,'local_child_user_CPU_seconds':after.ru_utime-before.ru_utime,'local_child_system_CPU_seconds':after.ru_stime-before.ru_stime,'stdout_sha256':sha(x.stdout),'stderr_sha256':sha(x.stderr),'stdout_bytes':len(x.stdout),'stderr_bytes':len(x.stderr),'scope':'Selected authored finite assertions; not universal proof or historical/physical verification.'}
   rows.append(row);print(json.dumps(row),flush=True)
   if x.returncode!=0 or x.stderr:raise RuntimeError((name,x.returncode,x.stderr.decode(errors='replace')[:1000]))
  current={p.relative_to(package).as_posix():sha(p.read_bytes()) for p in package.rglob('*') if p.is_file()};assert current==original
 out.write_text(json.dumps({'schema':'astra.gf-public-replay.v1','environment':json.loads(env.stdout),'preparation_copy_wall_seconds':prep,'original_file_hashes_unchanged':len(original),'checks':rows,'status':'PASS_SELECTED_ASSERTIONS','inference_usage':None,'resource_limit_scope':'45 second per-check subprocess timeout; memory peaks/process descendants not independently monitored, no OS sandbox claimed.','boundaries':['Originals and frozen author receipts untouched; candidate outputs only on temporary copy.','No acquired scientific code, acquisitions, installs, paid API calls or physical experiment.','No byte-for-byte reproduction claim for volatile timings/paths in regenerated receipts.']},indent=2)+'\n')
if __name__=='__main__':main()
