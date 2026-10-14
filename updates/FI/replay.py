#!/usr/bin/env python3
"""Bounded copy-first FI algebra/certificate checks.

Requires SymPy, NumPy, SciPy and mpmath. Output must be a new or empty directory
outside this checkout. Original inputs and frozen derived artifacts are hashed
before and after. The original historical kinetic endpoint-equality audit FAIL
is retained, not relabelled by the distinct successful checks run here.
Producer Compiler/certificate contractions are explicitly reused for large
kinetic recertification; the separate small exact checkers have their own code.
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
    ap.add_argument('--group', choices=['quartic', 'kinetics', 'barrier'], required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    a = ap.parse_args()
    out = a.output_dir.resolve()
    if out.is_relative_to(ROOT) or (out.exists() and any(out.iterdir())):
        raise ValueError('Use a new or empty owned directory outside the publication checkout')
    out.mkdir(parents=True, exist_ok=True)

    def hashes():
        for name in ['SOURCE_MANIFEST.json', 'DERIVED_MANIFEST.json']:
            for row in json.loads((HERE / name).read_text())['files']:
                p = ROOT / row['path']
                if p.stat().st_size != row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
                    raise ValueError('Input mismatch: ' + row['path'])

    def cp(src, dst):
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    def py(p, *args):
        return [sys.executable, '-B', str(out / p), *map(str, args)]

    hashes()
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    jobs = []
    if a.group == 'quartic':
        cp(HERE / 'package/quartic', out / 'FI-sources/quartic')
        cp(HERE / 'synthesis/quartic', out / 'FI-quartic')
        cp(HERE / 'synthesis/quartic_critic', out / 'FI-quartic-critic')
        for p in [
            'FI-sources/quartic/verify_positive_definite.py',
            'FI-quartic/results/check_fi_quartic.py',
            'FI-quartic-critic/independent_checker.py',
            'FI-quartic-critic/independent_rigidity_checker.py',
            'FI-quartic-critic/delta/delta_audit.py',
            'FI-quartic-critic/delta/compatible/compatible_acoustic_realization.py',
            'FI-quartic-critic/delta/compatible/fullrank/fullrank_acoustic_realization.py',
        ]:
            jobs.append((py(p), out))
    elif a.group == 'kinetics':
        cp(HERE / 'package/kinetics', out / 'FI-sources/kinetics')
        cp(HERE / 'synthesis/kinetics', out / 'FI-kinetics')
        cp(HERE / 'synthesis/kinetics_critic', out / 'FI-kinetics-critic')
        cp(HERE / 'synthesis/root', out / 'FI-root')
        cp(HERE / 'package/kinetics', out / 'FI-kinetics/replica')
        cp(HERE / 'package/kinetics', out / 'FI-kinetics/source_snapshot')
        for p in [
            'FI-kinetics-critic/independent_check.py',
            'FI-kinetics-critic/reverse_query_check.py',
            'FI-kinetics-critic/countermodels.py',
            'FI-kinetics-critic/finite_response_check.py',
            'FI-kinetics/analysis/degree3_countermodel.py',
        ]:
            jobs.append((py(p), out))
        # Verify the retained vectors before running a fresh proposal/certificate.
        jobs.append((py('FI-root/verify_retained_alpha.py',
                        '--source-dir', out / 'FI-sources/kinetics',
                        '--evidence', out / 'FI-kinetics/analysis/fresh_replay_results.json',
                        '--output-dir', out / 'FI-root'), out))
        jobs.append((py('FI-kinetics/analysis/verify_weighted_alpha_correction.py'), out))
        jobs.append((py('FI-kinetics/analysis/kinetics_audit.py'), out))
    else:
        cp(HERE / 'package/barrier', out / 'FI-sources/barrier')
        cp(HERE / 'synthesis/barrier', out / 'FI-barrier')
        cp(HERE / 'synthesis/root', out / 'FI-root')
        jobs.append((py('FI-sources/barrier/verify_barrier_gating.py', '--output', out / 'source_results.json'), out))
        jobs.append((py('FI-barrier/deepening_checker.py'), out))
        jobs.append((py('FI-barrier/delta_mixed_gate_checker.py'), out))
        jobs.append((py('FI-root/mixed_compliance_gate.py', '--output-dir', out / 'FI-root'), out))

    rows = []
    for i, (cmd, cwd) in enumerate(jobs):
        start = time.monotonic()
        try:
            r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=240)
            code, stdout, stderr = r.returncode, r.stdout, r.stderr
        except subprocess.TimeoutExpired as e:
            code = 124
            stdout = e.stdout or ''
            stderr = e.stderr or ''
            if isinstance(stdout, bytes):
                stdout = stdout.decode(errors='replace')
            if isinstance(stderr, bytes):
                stderr = stderr.decode(errors='replace')
            stderr += '\nBounded replay timed out after 240 seconds.'
        log = out / (str(i) + '-' + Path(cmd[2]).stem + '.log')
        log.write_text(stdout + '\nSTDERR:\n' + stderr)
        rows.append(dict(command=cmd, exit_code=code, seconds=time.monotonic() - start,
                         log=log.name, log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
        if code:
            break
    hashes()
    status = 'PASS' if len(rows) == len(jobs) and all(x['exit_code'] == 0 for x in rows) else 'FAIL'
    report = dict(status=status, group=a.group, python=platform.python_version(), executable=sys.executable,
                  checks=rows, expected_steps=len(jobs), published_inputs_hash_unchanged=True,
                  historical_kinetic_endpoint_equality_audit='FAIL retained; not rerun or relabelled by this wrapper',
                  scope='Bounded exact algebra/model checks. Large kinetic replay explicitly reuses producer compiler/contractions. '
                        'Reported 14576 source assertions and exploratory searches are not all rerun. '
                        'No external proof/novelty review, physical acquisition or runtime superiority established.')
    (out / 'REPLAY_WRAPPER_RECEIPT.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=status, group=a.group, steps=len(rows), expected_steps=len(jobs))))
    return 0 if status == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
