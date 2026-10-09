#!/usr/bin/env python3
"""Portable exact diagnostics. No sources, network or third-party packages needed."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional receipt path')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    scripts = ['verify_core.py',
               'work/reports/sol1_signed/exact_falsifiers.py',
               'work/reports/sol2_alternative/dilation_certificate.py']
    results = []
    with tempfile.TemporaryDirectory(prefix='astra-exact-') as scratch:
        for rel in scripts:
            source = root / rel
            dest = Path(scratch) / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            start = time.perf_counter()
            run = subprocess.run([sys.executable, '-I', str(dest)], cwd=scratch,
                                 text=True, capture_output=True, timeout=120)
            results.append({'script': rel, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                            'exit_code': run.returncode, 'elapsed_seconds': time.perf_counter()-start,
                            'stdout': run.stdout, 'stderr': run.stderr})
    receipt = {'status': 'PASS' if all(r['exit_code'] == 0 for r in results) else 'FAIL',
               'python': platform.python_version(), 'platform': platform.platform(),
               'network_required': False, 'third_party_packages_required': False,
               'proof_scope': 'Exact counterexamples and finite diagnostics; not universal amplifier proof certification',
               'results': results}
    text = json.dumps(receipt, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    return int(receipt['status'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
