"""Exact separated prescribed-divergence completion on gap orthants.
No multidimensional grid or Poisson matrix is allocated. Each univariate field
is a finite sum of shifted geometric tails q^(g-a) 1_(g>=a), |q|<1.
This prototype explicitly expands finite prefix windows, so their lengths count.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
from fractions import Fraction as F
from collections import defaultdict
from functools import lru_cache
from itertools import product
from pressure_basis import geo,ip,val
import json,time,random

def clean(v):return {k:F(c) for k,c in v.items() if c}
def add(*args):
    out=defaultdict(F)
    for scale,v in args:
        for k,c in v.items():out[k]+=scale*c
    return clean(out)
def tensor_value(v,g):
    return sum(c*product_f(val(s,x) for s,x in zip(key,g)) for key,c in v.items())
def product_f(v):
    r=F(1)
    for a in v:r*=a
    return r

def inner(v,w):
    return sum(c*C*product_f(ip(s,t) for s,t in zip(key,Key)) for key,c in v.items() for Key,C in w.items())

def mass(v):return sum(c*product_f(1/(1-q) for a,q in key) for key,c in v.items())

def forward(s):
    a,q=s
    return {geo(q,a-1):F(1)} if a else ({s:q} if q else {})
def back(s):return geo(s[1],s[0]+1)

def shifted(v,axis):
    return {tuple(back(s) if i==axis else s for i,s in enumerate(key)):c for key,c in v.items()}

def divergence(flows):
    out=defaultdict(F)
    for i,v in enumerate(flows):
        for key,c in v.items():
            out[key]+=c
            target=tuple(back(s) if j==i else s for j,s in enumerate(key));out[target]-=c
    return clean(out)

def prefix_zero_mass(u,rho=geo(0)):
    """Prefix of u - mass(u)*rho/mass(rho). rho must start at zero."""
    a,q=u;b,r=rho
    if b:raise ValueError('Reference must start at zero')
    m=1/(1-q);out=defaultdict(F)
    # m*r^(x+1)-m*1_[0,a)-m*q*q^(x-a)1_(x>=a)
    if r:out[geo(r)]+=m*r
    for j in range(a):out[geo(0,j)]-=m
    if q:out[geo(q,a)]-=m*q
    return clean(out)

def complete(b,rhos=None):
    if not b:return []
    dim=len(next(iter(b)))
    if any(len(k)!=dim for k in b):raise ValueError('Mixed tensor dimensions')
    if mass(b):raise ValueError('Source is not mean zero')
    rhos=rhos or [geo(0)]*dim
    if len(rhos)!=dim or any(a for a,q in rhos):raise ValueError('Bad references')
    out=[defaultdict(F) for _ in range(dim)]
    for key,c in b.items():
        means=[1/(1-q) for a,q in key]
        for i in range(dim):
            # product left u, right means*normalized rho, middle primitive
            scale=c*product_f(means[j]*(1-rhos[j][1]) for j in range(i+1,dim))
            for p,pcoef in prefix_zero_mass(key[i],rhos[i]).items():
                target=key[:i]+(p,)+tuple(rhos[j] for j in range(i+1,dim))
                out[i][target]+=scale*pcoef
    return list(map(clean,out))

def route_edges(flows):
    """Return labels (move left of particle j, source gap shifted by e_(j-1)).
    Payload retains the UNshifted base coordinate g. This permits a direct
    symbolic quantum lift: insert a zero gap at position j and two singles.
    """
    m=len(flows);out=[{} for _ in range(m)]
    for j in range(m):out[j]=add(*[(1,flows[i]) for i in range(j,m)])
    return out

def routed_divergence(routes):
    out=defaultdict(F)
    for j,v in enumerate(routes):
        for key,c in v.items():
            src=key if j==0 else tuple(back(s) if i==j-1 else s for i,s in enumerate(key))
            dst=tuple(back(s) if i==j else s for i,s in enumerate(key))
            out[src]+=c;out[dst]-=c
    return clean(out)

def tests():
    start=time.perf_counter();rng=random.Random(261013)
    counts=dict(prefix=0,divergence=0,routing=0,pointwise=0,large_extent=0)
    for _ in range(30):
        u=geo(F(rng.randint(-3,3),4),rng.randrange(5));rho=geo(F(rng.randrange(4),4))
        v=prefix_zero_mass(u,rho);m=1/(1-u[1])
        for x in range(15):
            delta=sum(c*val(s,x) for s,c in v.items())-sum(c*val(s,x-1) for s,c in v.items())
            assert delta==val(u,x)-m*(1-rho[1])*val(rho,x)
        counts['prefix']+=1
    for dim in range(1,6):
        for it in range(3):
            key=tuple(geo(F(rng.randint(-2,3),4),rng.randrange(3)) for i in range(dim))
            b={key:F(1),tuple(geo(0) for i in range(dim)):-product_f(1/(1-q) for a,q in key)}
            b=clean(b);rhos=[geo(F(1,2))]*dim if it%2 else None
            flows=complete(b,rhos);res=add((1,divergence(flows)),(-1,b))
            assert inner(res,res)==0;counts['divergence']+=1
            routes=route_edges(flows);res=add((1,routed_divergence(routes)),(-1,b))
            assert inner(res,res)==0;counts['routing']+=1
            for g in [tuple(rng.randrange(10) for _ in range(dim)) for _ in range(5)]:
                assert tensor_value(res,g)==0;counts['pointwise']+=1
    # Extremely long tails: the representation has no radius cutoff.
    dim=4;q=1-F(1,2**40);key=(geo(q),)*dim
    b={key:(1-q)**dim,(geo(0),)*dim:F(-1)}
    flows=complete(b);routes=route_edges(flows)
    res=add((1,routed_divergence(routes)),(-1,b));assert inner(res,res)==0
    norm=sum(inner(v,v) for v in routes)
    counts['large_extent']=1
    out=dict(counts=counts,seconds=time.perf_counter()-start,
       long_tail_ratio=str(q),long_tail_length_scale=2**40,
       long_tail_source_atoms=len(b),long_tail_grid_atoms=sum(map(len,flows)),
       long_tail_routed_atoms=sum(map(len,routes)),long_tail_norm2=str(norm),
       status='exact rational identities; no multidimensional enumeration')
    return out
if __name__=='__main__':
    from pathlib import Path
    out=tests();Path('separable_repair_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
