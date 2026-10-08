#!/usr/bin/env python3
"""Finite matrix/polarization checks for the concentration proof.

Constructs permutation-twirled heterogeneous product populations. They satisfy
the stated MGF with A=1,B=1/2 by conditional product Hoeffding, and have faithful
marginals away from I/d. They are fully separable: no entanglement claim.
"""
from itertools import permutations,product
from math import comb,factorial,e
from pathlib import Path
import json
import numpy as np


def normalized_basis(d):
    result=[]
    for i in range(d):
        for j in range(i+1,d):
            a=np.zeros((d,d),dtype=complex);a[i,j]=a[j,i]=1/np.sqrt(2)
            b=np.zeros((d,d),dtype=complex);b[i,j]=-1j/np.sqrt(2);b[j,i]=1j/np.sqrt(2)
            result.extend([a,b])
    for k in range(1,d):
        result.append(np.diag([1]*k+[-k]+[0]*(d-k-1))/np.sqrt(k*(k+1)))
    return result


def kron_all(items):
    out=np.array([[1]],dtype=complex)
    for x in items:out=np.kron(out,x)
    return out


def population(d):
    v0=np.zeros(d,dtype=complex);v0[0]=1
    v1=np.zeros(d,dtype=complex);v1[:2]=[1,1];v1/=np.sqrt(2)
    v2=np.zeros(d,dtype=complex)
    v2[:d]=[1,1j] if d==2 else [1,1j,1]
    v2/=np.linalg.norm(v2)
    return [np.outer(v,v.conj()) for v in [v0,v1,v2]]


def tensor_corr(signals,k):
    n,s=signals.shape
    out=np.zeros([s]*k)
    for ids in permutations(range(n),k):
        z=signals[ids[0]]
        for i in ids[1:]:z=np.multiply.outer(z,signals[i])
        out+=z
    return out/(factorial(n)//factorial(n-k))


def scalar_corr(signals,vectors):
    n=signals.shape[0];k=len(vectors)
    projected=signals@np.stack(vectors).T
    return sum(np.prod([projected[idx,j] for j,idx in enumerate(ids)])
               for ids in permutations(range(n),k))/(factorial(n)//factorial(n-k))


def small_case(d,r):
    distinct=population(d)
    states=distinct*2;n=len(states)
    tau=sum(states)/n
    basis=normalized_basis(d);s=len(basis)
    hs=np.array([[np.trace(a@b) for b in basis] for a in basis])
    assert np.max(np.abs(hs-np.eye(s)))<1e-12
    centered=[a-np.trace(tau@a)*np.eye(d) for a in basis]
    signals=np.array([[np.trace(st@a).real for a in centered] for st in states])
    assert np.max(np.abs(signals.sum(axis=0)))<1e-12
    gram=np.array([[np.trace(tau@a@b) for b in centered] for a in centered])
    kappa=float(np.linalg.eigvalsh(tau)[0])
    assert np.linalg.eigvalsh(gram)[0]>=kappa-1e-12
    rho=sum(kron_all([states[i] for i in ids])
            for ids in permutations(range(n),r))/(factorial(n)//factorial(n-r))
    reference=kron_all([tau]*r)
    delta=rho-reference
    # Exact trace identity avoids subtracting nearly equal purities.
    direct=float(np.trace(delta@delta@np.linalg.inv(reference)).real)
    reconstructed=0.;parts=[]
    for k in range(2,r+1):
        corr=tensor_corr(signals,k).ravel()
        ginv=kron_all([np.linalg.inv(gram)]*k)
        term=float(np.vdot(corr,ginv@corr).real)*comb(r,k)
        reconstructed+=term;parts.append(dict(weight=k,term=term))
    assert abs(direct-reconstructed)<2e-12
    rng=np.random.default_rng(20261008+d+r)
    residuals=[]
    for k in [2,3,4]:
        vecs=[x/np.linalg.norm(x) for x in rng.normal(size=(k,s))]
        exact=scalar_corr(signals,vecs)
        pol=sum(np.prod(eps)*scalar_corr(signals,[sum(eps[j]*vecs[j]
                        for j in range(k))]*k) for eps in product([-1,1],repeat=k))
        pol/=2**k*factorial(k)
        assert abs(exact-pol)<2e-12
        residuals.append(float(abs(exact-pol)))
    return dict(d=d,N=n,r=r,kappa=kappa,
                tau_white_hilbert_schmidt_distance=float(np.linalg.norm(tau-np.eye(d)/d)),
                reference_commutator_norm=float(np.linalg.norm(rho@reference-reference@rho)),
                gram_min_eigenvalue=float(np.linalg.eigvalsh(gram)[0]),
                petz_chi_square=direct,weighted_support_parseval=reconstructed,
                per_weight=parts,polarization_orders=[2,3,4],polarization_residuals=residuals)


def legal_range_pair(d,n=300000):
    states=population(d);tau=sum(states)/3
    centered=[x-tau for x in states]
    covariance=sum(np.kron(x,x) for x in centered)/3
    delta=-covariance/(n-1)
    reference=np.kron(tau,tau)
    value=float(np.trace(delta@delta@np.linalg.inv(reference)).real)
    kappa=float(np.linalg.eigvalsh(tau)[0]);s=d*d-1;alpha=2/n
    x=2*e*e*2.5*s*alpha/(kappa*(1-alpha)**2)
    assert x<1 and alpha<=kappa/(16*e*e*2.5*s)
    bound=x*x/(1-x)
    assert value<=bound
    return dict(d=d,N=n,r=2,MGF_A=1,MGF_B=.5,kappa=kappa,
                exact_two_body_operator_formula=True,petz_chi_square=value,
                N2_scaled_chi=n*n*value,theorem_x=x,theorem_bound=bound,
                tau_white_hilbert_schmidt_distance=float(np.linalg.norm(tau-np.eye(d)/d)),
                reference_commutator_norm=float(np.linalg.norm(delta@reference-reference@delta)))


if __name__=='__main__':
    small=[small_case(d,r) for d in [2,3] for r in [2,3]]
    legal=[legal_range_pair(d) for d in [2,3]]
    result=dict(status='finite_complex_matrix_and_real_polarization_diagnostics',
                small_population_fixtures=small,legal_range_pair_fixtures=legal,
                scope='MGF follows analytically from conditional product Hoeffding; no finite direction grid is claimed to establish the MGF.',
                warnings=['Small N6 fixtures lie outside the displayed finite theorem range.',
                    'All fixture states are fully separable.',
                    'No formal replay, all-state validation or historical priority evidence.'])
    (Path(__file__).resolve().parent/'normalization_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
