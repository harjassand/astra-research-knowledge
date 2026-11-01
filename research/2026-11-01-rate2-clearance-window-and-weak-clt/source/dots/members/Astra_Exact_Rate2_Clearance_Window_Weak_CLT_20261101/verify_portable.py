#!/usr/bin/env python3
"""NEW portable scientific verification, not an old full-author-freeze replay.
Default executes only unchanged admit.py/sample and the CLT temporary exact
checkers. No numerical solver, meter, cache experiment or historical harness.
All package files are read-only; child-generated CLT data live in temp dirs.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
import argparse, hashlib, json, math, os, subprocess, sys
ROOT=Path(__file__).resolve().parent
S=ROOT/'sources'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):return json.loads(path.read_text())
def checked(base,entry):
 rel=entry.get('archive_path',entry.get('path'))
 q=PurePosixPath(rel)
 assert not q.is_absolute() and '..' not in q.parts and '\\' not in rel,rel
 p=base/rel
 assert p.is_file() and not p.is_symlink(),rel
 b=p.read_bytes();assert sha(b)==entry['sha256'],rel
 if 'bytes' in entry:assert len(b)==entry['bytes'],rel
 return b
p=argparse.ArgumentParser();p.add_argument('--integrity-only',action='store_true');args=p.parse_args()
allow=read(ROOT/'PORTABLE_SCIENTIFIC_ALLOWLIST.json')
for row in allow['files']:checked(ROOT,row)
if (ROOT/'PACKAGE_MANIFEST.json').exists():
 package=read(ROOT/'PACKAGE_MANIFEST.json')
 expected={x['path']for x in package['files']}|{'PACKAGE_MANIFEST.json'}
 actual={str(x.relative_to(ROOT))for x in ROOT.rglob('*')if x.is_file()}
 assert actual==expected,('unexpected or missing package members',actual^expected)
 for row in package['files']:checked(ROOT,row)
before={str(x.relative_to(ROOT)):sha(x.read_bytes())for x in ROOT.rglob('*')if x.is_file()}
receiver=S/'clearance_window_receiver_20261101'
runtime=read(receiver/'SOURCE_BINDINGS.json')
assert sha((receiver/'SOURCE_BINDINGS.json').read_bytes())=='ec0bd61d36ff51dfe39090ae67e22b9cb94dfb4208ee2b58b8370cdf24fda016'
assert sha((receiver/'admit.py').read_bytes())=='2fcc71ac4789d18480d888ce9f71ff7f76a9d6ddb04615fadb509643118071de'
assert len(runtime['files'])==159
for row in runtime['files']:checked(S,row)
assert not (receiver/'test_loading_isolation.py').exists()
assert not (receiver/'verify_saved.py').exists()
assert not (receiver/'test_admit.py').exists()
receipt=read(S/'clearance_window_receiving_audit_20261101/RECEIVING_RECEIPT.json')
assert receipt['status']=='PASS_ORDINARY_SCIENTIFIC_NUMERICAL_RECEIVER' and not receipt['open_scientific_blockers']
for name,row in receipt['bindings'].items():
 if name!='historical_loading_evidence_preserved_not_repeated':checked(S,row)
join=S/'return_path_construction_20261101/rate2_explicit_receiver_join_review_20261101_0544/REVIEW_RECEIPT.json'
j=read(join);assert not j['open_blockers']
for row in j['source_bindings'].values():checked(S,row)
old=read(S/'return_path_construction_20261101/rate2_uniform_removal_composition/independent_review_20261101_0454/REVIEW_RECEIPT.json')
for row in old['dependencies'].values():checked(S,row)
A=S/'clearance_fluctuation_bridge_20261101/audit_actual_clt_20261101_0607'
params=read(A/'PARAMETER_BINDING_READBACK.json');parameter_rows=0
for block in params['manifests']:
 checked(S,{'path':block['manifest'],'sha256':block['sha256']})
 for row in block['files']:checked(S,row);parameter_rows+=1
sources=read(A/'SOURCE_READBACK.json')['files']
for row in sources:checked(S,row)
# Saved scalar arithmetic, not reintegration of the ODE.
scalar=read(S/'inverse_clearance_clock_20261101/CERTIFICATE_FINE.json')
sL,sU=map(F,(scalar['s_star_lower'],scalar['s_star_upper']))
assert sL==F(scalar['s_at_E_lower'])+F(scalar['tail_refined_lower'])
assert sU==F(scalar['s_at_E_upper'])+F(scalar['tail_refined_upper'])
assert F(scalar['total_width'])==sU-sL
assert F(scalar['s_star_decimal_outward'][0])<=sL<sU<=F(scalar['s_star_decimal_outward'][1])
variance=read(S/'inverse_clock_variance_20261101/VARIANCE_CERTIFICATE.json')
vL,vU=map(F,(variance['sigma_squared_lower'],variance['sigma_squared_upper']))
assert vL==F(variance['startup_variance_lower'])+F(variance['inverse_variance_lower'])
assert vU==F(variance['startup_variance_upper'])+F(variance['inverse_variance_upper'])+F(variance['tail_and_gap_charged_width'])
assert F(variance['tail_and_gap_charged_width'])>=F(variance['gap_variance_upper'])+F(variance['tail_variance_upper'])
assert vU-vL==F(variance['total_width'])<F(1,1000)
assert F(variance['sigma_squared_decimal_outward'][0])<=vL<vU<=F(variance['sigma_squared_decimal_outward'][1])
# Independently reconstruct fixture's endpoints, eight paid tails and reserve ledger.
v=read(receiver/'SAMPLE_INPUT.json');result=read(receiver/'SAMPLE_RESULT.json')
N=int(v['N']);K=int(v['K']);a=F(int(v['a_num']),int(v['a_den']));T=int(result['T']);D=10**100
assert N==10**1300==T**5 and K==10**40
root=math.isqrt(K+1);ceil=root+(root*root<K+1);q=2*ceil+1;H=K+1+q+1
beta=F(1,K*math.isqrt(K));h=1600*D**2
lower=max(F(0),sL-a-beta);upper=sU+a+32*beta+F(h,T)
assert list(map(F,result['normalized_window_exact']))==[lower,upper]
assert list(map(F,result['physical_window_exact']))==[lower*T,upper*T]
assert list(map(F,result['s_star_interval_exact']))==[sL,sU]
assert F(result['normalized_window_decimal_outward'][0])<lower<upper<F(result['normalized_window_decimal_outward'][1])
clock=F(10**5*H**6,T)/a**6
assert clock==F(result['B_clock_rational_upper'])
tails=[(F(K*T,64)-1,36*H**3*T**3,None),(F(N//(2*D)-1,2)-(4*T+h),1,N//(2*D)-1),(F(K*T,3*10**12),32,None),(F((N+D-1)//D,2)-F(40000,10**50),1,(N+D-1)//D),(F(N,2000*D),32*N*N*h,None),(F(600*N*N,96*h+20),1,None),(F(N,2),1,None),(F(N,96),1,None)]
assert len(result['tail_receipts'])==len(tails)==8
for (exponent,pref,r),row in zip(tails,result['tail_receipts']):
 floor=exponent.numerator//exponent.denominator;b=0 if pref==1 else pref.bit_length()
 assert floor>=b+40 and row['prefactor_bit_upper']==b
 assert row['required_exponent_floor']==b+40 and row['exponent_floor_bit_length']==floor.bit_length()
 assert F(row['upper'])==F(1,2**40)
 if r is not None:assert row['integer_threshold_bit_length']==r.bit_length()
failure=clock+F(8,2**40)
assert failure==F(result['failure_upper_exact'])<=F(result['failure_decimal_upper'])<F(1,10**6)
assert all(result['admission_tests'].values())
challenge=read(receiver/'OUTWARD_ROUNDING_CHALLENGE.json')
assert lower-F(result['normalized_window_decimal_outward'][0])==F(challenge['lower_margin_exact'])>0
assert F(result['normalized_window_decimal_outward'][1])-upper==F(challenge['upper_margin_exact'])>0
records=[read(receiver/n)for n in ['DEVELOPMENT_ACQUISITION_V0.json','history_pre_bytecode_isolation/SCALAR_ACQUISITION.json','SCALAR_ACQUISITION.json']]
keys=['replays','arithmetic_operation_counts','charged_rational_operations','max_rational_temporary_bit_upper','rational_schoolbook_bit_charge','rejected_refinements']
for key in keys:assert records[0][key]==records[1][key]==records[2][key],key
cost=read(receiver/'ACQUISITION_COST_SUMMARY.json')
assert sum(r['charged_rational_operations']for r in records)==cost['total_charged_rational_operations']==92474955
assert sum(int(r['rational_schoolbook_bit_charge'])for r in records)==int(cost['total_rational_schoolbook_bit_charge'])
assert len(records)==3 and cost['max_rational_temporary_bit_upper']==1618
ledger=result['cost_ledger'];runtime_bytes=sum(x['bytes']for x in runtime['files'])+(receiver/'SOURCE_BINDINGS.json').stat().st_size
assert runtime_bytes==ledger['source_bytes_read_and_hashed']==733616
assert ledger['source_files_read_and_hashed']==160
work=3*10**27+2*10**24+(runtime_bytes+(receiver/'SAMPLE_INPUT.json').stat().st_size)*1048576
assert work==int(ledger['total_cold_work_upper'])==3002000000000000770888957952
assert work<int(v['work_budget'])
# Preserve empirical wins/failures by readback, never treat the pilots as proof.
base=read(S/'rate2_baseline_pilot_20261101/SUMMARY.json')
assert sum(x['requested']for x in base)==sum(x['completed']for x in base)==148
assert sum(x['events_total']for x in base)==224543093
lna=read(S/'rate2_lna_extension_20261101/SUMMARY.json');middle=next(x for x in lna if x['N']==1000)
assert abs(middle['LNA_time_variance']-middle['SSA_sample_variance'])<abs(middle['candidate_clock_variance']-middle['SSA_sample_variance'])
domain=read(S/'rate2_lna_extension_20261101/DOMAIN_DIAGNOSTIC.json')
assert all(x['max_diagonal_variance_to_exact_second_moment_ceiling_ratio']>1 for x in domain['runs'])
run_info={'performed':False}
if not args.integrity_only:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 command=[sys.executable,'-B','-I',str(receiver/'admit.py'),str(receiver/'SAMPLE_INPUT.json')]
 proc=subprocess.run(command,cwd=S,env=env,check=True,capture_output=True,text=True)
 actual=json.loads(proc.stdout);expected=dict(result)
 actual.pop('elapsed_ns_nonproof');expected.pop('elapsed_ns_nonproof')
 assert actual==expected,'unchanged receiver non-timing result mismatch'
 clt=subprocess.run([sys.executable,'-B',str(A/'verify_audit.py'),'--original-root',str(S)],cwd=S,env=env,check=True,capture_output=True,text=True)
 clt_result=json.loads(clt.stdout);assert clt_result['numerical_parameter_solvers_rerun'] is False
 run_info={'performed':True,'unchanged_receiver_all_non_timing_fields_match':True,'receiver_non_timing_canonical_sha256':sha(json.dumps(actual,sort_keys=True,separators=(',',':')).encode()),'clt_exact_replay':clt_result}
after={str(x.relative_to(ROOT)):sha(x.read_bytes())for x in ROOT.rglob('*')if x.is_file()}
assert before==after,'package source mutation detected'
print(json.dumps({'status':'PASS_PORTABLE_SCIENTIFIC_CORE','source_payloads':len(allow['files']),'runtime_dependency_rows':159,'clt_original_source_rows':len(sources),'deterministic_parameter_rows':parameter_rows,'saved_rational_endpoints_tails_variance_aggregation_and_three_cost_records':'PASS','baseline_saved_evidence_readback':'PASS_NOT_A_PROOF_DEPENDENCY','standard_replay':run_info,'package_bytes_unchanged':True,'numerical_solver_acquisitions_performed':0,'historical_full_author_and_receiving_closure_reproduced':False,'omitted_historical_harnesses_executed':False,'security_certification_claimed':False},indent=2))
