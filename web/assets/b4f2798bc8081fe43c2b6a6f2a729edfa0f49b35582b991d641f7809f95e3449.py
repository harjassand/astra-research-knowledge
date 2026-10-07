#!/usr/bin/env python3
"""Independent, all-rational local diffusion/weight fixture.

Run from any directory. Writes only beside this file. This is a one-step
quantum-sandwich fixture, NOT the large-N heat-seed Gibbs compiler.
No numpy, sympy, floating eigensolver, continuous random draw, or peer code.
"""
from fractions import Fraction as Q
from math import isqrt, factorial
from pathlib import Path
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
N, DIM = 4, 16
HSTEP = Q(1, 1024)
SQRT_H = Q(1, 32)
ROOT_BITS, WEIGHT_BITS, SELECT_BITS, SQRT_CERT_BITS = 48, 80, 64, 96
P_EXP = 7
C = [Q(1), Q(4), Q(9)]
R0_SQUARED = Q(1, 160)
SEEDS = [([Q(0), Q(0), Q(0)], Q(1, 3)),
         ([Q(1, 64), Q(0), Q(1, 64)], Q(2, 3))]


def enc(x):
    return str(x.numerator) + '/' + str(x.denominator)


def sqrt_interval(x, bits):
    assert x >= 0
    scale = 1 << bits
    k = isqrt((x.numerator << (2 * bits)) // x.denominator)
    lo, hi = Q(k, scale), Q(k + 1, scale)
    assert lo * lo <= x < hi * hi
    return lo, hi


def exp_positive_interval(x, order=20):
    assert 0 <= x < 1
    value, term = Q(1), Q(1)
    for k in range(1, order + 1):
        term *= x / k
        value += term
    # Integral Taylor remainder <= e^x x^(order+1)/(order+1)!.
    remainder = x ** (order + 1) / (factorial(order + 1) * (1 - x))
    return value, value + remainder


def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    z = zero(n)
    for i in range(n):
        z[i][i] = Q(1)
    return z


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(a, k):
    return [[x * k for x in row] for row in a]


def multiply(a, b):
    n = len(a)
    z = zero(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    if b[k][j]:
                        z[i][j] += a[i][k] * b[k][j]
    return z


def transpose(a):
    return [list(row) for row in zip(*a)]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def frobenius_squared(a):
    return sum(x * x for row in a for x in row)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def generator(m):
    p = [[Q(i == j) - m[i] * m[j] for j in range(3)] for i in range(3)]
    cross = [[Q(0), -m[2], m[1]], [m[2], Q(0), -m[0]],
             [-m[1], m[0], Q(0)]]
    cd = [[C[i] if i == j else Q(0) for j in range(3)] for i in range(3)]
    d = sub(multiply(multiply(p, cd), p),
            multiply(multiply(cross, cd), transpose(cross)))
    cm = [C[i] * m[i] for i in range(3)]
    energy = dot(m, cm)
    # N=4, s^2=8 and b=0. All quantities here are rational.
    a = [Q(3, 16) * (cm[i] - energy * m[i]) for i in range(3)]
    v = Q(3, 8) * energy + Q(1, 8) * sum(C)
    return d, a, v


def rational_cholesky(d):
    l = zero(3)
    intervals = []
    for i in range(3):
        for j in range(i + 1):
            residual = d[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                assert residual > 0
                lo, hi = sqrt_interval(residual, ROOT_BITS)
                assert lo > 0
                l[i][j] = lo
                intervals.append({'pivot': i, 'argument': enc(residual),
                                  'lower': enc(lo), 'upper': enc(hi)})
            else:
                l[i][j] = residual / l[j][j]
    covariance_error = sub(multiply(l, transpose(l)), d)
    err_squared = frobenius_squared(covariance_error)
    lo, hi = sqrt_interval(err_squared, SQRT_CERT_BITS)
    # Frobenius residual bounds operator residual without a spectral oracle.
    assert hi < Q(1, 10 ** 12)
    return l, intervals, hi


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def product_kernel(m):
    x, y, z = m
    tau = [[((1 + z) / 2, Q(0)), (x / 2, -y / 2)],
           [(x / 2, y / 2), ((1 - z) / 2, Q(0))]]
    result = []
    for i in range(DIM):
        row = []
        for j in range(DIM):
            value = (Q(1), Q(0))
            for bit in range(N):
                value = cmul(value, tau[(i >> bit) & 1][(j >> bit) & 1])
            row.append(value)
        result.append(row)
    return result


def quantum_hamiltonian():
    jx, by, jz = zero(DIM), zero(DIM), zero(DIM)
    for ket in range(DIM):
        jz[ket][ket] = Q(N, 2) - ket.bit_count()
        for bit in range(N):
            bra = ket ^ (1 << bit)
            jx[bra][ket] += Q(1, 2)
            by[bra][ket] += Q(1, 2) if not ((ket >> bit) & 1) else -Q(1, 2)
    # Jy=i*by, hence Jy^2=-by^2. H is real symmetric and PSD.
    h = scale(add(sub(multiply(jx, jx), scale(multiply(by, by), 4)),
                  scale(multiply(jz, jz), 9)), Q(1, 8))
    assert h == transpose(h)
    return h


def matrix_exp_polynomial(a, order):
    out = eye(len(a))
    term = eye(len(a))
    for k in range(1, order + 1):
        term = scale(multiply(term, a), Q(1, k))
        out = add(out, term)
    return out


def weighted_real_matrix(branches, probabilities):
    result = zero(DIM)
    imag = zero(DIM)
    for branch, prob in zip(branches, probabilities):
        kernel = product_kernel(branch['m'])
        for i in range(DIM):
            for j in range(DIM):
                result[i][j] += prob * kernel[i][j][0]
                imag[i][j] += prob * kernel[i][j][1]
    assert all(x == 0 for row in imag for x in row)
    assert result == transpose(result)
    assert trace(result) == 1
    return result


def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2) + '\n')


def main():
    started = time.monotonic()
    branches, raw_weights, root_certificates, weight_certificates = [], [], [], []
    for seed_id, (m0, p0) in enumerate(SEEDS):
        assert dot(m0, m0) < R0_SQUARED
        d, a, v = generator(m0)
        l, pivots, cov_error = rational_cholesky(d)
        root_certificates.append({'seed': seed_id, 'matrix': [[enc(x) for x in r] for r in d],
                                  'factor': [[enc(x) for x in r] for r in l],
                                  'pivot_intervals': pivots,
                                  'covariance_frobenius_error_upper': enc(cov_error)})
        wlo, whi = exp_positive_interval(HSTEP * v)
        w = Q((wlo * (1 << WEIGHT_BITS)).numerator //
              (wlo * (1 << WEIGHT_BITS)).denominator, 1 << WEIGHT_BITS)
        assert 0 < w <= wlo <= whi
        weight_certificates.append({'seed': seed_id, 'potential': enc(v),
                                    'exponent': enc(HSTEP * v), 'weight': enc(w),
                                    'exact_weight_lower': enc(wlo),
                                    'exact_weight_upper': enc(whi),
                                    'weight_error_upper': enc(whi - w)})
        for code in range(8):
            noise = [Q(1) if ((code >> bit) & 1) else -Q(1) for bit in range(3)]
            m = [m0[i] + HSTEP * a[i] + SQRT_H * dot(l[i], noise) / 4
                 for i in range(3)]
            assert dot(m, m) < R0_SQUARED
            branches.append({'seed': seed_id, 'noise_bits': code, 'm': m})
            raw_weights.append(p0 * w / 8)

    mass = sum(raw_weights)
    probabilities = [w / mass for w in raw_weights]
    denominator = 1 << SELECT_BITS
    counts = [int(p * denominator) for p in probabilities[:-1]]
    counts.append(denominator - sum(counts))
    assert all(c > 0 for c in counts)
    selected_probabilities = [Q(c, denominator) for c in counts]
    categorical_tv = sum(abs(x - y) for x, y in zip(probabilities, selected_probabilities)) / 2
    assert categorical_tv <= Q(len(branches) - 1, denominator)
    # Down-rounding the first R-1 categories breaks the conjugate pair symmetry
    # only in the final residual category. Include this exact TV separately;
    # compare the conjugate-symmetric rational weighted mixture to the target.
    w_matrix = weighted_real_matrix(branches, probabilities)
    rho0 = weighted_real_matrix([{'m': m} for m, _ in SEEDS], [p for _, p in SEEDS])

    h = quantum_hamiltonian()
    e_polynomial = matrix_exp_polynomial(scale(h, HSTEP / 2), P_EXP)
    gp = multiply(multiply(e_polynomial, rho0), e_polynomial)
    zp = trace(gp)
    assert zp >= 1
    gp_normalized = scale(gp, 1 / zp)
    discrepancy = sub(w_matrix, gp_normalized)
    frob_squared = frobenius_squared(discrepancy)
    frob_lo, frob_hi = sqrt_interval(frob_squared, SQRT_CERT_BITS)
    # ||H|| <= 9*jmax*(jmax+1)/s^2=27/4. Tr rho0 e^(hH)>=1.
    x = HSTEP * Q(27, 4) / 2
    exp_op_error = x ** (P_EXP + 1) / (factorial(P_EXP + 1) * (1 - x))
    sandwich_raw_error = 2 * exp_op_error / (1 - x)
    trace_distance_upper = 2 * frob_hi + sandwich_raw_error + categorical_tv
    # Finite fixture claim, verified without floating arithmetic.
    assert trace_distance_upper < Q(1, 10000)

    payload = {'description': '16 positive identical-product branches, exact rational local states',
               'N': N, 'categorical_bits': SELECT_BITS,
               'categorical_denominator': denominator,
               'branches': [{'seed': br['seed'], 'noise_bits': br['noise_bits'],
                             'bloch': [enc(x) for x in br['m']],
                             'bloch_norm_squared': enc(dot(br['m'], br['m'])),
                             'raw_weight': enc(raw), 'probability': enc(p),
                             'dyadic_count': count}
                            for br, raw, p, count in zip(branches, raw_weights, probabilities, counts)]}
    write_json('branches.json', payload)
    rng = random.Random(700803)
    emitted = []
    for draw_id in range(12):
        bitword = rng.getrandbits(SELECT_BITS)
        cumulative, selected = 0, None
        for idx, count in enumerate(counts):
            cumulative += count
            if bitword < cumulative:
                selected = idx
                break
        assert selected is not None
        emitted.append({'draw': draw_id, 'random_word': bitword, 'branch': selected,
                        'N_identical_qubit_bloch_states': [enc(x) for x in branches[selected]['m']]})
    write_json('output_trace.json', {'random_stream': 'Python Random seed 700803, reproducibility fixture only',
                                     'law': 'Exact when each input is an independent uniform 64-bit word',
                                     'outputs': emitted, 'native_quantum_hardware': 'NOT_EXECUTED'})
    max_bits = max(max(x.numerator.bit_length(), x.denominator.bit_length())
                   for row in discrepancy for x in row)
    check = {'status': 'PASS', 'scope': 'one-step full-16-dimensional quantum sandwich',
             'not_claimed': ['heat seed at large N', 'stopped/cutoff SDE over unit time',
                             'general full Gibbs compiler', 'native qubit preparation', 'novelty'],
             'parameters': {'N': N, 'C': ['1/1', '4/1', '9/1'], 'b': ['0/1'] * 3,
                            'step': enc(HSTEP), 's_squared': '8/1', 'r0_squared': enc(R0_SQUARED),
                            'M': '4/1', 'Lambda': '5/1', 'A': ['-4/1', '-1/1', '4/1'],
                            't0': '-1/8', 'large_N_heat_seed_threshold_met': False},
             'root_bits': ROOT_BITS, 'weight_bits': WEIGHT_BITS,
             'select_bits': SELECT_BITS, 'matrix_exp_order': P_EXP,
             'all_bloch_branches_inside_inner_ball': True,
             'stopping_or_rare_event_error': '0/1 (finite exhaustive one-step support)',
             'root_certificates': root_certificates, 'weight_certificates': weight_certificates,
             'categorical_tv_exact': enc(categorical_tv),
             'frob_squared_exact': enc(frob_squared),
             'frob_lower': enc(frob_lo), 'frob_upper': enc(frob_hi),
             'target_matrix_exp_operator_remainder_upper': enc(exp_op_error),
             'sandwich_raw_error_upper': enc(sandwich_raw_error),
             'target_trace_lower': '1/1', 'polynomial_target_trace': enc(zp),
             'full_output_trace_distance_upper': enc(trace_distance_upper),
             'decimal_for_display_only': float(trace_distance_upper),
             'exact_fraction_max_bits_in_final_discrepancy': max_bits,
             'elapsed_seconds': time.monotonic() - started,
             'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'branches_sha256': hashlib.sha256((HERE / 'branches.json').read_bytes()).hexdigest(),
             'output_trace_sha256': hashlib.sha256((HERE / 'output_trace.json').read_bytes()).hexdigest()}
    write_json('certificate.json', check)
    print(json.dumps({'status': 'PASS', 'branches': len(branches),
                      'trace_distance_upper_display': float(trace_distance_upper),
                      'exact_upper_lt': '1/10000',
                      'rare_event_error': 0, 'elapsed_seconds': check['elapsed_seconds']}))


if __name__ == '__main__':
    main()
