"""Positive Cole-Hopf receiver at diffusive times, with natural-scale score.
Exact model formulas; numerical sampling uses numpy vonmises and truncated wrapped
Gaussian sums (not certified finite-bit coins). No claim of new Cole-Hopf method.
"""
import json,time
import numpy as np
from scipy.integrate import quad
from scipy.special import i0e

NU=1/12;GAMMA=np.sqrt(2)/4
T=np.log(2)/2 # NU * k^2 * (6 log 2/k^2)

def kernel(theta):
    z=(theta+np.pi)%(2*np.pi)-np.pi
    d=z[...,None]+2*np.pi*np.arange(-5,6)
    terms=np.exp(-d*d/(4*T))/np.sqrt(4*np.pi*T)
    value=terms.sum(axis=-1)
    slope=(-d/(2*T)*terms).sum(axis=-1)
    return value,slope/value

def draw(A,y,N,rng):
    out=[];attempts=0
    kmax=kernel(np.array(0.))[0]
    while sum(map(len,out))<N:
        batch=max(256,int((N-sum(map(len,out)))*8))
        theta=rng.vonmises(-np.pi/2,A,batch)
        kval,_=kernel(theta-y)
        accepted=theta[rng.random(batch)<kval/kmax]
        out.append(accepted);attempts+=batch
    return np.concatenate(out)[:N],attempts

def baseline(A,y):
    # Adaptive ordinary quadrature in centered von-Mises coordinates; same inputs.
    # e^[-A(1+sin theta)] avoids overflow and presents the same peak.
    # split around known peak, with width1/sqrt(A); exact full integral retained.
    def f(z):
        th=-np.pi/2+z
        w=np.exp(-A*(1-np.cos(z)))
        kval,score=kernel(np.array(th-y))
        return w*kval,w*kval*score
    cuts=sorted(set([-np.pi,np.pi,0]+[max(-np.pi,min(np.pi,s*4/np.sqrt(max(A,1)))) for s in [-1,1]]))
    den=sum(quad(lambda z:f(z)[0],l,r,epsabs=1e-12)[0] for l,r in zip(cuts,cuts[1:]))
    num=sum(quad(lambda z:f(z)[1],l,r,epsabs=1e-12)[0] for l,r in zip(cuts,cuts[1:]))
    return 2*NU/GAMMA*num/den

rng=np.random.default_rng(20261029);rows=[]
for A in [.1,1,10,100,1000,10000]:
    y=.25;N=20000;t0=time.perf_counter();theta,attempts=draw(A,y,N,rng)
    _,score=kernel(theta-y)
    natural_score=2*NU/GAMMA*score
    # u/k = delta/k E cos(theta); delta/k=2NU A/GAMMA.
    natural_direct=2*NU*A/GAMMA*np.cos(theta)
    base=baseline(A,y)
    rows.append({'A':A,'accepted':N,'generated_proposals':attempts,'score_u_over_k':float(natural_score.mean()),'score_standard_error':float(natural_score.std(ddof=1)/np.sqrt(N)),'direct_u_over_k':float(natural_direct.mean()),'direct_standard_error':float(natural_direct.std(ddof=1)/np.sqrt(N)),'ordinary_adaptive_quadrature':float(base),'wall_seconds':time.perf_counter()-t0})
print(json.dumps({'T':T,'nu':NU,'gamma':GAMMA,'fixed_query_y':.25,'rows':rows},indent=2))
