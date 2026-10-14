#!/usr/bin/env python3
"""Copy-first bounded FH checks; never execute supplied shell/audit missions.

Requires SymPy,NumPy,SciPy. Output must be a new/empty directory outside the
publication checkout. Frozen source and derived bytes are checked before/after.
The root retained-witness replay explicitly reuses producer certificate code.
No run establishes external correctness,novelty or physical validation.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--group',choices=['quartic','escape','spectral'],required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();out=a.output_dir.resolve()
 if out.is_relative_to(ROOT) or out.exists() and any(out.iterdir()):raise ValueError('Use a new or empty owned directory outside the publication checkout')
 out.mkdir(parents=True,exist_ok=True)
 def hashes():
  for name in ['SOURCE_MANIFEST.json','DERIVED_MANIFEST.json']:
   for x in json.loads((HERE/name).read_text())['files']:
    p=ROOT/x['path']
    if p.stat().st_size!=x['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:raise ValueError('Input mismatch:'+x['path'])
 hashes()
 def cp(src,dst):shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');jobs=[]
 def py(p,*args):return [sys.executable,'-B',str(out/p),*map(str,args)]
 if a.group=='quartic':
  cp(HERE/'package/quartic',out/'FH-sources/quartic');cp(HERE/'synthesis/quartic',out/'FH-quartic');cp(HERE/'synthesis/quartic_critic',out/'FH-quartic-critic');cp(HERE/'synthesis/root',out/'FH-root')
  for p in ['FH-sources/quartic/verify_rigidity.py','FH-quartic/independent_quant_checks.py','FH-quartic-critic/independent_checks.py','FH-quartic-critic/DELTA_INDEPENDENT_CHECKS.py']:jobs.append((py(p),out))
  jobs.append((py('FH-root/near_face_deflation.py','--output-dir',out/'FH-root'),out))
 elif a.group=='escape':
  cp(HERE/'package/escape',out/'FH-sources/escape');cp(HERE/'synthesis/escape',out/'FH-escape');cp(HERE/'synthesis/root',out/'FH-root');cp(HERE/'package/escape',out/'FH-escape/source_snapshot/escape')
  for p in ['FH-escape/independent_checks.py','FH-escape/query_tree_audit.py','FH-escape/query_tree_exact_replay.py']:jobs.append((py(p),out))
  jobs.append((py('FH-root/positive_graph_acquisition.py','--output-dir',out/'FH-root'),out))
  jobs.append((py('FH-root/replay_acquired_certificate.py','--source-dir',out/'FH-sources/escape','--output-dir',out/'FH-root'),out))
 else:
  cp(HERE/'package/spectral',out/'FH-sources/spectral');cp(HERE/'synthesis/spectral',out/'FH-spectral')
  for p in ['FH-sources/spectral/validate_operation.py','FH-spectral/analysis/independent_checks.py','FH-spectral/analysis/cross_implementation_check.py']:jobs.append((py(p),out))
 rows=[]
 for i,(cmd,cwd) in enumerate(jobs):
  st=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=240)
  log=out/(str(i)+'-'+Path(cmd[2]).stem+'.log');log.write_text(r.stdout+'\nSTDERR:\n'+r.stderr)
  rows.append(dict(command=cmd,exit_code=r.returncode,seconds=time.monotonic()-st,log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
  if r.returncode:break
 hashes();status='PASS' if len(rows)==len(jobs) and all(x['exit_code']==0 for x in rows) else 'FAIL'
 report=dict(status=status,group=a.group,python=platform.python_version(),executable=sys.executable,checks=rows,expected_steps=len(jobs),published_inputs_hash_unchanged=True,scope='Bounded exact algebra/model replay only;producer imported for retained ring witness explicitly. Does not rerun reported6818 assertions,full exploratory searches,external proof/novelty review or physical acquisition.')
 (out/'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=status,group=a.group,steps=len(rows),expected_steps=len(jobs))));return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
