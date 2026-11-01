#!/usr/bin/env python3
"""Multi-port, dark-mode and actual-count checks for the new compiler lemmas."""
import json
from pathlib import Path
import math
import numpy as np
from loss_clock import annihilators,gamma,expm,norm,CoupledBath

P=Path(__file__).resolve().parent
rng=np.random.default_rng(20261101)
rows=[]
for trial in range(12):
    M=2+trial%3;K=2;r=1+trial%M
    x=rng.normal(size=(M,M))+1j*rng.normal(size=(M,M))
    H=(x+x.conj().T)/2
    E=(rng.normal(size=(M,r))+1j*rng.normal(size=(M,r)))/2
    if trial==0:
        # An exact dark invariant one-particle mode: a global gap is absent.
        H=np.diag(np.arange(M)+1.)
        E=np.zeros((M,1),complex);E[0,0]=2
    A=-1j*H-E@E.conj().T/2
    states,bs=annihilators(M,K)
    G0=sum(A[i,j]*bs[i].conj().T@bs[j] for i in range(M) for j in range(M))
    ts=[0,.01,.2,1.3]
    maxerr=0.;qerr=0.;derivative=0.
    for t in ts:
        F=expm(A*t);gf=gamma(F,K)
        actual=np.vstack([sum(np.conj(E[j,mu])*bs[j] for j in range(M))@gf for mu in range(r)])
        vec=E.conj().T@F
        constructed=np.vstack([gf@sum(vec[mu,j]*bs[j] for j in range(M)) for mu in range(r)])
        maxerr=max(maxerr,norm(actual-constructed))
        qerr=max(qerr,norm(gf-expm(G0*t)))
        assert norm(actual)<=math.sqrt(K)*float(np.linalg.norm(vec))+1e-10
        assert 0<=M-float(np.trace(F.conj().T@F).real)+1e-10<=M+1e-10
    # Positive quadrature verifies the trace/CDF identity without a spectral gap.
    xx,ww=np.polynomial.legendre.leggauss(96);T=1.3
    integ=sum(w*float(np.linalg.norm(E.conj().T@expm(A*((x+1)*T/2)))**2) for x,w in zip(xx,ww))*T/2
    F=expm(A*T);J=M-float(np.trace(F.conj().T@F).real)
    assert abs(integ-J)<1e-10
    assert maxerr<1e-10 and qerr<1e-10
    rows.append({'trial':trial,'M':M,'ports':r,'exact_dark_mode':trial==0,
                 'intertwining_error':maxerr,'second_quantization_error':qerr,
                 'CDF_vs_positive_integral':abs(J-integ),'J(T)':J})

counts=[]
for R in [4.,40.,4000.]:
    b=CoupledBath(R,K=2);d=len(b.G);T=1.;chi=1.
    H=1j*(b.G-b.G.conj().T)/2
    # G already includes the non-Hermitian no-jump generator.
    tilted=np.kron(np.eye(d),b.G)+np.kron(np.conj(b.G),np.eye(d))+math.exp(chi)*np.kron(np.conj(b.L),b.L)
    rho=np.zeros((d,d),complex);rho[0,0]=1
    out=(expm(tilted*T)@rho.reshape(-1,order='F')).reshape(d,d,order='F')
    occup=np.array([sum(n) for n in b.states]*2)
    mgf=float(np.sum(np.exp(chi*occup)*np.diag(out)).real)
    a=float(np.linalg.norm(b.c));bound=math.exp((a*T)**2*(math.e-1))
    assert 1-1e-7<=mgf<=bound+1e-7
    counts.append({'R':R,'N_plus_emitted_count_MGF':mgf,'proved_MGF_upper':bound,
                   'T':T,'initial':'system |0>, retained vacuum','chi':chi})

result={'scope':'Finite independent multi-port and dark-mode identities, plus counted full quantum-process MGF checks. No claim of independent proof audit.',
        'passive_networks':rows,'actual_emission_count_checks':counts}
(P/'results/generic_gaussian_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
