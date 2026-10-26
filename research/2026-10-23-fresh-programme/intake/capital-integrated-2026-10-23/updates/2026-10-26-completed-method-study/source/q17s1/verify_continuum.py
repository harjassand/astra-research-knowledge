"""Check continuum transform against independently solved finite RC ladders."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve_banded

OUT=Path(__file__).resolve().parent


def design(n,ratio):
    delta=np.log(ratio)/(n-1)
    rho=np.exp(-delta)
    s=np.exp(np.linspace(0,np.log(ratio),n))
    c=np.diff(np.r_[0,s])
    w=np.full(n,(1-rho)/(1+rho))
    w[0]=w[-1]=1/(1+rho)
    a=w/w.sum()
    return c,a/s


def finite_transform(c,r,z):
    n=len(c); g=1/r
    diag=g.copy(); diag[1:]+=g[:-1]
    ab=np.zeros((3,n),dtype=complex)
    ab[0,1:]=-g[:-1]
    ab[1,:]=diag+z*c
    ab[2,:-1]=-g[:-1]
    inp=np.zeros(n);inp[0]=1
    return g[-1]*solve_banded((1,1),ab,inp)[-1]


def continuum_transform(ratio,z):
    L=np.log(ratio);kappa=1/(L+2);h=kappa*z
    beta=np.sqrt(.25+h+0j)
    den=(1+2*h)*np.cosh(beta*L)+(h*h+2*h+.5)/beta*np.sinh(beta*L)
    return np.exp(L/2)/den


if __name__=='__main__':
    rows=[]
    for ratio in [2.,10.,100.,10000.]:
        for n in [8,32,128,512]:
            c,r=design(n,ratio)
            errs=[]
            vals=[]
            for z in [.1,1.,5.,20.,1j,5j]:
                f=finite_transform(c,r,z); fc=continuum_transform(ratio,z)
                errs.append(abs(f-fc))
                vals.append(dict(z_real=float(np.real(z)),z_imag=float(np.imag(z)),
                                 finite_real=float(f.real),finite_imag=float(f.imag),
                                 continuum_real=float(fc.real),continuum_imag=float(fc.imag)))
            rows.append(dict(ratio=ratio,n=n,max_abs_error=float(max(errs)),values=vals))
    (OUT/'continuum_verification.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps([dict(ratio=x['ratio'],n=x['n'],max_abs_error=x['max_abs_error']) for x in rows],indent=2))
