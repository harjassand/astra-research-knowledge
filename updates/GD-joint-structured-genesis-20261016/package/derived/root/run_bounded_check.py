"""Root-reviewed check adapter. Every scientific script runs in a fresh copy.

No installs, source writes, stochastic searches or acquired code execution.
Exit zero means only the named bounded acceptance conditions passed.
"""
from pathlib import Path
import argparse,hashlib,json,math,shutil,subprocess,sys,tempfile,zipfile
HERE=Path(__file__).resolve().parent
DERIVED=HERE.parent
PACKAGE=DERIVED.parent
CHECKS={
 'polar':('root/check_known_operator_compiler.py','KNOWN_OPERATOR_CHECKS.json',{'status':'PASS_BOUNDED_ALGEBRA','polar_cases':32,'edge_cases':16}),
 'abstract':('root/check_abstract_isometry.py','ABSTRACT_ISOMETRY_CHECKS.json',{'status':'PASS','norm_polynomial_identity':True}),
 'compiler':('workers/gd_compiler_genesis/check_compiler_genesis.py','CHECKS.json',{}),
 'rotation':('workers/gd_compiler_adversary/independent_checks.py','CHECK_RESULTS.json',{}),
 'memory':('workers/gd_memory_receiving/check_receiving.py','checks.json',{'all_checks_passed':True}),
 'physical':('workers/gd_physical_operation/calculations/check_local_operation.py','CHECK_RESULTS.json',{}),
 'positivity':('workers/gd_positivity_frontier/check_exact.py','CHECKS.json',{'status':'PASS','number_of_checks':43}),
 'ticket':('../originals/pair_clock/pair_clock_adversary/check_ticket.py',None,{}),
 'runner':('workers/gd_replay_contract/test_gd_replay_contract.py',None,{})
}
def strict(s):
 return json.loads(s,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON '+x)))
def finite(v):
 if isinstance(v,float):assert math.isfinite(v),'nonfinite numeric output'
 if isinstance(v,dict):
  for x in v.values():finite(x)
 if isinstance(v,list):
  for x in v:finite(x)
def integrity():
 m=strict((PACKAGE/'SOURCE_MANIFEST.json').read_text())
 for row in m['archives']:
  p=PACKAGE/'originals'/row['archive'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];assert p.stat().st_size==row['bytes']
  with zipfile.ZipFile(p) as z:assert z.testzip() is None
 for row in m['members']:
  p=PACKAGE/row['path'];assert p.stat().st_size==row['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 assert len(m['archives'])==4 and len(m['members'])==43
 return {'archives':4,'expanded_members':43,'integrity_only':True}
def main():
 a=argparse.ArgumentParser();a.add_argument('--check',required=True,choices=['identity',*CHECKS]);args=a.parse_args()
 if args.check=='identity':data=integrity()
 else:
  rel,out,fields=CHECKS[args.check];source=(DERIVED/rel).resolve();assert source.is_file()
  with tempfile.TemporaryDirectory(prefix='gd-public-bounded-') as td:
   t=Path(td);dest=t/source.name;shutil.copy2(source,dest)
   if args.check=='runner':shutil.copy2(source.with_name('gd_replay_contract.py'),t/'gd_replay_contract.py')
   proc=subprocess.run([sys.executable,'-W','error',str(dest)],cwd=t,capture_output=True,text=True,timeout=240)
   if proc.returncode!=0 or (args.check!='runner' and proc.stderr):
    print(proc.stdout);print(proc.stderr,file=sys.stderr);raise AssertionError(f'{args.check} strict replay failed ({proc.returncode})')
   if out:
    output=t/out;assert output.is_file(),'missing fresh output';data=strict(output.read_text());finite(data)
    for k,v in fields.items():assert data.get(k)==v,(k,data.get(k),v)
    if args.check=='compiler':
     assert data['signed_jump_replacement']['cases']==16
     assert data['signed_jump_replacement']['same_floor_all_cases'] is True
     assert data['sharp_affine_Pauli_replacement']['cases']==48
    elif args.check=='rotation':
     assert data['actual_correction_unitary_errors']['cases']==360
     assert data['overlap_incidence']['both_css_sector_incidence']==22
    elif args.check=='physical':
     assert abs(data['inactive_difference_unhalved_trace_norm']-1)<1e-12
     assert data['both_sector_stream_incidence_by_duality']==22
    data={'fresh_json_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'finite_numeric_output':True}
   elif args.check=='runner':
    assert 'Ran 5 tests' in proc.stderr and 'OK' in proc.stderr;data={'bounded_contract_tests':5}
   else:
    assert '32556' in proc.stdout and '319' in proc.stdout;data={'comparable_ticket_checks':32556,'reachable_states':319}
 print(json.dumps({'status':'PASS','check':args.check,'evidence':data,'scope':'Named bounded acceptance only; no universal proof, external verification or physical validation.'}))
if __name__=='__main__':main()
