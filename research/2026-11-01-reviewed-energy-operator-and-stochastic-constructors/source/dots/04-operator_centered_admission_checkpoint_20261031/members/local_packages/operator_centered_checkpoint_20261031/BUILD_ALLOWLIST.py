"""Deterministic explicit-allowlist LOCAL archive; no networking/upload."""
from pathlib import Path
import hashlib,json,zipfile,stat
ROOT=Path(__file__).resolve().parents[2]
PKG=Path(__file__).resolve().parent
GROUPS={
'raw_local_operator_acquisition_20261031': '''RAW_OPERATOR_ACQUISITION_AND_RECEIVING.md
RAW_OPERATOR_INDEPENDENT_REVIEW.md
OPERATOR_SCHEDULE_INDEPENDENT_REVIEW.md
acquire_operator_certificate.py
acquire_operator_certificate_pre_complex_normalization.py
test_operator_certificate.py
receive_operator_schedule.py
test_operator_schedule.py
check_raw_operator_independent.py
check_schedule_independent.py
raw_operator_independent_checks.json
schedule_independent_checks.json
operator_certificate_checks.json
operator_schedule_checks.json
operator_acquisition_resource_rows.json
mixed_qutrit_input.json
mixed_qutrit_certificate.json
qubit_hopping_input.json
qubit_hopping_certificate.json
charged_creation_input.json
charged_creation_certificate.json
qutrit_complete_schedule_input.json
qutrit_complete_schedule_certificate.json'''.splitlines(),
'centered_source_acquisition_20261031': '''GENERAL_DRIFT_CLAMPED_RECEIVER.md
CENTERED_SOURCE_ACQUISITION_SPEC.md
CENTERED_ACQUISITION_INDEPENDENT_REVIEW.md
acquire_centered_certificate.py
receive_centered_schedule.py
test_centered_acquisition.py
check_centered_independent.py
centered_acquisition_checks.json
centered_independent_checks.json
centered_resource_rows.json
x_loss_input.json
x_loss_certificate.json
x_complete_schedule_input.json
x_complete_schedule_certificate.json
paid_activation_input.json
paid_activation_certificate.json
two_jump_qutrit_input.json
two_jump_qutrit_certificate.json
guarded_comparison_input.json
guarded_comparison_certificate.json'''.splitlines(),
'local_injection_fault_admission_20261031': '''CLAMPED_WEIGHT_INJECTION_CANDIDATE.md
CLAMPED_WEIGHT_INDEPENDENT_REVIEW.md
CLAMPED_WEIGHT_FINAL_SOURCE_BINDING.md
CLAMPED_WEIGHT_REVIEWER_RECEIPT.md
check_clamped_weight_independent.py
check_clamped_weight_independent.json
SOURCE_CREATION_ACTIVITY_CANDIDATE.md
SOURCE_CREATION_ACTIVITY_REVIEW.md
check_creation_activity.py
check_creation_activity.json'''.splitlines(),
'local_energy_fault_admission_20261031': '''QUANTUM_OCCUPATION_LOCAL_ADMISSION_CANDIDATE.md
INDEPENDENT_LOCAL_ADMISSION_REVIEW.md
LOSS_TO_COUPLING_RESOURCE_COROLLARY.md
LOSS_TO_COUPLING_INDEPENDENT_REVIEW.md
acquire_local_admission.py
KNOWN_MODEL_COMPILER_SPEC.md
KNOWN_MODEL_COMPILER_INDEPENDENT_REVIEW.md
PRIMARY_COMPARISON_AND_CONSEQUENCE_BOUNDARY.md
SHARED_SPECTATOR_GUARD_EXTENSION.md
SHARED_SPECTATOR_INDEPENDENT_REVIEW.md'''.splitlines(),
'local_packages/operator_centered_checkpoint_20261031':['README.md','REVIEW_BINDINGS.json','BUILD_ALLOWLIST.py']}
paths=sorted(str(Path(d)/f) for d,fs in GROUPS.items() for f in fs)
if len(paths)!=len(set(paths)):raise RuntimeError('duplicate allowlist')
payload={}
for rel in paths:
    p=ROOT/rel
    if not p.is_file() or p.is_symlink() or '..' in Path(rel).parts:raise RuntimeError('invalid allowlisted path '+rel)
    payload[rel]=p.read_bytes()
bindings=json.loads((PKG/'REVIEW_BINDINGS.json').read_text())
for item in bindings['files']:
    if item['path'] not in payload:raise RuntimeError('binding outside payload')
    if hashlib.sha256(payload[item['path']]).hexdigest()!=item['sha256']:raise RuntimeError('binding mismatch '+item['path'])
manifest={'format':'explicit-scientific-allowlist-v1','files':[{'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for rel,b in sorted(payload.items())]}
manifest_bytes=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
(PKG/'MANIFEST.json').write_bytes(manifest_bytes)
payload['MANIFEST.json']=manifest_bytes
out=PKG.parent/'operator_centered_admission_checkpoint_20261031.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for rel,b in sorted(payload.items()):
        info=zipfile.ZipInfo(rel,date_time=(2026,10,31,17,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(out) as z:
    if set(z.namelist())!=set(payload) or len(z.namelist())!=len(payload):raise RuntimeError('ZIP member mismatch')
    if z.testzip() is not None:raise RuntimeError('ZIP CRC failure')
    for rel,b in payload.items():
        if z.read(rel)!=b:raise RuntimeError('readback mismatch '+rel)
print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':len(payload),'local_only':True},indent=2))
