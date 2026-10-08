#!/usr/bin/env python3
"""Exact finite-time certificate for N=4 collective thermalization.

The pass/fail decisions use rational arithmetic, not rounded eigenvalues.
Model: Gamma[(nu+1)D[J_-]+nu D[J_+]], nu=1/5, Gamma*t=8,
initial state I/16. Uniformization has an explicit rational truncation bound.
Requires Python 3.10+ and sympy. Writes certificate.json beside this script.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as s

R = s.Rational
N, DIM = 4, 16
NU, T, RATE, TERMS = R(1,5), R(8), R(9), 400

def identity(n: int) -> s.Matrix:
    return s.eye(n)

def swap_matrix(a: int, b: int) -> s.Matrix:
    result = s.zeros(DIM)
    for x in range(DIM):
        y = x
        if ((x >> a) & 1) != ((x >> b) & 1):
            y ^= (1 << a) | (1 << b)
        result[y, x] = 1
    return result

def partial_transpose_qubit(a: s.Matrix, qubit: int) -> s.Matrix:
    result = s.zeros(DIM)
    bit = 1 << qubit
    for i in range(DIM):
        for j in range(DIM):
            ni = (i & ~bit) | (j & bit)
            nj = (j & ~bit) | (i & bit)
            result[ni, nj] = a[i, j]
    return result

def positive_ldl(a: s.Matrix) -> list[s.Rational]:
    """Exact no-pivot LDL: positive pivots certify strict positive definiteness."""
    n = a.rows
    l = s.eye(n)
    pivots = []
    for k in range(n):
        pivot = a[k,k] - sum(l[k,r]**2*pivots[r] for r in range(k))
        pivot = s.cancel(pivot)
        if not (pivot > 0):
            raise AssertionError(f'Nonpositive LDL pivot {k}')
        pivots.append(pivot)
        for i in range(k+1, n):
            l[i,k] = s.cancel((a[i,k] - sum(l[i,r]*l[k,r]*pivots[r]
                             for r in range(k))) / pivot)
    return pivots

def population(j: int) -> tuple[s.Matrix, s.Rational]:
    d = 2*j+1
    q = s.zeros(d)
    for r in range(d):
        # r=m+j, so r=0 is the ground level.
        if r > 0:
            q[r-1,r] = (NU+1)*r*(d-r)
        if r < d-1:
            q[r+1,r] = NU*(r+1)*(d-r-1)
        q[r,r] = -sum(q[u,r] for u in range(d) if u != r)
    p = s.eye(d)+q/RATE
    assert all(x >= 0 for x in p)
    assert all(sum(p[u,r] for u in range(d)) == 1 for r in range(d))
    mu = RATE*T
    term, normalizer = R(1), R(1)
    vector = s.ones(d,1)/d
    accumulator = vector.copy()
    for r in range(1, TERMS+1):
        term *= mu/r
        vector = p*vector
        accumulator += term*vector
        normalizer += term
    tail_upper = term*mu/(TERMS+1)/(1-mu/(TERMS+2))
    epsilon = s.cancel(2*tail_upper/normalizer)
    return accumulator/normalizer, epsilon

def main() -> None:
    ident = identity(DIM)
    jz_values = [R(N,2)-int(i).bit_count() for i in range(DIM)]
    jz = s.diag(*jz_values)
    j2 = R(N*(4-N),4)*ident
    for a in range(N):
        for b in range(a+1,N):
            j2 += swap_matrix(a,b)
    rho = s.zeros(DIM)
    eps = R(0)
    for j in (0,1,2):
        proj = ident.copy()
        for k in (0,1,2):
            if k != j:
                proj = proj*(j2-k*(k+1)*ident)/(j*(j+1)-k*(k+1))
        probs, error = population(j)
        eps = max(eps,error)
        for r in range(2*j+1):
            m = r-j
            mask = s.diag(*[int(z==m) for z in jz_values])
            rho += R(2*j+1,DIM)*probs[r]*proj*mask
    assert s.trace(rho)==1 and rho==rho.T
    assert s.trace(rho*j2)==3
    margin = R(1,20000)
    # Permutation invariance covers the remaining singleton cuts.
    for a in range(N-1):
        swap = swap_matrix(a,a+1)
        assert swap*rho*swap==rho
    pivots = positive_ldl(partial_transpose_qubit(rho,0)-margin*ident)
    magnetization = -s.trace(rho*jz)
    witness = R(N,4)-magnetization**2
    assert witness < -R(4,100)
    assert margin > eps

    # Groups A=(0,1), B=(2,3), each keeping its triplet.
    triplet_a = (ident+swap_matrix(0,1))/2
    triplet_b = (ident+swap_matrix(2,3))/2
    project = triplet_a*triplet_b
    qbath = NU/(1+NU)
    # K†K=q^(2-J_z), two group filters K_j, j=1.
    filter_square = s.diag(*[qbath**(2-z) for z in jz_values])
    herald_probability = s.trace(rho*project*filter_square)
    # Unique A-spin=1, B-spin=1 total-singlet component is invariant.
    singlet_numerator = qbath**2/R(DIM)
    fidelity = singlet_numerator/herald_probability
    assert herald_probability > R(49,10000)
    assert fidelity > R(7,20)

    # Bounds also cover arbitrary perturbations with ||delta rho||_1<=eta.
    eta = R(1,100000)
    total = eta+eps
    # PT operator error <= Frobenius error <= trace error.
    assert margin > total
    # Change in <J²>-|<J>|² <= ||J²||*eta + 2||<J>||*sqrt(3)||Jz||*eta
    # + 3||Jz||² eta²; conservative rational sqrt(3)<2.
    witness_error = R(6)*total + 8*magnetization*total + 12*total**2
    assert witness+witness_error < 0
    assert herald_probability-total > R(49,10000)
    assert (singlet_numerator-total)/(herald_probability+total) > R(7,20)

    result = {
        'status': 'PASS: exact rational inequalities; no proof-assistant certification',
        'model': {'N':N,'nu':str(NU),'Gamma_t':str(T),'jump_normalization':'unnormalized J_±'},
        'uniformization': {'rate':str(RATE),'mu':str(RATE*T),'K':TERMS,
                           'trace_error_upper_display':str(s.N(eps,12)),
                           'trace_error_upper_exact':str(eps)},
        'strict_singleton_PPT_margin_certified':str(margin),
        'all_16_LDL_pivots_positive':bool(all(x>0 for x in pivots)),
        'permutation_symmetry_verified':True,
        'witness_minus_N_over_2_display':str(s.N(witness,16)),
        'magnetization_display':str(s.N(magnetization,16)),
        'herald_probability_display':str(s.N(herald_probability,16)),
        'singlet_fidelity_display':str(s.N(fidelity,16)),
        'arbitrary_trace_norm_perturbation_certified':str(eta),
        'limitations': ['PPT certified, not finite-time singleton separability',
                       'No finite-time depth certificate',
                       'Heralded state is mixed; distillation overhead not included',
                       'Uniform collective coupling assumed'],
    }
    path=Path(__file__).with_name('certificate.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='uniformization'},indent=2))
    print('Uniformization trace error bound:',s.N(eps,12))
    print('Saved:',path)

if __name__=='__main__':
    main()
