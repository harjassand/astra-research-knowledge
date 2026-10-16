#!/usr/bin/env python3
"""Hash and replay exact rejection certificates; never run a candidate solver."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def get(x,key):
 for p in key.split('.'):x=x[p]
 return x

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,default=Path('verification_output'));a=ap.parse_args();out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 manifest=json.loads((ROOT/'PACKET_MANIFEST.json').read_text())
 for rel,record in manifest['files'].items():
  path=ROOT/rel
  if not path.is_file() or digest(path)!=record['sha256']:raise SystemExit(f'Hash mismatch: {rel}')
 print(f'PASS: {len(manifest["files"])} packet file hashes',flush=True)
 env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 results=[]
 with tempfile.TemporaryDirectory(prefix='schlogl_exact_replay_') as temporary:
  work=Path(temporary)
  for p in (ROOT/'verification').glob('*.py'):shutil.copy2(p,work/p.name)
  def run(script,args,filename,recorded,keys=None):
   log=out/(filename+'.log');actual_path=out/filename
   if actual_path.exists():actual_path.unlink()
   command=[sys.executable,str(work/script),*map(str,args)]
   completed=subprocess.run(command,cwd=work,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=150)
   log.write_text(completed.stdout)
   if completed.returncode:raise RuntimeError(f'{script} failed ({completed.returncode}); see {log}')
   if not actual_path.exists():shutil.copy2(work/filename,actual_path)
   actual=json.loads(actual_path.read_text());expected=json.loads((ROOT/recorded).read_text())
   if keys is None:
    if actual!=expected:raise AssertionError(f'{script}: complete exact record differs')
   else:
    for key in keys:
     if get(actual,key)!=get(expected,key):raise AssertionError(f'{script}: exact field differs: {key}')
   results.append(dict(check=script,result='PASS',output=filename,matched_fields=keys or 'complete deterministic JSON'))
   print(f'PASS: {script} -> {filename}',flush=True)
   return actual
  v='verification/'
  run('test_verifier.py',[],'self_tests.json',v+'self_tests.json')
  first=ROOT/'experiments/candidate.json';weighted=ROOT/'experiments/weighted_repair/candidate.json';third=ROOT/'experiments/constrained_test/candidate.json'
  tail=run('verify_uniform_tail.py',[first,'--output',out/'tail_rejection.json'],'tail_rejection.json',v+'tail_rejection.json',['status','npz_sha256','initial_l1_defect_exact','join_l1_defect_exact','augmented_integrated_l1_residual_lower.exact','endpoint_overflow.lower.exact'])
  common=['status','candidate_sha256','initial_l1_defect_exact','join_l1_defect_exact','augmented_integrated_l1_residual_lower.exact','true_probability_outside_box_or_overflow_upper.exact','mass_defect_absolute_upper.exact','actual_augmented_state_l1_error_lower_balanced_witness.exact']
  first_product=run('verify_product_tail.py',[first,'--total-mass','--output',out/'original_balanced_rejection.json'],'original_balanced_rejection.json',v+'original_balanced_rejection.json',common)
  assert first_product['augmented_integrated_l1_residual_lower']['exact']==tail['augmented_integrated_l1_residual_lower']['exact']
  run('verify_product_tail.py',[weighted,'--total-mass','--output',out/'weighted_rejection.json'],'weighted_rejection.json',v+'weighted_rejection.json',common)
  run('verify_slab.py',[third,'--budget','1e-13','--memory-mib','512','--cpu-seconds','120','--output',out/'constrained_coordinate.json'],'constrained_coordinate.json',v+'constrained_coordinate.json',['status','npz_sha256','initial_join_selected_lower.exact','global_initial_defect_exact','full_1e9_interior_budget_rejected','integrated_l1_residual_selected_lower.exact'])
  run('check_localization.py',[first,'--tail-result',out/'tail_rejection.json','--output',out/'localization_rejection.json'],'localization_rejection.json',v+'localization_rejection.json',['status','candidate_sha256','true_probability_outside_box_or_overflow_upper.exact','actual_augmented_state_l1_error_lower.exact'])
  source=ROOT/'references/cap_source/fz_kinetic_cap_certificate_audit_EXACT_AUDIT.json'
  run('check_physical_overflow.py',[first,'--source-audit',source,'--output',out/'physical_rejection.json'],'physical_rejection.json',v+'physical_rejection.json',['status','candidate_sha256','source_audit_sha256','K_exact','overflow_bound_T1.exact','overflow_bound_slab_h.exact','actual_augmented_state_l1_error_lower.exact'])
  # The scalar checker writes beside itself. Copy to the temporary workspace;
  # no acquired program or candidate solver is imported or executed.
  shutil.copy2(ROOT/'references/incumbent/check_poisson_specialization.py',work/'check_poisson_specialization.py')
  run('check_poisson_specialization.py',[],'poisson_specialization.json','references/incumbent/poisson_specialization.json')
 summary={'status':'PASS_ALL_REPLAYED_EXACT_CERTIFICATES','hashes_verified':len(manifest['files']),'checks':results,'candidate_solvers_executed':False,'acquired_third_party_code_executed':False,'warning':'These certificates reject the three saved candidates or their full-forward certificate route; they do not certify a target success probability or exhaust AMEn.'}
 (out/'replay_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('PASS: all exact certificates reproduced; no candidate solver or acquired code executed.')
if __name__=='__main__':main()
