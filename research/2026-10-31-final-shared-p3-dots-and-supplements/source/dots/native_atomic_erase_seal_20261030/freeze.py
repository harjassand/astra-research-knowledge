from pathlib import Path
import hashlib,json,shutil
root=Path('producer-workspace/shared'); out=Path(__file__).parent
files=[
'atomic_erasure_root_20261030/FREE_TAG_ERASE_AND_RESERVE.md',
'native_locc_rollback_integration_20261030/EXTENDED_MACHINE_AND_OPERATOR_PROOF.md',
'native_locc_rollback_integration_20261030/check_extended_owner_table.py',
'autonomous_qca_native_bridge_20261030/EXACT_NATIVE_ATTEMPT_COMPILER.md',
'autonomous_qca_native_bridge_20261030/ACTUAL_GENERIC_TWO_SUCCESS_WITNESS_SUBSTITUTION.md',
'native_qca_service_independent_audit_20261030/INDEPENDENT_SERVICE_REVIEW.md',
'autonomous_quantum_handoff_20261030/NATIVE_PAUSE_RETIRE_AND_LIVE_ACK_ADAPTER.md',
'native_pause_stopped_interface_audit_20261030/INDEPENDENT_REVIEW.md',
'native_pause_stopped_interface_audit_20261030/check_actual_park_extension.py',
'native_pause_stopped_interface_audit_20261030/check_actual_park_extension.json',
'autonomous_qca_native_bridge_20261030/READ_ONLY_CLASSICAL_CLOCK_COMPILER.md',
'autonomous_qca_native_bridge_20261030/MECHANICAL_LEADING_RECTANGLE.md',
 'transactional_data_bridge_20261029/COEFFICIENTWISE_COMPILER_INTERFACE.md',
 'transactional_regeneration_20261029/ACTUAL_RESET_INSTRUMENT_TAIL.md',
 'transactional_regeneration_20261029/JOINT_LOCAL_LYAPUNOV_TAIL.md']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=[]
for rel in files:
 p=root/rel
 if not p.exists():raise FileNotFoundError(p)
 q=out/'frozen_dependencies'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 manifest.append({'live':str(p),'snapshot':str(q),'sha256':sha(p)})
(out/'DEPENDENCY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for p in sorted(out.glob('*')):
 if p.is_file() and p.suffix in {'.md','.py','.json'}:print(sha(p),p.name)
