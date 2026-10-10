#!/usr/bin/env python3
"""Finite-matrix checks of the rational-transducer Choi representation.

These verify the multiplier/multiplicity algebra, not the physical Gaussian
theta coefficients or a quantum-capacity claim.
"""
import json
import math
from pathlib import Path
import numpy as np


def entropy(eigenvalues):
    positive = eigenvalues[eigenvalues>0]
    return -float(np.sum(positive*np.log2(positive)))


def check(p,q,k):
    assert math.gcd(p,q)==1 and math.gcd(k,p*q)==1
    omega=np.exp(2j*math.pi/k)
    x=np.roll(np.eye(k,dtype=complex),1,axis=0)
    z=np.diag(omega**np.arange(k))
    terms=[]
    for a in range(k):
        for b in range(k):
            u=np.linalg.matrix_power(x,a) @ np.linalg.matrix_power(z,p*b)
            v=np.linalg.matrix_power(x,a) @ np.linalg.matrix_power(z,q*b)
            terms.append(np.kron(u.T,v.conj().T))
    rng=np.random.default_rng(20261010+p+q+k)
    coefficients=rng.standard_normal(k*k)+1j*rng.standard_normal(k*k)
    operator=sum(c*t for c,t in zip(coefficients,terms))
    operator=(operator+operator.conj().T)/2
    operator-=np.trace(operator)*np.eye(k*k)/(k*k)
    scale=np.linalg.norm(operator,2)
    choi=(np.eye(k*k)+.5*operator/scale)/(k*k)
    eigenvalues=np.linalg.eigvalsh(choi)
    g=math.gcd(k,q-p)
    d=k//g
    groups=eigenvalues.reshape(-1,d)
    marginal=np.trace(choi.reshape(k,k,k,k),axis1=1,axis2=3)
    return dict(p=p,q=q,k=k,g=g,irrep_dimension=d,multiplicity=d,
                max_spectral_multiplicity_spread=float(np.max(np.ptp(groups,axis=1))),
                choi_trace_error=abs(float(np.trace(choi).real)-1),
                maximally_mixed_marginal_error=float(np.linalg.norm(marginal-np.eye(k)/k)),
                choi_entropy=entropy(eigenvalues),
                maxmixed_coherent_information=math.log2(k)-entropy(eigenvalues),
                status='algebra_diagnostic_not_gaussian_channel_certificate')


def main():
    records=[check(*triple) for triple in [(3,4,5),(7,9,2),(7,9,4),(11,13,6),(5,9,7)]]
    path=Path(__file__).with_name('rational_algebra_diagnostics.json')
    path.write_text(json.dumps(records,indent=2)+'\n')
    for record in records:
        print(json.dumps(record))
    print('saved',path)


if __name__=='__main__':
    main()
