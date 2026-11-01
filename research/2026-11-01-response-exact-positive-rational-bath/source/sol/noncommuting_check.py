#!/usr/bin/env python3
"""Finite noncommuting channel checks for the explicit two-mode realization.

This tests the finite Lindblad construction/cutoff, not arbitrary continuum
simulation, practicality, or novelty. The analytic bound supplies that scope.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent


def model(K, alpha=.2, a=1.):
    basis=[(i,j) for i in range(K+1) for j in range(K+1-i)]
    index={v:i for i,v in enumerate(basis)}
    d=len(basis)
    bs=[]
    for mode in [0,1]:
        b=np.zeros((d,d),complex)
        for col,v in enumerate(basis):
            if v[mode]:
                u=list(v);u[mode]-=1
                b[index[tuple(u)],col]=math.sqrt(v[mode])
        bs.append(b)
    c=np.sqrt(alpha/(2*a))*np.array([-1j*a,1])/2
    Haux=1j*bs[0].conj().T@bs[1]-1j*bs[1].conj().T@bs[0]
    field=c[0]*bs[0]+c[1]*bs[1]
    field=field+field.conj().T
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.diag([1.,-1.])
    Hs=.7*sz+.31*sy
    H=np.kron(Hs,np.eye(d))+np.kron(np.eye(2),Haux)+np.kron(sx,field)
    jump=np.kron(np.eye(2),2*bs[1]);loss=jump.conj().T@jump
    rho=np.zeros((4,2*d,2*d),complex)
    for k,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
        rho[k,i*d,j*d]=1
    return H,jump,loss,rho,np.array([sum(v) for v in basis])


def evolve(K,T=2.,steps=1000):
    H,L,R,rho,occup=model(K)
    dt=T/steps
    def rhs(x):
        return -1j*(H@x-x@H)+L@x@L.conj().T-(R@x+x@R)/2
    for _ in range(steps):
        k1=rhs(rho);k2=rhs(rho+dt*k1/2)
        k3=rhs(rho+dt*k2/2);k4=rhs(rho+dt*k3)
        rho+=dt*(k1+2*k2+2*k3+k4)/6
    d=len(occup)
    out=np.trace(rho.reshape(4,2,d,2,d),axis1=2,axis2=4)
    choi=np.block([[out[0],out[1]],[out[2],out[3]]])/2
    probs=np.diag(rho[0]).real.reshape(2,d).sum(axis=0)
    lam=.2*T*T/4
    moments=[]
    for k in range(1,min(K,4)+1):
        falling=np.ones(d)
        for j in range(k):falling*=np.maximum(occup-j,0)
        moment=float(falling@probs)
        moments.append({'order':k,'actual':moment,'upper':lam**k})
        assert moment <= lam**k+1e-9
    eig=np.linalg.eigvalsh((choi+choi.conj().T)/2)
    trace_error=max(abs(np.trace(out[k])-(1 if k in [0,3] else 0)) for k in range(4))
    assert eig.min()>-1e-9
    assert trace_error<1e-10
    bound=2*math.sqrt(.2/4)*T*math.sqrt(K+1)*math.sqrt(lam**K/math.factorial(K))
    return choi,{'cutoff':K,'steps':steps,'joint_dimension':2*d,
                 'minimum_Choi_eigenvalue':float(eig.min()),'TP_residual':float(trace_error),
                 'proved_channel_cutoff_bound':min(2,bound),'moments':moments}


def main():
    outputs={};rows=[]
    for K in [2,3,4,5,6]:
        choi,row=evolve(K)
        outputs[K]=choi;rows.append(row)
    refined,rr=evolve(6,steps=2000)
    numerical_error=float(2*np.linalg.norm(refined-outputs[6],ord='nuc'))
    assert numerical_error < 1e-7
    for row in rows:
        K=row['cutoff']
        delta=float(2*np.linalg.norm(outputs[K]-refined,ord='nuc'))
        row['diamond_upper_to_refined_K6']=delta
        assert delta <= row['proved_channel_cutoff_bound']+rr['proved_channel_cutoff_bound']+1e-7
    result={'scope':'Noncommuting Hs=.7 sigma_z+.31 sigma_y, Q=sigma_x; two coupled vacuum modes; alpha=.2; a=1; T=2. RK4 checks, not continuum validation.',
            'cutoff_checks':rows,'step_refinement_channel_upper':numerical_error,
            'bound_kind':'For normalized qubit Choi difference, 2 times nuclear norm is an upper bound on diamond norm.'}
    (ROOT/'results'/'noncommuting_channel.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
