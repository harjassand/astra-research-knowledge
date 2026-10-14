"""Floating discovery only; exact reconstruction follows separately."""
import numpy as np
from scipy.special import roots_legendre
from fractions import Fraction
import json
from pathlib import Path
ROOT=Path(__file__).parent
A,B,C,E,L,M=107/24,3,19,-13,-29/2,-12
n,m=1,-1

def avg(p,q,r,s, norm=False):
    u2=p**4+q**4+4*p*p*q*q
    v2=n**4*r**4+m**4*s**4+4*n*n*m*m*r*r*s*s
    uv=(p*p+q*q)*(n*n*r*r+m*m*s*s)+2*n*m*r*s*p*q
    w2=(n*r*q-m*s*p)**2/2
    qu=n*r*p**3+m*s*q**3+2*m*s*p*p*q+2*n*r*p*q*q
    qv=n**3*r**3*p+m**3*s**3*q+2*m*n*n*r*r*s*q+2*n*m*m*s*s*r*p
    if norm: return u2+v2+2*uv
    return A*u2+B*v2+C*uv+E*w2+L*qu+M*qv

def edges(V,widths,eta):
    nodes,w=roots_legendre(3);t=(nodes+1)/2;w=w/2
    orig=np.repeat(np.arange(len(V)),len(V));dest=np.tile(np.arange(len(V)),len(V))
    d=V[dest]-V[orig]
    r=(V[orig,0,None]+d[:,0,None]*t);s=(V[orig,1,None]+d[:,1,None]*t)
    best=np.full(len(orig),np.inf);wi=np.zeros(len(orig),int);ce=np.zeros(len(orig));ne=np.zeros(len(orig))
    for h,tau in enumerate(widths):
        p=d[:,0,None]/tau;q=d[:,1,None]/tau
        c=tau*(avg(p,q,r,s)*w).sum(1);nn=tau*(avg(p,q,r,s,True)*w).sum(1)
        val=c-eta*nn;better=val<best
        best[better]=val[better];wi[better]=h;ce[better]=c[better];ne[better]=nn[better]
    return orig,dest,best,wi,ce,ne

def bellman(n,orig,dest,w):
    d=np.zeros(n)
    for it in range(n):
        nd=d.copy();np.minimum.at(nd,dest,d[orig]+w)
        if np.min(nd-d)>-1e-8:return d,it,False
        d=nd
    return d,n,True
for lim,step in [(2,.25),(2,.5),(1,.25)]:
    axis=np.arange(0,lim+1e-6,step);V=np.array([(x,y) for x in axis for y in axis])
    widths=[.125,.25,.5,1.,2.]
    for eta in [0.,.25,.5,1.]:
        i,j,w,wi,c,n4=edges(V,widths,eta)
        d,it,neg=bellman(len(V),i,j,w)
        slack=w-d[j]+d[i]
        print(lim,step,len(V),'eta',eta,'negative_edges',int(sum(w<-1e-7)), 'cycle?',neg,'min',w.min(),'its',it,'slackmin',slack.min(),flush=True)
        if lim==2 and step==.25 and eta==.25 and not neg:
            out={'n':n,'m':m,'eta':'1/4','vertices':V.tolist(),'widths':widths,'potentials_float':d.tolist(),'iterations':it,'negative_edges':int(sum(w<-1e-7))}
            (ROOT/'graph_opposite_discovery.json').write_text(json.dumps(out,indent=2))
