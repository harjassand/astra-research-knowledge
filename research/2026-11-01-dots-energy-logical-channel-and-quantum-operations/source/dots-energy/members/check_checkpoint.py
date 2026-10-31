#!/usr/bin/env python3
"""Read-only focused reproduction, not an independent mathematical review."""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def main():
    os.chdir(ROOT)
    report = {'scope': 'Focused local checkpoint reproduction; not a new independent scientific review.'}
    report['environment'] = {'python': sys.version.split()[0]}
    for name in ('numpy', 'scipy', 'mpmath', 'sympy'):
        report['environment'][name] = importlib.metadata.version(name)
    science = json.loads((ROOT/'ALLOWLIST.json').read_text())['files']
    n_py = n_json = 0
    for item in science:
        path = ROOT/item['path']
        if path.suffix == '.py':
            compile(path.read_bytes(), item['path'], 'exec')
            n_py += 1
        elif path.suffix == '.json':
            json.loads(path.read_text())
            n_json += 1
    report['parsed_scientific_sources'] = {'python': n_py, 'json': n_json}
    report['exact_ledger_rows'] = {}
    for folder, module in (
        ('native_resource_audit_20261031', 'resource_ledger'),
        ('native_first_event_optimization_20261031', 'sharp_ledger'),
        ('native_first_event_optimization_20261031', 'last_refresh_operation_ledger'),
    ):
        sys.path.insert(0, str(ROOT/folder))
        mod = importlib.import_module(module)
        old = json.loads((ROOT/folder/(module+'.json')).read_text())['rows']
        for row in old:
            # The original displayed fixture is stored as exact integer strings.
            epsden = int(row['epsilon'].split('/')[1])
            new = mod.case(row['n'], epsden, int(row['lambda_value']))
            assert new == row, (module, row['n'], row['epsilon'], row['lambda_value'])
        report['exact_ledger_rows'][module] = len(old)
    sys.path.insert(0, str(ROOT/'native_first_event_optimization_20261031'))
    bridge = importlib.import_module('check_last_refresh_bridge').check()
    report['bridge_diagnostics'] = {k: len(bridge[k]) for k in ('bridge_cases', 'event_race_cases')}
    sys.path.insert(0, str(ROOT/'reusable_identity_discovery_20261031'))
    matrix = importlib.import_module('compile_and_test')
    scheme = json.loads((ROOT/'reusable_identity_discovery_20261031/acquired_scheme.json').read_text())['scheme']
    circuit = matrix.compile_scheme(scheme)
    report['matrix_exact_tests'] = matrix.test(circuit, scheme)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    run = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_construction'],
                         cwd=ROOT/'hidden_parity_acquisition_20261031', env=env,
                         text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.stderr.write(run.stdout + run.stderr)
    assert run.returncode == 0, 'parity unit tests failed'
    assert 'Ran 10 tests' in run.stderr, 'unexpected parity test count'
    report['parity_unit_tests'] = {'count': 10, 'passed': True}
    report['all_requested_checks_passed'] = True
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
