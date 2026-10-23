"""Archive-level replay wrapper, installed as replay.py at the archive root.

Runs frozen new checks in an isolated copy. It never reruns the resolved
incoming moment construction and never modifies packaged original receipts.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, time, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OWNER_NAME = 'Astra_Restore_PRO2_20261021'
OWNER_SIZE = 6330093
OWNER_HASH = 'f58b4f09eb259f0ac2d3962b955abd0fc7d603a7960a038257b72b1f00624115'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_manifest():
    m = json.loads((ROOT/'MANIFEST.json').read_text())
    for entry in m['files']:
        rel = Path(entry['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('unsafe manifest path')
        p = ROOT/rel
        if p.stat().st_size != entry['byte_size'] or sha(p) != entry['sha256']:
            raise ValueError('manifest mismatch: '+str(rel))
    return len(m['files'])


def extract_owner(archive, destination):
    if archive.stat().st_size != OWNER_SIZE or sha(archive) != OWNER_HASH:
        raise ValueError('original owner ZIP identity mismatch')
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            p = Path(info.filename)
            if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != OWNER_NAME:
                raise ValueError('unexpected original ZIP path')
            if ((info.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError('symbolic link in original ZIP')
            target = destination.joinpath(*p.parts[1:])
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(info))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--quick', action='store_true', help='Skip the already independently replayed 39-second joint inertia calculation.')
    args = ap.parse_args()
    started = time.perf_counter()
    out = args.output.resolve()
    if out.exists() or ROOT == out or ROOT in out.parents:
        raise ValueError('output must be a new directory outside this immutable package')
    count = verify_manifest()
    out.mkdir(parents=True)
    shutil.copytree(ROOT/'research', out/'research', ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    extract_owner(ROOT/'sources'/(OWNER_NAME+'.zip'), out/'restore_pro2')
    logs = out/'logs'
    logs.mkdir()
    commands = [
        ['checks/check_exact_matmul.py'],
        ['checks/check_completion_exact.py'],
        ['checks/check_sparse_identifiability.py','--verify'],
        ['checks/check_symmetric_sparse_identifiability.py','--verify'],
        ['checks/check_sparse_degeneracy.py'],
        ['checks/check_eight_probe_obstruction.py'],
        ['src/sparse_condition_witness.py','--replay'],
        ['checks/check_sparse_noise_audit.py'],
        ['checks/check_path_stability.py'],
        ['checks/check_row_cap_counterexample.py'],
        ['checks/check_forest_recovery.py'],
    ]
    if not args.quick:
        commands.append(['src/common_action.py','--replay'])
    env = os.environ.copy()
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
        env[key] = '1'
    rows = []
    for index, command in enumerate(commands):
        st = time.perf_counter()
        cp = subprocess.run([sys.executable]+command, cwd=out/'research', env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        wall = time.perf_counter()-st
        path = logs/f'{index+1:02d}_{Path(command[0]).stem}.txt'
        path.write_text(cp.stdout)
        rows.append({'command':command,'returncode':cp.returncode,'wall_seconds':wall,
                     'log':str(path.relative_to(out)),'log_sha256':sha(path)})
        print(json.dumps(rows[-1]), flush=True)
        if cp.returncode:
            break
    manifest_count_after = verify_manifest()
    result = {'PASS':all(r['returncode']==0 for r in rows) and len(rows)==len(commands),
              'mode':'quick_portability_only' if args.quick else 'full_new_certificate_replay',
              'main_joint_inertia_recomputed':not args.quick,
              'incoming_resolved_moment_recomputed':False,
              'new_proposals_or_probes':False,'manifest_files_checked':count,
              'manifest_files_checked_after':manifest_count_after,
              'original_owner_zip_sha256':OWNER_HASH,'runs':rows,
              'enclosing_wall_seconds':time.perf_counter()-started,
              'output_directory':str(out),'packaged_receipts_unchanged':True}
    (out/'REPLAY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not result['PASS']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
