#!/usr/bin/env python3
"""Finite cubature and classical-basis checks (floating point, not formal proof).

Constructs explicit weighted complex projective designs using Gauss-Jacobi
quadrature for Dirichlet stick variables and roots of unity for phases.
The exact construction and proof are in RESEARCH_PROOF.md. SciPy evaluates
algebraic quadrature nodes numerically; it does not return exact certificates.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path
import numpy as np
import scipy
from scipy.special import roots_jacobi
from verify_construction import coherent, occupations, RNG

HERE=Path(__file__).resolve().parent
CHECKS=[]
TOL=2e-10

def check(name, residual, **scope):
    residual=float(residual)
    if not math.isfinite(residual) or residual>TOL:
        raise ArithmeticError(f'{name}: {residual}')
    CHECKS.append({'name':name,'status':'pass','residual':residual,
                   'tolerance':TOL,'scope':scope})

def finite_design(d:int, degree:int):
    if d<2 or degree<1:
        raise ValueError('Requires d>=2 and degree>=1')
    q=(degree+2)//2
    phases=degree+1
    size=(q*phases)**(d-1)
    if size>20000:
        raise ValueError(f'Requested {size} points; this diagnostic is capped at 20000')
    rules=[]
    for j in range(d-1):
        # t_j ~ Beta(1,d-j-1), using zero-based j.
        beta=d-j-1
        nodes,weights=roots_jacobi(q,beta-1,0)
        nodes=(nodes+1)/2
        weights=weights/weights.sum()
        rules.append((nodes,weights))
    vectors=[]; ww=[]
    for indices in itertools.product(range(q),repeat=d-1):
        probs=[]; remaining=1.0; weight=1.0
        for j,index in enumerate(indices):
            node,w=rules[j][0][index],rules[j][1][index]
            probs.append(remaining*node)
            remaining*=1-node
            weight*=w
        probs.append(remaining)
        for exponents in itertools.product(range(phases),repeat=d-1):
            angle=np.array(list(exponents)+[0],float)*(2*np.pi/phases)
            vectors.append(np.sqrt(probs)*np.exp(1j*angle))
            ww.append(weight/phases**(d-1))
    return np.asarray(vectors),np.asarray(ww)

def main():
    outcomes=[]
    for d,degree,length in ((3,4,1),(2,8,2)):
        states,w=finite_design(d,degree)
        check(f'design_normalization_d{d}_t{degree}',
              max(abs(w.sum()-1),np.max(np.abs(np.sum(abs(states)**2,axis=1)-1))))
        if np.min(w)<=0:
            raise ArithmeticError('Nonpositive weight')
        for t in range(1,degree+1):
            v=np.asarray([coherent(psi,t) for psi in states])
            moment=(v.T*w)@v.conj()
            dim=math.comb(d+t-1,t)
            check(f'ALL_finite_cubature_moment_d{d}_degree{degree}_order{t}',
                  np.max(np.abs(moment-np.eye(dim)/dim)),
                  points=len(w),symmetric_dimension=dim)
        counts=[2**r for r in range(length+1)]
        sizes=[math.comb(d+k-1,k) for k in counts]
        offsets=[0]+[int(z) for z in np.cumsum(sizes)]
        total=offsets[-1]; kmax=counts[-1]
        blocks=[np.asarray([coherent(psi,k) for psi in states]) for k in counts]
        # Exact-moment state-estimation measurement, evaluated numerically.
        overlaps=abs(states.conj()@states.T)**2
        for r,k in enumerate(counts[1:],start=1):
            dim=sizes[r]
            povm_sum=dim*(blocks[r].T*w)@blocks[r].conj()
            fidelity=dim*np.sum(w[:,None]*w[None,:]*overlaps**(k+1))
            check(f'finite_covariant_EB_POVM_d{d}_k{k}',
                  np.max(abs(povm_sum-np.eye(dim))))
            check(f'optimal_decoded_estimation_score_d{d}_k{k}',
                  abs(fidelity-(k+1)/(k+d)),
                  attained_fidelity=float(fidelity),
                  limitation='Matches decoded fidelity, not full-family trace reconstruction error')
        theoretical=sum(math.comb(d+k-1,k)/math.comb(d+2*k-1,2*k) for k in counts[1:])
        beta=min(1.0,math.sqrt(theoretical))
        averages=[]
        for trial in range(12):
            z=RNG.normal(size=(total,total))+1j*RNG.normal(size=(total,total))
            basis,_=np.linalg.qr(z)
            g=np.zeros((len(w),total))
            for r in range(1,length+1):
                overlaps_basis=blocks[r].conj()@basis[offsets[r]:offsets[r+1]]
                g+=abs(overlaps_basis)**2
            maximum=np.max(g,axis=1)
            avg=float(w@maximum)
            # Direct finite evaluation of the Jensen moment estimate and max bound.
            summed_moment=float(np.sum(w[:,None]*g**2))
            check(f'finite_basis_SECOND_moment_inequality_d{d}_L{length}_trial{trial}',
                  max(0,summed_moment-theoretical,avg-beta),
                  basis_trial=trial,average_maximum=avg,analytic_upper_bound=beta)
            averages.append(avg)
        outcomes.append({'d':d,'L':length,'design_degree':degree,'point_count':len(w),
                         'random_bases_tested':len(averages),
                         'largest_average_diagonal_overlap':max(averages),
                         'basis_independent_analytic_bound':beta})
    receipt={'status':'all_executed_checks_passed','check_count':len(CHECKS),
             'numpy':np.__version__,'scipy':scipy.__version__,
             'scope':'Floating-point complete finite ensembles and finitely many bases; all-basis/all-dimension statements rest on the proof.',
             'checks':CHECKS,'outcomes':outcomes}
    (HERE/'finite_design_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'check_count':len(CHECKS),
                      'max_residual':max(c['residual'] for c in CHECKS),'outcomes':outcomes},indent=2))

if __name__=='__main__':main()
