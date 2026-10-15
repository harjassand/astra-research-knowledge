"""Independent clock-with-deletions construction; author fixtures unchanged.
Upstream files are read as reference only. All routines here are independent.
"""
import sys,time,json,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.stats import kstest,ks_2samp
ROOT=Path(__file__).resolve().parent

def clock(th,f0,temp,rng=None,E=None,avalanche=True):
    th=np.asarray(th); n=len(th); F=n*f0
    if E is None:
        E=rng.exponential(size=n)*np.exp(th/temp)
    alive=np.ones(n,dtype=bool); k=n; s=0.; t=0.; a=0; q=0
    strength_order=np.argsort(th,kind='stable'); time_order=np.argsort(E,kind='stable')
    events=[]
    def close(k,a):
        if not avalanche:return k,a
        while a<n:
            i=strength_order[a]
            if not alive[i]:a+=1;continue
            if th[i]>F/k:break
            alive[i]=False;k-=1;a+=1
            if k==0:break
        return k,a
    k,a=close(k,a);events.append((0.,k,-1))
    while k:
        while not alive[time_order[q]]:q+=1
        i=time_order[q];q+=1
        ds=E[i]-s
        assert ds>=0
        t+=ds*np.exp(-F/(k*temp));s=E[i]
        alive[i]=False;k-=1
        if k:k,a=close(k,a)
        events.append((float(t),k,int(i)))
    return t,events

def naive_clock(th,f0,temp,E):
    # Independent O(n^2) residual hazard implementation for pathwise comparison.
    th=np.asarray(th); ids=np.arange(len(th)); F=len(th)*f0
    remaining=E.copy();t=0.;events=[]
    def close(ids,remaining):
        while len(ids):
            keep=th[ids]>F/len(ids)
            if keep.all():break
            ids=ids[keep];remaining=remaining[keep]
        return ids,remaining
    ids,remaining=close(ids,remaining);events.append((0.,len(ids),-1))
    while len(ids):
        j=np.argmin(remaining);ds=remaining[j];t+=ds*np.exp(-F/(len(ids)*temp));i=ids[j]
        remaining-=ds
        ids=np.delete(ids,j);remaining=np.delete(remaining,j)
        ids,remaining=close(ids,remaining);events.append((float(t),len(ids),int(i)))
    return t,events

def independent_Q(th,f0,temp):
    n=len(th);F=n*f0
    def closure(ids):
        while ids:
            new=tuple(i for i in ids if th[i]>F/len(ids))
            if new==ids:return ids
            ids=new
        return ()
    initial=closure(tuple(range(n)))
    states=[initial];idx={initial:0};edges=[]
    for st in states:
        ee=[]
        if st:
            for i in st:
                target=closure(tuple(j for j in st if j!=i))
                if target not in idx:idx[target]=len(states);states.append(target)
                ee.append((idx[target],float(np.exp((F/len(st)-th[i])/temp))))
        edges.append(ee)
    Q=np.zeros((len(states),len(states)))
    for r,ee in enumerate(edges):
        for c,v in ee:Q[r,c]+=v;Q[r,r]-=v
    return Q,states,idx

def gillespie(th,f0,temp,rng):
    h=np.array(th,copy=True);F=len(h)*f0;t=0.
    while len(h):
        keep=h>F/len(h)
        if not keep.all():h=h[keep];continue
        rates=np.exp((F/len(h)-h)/temp);total=rates.sum()
        t+=rng.exponential()/total
        chosen=rng.choice(len(h),p=rates/total)
        h=np.delete(h,chosen)
    return t

def run():
    out={'kind':'computational verification only; no fitted experimental rates','sources':{
      'paper':'https://arxiv.org/abs/2508.13367','code':'https://github.com/ComplexityBiosystems/fiber-bundle','data':'https://doi.org/10.5281/zenodo.16413747'}}
    rng=np.random.default_rng(20261015)
    # Author's exact unit-test fixture, fig2.py test_cond_heterog_lifetime.
    th=np.sort(np.random.RandomState(0).rand(5));f0=.125;temp=.05
    Q,states,idx=independent_Q(th,f0,temp)
    grid=np.array([1,5,10,25,50,100,200,500,1000.])
    exact=np.array([expm(Q*x)[0,idx[()]] for x in grid])
    N=50000
    start=time.perf_counter();samples=np.array([clock(th,f0,temp,rng)[0] for _ in range(N)]);elapsed=time.perf_counter()-start
    emp=np.array([(samples<=x).mean() for x in grid])
    # Avoid N expensive exponentials: use exact CDF at independent fixed grid,
    # DKW simultaneous 99% bound holds for all x, hence this grid too.
    dkw=float(np.sqrt(np.log(200)/(2*N)))
    ref_rng=np.random.default_rng(910000)
    src=np.array([gillespie(th,f0,temp,ref_rng) for j in range(10000)])
    noav=np.array([clock(th,f0,temp,rng,avalanche=False)[0] for _ in range(N)])
    out['author_fixture']={'thresholds':th.tolist(),'f0':f0,'temperature':temp,'reachable_states_including_absorption':len(states),'grid':grid.tolist(),'exact_cdf':exact.tolist(),'clock_empirical_cdf':emp.tolist(),'max_grid_error':float(np.max(abs(emp-exact))),'DKW_99_bound':dkw,'samples':N,'seconds':elapsed,'clock_mean':float(samples.mean()),'independent_gillespie_mean':float(src.mean()),'two_sample_KS':dict(zip(['statistic','pvalue'],map(float,ks_2samp(samples,src)))),'without_avalanche_mean':float(noav.mean()),'without_avalanche_cdf':[(noav<=x).mean().item() for x in grid]}
    # Pathwise comparisons using independently maintained residual clocks.
    maxerr=0.;cases=0
    for n in [2,3,5,10,50,400]:
      for f in [.125,.15,.175]:
       for T in [.05,.1,.15]:
        for rep in range(20):
         h=np.sort(rng.uniform(size=n)); E=rng.exponential(size=n)*np.exp(h/T)
         t,e=clock(h,f,T,E=E);u,z=naive_clock(h,f,T,E)
         assert [(x[1],x[2]) for x in e]==[(x[1],x[2]) for x in z]
         err=abs(t-u)/max(1,abs(t));maxerr=max(maxerr,err);assert err<1e-12;cases+=1
    # Equality survives nowhere; initial overload can destroy all at t=0.
    boundary=[]
    for h,f in [([.25,.5],.25),([.5,.5],.5),([1.,1.],.25),([.1,.8,1.2],.2)]:
      t,e=clock(h,f,.15,E=np.arange(1,len(h)+1,dtype=float));boundary.append({'h':h,'f0':f,'time':t,'events':e})
    out['pathwise']={'cases':cases,'max_relative_error':maxerr,'boundary_cases':boundary}
    # Larger n: computational speed check at author's published default parameters.
    scaling=[]
    for n in [100,1000,10000,100000]:
      h=np.sort(rng.uniform(size=n)); E=rng.exponential(size=n)*np.exp(h/.1)
      a=time.perf_counter(); t,e=clock(h,.15,.1,E=E);dt=time.perf_counter()-a
      scaling.append({'n':n,'seconds':dt,'thermal_events':len(e)-1,'tau':t})
    out['scaling']=scaling
    out['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'upstream').glob('*') if p.is_file()}
    (ROOT/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':run()
