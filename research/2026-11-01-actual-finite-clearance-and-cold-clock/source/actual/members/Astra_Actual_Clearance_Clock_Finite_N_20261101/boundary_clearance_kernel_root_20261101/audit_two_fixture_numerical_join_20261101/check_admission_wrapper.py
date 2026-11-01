#!/usr/bin/env python3
"""Read-only original binding checks; ordinary CLI/refusal tests use copies only."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
CONSUMER=ROOT/'boundary_clearance_kernel_root_20261101/finite_window_consumer'
EXPECTED_CODE='ec16653b1c91774ba7474006459612368225c51b5c0528c32831bee2c2dabfcd'
EXPECTED_MANIFEST='fee8f271579ea33764074c824624c8b1882f8602a9fdeb8aac9ac575f5848f48'
EXPECTED_OUTPUT='272e0b0b442872a45bb99621ab4888d5e108e2aa212c84a7c1da47fd9f54fa32'
EXPECTED_FREEZE='a45d767ce9b4f3e21766c7a44303dc65e4a60e326f3f89131d686923c6bcd5ee'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(CONSUMER/'admit.py')==EXPECTED_CODE
assert sha(CONSUMER/'ADMISSION_SOURCE_BINDINGS.json')==EXPECTED_MANIFEST
assert sha(CONSUMER/'ADMITTED_WINDOWS.json')==EXPECTED_OUTPUT
assert sha(CONSUMER/'AUTHOR_FREEZE.json')==EXPECTED_FREEZE
freeze=json.loads((CONSUMER/'AUTHOR_FREEZE.json').read_text())
assert len(freeze['files'])==6
for row in freeze['files']:assert sha(CONSUMER/row['path'])==row['sha256']
manifest=json.loads((CONSUMER/'ADMISSION_SOURCE_BINDINGS.json').read_text())
assert manifest['status']=='ALL_REQUIRED_COMPONENTS_RECEIVED'
assert len(manifest['files'])==41
names=set();total_bytes=0
for row in manifest['files']:
 name=row['path'];assert name not in names;names.add(name)
 p=ROOT/name;assert sha(p)==row['sha256'];assert p.stat().st_size==row['bytes']
 total_bytes+=row['bytes']
 if 'accepted_status' in row:
  assert json.loads(p.read_text())[row.get('accepted_status_key','status')]==row['accepted_status']
assert total_bytes==435087

expected=json.loads((CONSUMER/'ADMITTED_WINDOWS.json').read_text())
arith=json.loads((HERE/'ARITHMETIC_RESULTS_PENDING_ADMISSION.json').read_text())
assert expected['confidence_lower']=='99%' and expected['source_files_verified']==41
for got,want in zip(expected['fixtures'],arith['fixtures']):
 for key in ['N','T','scaled_interval','physical_interval','residual_upper','bracket_upper','jump_upper','martingale_radius_upper','epsilon_upper']:
  assert got[key]==want[key]
 assert got['cold_speedup_claim'] is False

tests=[]
with tempfile.TemporaryDirectory(prefix='clock_fixture_ordinary_refusal_',dir='/tmp') as td:
 copyroot=Path(td)
 for row in manifest['files']:
  dest=copyroot/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/row['path'],dest)
 copyconsumer=copyroot/'boundary_clearance_kernel_root_20261101/finite_window_consumer'
 copyconsumer.mkdir(parents=True,exist_ok=True)
 for name in ['admit.py','ADMISSION_SOURCE_BINDINGS.json']:
  shutil.copyfile(CONSUMER/name,copyconsumer/name)
 def run(label,args=(),valid=False,expected_rows=None):
  proc=subprocess.run([sys.executable,str(copyconsumer/'admit.py'),*args],capture_output=True,text=True,check=False)
  if valid:
   assert proc.returncode==0,(label,proc.stdout,proc.stderr)
   obj=json.loads(proc.stdout);assert obj['status']=='ADMITTED_UNDER_BOUND_SOURCE_THEOREMS'
   assert obj['fixtures']==expected_rows
  else:
   assert proc.returncode==2,(label,proc.returncode,proc.stdout,proc.stderr)
   if proc.stdout.strip():
    obj=json.loads(proc.stdout);assert obj['status']=='UNKNOWN'
   else:obj={'status':'ARGUMENT_REJECTED','reason':proc.stderr.splitlines()[-1]}
   assert '"status": "ADMITTED' not in proc.stdout
  reason=obj.get('reason')
  if reason is not None:reason=reason.replace(str(copyroot),'<temporary_fixture_root>')
  tests.append({'label':label,'exit_code':proc.returncode,'status':obj['status'],'reason':reason,
                'byte_identical_to_saved_output':proc.stdout==(CONSUMER/'ADMITTED_WINDOWS.json').read_text() if label=='both_fixtures' else None})
 run('both_fixtures',valid=True,expected_rows=expected['fixtures'])
 for t,row in zip(['10000','100000'],expected['fixtures']):run('single_fixture_'+t,['--T',t],True,[row])
 for bad in ['9999','50000','100001','100000000000000000000']:
  run('unsupported_T_'+bad,['--T',bad])

 # Reproduce the precise omission weakness reported against the first wrapper;
 # the repaired digest pin must reject it despite >20 files remaining.
 raw_receipt='boundary_clearance_kernel_root_20261101/audit_global_clock_bracket_residual_20261101/REVIEW_RECEIPT.json'
 changed=dict(manifest);changed['files']=[r for r in manifest['files'] if r['path']!=raw_receipt]
 assert len(changed['files'])==40
 (copyconsumer/'ADMISSION_SOURCE_BINDINGS.json').write_text(json.dumps(changed,indent=2)+'\n')
 run('manifest_omits_essential_raw_receipt_with_40_files_left')
 shutil.copyfile(CONSUMER/'ADMISSION_SOURCE_BINDINGS.json',copyconsumer/'ADMISSION_SOURCE_BINDINGS.json')

 targets=[
  ('missing_raw_residual','boundary_clearance_kernel_root_20261101/actual_clock_residual_receiver_20261101/ACTUAL_CLOCK_RESIDUAL_BUDGET.md','delete'),
  ('changed_full_bracket','return_path_construction_20261101/rate2_task_observable_corrector/global_l_weighted_bracket/FULL_CORRECTED_CLOCK_BRACKET.md','append'),
  ('changed_scalar_certificate','inverse_clearance_clock_20261101/CERTIFICATE_FINE.json','append'),
  ('changed_gate_receipt','boundary_clearance_kernel_root_20261101/audit_actual_gates_tilted_20261101_0800/REVIEW_RECEIPT.json','append'),
  ('missing_entropy_receipt','return_path_construction_20261101/rate2_factorial_entropy_service/audit_factorial_entropy_service_20261101_0721/REVIEW_RECEIPT.json','delete'),
 ]
 for label,name,kind in targets:
  p=copyroot/name
  if kind=='delete':p.unlink()
  else:p.write_bytes(p.read_bytes()+b'\n')
  run(label)
  shutil.copyfile(ROOT/name,p)
 run('restored_complete_copy',valid=True,expected_rows=expected['fixtures'])

for row in manifest['files']:
 assert sha(ROOT/row['path'])==row['sha256']
assert sha(CONSUMER/'admit.py')==EXPECTED_CODE
assert sha(CONSUMER/'ADMISSION_SOURCE_BINDINGS.json')==EXPECTED_MANIFEST

result={
 'status':'PASS_REPAIRED_SOURCE_BOUND_WRAPPER_AND_ORDINARY_REFUSALS',
 'code_sha256':EXPECTED_CODE,'manifest_sha256':EXPECTED_MANIFEST,'output_sha256':EXPECTED_OUTPUT,
 'author_freeze_sha256':EXPECTED_FREEZE,'author_freeze_files_verified':6,
 'manifest_files_verified':41,'manifest_payload_bytes':total_bytes,
 'independent_arithmetic_match':True,'ordinary_cli_tests':tests,
 'negative_tests_used_only_temporary_copies':True,
 'original_sources_unchanged':True,
 'no_cache_or_hardware_experiments':True,
}
(HERE/'ADMISSION_WRAPPER_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
