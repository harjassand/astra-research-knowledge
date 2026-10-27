#!/usr/bin/env python3
"""Interaction sign control without loss of exact protected parity-band separation.
Real local ladder: independent direct and crossed memory couplings t,s on first rung.
"""
import numpy as np,math,json
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq
A=4-2*math.sqrt(3)
B=4/math.sqrt(3)-2

def parity_spectrum(c,which,n=256):
    diag=np.r_[3.,np.full(n,5. if which==1 else 1.)]
    off=np.r_[c,np.full(n-1,-.5)]
    w,U=eigh_tridiagonal(diag,off)
    u=U[0,:]**2
    atom=np.flatnonzero((w>2)&(w<4))
    assert len(atom)==1
    return w,u,float(w[atom[0]])

def run_one(t,s,n=256):
    plus=parity_spectrum(t+s,1,n)
    minus=parity_spectrum(t-s,-1,n)
    ep,em=plus[2],minus[2]
    def L(z,sp):
        x,w,_=sp
        return np.sum((w[:,None]*w[None,:])/(x[:,None]+x[None,:]-z))
    Ep=brentq(lambda z:L(z,plus)+L(z,minus),2*ep+1e-12,2*em-1e-12,xtol=9e-15)
    chi=Ep-ep-em
    chi4=-8*A*B*t*s*(t*t+s*s)
    return dict(direct_t=t,cross_s=s,plus_endpoint_coupling=t+s,minus_endpoint_coupling=t-s,
     bound_plus=ep,bound_minus=em,pair_energy=Ep,connected_shift=chi,
     perturbative_fourth_order_chi=chi4,
     pair_embedded_in_odd_global_two_photon_band=4<Ep<8,
     even_gap_to_essential_spectrum=min(Ep-(em+2),(ep+4)-Ep))

if __name__=='__main__':
    arr=[run_one(.20,s) for s in (-.04,-.02,0,.02,.04)]
    out=dict(quartic_general_exact_coefficient='-8*(4-2sqrt(3))*(4/sqrt(3)-2)*t*s*(t*t+s*s)',cases=arr)
    with open('/mnt/data/astra_local_pair_interaction_tunability_results.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))
