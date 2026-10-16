#!/usr/bin/env python3
"""Verify supplied payload manifests; hashing labels is integrity only."""
from pathlib import Path
import hashlib, json, subprocess, sys

P = Path(__file__).resolve().parent
D = Path('/Users/harjas/Downloads/Dots')
names = {
    'willow_empirical_evaluator_2026-10-15': 'MANIFEST_SHA256.json',
    'autonomous_correction_decision_2026-10-15': 'SHA256SUMS',
    'matched_memory_benchmark_packet_2026-10-15': 'SHA256SUMS',
    'measured_randomizer_benchmark_2026-10-15': 'MANIFEST_SHA256.json'
}
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

packages = {}
for name, manifest in names.items():
    root = D/name
    mf = root/manifest
    if manifest.endswith('.json'):
        expected = json.loads(mf.read_text())
    else:
        expected = {}
        for line in mf.read_text().splitlines():
            if line.strip():
                h, path = line.split('  ',1)
                expected[path] = h
    files = {}
    for name, expected_sha in expected.items():
        f = root/name
        actual_sha = sha(f)
        assert actual_sha == expected_sha, str(f)
        files[name] = {'bytes': f.stat().st_size, 'sha256': actual_sha}
    packages[root.name] = {'source_root': str(root), 'supplied_manifest': manifest,
                           'supplied_manifest_sha256': sha(mf), 'verified_files': len(files),
                           'payload_bytes': sum(a['bytes'] for a in files.values()),
                           'files': files}

W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
observed_pin = subprocess.run(['git','rev-parse','HEAD'],cwd=W,text=True,capture_output=True,check=True).stdout.strip()
pin = '61389569d6c53b439764f0d148b35b7fa6083eec'
context_names = ['AGENTS.md','00_START_HERE.txt',
    'cards/N881-autonomous-memory-structured-noise-and-bath-interfaces.txt',
    'frontier/dossiers/N881.txt', 'frontier/gates/G-FZ-SIG-N881-CAPABILITY.json',
    'frontier/gates/G-FZ-SIG-N881-REVIEW.json']
context_files = {}
for name in context_names:
    frozen = subprocess.run(['git','show',f'{pin}:{name}'],cwd=W,capture_output=True,check=True).stdout
    context_files[name] = hashlib.sha256(frozen).hexdigest()
actual = json.loads((P/'autonomous_aggregate_evaluation.json').read_text())
expected = json.loads((D/'autonomous_correction_decision_2026-10-15/autonomous_correction_evaluator/evaluation.json').read_text())
assert actual == expected
result = {'status': 'PASS', 'source_class': 'Supplied packet bytes, independently rehashed against supplied manifests. Not independently authenticated device data.',
          'main_worktree_pin': pin, 'main_context_hashes': context_files,
          'later_observed_worktree_HEAD': observed_pin,
          'revision_note': 'Shared worktree advanced during investigation. Context hashes explicitly use initial 61389569 revision via git show, not the later HEAD.',
          'packages': packages, 'autonomous_aggregate_saved_JSON_exact_match': True,
          'hashing_reserved_labels_is_not_outcome_analysis': True,
          'python': sys.version}
(P/'source_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','packages':{n:a['verified_files'] for n,a in packages.items()},
                  'autonomous_aggregate_exact_match':True,'main_pin':pin},indent=2))
