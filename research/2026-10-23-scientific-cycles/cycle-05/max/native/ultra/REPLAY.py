#!/usr/bin/env python3
"""Verify source, replay new bounded admissions in a disposable fresh copy.

Standard library exact-only mode; full mode additionally needs NumPy.
No network, installations, optimizers or historical search/replay campaign.
"""
from pathlib import Path
import argparse, hashlib, json, os, resource, shutil, subprocess, sys, tempfile, time, zipfile

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root):
    manifest=json.loads((root/'MANIFEST.json').read_text())
    named=set()
    for row in manifest['files']:
        path=root/row['path'];named.add(row['path'])
        assert path.is_file() and path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],row['path']
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual==named|{'MANIFEST.json'},'unmanifested or missing payload'
    for name in ['Astra_Amplification_Cycle3_ULTRA_20261022.zip',
                 'Astra_Cycle4_Operator_Capital_20261022.zip']:
        with zipfile.ZipFile(root/'sources'/name) as z:
            assert z.testzip() is None,name
    return len(named)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--exact-only',action='store_true')
    parser.add_argument('--output-dir')
    args=parser.parse_args()
    source=Path(__file__).resolve().parent;before=verify(source)
    if args.output_dir:
        out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=False)
    else:
        out=Path(tempfile.mkdtemp(prefix='astra-cycle4-replay-'))
    copy=out/'payload';shutil.copytree(source,copy)
    env=os.environ.copy()
    for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    jobs=[['audits/nonmax_cut/replay.py'],
          ['audits/physical_structure/replay.py'],
          ['audits/witness_audit/verify_gap_obstruction.py']]
    if not args.exact_only:jobs.append(['replay/principal/replay.py'])
    rows=[];wall=time.perf_counter();cpu0=resource.getrusage(resource.RUSAGE_CHILDREN)
    for job in jobs:
        started=time.perf_counter()
        proc=subprocess.run([sys.executable,*job],cwd=copy,env=env,text=True,capture_output=True,timeout=45)
        rows.append({'command':[sys.executable,*job],'exit_code':proc.returncode,
                     'wall_seconds':time.perf_counter()-started,
                     'stdout':proc.stdout[-10000:],'stderr':proc.stderr[-3000:]})
        if proc.returncode:break
    cpu1=resource.getrusage(resource.RUSAGE_CHILDREN)
    unchanged=verify(source)==before
    receipt={
        'status':'PASS' if len(rows)==len(jobs) and all(row['exit_code']==0 for row in rows) and unchanged else 'FAIL',
        'source':str(source),'fresh_copy':str(copy),'source_manifest_files_verified':before,
        'source_preserved_unchanged':unchanged,'exact_only':args.exact_only,'checks':rows,
        'wall_seconds':time.perf_counter()-wall,
        'child_cpu_seconds':cpu1.ru_utime+cpu1.ru_stime-cpu0.ru_utime-cpu0.ru_stime,
        'child_peak_RSS_platform_units':cpu1.ru_maxrss,'python':sys.version,
        'old_search_or_old_scientific_replay_run':False,
        'total_discovery_coordination_reasoning_cost':'UNKNOWN',
        'scope':'producer relocated replay of new bounded admissions; not universal numerical proof, recipient execution, acceptance, historical priority or hardware performance'
    }
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','source_manifest_files_verified','source_preserved_unchanged','wall_seconds','child_cpu_seconds']}))
    if receipt['status']!='PASS':sys.exit(1)

if __name__=='__main__':main()
