#!/usr/bin/env python3
"""Independent quadrature-diagonalized finite-Fock two-kick check.

This does not use the root Bessel/packet summation. Two bath modes realize the
Gram matrix of the two continuum field vectors exactly. Only the oscillator
Fock truncation is varied. Numerical convergence is a diagnostic, not a proof.
"""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.linalg import eigh
import json,time


def one(n):
    var=2.1; delay=.6; corr=var/(1-1j*delay)
    f0=np.sqrt(var)
    ft0=corr/f0
    ft1=np.sqrt(var-abs(ft0)**2)
    a=np.diag(np.sqrt(np.arange(1,n)),1).astype(complex)
    phi0=f0*(a+a.conj().T)
    eig0,u0=eigh(phi0)
    c=u0@(np.cos(.5*np.sin(eig0))*u0[0,:].conj())
    s=u0@(np.sin(.5*np.sin(eig0))*u0[0,:].conj())
    psi=np.zeros((2,n,n,2),complex)
    psi[0,:,0,0]=c;psi[1,:,0,1]=c
    psi[1,:,0,0]=-1j*s;psi[0,:,0,1]=-1j*s
    phi_a=ft0*a.conj().T+ft0.conjugate()*a
    phi_b=ft1*(a+a.conj().T)
    la,ua=eigh(phi_a);lb,ub=eigh(phi_b)
    for source in range(2):
        phase=np.exp(-1j*.75*(1-2*source)*np.sin(la[:,None]+lb[None,:]))
        for inp in range(2):
            x=ua.conj().T@psi[source,:,:,inp]@ub.conj()
            psi[source,:,:,inp]=ua@(phase*x)@ub.T
    mats={}
    number=np.arange(n)[:,None]+np.arange(n)[None,:]
    for name,z in [('all',1.),('no1',.4),('no2',.75),('no12',.15)]:
        mats[name]=np.einsum('sabi,ab,sabj->ij',psi.conj(),z**number,psi,optimize=True)
    patterns={'neither':mats['no12'],
              'only1':mats['no2']-mats['no12'],
              'only2':mats['no1']-mats['no12'],
              'both':mats['all']-mats['no1']-mats['no2']+mats['no12']}
    vectors={'zero':np.array([1.,0.]),'one':np.array([0.,1.]),
             'plus':np.array([1.,1.])/np.sqrt(2),
             'plus_i':np.array([1.,1j])/np.sqrt(2)}
    return {'cutoff_per_mode':n,'isometry_defect':float(np.linalg.norm(mats['all']-np.eye(2),2)),
            'effects':{k:[float(q[0,0].real),float(q[1,1].real),float(q[0,1].real),float(q[0,1].imag)] for k,q in patterns.items()},
            'probabilities':{k:{s:float(np.vdot(v,q@v).real) for s,v in vectors.items()} for k,q in patterns.items()}}


def run():
    start=time.time();out=[]
    for n in [48,80,120,160]:
        x=one(n)
        if out:
            x['max_probability_change_from_previous']=max(abs(x['probabilities'][r][s]-out[-1]['probabilities'][r][s]) for r in x['probabilities'] for s in x['probabilities'][r])
        out.append(x)
        print(n,x.get('max_probability_change_from_previous'),time.time()-start,flush=True)
    dest=Path(__file__).with_suffix('.json')
    dest.write_text(json.dumps({'status':'independent finite-Fock diagnostic, no rigorous Fock-tail claim','results':out,'runtime':time.time()-start},indent=2)+'\n')


if __name__=='__main__':run()
