#!/usr/bin/env python3
"""Exact Fourier construction and certificate for a near-harmonic compiler.

This module implements the free frame, its inverse, the periodic isometry
fixed point and the explicit smallness/curvature certificate. The full
global potential is defined constructively in THEOREM_AND_ALGORITHM.txt.
This code is a mathematical reference, not a manufactured mechanical device
or a fast long-time predictor. All arithmetic below is exact.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from math import factorial


@dataclass(frozen=True)
class GQ:
    re: F = F(0)
    im: F = F(0)

    def __add__(self, other):
        if not isinstance(other, GQ):
            other = GQ(F(other))
        return GQ(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return GQ(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, GQ):
            return GQ(self.re * other, self.im * other)
        return GQ(self.re * other.re - self.im * other.im,
                  self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def conjugate(self):
        return GQ(self.re, -self.im)

    def size(self):
        return abs(self.re) + abs(self.im)

    def __bool__(self):
        return bool(self.re or self.im)


ZERO = GQ()
ONE = GQ(F(1))
I = GQ(F(0), F(1))
Poly = dict[tuple[int, ...], GQ]


def clean(a: Poly) -> Poly:
    return {k: v for k, v in a.items() if v}


def constant(value, m: int) -> Poly:
    z = value if isinstance(value, GQ) else GQ(F(value))
    return {(0,) * m: z} if z else {}


def add(a: Poly, b: Poly) -> Poly:
    out = a.copy()
    for k, v in b.items():
        out[k] = out.get(k, ZERO) + v
    return clean(out)


def scale(a: Poly, value) -> Poly:
    return clean({k: v * value for k, v in a.items()})


def sub(a: Poly, b: Poly) -> Poly:
    return add(a, scale(b, -1))


def mul(a: Poly, b: Poly) -> Poly:
    out = {}
    for k, v in a.items():
        for l, w in b.items():
            kl = tuple(x + y for x, y in zip(k, l))
            out[kl] = out.get(kl, ZERO) + v * w
    return clean(out)


def derivative(a: Poly, i: int) -> Poly:
    return clean({k: v * (I * k[i]) for k, v in a.items()})


def elliptic(a: Poly, inverse=False) -> Poly:
    out = {}
    for k, v in a.items():
        factor = -(1 + sum(x * x for x in k))
        out[k] = v * (F(1, factor) if inverse else factor)
    return clean(out)


def cosine(k: tuple) -> Poly:
    negative = tuple(-x for x in k)
    return add({k: GQ(F(1, 2))}, {negative: GQ(F(1, 2))})


def sine(k: tuple) -> Poly:
    negative = tuple(-x for x in k)
    return add({k: GQ(F(0), F(-1, 2))}, {negative: GQ(F(0), F(1, 2))})


def norm(a: Poly, weight=F(2), order=2) -> F:
    return sum((v.size() * weight ** sum(map(abs, k))
                * (1 + sum(map(abs, k))) ** order for k, v in a.items()), F(0))


def vnorm(v: list[Poly], weight=F(2), order=2) -> F:
    return sum((norm(a, weight, order) for a in v), F(0))


def derivative_bound(v: list[Poly], order: int) -> F:
    return max(sum((z.size() * sum(map(abs, k)) ** j
                    for a in v for k, z in a.items()), F(0))
               for j in range(order + 1))


def vadd(v, w):
    return [add(a, b) for a, b in zip(v, w)]


def vsub(v, w):
    return [sub(a, b) for a, b in zip(v, w)]


def vscale(v, c):
    return [scale(a, c) for a in v]


def dv(v, i):
    return [derivative(a, i) for a in v]


def dot(v, w):
    out = {}
    for a, b in zip(v, w):
        out = add(out, mul(a, b))
    return out


def eval_zero(a: Poly) -> F:
    value = sum(a.values(), ZERO)
    assert value.im == 0
    return value.re


def eval_quarters(a: Poly, angles: tuple[int, ...]) -> F:
    phases = [ONE, I, -ONE, -I]
    out = ZERO
    for k, v in a.items():
        out += v * phases[sum(x * y for x, y in zip(k, angles)) % 4]
    assert out.im == 0
    return out.re


def inverse_matrix(matrix):
    n = len(matrix)
    work = [list(map(F, row)) + [F(int(i == j)) for j in range(n)]
            for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if work[i][j])
        work[j], work[pivot] = work[pivot], work[j]
        p = work[j][j]
        work[j] = [x / p for x in work[j]]
        for i in range(n):
            if i != j and work[i][j]:
                p = work[i][j]
                work[i] = [x - p * y for x, y in zip(work[i], work[j])]
    assert all(work[i][j] == int(i == j) for i in range(n) for j in range(n))
    return [row[n:] for row in work]


def build_frame(d: int, extra_frequencies=()):
    assert d >= 1
    m = d + 1
    frequencies = []
    for i in range(d):
        k = [0] * d
        k[i] = 1
        frequencies.append(tuple(k))
    for i, j in combinations(range(d), 2):
        k = [0] * d
        k[i] = k[j] = 1
        frequencies.append(tuple(k))
    for k in extra_frequencies:
        k = tuple(k)
        if not any(k):
            continue
        if next(x for x in k if x) < 0:
            k = tuple(-x for x in k)
        if k not in frequencies:
            frequencies.append(k)
    count = len(frequencies)
    kappa = F(1, count + 1)
    anchor = (1 - count * kappa * kappa) / (1 + count * kappa * kappa)
    amplitude = 2 * kappa / (1 + count * kappa * kappa)
    assert anchor > 0 and anchor * anchor + count * amplitude * amplitude == 1
    psi = [constant(anchor, m)]
    for k in frequencies:
        extended = tuple(k) + (0,)
        psi += [scale(cosine(extended), amplitude), scale(sine(extended), amplitude)]
    clock = (0,) * d + (1,)
    q0 = [mul(a, cosine(clock)) for a in psi] + [mul(a, sine(clock)) for a in psi]
    assert dot(q0, q0) == constant(1, m)
    pairs = [(i, j) for i in range(m) for j in range(i, m)]
    derivatives = [dv(q0, i) for i in range(m)]
    frame = derivatives + [dv(dv(q0, i), j) for i, j in pairs]
    gram = []
    for u in frame:
        row = []
        for v in frame:
            polynomial = dot(u, v)
            value = eval_zero(polynomial)
            assert polynomial == constant(value, m)
            row.append(value)
        gram.append(row)
    inv = inverse_matrix(gram)
    columns = []
    for j in range(len(frame)):
        column = [{} for _ in q0]
        for i in range(len(frame)):
            if inv[i][j]:
                column = vadd(column, vscale(frame[i], inv[i][j]))
        columns.append(column)
    ce = max(F(1), max(vnorm(column) for column in columns))
    gm = [[eval_zero(dot(derivatives[i], derivatives[j])) for j in range(d)]
          for i in range(d)]
    return dict(d=d, m=m, frequencies=frequencies, anchor=anchor,
                amplitude=amplitude, q0=q0, pairs=pairs, frame=frame,
                gram=gram, inverse=inv, columns=columns, ce=ce, gm=gm)


def apply_frame_inverse(data, rhs):
    result = [{} for _ in data['q0']]
    for column, h in zip(data['columns'], rhs):
        if h:
            result = vadd(result, [mul(v, h) for v in column])
    return result


def gunther_observations(v, m):
    av = [elliptic(a) for a in v]
    first = [dv(v, i) for i in range(m)]
    qi = [elliptic(dot(av, first[i]), inverse=True) for i in range(m)]
    qij = []
    for i in range(m):
        for j in range(i, m):
            acc = dot(first[i], first[j])
            for k in range(m):
                acc = add(acc, scale(dot(dv(first[i], k), dv(first[j], k)), 2))
            acc = sub(acc, scale(dot(av, dv(first[i], j)), 2))
            qij.append(elliptic(acc, inverse=True))
    return qi, qij


def nonlinear(data, v):
    qi, qij = gunther_observations(v, data['m'])
    return apply_frame_inverse(data, [scale(a, -1) for a in qi]
                               + [scale(a, F(1, 2)) for a in qij])


def metric_parts(data, y):
    d, m, gm = data['d'], data['m'], data['gm']
    t = F(4, 5)
    gy = []
    for i in range(d):
        out = {}
        for j in range(d):
            out = add(out, scale(y[j], gm[i][j]))
        gy.append(out)
    ygy = dot(y, gy)
    h1, h2 = [], []
    for i, j in data['pairs']:
        h1.append(scale(gy[i], -1 / (t * t)) if i < d and j == d else {})
        h2.append(scale(ygy, 1 / (t * t)) if i == j == d else {})
    return h1, h2


def dyadic_below(value: F):
    exponent = 0
    while F(1, 1 << exponent) > value:
        exponent += 1
    return F(1, 1 << exponent), exponent


def make_certificate(data, y, eta=F(1, 4)):
    assert 0 < eta < 1
    m, ce = data['m'], data['ce']
    h1, h2 = metric_parts(data, y)
    h_bound = vnorm(h1) + vnorm(h2)
    A = max(F(1), ce * h_bound / 2)
    sym = m * (m + 1) // 2
    B = max(F(1), ce * (m + 1) * (m + F(sym * (2 * m + 3), 2)))
    s, t = F(3, 5), F(4, 5)
    baseline = {k: (s + t) * derivative_bound(data['q0'], k) for k in range(5)}
    correction = {k: 2 * A * factorial(k) * 2 ** k for k in range(5)}
    q_bound = {k: baseline[k] + correction[k] for k in range(5)}
    anchor, amplitude = data['anchor'], data['amplitude']
    lower = s / (2 * ((1 + 1 / anchor) / amplitude + 1 / anchor))
    rho = min(F(1, 8), lower * lower / (8 * (q_bound[2] + 1)))
    lam = lower * lower / 2
    b1, b2, b3 = q_bound[1], q_bound[2], q_bound[3]
    x1 = b1 / lam
    x2 = ((3 * b1 * b2 + 2 * rho * b3) * x1 * x1 + 2 * b2 * x1) / lam
    pi1 = b1 * x1
    pi2 = b2 * x1 * x1 + b1 * x2
    nu1 = 1 + pi1
    y3 = derivative_bound(y, 3)
    ca = 4 * baseline[2] * correction[2] + 2 * correction[2] ** 2
    cb = correction[4] + correction[2] + (8 * y3 + 32 * y3 * y3) * q_bound[4]
    h0 = ca + cb * rho
    hh1 = ca * x1 + cb * x1 * rho + cb * nu1
    hh2 = (ca + cb * rho) * (x1 * x1 + x2) + 2 * cb * x1 * nu1 + cb * pi2
    distance1 = 2 * nu1 / rho
    distance2 = 2 * (nu1 * nu1 + rho * pi2) / (rho * rho)
    cutoff1 = 1024 * distance1
    cutoff2 = 65536 * distance1 * distance1 + 1024 * distance2
    cv = hh2 + 2 * cutoff1 * hh1 + cutoff2 * h0
    maximum = min(F(1), 1 / (16 * A * B), 1 / (32 * A), eta / (2 * cv))
    epsilon, exponent = dyadic_below(maximum)
    radius = 2 * A * epsilon
    lipschitz = 2 * B * radius
    assert lipschitz <= F(1, 4)
    assert radius <= F(1, 16)
    assert cv * epsilon <= eta / 2
    assert lower * lower - 2 * rho * q_bound[2] >= lam
    h = [add(scale(a, epsilon), scale(b, epsilon * epsilon)) for a, b in zip(h1, h2)]
    linear = apply_frame_inverse(data, [{} for _ in range(m)]
                                + [scale(a, F(-1, 2)) for a in h])
    assert vnorm(linear) <= A * epsilon
    return dict(A=A, B=B, h=h, linear=linear, epsilon=epsilon,
                epsilon_exponent=exponent, eta=eta, radius=radius,
                lipschitz=lipschitz, co_lipschitz=lower, tube_radius=rho,
                projection_eigenvalue=lam, curvature_constant=cv,
                certified_hessian_error=cv * epsilon, baseline=baseline,
                correction=correction, q_bound=q_bound, y3=y3,
                value_jet_constant=ca, gradient_jet_constant=cb,
                projection_first=x1, projection_second=x2)


def picard_step(data, certificate, v):
    return vadd(certificate['linear'], nonlinear(data, v))


def ceil_log_two_integer(value: int) -> int:
    assert value >= 1
    return (value - 1).bit_length()


def finite_precision_embedding(data, certificate, bits: int, derivative_order=0):
    """A truncated/rounded evaluator with a posteriori C^r error certificate.

    The weak analytic norm uses weight 3/2. All calculations are rational.
    The global-potential evaluation algorithm is specified in the report.
    """
    assert bits >= 0 and derivative_order >= 0
    c_r = factorial(derivative_order) * 3 ** derivative_order
    bstar = bits + ceil_log_two_integer(c_r) + 8
    cutoff = 4 * (bstar + 4)
    dimension = len(data['q0'])
    m = data['m']
    coefficient_count_bound = dimension * (2 * cutoff + 1) ** m
    precision = bstar + cutoff + ceil_log_two_integer(
        32 * coefficient_count_bound * (cutoff + 1) ** 2)
    unit = 1 << precision
    target = F(1, (1 << bits) * c_r)
    v = [{} for _ in data['q0']]
    for step in range(bstar + 10):
        exact_next = picard_step(data, certificate, v)
        residual = vnorm(vsub(v, exact_next), weight=F(3, 2))
        error = residual / (1 - certificate['lipschitz'])
        if error <= target:
            return v, {'steps': step, 'bits': bits, 'derivative_order': derivative_order,
                       'cutoff': cutoff, 'coefficient_precision': precision,
                       'weak_norm_error': error, 'C_r_error': c_r * error}
        out = []
        for polynomial in exact_next:
            rounded = {}
            for k, z in polynomial.items():
                if sum(map(abs, k)) <= cutoff:
                    value = GQ(F(int(z.re * unit), unit), F(int(z.im * unit), unit))
                    if value:
                        rounded[k] = value
            out.append(rounded)
        assert vnorm(out) <= certificate['radius']
        v = out
    raise AssertionError('The proved convergence bound was not met')


def metric_residual(data, certificate, v):
    r = vadd(data['q0'], v)
    residuals = []
    for (i, j), h in zip(data['pairs'], certificate['h']):
        residuals.append(sub(sub(dot(dv(r, i), dv(r, j)),
                                 dot(dv(data['q0'], i), dv(data['q0'], j))), h))
    return residuals


def linearized_metric(data, v):
    return [add(dot(dv(data['q0'], i), dv(v, j)),
                dot(dv(data['q0'], j), dv(v, i))) for i, j in data['pairs']]


def serialize_fraction(x):
    return {'numerator': str(x.numerator), 'denominator': str(x.denominator)}


def serialize_poly(p):
    return [{'frequency': list(k), 'real': serialize_fraction(z.re),
             'imaginary': serialize_fraction(z.im)} for k, z in sorted(p.items())]
