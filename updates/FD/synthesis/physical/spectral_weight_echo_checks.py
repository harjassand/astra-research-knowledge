#!/usr/bin/env python3
"""Exact retained-record certificate, finite echo and Pauli-reset diagnostics.

No laboratory data; no floating value is used to prove the rational interval.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import argparse,hashlib,itertools,json,math
import numpy as np
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'sources'/'cray_active_acquisition'

def herm(rng,d):
    a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    return (a+a.conj().T)/(2*math.sqrt(d))

def norm(a):
    return float(np.linalg.norm(a,2))

def ptr_s(a,d,b):
    return np.einsum('aiaj->ij',a.reshape(d,b,d,b))

def exact_retained_record():
    path=SOURCE/'retained_memory_results.json'
    data=json.loads(path.read_text())
    assert data['N']==100_000_000 and data['failures']==7
    n=data['N'];s=data['failures'];q=F(161,10**9);x=n*q
    poly=sum((x/(1-q))**j/F(factorial(j)) for j in range(s+1))
    exp_lower=sum(x**j/F(factorial(j)) for j in range(101))
    tail=poly/exp_lower
    assert tail<F(1,100)
    Lam=F(879,50);d=8;t=F(1,50);w=F(1,5)
    c=t*t*(1-Lam*t/2)**2/(4*d)
    assert c==F(16982641,2000000000000)
    rows=[]
    for gamma,radius in [(F(0),F(138,1000)),(F(1,10**8),F(142,1000)),
                         (F(1,10**7),F(176,1000))]:
        rs=(q+gamma)/c
        assert rs<radius*radius
        rows.append({'gamma':str(gamma),'radius_square_exact':str(rs),
                     'radius_upper':str(radius),
                     'DeltaF_interval':[str(w-radius),str(w+radius)],
                     'sign_certified':radius<w})
    return {'source_path':str(path),
            'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_data_kind':'Producer simulated retained quantum-memory instrument trajectory',
            'n':n,'failures':s,'confidence':'conditional 99 percent',
            'q_upper_exact':str(q),'tail_upper_exact':str(tail),
            'tail_upper_display':float(tail),'Lambda':str(Lam),'time':str(t),
            'dimension':d,'coefficient_exact':str(c),'rows':rows,
            'physical_calibration_verified':False,
            'external_theorem_review':'UNKNOWN','novelty':'UNKNOWN'}

def finite_echo_checks():
    rng=np.random.default_rng(202610140192)
    worst_remainder=0.;lowest_prob=math.inf;models=0
    for d in [2,3,4,5,6]:
        for b in [2,3]:
            for j in range(8):
                touch=herm(rng,d*b)
                outside=(1+40*j)*herm(rng,b)
                K=touch+np.kron(np.eye(d),outside)
                r=herm(rng,d);delta=float(rng.uniform(.02,1))
                r*=delta/norm(r)
                R=np.kron(r,np.eye(b));cap=delta+.1
                Lam=2*norm(touch)+cap
                t=float(rng.uniform(.15,1.65))/Lam
                E=expm(1j*K*t)@expm(-1j*(K+R)*t)
                remainder=norm(E-np.eye(d*b)+1j*t*R)
                bound=Lam*t*t*delta/2
                assert remainder<=bound+1e-10
                worst_remainder=max(worst_remainder,remainder/bound)
                Q=(E-np.eye(d*b)).conj().T@(E-np.eye(d*b))
                P=ptr_s(Q,d,b)/(4*d)
                p_min=float(np.linalg.eigvalsh((P+P.conj().T)/2)[0])
                lb=t*t*(1-Lam*t/2)**2*delta**2/(4*d)
                assert p_min+1e-12>=lb
                lowest_prob=min(lowest_prob,p_min/lb)
                models+=1
    return {'models':models,'outside_state_scope':'all outside states via minimum eigenvalue',
            'largest_remainder_to_operator_bound_ratio':worst_remainder,
            'smallest_probability_to_sharper_bound_ratio':lowest_prob,
            'evidence_scope':'floating diagnostics only; arbitrary entangling boundary terms allowed'}

def twirl_checks():
    rng=np.random.default_rng(202610140193)
    I=np.eye(2);X=np.array([[0,1],[1,0]])
    Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    paulis=[I,X,Y,Z];worst=0.;tests=0
    for ell in [1,2,3]:
        d=2**ell;b=3
        for _ in range(5):
            a=rng.normal(size=(d*b,d*b))+1j*rng.normal(size=(d*b,d*b))
            rho=a@a.conj().T;rho/=np.trace(rho)
            tau=ptr_s(rho,d,b)
            average=np.zeros_like(rho)
            for factors in itertools.product(paulis,repeat=ell):
                p=np.array([[1.]])
                for f in factors:p=np.kron(p,f)
                u=np.kron(p,np.eye(b))
                average+=u@rho@u.conj().T/(4**ell)
            error=norm(average-np.kron(np.eye(d)/d,tau))
            assert error<1e-12
            worst=max(worst,error);tests+=1
    return {'correlated_host_states':tests,'largest_twirl_decoupling_error':worst,
            'status':'finite numerical check of exact Pauli identity; no hardware noise model',
            'fresh_random_bits_each_trial':'2*ell',
            'forbidden_data_flow':'postselection by current Pauli key; batching a fixed key without fresh independent randomization'}

def obstructions():
    # Locality/full support cannot be dropped: unseen outside or collar sectors.
    delta=.3;t=.2;I=np.eye(2);P=np.diag([1.,0.])
    outside_R=np.kron(I,delta*P)
    outside_rho=np.kron(I/2,np.diag([0.,1.]))
    local_R=np.kron(delta*P,I)
    unsupported_rho=np.kron(np.diag([0.,1.]),I/2)
    vals=[]
    for R,rho in [(outside_R,outside_rho),(local_R,unsupported_rho)]:
        E=expm(-1j*R*t)
        p=float((1-np.trace(rho@E).real)/2)
        assert abs(p)<1e-14 and norm(R)>.29
        vals.append(p)
    # Channel witness strictly broader than unitary positive comparison.
    K0=np.diag([0.,2.]);K1=np.diag([1.1,1.2]);X=np.array([[0.,1.],[1.,0.]])
    phi=(K0+X@K0@X)/2
    margin=float(np.linalg.eigvalsh(K1-phi)[0])
    assert margin>.099 and K1[-1,-1]<K0[-1,-1]
    return {'nonlocal_unseen_sector_failure_probability':vals[0],
            'non_full_support_reset_failure_probability':vals[1],
            'nonzero_residual_norm':delta,
            'channel_averaging_margin':margin,
            'unitary_positive_comparison_impossible_by_ordered_top_eigenvalue':True,
            'rank_one_exact_probability':'sin(delta*time/2)^2/d; dimension factor is necessary for prescribed null protocol'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path,default=None,
                        help='Path to preserved cray_active_acquisition producer packet')
    parser.add_argument('--output-dir',type=Path,default=HERE,
                        help='Directory for the new diagnostic result; originals are never edited')
    args=parser.parse_args()
    if args.source_dir is not None:
        SOURCE=args.source_dir
    elif not SOURCE.exists():
        candidates=[p/'updates/FD/package/echo_acquisition/cray_active_acquisition'
                    for p in [HERE,*HERE.parents]]
        SOURCE=next((p for p in candidates if p.is_dir()),SOURCE)
    if not (SOURCE/'retained_memory_results.json').is_file():
        parser.error('Preserved source not found; provide --source-dir')
    args.output_dir.mkdir(parents=True,exist_ok=True)
    data={'exact_retained_record':exact_retained_record(),'finite_echo':finite_echo_checks(),
          'twirl':twirl_checks(),'obstructions':obstructions()}
    (args.output_dir/'SPECTRAL_WEIGHT_ECHO_RESULTS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'exact_rows':data['exact_retained_record']['rows'],
                      'tail':data['exact_retained_record']['tail_upper_display'],
                      'finite_echo':data['finite_echo'],'twirl':data['twirl'],
                      'obstructions':data['obstructions']},indent=2))
