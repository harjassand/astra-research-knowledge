import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from completion import CompletionSampler
from feature_gibbs import run_feature_gibbs
import numpy as np,time,json,platform
from pathlib import Path

def fixture(n,d,seed,mode,beta=100.):
    rng=np.random.default_rng(seed)
    x=(np.arange(n)+.35+rng.uniform(-.15,.15,n))/n
    if mode=='local':y=(x+rng.uniform(-.35,.35,n)/n)%1
    elif mode=='irregular':y=(x[rng.permutation(n)]+rng.uniform(-.12,.12,n)/n)%1
    else: raise ValueError(mode)
    sites=np.column_stack([x,y]).ravel(); rows=[np.ones(2*n)]; k=1
    while len(rows)<d:
        attenuation=np.exp(-.0003*(2*np.pi*k)**2)
        rows.append(np.sqrt(2)*attenuation*np.cos(2*np.pi*k*sites))
        if len(rows)<d:rows.append(np.sqrt(2)*attenuation*np.sin(2*np.pi*k*sites))
        k+=1
    return np.ascontiguousarray(np.sqrt(beta/n)*np.array(rows).T)

def ess(x):
    x=np.asarray(x,float); x=x-x.mean(); n=len(x)
    if np.dot(x,x)==0:return 0.
    m=1<<(2*n-1).bit_length(); f=np.fft.rfft(x,m)
    ac=np.fft.irfft(f*f.conj(),m)[:n]
    ac/=np.arange(n,0,-1); ac/=ac[0]
    tau=1.
    for i in range(1,min(n-1,2000),2):
        pair=ac[i]+ac[i+1]
        if pair<=0:break
        tau+=2*pair
    return float(n/max(1.,tau))

X=fixture(8,4,123,'local')
t=time.perf_counter(); o=CompletionSampler(X,np.repeat(np.arange(8),2)); o.sample(10,2)
run_feature_gibbs(X,10,8,80,1)
jit=time.perf_counter()-t
rows=[]; metadata=[]
for n,d,mode in [(32,8,'irregular'),(64,16,'local'),(64,16,'irregular'),(128,16,'irregular')]:
    X=fixture(n,d,314,mode); groups=np.repeat(np.arange(n),2)
    t=time.perf_counter(); obj=CompletionSampler(X,groups); prep=time.perf_counter()-t
    print('case',n,d,mode,'C',obj.collision_sum,flush=True)
    np.savez_compressed(f'results/instance_n{n}_d{d}_{mode}.npz',X=X,groups=groups)
    for seed in [81,82,83,84,85]:
        t=time.perf_counter(); s,diag=obj.sample(5000,seed,max_trials=2000000); sec=time.perf_counter()-t
        bits=s%2
        row=dict(n=n,d=d,mode=mode,seed=seed,method='completion',seconds=sec+prep,
                 preprocessing_seconds=prep,ess_bit0=ess(bits[:,0]),
                 ess_mean_choices=ess(bits.mean(axis=1)),mean_bit0=float(bits[:,0].mean()),
                 mean_choice=float(bits.mean()),**diag)
        rows.append(row)
        # One whole sweep per recorded sample, plus 20 burn-in sweeps (charged).
        t=time.perf_counter(); s,updates,ac,rf=run_feature_gibbs(X,5000,n,20*n,seed)
        secs=time.perf_counter()-t
        row=dict(n=n,d=d,mode=mode,seed=seed,method='rank_update_gibbs',seconds=secs,
                 samples=len(s),updates=updates,inverse_rebuilds=rf,ess_bit0=ess(s[:,0]),
                 ess_mean_choices=ess(s.mean(axis=1)),mean_bit0=float(s[:,0].mean()),mean_choice=float(s.mean()))
        rows.append(row)
    print('completed',n,d,mode,flush=True)
meta=dict(python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),
          initial_jit_seconds=jit,thread_environment='OPENBLAS_NUM_THREADS=1',
          samples_per_run=5000,seeds=[81,82,83,84,85],
          caveats=['Model-based Fourier diffusion fixtures, not experimental measurements',
            'Gibbs ESS is an estimated autocorrelation diagnostic, not a rigorous accuracy certificate',
            'No formal floating-point error enclosure in the fast sampler',
            'One machine, no GPU, no cross-hardware performance claims'])
Path('results/scaling.json').write_text(json.dumps(dict(metadata=meta,runs=rows),indent=2))
for case in [(32,8,'irregular'),(64,16,'local'),(64,16,'irregular'),(128,16,'irregular')]:
 for method in ['completion','rank_update_gibbs']:
    rs=[r for r in rows if (r['n'],r['d'],r['mode'])==case and r['method']==method]
    print(case,method,'median_seconds',np.median([r['seconds'] for r in rs]),
          'median_ESSbit',np.median([r['ess_bit0'] for r in rs]),
          'median_ESSmean',np.median([r['ess_mean_choices'] for r in rs]),flush=True)
