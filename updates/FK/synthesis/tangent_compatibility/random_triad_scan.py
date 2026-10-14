#!/usr/bin/env python3
"""Bounded exploratory scan of compatible anisotropic tangent triads.

Every tested field is a sum of three exact periodic rank-one Fourier modes
with k1+k2=k3.  The first-order covariance tilt is balanced to zero.  This is
not an optimizer over all gradients and cannot establish a lower bound.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import minimize

from exact_tangent_triad import G, a, b, c, d, gradG, hessG

variables=(a,b,c,d)
grad_num=sp.lambdify(variables,gradG,"numpy")
hess_num=sp.lambdify(variables,hessG,"numpy")
G_num=sp.lambdify(variables,G,"numpy")


def rank_one(alpha,beta):
    return np.outer([np.cos(alpha),np.sin(alpha)],[np.cos(beta),np.sin(beta)]).reshape(4)


def fit_line(C):
    def obj(z):
        r=rank_one(*z)
        return -r@C@r
    starts=[(aa,bb) for aa in (-.08,0,.08) for bb in (np.pi/2-.08,np.pi/2,np.pi/2+.08)]
    best=None
    for x0 in starts:
        v=minimize(obj,np.array(x0),method="BFGS",options={"gtol":1e-10,"maxiter":300})
        if best is None or v.fun<best.fun: best=v
    return rank_one(*best.x),best.x,float(-best.fun)


def complete(A):
    A=A/np.linalg.norm(A)
    out=[A]
    for e in np.eye(4):
        v=e-A*(A@e)
        for u in out[1:]: v-=u*(u@v)
        n=np.linalg.norm(v)
        if n>1e-9: out.append(v/n)
        if len(out)==4: break
    return np.column_stack(out)


def make_field(N, modes, phases, rhos, rho_phases, ngrid=64):
    eps=1/N
    xx=np.arange(ngrid)[:,None]/ngrid
    yy=np.arange(ngrid)[None,:]/ngrid
    x=[np.zeros((ngrid,ngrid)) for _ in range(4)]
    for (p,q,amp),phi,rho,psi in zip(modes,phases,rhos,rho_phases):
        theta=2*np.pi*(p*xx+q*yy)
        s=amp*np.cos(theta+phi)
        res=eps**2*rho*np.cos(theta+psi)
        ratio=p/q
        aa=eps*ratio*s
        dd=1.5*aa+res
        cc=eps*ratio*dd
        for j,val in enumerate((aa,s,cc,dd)): x[j]+=val
    return x


def analyze(N,modes,phases,rhos,rho_phases):
    x=make_field(N,modes,phases,rhos,rho_phases)
    X=np.stack(x); M=X.shape[1]*X.shape[2]
    C=np.einsum('ixy,jxy->ij',X,X)/M
    R,angles,fitval=fit_line(C)
    s=np.einsum('i,ixy->xy',R,X)
    Y=X-R[:,None,None]*s[None,:,:]
    m2=np.mean(s**2);m3=np.mean(s**3);m4=np.mean(s**4)
    y2=np.mean(np.sum(Y**2,axis=0));y4=np.mean(np.sum(Y**2,axis=0)**2)
    delta=max(np.sqrt(y2/m2),(y4/m4)**.25)
    vals=[z.ravel() for z in X]
    grad=np.asarray(grad_num(*vals),float)
    Hess=np.asarray(hess_num(*vals),float)
    bv=grad.mean(axis=1); H=Hess.mean(axis=2)
    MR=np.asarray(hess_num(*[np.asarray([v]) for v in R]),float)[:,:,0]
    ev,U=np.linalg.eigh(MR); A=U[:,0]
    if A@np.array([1.,0.,0.,1.])<0:A=-A
    Q=complete(A); Hb=Q.T@H@Q
    ell=bv-(m3/(3*m2))*H@R
    eb=Q.T@ell;k=Hb[1:,0];D=Hb[1:,1:]
    h=Hb[0,0]; hs=h-k@np.linalg.solve(D,k)
    rs=eb[0]-k@np.linalg.solve(D,eb[1:])
    mineig=np.linalg.eigvalsh(H)[0]
    if mineig>1e-13: gap=float(np.mean(G_num(*vals))-.5*bv@np.linalg.solve(H,bv))
    else: gap=None
    ratio=float(rs*rs/(hs*m4*delta*delta)) if hs>1e-14 else None
    return {"ratio":ratio,"gap":gap,"delta":float(delta),"hstar":float(hs),
            "rstar":float(rs),"hstar_over_h":float(hs/h),"min_eigen_H":float(mineig),
            "fit_angles":list(map(float,angles)),"R":R.tolist(),"fit_value":float(fitval)}


def main():
    rng=np.random.default_rng(20261014)
    N=32
    rows=[]
    # A bounded design: 12 integer resonance triples, 4 amplitude balances,
    # 8 phase choices, and 8 residual choices, capped deterministically at 512.
    phaseset=[0,np.pi/4,np.pi/2,3*np.pi/4]
    for p1 in range(1,5):
      for p2 in range(-1,-6,-1):
        p3=p1+p2
        kappas=(float(p1),float(p2),float(p3)/2)
        if min(kappas)>=0 or max(kappas)<=0: continue
        for w2,w3 in ((1.,1.),(.5,1.),(2.,1.),(1.,2.)):
          w1=-(kappas[1]*w2+kappas[2]*w3)/kappas[0]
          if w1<=0 or w1>64: continue
          amps=(np.sqrt(w1),np.sqrt(w2),np.sqrt(w3))
          for phases in ((0.,0.,0.),(0.,0.,np.pi/2),(0.,np.pi/2,0.),(np.pi/4,0.,0.)):
            rhos=tuple(float(rng.choice([-2,-1,0,1,2])) for _ in range(3))
            rph=tuple(float(rng.choice(phaseset)) for _ in range(3))
            modes=((p1,1,amps[0]),(p2,1,amps[1]),(p3,2,amps[2]))
            item=analyze(N,modes,phases,rhos,rph)
            item.update({"p": [p1,p2,p3],"amplitudes":list(map(float,amps)),
                         "phases":list(phases),"rho":list(rhos),"rho_phases":list(rph)})
            rows.append(item)
            if len(rows)>=512: break
          if len(rows)>=512: break
        if len(rows)>=512: break
      if len(rows)>=512: break
    valid=[x for x in rows if x["ratio"] is not None]
    top=sorted(valid,key=lambda x:x["ratio"],reverse=True)[:10]
    min_gap=min((x["gap"] for x in valid if x["gap"] is not None),default=None)
    result={"scope":{"profiles_attempted":len(rows),"profiles_with_positive_hstar":len(valid),
                      "N":N,"grid":"64x64 exact trapezoidal average for quartic bandwidth",
                      "seed":20261014,"frequency_design":"k1=(p1,N), k2=(p2,N), k3=(p1+p2,2N)",
                      "covariance_balance":"sum_j (p_j/q_j) amplitude_j^2 = 0"},
            "largest_metric_ratios":top,"smallest_optimized_gap":min_gap}
    path=Path(__file__).with_name("random_triad_scan.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(path)


if __name__=="__main__":main()
