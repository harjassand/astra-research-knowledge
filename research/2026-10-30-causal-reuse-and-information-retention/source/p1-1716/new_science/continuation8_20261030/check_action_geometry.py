#!/usr/bin/env python3
"""Finite algebra and quadrature checks, not a microscopic LDP test."""
from pathlib import Path
import hashlib, json, platform
import numpy as np

def action_check(alpha):
    nx,nt=512,513
    s,m,v,T=1.3,.31,.4,1.7
    x=np.arange(nx)/nx; t=np.linspace(0,T,nt)
    amp=.14*(1-np.cos(np.pi*t/T))/2
    ap=.14*np.pi*np.sin(np.pi*t/T)/(2*T)
    phase=2*np.pi*(x[None,:]-v*t[:,None])
    rho=m+amp[:,None]*np.sin(phase)
    rx=amp[:,None]*2*np.pi*np.cos(phase)
    j0=v*amp[:,None]*np.sin(phase)+ap[:,None]/(2*np.pi)*np.cos(phase)
    chi=rho*(1-rho); C=chi.mean(axis=1); a0=j0+(s/2)*rx
    A=(1/chi).mean(axis=1); BB=(a0/chi).mean(axis=1)
    beta=alpha**2/(1-alpha**2); q=-BB/(A+beta/C); a=a0+q[:,None]
    E=a/(s*chi)+(beta*q/(s*C))[:,None]
    ME=s*chi*(E-alpha**2*(chi*E).mean(axis=1)[:,None]/C[:,None])
    primal=np.trapezoid(((a*a/chi).mean(axis=1)+beta*q*q/C)/(2*s),t)
    dual=np.trapezoid((E*a).mean(axis=1)-.5*(E*ME).mean(axis=1),t)
    contraction=np.trapezoid(((a0*a0/chi).mean(axis=1)-BB*BB/(A+beta/C))/(2*s),t)
    ordinary=np.trapezoid(((a0*a0/chi).mean(axis=1)-BB*BB/A)/(2*s),t)
    nz=64; ii=np.linspace(0,nx-1,nz,dtype=int); it=nt//2
    ch=chi[it,ii]; aa=a[it,ii]; cc=ch.mean()
    mat=s*(np.diag(ch)-alpha**2*np.outer(ch,ch)/(nz*cc))
    direct=np.linalg.solve(mat,aa); formula=aa/(s*ch)+beta*aa.mean()/(s*cc)
    assert abs(primal-dual)<1e-12 and abs(primal-contraction)<1e-12
    assert np.max(np.abs(direct-formula))<1e-11
    assert np.max(np.abs(ME-a))<1e-12 and primal>=ordinary-1e-12
    return dict(alpha=alpha,density_action=primal,ordinary_density_action=ordinary,
                density_cost_increase=primal-ordinary,primal_dual_error=abs(primal-dual),
                dense_inverse_error=float(np.max(np.abs(direct-formula))),
                maximum_optimal_circulation=float(np.max(np.abs(q))),
                spatial_points=nx,time_points=nt)

def paired_check(n,R):
    s=1.3; C=np.zeros((n,n))
    for r in range(1,R+1):
        for b in range(n):
            vv=np.zeros(n); vv[b]=1; vv[(b+r)%n]=-1
            C+=s*(n-1)/(2*n*R)*np.outer(vv,vv)
    B=np.zeros((n,n))
    for b in range(n): B[b,b]=-1; B[(b+1)%n,b]=1
    k=2*np.pi/n; wave=np.exp(1j*k*np.arange(n))
    lam=.5*abs(1-np.exp(1j*k))**2*s*(n-1)/(2*n*R)*sum(
        abs(1-np.exp(1j*k*r))**2 for r in range(1,R+1))
    residual=float(np.max(np.abs(.5*B@C@B.T@wave-lam*wave)))
    assert residual<1e-12 and np.max(np.abs(C@np.ones(n)))<1e-12
    out=dict(sites=n,range=R,fundamental_decay=lam,
             fundamental_relaxation_time=1/lam,mode_residual=residual)
    if R==n-1:
        out['full_density_generator_error']=float(np.max(np.abs(B@C@B.T-s*B@B.T)))
        assert out['full_density_generator_error']<1e-12
    return out

def main():
    out={'scope':'Analytic action/linear-bath checks; no acquisition, finite-N error certificate, or proof by simulation.',
         'python':platform.python_version(),'numpy':np.__version__,
         'action':[action_check(a) for a in (0.,.6,.9)],
         'paired':[paired_check(n,r) for n in (32,64,128) for r in (1,4,n-1)]}
    out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=Path(__file__).with_name('ACTION_GEOMETRY_CHECK.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'action':out['action'],'paired_cases':len(out['paired']),'output':str(path)},indent=2))

if __name__=='__main__': main()
