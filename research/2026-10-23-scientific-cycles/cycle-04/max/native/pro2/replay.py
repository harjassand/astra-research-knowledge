#!/usr/bin/env python3
"""One receiving use of frozen Cycle3 sources; no producer or old replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical_result(obj):
    """Remove only measured costs, preserving every substantive result."""
    ignored = {'case_wall_seconds', 'body_wall_seconds', 'body_cpu_seconds',
               'wall_seconds', 'cpu_seconds', 'max_rss_bytes', 'peak_rss_bytes'}
    if isinstance(obj, dict):
        return {k: canonical_result(v) for k, v in obj.items() if k not in ignored}
    if isinstance(obj, list):
        return [canonical_result(v) for v in obj]
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise FileExistsError('Refusing to overwrite receiving output: ' + str(out))
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Receiving output must be outside the immutable capsule')
    wall, cpu = time.perf_counter(), time.process_time()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    out.mkdir(parents=True)

    manifest_path = ROOT / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    for item in manifest['files']:
        relative = Path(item['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('unsafe payload path')
        path = ROOT / relative
        if path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
            raise ValueError('payload identity failed: ' + str(relative))

    commands = [
        ('independent_new_witnesses', 'checks/verify_new_witnesses.py', '--output'),
        ('classical_upper', 'checks/check_classical_upper.py', None),
        ('fan_port_checks', 'checks/check_fan_ports.py', '--output'),
        ('interface_challenge_checks', 'checks/check_interface_challenge.py', '--output'),
    ]
    records = []
    with tempfile.TemporaryDirectory(prefix='astra_pro2_cycle3_receive_') as temp:
        relocated = Path(temp) / 'source'
        shutil.copytree(ROOT, relocated,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'sources'))
        for name, script, flag in commands:
            destination = out / (name + '.json')
            cmd = [sys.executable, str(relocated / script)]
            if flag:
                cmd.append(flag)
            cmd.append(str(destination))
            started = time.perf_counter()
            completed = subprocess.run(cmd, cwd=relocated, capture_output=True,
                                       text=True, env={**os.environ,
                                       'PYTHONDONTWRITEBYTECODE': '1'})
            (out / (name + '.stdout.txt')).write_text(completed.stdout)
            (out / (name + '.stderr.txt')).write_text(completed.stderr)
            if completed.returncode != 0:
                raise RuntimeError('Receiving checker failed: ' + name)
            actual = json.loads(destination.read_text())
            original = json.loads((ROOT / 'results' / (name + '.json')).read_text())
            if canonical_result(actual) != canonical_result(original):
                raise ValueError('Substantive receiving result changed: ' + name)
            records.append({'check': name, 'returncode': completed.returncode,
                            'outer_wall_seconds': time.perf_counter() - started,
                            'substantive_record_matches': True,
                            'receipt_sha256': digest(destination)})

    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    receipt = {
        'schema': 'astra.cycle3_relocated_receiving_replay.v1',
        'status': 'passed',
        'python': sys.version,
        'platform': platform.platform(),
        'checked_manifest_sha256': digest(manifest_path),
        'checked_payload_files': len(manifest['files']),
        'original_witnesses_regenerated': False,
        'old_science_executed': False,
        'relocated': True,
        'checks': records,
        'outer_wall_seconds': time.perf_counter() - wall,
        'parent_cpu_seconds': time.process_time() - cpu,
        'children_cpu_seconds': (after.ru_utime + after.ru_stime
                                 - before.ru_utime - before.ru_stime),
        'parent_peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        'children_peak_rss_bytes': after.ru_maxrss * 1024,
        'scope': ('Payload hash verification including unchanged owned ZIP; '
                  'relocated new-source checks and comparison to frozen records. '
                  'No all-size theorem verification or recipient integration.')
    }
    (out / 'receiving_replay.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
