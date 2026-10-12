"""Floating-point local curvature audit, not a rounding implementation.
Artificial stress states need not be reachable by the algorithm.
"""
from __future__ import annotations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq

records=[]
for k,n,seed in [(1,96,61),(1,112,72),(2,160,83),(2,176,94)]:
    rng=np.random.default_rng(seed)
    K=64*k; R=math.isqrt(K); eta=1/(K*n); beta=1/(2*R); H=32*R*R
    m=12
    x=rng.uniform(-.15,.15,n)
    if k==2: x-=x.mean()  # a uniform-base-polytope tangent
    large=np.full(n,.9)
    p=.003*(.91+.18*rng.random((m,n))) if k==1 else .001*(.91+.18*rng.random((m,n)))
    b=np.sqrt(p)*rng.choice([-1,1],(m,n))
    q=p.sum(axis=1)
    scale=np.full(m,float(R))
    for i in range(m):
        while (scale[i]/2)**2>=q[i]:scale[i]/=2
    assert np.all(q<=scale**2) and np.all(scale**2<4*q)
    assert np.all(p.max(axis=1)<=q/K)
    assert np.all(p.sum(axis=0)+large**2<=1)
    assert large@large>R*R
    G=(p*(1-x*x)).sum(axis=1)
    background=np.diag(large**2)+eta*np.ones((n,n))
    def state(t, point=x):
        uplus=np.full(m,t); uplus[0]=-.1
        d=H+scale*(uplus-R*G/(2*scale**2)-12*R)
        uminus=(-d-H)/scale+R*G/(2*scale**2)+12*R
        u=np.concatenate([uplus,uminus])
        pp=np.concatenate([p,p]); bb=np.concatenate([b,-b]); rr=np.tile(scale,2)
        gg=bb/rr[:,None]-R*pp*x/(rr*rr)[:,None]
        ww=32*K*np.exp(beta*u)/rr**4
        M=background+(pp.T*ww)@pp
        return M,pp,gg,ww,rr,d,u
    def f(t):return np.linalg.eigvalsh(state(t)[0])[-1]-8.5
    assert f(-2000)<0<f(0)
    t=brentq(f,-2000,0,xtol=1e-12)
    M,pp,g,w,rr,d,u=state(t)
    ev,V=np.linalg.eigh(M); L=ev[-1]; v=V[:,-1]
    if v.sum()<0:v=-v
    s=pp@v
    U=(g.T*(w*beta*beta*s*s))@g
    Ddiag=(w*beta*R*s*s/(rr*rr))@pp
    D=np.diag(Ddiag)
    T=(pp.T*(w*beta*s))@g
    gradL=g.T@(w*beta*s*s)
    resolvent=(V[:,:-1]/(L-ev[:-1]))@V[:,:-1].T
    hessL=U-D+2*T.T@resolvent@T
    hessPhi=6*(L-8)*np.outer(gradL,gradL)+3*(L-8)**2*hessL-2*eta*np.eye(n)
    gradPhi=3*(L-8)**2*gradL-2*eta*x
    constraints=[large,rng.normal(size=n),gradPhi]
    if k==2:constraints.append(np.ones(n))
    constraints.extend(g[u>=-1])
    Z=null_space(np.array(constraints))
    small=Z.T@hessPhi@Z
    vals,Q=np.linalg.eigh(small)
    h=Z@Q[:,0]
    expected=float(h@hessPhi@h)
    def phi(a):
        xx=x+a*h
        dd=d+a*(b@h)
        GG=(p*(1-xx*xx)).sum(axis=1)
        uu=np.concatenate([(dd-H)/scale+R*GG/(2*scale**2)+12*R,
                           (-dd-H)/scale+R*GG/(2*scale**2)+12*R])
        ww=32*K*np.exp(beta*uu)/rr**4
        MM=background+(pp.T*ww)@pp
        LL=np.linalg.eigvalsh(MM)[-1]
        return max(LL-8,0)**3-eta*(xx@xx)
    dt=1e-3
    fd=(-phi(2*dt)+16*phi(dt)-30*phi(0)+16*phi(-dt)-phi(-2*dt))/(12*dt*dt)
    gap=L-ev[-2]
    diag_margin=float(np.max(np.diag(U)-2/R**2*Ddiag))
    assert gap>=eta-1e-11
    assert diag_margin<=1e-12
    assert expected<=-2*eta+1e-9
    assert abs(fd-expected)<2e-6
    records.append(dict(k=k,n=n,seed=seed,L=L,protected_pairs=int((u>=-1).sum()),
        gap=gap,required_gap=eta,diagonal_comparison_max_residual=diag_margin,
        residual_dimension=int(Z.shape[1]),curvature=expected,required_curvature=-2*eta,
        fourth_order_difference=fd,absolute_difference=abs(fd-expected)))
out=dict(status='Artificial floating-point local states; not reachable-state certification or a full algorithm run.',
         number_of_cases=len(records),all_passed=True,cases=records)
Path(__file__).with_name('spectral_audit_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
