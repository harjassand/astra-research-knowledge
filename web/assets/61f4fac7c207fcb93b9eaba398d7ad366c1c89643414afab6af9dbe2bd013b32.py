#!/usr/bin/env python3
"""Replay selected finite checks without changing the frozen research record.

Python 3.10+; the exact number-field ledger additionally needs SymPy.
No network access, downloaded code, source checkout, or Lean toolchain is used.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
JOBS = [
    ('ASM graph semantics', 'novelty_and_consequences/check_asm_graph_updates.py',
     'novelty_and_consequences/asm_graph_update_results.json', False),
    ('Logarithm scalar schedule', 'algebraic_log_audit/check_parameter_schedule.py',
     'algebraic_log_audit/parameter_schedule_checks.json', False),
    ('Exact number-field ledger', 'number_theory_bridges/check_algebraic_log_ledger.py',
     'number_theory_bridges/algebraic_log_exact_checks.json', True),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--quick', action='store_true', help='Run only the two standard-library checks.')
    p.add_argument('--output', type=Path, help='Write a replay report to this optional path.')
    args = p.parse_args()
    report = {'scope': 'Finite semantic and scalar diagnostics, not theorem or formal verification',
              'python': sys.version.split()[0], 'jobs': []}
    try:
        report['sympy'] = importlib.metadata.version('sympy')
    except importlib.metadata.PackageNotFoundError:
        report['sympy'] = None
    with tempfile.TemporaryDirectory(prefix='astra-second-record-') as td:
        temp = Path(td)
        for label, code, result, needs_sympy in JOBS:
            if args.quick and needs_sympy:
                continue
            target = temp / code
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / code, target)
            start = time.monotonic()
            ran = subprocess.run([sys.executable, str(target)], cwd=temp,
                                 text=True, capture_output=True)
            result_path = temp / result
            item = {'check': label, 'script': code, 'exit_code': ran.returncode,
                    'seconds': round(time.monotonic() - start, 3)}
            if ran.returncode == 0 and result_path.is_file():
                expected = json.loads((ROOT / result).read_text())
                actual = json.loads(result_path.read_text())
                item['saved_json_matches'] = expected == actual
                item['result_sha256'] = sha(result_path)
            else:
                item['saved_json_matches'] = False
                item['stderr'] = ran.stderr[-4000:]
            report['jobs'].append(item)
    report['all_selected_checks_passed'] = all(
        j['exit_code'] == 0 and j['saved_json_matches'] for j in report['jobs'])
    out = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(out)
    print(out, end='')
    return 0 if report['all_selected_checks_passed'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
