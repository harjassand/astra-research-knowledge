"""Acquisition runner. Public records and private simulation audit are separated.
Sets no information oracle on learner. All-probe simulation, not hardware or an
execution of terminal entangled payload / exact finite theorem certificates.
"""
import argparse, hashlib, json, os, platform, time
from pathlib import Path
import numpy as np
import scipy
from learner import Learner
from ordinary_comparator import OrdinaryComparator
from simulator import RetainedSource
from quantum_math import D,compile_decoder

class FiniteCoins:
    def __init__(self,seed): self.rng=np.random.default_rng(seed);self.bits=0
    def draw(self,n,cap=32):
        width=(n-1).bit_length();draws=[]
        for _ in range(cap):
            value=int(self.rng.integers(0,2**width));self.bits+=width;draws.append(value)
            if value<n: return value,draws
        raise RuntimeError('finite private sampler exhausted')
    def sign(self):
        b=int(self.rng.integers(0,2));self.bits+=1;return 2*b-1

def dump(path,obj):
    path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def jsonline(handle,obj):
    handle.write(json.dumps(obj,allow_nan=False)+'\n');handle.flush()

def run_one(out,n,seed,algorithm):
    directory=out/f'{algorithm}_N{n}_seed{seed}';directory.mkdir(parents=True,exist_ok=False)
    source=RetainedSource(100000+seed)
    coins=FiniteCoins(seed)
    learner=Learner() if algorithm=='bandit' else OrdinaryComparator()
    start=time.perf_counter();failures=[]
    with (directory/'public_records.jsonl').open('w') as records:
        for t in range(1,n+1):
            try:
                if algorithm=='bandit':
                    i,itries=coins.draw(D);z=coins.sign()
                    played,diag=learner.act(i,z)
                    stamp=time.perf_counter();ks,comp=compile_decoder(played)
                    diag['decoder_matrix_compilation_seconds']=time.perf_counter()-stamp
                    diag.update(comp)
                    j,jtries=coins.draw(3);s=coins.sign()
                    stamp=time.perf_counter();y=source.probe(ks,j,s)
                    diag['source_simulation_seconds']=time.perf_counter()-stamp
                    update=learner.observe(y)
                    record={'t':t,'i':i,'i_rejection_draws':itries,'z':z,
                            'j':j,'j_rejection_draws':jtries,'s':s,'y':y,
                            'diagnostics':diag,'update':update}
                    if not update['prox_success']: failures.append({'t':t,'failure':update['failure']})
                else:
                    stamp=time.perf_counter();decoder,diag=learner.decoder()
                    diag['decoder_svd_seconds']=time.perf_counter()-stamp
                    j,jtries=coins.draw(3);s=coins.sign();m,mtries=coins.draw(3)
                    stamp=time.perf_counter();b=source.probe_pauli(j,s,m)
                    diag['source_simulation_seconds']=time.perf_counter()-stamp
                    stamp=time.perf_counter();learner.observe(j,s,m,b)
                    diag['update_seconds']=time.perf_counter()-stamp
                    record={'t':t,'j':j,'j_rejection_draws':jtries,'s':s,
                            'm':m,'m_rejection_draws':mtries,'b':b,'diagnostics':diag}
                jsonline(records,record)
            except Exception as exc:
                failures.append({'t':t,'failure':repr(exc),'source_calls_at_failure':source.calls})
                break # never erase/restart a failed source trajectory
    runtime=time.perf_counter()-start
    with (directory/'private_source_audit.jsonl').open('w') as audit:
        for row in source.audit:jsonline(audit,row)
    dump(directory/'failures.json',failures)
    metadata={'algorithm':algorithm,'requested_N':n,'seed':seed,'source_seed':100000+seed,
              'private_rng_bits_consumed':coins.bits,'private_sampler_trial_cap':32,
              'total_acquisition_wall_seconds':runtime,'failure_count':len(failures),
              'gamma':1.,'epsilon':.25,'eta':1/(64*D*D),'delta':.25/(64*64*D*D),
              'expected_theorem_horizon_N':8388608,
              'terminal_payload_executed':False,'hardware_executed':False,
              'exact_rational_certification_executed':False,'plant':source.metadata(),
              'numpy':np.__version__,'scipy':scipy.__version__,'python':platform.python_version(),
              'platform':platform.platform(),'thread_environment':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
              'finished_unix_time':time.time()}
    # §5: least power of 2 >=512 D² k ceil(log2(16/epsilon))/(gamma epsilon)
    threshold=512*D*D*4*int(np.ceil(np.log2(16/.25)))/.25
    metadata['theorem_horizon_lower_threshold']=threshold
    metadata['expected_theorem_horizon_N']=2**int(np.ceil(np.log2(threshold)))
    dump(directory/'metadata.json',metadata)
    print(directory.name,'calls',source.calls,'seconds',round(runtime,3),'failures',len(failures),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=Path('runs'))
    parser.add_argument('--n',nargs='+',type=int,default=[128,512]);parser.add_argument('--seeds',nargs='+',type=int,default=[17,31,47,73])
    parser.add_argument('--algorithms',nargs='+',default=['bandit','ordinary'])
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    for n in args.n:
        for seed in args.seeds:
            for algorithm in args.algorithms:run_one(args.out,n,seed,algorithm)
