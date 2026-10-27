#!/usr/bin/env python3
"""Infinite half-line continuum quadrature, including every one-body atom.
No finite chain is used. g=1/5; h-z resolvents have positive imaginary part.
Double Gauss-Chebyshev quadrature locates and normalizes the even pair.
mpmath integrates the odd rank-one compressed continuum boundary value.
"""
import json
import platform
import math
from pathlib import Path
import numpy as np
import mpmath as mp

OUT = Path(__file__).resolve().parent
G = 0.2

def bisect(f, a, b, n=100):
    fa=f(a)
    for _ in range(n):
        c=(a+b)/2
        if c in (a,b): return c
        fc=f(c)
        if fa*fc <= 0: b=c
        else: a=c;fa=fc
    return (a+b)/2

def bath_np(z,c):
    w=z-c
    return 2*(-w+math.copysign(math.sqrt(w*w-1),w))

def bath_derivative_np(z,c):
    w=z-c
    return 2*(-1+abs(w)/math.sqrt(w*w-1))

def measure_np(plus,n):
    c=5. if plus else 1.
    k2=(2. if plus else 1.)*G**2
    e=bisect(lambda z:3-z-k2*bath_np(z,c),2.1,3.9)
    atom=1/(1+k2*bath_derivative_np(e,c))
    th=np.arange(1,n+1)*math.pi/(n+1)
    u=np.cos(th)
    x=c+u
    den=(3-x+2*k2*u)**2+4*k2*k2*(1-u*u)
    weight=2*k2/(n+1)*np.sin(th)**2/den
    return np.r_[e,x],np.r_[atom,weight]

def pair_np(n):
    sp=measure_np(True,n);sm=measure_np(False,n)
    def l(z,sp,der=0):
        x,w=sp
        d=x[:,None]+x[None,:]-z
        return float(np.sum((w[:,None]*w[None,:])/d**(1+der)))
    ep=bisect(lambda z:l(z,sp)+l(z,sm),2*sp[0][0]+1e-10,2*sm[0][0]-1e-10)
    normalizer=(2/(l(ep,sp,1)+l(ep,sm,1)))**.5
    return dict(n=n,pair_energy=ep,even_normalizer=normalizer,
                E_plus=sp[0][0],E_minus=sm[0][0],Z_plus=sp[1][0],Z_minus=sm[1][0],
                chi=ep-sp[0][0]-sm[0][0],
                measure_mass_plus=float(sp[1].sum()),measure_mass_minus=float(sm[1].sum()))


def compute(dps=45,n=96):
    mp.mp.dps=dps
    g=mp.mpf(1)/5
    def bath(z,c):
        w=mp.mpc(z)-c
        return 2*(-w+mp.sqrt(w-1)*mp.sqrt(w+1))
    def bd(z,c):
        w=z-c
        return 2*(-1+abs(w)/mp.sqrt(w*w-1))
    def density(x,plus):
        c=5 if plus else 1
        k2=(2 if plus else 1)*g*g
        u=x-c
        if abs(u)>=1:return mp.mpf(0)
        v=mp.sqrt(1-u*u)
        return 2*k2*v/(mp.pi*((3-x+2*k2*u)**2+4*k2*k2*v*v))
    eplus=mp.findroot(lambda z:3-z-2*g*g*bath(z,5), (mp.mpf('2.9'),mp.mpf('3.0'))).real
    eminus=mp.findroot(lambda z:3-z-g*g*bath(z,1), (mp.mpf('3.0'),mp.mpf('3.1'))).real
    zp=1/(1+2*g*g*bd(eplus,5));zm=1/(1+g*g*bd(eminus,1))
    def r(z,plus):
        return 1/(3-z-(2 if plus else 1)*g*g*bath(z,5 if plus else 1))
    def spectral_nodes(plus):
        c=5 if plus else 1
        k2=(2 if plus else 1)*g*g
        xx=[eplus if plus else eminus]
        ww=[zp if plus else zm]
        for j in range(1,n+1):
            t=mp.pi*j/(n+1);u=mp.cos(t);x=c+u
            den=(3-x+2*k2*u)**2+4*k2*k2*(1-u*u)
            xx.append(x);ww.append(2*k2/(n+1)*mp.sin(t)**2/den)
        return xx,ww
    sp=spectral_nodes(True);sm=spectral_nodes(False)
    def l(z,sp,derivative=False):
        xx,ww=sp
        power=2 if derivative else 1
        return mp.fsum(ww[i]*ww[j]/(xx[i]+xx[j]-z)**power for i in range(n+1) for j in range(n+1))
    init=pair_np(n)['pair_energy']
    ep=mp.findroot(lambda z:l(z,sp)+l(z,sm),(mp.mpf(init)-mp.mpf('0.00001'),mp.mpf(init)+mp.mpf('0.00001')))
    norm2=2/(l(ep,sp,True)+l(ep,sm,True))
    cn=mp.sqrt(norm2)
    # Split integrals at all continuum branch thresholds. The trigonometric
    # substitution cancels the endpoint square root of the measure density.
    def cint(plus,fun,cuts=()):
        c=5 if plus else 1
        inner=[mp.acos(x-c) for x in cuts if c-1<x<c+1]
        knots=sorted([mp.mpf(0),mp.pi]+inner)
        return mp.quad(lambda th:density(c+mp.cos(th),plus)*mp.sin(th)*fun(c+mp.cos(th)),knots)
    D=zp*r(ep-eplus,False)+cint(True,lambda x:r(ep-x,False),[ep-2,ep])
    Jp=zp*r(ep-eplus,True)*r(ep-eplus,False)+cint(True,lambda x:r(ep-x,True)*r(ep-x,False),[ep-2,ep])
    Jm=zm*r(ep-eminus,False)*r(ep-eminus,True)+cint(False,lambda y:r(ep-y,False)*r(ep-y,True),[ep-6,ep-4])
    A=Jp+Jm
    alpha=A/D
    lo=max(mp.mpf(4),ep-2);hi=min(mp.mpf(6),ep)
    W=lambda x:r(ep-x,True)+r(x,False)
    def shell(fun):
        # x=lo+(hi-lo)*sin(t)^2 regularizes both ends, including inner bath edge.
        return mp.quad(lambda t: density(lo+(hi-lo)*mp.sin(t)**2,True)*density(ep-lo-(hi-lo)*mp.sin(t)**2,False)*fun(lo+(hi-lo)*mp.sin(t)**2)*2*(hi-lo)*mp.sin(t)*mp.cos(t),[0,mp.pi/2])
    shellmass=shell(lambda x:1)
    mean=shell(W)/shellmass
    variance=shell(lambda x:abs(W(x)-mean)**2)
    rho=norm2*shell(lambda x:abs(W(x)-alpha)**2)
    rho_plemelj=norm2*(shell(lambda x:W(x)**2)-(A*A/D).imag/mp.pi)
    # Exact independent-product integration for the additive dressed source.
    wp=[r(ep-x,True) for x in sp[0]];wm=[r(ep-y,False) for y in sm[0]]
    source_norm2_direct=norm2*(mp.fsum(w*a*a for w,a in zip(sp[1],wp))+mp.fsum(w*a*a for w,a in zip(sm[1],wm))+2*l(ep,sp)*l(ep,sm))
    result=dict(dps=dps,gauss_nodes=n,
        g=str(g),E_plus=str(eplus),E_minus=str(eminus),Z_plus=str(zp),Z_minus=str(zm),
        pair_energy=str(ep),connected_shift=str(ep-eplus-eminus),normalizer_squared=str(norm2),
        even_root_residual=str(l(ep,sp)+l(ep,sm)),
        bare_pair_overlap_squared=str(norm2*l(ep,sp)**2),
        D_real=str(D.real),D_imag=str(D.imag),A_real=str(A.real),A_imag=str(A.imag),
        alpha_real=str(alpha.real),alpha_imag=str(alpha.imag),
        shell_interval=[str(lo),str(hi)],shell_product_density=str(shellmass),
        D_imag_consistency=str(D.imag-mp.pi*shellmass),
        A_imag_consistency=str(A.imag-mp.pi*shell(W).real),
        rho=str(rho),rho_plemelj=str(rho_plemelj.real),
        density_identity_residual=str(rho-rho_plemelj.real),
        variance_lower_bound=str(norm2*variance),
        source_norm_squared=str(source_norm2_direct.real),
        shell_W_samples={str(x):str(W(mp.mpf(x)).real) for x in ['4.2','4.5','5.0','5.5','5.8']},
        method='Exact half-line spectral densities, all one-body atoms, odd rank-one compression; continuum quadrature is numerical, positivity and finiteness are proved separately.')
    return result

if __name__=='__main__':
    data={'runtime':{'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__},'pair_convergence':[pair_np(n) for n in [16,32,64,96,128,256]],'continuum':compute()}
    (OUT/'continuum_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
