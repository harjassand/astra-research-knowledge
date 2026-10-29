"""Acquire richer COARSE residence histogram by paid SAME-stream replay.
It is not a second independent statistical sample. No extra microstate
readout is needed relative to a continuous total-coverage trace.
"""
import hashlib,json,subprocess,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent


def main():
    tic=time.perf_counter()
    subprocess.run(['/usr/bin/clang++','-O3','-std=c++17','native_log_hist.cpp','-o','native_log_hist'],cwd=HERE,check=True,capture_output=True)
    comp=time.perf_counter()-tic
    c=['./native_log_hist','NATIVE_INPUT.txt','BASELINE_HIST.csv','20000','2026102902','1','1']
    z=subprocess.run(c,cwd=HERE,check=True,capture_output=True,text=True)
    r=json.loads(z.stdout)
    old=np.genfromtxt(HERE/'BASELINE.csv',delimiter=',',names=True)
    new=np.genfromtxt(HERE/'BASELINE_HIST.csv',delimiter=',',names=True)
    for n in old.dtype.names:assert np.array_equal(old[n],new[n]),n
    H=np.column_stack([new[f'Tv{v}'] for v in range(33)])
    assert np.max(abs(H.sum(axis=1)-r['horizon_seconds']))<1e-18
    assert np.max(abs(H@np.arange(33)-new['Ivac']))<1e-17
    out=dict(status='PASS; original11 fields bit-identical for all20000 SAME trajectories',
       compile_seconds=comp,execution=r,new_independent_episodes=0,
       native_events_replayed=r['native_events'],
       source_sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest()
                      for n in ['native_log_hist.cpp','BASELINE_HIST.csv','BASELINE.csv']},
       scope='histogram from coarse total-vacancy trace; exact activity AO2 remains reserved for richer-access comparator')
    (HERE/'COARSE_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
