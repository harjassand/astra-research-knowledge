#!/usr/bin/env python3
"""Bounded copy-first FJ certificate/model replays, never truth certification.

Requires NumPy, SymPy, SciPy and mpmath. Use a fresh output directory outside
the checkout. The source Monte Carlo smoke run uses the frozen adapter that
only removes the Numba import/two decorators; its algorithm and floats are
unchanged. It is explicitly not an unmodified Numba performance replay or a
finite-bit continuous-TV certificate. No full search, laboratory test or large
producer run is silently rerun. Source and selected derived bytes are hashed
before and after all jobs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--group', choices=['quartic', 'nonlinear', 'physical', 'supporting'], required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    a = ap.parse_args()
    out = a.output_dir.resolve()
    if out.is_relative_to(ROOT) or (out.exists() and any(out.iterdir())):
        raise ValueError('Use a new or empty owned directory outside the publication checkout')
    out.mkdir(parents=True, exist_ok=True)

    def hashes():
        count = 0
        for mf in ['SOURCE_MANIFEST.json', 'DERIVED_MANIFEST.json']:
            for row in json.loads((HERE / mf).read_text())['files']:
                p = ROOT / row['path']
                if p.stat().st_size != row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
                    raise ValueError('Input mismatch: '+row['path'])
                count += 1
        return count

    def cp(src, dst):
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    # Keep workers' original relative layout in scratch, including any explicitly
    # used baseline data. Only copies may be overwritten by scientific scripts.
    for name in ['quartic', 'nonlinear', 'physical']:
        cp(HERE / 'package' / name, out / 'work/FJ-sources' / name)
    mapping = {
        'quartic': ['contact_audit', 'contact_global', 'compensation_general'],
        'nonlinear': ['nonlinear_audit', 'branching_spectral', 'nonlinear_benchmark', 'query_variance', 'decision_quantum_delta1', 'root'],
        'physical': ['hydro_audit', 'intervention_schur', 'wet_experiment', 'physical_alternative'],
        'supporting': ['decision_quantum', 'kinetic_observable'],
    }
    for name in mapping[a.group]:
        cp(HERE / 'synthesis' / name, out / 'work' / ('FJ-'+name.replace('_', '-')))

    jobs = []
    def py(p, *args):
        jobs.append([sys.executable, '-B', str(out / 'work' / p), *map(str, args)])

    if a.group == 'quartic':
        for p in [
            'FJ-sources/quartic/verify_contact_compensation.py', 'FJ-sources/quartic/verify_previous.py',
            'FJ-contact-audit/independent_checks.py', 'FJ-contact-global/near_contact_modes.py',
            'FJ-contact-global/verify_concentration_escape.py', 'FJ-compensation-general/verify_generalization.py',
        ]:
            py(p)
    elif a.group == 'nonlinear':
        py('FJ-sources/nonlinear/verify_certificates.py')
        py('FJ-nonlinear-audit/source-copy/nonlinear_query_plain.py', '--samples', '200', '--output', out / 'source_plain_200.json')
        for p in [
            'FJ-nonlinear-audit/exact_cases.py', 'FJ-nonlinear-audit/N722_composition_checks.py',
            'FJ-nonlinear-audit/sinh_degree_audit.py', 'FJ-branching-spectral/verify_certificate.py',
            'FJ-branching-spectral/delta-audit/verify_delta.py', 'FJ-branching-spectral/delta-audit/verify_post_root.py',
        ]:
            py(p)
        py('FJ-root/observation_channel.py', '--outputs', '200', '--output-dir', out / 'root_bounded_diagnostic')
        for p in [
            'FJ-nonlinear-benchmark/deterministic_interval.py',
            'FJ-decision-quantum-delta1/checks/gaussian_output_sampling_checks.py',
            'FJ-query-variance/verify_source_control.py', 'FJ-query-variance/antithetic_bias_check.py',
        ]:
            py(p)
    elif a.group == 'physical':
        for p in [
            'FJ-sources/physical/check_model.py', 'FJ-hydro-audit/exact_checks.py',
            'FJ-hydro-audit/noise_delta_checks.py', 'FJ-intervention-schur/verify_schur_intervention.py',
            'FJ-wet-experiment/calculations.py', 'FJ-physical-alternative/derived/electrokinetic_bound.py',
        ]:
            py(p)
    else:
        p = ROOT / 'updates/FI/synthesis/kinetics_critic/finite_response_results.json'
        d = out / 'work/astra-capital/updates/FI/synthesis/kinetics_critic/finite_response_results.json'
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, d)
        py('FJ-decision-quantum/assay_cost.py')
        py('FJ-kinetic-observable/code/verify_branch_assay.py')

    count = hashes()
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    rows = []
    for i, cmd in enumerate(jobs):
        start = time.monotonic()
        try:
            r = subprocess.run(cmd, cwd=out, env=env, capture_output=True, text=True, timeout=180)
            code, stdout, stderr = r.returncode, r.stdout, r.stderr
        except subprocess.TimeoutExpired as e:
            code, stdout, stderr = 124, e.stdout or '', e.stderr or ''
            if isinstance(stdout, bytes): stdout = stdout.decode(errors='replace')
            if isinstance(stderr, bytes): stderr = stderr.decode(errors='replace')
            stderr += '\nBounded replay timed out after180seconds.'
        log = out / (str(i)+'-'+Path(cmd[2]).stem+'.log')
        log.write_text(stdout+'\nSTDERR:\n'+stderr)
        rows.append(dict(command=cmd, exit_code=code, seconds=time.monotonic()-start,
                         log=log.name, log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
        if code:
            break
    assert hashes() == count
    status = 'PASS' if len(rows) == len(jobs) and all(x['exit_code'] == 0 for x in rows) else 'FAIL'
    receipt = dict(status=status, group=a.group, python=platform.python_version(), executable=sys.executable,
                   checks=rows, expected_steps=len(jobs), published_inputs_hash_unchanged=True,
                   hashed_original_and_derived_files=count,
                   scope='Bounded exact certificate/model and floating diagnostics. Numba removal adapter is explicit; no full producer Monte Carlo, original Numba timing, exhaustive search, external proof/novelty, digital-law or physical certification. Wall seconds are execution, not aggregate inference.')
    (out / 'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(dict(status=status, group=a.group, steps=len(rows), expected_steps=len(jobs))))
    return 0 if status == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
