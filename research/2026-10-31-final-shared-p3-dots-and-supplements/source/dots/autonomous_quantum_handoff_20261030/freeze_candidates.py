from pathlib import Path
import hashlib,json,shutil
base=Path('producer-workspace/shared');r=base/'autonomous_quantum_handoff_20261030'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[
'native_locc_rollback_integration_20261030/EXTENDED_MACHINE_AND_OPERATOR_PROOF.md',
'native_locc_rollback_integration_20261030/ACTUAL_SUCCESS_SERVICE_AND_GLOBAL_ASSEMBLY.md',
'native_locc_rollback_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'autonomous_qca_native_bridge_20261030/EXACT_NATIVE_ATTEMPT_COMPILER.md',
'autonomous_qca_native_bridge_20261030/ACTUAL_GENERIC_TWO_SUCCESS_WITNESS_SUBSTITUTION.md',
'autonomous_qca_native_bridge_20261030/MECHANICAL_LEADING_RECTANGLE.md',
'native_qca_service_independent_audit_20261030/INDEPENDENT_SERVICE_REVIEW.md',
'native_qca_cavity_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'autonomous_qca_native_bridge_20261030/CP_NOISE_CAVITY_AND_MIXED_BAD_BOX_V1.md',
'transactional_regeneration_20261029/ACTUAL_RESET_INSTRUMENT_TAIL.md',
'transactional_regeneration_20261029/JOINT_LOCAL_LYAPUNOV_TAIL.md',
'global_energy_memory_root_20261030/GLOBAL_EXPONENTIAL_COMPILER.md',
'autonomous_gate_bridge_20261030/GLOBAL_EXPONENTIAL_CONTROLLER_INTERFACE_CANDIDATE.md',
'global_exponential_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md',
'live_busy_energy_root_20261030/DIRECT_SINGLETON_DERIVATION_V1.md',
'live_busy_activity_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'live_busy_activity_independent_audit_20261030/CONSTANT_SINGLETON_BUSY_MOMENT.md',
'native_locc_continuous_recipient_interface_20261030/Q_AND_RECEIVER_GLOBAL_MEMORY_CONTRACT.md',
'reusable_frame_handoff_20261030/REUSABLE_FINITE_GROUP_FRAME.md',
'reusable_frame_independent_audit_20261030/INDEPENDENT_REVIEW.md']
files=[]
for rel in paths:
 p=base/rel;assert p.exists(),rel
 d=r/'frozen_dependencies'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
 files.append({'path':str(p),'snapshot':str(d.relative_to(r)),'sha256':sha(p)})
local=sorted([p for p in r.iterdir() if p.is_file() and p.suffix in ['.md','.json','.py'] and p.name not in ['DEPENDENCY_MANIFEST.json','freeze_candidates.py']])
g=[{'path':p.name,'sha256':sha(p)} for p in local]
manifest={'status':'scoped new physical adapter/stopped-interface candidates; independent review pending; no whole computation theorem','author':'producer-workspace/complete_local_rollback_bridge; root supplied two-stopped-instrument simplification and SWAP routing comparator','governing':g,'files':files}
(r/'DEPENDENCY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
(r/'DEPENDENCY_SHA256.txt').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in files))
(r/'CANDIDATE_SHA256.txt').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in g))
print(len(files),'dependencies frozen.');print((r/'CANDIDATE_SHA256.txt').read_text())
