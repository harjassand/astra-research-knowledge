"""Strong source-aware tail-window baseline; no full-chain state enumeration.
Only its explicitly charged local window of 2**w states is enumerated.
"""
from fractions import Fraction as F
from time import perf_counter
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
import numpy as np,json,sys

def solve_window(w,k,eps,root,verify=True):
    t=perf_counter();q=F(1,k*k+1);ef=F(eps)
    root={'min':ef,'max':F(1),'average':ef+(1-ef)*q}[root]
    N=2**w; rows=[];cols=[];data=[];rationalrows=[]
    for x in range(N):
        rr=[];diag=F(0)
        for i in range(w):
            a=root if i==0 else (F(1) if x&(1<<(i-1)) else ef)
            rate=(1-q if x&(1<<i) else q)*a
            rr.append((x^(1<<i),-rate));diag+=rate
        diag+=q*(F(1) if x&(1<<(w-1)) else ef)
        rr.append((x,diag));rationalrows.append(rr)
        for y,r in rr:rows.append(x);cols.append(y);data.append(float(r))
    A=coo_matrix((data,(rows,cols)),shape=(N,N)).tocsr()
    v=spsolve(A,np.ones(N))
    source=np.array([float(q**x.bit_count()*(1-q)**(w-x.bit_count())) for x in range(N)])
    value=float(source@v)
    res={'width':w,'states':N,'root':str(root),'estimate':value,'solve_seconds':perf_counter()-t}
    if verify:
        vf=[F.from_float(float(vv)) for vv in v]
        delta=max(abs(sum(a*vf[y] for y,a in rr)-1) for rr in rationalrows)
        assert delta<1 and min(v)>0
        val=sum(q**x.bit_count()*(1-q)**(w-x.bit_count())*vf[x] for x in range(N))
        lo=val/(1+delta);hi=val/(1-delta)
        res.update({'lower':float(lo),'upper':float(hi),'delta':float(delta),'exact_residual':True})
    res['total_seconds']=perf_counter()-t
    return res

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=5);p.add_argument('--eps',default='0.0001');p.add_argument('--widths',default='4,6,8,10');p.add_argument('--out',default='window_results.json')
    a=p.parse_args();out=[]
    for w in map(int,a.widths.split(',')):
        low=solve_window(w,a.k,a.eps,'average');up=solve_window(w,a.k,a.eps,'min')
        row={'w':w,'k':a.k,'eps':a.eps,'lower':low,'upper':up,'ratio':up['upper']/low['lower']};out.append(row);print(json.dumps(row),flush=True)
    open(a.out,'w').write(json.dumps(out,indent=2))
