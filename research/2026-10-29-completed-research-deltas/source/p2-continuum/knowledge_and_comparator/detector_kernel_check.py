#!/usr/bin/env python3
"""Independent finite-Fock check of the continuum coherent detector identity.

The analytic kernel never truncates Fock space. The comparison does, at total
number N, and its coefficient omissions are reported. This is a numerical
diagnostic, not interval validation or a P2-device model.
"""
from pathlib import Path
from itertools import combinations
from math import comb, factorial
import json
import numpy as np
from scipy.linalg import eigh
from scipy.stats import poisson


def gamma_matrix(b, nmax):
    blocks = []
    for n in range(nmax + 1):
        mat = np.zeros((n + 1, n + 1), complex)
        for k in range(n + 1):
            for l in range(n + 1):
                value = 0j
                for u in range(max(0, l - n + k), min(k, l) + 1):
                    value += (comb(k, u) * comb(n-k, l-u)
                              * b[0, 0]**u * b[1, 0]**(k-u)
                              * b[0, 1]**(l-u)
                              * b[1, 1]**(n-k-l+u))
                mat[l, k] = value * np.sqrt(
                    factorial(l)*factorial(n-l)
                    / (factorial(k)*factorial(n-k)))
        blocks.append(mat)
    dim = (nmax+1)*(nmax+2)//2
    result = np.zeros((dim, dim), complex)
    offset = 0
    for block in blocks:
        size = len(block)
        result[offset:offset+size, offset:offset+size] = block
        offset += size
    return result


def coherent(alpha, nmax):
    return np.array([np.exp(-np.vdot(alpha, alpha).real/2)
                     * alpha[0]**k * alpha[1]**(n-k)
                     / np.sqrt(factorial(k)*factorial(n-k))
                     for n in range(nmax+1) for k in range(n+1)])


def kernel(beta, alpha, effect):
    return np.exp(-(np.vdot(beta, beta).real+np.vdot(alpha, alpha).real)/2
                  + np.vdot(beta, (np.eye(2)-effect)@alpha))


def powerset(values):
    for n in range(len(values)+1):
        yield from combinations(values, n)


def run():
    nmax = 14
    e1 = .4*np.array([[1., 0.], [0., 0.]])
    e2 = .2*np.ones((2, 2))
    effects = [e1, e2]
    alphas = [np.array([.7, .3j]), np.array([-.5, .4]),
              np.array([.2j, -.6])]
    bs = [np.diag([.8, .2]).astype(complex),
          np.array([[0, .4j], [.3, 0]], complex),
          np.array([[.2, .1], [.15j, -.5]], complex)]
    overlap = np.array([[kernel(b, a, np.zeros((2, 2)))
                         for a in alphas] for b in alphas])
    metric = sum(overlap[b, a]*(bs[b].conj().T@bs[a])
                 for a in range(3) for b in range(3))
    ev, eu = eigh(metric)
    invsqrt = (eu/np.sqrt(ev))@eu.conj().T
    bs = [b@invsqrt for b in bs]
    v = sum(np.kron(b, coherent(a, nmax)[:, None])
            for a, b in zip(alphas, bs))
    fdim = (nmax+1)*(nmax+2)//2
    v3 = v.reshape(2, fdim, 2)
    nock = {}
    for subset in powerset([0, 1]):
        e = sum((effects[r] for r in subset), np.zeros((2, 2)))
        nock[subset] = gamma_matrix(np.eye(2)-e, nmax)
    results = {}
    probs = {}
    choi_sum = np.zeros((4, 4), complex)
    for clicked in powerset([0, 1]):
        empty = tuple(r for r in [0, 1] if r not in clicked)
        operator = np.zeros((fdim, fdim), complex)
        kval = np.zeros((3, 3), complex)
        for extra in powerset(list(clicked)):
            subset = tuple(sorted(empty+extra))
            sign = (-1)**len(extra)
            operator += sign*nock[subset]
            e = sum((effects[r] for r in subset), np.zeros((2, 2)))
            kval += sign*np.array([[kernel(b, a, e) for a in alphas]
                                    for b in alphas])
        direct = np.einsum('sbi,cb,tcj->sitj', v3, operator,
                           v3.conj(), optimize=True).reshape(4, 4)
        analytic = sum(kval[b, a]*np.outer(bs[a].ravel(), bs[b].ravel().conj())
                       for a in range(3) for b in range(3))
        choi_sum += analytic
        label = ''.join('1' if r in clicked else '0' for r in [0, 1])
        prob = np.trace(analytic).real/2
        probs[label] = float(prob)
        results[label] = {
            'choi_spectral_difference':float(np.linalg.norm(direct-analytic, 2)),
            'analytic_min_choi_eigenvalue':float(eigh(analytic,eigvals_only=True)[0]),
            'fock_effect_min_eigenvalue':float(eigh(operator,eigvals_only=True)[0]),
            'probability_maximally_mixed_source':float(prob)}
    joint = nock[(0, 1)]
    incorrect = nock[(0,)]@nock[(1,)]
    output = {
        'status':'numerical diagnostic; no device or interval certificate',
        'total_number_cutoff':nmax,
        'fock_dimension':fdim,
        'sum_effects_largest_eigenvalue':float(eigh(e1+e2,eigvals_only=True)[-1]),
        'effect_commutator_norm':float(np.linalg.norm(e1@e2-e2@e1, 2)),
        'poisson_packet_tail_max':float(max(poisson.sf(nmax, np.vdot(a,a).real) for a in alphas)),
        'finite_fock_isometry_defect':float(np.linalg.norm(v.conj().T@v-np.eye(2), 2)),
        'joint_no_click_vs_wrong_input_product_norm':float(np.linalg.norm(joint-incorrect,2)),
        'wrong_input_product_nonhermiticity':float(np.linalg.norm(incorrect-incorrect.conj().T,2)),
        'record_probability_sum':float(sum(probs.values())),
        'two_click_covariance_mixed_input':float(probs['11']-(probs['10']+probs['11'])*(probs['01']+probs['11'])),
        'records':results}
    assert max(r['choi_spectral_difference'] for r in results.values()) < 2e-12
    assert min(r['analytic_min_choi_eigenvalue'] for r in results.values()) > -2e-13
    assert abs(sum(probs.values())-1) < 2e-13
    assert output['joint_no_click_vs_wrong_input_product_norm'] > .05
    dest = Path(__file__).with_suffix('.json')
    dest.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    run()
