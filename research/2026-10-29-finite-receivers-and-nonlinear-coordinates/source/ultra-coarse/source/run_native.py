"""One locked batch: one baseline acquisition + three fresh held-out controls.
No learned rates, adaptive target selection, long-run stationarity or lab data.
"""
import hashlib,json,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent


def main():
    tic=time.perf_counter()
    command=['/usr/bin/clang++','-O3','-std=c++17','native_log.cpp','-o','native_log']
    subprocess.run(command,cwd=HERE,check=True,capture_output=True)
    compile_seconds=time.perf_counter()-tic
    designs=[('BASELINE',1.,1.,2026102902),
             ('HELDOUT_080_090',.8,.9,2026102903),
             ('HELDOUT_090_080',.9,.8,2026102904),
             ('HELDOUT_080_080',.8,.8,2026102905)]
    records=[]
    for name,a,b,seed in designs:
        c=['./native_log','NATIVE_INPUT.txt',name+'.csv','20000',str(seed),str(a),str(b)]
        result=subprocess.run(c,cwd=HERE,check=True,capture_output=True,text=True)
        r=json.loads(result.stdout);r.update(name=name,seed=seed,
          data_sha256=hashlib.sha256((HERE/(name+'.csv')).read_bytes()).hexdigest())
        (HERE/(name+'.json')).write_text(json.dumps(r,indent=2)+'\n');records.append(r)
    cost=dict(compile_seconds=compile_seconds,records=records,
         total_episodes=sum(r['episodes'] for r in records),
         total_native_events=sum(r['native_events'] for r in records),
         total_condition_checks=sum(r['condition_checks'] for r in records),
         total_rng_words64=sum(r['rng_words64'] for r in records),
         total_model_exposure_seconds=sum(r['episodes']*r['horizon_seconds'] for r in records),
         total_sampling_write_seconds=sum(r['compute_and_write_seconds'] for r in records),
         source_sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest()
                        for n in ['native_log.cpp','NATIVE_INPUT.txt','MODEL.json']},
         sampling_contract='independent clean-start standard Gillespie model, binary64 and seeded mt19937_64 diagnostic; ideal-law confidence theorem is conditional, not formal bit-level/physical verification',
         scope='32-site periodic published-catalog instance; all new records are COMPUTATIONAL, not measured RuO2 trajectories')
    (HERE/'ACQUISITION.json').write_text(json.dumps(cost,indent=2)+'\n')
    print(json.dumps(cost,indent=2))


if __name__=='__main__':main()
