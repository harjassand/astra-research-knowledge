#!/usr/bin/env python3
"""Copy-first bounded FE scientific replay; never modifies published evidence.

Uses only stdlib orchestration. Quartic checks additionally need SymPy; hidden
stored transcripts and interferometry need NumPy/SciPy. This verifies finite
algebra/software claims, not analytic proofs, novelty or physical availability.
It does not rerun optimizers or generate a new acquisition benchmark.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--group',choices=['quartic','hidden_gate','interferometry'],required=True)
 p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();out=a.output_dir.resolve()
 if out.exists() and any(out.iterdir()):raise ValueError('Use a new or empty owned output directory')
 if out.is_relative_to(ROOT):raise ValueError('Replay output must be outside the publication checkout')
 out.mkdir(parents=True,exist_ok=True)
 for r in json.loads((HERE/'SOURCE_MANIFEST.json').read_text())['files']:
  data=(ROOT/r['path']).read_bytes()
  if hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('Source hash mismatch:'+r['path'])
 def cp(src,dst):shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 jobs=[]
 if a.group=='quartic':
  cp(HERE/'package/quartic',out/'FE-sources/quartic');cp(HERE/'synthesis/quartic',out/'FE-quartic');cp(HERE/'synthesis/quartic_critic',out/'FE-quartic-critic')
  jobs=[['FE-quartic/replay/verify_morrey_quartics.py'],['FE-quartic/replay/exact_fourier_moments.py'],
        ['FE-quartic/checks/verify_closed_heat.py'],['FE-quartic-critic/independent_audit.py'],['FE-quartic-critic/verify_heat_independent.py']]
 elif a.group=='hidden_gate':
  cp(HERE/'package/hidden_gate',out/'hidden_gate_source');cp(HERE/'synthesis/hidden_gate',out/'hidden_gate_audit');cp(HERE/'synthesis/root',out/'root_audit')
  jobs=[['hidden_gate_source/exact_checks.py'],['hidden_gate_source/audit_artifacts.py'],
        ['hidden_gate_audit/derived/independent_checks.py'],['root_audit/exact_query_counterexamples.py','--output-dir',str(out/'root_audit')]]
 else:
  cp(HERE/'package/interferometry',out/'interferometry_source');cp(HERE/'synthesis/interferometry',out/'interferometry_audit')
  jobs=[['interferometry_source/check_history_interferometer.py','--output',str(out/'interferometry_audit/replay/results.json')],
        ['interferometry_audit/independent_interferometry_checks.py','--source-dir',str(out/'interferometry_source'),
         '--replay-dir',str(out/'interferometry_audit/replay'),'--output',str(out/'interferometry_audit/independent_results.json')]]
 rows=[]
 for i,job in enumerate(jobs):
  cmd=[sys.executable,'-B',str(out/job[0]),*job[1:]];start=time.monotonic()
  r=subprocess.run(cmd,cwd=out,env=env,capture_output=True,text=True,timeout=180)
  log=out/(str(i)+'-'+Path(job[0]).stem+'.log');log.write_text(r.stdout+'\nSTDERR:\n'+r.stderr)
  rows.append(dict(command=job,exit_code=r.returncode,seconds=time.monotonic()-start,log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
  if r.returncode:break
 report=dict(status='PASS' if len(rows)==len(jobs) and all(x['exit_code']==0 for x in rows) else 'FAIL',group=a.group,
   python=platform.python_version(),executable=sys.executable,output_dir=str(out),checks=rows,
   scope='Finite exact algebra/numerical replay only. Analytic implications written separately. No external proof/priority/physical certification.')
 (out/'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 return 0 if report['status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
