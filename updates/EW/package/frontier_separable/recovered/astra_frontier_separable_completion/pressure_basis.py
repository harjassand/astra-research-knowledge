"""Infinite-domain separated pressure Galerkin solver. Discovery is floating.
Coordinates are gaps between three ordered particles; no grid is constructed.
Exact certification is in pressure_certificate.py.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
from fractions import Fraction as F
from functools import lru_cache
import numpy as np
import scipy.linalg as la
import time

def geo(q,a=0):
    q=F(q)
    if not -1<q<1 or a<0: raise ValueError('Unstable ratio or negative offset')
    return int(a),q

def val(s,x):
    a,q=s
    return F(0) if x<a else q**(x-a)

@lru_cache(None)
def ip(u,v):
    a,q=u; b,r=v; k=max(a,b)
    return q**(k-a)*r**(k-b)/(1-q*r)

@lru_cache(None)
def ip_forward(u,v):
    b,r=v
    return ip(u,(b-1,r)) if b else r*ip(u,v)

def build_unis(L,K):
    return [geo(0,j) for j in range(L)]+[geo(1-F(1,2**k),L) for k in range(K+1)]

def pairs(n,anti):
    return [(i,j) for i in range(n) for j in range(i+(1 if anti else 0),n)]

def terms(ij,anti):
    i,j=ij
    return [(1,i,j)] if i==j else [(1,i,j),(-1 if anti else 1,j,i)]

def matrices(unis,exact=False):
    B=[[ip(u,v) for v in unis] for u in unis]
    P=[[ip_forward(u,v) for v in unis] for u in unis]
    s=[val(u,0) for u in unis]; s1=[val(u,1) for u in unis]
    if exact: return B,P,s,s1
    return tuple(np.array(v,dtype=float) for v in (B,P,s,s1))

def make_gram(B,P,s,s1,exact=False):
    n=len(s); pp=pairs(n,True); cp=[(ij,t) for ij in pairs(n,False) for t in(0,1)]
    def pot(i,j,k,l):
        bik=B[i][k]; bjl=B[j][l]
        gik=bik-s[i]*s[k]; gjl=bjl-s[j]*s[l]
        aik=bik-P[i][k]-P[k][i]+gik
        ajl=bjl-P[j][l]-P[l][j]+gjl
        return aik*bjl+bik*ajl+bik*gjl+gik*bjl-P[i][k]*P[l][j]-P[k][i]*P[j][l]
    def cyc(i,j,k,l,t,T):
        b=B[i][k]*B[j][l]
        if t==T: return 3*b
        if t==0: return b+B[i][k]*P[l][j]+P[k][i]*B[j][l]
        return b+B[i][k]*P[j][l]+P[i][k]*B[j][l]
    G=[[sum(c*C*pot(i,j,k,l) for c,i,j in terms(a,True) for C,k,l in terms(b,True)) for b in pp] for a in pp]
    H=[[sum(c*C*cyc(i,j,k,l,t,T) for c,i,j in terms(a,False) for C,k,l in terms(b,False)) for b,T in cp] for a,t in cp]
    rhs=[sum(c*(s[i]*s1[j]-s1[i]*s[j]) for c,i,j in terms(a,True)) for a in pp]
    vb=[-sum(c*s[i]*s[j] for c,i,j in terms(a,False)) for a,t in cp]
    if exact: return G,H,rhs,vb,pp,cp
    return np.array(G),np.array(H),np.array(rhs),np.array(vb),pp,cp

def solve(G,b,rcond=1e-13):
    sc=np.sqrt(np.diag(G)); H=G/sc[:,None]/sc[None,:]; rhs=b/sc
    vals,vecs=la.eigh(H); use=vals>max(vals[-1]*rcond,1e-16)
    return (vecs[:,use]@((vecs[:,use].T@rhs)/vals[use]))/sc,int(use.sum()),float(vals[0])

def run(L,K):
    start=time.perf_counter(); unis=build_unis(L,K)
    G,H,rhs,vb,pp,cp=make_gram(*matrices(unis))
    x,rr,ev=solve(G,rhs); y,rr2,ev2=solve(H,-vb)
    lo=2*rhs@x-x@G@x; hi=1+2*vb@y+y@H@y
    out=dict(L=L,K=K,lower=float(lo),upper=float(hi),width=float(hi-lo),
      n_lower=len(x),n_upper=len(y),rank_lower=rr,rank_upper=rr2,
      seconds=time.perf_counter()-start,min_eig_lower=ev,min_eig_upper=ev2)
    return out,x,y
