#!/usr/bin/env python3
"""Replay the saved finite fixture through independent matrix formulas.

The full Hamiltonian is reconstructed from two-spin flips, not from squared
Pauli matrices. Product matrix entries use binomial moments, not repeated
Gaussian-rational tensor multiplication. The all-N analytic theorem is not
verified by these finite computations.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb, factorial
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent


def load_fraction(x):
    return F(x)


def zeros(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(a)))
             for j in range(len(a))] for i in range(len(a))]


def transpose(a):
    return [list(x) for x in zip(*a)]


def kernel_real_element(bloch, bra, ket, n):
    x, y, z = bloch
    counts = [0, 0, 0, 0]
    for bit in range(n):
        counts[2 * ((bra >> bit) & 1) + ((ket >> bit) & 1)] += 1
    n00, n01, n10, n11 = counts
    real_offdiag = F(0)
    for p in range(n01 + 1):
        for q in range(n10 + 1):
            if (p + q) % 2 == 0:
                real_offdiag += (comb(n01, p) * comb(n10, q)
                                 * x ** (n01 + n10 - p - q) * y ** (p + q)
                                 * (-1) ** (p + (p + q) // 2))
    return ((1 + z) ** n00 * (1 - z) ** n11 * real_offdiag) / (2 ** n)


def mixture(states, weights, n):
    return [[sum(p * kernel_real_element(m, i, j, n)
                 for m, p in zip(states, weights))
             for j in range(2 ** n)] for i in range(2 ** n)]


def verify():
    started = time.monotonic()
    cert = json.loads((HERE / 'certificate.json').read_text())
    branches = json.loads((HERE / 'branches.json').read_text())
    checks = []
    assert cert['script_sha256'] == hashlib.sha256((HERE / 'certified_cubature.py').read_bytes()).hexdigest()
    assert cert['branches_sha256'] == hashlib.sha256((HERE / 'branches.json').read_bytes()).hexdigest()
    assert cert['output_trace_sha256'] == hashlib.sha256((HERE / 'output_trace.json').read_bytes()).hexdigest()
    checks.append('saved script and payload hashes')
    n, dim = cert['parameters']['N'], 2 ** cert['parameters']['N']
    assert n == 4
    radius_sq = load_fraction(cert['parameters']['r0_squared'])
    hstep = load_fraction(cert['parameters']['step'])
    rows = branches['branches']
    states = [[load_fraction(x) for x in row['bloch']] for row in rows]
    probs = [load_fraction(row['probability']) for row in rows]
    weights = [load_fraction(row['raw_weight']) for row in rows]
    for m, row in zip(states, rows):
        norm_sq = sum(x * x for x in m)
        assert norm_sq == load_fraction(row['bloch_norm_squared']) < radius_sq < 1
    assert probs == [w / sum(weights) for w in weights]
    assert sum(probs) == 1
    checks.append('all rational product states physical and inside stopping ball')
    denom = branches['categorical_denominator']
    counts = [row['dyadic_count'] for row in rows]
    assert sum(counts) == denom == 2 ** cert['select_bits']
    assert all(c >= 0 for c in counts)
    cat_tv = sum(abs(F(c, denom) - p) for c, p in zip(counts, probs)) / 2
    assert cat_tv == load_fraction(cert['categorical_tv_exact']) <= F(len(rows) - 1, denom)
    checks.append('bounded exact categorical law and TV allocation')
    # Complex conjugate pairs make the real-entry calculation sufficient.
    for i, (m, row) in enumerate(zip(states, rows)):
        paired = row['seed'] * 8 + (row['noise_bits'] ^ 2)
        assert probs[paired] == probs[i]
        assert states[paired] == [m[0], -m[1], m[2]]
    checks.append('exact cancellation of every imaginary matrix entry')
    seed_states = [[F(0)] * 3, [F(1, 64), F(0), F(1, 64)]]
    coefficient_c = [F(1), F(4), F(9)]
    for seed, root in enumerate(cert['root_certificates']):
        m = seed_states[seed]
        d = [[load_fraction(x) for x in row] for row in root['matrix']]
        l = [[load_fraction(x) for x in row] for row in root['factor']]
        axes_cross_m = [[F(0), -m[2], m[1]], [m[2], F(0), -m[0]],
                        [-m[1], m[0], F(0)]]
        independent_d = [[sum(coefficient_c[k]
                              * ((F(k == i) - m[k] * m[i])
                                 * (F(k == j) - m[k] * m[j])
                                 - axes_cross_m[k][i] * axes_cross_m[k][j])
                              for k in range(3)) for j in range(3)] for i in range(3)]
        assert d == independent_d
        assert all(l[i][j] == 0 for i in range(3) for j in range(i + 1, 3))
        assert all(l[i][i] > 0 for i in range(3))
        product = matmul(l, transpose(l))
        residual_sq = sum((product[i][j] - d[i][j]) ** 2 for i in range(3) for j in range(3))
        residual_hi = load_fraction(root['covariance_frobenius_error_upper'])
        assert residual_sq <= residual_hi ** 2 < F(1, 10 ** 24)
        energy = sum(coefficient_c[i] * m[i] ** 2 for i in range(3))
        drift = [F(3, 16) * (coefficient_c[i] - energy) * m[i] for i in range(3)]
        for code in range(8):
            noise = [F(1) if (code >> bit) & 1 else F(-1) for bit in range(3)]
            expected = [m[i] + hstep * drift[i] + F(1, 128) * sum(l[i][j] * noise[j] for j in range(3))
                        for i in range(3)]
            assert expected == states[seed * 8 + code]
        wc = cert['weight_certificates'][seed]
        v = F(3, 8) * energy + F(7, 4)
        assert v == load_fraction(wc['potential'])
        x = hstep * v
        elo = sum(x ** k / factorial(k) for k in range(21))
        ehi = elo + x ** 21 / (factorial(21) * (1 - x))
        w = load_fraction(wc['weight'])
        assert load_fraction(wc['exact_weight_lower']) == elo
        assert load_fraction(wc['exact_weight_upper']) == ehi
        assert w <= elo <= ehi
        assert ehi - w == load_fraction(wc['weight_error_upper'])
    checks.append('axis-generator covariance, rational roots, full updates and weight intervals')
    # Independent Hamiltonian: every off-diagonal term flips exactly two spins.
    H = zeros(dim)
    for ket in range(dim):
        jz = F(n, 2) - ket.bit_count()
        H[ket][ket] = (F(5) + 9 * jz ** 2) / 8
        for p in range(n):
            for q in range(p + 1, n):
                bra = ket ^ (1 << p) ^ (1 << q)
                equal = ((ket >> p) & 1) == ((ket >> q) & 1)
                H[bra][ket] = F(-3 if equal else 5, 16)
    assert H == transpose(H)
    ep = zeros(dim)
    power = zeros(dim)
    for i in range(dim):
        ep[i][i] = power[i][i] = F(1)
    for k in range(1, cert['matrix_exp_order'] + 1):
        power = matmul(power, H)
        coef = (hstep / 2) ** k / factorial(k)
        ep = [[ep[i][j] + coef * power[i][j] for j in range(dim)] for i in range(dim)]
    rho0 = mixture(seed_states, [F(1, 3), F(2, 3)], n)
    gp = matmul(matmul(ep, rho0), ep)
    zp = sum(gp[i][i] for i in range(dim))
    assert zp == load_fraction(cert['polynomial_target_trace']) >= 1
    wmat = mixture(states, probs, n)
    discrepancy = [[wmat[i][j] - gp[i][j] / zp for j in range(dim)] for i in range(dim)]
    fsq = sum(x * x for row in discrepancy for x in row)
    assert fsq == load_fraction(cert['frob_squared_exact'])
    flo, fhi = load_fraction(cert['frob_lower']), load_fraction(cert['frob_upper'])
    assert flo ** 2 <= fsq <= fhi ** 2
    x = hstep * F(27, 8)
    exp_bound = x ** 8 / (factorial(8) * (1 - x))
    raw_bound = 2 * exp_bound / (1 - x)
    assert exp_bound == load_fraction(cert['target_matrix_exp_operator_remainder_upper'])
    assert raw_bound == load_fraction(cert['sandwich_raw_error_upper'])
    upper = 2 * fhi + raw_bound + cat_tv
    assert upper == load_fraction(cert['full_output_trace_distance_upper']) < F(1, 10 ** 6)
    checks.append('independent full Hamiltonian/product matrices and exact <1e-6 output trace bound')
    out = {'status': 'PASS', 'exact_checks': checks,
           'exact_trace_distance_upper': str(upper),
           'display_only_upper': float(upper),
           'all_N_theorem_status': 'NOT_PROVED_BY_FINITE_CHECKS',
           'native_hardware_status': 'NOT_EXECUTED',
           'elapsed_seconds': time.monotonic() - started}
    (HERE / 'verification.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('exact_trace_distance_upper', 'exact_checks')}
                     | {'check_groups': len(checks)}))


if __name__ == '__main__':
    verify()
