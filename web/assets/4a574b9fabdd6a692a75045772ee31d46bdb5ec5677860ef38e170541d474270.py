#!/usr/bin/env python3
"""Qutrit Schur/Gram normalization diagnostic, not all-size certification.

Constructs a coherent fundamental residual times a three-qutrit determinant
singlet, then twirls four sites. Its sole Young shape is (2,1,1), K=1.
"""
from itertools import permutations
from pathlib import Path
import json
import numpy as np


def kron_all(mats):
    z=np.array([[1]],dtype=complex)
    for a in mats: z=np.kron(z,a)
    return z


def main():
    d,n,r=3,4,2
    singlet=np.zeros(d**3,dtype=complex)
    for p in permutations(range(d)):
        inversions=sum(p[a]>p[b] for a in range(d) for b in range(a+1,d))
        idx=sum(p[k]*d**(d-1-k) for k in range(d))
        singlet[idx]=(-1)**inversions/np.sqrt(6)
    psi=np.array([1,1j,1],dtype=complex)/np.sqrt(3)
    ket=np.kron(singlet,psi)
    raw=np.outer(ket,ket.conj()).reshape([d]*(2*n))
    rho=sum(raw.transpose(p+tuple(x+n for x in p)).reshape(d**n,d**n)
            for p in permutations(range(n)))/24
    assert abs(np.trace(rho)-1)<1e-12
    assert np.linalg.eigvalsh(rho)[0]>-1e-12
    tau=np.trace(rho.reshape(d,d**3,d,d**3),axis1=1,axis2=3)
    predicted_tau=(np.eye(d)+np.outer(psi,psi.conj()))/4
    assert np.max(np.abs(tau-predicted_tau))<1e-12
    red=np.trace(rho.reshape(d**r,d**(n-r),d**r,d**(n-r)),axis1=1,axis2=3)
    basis=[]
    for i in range(d):
        for j in range(i+1,d):
            x=np.zeros((d,d),dtype=complex); x[i,j]=x[j,i]=np.sqrt(d/2)
            y=np.zeros((d,d),dtype=complex); y[i,j]=-1j*np.sqrt(d/2); y[j,i]=1j*np.sqrt(d/2)
            basis.extend([x,y])
    for k in range(1,d):
        values=[1]*k+[-k]+[0]*(d-k-1)
        basis.append(np.diag(values)*np.sqrt(d/(k*(k+1))))
    hs=np.array([[np.trace(a@b)/d for b in basis] for a in basis])
    assert np.max(np.abs(hs-np.eye(d*d-1)))<1e-12
    b=np.array([np.trace(tau@a).real for a in basis])
    centered=[a-v*np.eye(d) for a,v in zip(basis,b)]
    gram=np.array([[np.trace(tau@a@z) for z in centered] for a in centered])
    coeff=np.array([np.trace(red@np.kron(a,z)) for a in centered for z in centered])
    inverse=np.linalg.inv(gram)
    parseval=float(np.vdot(coeff,np.kron(inverse,inverse)@coeff).real)
    ref=np.kron(tau,tau)
    direct=float(np.trace(red@red@np.linalg.inv(ref)).real-1)
    assert abs(parseval-direct)<1e-12
    rng=np.random.default_rng(20261008)
    tests=[]
    for singular in [False,True]:
        for k in range(4):
            a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
            if singular: a[-1]=a[0]+2*a[1]
            lhs=np.trace(rho@kron_all([a]*n))
            rhs=np.linalg.det(a)*np.vdot(psi,a@psi)
            err=abs(lhs-rhs)
            assert err<1e-10
            tests.append(dict(singular=singular,error=float(err),
                              lhs_absolute=float(abs(lhs)),rhs_absolute=float(abs(rhs))))
    result=dict(status='finite_complex_matrix_normalization_diagnostic',d=d,N=n,r=r,
                young_shape=[2,1,1],residual_K=1,
                tau_decomposition_max_error=float(np.max(np.abs(tau-predicted_tau))),
                complex_gram_min_eigenvalue=float(np.linalg.eigvalsh(gram)[0]),
                petz_chi_square=direct,weighted_support_parseval=parseval,
                rho_reference_commutator_norm=float(np.linalg.norm(red@ref-ref@red)),
                schur_determinant_tests=tests,
                limitations=['N4,r2 lies outside the stated theorem finite range.',
                   'One qutrit sector validates normalizations only.',
                   'No all-size, formal or external validation.'])
    (Path(__file__).resolve().parent/'qudit_normalization_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
