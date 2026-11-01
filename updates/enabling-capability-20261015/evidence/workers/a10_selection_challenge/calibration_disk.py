"""Exact noiseless three-channel compatibility and conditional noisy lower bound.
No claim of novelty. Published 1-sigma envelope summaries are not hard disks.
"""
from pathlib import Path
import json,time
import numpy as np
P=Path(__file__).resolve().parent

def disk_certificate(y,w,eps):
    y=np.asarray(y,dtype=complex);w=np.asarray(w,dtype=complex);eps=np.asarray(eps,float)
    if np.any(eps<0) or np.any(eps>=1):raise ValueError('Need 0 <= eps_i < 1')
    c=1/(1-eps**2);r=eps/(1-eps**2);a=np.conj(w)*y;z=np.sum(a*c);R=np.sum(abs(a)*r)
    m=max(abs(z)-R,0.)
    direction=z/abs(z) if abs(z)>0 else 1.+0j
    lam=min(1.,abs(z)/R) if R>0 else 0.
    shifts=np.zeros_like(a);nonzero=abs(a)>0
    shifts[nonzero]=-lam*r[nonzero]*direction*np.conj(a[nonzero])/abs(a[nonzero])
    inv_c=c+shifts
    variance_upper=np.sum(abs(w)**2/(1-eps)**2)
    return dict(min_transformed_residual=m,inv_gain=inv_c,noise_normalized_lower=m*m/variance_upper,nominal_residual=abs(np.vdot(w,y)),disk_radius=R,center=complex(z))

def checks():
    rng=np.random.default_rng(319093);max_formula_error=0.;max_gain_excess=-np.inf;false_reject=0;monotonic_violation=0.;n=10000
    for _ in range(n):
        A=rng.normal(size=(3,2))+1j*rng.normal(size=(3,2));U,s,V=np.linalg.svd(A,full_matrices=True);w=U[:,-1]
        h=rng.normal(size=2)+1j*rng.normal(size=2);eps=rng.uniform(0,.3,size=3)
        gain=1+eps*np.sqrt(rng.uniform(size=3))*np.exp(2j*np.pi*rng.uniform(size=3));y=gain*(A@h)
        d=disk_certificate(y,w,eps)
        false_reject+=d['min_transformed_residual']>1e-12
        for y in [y, rng.normal(size=3)+1j*rng.normal(size=3)]:
            d=disk_certificate(y,w,eps)
            actual=abs(np.vdot(w,d['inv_gain']*y))
            max_formula_error=max(max_formula_error,abs(actual-d['min_transformed_residual']))
            max_gain_excess=max(max_gain_excess,float(np.max(abs(1/d['inv_gain']-1)-eps)))
            nominal=disk_certificate(y,w,np.zeros(3))['noise_normalized_lower']
            monotonic_violation=max(monotonic_violation,d['noise_normalized_lower']-nominal)
    return dict(trials=n,random_seed=319093,known_tensor_gain_false_rejections=false_reject,max_exact_formula_error=max_formula_error,max_gain_disk_violation=max_gain_excess,max_lower_bound_above_nominal=monotonic_violation,scope='Finite numerical checks of algebraic formula; proof supplied separately.')

if __name__=='__main__':
    t=time.perf_counter();r=checks();r['runtime_s']=time.perf_counter()-t
    (P/'DISK_CERTIFICATE_CHECK.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
