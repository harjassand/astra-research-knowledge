"""Exact finite arithmetic for the acquired chaotic-structure construction.

No private source law is imported here. Python integers and Fraction are the
arithmetic model; NumPy is used only for storing the supplied integer grid.
"""
from fractions import Fraction as F
from math import isqrt


def frac(x):
    return x if isinstance(x, F) else F(x)


def floor(x):
    x = frac(x)
    return x.numerator // x.denominator


def mod1(x):
    x = frac(x)
    return x - floor(x)


def dyadic_round(x, bits):
    scale = 1 << bits
    return F(floor(frac(x) * scale + F(1, 2)), scale)


def sqrt_upper(x, bits=60):
    x = frac(x)
    assert x >= 0
    scale = 1 << bits
    z = isqrt((x.numerator * scale * scale) // x.denominator)
    if F(z * z, scale * scale) < x:
        z += 1
    return F(z, scale)


def eye(d):
    return [[int(i == j) for j in range(d)] for i in range(d)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, x):
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def matpow(a, n):
    result = eye(len(a))
    while n:
        if n & 1:
            result = matmul(result, a)
        a = matmul(a, a)
        n >>= 1
    return result


def matrix_minus(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def solve(a, b):
    n = len(a)
    rows = [[frac(x) for x in row] + [frac(rhs)] for row, rhs in zip(a, b)]
    for i in range(n):
        p = next(j for j in range(i, n) if rows[j][i])
        rows[i], rows[p] = rows[p], rows[i]
        pivot = rows[i][i]
        rows[i] = [x / pivot for x in rows[i]]
        for j in range(n):
            if j != i and rows[j][i]:
                t = rows[j][i]
                rows[j] = [x - t * y for x, y in zip(rows[j], rows[i])]
    return [row[-1] for row in rows]


def determinant(a):
    """Exact rational Gaussian determinant; no floating eigenvalues."""
    n = len(a)
    rows = [[frac(x) for x in row] for row in a]
    out = F(1)
    for i in range(n):
        pivots = [j for j in range(i, n) if rows[j][i]]
        if not pivots:
            return 0
        p = pivots[0]
        if p != i:
            rows[i], rows[p] = rows[p], rows[i]
            out = -out
        pivot = rows[i][i]
        out *= pivot
        for j in range(i + 1, n):
            t = rows[j][i] / pivot
            for k in range(i + 1, n):
                rows[j][k] -= t * rows[i][k]
            rows[j][i] = 0
    assert out.denominator == 1
    return int(out)


def affine_periodic_base(a, b, period, label):
    d = len(a)
    s = [F(0)] * d
    for _ in range(period):
        s = [x + y for x, y in zip(matvec(a, s), b)]
    dm = matrix_minus(matpow(a, period), eye(d))
    x0 = solve(dm, [frac(k) - z for k, z in zip(label, s)])
    xs = []
    x = x0
    for _ in range(period):
        xs.append([mod1(z) for z in x])
        x = [z + w for z, w in zip(matvec(a, x), b)]
    assert all(x[i] == x0[i] + label[i] for i in range(d))
    least = next(t for t in range(1, period + 1)
                 if period % t == 0 and xs[t % period] == xs[0])
    return xs, least


def cyclic_green(a, values):
    """Solve u[t+1]-A u[t]=values[t], u[m]=u[0], exactly."""
    m, d = len(values), len(a)
    r = [F(0)] * d
    for v in values:
        r = [x + y for x, y in zip(matvec(a, r), v)]
    coeff = matrix_minus(eye(d), matpow(a, m))
    u0 = solve(coeff, r)
    out, u = [], u0
    for v in values:
        out.append(u)
        u = [x + y for x, y in zip(matvec(a, u), v)]
    assert u == u0
    return out


class GridResidual:
    """Periodic Freudenthal interpolation; exact rational input/output."""
    def __init__(self, numerators, denominator):
        self.values = numerators
        self.q = numerators.shape[0]
        self.d = numerators.shape[-1]
        self.denominator = denominator

    def __call__(self, x):
        s = [mod1(t) * self.q for t in x]
        vertex = [floor(t) for t in s]
        rem = [t - k for t, k in zip(s, vertex)]
        order = sorted(range(self.d), key=lambda j: (-rem[j], j))
        last = [int(v) for v in self.values[tuple(vertex)]]
        value = [F(v, self.denominator) for v in last]
        for j in order:
            vertex[j] = (vertex[j] + 1) % self.q
            nxt = [int(v) for v in self.values[tuple(vertex)]]
            value = [z + rem[j] * F(v - w, self.denominator)
                     for z, v, w in zip(value, nxt, last)]
            last = nxt
        return value


def orbit_compile(a, b, residual, period, label, tau, epsilon, bits=60):
    """Compile one later address, using a posteriori exact contraction error."""
    d = len(a)
    root_d = sqrt_upper(F(d))
    assert tau < 1
    assert root_d / (1 << (bits + 1)) < (1 - tau) * epsilon / 8
    bases, least = affine_periodic_base(a, b, period, label)
    u = [[F(0)] * d for _ in range(period)]
    iterations = 0
    peak_numerator_bits = 0
    peak_denominator_bits = 0
    while True:
        vals = [residual([x + z for x, z in zip(base, corr)])
                for base, corr in zip(bases, u)]
        new = cyclic_green(a, vals)
        for row in new:
            for z in row:
                peak_numerator_bits = max(peak_numerator_bits, abs(z.numerator).bit_length())
                peak_denominator_bits = max(peak_denominator_bits, z.denominator.bit_length())
        err = root_d * max(abs(x - y) for row, old in zip(new, u)
                           for x, y in zip(row, old)) / (1 - tau)
        if err <= epsilon:
            break
        u = [[dyadic_round(z, bits) for z in row] for row in new]
        iterations += 1
        assert iterations <= 10000, "Unexpected failure of certified contraction."
    points = [[mod1(x + z) for x, z in zip(base, corr)]
              for base, corr in zip(bases, u)]
    return {
        "period_requested": period,
        "least_period": least,
        "integer_label": list(label),
        "iterations": iterations,
        "dyadic_rounding_bits": bits,
        "algorithm_error_bound": str(err),
        "algorithm_error_decimal": float(err),
        "peak_rational_numerator_bits": peak_numerator_bits,
        "peak_rational_denominator_bits": peak_denominator_bits,
        "points": [[str(z) for z in row] for row in points],
    }


def cat_entropy_interval(terms=50, bits=140):
    """2 log((3+sqrt(5))/2), enclosed by a rational atanh series."""
    scale = 1 << bits
    n = isqrt(5 * scale * scale)
    lo, hi = F(n, scale), F(n + 1, scale)
    series = sum((F(1, (2*j+1) * 5**j) for j in range(terms)), F(0))
    tail = F(5, 4 * (2*terms+1) * 5**terms)
    return 4 * series / hi, 4 * (series + tail) / lo
