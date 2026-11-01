"""Arita/Varadhan--Spohn local Ritz upper bounds for a nongradient exclusion gas.

Infinite one-dimensional chain, density rho=1/2,
c_(i,i+1)=1+alpha*eta_(i-1)*eta_(i+2), positive integer alpha.
No finite physical ring is substituted. Local Bernoulli expectations are exact
Walsh products. Every corrector shape up to span R is included modulo translation.
Floating sparse LU proposes coefficients; the evaluated upper bound is rational.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path
import time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu


def build(R, alpha):
    offset=R-1
    def mask(points):
        return sum(1<<(x+offset) for x in points)
    shapes=[tuple(i for i in range(R) if s>>i&1) for s in range(1,1<<R,2) if s.bit_count()>=2]
    derivatives=[]
    rows=defaultdict(dict)
    for col,S in enumerate(shapes):
        g=defaultdict(int)
        for shift in {v-i for v in (0,1) for i in S}:
            translated={i+shift for i in S}
            if (0 in translated)==(1 in translated):continue
            old=mask(translated);new=old^mask((0,1))
            g[new]+=1;g[old]-=1
        g={k:v for k,v in g.items() if v}
        derivatives.append(g)
        for k,v in g.items(): rows[k][col]=v
    # Four times the rate polynomial; w.r.t. s_i=2eta_i-1.
    rate={0:4+alpha,mask((-1,)):alpha,mask((2,)):alpha,mask((-1,2)):alpha}
    gram=defaultdict(int)
    for T,c in rate.items():
        for k,rr in rows.items():
            ss=rows.get(k^T)
            if ss is None:continue
            for i,a in rr.items():
                for j,b in ss.items():gram[i,j]+=c*a*b
    entries={k:v for k,v in gram.items() if v}
    row,col,val=zip(*[(i,j,v) for (i,j),v in entries.items()])
    Gnum=sp.csc_matrix((np.array(val,dtype=np.int64),(row,col)),shape=(len(shapes),len(shapes)))
    bnum=np.zeros(len(shapes),dtype=np.int64)
    for T,c in rate.items():
        for H,sign in [(mask((0,)),1),(mask((1,)),-1)]:
            for j,v in rows.get(T^H,{}).items():bnum[j]+=c*sign*v
    return shapes,Gnum,bnum


def solve(R,alpha=1,bits=80):
    start=time.perf_counter();shapes,G,b=build(R,alpha);scale=1<<bits
    if np.any(b):
        lu=splu(G.astype(float))
        # G_actual=G/2, b_actual=b/4; minimizer=-G_actual^-1 b_actual.
        x=-.5*lu.solve(b.astype(float))
    else:x=np.zeros(len(shapes))
    xn=[round(float(v)*scale) for v in x]
    quadratic=0
    for j in range(len(shapes)):
        for at in range(G.indptr[j],G.indptr[j+1]):
            i=int(G.indices[at]);quadratic+=xn[i]*int(G.data[at])*xn[j]
    linear=sum(int(z)*w for z,w in zip(b,xn))
    upper=F((4+alpha)*scale*scale+2*scale*linear+2*quadratic,4*scale*scale)
    # Known two-dimensional gradient-flow lower, calculated without target inverse.
    p=F(1,2)
    g00=F(3,4)+F(1,4*(1+alpha));g01=F(1,2)+F(1,2*(1+alpha));g11=F(1,2)+F(1,1+alpha)
    det=g00*g11-g01*g01
    lower=(g11-2*g01+g00)/det
    assert lower<=upper<=F(4+alpha,4)
    return {"R":R,"alpha":alpha,"density":"1/2","corrector_orbits":len(shapes),
            "gram_nonzeros":int(G.nnz),"upper":float(upper),
            "upper_fraction":[str(upper.numerator),str(upper.denominator)],
            "gradient_flow_lower":float(lower),"relative_width":float((upper-lower)/lower),
            "seconds":time.perf_counter()-start,
            "status":"Exact infinite-volume rational upper from finite local trial; float LU only proposes coefficients"}


if __name__=="__main__":
    out=[]
    for alpha in [1,9]:
        for R in [2,3,4,5,6,7,8,9,10,11,12]:
            r=solve(R,alpha);out.append(r);print(json.dumps(r),flush=True)
            Path(__file__).with_name("exclusion_local_ritz_results.json").write_text(json.dumps(out,indent=2)+"\n")
