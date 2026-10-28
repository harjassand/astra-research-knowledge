#!/usr/bin/env python3
"""Actual smooth periodic gradient fields; finite numerical acquisition only.

Three Fourier modes k1,k2,k1+k2 on an arbitrary parallelogram cell.
The overall field amplitude is eliminated analytically: negative Jensen
requires P3^2/(4 P2 P4)>1. Every reported field is curl-free by construction.
No absence claim follows from a finite search.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import minimize

HERE=Path(__file__).resolve().parent
grid=np.arange(16)*2*np.pi/16
y1,y2=np.meshgrid(grid,grid,indexing='ij')
COS=np.stack([np.cos(y1).ravel(),np.cos(y2).ravel(),np.cos(y1+y2).ravel()],axis=1)

def coefficients(z,A,kappa,L):
    u=np.asarray(z[:6]).reshape(3,2)
    phi,angle,logr=z[6:]
    k1=np.array([np.cos(phi),np.sin(phi)])
    k2=np.exp(logr)*np.array([np.cos(phi+angle),np.sin(phi+angle)])
    waves=np.stack([k1,k2,k1+k2])
    G=np.einsum('ni,ij,ik->njk',COS,u,waves)
    a,b,c,d=(G[:,i,j] for i,j in [(0,0),(0,1),(1,0),(1,1)])
    aa,bb,cc,dd=A.ravel()
    TA=np.sum(A*A);qA=np.linalg.det(A);xA=aa*aa+cc*cc-bb*bb-dd*dd
    Tl=2*(aa*a+bb*b+cc*c+dd*d);Tg=a*a+b*b+c*c+d*d
    ql=dd*a-cc*b-bb*c+aa*d;qg=a*d-b*c
    xl=2*(aa*a+cc*c-bb*b-dd*d);xg=a*a+c*c-b*b-d*d
    P2=np.mean(Tl*Tl+2*TA*Tg+kappa*(ql*ql+2*qA*qg)+L*(qA*xg+ql*xl+qg*xA))
    P3=np.mean(2*Tl*Tg+2*kappa*ql*qg+L*(ql*xg+qg*xl))
    P4=np.mean(Tg*Tg+kappa*qg*qg+L*qg*xg)
    return P2,P3,P4

def objective(z,A,kappa,L):
    p2,p3,p4=coefficients(z,A,kappa,L)
    if p2.real<=0 or p4.real<=0:return np.array(1e6,dtype=z.dtype)
    return -p3*p3/(4*p2*p4)

def derivative(z,A,kappa,L):
    ans=[]
    for i in range(len(z)):
        zz=np.array(z,dtype=complex);zz[i]+=1e-24j
        ans.append(objective(zz,A,kappa,L).imag/1e-24)
    return np.array(ans)

def run():
    start=time.perf_counter();rng=np.random.default_rng(128742)
    controls=[('norm4',np.eye(2),0.,0.),
              ('main99',np.diag([36.,35.])/np.sqrt(2521),252/25,99/25),
              ('family197',np.eye(2),12.,4*(197**2-1)/(197**2+1))]
    rows=[];bounds=[(-1,1)]*6+[(-np.pi,np.pi),(.025,np.pi-.025),(-2.5,2.5)]
    for label,A,kappa,L in controls:
        best=None;attempts=[]
        for j in range(64):
            u=rng.normal(size=6);u/=np.linalg.norm(u)
            z=np.r_[u,rng.uniform(-np.pi,np.pi),rng.uniform(.1,np.pi-.1),rng.uniform(-2,2)]
            fit=minimize(objective,z,args=(A,kappa,L),jac=derivative,method='L-BFGS-B',bounds=bounds,
                options={'maxiter':500,'ftol':1e-13,'gtol':1e-9,'maxls':40})
            attempts.append({'ratio':float(-fit.fun),'iterations':int(fit.nit),'success':bool(fit.success)})
            if best is None or fit.fun<best.fun:best=fit
        p2,p3,p4=coefficients(best.x,A,kappa,L)
        row={'label':label,'scope':'FINITE_NUMERICAL_SEARCH_ONLY','A':A.tolist(),'kappa':kappa,'L':L,
             'best_ratio':float(-best.fun),'parameters':best.x.tolist(),
             'P2_P3_P4':list(map(float,[p2,p3,p4])),'attempts':attempts,
             'elapsed_seconds':time.perf_counter()-start}
        rows.append(row);print(json.dumps({k:row[k] for k in ['label','best_ratio','P2_P3_P4','elapsed_seconds']}),flush=True)
        (HERE/'TRIAD_SEARCH.json').write_text(json.dumps({'records':rows,'elapsed_seconds':time.perf_counter()-start},indent=2)+'\n')

if __name__=='__main__':run()
