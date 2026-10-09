"""Run selected scoped diagnostics from a pack containing no third-party sources.

The tests check stated finite identities or arithmetic. Passing is not external
proof validation, a novelty determination, or empirical confirmation.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

TESTS = [
    ('hidden_seed', ['work/sol/hidden_realization/verify_exact_certificate.py']),
    ('hidden_seed_optimized', ['-O', 'work/sol/hidden_realization/verify_exact_certificate.py']),
    ('hidden_fixed_lag', ['work/sol/hidden_realization/fixed_lag_certificate_v1.py']),
    ('independent_frame', ['work/natural/n22_reversible_frame/verify_frame_obstruction.py']),
    ('observable_coefficients', ['work/sol/observable_separation/build_and_verify_witness_v1.py']),
    ('observable_coefficients_optimized', ['-O', 'work/sol/observable_separation/build_and_verify_witness_v1.py']),
    ('independent_observable', ['work/sol/hidden_realization/observable_audit_v1.py']),
    ('word_evaluator', ['work/sol/observable_separation/evaluate_witness_v1.py', '--word', '0', '1', '0', '0', '2', '0', '3']),
    ('intrinsic_arrays_t3', ['work/sol/local_chart_decoder/check_intrinsic_bicomplex.py', '--t', '3', '--trials', '64']),
    ('intrinsic_arrays_t4', ['work/sol/local_chart_decoder/check_intrinsic_bicomplex.py', '--t', '4', '--trials', '64']),
    ('fixed_color', ['work/sol/local_chart_decoder/check_fixed_color_charging.py']),
    ('global_fault_masks', ['work/applied/a22_quantum_global_mask/check_masks.py']),
    ('encoded_transfer', ['work/sol/quantum_faults/teleport_check.py']),
    ('cosmology_cross_species', ['work/sol/causal_cosmology/exact_checks.py']),
    ('cosmology_tensor_kernel', ['work/sol/causal_cosmology/tensor_kernel_checks_v1.py']),
    ('cosmology_health_source', ['work/sol/causal_cosmology/health_source_checks_v1.py']),
    ('robust_gaussian_moments', ['work/sol/robust_recovery/exact_checks_v1.py']),
    ('periodic_continuum_constants', ['work/sol/fault_nucleation/periodic_constants_check.py']),
    ('horn30', ['work/natural/n24_small_horn/certify_small_horn.py']),
    ('binary_hierarchy', ['work/natural/n10_hidden_dissipation/verify_binary_hierarchy.py']),
    ('arithmetic_parameters', ['work/theory/arithmetic_review/parameter_check_v1.py']),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    args = ap.parse_args()
    root = args.root.resolve()
    for forbidden in ['work/sources', 'work/sol/hidden_realization/.venv']:
        if (root / forbidden).exists():
            raise RuntimeError('Replay must omit source repositories and private runtimes')
    out = root / 'checks'
    out.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

    def run(item):
        name, command = item
        start = time.monotonic()
        try:
            p = subprocess.run([sys.executable, *command], cwd=root, env=env,
                               capture_output=True, text=True, timeout=240)
            text = p.stdout + ('\nSTDERR:\n' + p.stderr if p.stderr else '')
            code = p.returncode
        except subprocess.TimeoutExpired as exc:
            text = str(exc)
            code = 124
        log = out / (name + '.txt')
        log.write_text(text)
        return dict(name=name, command=[sys.executable, *command], exit_code=code,
                    status='PASS' if code == 0 else 'FAIL', seconds=round(time.monotonic()-start, 3),
                    log=str(log.relative_to(root)), sha256=hashlib.sha256(log.read_bytes()).hexdigest())

    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run, item) for item in TESTS]
        for future in as_completed(futures):
            r = future.result()
            results.append(r)
            print(r['name'], r['status'], r['seconds'], flush=True)
    result = dict(scope='Selected finite diagnostics and arithmetic only; no source repositories or PDFs present.',
                  python=sys.version, count=len(results), passed=sum(r['exit_code'] == 0 for r in results),
                  results=sorted(results, key=lambda x: x['name']))
    (out / 'REPLAY_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    if result['passed'] != result['count']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
