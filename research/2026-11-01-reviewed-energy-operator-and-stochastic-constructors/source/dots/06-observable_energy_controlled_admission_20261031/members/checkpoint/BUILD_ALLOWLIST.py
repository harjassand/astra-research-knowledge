"""Local-only, literal-allowlist scientific checkpoint. No network or uploads."""
from pathlib import Path
import hashlib, json, zipfile, sys
META=Path(__file__).resolve().parent
ROOT=(META.parent if (META.parent/'centered_mixing_fault_admission_20261031').is_dir() else META.parents[1])
FILES=[
'centered_mixing_fault_admission_20261031/OBSERVABLE_DECAY_LOCAL_ADMISSION_CANDIDATE.md',
'centered_mixing_fault_admission_20261031/OBSERVABLE_DECAY_INDEPENDENT_REVIEW.md',
'centered_mixing_fault_admission_20261031/OBSERVABLE_DECAY_REVIEWER_RECEIPT.md',
'centered_mixing_fault_admission_20261031/BACKWARD_CONTROLLED_OBSERVABLE_ADMISSION_CANDIDATE.md',
'centered_mixing_fault_admission_20261031/BACKWARD_CONTROLLED_INDEPENDENT_REVIEW.md',
'centered_mixing_fault_admission_20261031/ROBUST_BACKWARD_OBSERVABLE_COROLLARY.md',
'centered_mixing_fault_admission_20261031/ROBUST_BACKWARD_INDEPENDENT_REVIEW.md',
'centered_mixing_fault_admission_20261031/BACKWARD_AND_ROBUST_REVIEWER_RECEIPT.md',
'centered_mixing_fault_admission_20261031/ENERGY_TO_CONTROLLED_FAULT_RECEIVING.md',
'centered_mixing_fault_admission_20261031/ENERGY_RECEIVING_INDEPENDENT_REVIEW.md',
'centered_mixing_fault_admission_20261031/PHYSICAL_RECEIVING_AND_CONSEQUENCE_BOUNDARY.md',
'centered_mixing_fault_admission_20261031/check_observable_decay.py',
'centered_mixing_fault_admission_20261031/check_observable_decay.json',
'centered_mixing_fault_admission_20261031/check_backward_control.py',
'centered_mixing_fault_admission_20261031/check_backward_control.json',
'quantum_effective_channel_20261031/DARK_SOURCE_LOGICAL_REDUCTION_CANDIDATE.md',
'quantum_effective_channel_20261031/DARK_LOGICAL_REDUCTION_INDEPENDENT_REVIEW.md',
'centered_creation_benchmark_20261031/EXACT_DEPHASING_AMPLITUDE_BENCHMARK.md',
'centered_creation_benchmark_20261031/BENCHMARK_LOCAL_INDEPENDENT_REVIEW.md',
'centered_creation_benchmark_20261031/check_benchmark.py',
'centered_creation_benchmark_20261031/benchmark_checks.json',
'effective_operation_tradeoff_20261031/SOURCE_ONLY_MEDIATOR_TRADEOFF_CANDIDATE.md',
'effective_operation_tradeoff_20261031/SOURCE_ONLY_MEDIATOR_INDEPENDENT_REVIEW.md',
'effective_operation_tradeoff_20261031/check_mediator_algebra.py',
'effective_operation_tradeoff_20261031/check_mediator_algebra.json',
'effective_operation_tradeoff_20261031/mediator_independent_rerun.json',
]
BINDINGS=[
(FILES[0],'faedb2f2f8ec0c491f4ade4d71a4075df143eb7fa2489c8f0e8c091a0af5d37e',[FILES[2]]),
(FILES[3],'f2d89255727d94d8a4e1a4af08c906e1e39c7fbff6149c40ee72b0f54b4d3a3c',[FILES[4],FILES[7]]),
(FILES[5],'e2c7a9a80aad1bca93a50cfee8b29b2c3bb0d44679aa8675a0d0f8bdc10a5ad6',[FILES[6],FILES[7]]),
(FILES[8],'6e27181cb87d96137e0cc3793ba926beb598bbc9c4c63ec9f50db8a0b7933a4e',[FILES[9]]),
(FILES[15],'ff711b0d4c93d0b0a0b86a1ac09bcc20affac0716ef50d87732036601acf2229',[FILES[16],FILES[9]]),
(FILES[17],'56c28983afe5148104ccb759888ef63f22ee7253dd690fc5564942c37eaeed99',[FILES[18]]),
(FILES[21],'a5dfb31c88cb9127149370c07fa1bd8bcfd86f682b7a5e8301de87d81306d8d0',[FILES[22]]),
]
def digest(b):return hashlib.sha256(b).hexdigest()
def read(path):
 p=ROOT/path
 if p.is_symlink() or not p.is_file():raise ValueError('not a regular allowed file: '+path)
 return p.read_bytes()
payload={f:read(f) for f in FILES}
records=[]
for source,expected,receipts in BINDINGS:
 assert digest(payload[source])==expected,(source,'source hash changed')
 for receipt in receipts:assert expected.encode() in payload[receipt],(receipt,'missing full source binding')
 records.append({'source':source,'sha256':expected,'receipts':[{'path':p,'sha256':digest(payload[p])} for p in receipts]})
binding={'bindings':records,'historical_review':{'path':FILES[1],'binds':'c2905f139495a5a4d13754f9d85b42c618eee6ebe15feeecc03868d8fe2180a3','scope':'Earlier source version. Current faed source is bound by OBSERVABLE_DECAY_REVIEWER_RECEIPT.md. No inference that this earlier receipt binds current bytes.'},'comparison_note':'Physical receiving note is scoped assessment, not an additional independently reviewed theorem. Benchmark local receipt does not re-audit all cited literature.'}
(META/'REVIEW_BINDINGS.json').write_text(json.dumps(binding,indent=2)+'\n')
for name in ['README.md','REVIEW_BINDINGS.json','BUILD_ALLOWLIST.py']:
 p=META/name
 assert p.is_file() and not p.is_symlink()
 payload['checkpoint/'+name]=p.read_bytes()
manifest={'format':'strict-allowlist-local-checkpoint-v1','scope':'Reviewed mathematical local admission closure; no hardware/gate backend/novelty claim; local only.','files':[{'path':n,'bytes':len(b),'sha256':digest(b)} for n,b in sorted(payload.items())]}
mb=(json.dumps(manifest,indent=2)+'\n').encode();(META/'MANIFEST.json').write_bytes(mb);payload['checkpoint/MANIFEST.json']=mb
out=ROOT/'local_packages/observable_energy_controlled_admission_20261031.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,b in sorted(payload.items()):
  info=zipfile.ZipInfo(name,date_time=(2026,10,31,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,b)
with zipfile.ZipFile(out) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(payload)
 assert set(z.namelist())==set(payload)
 assert z.testzip() is None
 for name,b in payload.items():assert z.read(name)==b
 # Validate manifest independently against ZIP readback.
 for rec in json.loads(z.read('checkpoint/MANIFEST.json'))['files']:
  b=z.read(rec['path']);assert len(b)==rec['bytes'] and digest(b)==rec['sha256']
# Prove original scientific files were not changed while building.
for name in FILES:assert read(name)==payload[name]
print(json.dumps({'path':str(out),'bytes':out.stat().st_size,'sha256':digest(out.read_bytes()),'members':len(payload),'verified':'literal allowlist, exact binding hashes, no duplicate members, CRC, byte readback, manifest, original bytes'},indent=2))
