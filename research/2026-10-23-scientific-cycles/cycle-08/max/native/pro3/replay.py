#!/usr/bin/env python3
"""Verify a source checkpoint and replay only its two new bounded checks."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
import traceback


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError('Assertions must remain enabled; do not run with -O.')
    root = Path(__file__).resolve().parent
    output = args.output.expanduser().resolve()
    if root == output or root in output.parents:
        raise RuntimeError('Place the replay receipt outside the frozen source directory.')
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    wall = time.perf_counter()
    record = {'started_utc': started, 'python': sys.version,
              'platform': platform.platform(), 'source_root': str(root),
              'scope': 'manifest plus two bounded Cycle7 diagnostics; no predecessor replay',
              'discovery_inference_token_monetary_cost': 'unknown', 'runs': []}
    try:
        manifest = json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
        names = set()
        for entry in manifest['files']:
            rel = Path(entry['path'])
            if rel.is_absolute() or '..' in rel.parts or entry['path'] in names:
                raise RuntimeError('Unsafe or repeated manifest path: '+entry['path'])
            names.add(entry['path'])
            data = (root/rel).read_bytes()
            if len(data) != entry['bytes'] or digest(data) != entry['sha256']:
                raise RuntimeError('Manifest mismatch: '+entry['path'])
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts
                  and p.name != 'MANIFEST.json'}
        if actual != names:
            raise RuntimeError('Unmanifested or missing files: '+repr(actual ^ names))
        record['manifest'] = {'status': 'PASS', 'files': len(names),
                              'sha256': digest((root/'MANIFEST.json').read_bytes())}
        env = dict(os.environ)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        env.pop('PYTHONOPTIMIZE', None)
        jobs = [('reciprocal_checks.py', ['EXACT_INPUTS.json', 'RECIPROCAL_CHECKS.json']),
                ('fanout_checks.py', ['FANOUT_INPUTS.json', 'FANOUT_CHECKS.json'])]
        with tempfile.TemporaryDirectory(prefix='astra-pro3-cycle7-replay-') as temp:
            for i, (script, files) in enumerate(jobs):
                dest = Path(temp)/str(i)
                command = [sys.executable, str(root/'code'/script), '--output-dir', str(dest)]
                t0 = time.perf_counter()
                proc = subprocess.run(command, capture_output=True, text=True, env=env,
                                      timeout=60, check=False)
                run = {'script': script, 'returncode': proc.returncode,
                       'process_wall_seconds': time.perf_counter()-t0,
                       'stdout': proc.stdout, 'stderr': proc.stderr, 'comparisons': []}
                record['runs'].append(run)
                if proc.returncode:
                    raise RuntimeError('Diagnostic failed: '+script)
                for name in files:
                    current = (dest/name).read_bytes()
                    expected = (root/'evidence'/name).read_bytes()
                    identical = current == expected
                    run['comparisons'].append({'file': name, 'byte_identical': identical,
                                               'bytes': len(current), 'sha256': digest(current)})
                    if not identical:
                        raise RuntimeError('Deterministic output mismatch: '+name)
        record['status'] = 'PASS'
    except Exception:
        record['status'] = 'FAIL'
        record['traceback'] = traceback.format_exc()
    record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    record['wall_seconds'] = time.perf_counter()-wall
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({'status': record['status'], 'receipt': str(output),
                      'manifest': record.get('manifest'),
                      'wall_seconds': record['wall_seconds']}, indent=2))
    if record['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
