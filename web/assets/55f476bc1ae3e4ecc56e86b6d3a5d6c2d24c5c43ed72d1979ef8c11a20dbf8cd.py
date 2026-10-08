#!/usr/bin/env python3
"""Independent exact normalization and numerical counterexample searches.

The candidate's verification script is not imported or read. Exact arithmetic
checks algebraic fixtures; matrix and leverage checks are diagnostics only.
"""
from collections import Counter
from fractions import Fraction as F
from functools import reduce
from itertools import product
from math import comb, factorial, sqrt
from pathlib import Path
import json
import numpy as np

OUT = Path(__file__).parent
I = np.eye(2, dtype=complex)
P = [np.array([[0, 1], [1, 0]], complex),
     np.array([[0, -1j], [1j, 0]], complex),
     np.array([[1, 0], [0, -1]], complex)]


def kron(items):
    return reduce(np.kron, items, np.array([[1.0]], complex))


def df(n):
    ans = 1
    for a in range(n, 0, -2):
        ans *= a
    return ans


def counts(k):
    return [(a, b, k-a-b) for a in range(k+1) for b in range(k-a+1)]


def mult(n):
    return factorial(sum(n)) // reduce(lambda a, b: a*b,
                                      (factorial(x) for x in n), 1)


def sphere_moment(n):
    if any(a % 2 for a in n):
        return F(0)
    return F(reduce(lambda a, b: a*b, (df(a-1) for a in n), 1),
             df(sum(n)+1))


def sphere_checks():
    rng = np.random.default_rng(4001)
    checks = []
    for k in range(1, 8):
        for trial in range(4):
            tensor = {n: int(rng.integers(-8, 9)) for n in counts(k)}
            coeff = {n: mult(n)*v for n, v in tensor.items()}
            integral = sum(F(a*b)*sphere_moment(tuple(x+y for x,y in zip(n,m)))
                           for n,a in coeff.items() for m,b in coeff.items())
            frob = sum(mult(n)*v*v for n,v in tensor.items())
            traced_sum = 0
            for s in range(k//2+1):
                residual = k-2*s
                trace_norm = 0
                for n in counts(residual):
                    tr = 0
                    for axes in product(range(3), repeat=s):
                        shift = Counter(axes)
                        original = tuple(n[a]+2*shift[a] for a in range(3))
                        tr += tensor[original]
                    trace_norm += mult(n)*tr*tr
                pairing_count = comb(k, 2*s)**2 * df(2*s-1)**2 * factorial(k-2*s)
                traced_sum += pairing_count * trace_norm
            assert integral == F(traced_sum, df(2*k+1))
            lower = F(factorial(k)*frob, df(2*k+1))
            assert integral >= lower
            checks.append({'k':k, 'trial':trial, 'excess':str(integral-lower)})
    return checks


def shifted_norm(N, k, beta):
    return sum(F(comb(k,l)**2, comb(N,l))*beta**(2*(k-l))
               for l in range(k+1))


def diag_centered(N,k,h,beta):
    # h positive eigenvalues of u.sigma among N independent white qubits.
    return sum(F(comb(h,i)*comb(N-h,k-i), comb(N,k)) *
               (1-beta)**i * (-1-beta)**(k-i)
               for i in range(max(0,k-(N-h)),min(k,h)+1))


def exact_norm_checks():
    small, transfer = 0, 0
    for N in range(1, 15):
        for k in range(1,min(N,6)+1):
            for beta in (F(1,7), F(-2,5)):
                direct = sum(F(comb(N,h),2**N)*diag_centered(N,k,h,beta)**2
                             for h in range(N+1))
                assert direct == shifted_norm(N,k,beta)
                small += 1
    for N in (1,2,3,4,7,8,11,12,16,20,32):
        for k in range(1,min(N,6)+1):
            beta = F(1,10)
            block_trace = F(0)
            for twice_j in range(N%2,N+1,2):
                h0=(N-twice_j)//2
                multiplicity=comb(N,h0)-(comb(N,h0-1) if h0 else 0)
                pj=F((twice_j+1)*multiplicity,2**N)
                values=[diag_centered(N,k,(N+twice_m)//2,beta)**2
                        for twice_m in range(-twice_j,twice_j+1,2)]
                block_trace += pj*sum(values)/F(twice_j+1)
            assert block_trace == shifted_norm(N,k,beta)
            transfer += 1
    inequalities = 0
    for N in (2,3,8,32,64,128,256,384,512,1024):
        for k in range(1,min(N,16)+1):
            beta2=F(3,N)
            norm=sum(F(comb(k,l)**2,comb(N,l))*beta2**(k-l)
                     for l in range(k+1))
            assert norm <= F(4**k,comb(N,k))
            for l in range(k+1):
                m=k-l
                lhs=F(comb(N,k)*comb(k,l)**2,comb(N,l))*beta2**m
                rhs=F(comb(k,m)*3**m,factorial(m))
                assert lhs <= rhs
            inequalities += 1
    rational_derivative=(F(10)+F(135,256))*F(128,119)**5
    assert rational_derivative == F(7381975040,487010951) < 16
    assert 108*16*F(9,2)**2 == 34992
    assert F(3,256) < F(1,81)
    return {'direct_HS_identities':small,'exact_white_block_trace_identities':transfer,
            'shifted_upper_bound_cases':inequalities,
            'derivative_upper_bound':str(rational_derivative),
            'constant':34992}


def grid_checks():
    results=[]
    for k in (1,2,3,4,6,8,12):
        for j in (0,.5,1,2.5,4*k*k-.5,4*k*k,8*k*k,40*k*k):
            size=int(2*j+1)
            x=np.linspace(-1,1,size) if size>1 else np.array([0.0])
            degree=min(k,size-1)
            design=np.polynomial.chebyshev.chebvander(x,degree)
            Q,_=np.linalg.qr(design,mode='reduced')
            # Exact mathematical maximum over the discrete polynomial subspace;
            # QR here evaluates it numerically, without sampling polynomials.
            ratio=float(size*np.max(np.sum(Q*Q,axis=1)))
            assert ratio <= 36*k*k*(1+1e-11)
            results.append({'k':k,'j':j,'max_grid_to_mean_ratio':ratio,
                            'claimed_upper':36*k*k})
    return results


def make_spin_actions(twice_j):
    j=twice_j/2
    m=np.arange(j,-j-1,-1)
    a=np.sqrt(np.maximum(0,j*(j+1)-m[1:]*(m[1:]+1)))
    def act(v):
        plus=np.zeros_like(v); minus=np.zeros_like(v)
        plus[:-1]=a*v[1:]; minus[1:]=a*v[:-1]
        return ((plus+minus)/2,(plus-minus)/(2j),m*v)
    return act


def sector_fixture(N, mode):
    sectors=[]
    for tj in range(N%2,N+1,2):
        h=(N-tj)//2
        mj=comb(N,h)-(comb(N,h-1) if h else 0)
        weight=((tj+1)*mj)/(2**N)
        dim=tj+1
        v=np.zeros(dim,complex)
        if mode=='highest':
            v[0]=1
        elif dim==1:
            v[0]=1
        else:
            amplitudes=np.array([sqrt(.65),sqrt(.25)*np.exp(1j*(.2+.07*tj)),
                                 sqrt(.10)*np.exp(1j*(.7+.11*tj))])[:min(3,dim)]
            amplitudes/=np.linalg.norm(amplitudes)
            v[:len(amplitudes)]=amplitudes
        sectors.append((weight,v,make_spin_actions(tj)))
    return sectors


def directional_moment(sectors,N,k,u):
    ans=0.0
    for w,v,act in sectors:
        if w==0:
            continue
        eminus=np.zeros_like(v); e=v.copy()
        for l in range(k):
            actions=act(e)
            se=2*sum(u[a]*actions[a] for a in range(3))
            enext=(se-(N-l+1)*eminus)/(l+1)
            eminus,e=e,enext
        ans += w*np.vdot(v,e).real/comb(N,k)
    return ans


def coefficients_from_directions(sectors,N,r):
    rng=np.random.default_rng(7300+N)
    coefs={0:{(0,0,0):1.0}}
    condition=[]
    for k in range(1,r+1):
        ns=counts(k)
        # Oversampling improves conditioning; all equations concern the same
        # exact degree-k homogeneous polynomial, not a fitted approximation.
        directions=rng.normal(size=(4*len(ns),3))
        directions/=np.linalg.norm(directions,axis=1)[:,None]
        design=np.array([[np.prod(u**np.array(n))*mult(n) for n in ns]
                         for u in directions])
        values=np.array([directional_moment(sectors,N,k,u) for u in directions])
        sol,residual,rank,singular=np.linalg.lstsq(design,values,rcond=None)
        assert rank==len(ns)
        assert np.max(np.abs(design@sol-values)) < 1e-11
        condition.append(float(singular[0]/singular[-1]))
        coefs[k]=dict(zip(ns,sol))
    return coefs,condition


def marginal_from_coefficients(coefs,r):
    rho=np.zeros((2**r,2**r),complex)
    for labels in product(range(4),repeat=r):
        n=tuple(labels.count(a+1) for a in range(3)); k=sum(n)
        rho += coefs[k][n]*kron([I if a==0 else P[a-1] for a in labels])/(2**r)
    return (rho+rho.conj().T)/2


def matrix_check(N,r,mode):
    sectors=sector_fixture(N,mode)
    coefs,condition=coefficients_from_directions(sectors,N,r)
    rho=marginal_from_coefficients(coefs,r)
    b=np.array([coefs[1][tuple(1 if a==j else 0 for a in range(3))]
                for j in range(3)])
    tau=(I+sum(b[a]*P[a] for a in range(3)))/2
    sigma=kron([tau]*r); inv=np.linalg.inv(sigma); delta=rho-sigma
    chi=float(np.trace(delta@delta@inv).real)
    petz=float(np.trace(rho@rho@inv).real)-1
    assert abs(chi-petz)<3e-12
    A=[P[a]-b[a]*I for a in range(3)]
    G=np.array([[np.trace(tau@A[a]@A[c]) for c in range(3)] for a in range(3)])
    t=np.linalg.norm(b)
    assert np.max(np.abs(np.linalg.eigvalsh(G)-np.sort([1-t,1+t,1-t*t])))<2e-12
    GI=np.linalg.inv(G); naive_GI=np.linalg.inv(G.real)
    parseval=0.; naive=0.; degree1=0.
    for k in range(1,r+1):
        ds=np.array([np.trace(rho@kron([A[a] for a in axes]+[I]*(r-k))).real
                     for axes in product(range(3),repeat=k)])
        if k==1:
            degree1=float(np.linalg.norm(ds))
        parseval += comb(r,k)*np.vdot(ds,kron([GI]*k)@ds).real
        naive += comb(r,k)*np.vdot(ds,kron([naive_GI]*k)@ds).real
    assert abs(parseval-chi)<5e-12
    assert degree1<2e-12
    er,vr=np.linalg.eigh(rho); es,vs=np.linalg.eigh(sigma)
    assert er.min()>-3e-12 and es.min()>0
    overlap=np.abs(vr.conj().T@vs)**2
    D=float(np.sum(np.where(er>0,er*np.log(np.maximum(er,1e-300)),0))-
            np.sum(er[:,None]*overlap*np.log(es)[None,:]))
    traceD=float(np.sum(np.abs(np.linalg.eigvalsh(delta)))/2)
    assert D<=np.log1p(chi)+3e-12
    assert traceD<=sqrt(max(chi,0))/2+3e-12
    assert chi <= 34992*(r/N)**2 + 3e-12
    return {'N':N,'r':r,'mode':mode,'legal_range':r<=N/128,
            'bloch_norm':float(t),'chi_P':chi,'relative_entropy':D,
            'trace_distance':traceD,'theorem_upper_bound':34992*(r/N)**2,
            'parseval_error':abs(parseval-chi),'degree1_norm':degree1,
            'naive_real_Gram_error':abs(naive-chi),
            'noncommutator_norm':float(np.linalg.norm(rho@sigma-sigma@rho)),
            'rho_min_eigenvalue':float(er.min()),
            'interpolation_condition_max':max(condition)}


def main():
    exact=exact_norm_checks(); spheres=sphere_checks(); grids=grid_checks()
    matrices=[matrix_check(N,r,mode)
              for N,r in ((256,2),(384,3),(512,4),(1024,4))
              for mode in ('highest','coherent_superposition')]
    assert any(x['noncommutator_norm']>1e-10 for x in matrices)
    assert any(x['naive_real_Gram_error']>1e-12 for x in matrices)
    result={'status':'all independent assertions passed',
            'candidate_verification_code_read':False,
            'thermal_proof_read':False,
            'scope':'exact algebraic fixtures; numerical quantum/grid diagnostics, not proof validation',
            'exact_normalizations':exact,'sphere_pairing_checks':spheres,
            'polynomial_grid_leverage_checks':grids,
            'legal_large_N_quantum_matrix_cases':matrices}
    (OUT/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'matrix_cases':len(matrices),
                      'max_parseval_error':max(x['parseval_error'] for x in matrices),
                      'max_noncommutator_norm':max(x['noncommutator_norm'] for x in matrices),
                      'largest_naive_real_Gram_error':max(x['naive_real_Gram_error'] for x in matrices),
                      'output':str(OUT/'independent_checks.json')},indent=2))


if __name__=='__main__':
    main()
