#!/usr/bin/env python3
"""Constructive response-exact positive rational bath; derivation in DERIVATION.md.

Dependencies: numpy, mpmath, sympy. No bath-fitting oracle or data service.
Numerics are checks of the analytic construction, not a correctness/novelty audit.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent


def nodes(L: int, m: int):
    return [mp.mpf(2) ** j * (1 + mp.mpf(k) / m)
            for j in range(-L, L) for k in range(m)] + [mp.mpf(2) ** L]


def repeated_dyadic_nodes(L: int, m: int):
    """Reciprocal grid; odd m gives the pole-separation proof in DERIVATION.md."""
    assert m % 2
    return [mp.mpf(2)**j for j in range(-L,L+1) for _ in range(m)]


def z2(x, aa):
    x = abs(mp.mpf(x))
    return mp.fprod(((a - x) / (a + x)) ** 2 for a in aa)


def majorant(x, aa):
    x = abs(mp.mpf(x))
    if not x:
        return 1 / (2 * sum(1 / a for a in aa))
    q = z2(x, aa)
    return x * (1 + q) / (1 - q)


def spectrum(w, aa, alpha=1):
    w = mp.mpf(w)
    if not w:
        return alpha * majorant(0, aa)
    x = abs(w)
    q = z2(x, aa)
    return 2 * alpha * x * (1 if w > 0 else q) / ((1 - q) * (1 + x*x)**2)


def variance_bound(L, m, alpha=1):
    q = mp.mpf(3) ** (-2*m)
    return alpha / mp.pi * (2 * mp.mpf(4)**(-L) + q/(1-q))


def excess_variance(aa, alpha=1):
    # Positive integrand: stable product, no subtraction of large Fourier sums.
    cuts = sorted(set([mp.mpf(0), mp.mpf(1)] + aa)) + [mp.inf]
    def integrand(x):
        if not x:
            return majorant(0, aa)
        q = z2(x, aa)
        return 2*x*q / ((1-q)*(1+x*x)**2)
    return alpha / mp.pi * mp.quad(integrand, cuts)


def choose_parameters(T, eps, q_norm=1., alpha=1.):
    if T <= 0 or q_norm <= 0 or alpha <= 0:
        return {"L": 1, "m": 1, "nodes": 3, "modes": 4, "channel_bound": 0.}
    eta = math.pi**2 * eps**2 / (8*q_norm*q_norm*T*T*alpha)
    L = max(1, math.ceil(math.log(4/eta, 4)))
    m = max(1, math.ceil(math.log((2+eta)/eta, 9)))
    if m % 2 == 0:
        m += 1
    var = float(variance_bound(L, m, alpha))
    return {"L": L, "m": m, "node_rule":"odd-m repeated reciprocal dyadic grid",
            "nodes": m*(2*L+1), "modes": m*(2*L+1)+1,
            "variance_bound": var,
            "channel_bound": min(2., 2*q_norm*T*math.sqrt(2*var/math.pi))}


def occupation_cutoff(T, coupling_norm, error):
    lam = (T*coupling_norm)**2
    K = max(1, math.ceil(math.e*lam))
    while True:
        log_bound = (math.log(2*coupling_norm*T) + .5*math.log(K+1)
                     + .5*(K*math.log(lam) - math.lgamma(K+1))) if lam else -math.inf
        if log_bound <= math.log(error):
            return {"K": K, "lambda": lam,
                    "channel_cutoff_bound": math.exp(log_bound)}
        K += 1


def realize(aa, alpha=1):
    """Monotone scalar root solves + explicit Gramian, at mp precision.

    The double pole -1 uses a two-state Jordan block. All other poles are simple.
    Avoid specially chosen nodes whose D also has a pole at 1 in this prototype.
    """
    aa = list(map(mp.mpf, aa))
    n = len(aa)
    theta = lambda y: sum(mp.atan(y/a) for a in aa)
    ss = []
    hi = 2*sum(aa)/mp.pi * mp.mpf('1.01')
    for j in range(1, n):
        lo, up = mp.mpf(0), hi
        for _ in range(4*mp.mp.dps):
            mid = (lo+up)/2
            if theta(mid) < j*mp.pi/2:
                lo = mid
            else:
                up = mid
        ss.append((lo+up)/2)
    if any(abs(s-1) < mp.mpf(10)**(-mp.mp.dps//3) for s in ss):
        raise ValueError('Pole at 1 needs a larger Jordan block; prototype excludes it.')
    kappa = mp.sqrt(alpha/(2*sum(aa)))
    b2 = kappa * mp.fprod(-1-1j*a for a in aa) / mp.fprod(s-1 for s in ss)
    b1 = b2 * (sum(1/(-1-1j*a) for a in aa) - sum(1/(s-1) for s in ss))
    residues = []
    for j,s in enumerate(ss):
        residues.append(kappa * mp.fprod(-s-1j*a for a in aa)
                        / ((1-s)**2 * mp.fprod(v-s for k,v in enumerate(ss) if k!=j)))
    d = n+1
    A0 = mp.zeros(d); b0 = mp.matrix([0,1]+[1]*(n-1))
    A0[0,0] = -1; A0[0,1] = 1; A0[1,1] = -1
    for j,s in enumerate(ss, 2):
        A0[j,j] = -s
    c0 = mp.matrix([[b2,b1]+residues])
    W = mp.zeros(d)
    W[0,0] = mp.mpf(1)/4
    W[0,1] = W[1,0] = mp.mpf(1)/4
    W[1,1] = mp.mpf(1)/2
    for j,s in enumerate(ss, 2):
        W[0,j] = W[j,0] = 1/(1+s)**2
        W[1,j] = W[j,1] = 1/(1+s)
        for k,t in enumerate(ss, 2):
            W[j,k] = 1/(s+t)
    L = mp.cholesky(W)
    A = L**-1*A0*L; ell = L**-1*b0; c = c0*L
    H = 1j*(A-A.H)/2
    gram_eigs = mp.eigsy(W, eigvals_only=True)
    norm = lambda X: max(abs(v) for v in X)
    def transfer(s):
        s = mp.mpc(s)
        return kappa*mp.fprod(s-1j*a for a in aa) / ((s+1)**2*mp.fprod(s+t for t in ss))
    freqs = [-10,-2,-1,-.13,0,.13,1,2,10] + [-a for a in aa]
    transfer_err = max(abs(abs(transfer(-1j*w))**2-spectrum(w,aa,alpha)) for w in freqs)
    response_err = max(abs(mp.im((c*mp.expm(A*t)*c.H)[0])
                           +alpha*t*mp.exp(-t)/4) for t in [0,.1,.7,1,3,8])
    return {"A": A, "ell": ell, "c": c, "H": H,
            "poles": ss, "gram_condition": gram_eigs[d-1]/gram_eigs[0],
            "physical_residual": norm(A+A.H+ell*ell.H),
            "gram_residual": norm(A0*W+W*A0.H+b0*b0.H),
            "transfer_error": transfer_err, "response_error": response_err,
            "coupling_variance": (c*c.H)[0]}


def exact_symbolic_checks():
    w,a,alpha,t = sp.symbols('w a alpha t', positive=True, real=True)
    A = sp.Matrix([[0,1],[-1,-2]])
    ell = sp.Matrix([0,2])
    c = sp.sqrt(alpha/(2*a))*sp.Matrix([[-sp.I*a,1]])/2
    ct = (c*sp.exp(A*t)*sp.conjugate(c.T))[0]
    expected = alpha*sp.exp(-t)*((1+a*a)+(a*a-1-2*sp.I*a)*t)/(8*a)
    h = (c*(-sp.I*w*sp.eye(2)-A).inv()*ell)[0]
    assert sp.simplify(ct-expected) == 0
    assert sp.simplify(h*sp.conjugate(h)-alpha*(w+a)**2/(2*a*(1+w*w)**2)) == 0
    assert A+A.H+ell*ell.H == sp.zeros(2)
    return {"two_mode_correlation": "exact PASS", "two_mode_spectrum": "exact PASS",
            "two_mode_CPTP_identity": "exact PASS"}


def save_complex_matrix(mat):
    return [[[float(mp.re(mat[i,j])),float(mp.im(mat[i,j]))]
             for j in range(mat.cols)] for i in range(mat.rows)]


def run_checks():
    mp.mp.dps = 65
    result = {"status":"derived single-worker checks; not external audit", "exact":exact_symbolic_checks()}
    approximations = []
    for L,m in [(1,1),(2,1),(3,1),(2,2),(3,2),(4,2),(4,3),(5,3)]:
        aa=nodes(L,m)
        var=excess_variance(aa)
        bound=variance_bound(L,m)
        assert var <= bound
        grid=[mp.mpf(10)**(mp.mpf(k)/5) for k in range(-30,31)]
        minimum=min(majorant(x,aa)-x for x in grid)
        assert minimum >= -mp.mpf('1e-55')
        response=max(abs(spectrum(x,aa)-spectrum(-x,aa)-2*x/(1+x*x)**2) for x in grid)
        assert response < mp.mpf('1e-55')
        zeros=max(abs(spectrum(-a,aa)) for a in aa)
        assert zeros == 0
        approximations.append({"L":L,"m":m,"nodes":len(aa),"modes":len(aa)+1,
                               "excess_variance":float(var),"proved_variance_bound":float(bound),
                               "response_residual":float(response),"thermal_node_residual":float(zeros)})
    result['positive_approximation_checks']=approximations
    realizations=[]
    for label,aa in [('single_node',[mp.mpf(1)]),('dyadic_L1',nodes(1,1)),('dyadic_L2',nodes(2,1)),('dyadic_L3',nodes(3,1))]:
        r=realize(aa)
        assert r['physical_residual'] < mp.mpf('1e-45')
        assert r['transfer_error'] < mp.mpf('1e-45')
        assert r['response_error'] < mp.mpf('1e-42')
        row={"label":label,"modes":len(aa)+1,
             **{k:float(mp.re(r[k])) for k in ['gram_condition','physical_residual','gram_residual','transfer_error','response_error','coupling_variance']},
             "poles":[float(x) for x in r['poles']]}
        realizations.append(row)
        (ROOT/'results'/f'realization_{label}.json').write_text(json.dumps({
            'nodes':[str(a) for a in aa],
            **{k:save_complex_matrix(r[k]) for k in ['A','H','ell','c']},'checks':row},indent=2))
    result['physical_realizations']=realizations
    costs=[]
    for T,eps in [(1,.1),(10,.1),(100,.1),(100,.01),(1000,.001)]:
        pp=choose_parameters(T,eps/3,alpha=.2)
        c2=.2/(2*math.pi)+pp['variance_bound']
        kk=occupation_cutoff(T,math.sqrt(c2),eps/3)
        costs.append({'T':T,'error':eps,**pp,**kk,
                      'bath_qubits':pp['modes']*math.ceil(math.log2(kk['K']+1))})
        assert pp['channel_bound']+kk['channel_cutoff_bound'] <= 2*eps/3
    result['conservative_full_memory_costs']=costs
    (ROOT/'results'/'analytic_checks.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:run_checks()
