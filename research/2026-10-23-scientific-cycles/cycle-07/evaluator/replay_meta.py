#!/usr/bin/env python3
"""Bounded offline replay in a temporary copy; no original owner science runs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
VOLATILE = {'elapsed_seconds', 'wall_seconds', 'peak_rss_native',
            'rss_platform', 'peak_rss_kib_linux'}

def scientific(obj):
    if isinstance(obj, dict):
        return {k: scientific(v) for k, v in obj.items() if k not in VOLATILE}
    if isinstance(obj, list):
        return [scientific(x) for x in obj]
    return obj

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    jobs = [
        ('primary_table_transcription', 'taste_signal/extract_candidate_table.py', 'taste_signal/CANDIDATE_TABLES.json'),
        ('shared_factor', 'taste_signal/exact_shared_factor_test.py', 'taste_signal/EXACT_SHARED_FACTOR_RESULT.json'),
        ('proof_label_and_strong_control', 'taste_adversarial/exact_tests.py', 'taste_adversarial/EXACT_RESULTS.json'),
        ('native_queue_rational_enclosure', 'constructive_meta/verify_nuisance_family.py', 'constructive_meta/RESULT.json'),
        ('root_independent_exact', 'root_checks/independent_meta_check.py', 'root_checks/ROOT_EXACT_CHECK.json'),
        ('root_independent_decimal', 'root_checks/queue_arithmetic_crosscheck.py', 'root_checks/ROOT_QUEUE_ARITHMETIC.json'),
    ]
    start = time.perf_counter()
    records = []
    with tempfile.TemporaryDirectory(prefix='astra_cycle7_replay_') as directory:
        temp = Path(directory) / 'meta'
        shutil.copytree(ROOT / 'meta', temp)
        for label, script, output in jobs:
            t = time.perf_counter()
            child = subprocess.run([sys.executable, str(temp / script)],
                                   cwd=directory, capture_output=True, text=True,
                                   timeout=60, check=False)
            if child.returncode:
                raise RuntimeError(f'{label} failed: {child.stderr[-4000:]}')
            observed = json.loads((temp / output).read_text())
            expected = json.loads((ROOT / 'meta' / output).read_text())
            if scientific(observed) != scientific(expected):
                raise AssertionError(f'{label}: scientific output differs')
            records.append({'test': label, 'status': 'PASS',
                            'wall_seconds_including_launch': time.perf_counter() - t,
                            'stdout_sha256': hashlib.sha256(child.stdout.encode()).hexdigest(),
                            'scientific_output_matches': True})
    result = {'status': 'PASS', 'tests': records,
              'total_replay_wall_seconds': time.perf_counter() - start,
              'python': sys.version.split()[0],
              'scope': 'Replays bounded meta calculations and primary table extraction only. No proof-of-novelty, independent model experiment, owner simulation, full science revalidation or recursive amplification claim.',
              'unknown_costs': ['scientific design', 'all model inference', 'source reading', 'proof review', 'integration']}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
