"""Replay only the new finite native check, without modifying saved evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    script = root / 'meta/native_check.py'
    reference = json.loads((root / 'meta/NATIVE_CHECK.json').read_text())
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='astra-cycle8-native-') as temporary:
        result_path = Path(temporary) / 'new_native_result.json'
        result = subprocess.run(
            [sys.executable, str(script), '--output', str(result_path)],
            cwd=temporary, text=True, capture_output=True, timeout=30, check=True)
        current = json.loads(result_path.read_text())
    assert current['status'] == 'PASS'
    assert current['records'] == reference['records']
    assert current['source_sha256'] == reference['source_sha256']
    report = {
        'status': 'PASS', 'exact_native_cases': len(current['records']),
        'scientific_records_match_saved': True,
        'source_sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
        'python': platform.python_version(), 'platform': platform.platform(),
        'new_process_elapsed_seconds': time.perf_counter() - start,
        'new_script_measurement': {
            key: current[key] for key in
            ('wall_seconds', 'cpu_seconds', 'peak_rss_native_units')},
        'scope': 'New root finite check only; no owner suite executed. '
                 'Finite corroboration does not prove all k or discovery advantage.',
        'child_stdout': result.stdout.strip(),
    }
    path = Path(args.output).expanduser().resolve()
    assert path != root / 'meta/NATIVE_CHECK.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in
                      ('status', 'exact_native_cases', 'scientific_records_match_saved',
                       'new_process_elapsed_seconds')}, indent=2))


if __name__ == '__main__':
    main()
