"""Build new Cycle08 packet only after the independent zero-pending inventory.
Older proof packets remain byte-for-byte unchanged. Current top-level status
and ledger are versioned in checkpoint07 before checkpoint08 replacement.
"""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2];A=R/'work/agents';S=R/'work/state';O=R/'outputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
gate=json.loads((S/'CYCLE08_READY.json').read_text())
assert gate['pending_worker_reports']==gate['unclassified_artifacts']==0
parts={
 'general-origin':'foundational_transfer_sol/cycle08_general_kernel',
 'general-independent-variance':'variance_monogamy_sol/cycle08_universal_endpoint_review',
 'general-independent-complexity':'complexity_proof_recon/cycle08_universal_falsification',
 'general-physical-audit':'covariant_review_sol/cycle08_universal_gram_review',
 'general-representation':'algebra_proof_recon/cycle08_full_representation_audit',
 'general-canonical-consequences':'tensor_frame_sol/cycle08_general_canonical_consequences',
 'qubit-origin':'tensor_frame_sol/cycle08_complete_qubit',
 'qubit-scalar-independent':'complexity_proof_recon/cycle08_scalar_kernel',
 'qubit-exposed-review':'spin1_anisotropic_sol/cycle08_complete_qubit_review',
 'star-origin':'covariant_review_sol/cycle08_physical_gram',
 'star-independent-and-review':'variance_monogamy_sol/cycle08_nonlinear_star',
 'pure-boundary-review':'broadcasting_proof_sol/cycle08_pure_boundary_review',
 'secant-obstructions':'algebra_proof_recon/cycle08_secant_completion',
 'operator-convex-prior':'dilation_literature_luna/cycle08_petz_pi_prior',
 'qubit-prior':'dilation_literature_luna/cycle08_complete_qubit_prior',
 'universal-prior':'dilation_literature_luna/cycle08_universal_pi_endpoint_addendum',
 'root':'root_cycle08',
}
dest=O/'universal-entropy-pi';assert not dest.exists(),dest;dest.mkdir()
copied=[]
for label,rel in parts.items():
 src=A/rel;assert src.is_dir(),src
 shutil.copytree(src,dest/label,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for p in sorted((dest/label).rglob('*')):
  if p.is_file():
   original=src/p.relative_to(dest/label);assert p.read_bytes()==original.read_bytes()
   copied.append({'path':str(p.relative_to(dest)),'source':str(original.relative_to(R)),'sha256':sha(p)})
shutil.copyfile(S/'universal-entropy-pi_README.txt',dest/'README.txt')
rows=[{'path':str(p.relative_to(dest)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(dest.rglob('*')) if p.is_file()]
save(dest/'MANIFEST.json',{'checkpoint':'08','scope':'Integrity only, not external or formal mathematical validation.','copied_frozen_files':copied,'all_packet_files':rows})
ledger=json.loads((R/'work/checkpoints/checkpoint07/CLAIM_LEDGER.json').read_text())
addition=json.loads((S/'cycle08_claim_additions.json').read_text());old={c['id'] for c in ledger['claims']}
assert len({c['id'] for c in addition['claims']})==len(addition['claims'])
assert not old.intersection(c['id'] for c in addition['claims'])
ledger['claims'].extend(addition['claims'])
ledger.update(checkpoint='08',objective_achieved=False,historical_novelty='UNKNOWN',external_validation=False,formal_kernel_replay=False,
 current_lead='Sharp universal nonlinear entropy/root-energy constant pi for all finite KMS QMS, including complete finite reference amplification; internally proved and adversarially audited.',
 historical_entries_note='Earlier frozen statuses remain historical. Cycle08 closure and new entries explicitly supersede general nonlinear/complete endpoint UNKNOWN without rewriting older proofs.')
save(S/'CLAIM_LEDGER.json',ledger);save(O/'CLAIM_LEDGER.json',ledger)
print(json.dumps({'new_packet':'universal-entropy-pi','copied_files':len(copied),'claims':len(ledger['claims']),'objective_achieved':False},indent=2))
