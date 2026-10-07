"""Replay four small CLI fixtures after extracting the portable archive.

This packaging check does not repeat the N32/N64 scientific probes.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile


def rational(record):
    return Fraction(int(record['numerator']), int(record['denominator']))


def check_density(density):
    a, b = map(rational, density['diagonal'])
    real = rational(density['upper_right_real'])
    imag = rational(density['upper_right_imag'])
    if not (a >= 0 and b >= 0 and a+b == 1 and real*real+imag*imag <= a*b):
        raise ArithmeticError('portable output is not an exact PSD trace-one matrix')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, type=Path)
    parser.add_argument('--extract-root', required=True, type=Path)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    root = args.extract_root.resolve()
    root.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(args.archive) as archive:
        for name in archive.namelist():
            if not (root / name).resolve().is_relative_to(root):
                raise ValueError('archive member escapes the extraction directory')
        archive.extractall(root)
    impl = root / 'work/cycle6/c03_s01/implementation'
    expected = json.loads((impl / 'RESULTS.json').read_text())['source_sha256']
    for name, value in expected.items():
        if hashlib.sha256((impl / name).read_bytes()).hexdigest() != value:
            raise ArithmeticError('portable source hash mismatch: '+name)
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    cases = [
        ('dicke_compiler', 2, 'verify_model', ['--samples', '1']),
        ('whole_gibbs_compiler', 3, 'verify_whole_model', ['--alpha', '3', '--samples', '1']),
        ('filtered_sector_compiler', 2, 'verify_filtered', ['--alpha', '3']),
        ('filtered_sector_scaling', 2, 'verify_filtered', ['--alpha', '3']),
    ]
    records = []
    for module, n, verifier, extra in cases:
        output = root / (module+'_smoke.json')
        command = [sys.executable, '-B', str(impl / (module+'.py')),
                   '--n', str(n), '--delta', '1', '--h', '1/3',
                   '--epsilon', '1e-8', '--output', str(output)] + extra
        began = time.perf_counter()
        completed = subprocess.run(command, cwd=root, env=env, capture_output=True,
                                   text=True, timeout=20)
        if completed.returncode:
            raise RuntimeError(module+' portable CLI failed: '+completed.stderr[-2000:])
        result = json.loads(output.read_text())
        records.append({'module': module, 'n': n, 'verifier': verifier,
                        'output': output.name,
                        'cli_seconds': time.perf_counter()-began,
                        'cli_returncode': completed.returncode,
                        'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                        'samples': len(result['samples'])})
    # Import only the extracted portable hierarchy, after running its CLIs.
    sys.path.insert(0, str(impl))
    sys.dont_write_bytecode = True
    density_checks = 0
    for record in records:
        result = json.loads((root / record['output']).read_text())
        module = importlib.import_module(record['module'])
        if not getattr(module, record['verifier'])(result['model']):
            raise ArithmeticError('portable verifier did not confirm output')
        for sample in result['samples']:
            matrices = sample.get('local_density_matrices')
            if matrices is None:
                matrices = [sample['finite_product_local_density']]
            for matrix in matrices:
                check_density(matrix)
                density_checks += 1
        record['exact_json_roundtrip_verifier'] = 'PASS'
    receipt = {'utc': datetime.now(timezone.utc).isoformat(),
               'status': 'PASS_PORTABLE_SMALL_CLI_REPLAY',
               'scope': 'Four small CLI fixtures; packaging/import/serialization check only. No larger science benchmark rerun.',
               'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
               'source_sha256': expected, 'records': records,
               'exact_local_PSD_trace_one_checks': density_checks,
               'package_installations': 0,
               'hardcoded_host_imports_required': False}
    args.receipt.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'status': receipt['status'], 'CLI_fixtures': len(records),
                      'exact_local_PSD_checks': density_checks}))


if __name__ == '__main__':
    main()
