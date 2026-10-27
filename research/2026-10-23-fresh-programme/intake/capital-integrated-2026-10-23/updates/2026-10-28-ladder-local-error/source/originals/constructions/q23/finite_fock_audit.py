#!/usr/bin/env python3
"""Independent physical-Fock audit of the constrained response formula.

This check has discrete finite-chain spectra and does NOT estimate a continuum
lifetime. It compares entire complex resolvent matrix elements at finite eta.
"""
import json
import math
from pathlib import Path
import numpy as np
from local_detuning_response import bisect


def build_one(n, g):
    d = 2+2*n
    h = np.diag(np.r_[3.,3.,np.full(n,5.),np.full(n,1.)])
    h[0,2] = h[2,0] = g
    h[1,2] = h[2,1] = g
    h[0,2+n] = h[2+n,0] = g/math.sqrt(2)
    h[1,2+n] = h[2+n,1] = -g/math.sqrt(2)
    for start in (2,2+n):
        for j in range(n-1):
            h[start+j,start+j+1] = h[start+j+1,start+j] = -.5
    return h


def lift_hardcore(h):
    d = len(h)
    basis = [(i,j) for i in range(d) for j in range(i,d)
             if not (i==j and i<2)]
    lookup = {pair:i for i,pair in enumerate(basis)}
    h2 = np.zeros((len(basis),len(basis)))
    for col,(i,j) in enumerate(basis):
        h2[col,col] = h[i,i]+h[j,j]
        if i==j:
            for k in range(d):
                if k != i and h[k,i] != 0:
                    pair = tuple(sorted((k,i)))
                    if pair in lookup:
                        h2[lookup[pair],col] += math.sqrt(2)*h[k,i]
        else:
            for old, other in ((i,j),(j,i)):
                for k in range(d):
                    if k != old and h[k,old] != 0:
                        pair = tuple(sorted((k,other)))
                        if pair in lookup:
                            h2[lookup[pair],col] += (math.sqrt(2) if k==other else 1)*h[k,old]
    assert np.max(abs(h2-h2.T)) < 1e-14
    return h2,basis


def parity_measure(n,g,plus):
    h = np.diag(np.r_[3.,np.full(n,5. if plus else 1.)])
    h[0,1] = h[1,0] = (math.sqrt(2) if plus else 1)*g
    for j in range(1,n):
        h[j,j+1] = h[j+1,j] = -.5
    en,vec = np.linalg.eigh(h)
    return en,vec[0]**2


def check(n,g=.2,perturbation='memory'):
    h2,basis = lift_hardcore(build_one(n,g))
    ev,vec = np.linalg.eigh(h2)
    idx = int(np.argmax(vec[basis.index((0,1))]**2))
    lam,psi = ev[idx],vec[:,idx]
    v = np.array([(int(i==0)+int(j==0)-int(i==1)-int(j==1)) for i,j in basis])
    if perturbation == 'memory':
        eta = v*psi
    elif perturbation == 'first_rung':
        wone=np.zeros((len(build_one(n,g)),len(build_one(n,g))))
        wone[2,2+n]=wone[2+n,2]=1
        wtwo,wbasis=lift_hardcore(wone)
        assert wbasis == basis
        eta=wtwo@psi
    else:
        raise ValueError(perturbation)
    xp,wp = parity_measure(n,g,True)
    xm,wm = parity_measure(n,g,False)
    dp = xp[:,None]+xp[None,:]-lam
    dm = xm[:,None]+xm[None,:]-lam
    lpprime = np.sum(wp[:,None]*wp[None,:]/dp**2)
    lmprime = np.sum(wm[:,None]*wm[None,:]/dm**2)
    norm = math.sqrt(2/(lpprime+lmprime))
    fp=np.ones_like(xp) if perturbation=='memory' else (xp-3)/(math.sqrt(2)*g)
    fm=np.ones_like(xm) if perturbation=='memory' else (xm-3)/g
    jp = np.sum((wp*fp)[None,:]/dp,axis=1)
    jm = np.sum((wm*fm)[None,:]/dm,axis=1)
    eta_harmonic = norm*(jp[:,None]*fm[None,:]+fp[:,None]*jm[None,:])
    product_weight = wp[:,None]*wm[None,:]
    result = dict(n=n,g=g,perturbation=perturbation,physical_dimension=len(basis),pair_energy=float(lam),
                  detuning_vector_norm=float(np.linalg.norm(eta)),
                  norm_from_spectral_representation=float(np.sqrt(np.sum(product_weight*eta_harmonic**2))),
                  forbidden_overlap=float(np.sum(product_weight*eta_harmonic)),
                  resolvent_checks=[])
    strength = abs(vec.T@eta)**2
    for shift,broadening in ((0.,.02),(.1,.05),(-.2,.01)):
        z = lam+shift+1j*broadening
        direct = np.sum(strength/(ev-z))
        den = xp[:,None]+xm[None,:]-z
        kval = np.sum(product_weight/den)
        cval = np.sum(product_weight*eta_harmonic/den)
        dval = np.sum(product_weight*eta_harmonic**2/den)
        schur = dval-cval*cval/kval
        error = abs(direct-schur)
        assert error < 2e-10, (n,z,direct,schur,error)
        result['resolvent_checks'].append(dict(shift=shift,broadening=broadening,
               direct_real=float(direct.real),direct_imag=float(direct.imag),
               rank_formula_real=float(schur.real),rank_formula_imag=float(schur.imag),
               absolute_difference=float(error)))
    assert abs(np.linalg.norm(eta)-result['norm_from_spectral_representation'])<1e-10
    assert abs(result['forbidden_overlap'])<1e-10
    return result


if __name__ == '__main__':
    result = dict(cases=[check(n,perturbation=kind) for kind in ['memory','first_rung'] for n in [6,10,14]],
                  scope='finite-volume resolvent identities only; no finite-chain linewidth')
    Path(__file__).with_name('finite_fock_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
