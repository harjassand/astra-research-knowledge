"""Constructive Shapira lower bounds from exact local divergence constraints.

rho=1/2 and c=1+alpha*eta[-1]*eta[2]. A local bond flow is
q=(eta[0]-eta[1])*h(outside spins). Translation-covariance divergence vanishes
iff the Walsh coefficients of q sum to zero in every translation orbit.
These constraints form an incidence matrix. A spanning-forest correction turns
floating candidate coefficients into exactly feasible rational flows.
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


def canonical(points):
    z=min(points)
    return tuple(sorted(x-z for x in points))


def solve(r,alpha=1,bits=80):
    start=time.perf_counter()
    outside=list(range(-r,0))+list(range(2,r+2));dim=1<<len(outside)
    vertices={};edges=[]
    def vertex(s):
        if s not in vertices:vertices[s]=len(vertices)
        return vertices[s]
    for e in range(dim):
        S={outside[i] for i in range(len(outside)) if e>>i&1}
        u=vertex(canonical(S|{0}));v=vertex(canonical(S|{1}))
        edges.append((u,v))
    nv=len(vertices)
    adj=[[] for _ in range(nv)]
    cr=[];cc=[];cv=[]
    for e,(u,v) in enumerate(edges):
        if u==v:continue
        cr.extend((u,v));cc.extend((e,e));cv.extend((1,-1))
        adj[u].append((v,e,1));adj[v].append((u,e,-1))
    C=sp.csr_matrix((np.array(cv,dtype=np.int64),(cr,cc)),shape=(nv,dim))
    # A forest certifies an independent set of constraints and later removes all
    # coefficient-rounding error while preserving an exactly local flow.
    seen=set();keep=[];post=[];roots=[]
    for root in range(nv):
        if root in seen:continue
        roots.append(root);seen.add(root);stack=[root]
        while stack:
            u=stack.pop()
            for v,e,sign_u in adj[u]:
                if v in seen:continue
                seen.add(v);keep.append(v);stack.append(v)
                post.append((v,u,e,-sign_u))
    left=1<<outside.index(-1);right=1<<outside.index(2)
    masks=[0,left,right,left^right]
    coefs=[4+alpha,alpha,alpha,alpha]
    ar=np.repeat(np.arange(dim),4);ac=np.array([i^m for i in range(dim) for m in masks])
    av=np.tile(np.array(coefs,dtype=np.int64),dim)
    T=sp.csr_matrix((av,(ar,ac)),shape=(dim,dim)) # 4 times multiplication by c
    Ck=C[keep,:]
    H=(Ck@T@Ck.T).tocsc()
    b=np.asarray((Ck@T[:,0]).toarray()).ravel()
    lam=splu(H.astype(float)).solve(b.astype(float)) if len(keep) else np.zeros(0)
    z=np.zeros(dim);z[0]=1
    z-=np.asarray(Ck.T@lam).ravel()
    x=np.asarray(T@z).ravel()/4
    scale=1<<bits;xn=[round(float(w)*scale) for w in x]
    residual=[0]*nv
    for e,(u,v) in enumerate(edges):residual[u]+=xn[e];residual[v]-=xn[e]
    proposal_violation=max(map(abs,residual))
    for v,u,e,sign_v in reversed(post):
        delta=-sign_v*residual[v]
        xn[e]+=delta;residual[u]+=residual[v];residual[v]=0
    assert all(z==0 for z in residual)
    check=[0]*nv
    for e,(u,v) in enumerate(edges):check[u]+=xn[e];check[v]-=xn[e]
    assert all(z==0 for z in check)
    # Multiplication by 1/c has denominator 4(1+alpha).
    den=4*(1+alpha)
    energy=sum(xn[e]*((4+3*alpha)*xn[e]-alpha*(xn[e^left]+xn[e^right]+xn[e^left^right])) for e in range(dim))
    assert energy>0
    lower=F(den*xn[0]*xn[0],energy)
    upper=F(4+alpha,4)
    assert lower<=upper
    return {"r":r,"flow_window_sites":2*r+2,"alpha":alpha,"density":"1/2",
            "flow_coefficients":dim,"divergence_orbits":nv,"independent_constraints":len(keep),
            "constraint_components":len(roots),"linear_system_nonzeros":int(H.nnz),
            "lower":float(lower),"lower_fraction":[str(lower.numerator),str(lower.denominator)],
            "proposal_divergence_max":float(F(proposal_violation,scale)),
            "certified_divergence":"exactly zero after integer forest correction",
            "seconds":time.perf_counter()-start,
            "status":"Exact infinite-volume rational lower via explicit local admissible flow"}


if __name__=="__main__":
    out=[]
    for alpha in [1,9]:
        for r in [1,2,3,4,5,6]:
            result=solve(r,alpha);out.append(result);print(json.dumps(result),flush=True)
            Path(__file__).with_name("exclusion_local_flow_results.json").write_text(json.dumps(out,indent=2)+"\n")
