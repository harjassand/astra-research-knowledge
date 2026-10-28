"""Exact all-length certificate: hidden dynamics need no contraction gap.
We instead check a gap in the chosen, finite computational coefficient maps.
"""
from fractions import Fraction as F
from echo_compiler import matvec, dot, interval_expr, echo_word

def transpose(a):
    return list(map(list, zip(*a)))

def mm(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]

def sub(a, b):
    return [[x-y for x, y in zip(row, rb)] for row, rb in zip(a, b)]

def scale(a, c):
    return [[c*x for x in row] for row in a]

def diagonal(x):
    return [[v if i == j else F(0) for j in range(len(x))]
            for i, v in enumerate(x)]

def psd(a, strict=False):
    n = len(a)
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    b = [row[:] for row in a]
    for k in range(n):
        pivot = b[k][k]
        if pivot < 0 or (strict and pivot == 0):
            return False
        if pivot == 0:
            if any(b[i][k] for i in range(k+1, n)):
                return False
            continue
        for i in range(k+1, n):
            for j in range(i, n):
                b[i][j] -= b[i][k]*b[k][j]/pivot
                b[j][i] = b[i][j]
    return True

def dominate(w, a, denominator=10**12):
    import numpy as np
    from scipy.linalg import eigvalsh
    wf = np.array([[float(x) for x in row] for row in w])
    af = np.array([[float(x) for x in row] for row in a])
    lam = max(0.0, float(eigvalsh(af, wf)[-1]))
    q = F(int(lam*denominator)+2, denominator)
    step = F(1, denominator)
    for _ in range(200):
        if psd(sub(scale(w, q), a)):
            return q
        q += step
        step *= 2
    raise RuntimeError('No exact domination within proposal budget')

def uniform_certificate(compiler, rho=F(9, 10), metric=None):
    r = compiler.r
    w = metric if metric is not None else compiler.gram_centers()
    if not psd(w, strict=True):
        raise ValueError('Proposed computational metric is not positive definite')
    if not 0 <= rho < 1:
        raise ValueError('A proved coefficient contraction rho<1 is required')
    for t in compiler.maps:
        if not psd(sub(scale(w, rho*rho), mm(transpose(t), mm(w, t)))):
            raise ValueError('Common contraction certificate failed')
    eye = [[F(int(i == j)) for j in range(r)] for i in range(r)]
    residual_uppers, epsilons_squared = [], []
    for i in range(compiler.q):
        entries = [[interval_expr(compiler.residual_expr(i, eye[j], eye[k]),
                                  compiler.records) for k in range(r)] for j in range(r)]
        midpoint = [[x.center for x in row] for row in entries]
        rows = [sum((x.radius for x in row), F(0)) for row in entries]
        upper = [[midpoint[j][k]+(rows[j] if j == k else 0)
                  for k in range(r)] for j in range(r)]
        residual_uppers.append(upper)
        epsilons_squared.append(dominate(w, upper))
    def reading_radius_bound(middle):
        rows = [sum((compiler.records[echo_word(a, middle, b)].radius
                     for b in compiler.dictionary), F(0))
                for a in compiler.dictionary]
        return dominate(w, diagonal(rows))
    gamma_g = reading_radius_bound(())
    gamma_m = max(reading_radius_bound((i,)) for i in range(compiler.q))
    eps2 = max(epsilons_squared)
    initial_w_norm2 = dot(compiler.initial, matvec(w, compiler.initial))
    remainder = initial_w_norm2*eps2/(1-rho)**2
    measurement = initial_w_norm2*(gamma_g+(gamma_m+gamma_g*rho)/(1-rho))
    return {'metric': w, 'rho': rho, 'eps2': eps2,
            'per_action_eps2': epsilons_squared,
            'residual_uppers': residual_uppers,
            'gamma_g': gamma_g, 'gamma_m': gamma_m,
            'initial_metric_norm_squared': initial_w_norm2,
            'all_word_residual_bound': remainder,
            'all_word_measurement_bound': measurement,
            'all_word_total_bound': remainder+measurement,
            'exact_psd_checks_passed': True}
