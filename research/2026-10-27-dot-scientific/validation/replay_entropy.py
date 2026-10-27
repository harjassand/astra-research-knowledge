#!/usr/bin/env python3
"""Replay selected frozen entropy checkers in a disposable copy, never originals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

SCRIPTS = [
    'reduction_criterion_stationary_check.py',
    'relative_peak_parametric_contraction_check.py',
    'relative_peak_nine_fifths_scalar_check.py',
    'relative_peak_nine_fifths_margin_check.py',
    'relative_marginal_bkm_entropy_region_certificate.py',
    'one_sided_relative_peak_entropy_certificate.py',
    'local_variance_index_27_over_4_check.py',
    'local_index_twenty_seven_fourths_certificate.py',
    'flat_mixed_success_arbitrary_bump_one_crossing_certificate.py',
    'flat_mixed_success_arbitrary_reset_hole_clock_certificate.py',
    'nonflat_two_mode_white_rank_one_reset_certificate.py',
    'nonflat_two_mode_white_rank_one_reset_actual_ratio_check.py',
    'nonflat_three_mode_maxent_reset_certificate.py',
    'nonflat_three_mode_maxent_reset_actual_ratio_check.py',
    'relative_peak_three_halves_rigidity_check.py',
    'low_schmidt_boundary_gap_certificate.py',
    'reference_two_inverse_boundary_check.py',
    'reference_classical_inverse_trace_check.py',
    'qubit_small_bias_logdet_constants_check.py',
    'relative_peak_local_variance_cap_counterexample.py',
    'relative_peak_near_one_cap_obstruction_check.py',
    'generic_relative_peak_two_surrogate_failure_check.py',
    'source_weighted_jensen_cubic_sharp_check.py',
    'whole_source_single_variance_payment_failure_check.py',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[1] / 'source' / 'quantum_operational_certification_20261024')
    parser.add_argument('--output', type=Path, required=True, help='New disposable output directory; must not exist')
    parser.add_argument('--timeout', type=int, default=240)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    work = args.output / 'source-copy'
    shutil.copytree(args.source_root, work)
    records = []
    for name in SCRIPTS:
        script = work / name
        frozen = {p.name: sha(p.read_bytes()) for p in args.source_root.glob('*.json')}
        start = time.monotonic()
        try:
            result = subprocess.run([sys.executable, str(script.resolve())], cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=args.timeout, env={**os.environ, 'OPENBLAS_NUM_THREADS': '1'})
            output, code = result.stdout, result.returncode
            status = 'PASS' if code == 0 else 'FAIL'
        except subprocess.TimeoutExpired as error:
            output, code, status = error.stdout or b'', None, 'TIMEOUT'
        (args.output / (name + '.log')).write_bytes(output)
        changes = [{'file': p.name, 'replay_sha256': sha(p.read_bytes()), 'frozen_sha256': frozen.get(p.name)} for p in work.glob('*.json') if sha(p.read_bytes()) != frozen.get(p.name)]
        records.append({'script': name, 'source_sha256': sha((args.source_root / name).read_bytes()), 'status': status, 'exit_code': code, 'seconds': round(time.monotonic() - start, 3), 'changed_json_outputs': changes, 'output_sha256': sha(output)})
        (args.output / 'report.json').write_text(json.dumps({'scope': 'Selected supplied symbolic/rational/finite checkers; not full theorem reproof, independent moment acquisition, physical evidence or practical advantage.', 'records': records}, indent=2) + '\n')
        print(name, status, flush=True)
    if any(row['status'] != 'PASS' or row['changed_json_outputs'] for row in records):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
