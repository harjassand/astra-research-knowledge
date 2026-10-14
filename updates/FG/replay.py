#!/usr/bin/env python3
"""Copy-first, bounded FG algebra replay. Published inputs are never written.

Quartic needs SymPy;compact source checks and history need NumPy/SciPy.
Compact integer replay additionally needs C++17 and GMP/pkg-config. It rebuilds
owned backends from source and never runs preserved binaries or loads pickle.
Original failed history replays remain frozen evidence;this wrapper checks the
separate repaired reference and independent diagnostics without relabeling FAIL.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,shlex,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--group',choices=['quartic','compact','history'],required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();out=a.output_dir.resolve()
 if out.is_relative_to(ROOT) or out.exists() and any(out.iterdir()):raise ValueError('Use a new or empty owned directory outside publication checkout')
 out.mkdir(parents=True,exist_ok=True)
 for name in ['SOURCE_MANIFEST.json','DERIVED_MANIFEST.json']:
  for x in json.loads((HERE/name).read_text())['files']:
   if hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']:raise ValueError('Input hash mismatch:'+x['path'])
 def cp(src,dst):shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1');jobs=[]
 def py(p,*args):return [sys.executable,'-B',str(out/p),*map(str,args)]
 if a.group=='quartic':
  cp(HERE/'package/quartic',out/'FG-sources/quartic');cp(HERE/'synthesis/quartic',out/'FG-quartic');cp(HERE/'synthesis/quartic_critic',out/'FG-quartic-critic')
  for p in ['FG-sources/quartic/verify_sharp_scalar.py','FG-sources/quartic/verify_explicit.py','FG-quartic/checks/verify_tensor_boundary.py','FG-quartic-critic/independent_sharp_audit.py']:jobs.append((py(p),out,None))
  jobs.append((py('FG-quartic-critic/adjacent/verify_adjacent_independent.py',out/'FG-quartic/checks/TENSOR_CERTIFICATE.json',out/'FG-quartic-critic/adjacent/PORTABLE_REPLAY_RESULTS.json'),out,None))
  for p in ['verify_scalar_obstruction_independent.py','verify_feature_reduction_independent.py']:jobs.append((py('FG-quartic-critic/adjacent/'+p),out,None))
 elif a.group=='compact':
  cp(HERE/'package/compact',out/'FG-sources/compact');cp(HERE/'synthesis/compact',out/'FG-compact');cp(HERE/'synthesis/root',out/'FG-root');cp(HERE/'synthesis/source_cut_critic',out/'FG-source-cut-critic')
  src=out/'FG-sources/compact';(out/'bin').mkdir()
  cflags=subprocess.check_output(['pkg-config','--cflags','--libs','gmpxx'],text=True).strip();flags=shlex.split(cflags)
  for backend in ['exact_contract','exact_continuum']:
   jobs.append(([os.environ.get('CXX','c++'),'-std=c++17','-O2',str(src/(backend+'.cpp')),'-o',str(out/'bin'/backend),*flags],out,None))
  for name,backend,suffix,degree,raw in [('n128','exact_contract','.dyadic.txt',2,'.exact_raw.txt'),('continuous128','exact_continuum','.continuum.txt',2,'.continuum_raw.txt')]:
   jobs.append(([str(out/'bin'/backend),str(src/(name+suffix)),str(degree)],out,src/(name+raw)))
  for p in ['audit_exact.py','energy_envelope_audit.py','conditional_envelope.py','conditional_reference.py','bath_completion.py']:jobs.append((py('FG-sources/compact/'+p),src,None))
  jobs.append((py('FG-compact/derived/source_schur_checks.py','--discrete-prefix',src/'pilot8','--output',out/'SCHUR_REPLAY_RESULTS.json'),out,None))
  for p in ['source_normalization_cut.py','correlated_source_hardness.py']:jobs.append((py('FG-root/'+p,'--output-dir',out/'FG-root'),out,None))
  for p in ['independent_audit.py','correlated_source_audit.py','global_power_audit.py','optimized_lower_audit.py']:jobs.append((py('FG-source-cut-critic/'+p),out,None))
 else:
  cp(HERE/'package/history',out/'FG-sources/history');cp(HERE/'synthesis/history',out/'FG-history')
  jobs=[(py('FG-sources/history/validate_extra.py'),out/'FG-sources/history',None),
        (py('FG-history/replay_repaired/validate.py'),out/'FG-history/replay_repaired',None),
        (py('FG-history/independent_history_checks.py','--output',out/'HISTORY_INDEPENDENT_REPLAY.json'),out,None)]
 rows=[]
 for i,(cmd,cwd,expected) in enumerate(jobs):
  st=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=240)
  equal=None if expected is None else r.stdout.encode()==expected.read_bytes()
  log=out/(str(i)+'-'+Path(cmd[2] if len(cmd)>2 and cmd[1]=='-B' else cmd[0]).stem+'.log');log.write_text(r.stdout+'\nSTDERR:\n'+r.stderr)
  rows.append(dict(command=cmd,exit_code=r.returncode,seconds=time.monotonic()-st,log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),integer_output_equal=equal))
  if r.returncode or equal is False:break
 # Strictly check the separately repaired reference result;process exit alone
 # did not reject the original nonfinite grid. Nonfinite originals stay frozen.
 extra=True
 if a.group=='history' and len(rows)==len(jobs):
  def finite(x):
   if isinstance(x,float):return __import__('math').isfinite(x)
   if isinstance(x,dict):return all(finite(v) for v in x.values())
   if isinstance(x,list):return all(finite(v) for v in x)
   return True
  extra=finite(json.loads((out/'FG-history/replay_repaired/validation_results.json').read_text()))
 status='PASS' if len(rows)==len(jobs) and all(x['exit_code']==0 and x['integer_output_equal'] is not False for x in rows) and extra else 'FAIL'
 report=dict(status=status,group=a.group,python=platform.python_version(),executable=sys.executable,checks=rows,repaired_validation_finite=extra if a.group=='history' else None,source_history_replay='Original unmodified FAIL with40nonfinites;separate repaired PASS. Original frozen receipts remain authoritative for those runs.' if a.group=='history' else None,scope='Bounded internal software/algebra replay only;not external proof,priority,physical experiment or capability certification.')
 (out/'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
