"""Run the unchanged finite scripts in disposable copies, preserving inputs."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPLAY = ROOT / 'replay'
REPLAY.mkdir(exist_ok=True)
RECEIPTS = []
for label, script in (
    ('compatibility', 'verify_compatibility.py'),
    ('calibration', 'verify_calibration.py'),
    ('sharp', 'verify_frontier.py'),
):
    work = ROOT / 'scratch' / 'runs' / label
    command = [sys.executable, '-B', script]
    started = time.monotonic()
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run(command, cwd=work, env=env, capture_output=True,
                            text=True, timeout=300)
    (REPLAY / (label + '.stdout.log')).write_text(result.stdout)
    (REPLAY / (label + '.stderr.log')).write_text(result.stderr)
    output = work / 'VERIFICATION_RECEIPT.json'
    data = json.loads(output.read_text()) if result.returncode == 0 else None
    if data is not None:
        (REPLAY / (label + '.receipt.json')).write_bytes(output.read_bytes())
    record = {
        'label': label,
        'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'cwd': str(work),
        'command': command,
        'python_optimization_disabled': True,
        'script_sha256': hashlib.sha256((work / script).read_bytes()).hexdigest(),
        'returncode': result.returncode,
        'elapsed_seconds': time.monotonic() - started,
        'stdout_sha256': hashlib.sha256(result.stdout.encode()).hexdigest(),
        'stderr_sha256': hashlib.sha256(result.stderr.encode()).hexdigest(),
        'number_of_reported_groups': None,
    }
    # Explicitly handle the calibration receipt's group-name list.
    if data is not None:
        if isinstance(data.get('groups'), int):
            record['number_of_reported_groups'] = data['groups']
        elif data.get('number_of_groups') is not None:
            record['number_of_reported_groups'] = data['number_of_groups']
        else:
            record['number_of_reported_groups'] = len(data.get('checks', []))
    RECEIPTS.append(record)
    (ROOT / 'REPLAY_CHECKS.json').write_text(json.dumps(RECEIPTS, indent=2) + '\n')
    print(label, 'returncode', result.returncode,
          'groups', record['number_of_reported_groups'],
          'seconds', round(record['elapsed_seconds'], 3), flush=True)
    if result.returncode != 0:
        print(result.stdout, result.stderr, flush=True)
        raise RuntimeError('Replay failed: ' + label)
