#!/usr/bin/env python3
"""Integrity check and bounded new admissions, in a fresh disposable copy.
Needs NumPy for the two scientific checks. No network/install/search jobs.
--integrity-only performs byte verification, not scientific replay.
"""
from pathlib import Path
import argparse,hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time,zipfile

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(root):
    manifest=json.loads((root/'MANIFEST.json').read_text());named=set()
    for row in manifest['files']:
        p=root/row['path'];named.add(row['path'])
        assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],row['path']
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual==named|{'MANIFEST.json'},'unexpected or missing payload'
    with zipfile.ZipFile(root/'sources/Astra_Amplification_Cycle4_ULTRA_20261022.zip') as z:
        assert z.testzip() is None
    return len(named)

def main():
    p=argparse.ArgumentParser();p.add_argument('--integrity-only',action='store_true');p.add_argument('--output-dir')
    args=p.parse_args();source=Path(__file__).resolve().parent;count=verify(source)
    if args.integrity_only:
        print(json.dumps({'status':'PASS','payload_files':count,'scope':'integrity only; no scientific job'}));return
    if args.output_dir:
        out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=False)
    else:out=Path(tempfile.mkdtemp(prefix='astra-cycle5-replay-'))
    copy=out/'payload';shutil.copytree(source,copy)
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[key]='1'
    jobs=['calculations/universal/replay.py','audits/sparse_support/replay.py']
    records=[];wall=time.perf_counter();start=resource.getrusage(resource.RUSAGE_CHILDREN)
    for job in jobs:
        t=time.perf_counter()
        run=subprocess.run([sys.executable,job],cwd=copy,env=env,text=True,capture_output=True,timeout=45)
        records.append({'script':job,'exit_code':run.returncode,'wall_seconds':time.perf_counter()-t,
                        'stdout':run.stdout[-7000:],'stderr':run.stderr[-3000:]})
        if run.returncode:break
    end=resource.getrusage(resource.RUSAGE_CHILDREN);unchanged=verify(source)==count
    receipt={'status':'PASS' if len(records)==len(jobs) and all(r['exit_code']==0 for r in records) and unchanged else 'FAIL',
             'source':str(source),'fresh_copy':str(copy),'verified_manifest_payloads':count,
             'source_preserved_unchanged':unchanged,'checks':records,'wall_seconds':time.perf_counter()-wall,
             'child_cpu_seconds':end.ru_utime+end.ru_stime-start.ru_utime-start.ru_stime,
             'child_peak_RSS_platform_units':end.ru_maxrss,'python':sys.version,
             'historical_search_or_scientific_replay':False,
             'total_scientific_discovery_cost':'UNKNOWN',
             'scope':'producer fresh-copy finite admissions only; not universal numerical proof, empirical calibration, recipient replay, acceptance or novelty'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','verified_manifest_payloads','source_preserved_unchanged','wall_seconds','child_cpu_seconds']}))
    if receipt['status']!='PASS':sys.exit(1)

if __name__=='__main__':main()
