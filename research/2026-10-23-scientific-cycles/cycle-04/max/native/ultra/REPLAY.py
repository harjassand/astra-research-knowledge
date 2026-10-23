#!/usr/bin/env python3
"""Verify immutable payload, copy to a fresh directory, replay exact checks.

Use --exact-only without NumPy. Full replay additionally needs NumPy.
No package installs, network access, optimization searches or old campaign runs.
"""
from pathlib import Path
import argparse, hashlib, json, os, resource, shutil, subprocess, sys, tempfile, time, zipfile

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(root):
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for row in manifest['files']:
        p=root/row['path']
        assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'], row['path']
    with zipfile.ZipFile(root/'sources/Astra_Amplification_Cycle2_ULTRA_20261022.zip') as z:
        assert z.testzip() is None
    return len(manifest['files'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--exact-only',action='store_true')
    ap.add_argument('--output-dir');args=ap.parse_args()
    source=Path(__file__).resolve().parent; before=verify(source)
    if args.output_dir:
        out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=False)
    else: out=Path(tempfile.mkdtemp(prefix='astra-cycle3-replay-'))
    copy=out/'payload';shutil.copytree(source,copy)
    env=os.environ.copy()
    for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    jobs=[
      ['audits/cone_challenge/certify.py'],
      ['audits/root_audit_q8.py'],
      ['audits/domino/verify_domino.py'],
      ['audits/invariant/verify_partition_lemma.py'],
      ['audits/independent_audit/check_independent.py'],
    ]
    if not args.exact_only:
        jobs += [['audits/endpoint/check_endpoint.py'],['audits/invariant/check_invariant.py']]
    rows=[];wall=time.perf_counter();cpu0=resource.getrusage(resource.RUSAGE_CHILDREN)
    for job in jobs:
        st=time.perf_counter()
        p=subprocess.run([sys.executable,*job],cwd=copy,env=env,text=True,capture_output=True,timeout=45)
        rows.append({'command':[sys.executable,*job],'exit_code':p.returncode,
                     'wall_seconds':time.perf_counter()-st,'stdout':p.stdout[-7000:],'stderr':p.stderr[-3000:]})
        if p.returncode: break
    cpu1=resource.getrusage(resource.RUSAGE_CHILDREN)
    unchanged=verify(source)==before
    receipt={'status':'PASS' if all(x['exit_code']==0 for x in rows) and len(rows)==len(jobs) and unchanged else 'FAIL',
       'source':str(source),'fresh_copy':str(copy),'source_manifest_files_verified':before,
       'source_preserved_unchanged':unchanged,'exact_only':args.exact_only,'checks':rows,
       'wall_seconds':time.perf_counter()-wall,
       'child_cpu_seconds':cpu1.ru_utime+cpu1.ru_stime-cpu0.ru_utime-cpu0.ru_stime,
       'child_peak_RSS_platform_units':cpu1.ru_maxrss,'python':sys.version,
       'total_scientific_discovery_cost':'UNKNOWN',
       'scope':'producer relocated replay only; not recipient execution, novelty, acceptance or hardware performance'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','source_manifest_files_verified','source_preserved_unchanged','wall_seconds','child_cpu_seconds']}))
    if receipt['status']!='PASS':sys.exit(1)

if __name__=='__main__':main()
