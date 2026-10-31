#!/usr/bin/env python3
"""Reproduce checks without rewriting the archived scientific artifacts."""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent
SCIENCE = ROOT/'effective_logical_channel_20261031'


def main():
    report = {'scope': 'Local reproduction only; existing independent receipts retain their separate scopes.'}
    report['environment'] = {'python': sys.version.split()[0]}
    for name in ('numpy', 'scipy', 'mpmath', 'sympy'):
        report['environment'][name] = importlib.metadata.version(name)
    py_count = json_count = 0
    for item in json.loads((ROOT/'ALLOWLIST.json').read_text())['files']:
        p = ROOT/item['path']
        if p.suffix == '.py':
            compile(p.read_bytes(), item['path'], 'exec')
            py_count += 1
        elif p.suffix == '.json':
            json.loads(p.read_text())
            json_count += 1
    report['parsed_scientific_sources'] = {'python': py_count, 'json': json_count}
    sys.path.insert(0, str(SCIENCE))
    acquisition = importlib.import_module('acquire_effective_qubit')
    author = importlib.import_module('test_effective_qubit').run()
    independent = importlib.import_module('independent_effective_qubit_audit').run()
    assert author['checks'] == 83 and independent['checks'] == 93
    report['author_assertions'] = author['checks']
    report['independent_assertions_rerun'] = independent['checks']
    report['certificate_verification'] = []
    for name, current in [('effective_qubit_certificate.json', True),
                          ('effective_billion_spin_certificate.json', True),
                          ('effective_qubit_certificate_1e4.json', False)]:
        obj = json.loads((SCIENCE/name).read_text())
        cp = acquisition.verify_channel(obj)
        whole = acquisition.verify_record(obj)
        assert cp is True and whole is current, name
        report['certificate_verification'].append({'file': name, 'CP_TP': cp,
                                                   'current_full_record': whole,
                                                   'expected_current': current})
    scripts = ['check_acquired_cp_channel.py', 'check_complete_cq_channel.py',
               'check_local_covariance_truncation.py', 'check_native_quantum_restriction.py']
    report['diagnostic_reruns'] = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='logical-channel-check-') as tmp:
        copy = Path(tmp)/'effective_logical_channel_20261031'
        shutil.copytree(SCIENCE, copy)
        for script in scripts:
            run = subprocess.run([sys.executable, '-B', str(copy/script)],
                                 cwd=tmp, env=env, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert run.returncode == 0, (script, run.stdout, run.stderr)
            output = json.loads((copy/Path(script).with_suffix('.json')).read_text())
            original = json.loads((SCIENCE/Path(script).with_suffix('.json')).read_text())
            row_count = len(output.get('rows', output.get('cases', [])))
            item = {'script': script, 'passed': True, 'output_rows': row_count,
                    'bitwise_structured_match_to_saved_diagnostic': output == original,
                    'floating_scope': 'Floating comparisons are diagnostics, not independently certified numerical bounds.'}
            if script == 'check_acquired_cp_channel.py':
                assert len(output['rows']) == 3
                assert all(r['exact_CP_TP_Kraus_checks'] for r in output['rows'])
                item['exact_Kraus_CP_TP_rows'] = 3
            report['diagnostic_reruns'].append(item)
    report['all_requested_checks_passed'] = True
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
