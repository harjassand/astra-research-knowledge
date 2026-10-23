#!/usr/bin/env python3
"""Exact sharpness identities plus bounded floating diagnostics; no theorem oracle."""
from fractions import Fraction as F
from pathlib import Path
import json
import platform
import time
import sys
import numpy as np


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b, scale=F(1)):
    return [[x + scale * y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, k):
    return [[k*x for x in row] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def exact_checks():
    eye = [[F(1), F(0)], [F(0), F(1)]]
    p = [[F(1), F(0)], [F(0), F(0)]]
    cases = []
    for s, c in [(F(3, 5), F(4, 5)), (F(20, 101), F(99, 101)),
                 (F(5, 13), F(12, 13))]:
        require(s*s+c*c == 1, 'Pythagorean pair')
        gamma, eta = F(101, 100), F(1)
        a = [[F(0), F(0)], [F(0), gamma]]
        b = scale([[s*s, s*c], [s*c, c*c]], gamma)
        q = add(eye, scale(b, 1/gamma), F(-1))
        m = add(p, q, F(-1))
        e = gamma*s
        perturbation = add(a, b, F(-1))
        w = scale(add(eye, scale(m, 1/s)), F(1, 2))
        require(mm(a, a) == scale(a, gamma), 'A spectrum polynomial')
        require(mm(b, b) == scale(b, gamma), 'B spectrum polynomial')
        require(mm(q, q) == q, 'Q projection')
        require(mm(m, m) == scale(eye, s*s), 'projection difference norm')
        require(mm(perturbation, perturbation) == scale(eye, e*e), 'perturbation norm')
        require(mm(w, w) == w and trace(w) == 1, 'pure probe projector')
        pa, pb = trace(mm(w, p)), trace(mm(w, q))
        require(pa == (1+s)/2 and pb == (1-s)/2, 'weighted CDF values')
        require(pa-pb == s and gamma > eta and gamma > e, 'horizontal failure')
        # sqrt(pb*(1-pb))=c/2, so the stronger upper bound at leakage s is exact.
        u_exact = c*c*pb+s*s*(1-pb)+s*c*c
        require(u_exact == pa, 'probability-dependent sharpness')
        cases.append({'s': str(s), 'c': str(c), 'gamma': str(gamma),
                      'eta': str(eta), 'error_norm': str(e),
                      'F_A': str(pa), 'F_B_shifted': str(pb),
                      'difference': str(pa-pb),
                      'sharpness_ratio': str(s/(e/eta)),
                      'fixed_probe_horizontal_failure': str(s*s)})
    return cases


def upper(q, delta):
    q, delta = np.clip(q, 0., 1.), np.clip(delta, 0., 1.)
    if q >= 1-delta*delta:
        return 1.
    return (np.sqrt((1-delta*delta)*q)+delta*np.sqrt(1-q))**2


def lower(q, delta):
    q, delta = np.clip(q, 0., 1.), np.clip(delta, 0., 1.)
    if q <= delta*delta:
        return 0.
    return (np.sqrt((1-delta*delta)*q)-delta*np.sqrt(1-q))**2


def hermitian(rng, n):
    z = rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n))
    return (z+z.conj().T)/2


def projector(eigvals, eigvecs, threshold):
    z = eigvecs[:, eigvals <= threshold]
    return z@z.conj().T


def floating_diagnostics():
    rng = np.random.default_rng(20261021)
    worst = {'additive_upper': 0., 'additive_lower': 0.,
             'angle_upper': 0., 'angle_lower': 0.,
             'projection_loewner': 0.}
    pair_count = 512
    for _ in range(pair_count):
        n = int(rng.integers(2, 13))
        a = hermitian(rng, n)
        error = hermitian(rng, n)
        error *= 10.**rng.uniform(-3., .3)/np.linalg.norm(error, 2)
        b = a+error
        e = np.linalg.norm(error, 2)
        av, au = np.linalg.eigh(a)
        bv, bu = np.linalg.eigh(b)
        t = rng.uniform(min(av[0], bv[0])-1, max(av[-1], bv[-1])+1)
        eta = 10.**rng.uniform(-3., .8)
        delta = min(1., e/eta)
        p = projector(av, au, t)
        qlo = projector(bv, bu, t-eta)
        qhi = projector(bv, bu, t+eta)
        for _ in range(4):
            v = rng.normal(size=n)+1j*rng.normal(size=n)
            v /= np.linalg.norm(v)
            fa = float(np.vdot(v, p@v).real)
            flo = float(np.vdot(v, qlo@v).real)
            fhi = float(np.vdot(v, qhi@v).real)
            violations = {'additive_upper': fa-fhi-delta,
                          'additive_lower': flo-delta-fa,
                          'angle_upper': fa-upper(fhi, delta),
                          'angle_lower': lower(flo, delta)-fa}
            for k, value in violations.items():
                worst[k] = max(worst[k], float(value))
    # Arbitrary projections, including unequal ranks and extreme ranks.
    projection_count = 256
    for _ in range(projection_count):
        n = int(rng.integers(2, 13))
        u, _ = np.linalg.qr(rng.normal(size=(n, n))+1j*rng.normal(size=(n, n)))
        v, _ = np.linalg.qr(rng.normal(size=(n, n))+1j*rng.normal(size=(n, n)))
        rp, rq = int(rng.integers(n+1)), int(rng.integers(n+1))
        p = u[:, :rp]@u[:, :rp].conj().T
        q = v[:, :rq]@v[:, :rq].conj().T
        leakage = np.linalg.norm(p@(np.eye(n)-q), 2)
        defect = float(np.linalg.eigvalsh(p-q)[-1])-leakage
        worst['projection_loewner'] = max(worst['projection_loewner'], defect)
    require(max(worst.values()) < 5e-12, 'floating diagnostic failure')
    return {'seed': 20261021, 'hermitian_pairs': pair_count,
            'probe_tests': 4*pair_count, 'arbitrary_projection_pairs': projection_count,
            'largest_positive_numerical_violations': worst,
            'tolerance': 5e-12, 'status': 'PASS (floating diagnostics only)'}


def main():
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    result = {'claim': 'shifted spectral-projection bounds',
              'exact_rational_cases': exact_checks(),
              'floating_diagnostics': floating_diagnostics(),
              'proof_status': 'analytic proof in notes/projection_lemma.md',
              'python': sys.version, 'numpy': np.__version__, 'platform': platform.platform()}
    result['wall_seconds'] = time.perf_counter()-wall_start
    result['cpu_seconds'] = time.process_time()-cpu_start
    out = Path(__file__).resolve().parents[1]/'results'/'projection_lemma_checks.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
