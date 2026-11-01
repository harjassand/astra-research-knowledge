#!/usr/bin/env python3
"""Replay immutable source checkers only in fresh disposable copies; no network."""
import argparse, hashlib, importlib.metadata, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
S=ROOT/'sources'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser()
parser.add_argument('--include-expensive-global',action='store_true',help='Deliberately rerun the already-replayed ~five-minute exact global supplement.')
args=parser.parse_args()
cases=[
 ('global_structural','quadratic_debt_global_audit_20261101_dp9w20ix/independent_structural_checks.py',['quadratic_debt_global_audit_20261101_dp9w20ix/INDEPENDENT_STRUCTURAL_CHECKS.json']),
 ('composition_saved_review','return_path_construction_20261101/rate2_uniform_removal_composition/independent_review_20261101_0454/verify_saved_review.py',[]),
 ('composition_author','return_path_construction_20261101/rate2_uniform_removal_composition/check_composition_constants.py',['return_path_construction_20261101/rate2_uniform_removal_composition/CHECK_RESULTS.json']),
 ('composition_independent','return_path_construction_20261101/rate2_uniform_removal_composition/independent_review_20261101_0454/independent_checks.py',['return_path_construction_20261101/rate2_uniform_removal_composition/independent_review_20261101_0454/EXACT_CHECK_RESULTS.json']),
 ('activation_saved_manifest','return_path_construction_20261101/rate2_uniform_activation/audit_uniform_activation_20261101_0444/verify_saved_audit.py',[]),
 ('activation_author','return_path_construction_20261101/rate2_uniform_activation/check_activation.py',['return_path_construction_20261101/rate2_uniform_activation/CHECK_RESULTS.json']),
 ('activation_independent','return_path_construction_20261101/rate2_uniform_activation/audit_uniform_activation_20261101_0444/independent_activation_checks.py',['return_path_construction_20261101/rate2_uniform_activation/audit_uniform_activation_20261101_0444/INDEPENDENT_CHECK_RESULTS.json','return_path_construction_20261101/rate2_uniform_activation/audit_uniform_activation_20261101_0444/POLYNOMIAL_IDENTITIES.json']),
 ('macro_author','return_path_construction_20261101/rate2_activated_macro_interface/check_macro_interface.py',['return_path_construction_20261101/rate2_activated_macro_interface/CHECK_RESULTS.json']),
 ('macro_independent','return_path_construction_20261101/rate2_activated_macro_interface/audit_activated_macro_20261101_0450/independent_checks.py',['return_path_construction_20261101/rate2_activated_macro_interface/audit_activated_macro_20261101_0450/CHECK_RESULTS.json']),
 ('rate2_obstruction_independent','return_path_construction_20261101/rate2_fixed_horizon_obstruction_independent_review_20261101/independent_exact_checks.py',['return_path_construction_20261101/rate2_fixed_horizon_obstruction_independent_review_20261101/independent_exact_results.json']),
 ('growth_saved_manifest','return_path_construction_20261101/rate2_uniform_initial_growth/audit_uniform_growth_20261101_0435/verify_saved_audit.py',[]),
 ('growth_author','return_path_construction_20261101/rate2_uniform_initial_growth/check_initial_growth.py',['return_path_construction_20261101/rate2_uniform_initial_growth/CHECK_RESULTS.json']),
 ('growth_independent','return_path_construction_20261101/rate2_uniform_initial_growth/audit_uniform_growth_20261101_0435/independent_initial_growth_checks.py',['return_path_construction_20261101/rate2_uniform_initial_growth/audit_uniform_growth_20261101_0435/INDEPENDENT_CHECK_RESULTS.json']),
 ('root_obstruction_independent','return_path_construction_20261101/root_obstruction_audit/check_obstruction.py',['return_path_construction_20261101/root_obstruction_audit/audit_results.json']),
 ('stopped_debt_author_high_precision','activation_debt_stopped_certificate_20261101/verify_exact_generator.py',['activation_debt_stopped_certificate_20261101/EXACT_GENERATOR_VALIDATION.json']),
 ('stopped_debt_independent_rational','activation_debt_stopped_audit_20261101_sc57xnn6/independent_finite_jump_checks.py',['activation_debt_stopped_audit_20261101_sc57xnn6/INDEPENDENT_CHECKS.json']),
 ('interior_author','return_path_construction_20261101/rate2_paid_interior_removal/check_interior_algebra.py',['return_path_construction_20261101/rate2_paid_interior_removal/check_results.json']),
 ('interior_independent','return_path_construction_20261101/rate2_paid_interior_removal_independent_review_20261101/independent_exact_audit.py',['return_path_construction_20261101/rate2_paid_interior_removal_independent_review_20261101/independent_exact_results.json']),
]
if args.include_expensive_global:
 cases.append(('global_expensive_optional','quadratic_debt_global_audit_20261101_dp9w20ix/independent_global_checks.py',['quadratic_debt_global_audit_20261101_dp9w20ix/INDEPENDENT_GLOBAL_CHECKS.json']))

rows=[]
for name,script,outputs in cases:
 with tempfile.TemporaryDirectory(prefix='return_component_replay_') as tmp:
  work=Path(tmp)/'sources';shutil.copytree(S,work)
  start=time.monotonic();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  result=subprocess.run([sys.executable,str(work/script)],cwd=work,env=env,text=True,capture_output=True,timeout=1200 if name=='global_expensive_optional' else 300)
  checks=[{'path':f,'expected_sha256':digest(S/f),'actual_sha256':digest(work/f),'byte_identical':digest(S/f)==digest(work/f)}for f in outputs]
  passed=result.returncode==0 and all(z['byte_identical']for z in checks)
  row={'case':name,'status':'PASS' if passed else 'FAIL','returncode':result.returncode,'script_sha256':digest(S/script),'clean_copy':True,'outputs':checks,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),'stderr_empty':not result.stderr}
  rows.append(row);print(json.dumps({'case':name,'status':row['status'],'seconds':row['elapsed_seconds']}),flush=True)
  if not passed:print(result.stdout);print(result.stderr);raise AssertionError(name)
# Prove the preserved source tree was not altered by any replay.
allow=json.loads((ROOT/'SOURCE_ALLOWLIST.json').read_text())['files']
assert all(digest(ROOT/z['archive_path'])==z['sha256']for z in allow)
global_dir=S/'quadratic_debt_global_audit_20261101_dp9w20ix'
global_receipt=json.loads((global_dir/'REPLAY_RECEIPT.json').read_text())
assert global_receipt['status']=='PASS_BYTE_IDENTICAL_FRESH_REPLAY' and digest(global_dir/'INDEPENDENT_GLOBAL_CHECKS.json')==global_receipt['result_sha256']
report={'preserved_expensive_global_replay':{'terminal_status':global_receipt['status'],'canonical_sha256':global_receipt['result_sha256'],'receipt_sha256':digest(global_dir/'REPLAY_RECEIPT.json'),'rerun_by_this_invocation':args.include_expensive_global,'policy':'Exact accepted auditor fresh-replay receipt preserved; no redundant expensive packaging run by default.'},'status':'PASS_ALL_CLEAN_COPY_REPLAYS','python_version':sys.version.split()[0],'dependencies':{k:importlib.metadata.version(k)for k in ['sympy','mpmath']},'case_count':len(rows),'preserved_source_files_unchanged':True,'network_used':False,'proof_not_replaced_by_tests':True,'timings_claimed_reproducible':False,'cases':rows}
(ROOT/'REPLAY_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
