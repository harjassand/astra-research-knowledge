"""Rehydrate exact published inputs into the workers' expected scratch layout.

Does not modify publication bytes. Math checks are finite diagnostics, not
analytic formalizations. Acquired external data/fulltexts are not downloaded.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import time

CASES = [
    ('ga_analytic_audit', 'verify_exact.py'),
    ('ga_ui_audit', 'verify_exact_witnesses.py'),
    ('ga_concentration_genesis', 'verify_exact.py'),
    ('ga_concentration_audit', 'verify_concentration_audit.py'),
    ('ga_weighted_audit', 'verify_weighted_audit.py'),
    ('ga_weighted_audit', 'verify_strict_addendum.py'),
    ('ga_nonlinear_stress_audit', 'exact_audit.py'),
    ('ga_polynomial_genesis', 'weighted_jet_verify.py'),
    ('ga_sharp_invention', 'verify.py'),
    ('ga_parametric_stress_genesis', 'verify_all_r.py'),
    ('ga_nonlinear_stress_audit', 'all_r_exact_audit.py'),
    ('ga_nonlinear_stress_audit', 'mixed_source_exact_audit.py'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path,
                        help='Published package containing originals/ and derived/.')
    parser.add_argument('--research', type=Path,
                        help='Unpublished research root containing originals/, root/, workers/.')
    parser.add_argument('--output', type=Path, required=True,
                        help='New scratch directory; existing directories are refused.')
    args = parser.parse_args()
    if (args.package is None) == (args.research is None):
        parser.error('Choose exactly one of --package or --research')
    source = (args.package or args.research).resolve()
    original = source/'originals'
    derived = source/'derived' if args.package else source
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(source):
        raise RuntimeError('Scratch output must be new and outside source tree')
    output.mkdir(parents=True)
    shutil.copytree(original, output/'originals')
    shutil.copytree(derived/'root', output/'root',
                    ignore=shutil.ignore_patterns('replay', 'replay_v2', '__pycache__'))
    # Explicitly select only published author/check artifacts, never a clone,
    # downloaded text, original scratch extraction, or runtime optimizer state.
    for worker, _ in CASES:
        src = derived/'workers'/worker
        dest = output/'workers'/worker
        dest.mkdir(parents=True, exist_ok=True)
        for path in src.iterdir():
            if path.is_file() and (path.suffix in {'.py', '.md', '.json'}
                                  or path.name in {'ALL_R_THEOREM_PROOF.txt', 'FAILED_NATURAL_STRESS_DERIVATION.txt'}):
                shutil.copyfile(path, dest/path.name)
    rows = []
    for worker, script in CASES:
        cwd = output/'workers'/worker
        start = time.monotonic()
        result = subprocess.run(['python3', script], cwd=cwd, text=True, capture_output=True)
        logdir = output/'logs'/(worker+'_'+Path(script).stem)
        logdir.mkdir(parents=True)
        (logdir/'stdout.log').write_text(result.stdout)
        (logdir/'stderr.log').write_text(result.stderr)
        rows.append({'worker':worker, 'script':script,
                     'script_sha256':hashlib.sha256((cwd/script).read_bytes()).hexdigest(),
                     'exit_code':result.returncode,
                     'wall_seconds':round(time.monotonic()-start, 3),
                     'stdout':str((logdir/'stdout.log').relative_to(output)),
                     'stderr':str((logdir/'stderr.log').relative_to(output))})
        print(worker, script, result.returncode, flush=True)
    receipt = {'schema':'astra.ga.public-replay.v1', 'cases':rows,
               'all_passed':all(row['exit_code']==0 for row in rows),
               'scope':'Exact finite replay in rehydrated scratch; source bytes unchanged; no analytic/physical/priority validation'}
    (output/'RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    if not receipt['all_passed']:
        raise RuntimeError('One or more checks failed; inspect retained logs')


if __name__ == '__main__':
    main()
