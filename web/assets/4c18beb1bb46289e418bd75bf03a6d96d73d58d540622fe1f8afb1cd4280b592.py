"""Build immutable Cycle07 packets after the final zero-pending inventory.

All previous output packets remain unchanged. The current status and ledger
are versioned in checkpoint06 before their planned checkpoint07 replacement.
"""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2]; A=R/'work/agents'; S=R/'work/state'; O=R/'outputs'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
gate=json.loads((S/'CYCLE07_READY.json').read_text())
assert gate['pending_worker_reports']==gate['unclassified_artifacts']==0
packets={
 'sharp-entropy-constants':{
  'stationary-origin':'variance_monogamy_sol/cycle07_stationary_hessian',
  'stationary-independent-and-nonlinear-gates':'complexity_proof_recon/cycle07_qubit_reference',
  'sharpness-independent-and-audit':'algebra_proof_recon/cycle07_pi_sharpness_review',
  'global-qubit-origin':'complexity_proof_recon/cycle07_qubit_constant',
  'global-qubit-review':'tensor_frame_sol/cycle07_global_qubit_pi_review',
  'physical-entropy-resolvent':'covariant_review_sol/cycle07_perspective_bridge',
  'finite-nonlinear-audit':'covariant_review_sol/cycle07_finite7_review',
  'nonlinear-secant-transfer':'variance_monogamy_sol/cycle07_nonlinear_transfer',
  'source-interface-checks':'dilation_literature_luna/cycle07_regularities_interfaces',
  'constant-prior-checks':'dilation_literature_luna/cycle07_pi_constant_prior',
  'root':'root_cycle07',
 },
 'record-stability-refinements':{
  'origin-and-failed-families':'foundational_transfer_sol/cycle07_two_record_gate',
  'independent-and-review':'spin1_anisotropic_sol/cycle07_classical_record_review',
 }
}
for name,parts in packets.items():
 dest=O/name; assert not dest.exists(),dest; dest.mkdir()
 copied=[]
 for label,rel in parts.items():
  src=A/rel; assert src.is_dir(),src
  shutil.copytree(src,dest/label,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  for p in sorted((dest/label).rglob('*')):
   if p.is_file():
    original=src/p.relative_to(dest/label)
    assert p.read_bytes()==original.read_bytes()
    copied.append({'path':str(p.relative_to(dest)),'source':str(original.relative_to(R)),'sha256':sha(p)})
 readme=S/(name+'_README.txt'); assert readme.exists(),readme
 shutil.copyfile(readme,dest/'README.txt')
 rows=[{'path':str(p.relative_to(dest)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(dest.rglob('*')) if p.is_file()]
 save(dest/'MANIFEST.json',{'checkpoint':'07','scope':'File integrity; not formal or external mathematical validation.','copied_frozen_files':copied,'all_packet_files':rows})
ledger=json.loads((R/'work/checkpoints/checkpoint06/CLAIM_LEDGER.json').read_text())
addition=json.loads((S/'cycle07_claim_additions.json').read_text())
old_ids={c['id'] for c in ledger['claims']}
assert len({c['id'] for c in addition['claims']})==len(addition['claims'])
assert not old_ids.intersection(c['id'] for c in addition['claims'])
ledger['claims'].extend(addition['claims'])
ledger.update(checkpoint='07',objective_achieved=False,historical_novelty='UNKNOWN',external_validation=False,formal_kernel_replay=False,
 current_lead='Sharp universal stationary entropy/root-energy constant pi; global nonlinear qubit pi; general nonlinear endpoint remains unresolved.',
 historical_entries_note='Earlier frozen entries retain historical status. Cycle07 closure and new entries record later strengthening without silently rewriting those artifacts.')
save(S/'CLAIM_LEDGER.json',ledger);save(O/'CLAIM_LEDGER.json',ledger)
print(json.dumps({'new_packets':list(packets),'claims':len(ledger['claims']),'objective_achieved':False},indent=2))
