from pathlib import Path
import hashlib,json,shutil
base=Path('producer-workspace/shared'); root=base/'native_locc_continuous_recipient_interface_20261030'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entries={}
for e in json.loads((base/'native_locc_continuous_memory_20261030/DEPENDENCY_MANIFEST.json').read_text())['files']:
    p=Path(e['path']); assert sha(p)==e['sha256'],str(p)
    entries[p]={'role':'transitive frozen whole continuous AB dependency','expected':e['sha256']}
paths={
'continuous AB whole':[
'native_locc_continuous_memory_20261030/ACTUAL_NATIVE_LOCC_CONTINUOUS_MEMORY_V1.md',
'native_locc_continuous_whole_independent_audit_20261030/WHOLE_RECEIPT.md'],
'new joint and activity receiving':[
'continuous_native_recipient_root_20261030/JOINT_OPERATOR_SOURCE_COMPOSITION.md',
'continuous_native_recipient_root_20261030/GLOBAL_ACTIVITY_DENSITY_LEMMA.md',
'continuous_recipient_joint_activity_audit_20261030/INDEPENDENT_REVIEW.md',
'continuous_recipient_actual_source_audit_20261030/INDEPENDENT_REVIEW.md'],
'exact Q/new-B theorem and apparatus':[
'global_energy_memory_root_20261030/GLOBAL_EXPONENTIAL_COMPILER.md',
'autonomous_gate_bridge_20261030/GLOBAL_EXPONENTIAL_CONTROLLER_INTERFACE_CANDIDATE.md',
'global_exponential_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md',
'native_continuous_bridge_20261030/NATIVE_CONTINUOUS_BRIDGE_MANUSCRIPT_V1.md',
'live_busy_energy_root_20261030/DIRECT_SINGLETON_DERIVATION_V1.md',
'live_busy_activity_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'live_busy_energy_root_20261030/READOUT_WITHOUT_RETIREMENT_DWELL.md',
'live_access_independent_audit_20261030/INDEPENDENT_REVIEW.md'],
'finite native AB shutdown ONLY; stochastic source not imported':[
'native_recipient_drain_bridge_20261030/NATIVE_OLD_LIVE_ACCESS_AND_SHUTOFF.md',
'native_recipient_drain_bridge_20261030/NATIVE_RECIPIENT_MANUSCRIPT_V1.md',
'native_recipient_whole_independent_audit_20261030/INDEPENDENT_WHOLE_REVIEW.md'],
'finite endpoint ONLY; atomic waiting/removal not imported':[
'recipient_memory_bridge_20261030/RATE_SEPARATED_RECIPIENT_V2.md',
'recipient_memory_bridge_20261030/FINITE_RAW_MASK_CARRIER.md',
'recipient_memory_bridge_20261030/FINITE_NATIVE_ACTIVATION_AND_WARM_CHANNEL_V2.md',
'recipient_memory_bridge_20261030/joint_span/JOINT_SIGNED_RESOURCE_TO_RECEIVER_SPAN.md',
'recipient_whole_independent_audit_20261030/INDEPENDENT_WHOLE_REVIEW.md',
'finite_data_shutoff_20261030/FINITE_DATA_SHUTOFF_SUPPORT_BRIDGE.md',
'finite_data_shutoff_independent_audit_20261030/INDEPENDENT_REVIEW.md',
'noisy_controller_boot_root_20261030/FINITE_TIME_BOOT.md',
'noisy_controller_boot_independent_audit_20261030/INDEPENDENT_REVIEW.md']}
for role,ls in paths.items():
    for rel in ls: entries[base/rel]={'role':role}
files=[]
for p,meta in entries.items():
    assert p.is_file(),str(p)
    dest=root/'frozen_dependencies'/p.relative_to(base);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    files.append({'path':str(p),'snapshot':str(dest.relative_to(root)),'sha256':sha(p),'role':meta['role']})
local=['CONTINUOUS_NATIVE_QUANTUM_RECIPIENT_V1.md','ACTUAL_TWO_LAB_ACTIVITY_AND_JOINT_SOURCE.md','Q_AND_RECEIVER_GLOBAL_MEMORY_CONTRACT.md','check_joint_kill_and_activity_order.py','check_joint_kill_and_activity_order.json']
manifest={'status':'FROZEN NEW whole continuous recipient candidate; fresh whole review pending','scope':'common waiting start; exact clean source; continuous moving-partner bounded-body incident joint-cb noise; actual finite endpoint; encoded Q input and ideal ordinary DATA recovery','governing':[{'path':x,'sha256':sha(root/x)} for x in local], 'files':files}
(root/'DEPENDENCY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
(root/'DEPENDENCY_SHA256.txt').write_text(''.join(e['sha256']+'  '+e['path']+'\n' for e in files))
(root/'GOVERNING_SHA256.txt').write_text(''.join(sha(root/x)+'  '+x+'\n' for x in local))
print(json.dumps({'dependencies':len(files),'governing':manifest['governing']},indent=2))
