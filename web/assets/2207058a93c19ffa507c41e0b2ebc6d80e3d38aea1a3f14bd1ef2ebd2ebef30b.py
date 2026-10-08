#!/usr/bin/env python3
"""Finite scalar diagnostics for the frozen bounded heat construction.

NumPy CPU only. These verify binomial identities and selected axis-aligned
product-array comparators, not the ALLSEP supremum or all-size theorem.
"""
from math import comb,exp,lgamma,sqrt
from pathlib import Path
import json
import numpy as np
from check_local_access import sector_law


def binomial_white(r):
    h=np.arange(r+1)
    p=np.exp(np.array([lgamma(r+1)-lgamma(int(k)+1)-lgamma(r-int(k)+1)
                       for k in h])-r*np.log(2))
    p/=p.sum()
    j=h-r/2
    t=float(p@np.exp(-j*j/r))
    q=float(p@(j*j/r*np.exp(-j*j/r)))
    return h,p,j,t,q,t-4*q


def krawtchouk(r):
    return np.array([[sum((-1)**a*comb(r-h,a)*comb(h,w-a)
                         for a in range(max(0,w-h),min(w,r-h)+1))
                       for w in range(r+1)] for h in range(r+1)],dtype=float)


def target_polynomial(n,r):
    ms,weights,_=sector_law(n)
    polys=[]
    for w in range(r+1):
        coeff=np.zeros(w+1)
        for ell in range(w//2+1):
            k=w-2*ell
            coeff[k]=(-1)**(w-ell)*sum(float(v)*comb((n-int(m))//2,ell)*comb(int(m),k)
                  for m,v in zip(ms,weights)
                  if (n-int(m))//2>=ell and int(m)>=k)/comb(n,w)
        polys.append(coeff)
    return -float(ms@weights)/n,polys


def signed_array_corr(n,r,plus):
    return np.array([sum((-1)**a*comb(n-plus,a)*comb(plus,w-a)
                 for a in range(max(0,w-plus),min(w,n-plus)+1))/comb(n,w)
                    for w in range(r+1)])


def heat_case(n,r,order):
    h,p,j,t,q,kappa=binomial_white(r)
    b,polys=target_polynomial(n,r)
    hf=kappa*n/(2*q*(n-1))
    c,wts=np.polynomial.legendre.leggauss(order)
    wts=wts/2
    beta=hf*b*c
    heat=np.exp(-(j[:,None]/sqrt(r)-beta[None,:]*sqrt(r)/2)**2)
    raw=np.stack([np.polynomial.polynomial.polyval(c,x) for x in polys])
    kernel=krawtchouk(r)
    target_prob=p[:,None]*(kernel@raw)
    assert float(target_prob.min())>-2e-12
    assert np.max(np.abs(target_prob.sum(axis=0)-1))<2e-11
    target=float(wts@np.sum(target_prob*heat,axis=0))
    a0=float(wts@(p@heat))
    target_low=a0+kappa*r*n*b*b/(3*(n-1))
    formal_low_sup=a0+kappa*r*(n*b*b+1)/(6*(n-1))
    power=c[None,:]**np.arange(r+1)[:,None]
    arrays=[]
    for d in np.linspace(-4,4,161):
        plus=max(0,min(n,int(round(n*(1+d/sqrt(n))/2))))
        gs=(2*plus-n)/n
        cs=signed_array_corr(n,r,plus)
        prob=p[:,None]*(kernel@(cs[:,None]*power))
        assert float(prob.min())>-2e-12
        value=float(wts@np.sum(prob*heat,axis=0))
        low=a0+kappa*r*(2*n*b*gs-n*gs*gs+1)/(6*(n-1))
        arrays.append(dict(plus=plus,sqrtN_mean=sqrt(n)*gs,
                           expectation=value,second_order_expectation=low))
    best=max(arrays,key=lambda x:x['expectation'])
    # Independent direct z-hypergeometric check at c=1.
    ms,weights,_=sector_law(n)
    direct=np.zeros(r+1)
    for m,v in zip(ms,weights):
        up=(n-int(m))//2
        for k in range(r+1):
            if k<=up and r-k<=n-up:
                direct[k]+=v*comb(up,k)*comb(n-up,r-k)/comb(n,r)
    corr_at_one=np.array([float(np.sum(x)) for x in polys])
    reconstructed=p*(kernel@corr_at_one)
    assert float(np.max(np.abs(direct-reconstructed)))<2e-11
    return dict(N=n,r=r,alpha=r/n,quadrature_order=order,
                Nb2=n*b*b,T=t,q=q,kappa=kappa,h=hf,
                white_shift_baseline=a0,target_expectation=target,
                target_second_order=target_low,
                target_remainder=target-target_low,
                formal_second_order_sep_sup=formal_low_sup,
                target_gap_to_best_tested_array=target-best['expectation'],
                target_gap_second_order=kappa*r*(n*b*b-1)/(6*(n-1)),
                best_tested_signed_array=best,
                grid_comparators=len(arrays),
                z_reconstruction_max_error=float(np.max(np.abs(direct-reconstructed))))


def main():
    scalar=[]
    for r in [2,3,4,8,16,128,1024,16384]:
        h,p,j,t,q,k=binomial_white(r)
        assert t>=exp(-.25)-1e-10 and q>=1/16-1e-10
        assert k>=exp(-12)/8-1e-10
        scalar.append(dict(r=r,T=t,q=q,kappa=k,h_asymptotic_N=k/(2*q)))
        if r<=128:
            for beta in [-.15,-.01,.001,.1]:
                ww=np.exp(-(j/sqrt(r)-beta*sqrt(r)/2)**2)
                f1=2/r*float(p@(j*ww))
                f2=float(p@((4*j*j-r)*ww))/(r*(r-1))
                assert abs(f1-2*beta*q)<=r*abs(beta)**3/4+2e-12
                assert abs(f2+k/(r-1))<=beta*beta+2e-12
    rows=[heat_case(n,r,64) for n,r in [(128,2),(256,4),(512,8),(1024,8),(2048,16)]]
    repeat=[heat_case(n,r,128) for n,r in [(128,2),(1024,8),(2048,16)]]
    for a,b in zip([rows[0],rows[3],rows[4]],repeat):
        assert abs(a['target_expectation']-b['target_expectation'])<1e-11
    result=dict(status='finite_double_precision_diagnostics_not_ALLSEP_certificate',
                model='selected nu=0 stationary exact-white-Schur target',
                scalar_identities=scalar,cases=rows,quadrature_repeats=repeat,
                limitations=['Signed z-axis product arrays are only a restricted null family.',
                  'Second-order supremum is not a finite-size sound bound without its remainder.',
                  'No finite test promotes the candidate theorem to external validation.'])
    (Path(__file__).resolve().parent/'local_heat_diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(cases=rows,scalar_fixtures=len(scalar)),indent=2))


if __name__=='__main__': main()
