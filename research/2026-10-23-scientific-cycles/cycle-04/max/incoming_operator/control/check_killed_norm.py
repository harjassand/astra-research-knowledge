#!/usr/bin/env python3
"""Diagnostics for the independently derived capped-exponent theorem.

No finite calculation certifies the universal theorem.  The proof is in
PROOF_OR_OBSTRUCTION.txt.  This script evaluates constants and checks the
actual killed matrices on a fixed, deterministic collection of admitted cases.
It does not inspect any instrument or other-arm files.
"""
import decimal
from decimal import Decimal as D
import json
import math
import os
from pathlib import Path
import random
import resource
import time

START_WALL = time.perf_counter()
START_CPU = time.process_time()
resource.setrlimit(resource.RLIMIT_CPU, (40, 40))
resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
decimal.getcontext().prec = 80


def g_dec(c):
    return c * (((1 - c) / c) * (1 - c).ln()).exp()


def root_g(a):
    if a >= 1:
        return D(1)
    lo, hi = D('1e-79'), D(1) - D('1e-79')
    for _ in range(280):
        mid = (lo + hi) / 2
        if g_dec(mid) < a:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


K, alpha, beta, h, c = D(1), D('.5'), D('.5'), D('.001'), D('.5')
H2 = -h * h.ln() - (1 - h) * (1 - h).ln()
delta = (-(K + H2) / (1 - h)).exp()
H = 1 - alpha * delta + beta * g_dec(c)
cap = min(D('.5'), -H.ln() / (2 * D(2).ln()))
rho_tilde = (1 + H.sqrt()) / 2
S = 1 + 1 / (2 * (1 - rho_tilde))
psi = root_g(alpha * (-K).exp() / beta)
chi = root_g(2 * alpha * (-K).exp() / beta)
kappa = -(1 - alpha * (-K).exp() / 2).ln()
old_upper = 1 + (1 + beta / 2).ln() / kappa
constants = {key: str(value) for key, value in {
    'K': K, 'alpha': alpha, 'beta': beta, 'h': h, 'c': c,
    'delta_h': delta, 'g_c': g_dec(c), 'H': H,
    'theta_cap': cap, 'rho_tilde': rho_tilde, 'first_hit_norm_sum_bound': S,
    'original_probe_eta_range_proved_by_simple_bound': cap / c,
    'new_asymptotic_psi': psi, 'new_coefficient_upper_K1_alpha_half_d1': 1 / psi,
    'source_chi': chi, 'source_coefficient_lower': 1 / chi,
    'source_coefficient_upper': old_upper,
}.items()}


def matmul_row(v, A):
    return [sum(v[i] * A[i][j] for i in range(len(v))) for j in range(len(A[0]))]


def norm(v, p):
    return sum(abs(x)**p for x in v)**(1 / p)


def proposal(m, kind):
    Q = [[0.0] * (m + 1) for _ in range(m + 1)]
    if kind == 'path':
        for i in range(m - 1):
            Q[i][i + 1] = Q[i + 1][i] = .5
    elif kind == 'complete':
        for i in range(m):
            for j in range(m):
                if i != j:
                    Q[i][j] = 1 / m
    elif kind == 'star':
        for j in range(1, m):
            Q[0][j] = Q[j][0] = 1 / (m - 1)
    elif kind == 'pairs':
        for i in range(0, m - 1, 2):
            Q[i][i + 1] = Q[i + 1][i] = 1
    for i in range(m + 1):
        Q[i][i] = 1 - sum(Q[i])
    return Q


def case(m, kind, eta, seed):
    rng = random.Random(seed)
    b = .62
    q_raw = [math.exp(rng.uniform(-30, 0)) for _ in range(m)]
    q = [b * x / sum(q_raw) for x in q_raw] + [1 - b]
    z = [rng.uniform(.1, 90) for _ in range(m)]
    pi = [q[i] * .001 * math.exp(-z[i]) for i in range(m)]
    pi += [1 - sum(pi)]
    W = [pi[i] / q[i] for i in range(m + 1)]
    Q = proposal(m, kind)
    G = [[0.0] * (m + 1) for _ in range(m + 1)]
    L = [[0.0] * (m + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(m + 1):
            if i == j:
                continue
            G[i][j] = q[j] * min(1., W[j] / W[i])
            lqr = math.log(q[j] / q[i])
            loga = min(0., eta * lqr) + min(0., math.log(pi[j] / pi[i]) - eta * lqr)
            L[i][j] = Q[i][j] * math.exp(loga)
        G[i][i] = 1 - sum(G[i])
        L[i][i] = 1 - sum(L[i])
    C = [[.5 * (float(i == j) + .5 * G[i][j] + .5 * L[i][j])
          for j in range(m + 1)] for i in range(m + 1)]
    theta = min(.5 * eta, float(cap))
    p = 1 / (1 - theta)
    T = [[C[i][j] * (q[i] / q[j])**theta for j in range(m)] for i in range(m)]
    Lt = [[L[i][j] * (q[i] / q[j])**theta for j in range(m)] for i in range(m)]
    g_actual = (theta / eta) * (1 - theta / eta)**((1 - theta / eta) / (theta / eta))
    row_L = max(map(sum, Lt))
    col_L = max(sum(Lt[i][j] for i in range(m)) for j in range(m))
    G_row = max(sum(G[i][:m]) for i in range(m))
    G_q_col = max(sum(q[i] * G[i][j] / q[j] for i in range(m)) for j in range(m))
    bound_sharp = .5 + .25 * b * 2**theta + .25 * (1 + g_actual)**(1 - theta) * 2**theta
    bound_simple = .5 + .5 * float(H) * 2**theta
    KL = sum(pi[i] * math.log(W[i]) for i in range(m + 1))
    assert KL < 1
    assert all(w < .001 for w in W[:-1]) and W[-1] >= .001
    tol = 3e-12
    assert row_L <= 1 + g_actual + tol
    assert col_L <= 2 + tol
    assert G_row <= b + tol
    assert G_q_col <= 2 * b + tol
    assert bound_sharp <= bound_simple + tol <= float(rho_tilde) + tol
    vectors = [[float(i == j) for i in range(m)] for j in range(m)]
    vectors += [[1.] * m, [q[i]**(1 - theta) for i in range(m)]]
    vectors += [[math.exp(rng.uniform(-10, 10)) for _ in range(m)] for _ in range(8)]
    observed = max(norm(matmul_row(v, T), p) / norm(v, p) for v in vectors)
    assert observed <= bound_sharp + tol
    killed = q[:-1]
    first_hit_sum = (q[-1]**(1 - theta))
    killed_recursion_max_ratio = 0.
    for j in range(25):
        y = [killed[i] / q[i]**theta for i in range(m)]
        next_killed = [sum(killed[i] * C[i][j] for i in range(m)) for j in range(m)]
        next_y = [next_killed[i] / q[i]**theta for i in range(m)]
        killed_recursion_max_ratio = max(killed_recursion_max_ratio, norm(next_y, p) / norm(y, p))
        hit = sum(killed[i] * C[i][-1] for i in range(m))
        first_hit_sum += hit / q[-1]**theta
        killed = next_killed
    assert killed_recursion_max_ratio <= float(rho_tilde) + tol
    assert first_hit_sum <= float(S) + tol
    return {'m_unsafe': m, 'Q_type': kind, 'eta': eta, 'seed': seed,
            'q': q, 'pi': pi, 'Q': Q, 'C': C, 'theta': theta, 'p': p,
            'KL': KL, 'max_local_row_sum': row_L, 'max_local_column_sum': col_L,
            'max_G_row_sum': G_row, 'max_G_q_density_column_sum': G_q_col,
            'trial_vector_max_norm_ratio_lower_estimate': observed,
            'analytic_norm_upper_bound': bound_sharp,
            'coarser_uniform_norm_upper_bound': float(rho_tilde),
            'killed_recursion_max_ratio': killed_recursion_max_ratio,
            'first_26_hit_norms_sum': first_hit_sum}


cases = []
for m in [2, 4, 8]:
    for kind in ['path', 'complete', 'star', 'pairs']:
        for eta in [.0001, .01, .1, .5, 1.]:
            cases.append(case(m, kind, eta, 10000 * m + 100 * len(cases) + 17))

output = {
    'status': 'All finite diagnostic assertions passed. They do not prove universality.',
    'precision': '80-digit Decimal scalar constants; binary64 matrices; no interval certification.',
    'constants': constants,
    'case_count': len(cases), 'cases': cases,
    'costs': {'numerical_cpu_seconds': time.process_time() - START_CPU,
              'wall_seconds': time.perf_counter() - START_WALL,
              'peak_process_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'cpu_limit_seconds': 40, 'address_space_limit_bytes': 512 * 1024**2},
}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'constants': constants, 'case_count': len(cases), 'costs': output['costs']}, indent=2))
