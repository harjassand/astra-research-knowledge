#!/usr/bin/env python3
"""Verify this complete source and replay only the NEW Cycle8 finite checks."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    assert __debug__, 'Run without -O'
    root = Path(__file__).resolve().parent
    out = (args.output_dir or Path(tempfile.mkdtemp(prefix='pro3_cycle8_replay_'))).resolve()
    assert out != root and root not in out.parents, 'Keep replay output outside frozen source'
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((root/'MANIFEST.json').read_text())
    expected = {entry['path']: entry for entry in manifest['files']}
    actual = {str(p.relative_to(root)) for p in root.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts
              and p.name != 'MANIFEST.json' and p.suffix != '.pyc'}
    assert set(expected) == actual, {'missing': sorted(set(expected)-actual),
                                     'extra': sorted(actual-set(expected))}
    for name, info in expected.items():
        path = root/name
        assert path.stat().st_size == info['bytes'] and sha(path) == info['sha256'], name
    proof_hash = sha(root/'ASYMMETRY_BUDGET_THEOREM.md')
    review = json.loads((root/'reviews/CRITERION_REVIEW.receipt.json').read_text())
    assert review['principal_sha256'] == proof_hash
    assert proof_hash == 'eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1'
    predecessor = root/'sources/Astra_Amplification_Cycle7_PRO3_20261022.zip'
    assert predecessor.stat().st_size == 2410386
    assert sha(predecessor) == 'fede9a15e5d94efee2152b3527e05d78ce92d2a92c1160ed8a253346df42fdc9'
    freeze = json.loads((root/'evidence/PREEXECUTION_FREEZE.json').read_text())
    assert all(sha(root/z['path']) == z['sha256'] for z in freeze['files'])
    wall = time.perf_counter()
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    proc = subprocess.run([sys.executable, '-B', str(root/'code/exact_checks.py'),
                           '--output-dir', str(out/'exact')],
                          capture_output=True, text=True, env=env, check=False)
    (out/'EXACT_STDOUT.txt').write_text(proc.stdout)
    (out/'EXACT_STDERR.txt').write_text(proc.stderr)
    assert proc.returncode == 0, proc.stderr
    checks = {}
    for name in ('EXACT_INPUTS.json', 'EXACT_RESULTS.json'):
        original, replayed = root/'evidence/exact'/name, out/'exact'/name
        assert original.read_bytes() == replayed.read_bytes(), name
        checks[name] = {'bytes': original.stat().st_size, 'sha256': sha(replayed),
                        'byte_identical': True}
    receipt = {
        'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(),
        'source_root': str(root), 'manifest_files_verified': len(expected),
        'principal_sha256': proof_hash, 'review_bound_to_source': True,
        'predecessor_unchanged': True, 'preexecution_freeze_unchanged': True,
        'new_diagnostic_replay_wall_seconds': time.perf_counter()-wall,
        'deterministic_checks': checks, 'subprocess_exit_code': proc.returncode,
        'prior_scientific_suites_rerun': 0,
        'scope': 'Byte integrity and exact finite replay; not discovery cost or asymptotic proof',
        'discovery_inference_token_monetary_cost': 'unknown'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

