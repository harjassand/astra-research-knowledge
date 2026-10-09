"""Copy the new frozen packet and append claims only after the final inventory."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2];A=R/'work/agents';S=R/'work/state';O=R/'outputs'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
gate=json.loads((S/'CYCLE09_READY.json').read_text())
assert gate['pending_worker_reports']==gate['unclassified_artifacts']==0
parts={
 'kms-origin':'foundational_transfer_sol/cycle09_full_lp',
 'kms-independent':'complexity_proof_recon/cycle09_lp_falsification',
 'kms-sharpness':'algebra_proof_recon/cycle09_lp_sharpness',
 'kms-review':'covariant_review_sol/cycle09_lp_review',
 'nonkms-lower':'foundational_transfer_sol/cycle09_nonreversible_lower',
 'nonkms-gram-review':'covariant_review_sol/cycle09_nonreversible_gram_review',
 'nonkms-p-review':'covariant_review_sol/cycle09_nonreversible_lp_review',
 'nonkms-upper':'covariant_review_sol/cycle09_nonreversible_gate',
 'nonkms-physical-review':'algebra_proof_recon/cycle09_nonreversible_review',
 'nonkms-upper-review':'algebra_proof_recon/cycle09_nonreversible_phase_review',
 'raw-origin':'tensor_frame_sol/cycle09_raw_quantum_classicality',
 'raw-review':'variance_monogamy_sol/cycle09_raw_gate_review',
 'stationarity-origin':'variance_monogamy_sol/cycle09_stationary_repair',
 'stationarity-review':'broadcasting_proof_sol/cycle09_stationarity_review',
 'petz-origin':'tensor_frame_sol/cycle09_petz_symmetrization',
 'petz-review':'variance_monogamy_sol/cycle09_quantum_petz',
 'lp-interfaces-prior':'dilation_literature_luna/cycle09_full_lp_interfaces',
 'sine-prior':'dilation_literature_luna/cycle09_sine_profile_prior',
 'nonkms-weak-prior':'dilation_literature_luna/cycle09_nonreversible_weak_prior',
 'tangent-prior':'dilation_literature_luna/cycle09_nonreversible_profile_prior',
 'stationary-petz-prior':'broadcast_literature_luna/cycle09_stationary_petz_prior',
 'pretty-good-prior':'broadcast_literature_luna/cycle09_pretty_good_reverse',
 'raw-power-prior':'broadcast_literature_luna/cycle09_raw_power_prior',
 'root':'root_cycle09',
}
dest=O/'stationary-regularity-and-raw-classicality';assert not dest.exists();dest.mkdir()
copied=[]
for label,rel in parts.items():
 src=A/rel;assert src.is_dir(),src
 shutil.copytree(src,dest/label,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for p in sorted((dest/label).rglob('*')):
  if p.is_file():
   original=src/p.relative_to(dest/label);assert p.read_bytes()==original.read_bytes()
   copied.append({'path':str(p.relative_to(dest)),'source':str(original.relative_to(R)),'sha256':sha(p)})
shutil.copyfile(S/'stationary-regularity-and-raw-classicality_README.txt',dest/'README.txt')
rows=[{'path':str(p.relative_to(dest)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(dest.rglob('*')) if p.is_file()]
save(dest/'MANIFEST.json',{'checkpoint':'09','scope':'Integrity only; no external/formal validation.','copied_frozen_files':copied,'all_packet_files':rows})
ledger=json.loads((R/'work/checkpoints/checkpoint08/CLAIM_LEDGER.json').read_text());addition=json.loads((S/'cycle09_claim_additions.json').read_text());old={c['id'] for c in ledger['claims']}
assert len({c['id'] for c in addition['claims']})==len(addition['claims']);assert not old.intersection(c['id'] for c in addition['claims'])
ledger['claims'].extend(addition['claims'])
ledger.update(checkpoint='09',objective_achieved=False,historical_novelty='UNKNOWN',external_validation=False,formal_kernel_replay=False,current_lead='Sharp complete positive regularity profiles for all finite faithful stationary QMS and raw common-margin bounded-information classicality; internally proved and independently audited.',historical_entries_note='Earlier statuses remain historical. Cycle09 closure supersedes only the all-p/non-KMS and raw fixed-margin gates it actually resolves; varying margins, observational radius and mixed Petz trace remain open.')
save(S/'CLAIM_LEDGER.json',ledger);save(O/'CLAIM_LEDGER.json',ledger)
print(json.dumps({'new_packet':dest.name,'copied_files':len(copied),'claims':len(ledger['claims']),'objective_achieved':False},indent=2))
