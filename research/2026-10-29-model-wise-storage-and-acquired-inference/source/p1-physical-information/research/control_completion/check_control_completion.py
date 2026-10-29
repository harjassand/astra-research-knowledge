"""Algebraic control-completion checks; no source draws or equipment.

Generator and transform checks use Fraction. The explicitly marked late-time
kernel control uses SciPy, while its negative eigenvalue has an ordinary
analytic proof in the companion note.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

import numpy as np
from scipy.linalg import expm


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(r, c)) for c in zip(*b)] for r in a]


def inv(a):
    n = len(a)
    v = [[F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next(k for k in range(j, n) if v[k][j])
        v[j], v[k] = v[k], v[j]
        d = v[j][j]
        v[j] = [x / d for x in v[j]]
        for i in range(n):
            if i != j:
                d = v[i][j]
                v[i] = [x - d * y for x, y in zip(v[i], v[j])]
    return [row[n:] for row in v]


def generator(flow, w):
    n = len(w)
    assert all(sum(flow[i]) == sum(row[i] for row in flow) for i in range(n))
    q = [[flow[i][j] / w[i] for j in range(n)] for i in range(n)]
    for i in range(n):
        q[i][i] = -sum(q[i])
    return q


def symmetric_tilt(q, s):
    # s_x=exp(u_x/2), allowing exact rational choices.
    n = len(q)
    out = zero(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                out[i][j] = q[i][j] * s[j] / s[i]
        out[i][i] = -sum(out[i])
    return out


def departure_tilt(q, c):
    return [[x * c[i] for x in row] for i, row in enumerate(q)]


def stationary(q, w):
    return all(sum(w[i] * q[i][j] for i in range(len(q))) == 0 for j in range(len(q)))


def generalized_db(q, w, theta):
    n = len(q)
    return all(w[i] == w[theta[i]] for i in range(n)) and all(
        w[i] * q[i][j] == w[theta[j]] * q[theta[j]][theta[i]]
        for i in range(n) for j in range(n))


def reset_transform(q, ports, s):
    ii = [x for x in range(len(q)) if x not in ports]
    r = inv([[(s if i == j else 0) - q[x][y]
              for j, y in enumerate(ii)] for i, x in enumerate(ii)])
    entry = [[q[b][x] / (-q[b][b]) for x in ii] for b in ports]
    exit_rates = [[q[x][b] for b in ports] for x in ii]
    return mul(mul(entry, r), exit_rates)


def glue(flow, weights, ports):
    ii = [x for x in range(len(weights)) if x not in ports]
    m, k = len(ports), len(ii)
    f = zero(m + 2 * k)
    w = [weights[b] for b in ports] + [weights[x] / 2 for x in ii] * 2
    theta = list(range(m)) + list(range(m + k, m + 2 * k)) + list(range(m, m + k))
    for i, b in enumerate(ports):
        for j, c in enumerate(ports):
            if b != c:
                f[i][j] = (flow[b][c] + flow[c][b]) / 2
        for j, x in enumerate(ii):
            xp, xm = m + j, m + k + j
            f[i][xp], f[xp][i] = flow[b][x] / 2, flow[x][b] / 2
            f[i][xm], f[xm][i] = flow[x][b] / 2, flow[b][x] / 2
    for i, x in enumerate(ii):
        for j, y in enumerate(ii):
            f[m + i][m + j] = flow[x][y] / 2
            f[m + k + i][m + k + j] = flow[y][x] / 2
    return generator(f, w), w, theta


def four_state():
    f = zero(4)
    p, r = F(3, 4), F(1, 4)
    for i, j, v in [(0, 2, p), (0, 3, r), (1, 2, r), (1, 3, p),
                    (2, 0, r), (2, 1, p), (3, 0, p), (3, 1, r)]:
        f[i][j] = v
    w, theta = [F(1)] * 4, [0, 1, 3, 2]
    q = generator(f, w)
    assert generalized_db(q, w, theta)
    sym_controls, dep_controls = [], []
    for a, b in [(F(1), F(1)), (F(2), F(1)), (F(1), F(3)), (F(2), F(2))]:
        s = [a, b, F(1), F(1)]
        qs = symmetric_tilt(q, s)
        ws = [w[i] * s[i] ** 2 for i in range(4)]
        assert generalized_db(qs, ws, theta) == (a == b)
        assert stationary(qs, ws) == (a == b)
        sym_controls.append(dict(a=a, b=b, paired_rates=[-qs[2][2], -qs[3][3]],
                                 generalized_equilibrium=(a == b)))
        c = [1 / (a * a), 1 / (b * b), F(1), F(1)]
        qd = departure_tilt(q, c)
        wd = [w[i] / c[i] for i in range(4)]
        assert stationary(qd, wd) and generalized_db(qd, wd, theta)
        for ss in [F(0), F(1), F(3)]:
            assert reset_transform(qd, [0, 1], ss) == reset_transform(q, [0, 1], ss)
        dep_controls.append(dict(a=a, b=b, generalized_equilibrium=True))

    qs = symmetric_tilt(q, [F(2), F(1), F(1), F(1)])
    pi = [F(52, 99), F(17, 99), F(19, 99), F(11, 99)]
    assert stationary(qs, pi)
    assert pi[0] / pi[1] == F(52, 17) != F(4)
    z = reset_transform(qs, [0, 1], F(0))
    one = reset_transform(qs, [0, 1], F(1))
    assert z[0][1] == F(17, 35) and z[1][0] == F(26, 35)
    assert one[0][1] == F(3, 11) and one[1][0] == F(46, 99)
    determinant = z[0][1] * one[1][0] - one[0][1] * z[1][0]
    assert determinant == F(16, 693)
    # Jump likelihood ratios form the gradient u_y-u_x, so their stationary
    # mean is zero. Only the exact escape-rate difference remains per time.
    s = [F(2), F(1), F(1), F(1)]
    for i in range(4):
        for j in range(4):
            if i != j and qs[i][j]:
                assert qs[i][j] / qs[theta[j]][theta[i]] == (s[j] / s[i]) ** 2
    sigma_theta = sum(pi[i] * (qs[i][i] - qs[theta[i]][theta[i]]) for i in range(4))
    assert sigma_theta == F(4, 99)
    return dict(symmetric_controls=sym_controls, departure_controls=dep_controls,
                controlled_stationary_law=pi, transforms_0=z, transforms_1=one,
                determinant=determinant, generalized_entropy_rate=sigma_theta,
                gibbs_port_ratio=F(4), actual_port_ratio=pi[0] / pi[1])


def robust_nine_state():
    eps, r = F(1, 4), F(1)
    f, w = zero(6), [F(1)] * 6
    for i in range(3):
        f[i][3 + i] = f[3 + i][i] = eps
        f[3 + i][3 + (i + 1) % 3] = r
    q, weights, theta = glue(f, w, [0, 1, 2])
    assert len(q) == 9 and generalized_db(q, weights, theta)
    controls = []
    for scales in [[F(1), F(1), F(1)], [F(2), F(1), F(1)],
                   [F(1), F(3), F(1)], [F(1), F(1), F(5)],
                   [F(2), F(3), F(5)]]:
        s = scales + [F(1)] * 6
        qs = symmetric_tilt(q, s)
        ws = [weights[i] * s[i] ** 2 for i in range(9)]
        assert stationary(qs, ws) and generalized_db(qs, ws, theta)
        controls.append(dict(port_scales=scales, equilibrium=True))
    A = [[weights[b] * q[b][x] for x in range(3, 9)] for b in range(3)]
    B = [[q[x][b] for b in range(3)] for x in range(3, 9)]
    K0 = mul(A, B)
    assert K0 == [[eps ** 2 if i == j else F(0) for j in range(3)] for i in range(3)]
    t = 2 * math.pi / (math.sqrt(3) * float(r))
    qn = np.array(q, dtype=float)
    kernel = np.array(A, dtype=float) @ expm(qn[3:, 3:] * t) @ np.array(B, dtype=float)
    eigenvalues = np.linalg.eigvalsh(kernel)
    exact_formula_float = -float(eps ** 2) * math.exp(-(1.5 * float(r) + float(eps)) * t)
    assert np.max(abs(kernel - kernel.T)) < 1e-13
    assert abs(eigenvalues[0] - exact_formula_float) < 1e-13
    assert abs(eigenvalues[1] - exact_formula_float) < 1e-13
    assert eigenvalues[1] < 0
    return dict(states=9, epsilon=eps, cycle_rate=r, controls=controls, K0=K0,
                numerical_late_kernel_control=dict(t=t, eigenvalues=eigenvalues.tolist(),
                analytic_negative_eigenvalue_evaluated=exact_formula_float,
                scope='Floating control of analytically proven negative eigenvalue.'))


def one_port_prediction_pair():
    f, w = zero(3), [F(1), F(2), F(3)]
    for i in range(3):
        j = (i + 1) % 3
        f[i][j], f[j][i] = F(2), F(1)
    q = generator(f, w)
    qr = generator([list(row) for row in zip(*f)], w)
    qg, wg, theta = glue(f, w, [0])
    assert generalized_db(qg, wg, theta)
    qp = symmetric_tilt(q, [F(2), F(1), F(1)])
    qm = symmetric_tilt(qr, [F(2), F(1), F(1)])
    qgt = symmetric_tilt(qg, [F(2)] + [F(1)] * 4)
    checks = []
    for s in [F(0), F(1, 5), F(1), F(3), F(7)]:
        baseline = (F(5, 9) * s + F(7, 6)) / (s * s + F(5, 2) * s + F(7, 6))
        assert reset_transform(q, [0], s)[0][0] == baseline
        assert reset_transform(qr, [0], s)[0][0] == baseline
        assert reset_transform(qg, [0], s)[0][0] == baseline
        plus = (F(10, 9) * s + F(3)) / (s * s + F(11, 3) * s + F(3))
        minus = (F(10, 9) * s + F(3)) / (s * s + F(23, 6) * s + F(3))
        assert reset_transform(qp, [0], s)[0][0] == plus
        assert reset_transform(qm, [0], s)[0][0] == minus
        lifted = reset_transform(qgt, [0], s)[0][0]
        assert lifted == (plus + minus) / 2
        checks.append(dict(s=s, baseline=baseline, controlled_original=plus,
                           controlled_reverse=minus, controlled_lift=lifted))
    gap = reset_transform(qp, [0], F(1))[0][0] - reset_transform(qm, [0], F(1))[0][0]
    assert gap == F(37, 3243)
    return dict(exact_transform_checks=checks, controlled_transform_gap_at_1=gap,
                source_draws=0)


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serialize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialize(v) for v in value]
    return value


def main():
    result = dict(status='PASS', four_state=four_state(), nine_state=robust_nine_state(),
                  one_port_prediction_pair=one_port_prediction_pair(),
                  source_draws=0, code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    out = Path(__file__).with_name('CONTROL_COMPLETION_CHECKS.json')
    out.write_text(json.dumps(serialize(result), indent=2) + '\n')
    print(json.dumps(dict(status='PASS', source_draws=0, exact_tilt_controls=13,
                         exact_reset_transform_comparisons=12,
                         exact_passive_and_controlled_pair_checks=30, output=str(out)), indent=2))


if __name__ == '__main__':
    main()
