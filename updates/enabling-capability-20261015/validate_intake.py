"""Validate curated intake integrity and scoped root claims, not scientific truth."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'EVIDENCE_MANIFEST_v0002.json').read_text())
assert manifest['worker_count'] == 30
for item in manifest['files']:
    path = ROOT / item['path']
    assert path.is_file(), item['path']
    blob = path.read_bytes()
    assert len(blob) == item['bytes'], item['path']
    assert hashlib.sha256(blob).hexdigest() == item['sha256'], item['path']

research = ROOT / 'evidence/root'
claims = json.loads((research / 'CLAIM_LEDGER.json').read_text())
assert len({c['id'] for c in claims}) == len(claims)
assert claims[0]['status'] == 'NOT_ACHIEVED'
assert claims[0]['decision'] == 'HOLD'
for claim in claims:
    for evidence in claim.get('evidence', []):
        assert (research / evidence).exists(), (claim['id'], evidence)
contributions = json.loads((research / 'CONTRIBUTIONS.json').read_text())
assert len(contributions) == 30
assert sum(c['model'] == 'gpt-6.1-sol' for c in contributions) == 16
assert sum(c['model'] == 'gpt-6-astra' for c in contributions) == 14
assert all(c['reasoning_effort'] == 'max' for c in contributions)
assert (ROOT / 'evidence/workers/premise_challenge/SYNTHESIS_AUDIT.txt').is_file()
assert (ROOT / 'evidence/workers/computation_search/FINAL_AMENDMENT_004.txt').is_file()
assert not (research / 'spectral_deconvolution.py').exists()
print(json.dumps({
    'status': 'PASS',
    'manifest_files': len(manifest['files']),
    'manifest_bytes': sum(f['bytes'] for f in manifest['files']),
    'workers': len(contributions),
    'claim_evidence_links': 'PASS',
    'scope': 'Curated byte integrity, root claim-link existence and worker accounting only',
    'scientific_truth_checked': False,
    'novelty_checked': False,
    'experiments_executed_by_validator': 0
}, indent=2))
