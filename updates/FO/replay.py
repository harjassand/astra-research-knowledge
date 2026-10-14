#!/usr/bin/env python3
"""Bounded copy-first FO checks; requires NumPy, SciPy and SymPy.

No optional producer search, primary downloads, laboratory experiment or
formal analytic theorem verification is performed. Only copied output changes.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
JOBS={'math': ['FM-sources/resonant/verify_circulation.py', 'FO-circulation-audit/independent_checks.py', 'FO-curvature-classification/verify_curvature.py', 'FO-signature-cancellation/checks.py', 'FO-continuous-calibration/verify_continuum_storage.py', 'FO-root/verify_continuum_storage.py', 'FO-root/test_multifrequency_storage.py', 'FO-curvature-classification/storage_critique/verify_storage_critique.py', 'FO-profile-prior/cone_followup/verify_cone_obstruction.py', 'FO-acoustic-face-review/checks/independent_acoustic_face_checks.py', 'FO-cycle-optimizer/certify_candidate_11_100.py', 'FO-cycle-optimizer/width_quantifier_audit.py'], 'chemical': ['FO-ancestry-audit/independent_checks.py', 'FO-causal-operation/check_identification.py', 'FO-chemical-state-interface/evidence/reconstruct.py'], 'physical': ['FM-sources/physical/calculate_bounds.py', 'FO-phase-audit/checks/rederive_audit.py', 'FO-symmetry-control/derive_checks.py', 'FO-retained-kinetics/ising_retention.py', 'FO-retained-kinetics/continuum_wall.py', 'FO-material-path/calculate_bounds.py', 'FO-alternative-physical/budget_checks.py'], 'response': ['FO-quantum-synthesis/path_flux_check.py']}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--group',choices=list(JOBS),required=True);p.add_argument('--output-dir',type=Path,required=True)
 args=p.parse_args();out=args.output_dir.resolve()
 if out.is_relative_to(ROOT) or (out.exists() and any(out.iterdir())):raise ValueError('Use a new or empty owned directory outside checkout')
 out.mkdir(parents=True,exist_ok=True)
 def hashes():
  count=0
  for name in ['SOURCE_MANIFEST.json','DERIVED_MANIFEST.json']:
   for row in json.loads((HERE/name).read_text())['files']:
    pp=ROOT/row['path']
    if pp.stat().st_size!=row['bytes'] or hashlib.sha256(pp.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Published input drift: '+row['path'])
    count+=1
  return count
 count=hashes()
 shutil.copytree(HERE/'package',out/'work/FM-sources')
 for d in sorted((HERE/'synthesis').iterdir()):
  if d.is_dir():shutil.copytree(d,out/'work'/('FO-'+d.name.replace('_','-')),ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 source=out/'work/FM-sources/resonant'
 shutil.copytree(source,out/'work/FO-circulation-audit/source-copy',ignore=shutil.ignore_patterns('exploration'))
 shutil.copytree(source,out/'work/FO-continuous-calibration/source-copy/resonant')
 shutil.copytree(source,out/'work/FO-cycle-optimizer/incoming_resonant')
 prior=out/'work/astra-capital/updates/FE/synthesis/quartic'
 (prior/'checks').mkdir(parents=True,exist_ok=True)
 shutil.copyfile(out/'work/FO-cycle-optimizer/n794_replay/QUARTIC_AUDIT_AND_PROOF.md',prior/'QUARTIC_AUDIT_AND_PROOF.md')
 shutil.copyfile(out/'work/FO-cycle-optimizer/n794_replay/FSTAR_CLOSED_HEAT_CERTIFICATE.json',prior/'checks/FSTAR_CLOSED_HEAT_CERTIFICATE.json')
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 rows=[]
 for i,relative in enumerate(JOBS[args.group]):
  command=[sys.executable,'-B',str(out/'work'/relative)];start=time.monotonic()
  try:
   run=subprocess.run(command,cwd=out,env=env,capture_output=True,text=True,timeout=180);code,stdout,stderr=run.returncode,run.stdout,run.stderr
  except subprocess.TimeoutExpired as e:
   code=124;stdout=e.stdout or '';stderr=e.stderr or ''
   if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
   if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
   stderr+='\nBounded replay exceeded180seconds.'
  log=out/(str(i)+'-'+Path(relative).stem+'.log');log.write_text(stdout+'\nSTDERR:\n'+stderr)
  rows.append(dict(command=command,exit_code=code,seconds=time.monotonic()-start,log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
  if not code and relative.endswith('FO-root/test_multifrequency_storage.py'):
   witness=json.loads((out/'work/FO-root/MULTIFREQUENCY_STORAGE_CHECK.json').read_text());assert witness['exact_negative'] and witness['exact_margin']=='-183426997/480000000'
  if code:break
 assert hashes()==count
 status='PASS' if len(rows)==len(JOBS[args.group]) and all(x['exit_code']==0 for x in rows) else 'FAIL'
 versions={}
 for name in ['numpy','scipy','sympy']:
  try:versions[name]=__import__(name).__version__
  except ImportError:versions[name]=None
 receipt=dict(status=status,group=args.group,python=platform.python_version(),executable=sys.executable,module_versions=versions,
   checks=rows,expected_steps=len(JOBS[args.group]),published_inputs_hash_unchanged=True,hashed_original_and_derived_files=count,
   scope='23bounded steps across4groups: producerprofile/heat replays,independent exact checks,one bounded20-start root storage-countertest,synthetic finite-state/wall models,and reported-data arithmetic. Ancestryproseonly. No broad optional producersearch,primary downloads,formal proof,priority,lab,totalcost or breakthrough validation. Wallseconds exclude aggregateinference.')
 (out/'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(dict(status=status,group=args.group,steps=len(rows),expected_steps=len(JOBS[args.group]))),flush=True)
 return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
