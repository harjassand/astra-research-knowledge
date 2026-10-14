#!/usr/bin/env python3
"""Bounded copy-first FL checks; requires NumPy, SciPy and SymPy.

No optional producer search, primary downloads, laboratory experiment or
formal analytic theorem verification is performed. Only copied output changes.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
JOBS={
 'global':[
  'FL-sources/global/verify_global_compatibility.py',
  'FL-global-audit/independent_checks.py',
  'FL-phase-geometry/phase_geometry_checks.py',
  'FL-laminate-construction/check_phase_only.py',
  'FL-packet-assembly/independent_packet_checks.py',
  'FL-global-moments/verify_global_moment_bridge.py',
  'FL-global-audit/post_review/independent_post_review.py',
  'FL-global-moments/curved_completion/verify_curved_completion.py'],
 'ancestry':[
  'FL-ancestry-audit/independent_checks.py',
  'FL-ancestry-audit/simulate_shared_code.py',
  'FL-ancestry-information/finite_checks.py',
  'FL-ancestry-information/simple_binary_review/finite_checks.py',
  'FL-code-design/code_design.py',
  'FL-isotope-experiment/analysis/analyze_published_isotopes.py',
  'FL-root/check_joint_ancestry.py',
  'FL-root/check_simple_binary.py',
  'FL-ancestry-audit/root_joint_review/review_checks.py'],
 'physical':[
  'FL-activation-audit/code/check_activation.py',
  'FL-activation-control/model.py',
  'FL-molecular-recovery/derive.py',
  'FL-physical-pivot/analyze.py']}

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
 shutil.copytree(HERE/'package',out/'work/FL-sources')
 for d in sorted((HERE/'synthesis').iterdir()):
  if d.is_dir():shutil.copytree(d,out/'work'/('FL-'+d.name.replace('_','-')),ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
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
  if code:break
 assert hashes()==count
 status='PASS' if len(rows)==len(JOBS[args.group]) and all(x['exit_code']==0 for x in rows) else 'FAIL'
 versions={}
 for name in ['numpy','scipy','sympy']:
  try:versions[name]=__import__(name).__version__
  except ImportError:versions[name]=None
 receipt=dict(status=status,group=args.group,python=platform.python_version(),executable=sys.executable,module_versions=versions,
   checks=rows,expected_steps=len(JOBS[args.group]),published_inputs_hash_unchanged=True,hashed_original_and_derived_files=count,
   scope='21boundedsoftware steps across3groups. Source global verifier only; ancestry/activation independent reconstructions because producer programs absent. Includes finite exact algebra,100campaign shared-code synthetic simulation and reported-data arithmetic. No search,formal proof,priority,physical/totalcost or breakthrough validation. Wall seconds exclude aggregate inference.')
 (out/'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(dict(status=status,group=args.group,steps=len(rows),expected_steps=len(JOBS[args.group]))),flush=True)
 return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
