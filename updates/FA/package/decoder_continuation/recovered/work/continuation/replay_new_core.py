"""Bounded new-construction replay from an extracted continuation package.

Python standard library only. Passed checks establish their recorded scopes;
they do not establish novelty, physical validity, or mission completion.
Run in a fresh extraction because audit scripts write receipts next to code.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
LOGS = BASE/'new_core_replay'
CHECKS = [
    ('comparison_tournament_quick', BASE/'root_ordinal/triangular_compact.py',
     ['--quick', '--output', str(LOGS/'tournament_quick.json')]),
    ('independent_quadratic_tournament', BASE/'luna08_ordinal_challenge/optimized_tournament_audit.py', []),
    ('independent_degree3_4', BASE/'luna08_ordinal_challenge/degree3_4_audit.py', []),
    ('independent_compact_degree3_4', BASE/'luna08_ordinal_challenge/compact_tournament_audit.py', []),
    ('euclidean_selector_counterexample', BASE/'luna01_prefix_geometry/verify_euclidean_selector_counterexamples.py', []),
    ('joint_quadratic_fibers', BASE/'luna02_joint_quadratics/exhaustive_check.py', []),
]


def main():
    LOGS.mkdir(exist_ok=True)
    checks = []
    for name, script, arguments in CHECKS:
        start = time.perf_counter()
        p = subprocess.run([sys.executable, str(script), *arguments], cwd=ROOT,
                           capture_output=True, text=True, timeout=90)
        log = p.stdout+'\nSTDERR\n'+p.stderr
        (LOGS/(name+'.log')).write_text(log)
        record = {'name': name, 'exit_code': p.returncode,
                  'seconds': time.perf_counter()-start,
                  'passed': p.returncode == 0,
                  'log_sha256': hashlib.sha256(log.encode()).hexdigest()}
        if record['passed'] and name == 'comparison_tournament_quick':
            cases = json.loads((LOGS/'tournament_quick.json').read_text())['cases']
            record['passed'] = len(cases) == 2 and all(
                c.get('all_raw_coordinate_polynomials_exact') and
                c.get('source_queries_during_compiled_execution') == 0 for c in cases)
        checks.append(record)
        print(json.dumps(record), flush=True)
    out = {'checks': checks, 'all_passed': all(c['passed'] for c in checks),
           'scope': 'Six new bounded exact/algebraic implementation groups; main compact learner replay only n8 and n12. No n64 rerun, physical model validation, priority clearance or mission completion.'}
    (LOGS/'RECEIPT.json').write_text(json.dumps(out, indent=2)+'\n')
    if not out['all_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
