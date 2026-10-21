#!/usr/bin/env python3
"""One N33 receiving application, not a new campaign or a general proof checker."""
import argparse
import ast
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fetch(record, destination):
    with urllib.request.urlopen(record['raw_url'], timeout=30) as stream:
        data = stream.read(record['bytes'] + 1)
    require(len(data) == record['bytes'], 'Unexpected public source size')
    require(hashlib.sha256(data).hexdigest() == record['sha256'], 'Wrong public source identity')
    destination.write_bytes(data)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    start, cpu = time.perf_counter(), time.process_time()
    require(not args.output_dir.exists(), 'Choose a fresh receiving directory')
    args.output_dir.mkdir(parents=True)
    sources = json.loads((HERE / 'SOURCE_MAP.json').read_text())
    original = ROOT / sources['original']['path']
    require(hashlib.sha256(original.read_bytes()).hexdigest() == sources['original']['sha256'], 'Wrong restored N33 original')
    require('SN-N33-source-recovery-and-draft-112' in (ROOT / 'frontier/dossiers/N33.txt').read_text(), 'N33 entry point lacks this handoff')
    report = fetch(sources['draft_112']['files']['REPORT.md'], args.output_dir / 'REPORT.md')
    code = fetch(sources['draft_112']['files']['verify_softmin_capture.py'], args.output_dir / 'verify_softmin_capture.py')
    require(b'5.3' in report, 'Expected source residence bound')
    # Execute only the hash-bound original pure function. Importing the whole
    # checker would repeat its historical default grids, which this task avoids.
    functions = [n for n in ast.parse(code).body if isinstance(n, ast.FunctionDef) and n.name == 'soft']
    require(len(functions) == 1, 'Expected one owner soft function')
    env = {'exp': math.exp, 'log': math.log}
    exec(compile(ast.Module(body=functions, type_ignores=[]), 'owner:soft', 'exec'), env)
    soft = env['soft']
    volume = 2400
    minimum, argmin, tested = float('inf'), None, 0
    for count in range(math.ceil(Fraction(1, 16) * volume), math.floor(Fraction(5) * volume) + 1):
        if Fraction(1, 5) * volume <= count <= Fraction(61, 20) * volume:
            continue
        x = count / volume
        up = volume * (soft(x + 1 / volume) - soft(x))
        down = volume * x * (soft(x - 1 / volume) - soft(x))
        for kin in (1, 2):
            for kout in (1, 2):
                generator = kin * up + kout * down
                if generator < minimum:
                    minimum, argmin = generator, [count, kin, kout]
                tested += 1
    require(minimum > .3 - 1e-7, 'Finite generator challenge defeats source bound')
    v, budget = 7500, 1e-6
    capture = math.exp(-3 * v / 578) + 2 * math.exp(-3 * v / 320) + 64 * v * math.exp(-v / 256)
    horizon = math.exp(v / 1024)
    residence = capture + 2 * math.exp(-11 * v / 320) + 8 * v * (8 + horizon) * math.exp(-v / 256)
    require(capture < budget < residence, 'Application decision differs from stated receiving question')
    # Exact excluded-input counterexample: both rates zero, initial x=1/10.
    # The process stays below 1/5 forever. It violates the source's rate box.
    require(Fraction(1, 10) < Fraction(1, 5), 'Counterexample initial state')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt = {
        'status': 'PASS_SOURCE_RECOVERY_AND_SCOPED_APPLICATION',
        'original_sha256': sources['original']['sha256'],
        'draft_revision': sources['draft_112']['revision'],
        'source_code_changed': False,
        'assumptions': {'network': '0 -> A and A -> 0', 'predictable_rate_box': [1, 2],
                        'initial_concentration_range': ['1/10', '4'], 'guard': ['1/16', '5'],
                        'capture': ['1/5', '61/20'], 'minimum_volume': 1200,
                        'time_units': 'nondimensional; no physical clock acquired'},
        'new_generator_challenge': {'volume': volume, 'tested_rate_corners': tested,
                                    'minimum_generator': minimum, 'argmin_count_kin_kout': argmin},
        'application': {'volume': v, 'failure_budget': budget, 'capture_deadline': 8,
                        'capture_bound': capture, 'residence_duration_after_deadline': horizon,
                        'residence_bound': residence, 'capture_budget_supported_by_bound': True,
                        'same_budget_residence_supported_by_bound': False,
                        'interpretation': 'Supplied bound insufficient for stronger residence claim, not actual residence failure'},
        'excluded_input': 'All-off rates leave x=1/10 outside capture forever; violates positive-rate assumption',
        'scope': 'New finite receiving use of hash-bound public source; ordinary floating arithmetic, no general theorem proof or stochastic simulation',
        'research_improvement': 'NOT_DEMONSTRATED; source access and executable scoped use demonstrated',
        'wall_seconds_including_source_fetch': time.perf_counter() - start,
        'self_cpu_seconds': time.process_time() - cpu,
        'process_peak_rss_bytes': peak if sys.platform == 'darwin' else peak * 1024,
        'python': sys.version,
    }
    (args.output_dir / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
