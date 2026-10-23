#!/usr/bin/env python3
"""Verify frozen source identities; optionally replay only four new diagnostics.

Default mode uses the Python standard library and writes no package files.
--replay needs NumPy and SciPy and runs in an isolated temporary copy.
Integrity and finite diagnostic checks are not mathematical certification.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parent
PREDECESSOR = 'preserved/Astra_Amplification_Cycle9_PRO1_20261022.zip'
PREDECESSOR_BYTES = 5895441
PREDECESSOR_SHA256 = '5aa0f7400b36a04a470043a20d3c39382b66893766eb62d97b07a7721f1f52e5'
PREDECESSOR_ROOT = 'Astra_Amplification_Cycle9_PRO1_20261022'
APPENDICES = ('INHERITED_ENDPOINT_RESPONSE.tex',
              'INHERITED_OPERATOR_CODING.tex', 'INHERITED_COMPRESSION.tex')
REVIEW_DIR = 'contributions/operator_challenge'
MAIN_PROOF = 'QUADRATIC_CAPACITY_FLOOR.tex'
REPLAYS = (
    'representation/gram_input_check.py',
    'representation/capacity_comparison.py',
    'contributions/charge_structure/exact_charge_check.py',
    'contributions/hamming_response/physical_hamming_check.py',
)

class VerificationError(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def relative_file(relative, base=ROOT):
    require(isinstance(relative, str) and bool(relative), 'Missing relative file path.')
    p = PurePosixPath(relative)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in relative,
            f'Unsafe relative file path: {relative!r}')
    target = base.joinpath(*p.parts)
    require(target.is_file() and not target.is_symlink(), f'Missing regular file: {relative}')
    require(target.resolve().is_relative_to(base.resolve()), f'File escapes package root: {relative}')
    return target

def matches_identity(path, identity):
    return (path.is_file() and path.stat().st_size == identity['bytes']
            and sha256(path) == identity['sha256'])

def check_identity(identity):
    require(isinstance(identity, dict), 'Malformed file identity record.')
    require(isinstance(identity.get('bytes'), int) and identity['bytes'] >= 0,
            'File identity has no valid byte count.')
    require(isinstance(identity.get('sha256'), str)
            and re.fullmatch(r'[0-9a-f]{64}', identity['sha256']) is not None,
            'File identity has no valid SHA256.')
    path = relative_file(identity.get('path'))
    require(matches_identity(path, identity), f"File identity mismatch: {identity['path']}")
    return identity['path']

def check_manifest():
    manifest = ROOT/'MANIFEST.sha256'
    require(manifest.is_file(), 'MANIFEST.sha256 is absent. Use the complete native archive.')
    entries = []
    seen = set()
    for number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
        require('  ' in line, f'Malformed manifest line {number}.')
        digest, relative = line.split('  ', 1)
        require(re.fullmatch(r'[0-9a-f]{64}', digest) is not None,
                f'Malformed SHA256 on manifest line {number}.')
        require(relative not in seen and relative != 'MANIFEST.sha256',
                f'Duplicate or self-referential manifest entry: {relative}')
        seen.add(relative)
        path = relative_file(relative)
        require(sha256(path) == digest, f'Manifest mismatch: {relative}')
        entries.append((relative, digest))
    require(bool(entries), 'Empty package manifest.')
    return entries

def check_predecessor_and_appendices():
    path = relative_file(PREDECESSOR)
    require(path.stat().st_size == PREDECESSOR_BYTES, 'Native Cycle9 byte count mismatch.')
    require(sha256(path) == PREDECESSOR_SHA256, 'Native Cycle9 SHA256 mismatch.')
    checked = []
    with zipfile.ZipFile(path) as archive:
        for name in APPENDICES:
            local = relative_file(name)
            original = archive.read(f'{PREDECESSOR_ROOT}/{name}')
            require(local.read_bytes() == original, f'Inherited appendix changed: {name}')
            checked.append({'path': name, 'bytes': len(original),
                            'sha256': hashlib.sha256(original).hexdigest(),
                            'byte_identical_to_native_cycle9': True})
    return {'filename': Path(PREDECESSOR).name, 'bytes': PREDECESSOR_BYTES,
            'sha256': PREDECESSOR_SHA256, 'status': 'MATCHED'}, checked

def check_reviews():
    """Verify the observed native receipt schema, including historical snapshots.

    Scientific status strings are reported, not promoted to external acceptance.
    Earlier bound sources are allowed to differ only when their exact reviewed
    bytes remain in the explicitly named reviewed/ snapshot directory.
    """
    final_path = ROOT/REVIEW_DIR/'FINAL_DELTA_REVIEW.json'
    integrated_path = ROOT/REVIEW_DIR/'INTEGRATED_MANUSCRIPT_REVIEW.json'
    snapshots = []
    final_result = {'status': 'ABSENT', 'meaning': 'No final-delta version binding available.'}
    if final_path.is_file():
        final = json.loads(final_path.read_text(encoding='utf-8'))
        bindings = final.get('bound_sources')
        require(isinstance(bindings, list) and bool(bindings),
                'Present final review has no recognizable bound_sources array.')
        names = [check_identity(item) for item in bindings]
        require(MAIN_PROOF in names, 'Final review does not bind the current main proof.')
        prior = final.get('prior_integrated_review')
        require(isinstance(prior, dict), 'Final review lacks its prior-review identity.')
        check_identity(prior)
        require(prior['path'] == f'{REVIEW_DIR}/INTEGRATED_MANUSCRIPT_REVIEW.json',
                'Unexpected prior integrated-review path.')
        snapshots = final.get('preserved_reviewed_snapshots', [])
        require(isinstance(snapshots, list), 'Malformed reviewed-snapshot list.')
        for item in snapshots:
            check_identity(item)
        final_result = {'status': 'MATCHED', 'current_file_bindings_checked': len(names),
                        'historical_snapshot_bindings_checked': len(snapshots),
                        'receipt_sha256': sha256(final_path),
                        'reported_internal_status': final.get('status')}
    require(integrated_path.is_file(), 'Integrated review receipt is missing.')
    integrated = json.loads(integrated_path.read_text(encoding='utf-8'))
    bindings = integrated.get('bound_sources')
    require(isinstance(bindings, list) and bool(bindings),
            'Integrated review has no recognizable bound_sources array.')
    historical = []
    for item in bindings:
        current = relative_file(item.get('path'))
        if matches_identity(current, item):
            continue
        old_relative = f"{REVIEW_DIR}/reviewed/{PurePosixPath(item['path']).name}"
        old_path = relative_file(old_relative)
        require(matches_identity(old_path, item),
                f"Old reviewed source has neither current nor retained matching bytes: {item['path']}")
        if snapshots:
            require(any(s['path'] == old_relative and s['sha256'] == item['sha256']
                        and s['bytes'] == item['bytes'] for s in snapshots),
                    f'Old reviewed source is absent from final snapshot bindings: {old_relative}')
        historical.append({'original_path': item['path'], 'retained_snapshot': old_relative})
    earlier = integrated.get('earlier_contribution')
    if earlier is not None:
        check_identity(earlier)
    return {'final_delta': final_result,
            'integrated_bound_sources_checked': len(bindings),
            'historical_versions_preserved': historical,
            'scope': 'File/version binding only; not an independent mathematical verdict.'}

def run_replays(entries):
    start = time.perf_counter()
    records = []
    with tempfile.TemporaryDirectory(prefix='astra_pro1_cycle10_verify_') as temporary:
        isolated = Path(temporary)/'native'
        isolated.mkdir()
        for relative, _ in entries:
            source = relative_file(relative)
            destination = isolated.joinpath(*PurePosixPath(relative).parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        shutil.copyfile(ROOT/'MANIFEST.sha256', isolated/'MANIFEST.sha256')
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            env[key] = '1'
        for relative in REPLAYS:
            script = relative_file(relative, isolated)
            begin = time.perf_counter()
            try:
                result = subprocess.run([sys.executable, '-B', str(script)], cwd=isolated,
                                        env=env, capture_output=True, text=True,
                                        timeout=60, check=False)
            except subprocess.TimeoutExpired as exc:
                raise VerificationError(f'New bounded replay timed out after 60 seconds: {relative}') from exc
            require(result.returncode == 0,
                    f'Replay failed: {relative}\n{(result.stderr or result.stdout)[-4000:]}')
            report = json.loads(script.with_suffix('.json').read_text(encoding='utf-8'))
            if relative.endswith('capacity_comparison.py'):
                rows = report.get('observations', [])
                eligible = [row for row in rows if 'cycle10_k' in row]
                require(bool(eligible) and all(row.get('all_analytic_scalar_margins_pass') is True
                                              for row in eligible),
                        'Capacity comparison did not report all new scalar assertions passing.')
                require(report.get('source_sha256') == sha256(script),
                        'Capacity comparison replay source binding mismatch.')
                passed = 'ALL_NEW_ANALYTIC_SCALAR_ASSERTIONS_PASSED'
            elif relative.endswith('physical_hamming_check.py'):
                require(report.get('all_checks') == 'PASS', 'Physical Hamming diagnostic did not pass.')
                passed = report['all_checks']
            else:
                require(report.get('status') == 'PASS', f'Replay did not report PASS: {relative}')
                passed = report['status']
            records.append({'script': relative, 'status': passed,
                            'whole_subprocess_wall_seconds': time.perf_counter()-begin,
                            'reported_body_wall_seconds': report.get('wall_seconds'),
                            'reported_peak_rss_kib_linux': report.get('peak_rss_kib_linux')})
    # An independent integrity pass confirms that no frozen output changed.
    after = check_manifest()
    require(after == entries, 'Frozen manifest entries changed during isolated replay.')
    return {'status': 'PASS', 'isolated_temporary_copy': True,
            'frozen_files_rechecked_unchanged': True, 'scripts': records,
            'total_replay_wall_seconds': time.perf_counter()-start,
            'scope': 'Only four new finite diagnostics; not all-length proof or discovery cost.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true',
                        help='Run exactly four new diagnostics in an isolated temporary copy; needs NumPy/SciPy.')
    args = parser.parse_args()
    start = time.perf_counter()
    entries = check_manifest()
    predecessor, appendices = check_predecessor_and_appendices()
    report = {'status': 'PASS', 'manifest_files_checked': len(entries),
              'predecessor': predecessor, 'inherited_appendices': appendices,
              'review_bindings': check_reviews(),
              'scope': 'Integrity, provenance and version checks only; not scientific acceptance.'}
    if args.replay:
        report['replay'] = run_replays(entries)
    report['verification_wall_seconds'] = time.perf_counter()-start
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (VerificationError, OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2), file=sys.stderr)
        sys.exit(1)
