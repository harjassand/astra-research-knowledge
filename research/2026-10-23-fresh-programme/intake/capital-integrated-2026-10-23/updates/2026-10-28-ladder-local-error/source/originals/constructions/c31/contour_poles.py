#!/usr/local/bin/python3
"""Diagnostic quadrature of the infinite-momentum contour construction.

This is a complex contour Nyström calculation, not an infinite-system proof.
Full eta is retained in the one-body h_eta; the TWO hard-core constraints are
then imposed on dGamma_2(h_eta). No rank-one approximation to V is made.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json, sys
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eig
from scipy.optimize import root
ROOT=Path(__file__).resolve().parent
E0=5.97857931516657854523653889398
RHO=2.12750672061584377235962562955e-8

def spectral_data(n,t,eta):
    x,w=leggauss(n)
    k=(x+1)*np.pi/2;w=w*np.pi/2
    phi=k-1j*t*np.sin(k)
    jac=1-1j*t*np.cos(k)
    d=2+2*n
    h=np.zeros((d,d),dtype=complex)
    h[0,0]=h[1,1]=3
    h[0,1]=h[1,0]=eta
    for mem,c,a,start in ((0,5,np.sqrt(2)/5,2),(1,1,1/5,2+n)):
        h[np.arange(start,start+n),np.arange(start,start+n)]=c-np.cos(phi)
        v=a*np.sqrt(2/np.pi)*np.sin(phi)*np.sqrt(jac*w)
        h[mem,start:start+n]=v;h[start:start+n,mem]=v
    vals,U=eig(h,check_finite=True)
    norms=np.einsum('ij,ij->j',U,U)
    U=U/np.sqrt(norms)[None,:]
    L=(U[0,:]+U[1,:])/np.sqrt(2)
    R=(U[0,:]-U[1,:])/np.sqrt(2)
    weights=(L*L,R*R,L*R)
    sums=vals[:,None]+vals[None,:]
    return sums,weights

def pole(n,t,eta):
    sums,(l,r,lr)=spectral_data(n,t,eta)
    ll=l[:,None]*l[None,:];rr=r[:,None]*r[None,:]
    cross=lr[:,None]*lr[None,:]
    def schur(z):
        den=sums-z
        L=np.sum(ll/den);R=np.sum(rr/den);X=np.sum(cross/den)
        Ke=(L+R+2*X)/2;Ko=(L+R-2*X)/2;Kx=(L-R)/2
        return Ke-Kx*Kx/Ko
    def fn(a):
        q=schur(complex(a[0],a[1]));return [q.real,q.imag]
    ans=root(fn,[E0,-np.pi*RHO*eta*eta],tol=1e-10)
    z=complex(*ans.x)
    return dict(n=n,t=t,eta=eta,pole_real=z.real,pole_imag=z.imag,
        real_shift_over_eta2=(z.real-E0)/(eta*eta) if eta else None,
        minus_imag_over_eta2=-z.imag/(eta*eta) if eta else None,
        target_pi_rho=np.pi*RHO,residual=abs(schur(z)),
        solver_success=bool(ans.success),message=str(ans.message))

n=int(sys.argv[1]) if len(sys.argv)>1 else 100
t=float(sys.argv[2]) if len(sys.argv)>2 else .2
out={'scope':'uncertified contour quadrature diagnostic; theorem is in PROOF.md',
     'results':[pole(n,t,eta) for eta in (0.,.005,.01,.02,.04)]}
(ROOT/f'contour_poles_n{n}_t{str(t).replace(".","p")}.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
