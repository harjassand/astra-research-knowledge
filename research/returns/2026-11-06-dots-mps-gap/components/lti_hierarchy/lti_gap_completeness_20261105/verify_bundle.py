"""Verify every archived payload hash and optionally run standalone functional tests.
Run from any working directory after extracting all four sibling folders.
Tests overwrite result JSONs, so manifest verification happens before execution.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,subprocess,sys,time
HOME=Path(__file__).resolve().parent
ROOT=HOME.parent
ap=argparse.ArgumentParser();ap.add_argument('--run-tests',action='store_true');ap.add_argument('--include-benchmarks',action='store_true');args=ap.parse_args()
records=[]
for line in (HOME/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1);path=ROOT/name
 assert path.resolve().is_relative_to(ROOT.resolve()),name
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 assert actual==digest,(name,digest,actual)
 records.append({'path':name,'sha256':digest})
report={'hash_status':'PASS','payload_files_verified':len(records),'python':platform.python_version(),'numpy':__import__('numpy').__version__,'scipy':__import__('scipy').__version__,'sympy':__import__('sympy').__version__,'tests':[]}
if args.run_tests:
 commands=[['lti_gap_completeness_20261105/test_repair.py'],['lti_gap_completeness_20261105/check_moments.py'],['lti_gap_completeness_20261105/full_operation.py'],['mps_gap_independent_audit_20261105/check_stitching.py'],['lti_gap_adversarial_second_20261105/check_independent_stitch.py'],['lti_gap_completeness_20261105/check_minimum_level.py'],['lti_gap_fresh_resource_audit_20261105/check_stitching.py'],['lti_gap_fresh_resource_audit_20261105/check_level_two.py']]
 if args.include_benchmarks:commands.extend([['lti_gap_completeness_20261105/reduced_benchmark/exchange.py'],['lti_gap_completeness_20261105/reduced_benchmark/benchmark.py']])
 env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['PYTHONNOUSERSITE']='1'
 for command in commands:
  source=ROOT/command[0];start=time.perf_counter()
  cwd=source.parent if command[0].startswith('lti_gap_fresh_resource_audit_20261105/') else ROOT
  argv=[source.name] if cwd==source.parent else command
  run=subprocess.run([sys.executable,*argv],cwd=cwd,env=env,capture_output=True,text=True)
  item={'script':command[0],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'exit_code':run.returncode,'seconds':time.perf_counter()-start,'stdout_tail':run.stdout[-1200:],'stderr':run.stderr[-2000:]}
  report['tests'].append(item)
  if run.returncode:print(json.dumps(report,indent=2));raise SystemExit(run.returncode)
 checks={}
 repairs=json.loads((HOME/'repair_results.json').read_text())
 assert len(repairs)==6
 assert max(x['isometry_error'] for x in repairs)<1e-10
 assert max(x['ideal_boundary_residual_norm'] for x in repairs)<1e-10
 checks['whole_code_repair']='PASS'
 moments=json.loads((HOME/'moment_checks.json').read_text())
 for x in moments.values():
  assert x['correct_gram_limit_L100_error']<1e-10
  assert x['ground_LTI_error']<1e-10
  assert x['local_energy_preservation_error']<1e-8
  assert x['pair_moment_preservation_error']<1e-8
  assert x['projected_trace']<=x['trace_bound_m_over_open_gap']+1e-8
 assert moments['generic_complex']['wrong_transposed_limit_L100_error']>.2
 checks['metric_and_moment_regressions']='PASS'
 full=json.loads((HOME/'full_operation_results.json').read_text())
 for key in ['trace_preservation_error','unchanged_core_energy_error','unchanged_core_square_error','joined_buffer_internal_annihilation_norm']:assert full[key]<1e-10
 assert full['complement_branch_trace']>0 and full['spectral_gap_inequality_slack']>=-1e-10
 checks['complete_channel_with_failure_branch']='PASS'
 first=json.loads((ROOT/'mps_gap_independent_audit_20261105/stitching_results.json').read_text())
 assert first['status'].startswith('PASS') and len(first['cases'])==4
 second=json.loads((ROOT/'lti_gap_adversarial_second_20261105/independent_stitch_results.json').read_text())
 assert len(second)==6 and max(x['ideal_seam_Frobenius'] for x in second)<1e-10
 fresh=json.loads((ROOT/'lti_gap_fresh_resource_audit_20261105/fresh_stitching_results.json').read_text())['results']
 assert len(fresh)==9
 assert max(x['ideal_seam_residual'] for x in fresh)<1e-10
 assert max(x['isometry_error'] for x in fresh)<1e-10
 assert all(x['bound_HK_by_two_map_difference'] for x in fresh)
 checks['three_independent_stitching_executables']='PASS'
 minimum=json.loads((HOME/'minimum_level_regression.json').read_text())
 assert minimum['status']=='PASS' and minimum['exact_integer_residual_zero']
 assert minimum['natural_nearest_neighbor_minimum_level']==3 and minimum['literal_appendix_D_minimum_level']==4
 freshlevel=json.loads((ROOT/'lti_gap_fresh_resource_audit_20261105/level_two_counterexample.json').read_text())
 assert freshlevel['exact_checks_passed'] and freshlevel['exact_eigenvalue']=='1/3'
 checks['two_exact_minimum_level_regressions']='PASS'
 if args.include_benchmarks:
  for n,expected in [(4,.282108),(5,.341787),(6,.345553)]:
   x=json.loads((HOME/f'reduced_benchmark/exchange_n{n}.json').read_text())
   assert abs(x['PSD_mixture_lower_exploratory']-expected)<5e-6
   assert x['max_abs_divergence_coefficient']<x['coefficient_bound']
  checks['optional_exploratory_benchmarks']='PASS; not rigorous gap certificates'
 report['asserted_checks']=checks
 report['functional_status']='PASS' 
 report['test_input_sha256']=hashlib.sha256((HOME/'mps_inputs.npz').read_bytes()).hexdigest()
 report['note']='All hashes were verified before tests. Generated result JSONs contain timing/resource measurements and are overwritten by reproduction; their post-run bytes need not match the archived records.'
print(json.dumps(report,indent=2))
