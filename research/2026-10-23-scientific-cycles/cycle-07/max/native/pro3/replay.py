#!/usr/bin/env python3
"""Verify this source and replay only the new exact Cycle6 diagnostics."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'MANIFEST.json').read_text())
    for entry in manifest['files']:
        data = (root/entry['path']).read_bytes()
        assert len(data) == entry['bytes'], entry['path']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='astra_cycle6_replay_') as tmp:
        output_dir = Path(tmp)/'checks'
        run = subprocess.run([sys.executable, str(root/'code/weighted_boundary_checks.py'),
                              '--output-dir', str(output_dir)], cwd=tmp,
                             capture_output=True, text=True, check=True)
        deterministic = {}
        for name in ['EXACT_INPUTS.json', 'WEIGHTED_CHECKS.json']:
            got, wanted = (output_dir/name).read_bytes(), (root/'evidence'/name).read_bytes()
            assert got == wanted, name
            deterministic[name] = {'bytes': len(got), 'sha256': hashlib.sha256(got).hexdigest()}
        resources = json.loads((output_dir/'CHECK_RESOURCES.json').read_text())
        receipt = {'status': 'PASS', 'manifest_payloads_verified': len(manifest['files']),
                   'deterministic_exact_matches': deterministic, 'diagnostic_resources': resources,
                   'total_replay_wall_seconds': time.perf_counter()-start,
                   'diagnostic_stdout': json.loads(run.stdout),
                   'scope': 'new diagnostic and source hashes only; no historical science replay',
                   'discovery_inference_tokens_money': 'unknown'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, sort_keys=True, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
