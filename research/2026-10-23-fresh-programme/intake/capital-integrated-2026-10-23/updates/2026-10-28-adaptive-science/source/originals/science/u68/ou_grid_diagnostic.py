"""Bounded-function OU-grid cross-check of the scalar chain.

Unlike unfiltered high-degree Galerkin projection, this keeps coefficient
functions bounded. Numerical interpolation/quadrature errors are not certified.
"""
import json
import math
from pathlib import Path
import numpy as np


def hermites(x,n):
    p=np.zeros((len(x),n+1));p[:,0]=1
    if n:p[:,1]=x
    for k in range(1,n):
        p[:,k+1]=(x*p[:,k]-math.sqrt(k)*p[:,k-1])/math.sqrt(k+1)
    return p


def run(lam,ngrid=1201,levels=7):
    grid=np.linspace(-24,24,ngrid)
    pts,pw=np.polynomial.legendre.leggauss(64)
    theta=(pts+1)*math.pi/4; tw=pw*math.pi/4
    t=np.cos(theta);s=np.sin(theta)
    z0,gw=np.polynomial.hermite_e.hermegauss(48)
    gw/=math.sqrt(2*math.pi)
    args=grid[:,None,None]*t[None,:,None]+s[None,:,None]*z0[None,None,:]
    rho=(pts+1)/2
    def kernel(x):
        return -lam*np.sum(.5*pw[None,:]*np.sin(x[:,None]*rho[None,:])*
                    np.exp(-.5*(1-rho*rho))[None,:],axis=1)
    K=kernel(grid);Dh=-lam*np.sin(grid);a=K-Dh
    rq=K*Dh
    G,W=np.polynomial.hermite_e.hermegauss(110);W/=math.sqrt(2*math.pi)
    Z,ZW=np.polynomial.hermite_e.hermegauss(90);ZW/=math.sqrt(2*math.pi)
    hz=hermites(Z,levels+2)
    kg=kernel(G);hg=-lam*np.sin(G);ag=kg-hg;r0=kg*hg
    u=np.zeros((len(G),len(Z)));ug=np.zeros_like(u)
    uz=np.zeros_like(u);jz=np.zeros_like(u)
    jointw=W[:,None]*ZW[None,:]
    rows=[]
    for q in range(levels+1):
        vals=np.interp(args.ravel(),grid,rq).reshape(args.shape)
        # The theta substitution removes the apparent 1/s singularity.
        f=np.sum(vals*(tw*t**(q+1)*s)[None,:,None]*gw[None,None,:],axis=(1,2))
        df=np.sum(vals*(tw*t**(q+2))[None,:,None]*(gw*z0)[None,None,:],axis=(1,2))
        fG=np.interp(G,grid,f);dfG=np.interp(G,grid,df)
        rG=np.interp(G,grid,rq)
        u+=(-math.sqrt(q+1)*fG)[:,None]*hz[:,q+1][None,:]
        ug+=(-math.sqrt(q+1)*dfG)[:,None]*hz[:,q+1][None,:]
        uz+=(-(q+1)*fG)[:,None]*hz[:,q][None,:]
        jz+=(-rG+(q+1)*fG)[:,None]*hz[:,q][None,:]
        lin=r0[:,None]+ag[:,None]*ug+uz+jz
        quadratic=-ug*ug+jz*uz
        y=lam*np.cos(G)[:,None]+Z[None,:]+u
        mean=float(np.sum(jointw*y))
        rows.append(dict(q=q, coefficient_sup=float(np.max(np.abs(rq))),
            linear_l2=math.sqrt(float(np.sum(jointw*lin*lin))),
            quadratic_l2=math.sqrt(float(np.sum(jointw*quadratic*quadratic))),
            DuG_l4=float(np.sum(jointw*ug**4))**.25,
            DuZ_l4=float(np.sum(jointw*uz**4))**.25,
            JZ_l4=float(np.sum(jointw*jz**4))**.25,
            mean_error=mean-lam*math.exp(-.5),
            variance=float(np.sum(jointw*(y-mean)**2))))
        rq=-math.sqrt(q+1)*a*df
    return dict(lam=lam,ngrid=ngrid,grid_interval=[-24,24],
                proved_first_step_L2_upper=5*lam**4/(1-2*math.sqrt(3)*lam)**2,
                rows=rows,
                scope='Uncertified quadrature/interpolation diagnostic, not a query sampler')


def main():
    out=[]
    for lam in (.03,.06,.12,.2):
        r=run(lam)
        out.append(r)
        print(json.dumps(dict(lam=lam,ngrid=r['ngrid'],last=r['rows'][-1])),flush=True)
    r=run(.12,ngrid=2401);out.append(r)
    print(json.dumps(dict(lam=.12,ngrid=r['ngrid'],last=r['rows'][-1])),flush=True)
    Path(__file__).with_name('ou_grid_results.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
