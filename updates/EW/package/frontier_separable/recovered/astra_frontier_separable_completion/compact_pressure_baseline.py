"""Matched sparse compact-support Hodge certificates (not best possible solver).
Potential and triangle-current trial spaces are finite, but their exact bounds
refer to the same infinite graph. Every exterior residual is retained.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
from fractions import Fraction as F
import time,json,resource,sys
from pathlib import Path

def run(L):
    start=time.perf_counter();n=L+1
    vertices=[(a,b) for a in range(n) for b in range(n)];vi={v:i for i,v in enumerate(vertices)}
    edges=[(e,a,b) for e in range(3) for a in range(n+1) for b in range(n+1)];ei={e:i for i,e in enumerate(edges)}
    cr=[];cc=[];cv=[]
    for a,b in vertices:
        k=2*vi[a,b]
        for idx,sgn in [((0,a,b),1),((1,a,b),-1),((2,a,b),-1)]:
            cr.append(ei[idx]);cc.append(k);cv.append(sgn)
        for idx,sgn in [((0,a,b+1),1),((1,a+1,b),-1),((2,a,b),-1)]:
            cr.append(ei[idx]);cc.append(k+1);cv.append(sgn)
    C=sp.coo_matrix((np.array(cv,np.int64),(cr,cc)),shape=(len(edges),2*len(vertices))).tocsr()
    gr=[];gc=[];gv=[]
    for i,(e,a,b) in enumerate(edges):
        u,v=([(a,b),(a+1,b)] if e==0 else [(a,b),(a,b+1)] if e==1 else [(a,b+1),(a+1,b)])
        for node,s in [(u,1),(v,-1)]:
            if node in vi:gr.append(i);gc.append(vi[node]);gv.append(s)
    G=sp.coo_matrix((np.array(gv,np.int64),(gr,gc)),shape=(len(edges),len(vertices))).tocsr()
    assert (C.T@G).nnz==0
    source=np.zeros(len(vertices));source[vi[0,1]]=1;source[vi[1,0]]=-1
    w0=np.zeros(len(edges));w0[ei[2,0,0]]=1
    phi=spla.spsolve((G.T@G).astype(float).tocsc(),source)
    psi=spla.spsolve((C.T@C).astype(float).tocsc(),-(C.T@w0))
    Q=2**44;x=np.rint(phi*Q).astype(np.int64);y=np.rint(psi*Q).astype(np.int64)
    dg=G@x;flow=C@y;flow[ei[2,0,0]]+=Q
    lo=F(2*Q*(int(x[vi[0,1]])-int(x[vi[1,0]]))-sum(int(a)**2 for a in dg),Q*Q)
    hi=F(sum(int(a)**2 for a in flow),Q*Q)
    gap=hi-lo;res=flow-dg
    assert gap==F(sum(int(a)**2 for a in res),Q*Q)
    return dict(cutoff=L,potential_variables=len(vertices),cycle_variables=2*len(vertices),
       lower=str(lo),upper=str(hi),width=float(gap),seconds=time.perf_counter()-start,
       peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       scope='exact infinite-graph bounds from compact trial fields; sparse direct baseline')
if __name__=='__main__':
    if len(sys.argv)>1:
        out=run(int(sys.argv[1]));print(json.dumps(out));
    else:
        rows=[]
        for L in(8,16,32,64,128):
            out=run(L);rows.append(out);print(json.dumps(out),flush=True)
        Path('compact_pressure_baseline.json').write_text(json.dumps(rows,indent=2))
