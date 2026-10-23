#!/usr/bin/env python3
"""Relocatable new-source receiving checks; never reruns historical science."""
import argparse,hashlib,json,resource,shutil,subprocess,sys,time
from pathlib import Path


def main(out):
    start=time.perf_counter();before=resource.getrusage(resource.RUSAGE_CHILDREN)
    root=Path(__file__).resolve().parent
    if out.exists(): raise SystemExit('output directory must not already exist')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for rec in manifest['files']:
        path=root/rec['path'];raw=path.read_bytes()
        if len(raw)!=rec['bytes'] or hashlib.sha256(raw).hexdigest()!=rec['sha256']:
            raise SystemExit('payload mismatch: '+rec['path'])
    out.mkdir(parents=True)
    work=out/'isolated';work.mkdir()
    for name in ('src','checks','witnesses'):
        shutil.copytree(root/name,work/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    (work/'results').mkdir()
    commands=[
        ['verify_separator_witnesses.py','--witnesses',str(work/'witnesses'),'--output',str(work/'results'/'separator_witness_independent.json')],
        ['check_separator_forest.py','--output',str(work/'results'/'separator_forest_checks.json')],
        ['check_tw2_local_design.py','--output',str(work/'results'/'tw2_local_design_check.json')],
        ['check_finite_palette.py'],['check_border_decoder_constant.py']]
    records=[]
    for args in commands:
        t=time.perf_counter()
        cmd=[sys.executable,str(work/'checks'/args[0]),*args[1:]]
        p=subprocess.run(cmd,cwd=work,capture_output=True,text=True,timeout=60)
        (out/(args[0]+'.stdout.txt')).write_text(p.stdout)
        (out/(args[0]+'.stderr.txt')).write_text(p.stderr)
        records.append({'program':args[0],'returncode':p.returncode,'enclosing_wall_seconds':time.perf_counter()-t})
        if p.returncode:raise SystemExit('receiving check failed: '+args[0])
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    result={'status':'passed','checked_payload_files':len(manifest['files']),'checks':records,
            'wall_seconds':time.perf_counter()-start,
            'child_cpu_seconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
            'maximum_child_peak_rss_bytes':after.ru_maxrss*1024,
            'scope':'one relocated delivery replay, overlapping per-program timers; no producer or historical scientific replay'}
    (out/'RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output.resolve())
