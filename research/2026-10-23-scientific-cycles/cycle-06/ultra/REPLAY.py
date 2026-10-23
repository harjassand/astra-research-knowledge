#!/usr/bin/env python3
"""Verify immutable payloads, then replay only Cycle6 jobs in disposable scratch."""
from pathlib import Path
import hashlib,json,math,os,shutil,subprocess,sys,tempfile,time,resource


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def stable(x):
    if isinstance(x,dict):
        return {k:stable(v) for k,v in x.items() if k not in
                ('measured_replay_cpu_seconds','measured_replay_wall_seconds')}
    if isinstance(x,list): return [stable(v) for v in x]
    return x


def same(a,b):
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12)
    if isinstance(a,dict) and isinstance(b,dict):
        return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())['payloads']
    for row in manifest:
        p=root/row['path']
        assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],row
    initial={p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
    wall=time.perf_counter(); before=resource.getrusage(resource.RUSAGE_CHILDREN)
    jobs=[]
    with tempfile.TemporaryDirectory(prefix='astra-cycle6-replay-') as td:
        target=Path(td)/'relocated'
        shutil.copytree(root,target)
        env=os.environ.copy()
        env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
        specs=[('calculations/queue/replay.py','calculations/queue/RESULT.json'),
               ('calculations/formation/formation_frontier.py','calculations/formation/RESULT.json'),
               ('calculations/clock/clock_repair_check.py','calculations/clock/CLOCK_RESULT.json')]
        for script,result in specs:
            t=time.perf_counter()
            completed=subprocess.run([sys.executable,str(target/script)],cwd=target,env=env,
                                     capture_output=True,text=True,timeout=60)
            assert completed.returncode==0,(script,completed.stdout,completed.stderr)
            observed=stable(json.loads((target/result).read_text()))
            expected=stable(json.loads((root/result).read_text()))
            assert same(expected,observed),result
            jobs.append(dict(script=script,status='PASS',wall_seconds=time.perf_counter()-t,
                             output=completed.stdout.strip(),result_reproduced=True))
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    final={p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
    assert final==initial,'Source modified by replay'
    print(json.dumps(dict(status='PASS',manifest_payloads=len(manifest),jobs=jobs,
          source_unchanged=True,wall_seconds=time.perf_counter()-wall,
          child_cpu_seconds=(after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime),
          scope='Only three new bounded Cycle6 jobs; no historical scientific campaigns or physical acquisition.'),indent=2))


if __name__=='__main__': main()
