#!/usr/bin/env python3
"""Explicit FZ authored selection. No original scientific file is edited.

Selections preserve final proofs, exact witnesses, scripts and failure receipts.
External papers, model datasets, workbooks, source clones and caches stay out.
This script prepares a hash-bound allowlist; copying requires its exact digest.
"""
from pathlib import Path
import hashlib
import json
import sys

R = Path(__file__).resolve().parents[1]
I = 'updates/FZ-positive-memory-genesis-20261016/'
BASE = '3dde9ce74d829a93388e64032d27351b36dd2221'
flags = ['contains_external_fulltext','contains_external_dataset',
         'contains_external_workbook','contains_external_clone','contains_runtime_cache']
workers = [
 'fz_input_identity_luna','fz_positive_calibration_audit',
 'fz_positive_conformal_genesis','fz_positive_representation_genesis',
 'fz_memory_quantum_audit','fz_memory_probability_audit',
 'fz_memory_structured_noise_genesis','fz_memory_priority_physical_audit',
 'fz_memory_bath_theorem_audit','fz_proposal_budget_audit',
 'fz_signed_gram_audit','fz_shear_elimination_audit',
 'fz_reciprocal_moment_genesis','fz_reciprocal_counterexample_audit',
 'fz_kinetic_path_genesis','fz_kinetic_obstruction_audit',
 'fz_kinetic_cap_certificate_audit','fz_catalysis_causal_genesis',
 'fz_current_capital_audit']
audit_dirs = {x for x in workers if 'audit' in x or 'identity' in x}
entries = []

def add(origin, name, role, kind, source_origin, reason):
    raw = origin.read_bytes()
    raw.decode('utf-8')
    destination = I+'package/derived/'+name
    if Path(destination).suffix not in {'.md','.txt','.json','.jsonl','.py','.tex','.sh','.csv','.tsv'}:
        destination += '.txt'  # Preserve failed-attempt log bytes, with original name recorded.
    entries.append(dict(path=destination, research_relative_path=name,
        origin_path=str(origin.resolve()), sha256=hashlib.sha256(raw).hexdigest(),
        bytes=len(raw), provenance_role=role, payload_kind=kind,
        source_origin=source_origin, selection_reason=reason,
        provenance_note='Exact selected bytes; original producers, audit inputs and external acquisition pointers retain their explicitly recorded provenance. No external correctness or physical status promotion.',
        **{k:False for k in flags}))

for name in workers:
    folder=R/'workers'/name
    assert folder.is_dir(), name
    for p in sorted(folder.iterdir()):
        if not p.is_file() or p.name=='oustry_pinned_README.txt':
            continue
        if p.suffix in {'.html','.pdf','.m'} or p.name.startswith('.'):
            continue
        assert p.suffix in {'.md','.txt','.json','.py','.tsv','.attempt1','.attempt2','.attempt3'}, p
        kind = 'code' if p.suffix=='.py' else 'receipt' if p.suffix in {'.json','.tsv'} or '.attempt' in p.name else 'review' if name in audit_dirs else 'proof'
        role = 'root_or_worker_executable_check' if kind=='code' else 'same_team_review' if name in audit_dirs else 'worker_derivation'
        add(p,str(p.relative_to(R)),role,kind,'worker_authored',
            'Final construction/audit, exact finite evidence, acquisition/source pin, or preserved failed-attempt trace for the named scoped scientific result.')

# Only these three small audit snapshot subtrees are needed by exact replay.
for name, children in {
 'fz_reciprocal_counterexample_audit':['frozen_inputs','earlier_audit'],
 'fz_kinetic_cap_certificate_audit':['inputs','candidate_frozen'],
 'fz_signed_gram_audit':['frozen_inputs'],
}.items():
    for child in children:
        for p in sorted((R/'workers'/name/child).rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts: continue
            if p.suffix in {'.html','.pdf'}: continue  # Acquired primary fulltext, never authored evidence.
            assert p.suffix in {'.md','.txt','.json','.py'}, p
            add(p,str(p.relative_to(R)),'same_team_review',
                'code' if p.suffix=='.py' else 'receipt' if p.suffix=='.json' else 'review',
                'worker_authored','Exact frozen audit input or earlier transcribed witness. This snapshot does not relabel the underlying source as new research; its input manifest records original identity.')

# The external acquisition worker supplies an explicit sanitized publication list.
folder=R/'workers/fz_catalysis_evidence_acquisition'
manifest=json.loads((folder/'PUBLICATION_MANIFEST.json').read_text())
for item in manifest['allowlist']:
    p=folder/item['path']; raw=p.read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    kind='code' if p.suffix=='.py' else 'receipt' if p.suffix=='.json' else 'review'
    role='root_or_worker_executable_check' if kind=='code' else 'acquired_primary_literature_receipt' if item['path'].startswith('receipts/') else 'worker_derivation'
    add(p,str(p.relative_to(R)),role,kind,
        'acquisition_pointer' if role=='acquired_primary_literature_receipt' else 'worker_authored',
        'Explicit primary-source worker publication allowlist; external binary originals, extracts and transport metadata excluded.')
add(folder/'PUBLICATION_MANIFEST.json',str((folder/'PUBLICATION_MANIFEST.json').relative_to(R)),
    'same_team_review','receipt','worker_authored','Preserve the exact sanitized publication boundary and exclusions.')

# Separately located existing quantum capital is NOT part of the 47 originals.
located=json.loads((R/'workers/fz_memory_quantum_audit/LOCATED_CAPITAL_ALLOWLIST.json').read_text())
for item in located['files']:
    p=Path(item['absolute_origin']);raw=p.read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    add(p,item['planned_relative_destination'],'capital_comparison',
        'receipt' if p.suffix=='.json' else 'proof','located_prior_capital',
        item['load_bearing_or_scope_reason'])

for name in ['STRUCTURED_HAMILTONIAN_RATE_THEOREM.v0001.md',
             'STRUCTURED_HAMILTONIAN_RATE_THEOREM.v0002.md',
             'STRUCTURED_HAMILTONIAN_RATE_THEOREM.v0003.md',
             'SCIENTIFIC_SYNTHESIS.v0001.md','ADJUDICATION_ADDENDUM.v0002.md',
             'FINAL_SCOPE_NOTES.v0001.md','RESEARCH_INVESTMENTS.v0001.json',
             'SELECTION_ATTEMPT_HISTORY.v0001.json',
             'select_public_evidence.py']:
    p=R/'root'/name
    add(p,'root/'+name,'root_synthesis','code' if p.suffix=='.py' else 'receipt' if p.suffix=='.json' else 'synthesis',
        'root_authored','Root scientific derivation, final adjudication, deployment scope or reproducible explicit evidence-selection code.')

assert len({x['path'] for x in entries})==len(entries)
payload={'schema':'astra.fz-selected-freeze.v1','intake_id':'FZ-positive-memory-genesis-20261016',
 'status':'FROZEN_ROOT_SELECTED','selected_by':'root','base_revision':BASE,
 'research_root':str(R),'original_manifest_sha256':'1dacbc13c8887912b8e21f3c06fb35cab81c735e22b1e0c8182d42b59550fec6',
 'files':entries,'total_files':len(entries),'total_bytes':sum(x['bytes']for x in entries),
 'authored_publication_exclusions':['externally acquired fulltexts','externally acquired datasets','externally acquired workbooks','external repository clones','runtime and acquisition caches'],
 'scope':'Exact root-selected authored evidence, separately located prior quantum capital, internal checks and sanitized acquisition pointers. No external validation or technological promotion; supplied originals have their own immutable inventory.'}
out=R/'root/SELECTED_FREEZE.v0001.json'
raw=(json.dumps(payload,indent=2,ensure_ascii=False)+'\n').encode()
if out.exists(): assert out.read_bytes()==raw,'Do not overwrite a frozen selection; append a new version.'
else: out.write_bytes(raw)
print(json.dumps({'files':len(entries),'bytes':payload['total_bytes'],'sha256':hashlib.sha256(raw).hexdigest()}))
