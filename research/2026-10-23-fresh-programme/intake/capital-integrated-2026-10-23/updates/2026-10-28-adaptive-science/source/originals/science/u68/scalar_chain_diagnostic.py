"""Galerkin diagnostic of the actual scalar full-source correction.

Uses analysis-level K and h' for h(x)=lambda*cos(x). Those are not runtime
oracles for the universal problem. Gaussian quadrature is diagnostic, not
a certified continuous-law TV computation.
"""
import json
import math
from pathlib import Path
import numpy as np


def hermites(x, degree):
    out=np.zeros((len(x),degree+1))
    out[:,0]=1
    if degree: out[:,1]=x
    for n in range(1,degree):
        out[:,n+1]=(x*out[:,n]-math.sqrt(n)*out[:,n-1])/math.sqrt(n+1)
    return out


def run(lam,degree=64,levels=10):
    nodes,weights=np.polynomial.hermite_e.hermegauss(180)
    weights=weights/math.sqrt(2*math.pi)
    hg=hermites(nodes,degree)
    z,zw=np.polynomial.hermite_e.hermegauss(90)
    zw=zw/math.sqrt(2*math.pi)
    hz=hermites(z,levels+2)
    pts,pw=np.polynomial.legendre.leggauss(160)
    rho=(pts+1)/2
    K=-lam*np.sum(pw[None,:]*.5*np.sin(nodes[:,None]*rho[None,:])*
        np.exp(-.5*(1-rho*rho))[None,:],axis=1)
    Dh=-lam*np.sin(nodes)
    a=K-Dh
    raw=K*Dh
    rq=hg.T@(weights*raw)
    u=np.zeros((len(nodes),len(z)))
    dug=np.zeros_like(u); duz=np.zeros_like(u)
    jz=np.zeros_like(u)
    rows=[]
    for q in range(levels+1):
        inv=rq/(np.arange(degree+1)+q+2)
        dinv=np.zeros(degree+1)
        dinv[:-1]=inv[1:]*np.sqrt(np.arange(1,degree+1))
        f=hg@inv
        df=hg@dinv
        rv=hg@rq
        uq=-math.sqrt(q+1)*f
        ug=-math.sqrt(q+1)*df
        uz=-(q+1)*f
        jj=-rv+(q+1)*f
        u+=uq[:,None]*hz[:,q+1][None,:]
        dug+=ug[:,None]*hz[:,q+1][None,:]
        duz+=uz[:,None]*hz[:,q][None,:]
        jz+=jj[:,None]*hz[:,q][None,:]
        linear=raw[:,None]+a[:,None]*dug+duz+jz
        nonlinear=-dug*dug+jz*duz
        jointw=weights[:,None]*zw[None,:]
        y=lam*np.cos(nodes)[:,None]+z[None,:]+u
        mean=float(np.sum(jointw*y))
        var=float(np.sum(jointw*(y-mean)**2))
        rows.append(dict(q=q, r_coefficient_l2=float(np.linalg.norm(rq)),
            linear_residual_l2=math.sqrt(float(np.sum(jointw*linear*linear))),
            quadratic_residual_l2=math.sqrt(float(np.sum(jointw*nonlinear*nonlinear))),
            full_residual_l2=math.sqrt(float(np.sum(jointw*(linear+nonlinear)**2))),
            output_mean_error=mean-lam*math.exp(-.5), output_variance=var))
        next_values=-math.sqrt(q+1)*a*df
        next_coeff=hg.T@(weights*next_values)
        rq=next_coeff
    return dict(lam=lam,degree=degree,levels=levels,
        max_abs_K_minus_Dh=float(np.max(np.abs(a))),
        rows=rows,
        scope='Analysis-level quadrature/Galerkin diagnostics; no TV certification or query claim')


def main():
    out=[run(lam) for lam in (.03,.06,.12,.2)]
    # A resolution check is included only as a finite stability diagnostic.
    out.append(run(.12,degree=80,levels=10))
    path=Path(__file__).with_name('scalar_chain_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    for case in out:
        print(json.dumps({k:v for k,v in case.items() if k!='rows'}))
        print(json.dumps(case['rows'][-1]))


if __name__=='__main__': main()
