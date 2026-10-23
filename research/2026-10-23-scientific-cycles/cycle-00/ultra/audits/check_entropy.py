import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['VECLIB_MAXIMUM_THREADS']='1'
import numpy as np
from scipy.optimize import minimize
import time,resource,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
start=time.perf_counter(); cpu=time.process_time(); rng=np.random.default_rng(20261021)
records=[]; witnesses={}

def calc(c,N):
    ac=np.zeros_like(c)
    for i in range(1,N+1):
        # First i coordinates are the leading axes in C-order.
        av=c.reshape(2**i,-1).mean(axis=0)
        ac+=np.tile(av,2**i)
    q=c*c; mask=q>0
    H=-float(np.sum(q[mask]*np.log(q[mask])))
    energy=float(c@ac)
    return np.log(2)*energy-H,H,energy,ac

def obj(v,N):
    norm=np.linalg.norm(v);c=v/norm
    F,H,energy,ac=calc(c,N)
    g=2*np.log(2)*ac+2*c*(np.log(np.maximum(c*c,1e-300))+1)
    grad=(g-c*np.dot(c,g))/norm
    return -F,-grad

for N in range(1,9):
    n=2**N
    starts=[np.r_[1.,np.full(n-1,1e-5)],np.ones(n),
            np.arange(1,n+1,dtype=float)**(-.5),
            np.arange(1,n+1,dtype=float)**(-1.)]
    starts.extend(np.exp(rng.normal(0,s,n)) for s in [1,2,4,8])
    best=None;trials=[]
    for k,v in enumerate(starts):
        if time.process_time()-cpu>48:break
        v=v/np.linalg.norm(v)
        fit=minimize(obj,v,args=(N,),jac=True,method='L-BFGS-B',bounds=[(1e-13,None)]*n,
                     options={'maxiter':1500,'ftol':1e-13,'gtol':1e-9,'maxls':50})
        c=fit.x/np.linalg.norm(fit.x)
        F,H,energy,_=calc(c,N)
        trials.append({'start':k,'F':F,'success':bool(fit.success),'message':str(fit.message),
                       'iterations':int(fit.nit),'grad_inf':float(np.max(np.abs(obj(fit.x,N)[1])))})
        if best is None or F>best['F']:
            best={'F':F,'H':H,'sum_projection_norm_sq':energy,'start':k};witnesses[f'N{N}']=c
    records.append({'N':N,'D':2,'best':best,'trials':trials})
    print(json.dumps(records[-1]),flush=True)
np.savez(ROOT/'witnesses.npz',**witnesses)
result={'scope':'Heuristic maximization only; no certified global bound or asymptotic inference.',
        'seed':20261021,'records':records,'wall_seconds':time.perf_counter()-start,
        'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'versions':{'numpy':np.__version__},'limits':{'cpu_seconds':60,'peak_rss_bytes':400*1024*1024}}
(ROOT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
