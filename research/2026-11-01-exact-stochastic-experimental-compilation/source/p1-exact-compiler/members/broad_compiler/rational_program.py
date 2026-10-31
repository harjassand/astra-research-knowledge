"""Exact finite-jet arithmetic and the explicit stochastic compiler coefficients.

No unknown experimental means are passed to these routines. They evaluate a
specified numerical program at rational count-grid arguments. Source bits are
the input to the separate factory. All arithmetic is fractions/integers.

The reference implementation is deliberately simple. Fixed jet order makes its
cost polynomial in the number of variables; the degree is high and no practical
large-dimension performance claim is made.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial, prod
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "broad_mechanism"))
from randomized_elevation import RationalOracle, ProductEnvelope, ElevationRace


@lru_cache(None)
def indices(m, order):
    if m == 0:
        return ((),)
    ans = []
    for j in range(order + 1):
        ans.extend((j,) + q for q in indices(m - 1, order - j))
    return tuple(ans)


class Jet:
    """Taylor coefficients, normalized by multiindex factorials."""
    def __init__(self, m, order, coeff=None):
        self.m, self.order = m, order
        self.coeff = {a: F(c) for a, c in (coeff or {}).items() if c}

    @classmethod
    def constant(cls, value, m, order):
        return cls(m, order, {(0,) * m: F(value)})

    @classmethod
    def variable(cls, value, i, m, order):
        ans = cls.constant(value, m, order)
        if order:
            a = [0] * m
            a[i] = 1
            ans.coeff[tuple(a)] = F(1)
        return ans

    def coerce(self, other):
        if isinstance(other, Jet):
            if (other.m, other.order) != (self.m, self.order):
                raise ValueError("incompatible jet truncation")
            return other
        return Jet.constant(other, self.m, self.order)

    def __add__(self, other):
        other = self.coerce(other)
        out = dict(self.coeff)
        for a, v in other.coeff.items():
            out[a] = out.get(a, F(0)) + v
        return Jet(self.m, self.order, out)

    __radd__ = __add__

    def __neg__(self):
        return Jet(self.m, self.order, {a: -v for a, v in self.coeff.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        out = {}
        for a, va in self.coeff.items():
            for b, vb in other.coeff.items():
                c = tuple(i + j for i, j in zip(a, b))
                if sum(c) <= self.order:
                    out[c] = out.get(c, F(0)) + va * vb
        return Jet(self.m, self.order, out)

    __rmul__ = __mul__

    def inverse(self):
        zero = (0,) * self.m
        c = self.coeff.get(zero, F(0))
        if not c:
            raise ZeroDivisionError("zero constant coefficient")
        # Finite geometric series is the exact inverse in the truncated ring.
        u = (c - self) * (1 / c)
        term = Jet.constant(1, self.m, self.order)
        ans = term
        for _ in range(self.order):
            term = term * u
            ans = ans + term
        return ans * (1 / c)

    def __truediv__(self, other):
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def truncate(self, order):
        return Jet(self.m, order, {a: c for a, c in self.coeff.items()
                                   if sum(a) <= order})

    def differentiate(self, alpha, order):
        if order + sum(alpha) > self.order:
            raise ValueError("insufficient jet order")
        out = {}
        for beta in indices(self.m, order):
            gamma = tuple(a + b for a, b in zip(alpha, beta))
            v = self.coeff.get(gamma, F(0))
            if v:
                out[beta] = v * prod(factorial(c) // factorial(b)
                                     for c, b in zip(gamma, beta))
        return Jet(self.m, order, out)

    def derivative(self, alpha):
        return self.coeff.get(tuple(alpha), F(0)) * prod(factorial(a) for a in alpha)

    def value(self):
        return self.coeff.get((0,) * self.m, F(0))


def solve_linear(a, b):
    """Actual elimination over rationals or jets, not an inverse oracle."""
    n = len(a)
    rows = [list(row) + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        pivot = rows[i][i]
        rows[i] = [v / pivot for v in rows[i]]
        for k in range(n):
            if k != i:
                q = rows[k][i]
                rows[k] = [v - q * u for v, u in zip(rows[k], rows[i])]
    return [row[-1] for row in rows]


def signed_response_program(point):
    """A concrete 2-parameter signed matrix calculation; accepts Jets too."""
    p, q = point
    matrix = [[2 * p - 1, q - p], [p + q - 1, 1 - 2 * q]]
    a = [[sum(matrix[i][k] * matrix[j][k] for k in range(2)) + int(i == j)
          for j in range(2)] for i in range(2)]
    sol = solve_linear(a, [1, 0])
    v = sol[0]
    return v / (1 + v)


class ProbabilityProgram:
    def __init__(self, m, builder):
        self.m, self.builder = m, builder
        self.grid_evaluations = 0

    @lru_cache(maxsize=128)
    def jet(self, point, order=12):
        self.grid_evaluations += 1
        variables = [Jet.variable(x, i, self.m, order) for i, x in enumerate(point)]
        value = self.builder(variables)
        if not isinstance(value, Jet):
            value = Jet.constant(value, self.m, order)
        return value

    def value(self, point):
        return F(self.builder(tuple(map(F, point))))

    def oracle(self):
        return RationalOracle(self.value,
            lambda point, alpha: self.jet(tuple(point), max(1, sum(alpha))).derivative(alpha))

    def coefficient_oracle(self, n, C, sign):
        """a_n for sign=-1, b_n for sign=+1, with exact derivatives to 8."""
        @lru_cache(maxsize=32)
        def coefficient(point):
            full = self.jet(tuple(point), 12)
            f = full.truncate(8)
            x = [Jet.variable(t, i, self.m, 8) for i, t in enumerate(point)]
            v = [t * (1 - t) for t in x]
            zero = Jet.constant(0, self.m, 8)
            A, cubic, fourth = zero, zero, zero
            for i in range(self.m):
                ai = [0] * self.m
                ai[i] = 2
                A += v[i] * full.differentiate(tuple(ai), 8) / 2
                ai[i] = 3
                cubic += v[i] * (1 - 2 * x[i]) * full.differentiate(tuple(ai), 8) / 3
                for j in range(self.m):
                    aij = [0] * self.m
                    aij[i] += 2
                    aij[j] += 2
                    fourth += v[i] * v[j] * full.differentiate(tuple(aij), 8) / 8
            B = -A + cubic + fourth
            h = f * (1 - f)
            return f - A / n + B / (n * n) + sign * C * h / (n ** 3)
        return RationalOracle(lambda point: coefficient(tuple(point)).value(),
                              lambda point, alpha: coefficient(tuple(point)).derivative(alpha))


def ceil_cuberoot(value):
    lo, hi = 0, 1
    while hi ** 3 < value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 >= value:
            hi = mid
        else:
            lo = mid
    return hi


def compiler_constants(m, K):
    if m < 1 or K < 2 or int(K) != K:
        raise ValueError("positive dimension and integer certified K>=2 required")
    Q = 10 ** 15 * (m + 1) ** 4 * (K + 1) ** 12
    R, T = 16 * Q * (m + 1) ** 6, 4 * Q
    C, J = 8 * R, 2 * K
    envelope_M = 128 * T * (m + 1) ** 8
    P = 1 + m * K * K + m * K ** 3 + m * m * K ** 4
    lower = max(3, 1024 * m * m * J * J, 8 * P,
                ceil_cuberoot(4 * C), (8 * envelope_M + C - 1) // C)
    n0 = 1 << (lower - 1).bit_length()
    return dict(Q=Q, R=R, T=T, C=C, J=J, n0=n0)


def exact_factory(program, K, source, bits):
    """Generic proved factory. Conservative n0 can be enormous; never hidden.

    source(i) must return a fresh independent Bernoulli bit. This routine does
    not inspect a source's means, and counts every requested experimental bit.
    The caller has earned the global derivative certificate K analytically.
    """
    c = compiler_constants(program.m, K)
    n, C = c["n0"], c["C"]
    counts = [sum(int(source(i)) for _ in range(n)) for i in range(program.m)]
    calls = program.m * n
    x = tuple(F(k, n) for k in counts)
    low = program.coefficient_oracle(n, C, -1).value(x)
    high = program.coefficient_oracle(n, C, 1).value(x)
    # Exact rational categorical selection with three cumulative masses.
    from randomized_elevation import integerize_rationals
    event = bits.integer_weighted(integerize_rationals((low, 1 - high, high - low)))
    while event == 2:
        for i in range(program.m):
            counts[i] += sum(int(source(i)) for _ in range(n))
        calls += program.m * n
        x = tuple(F(k, 2 * n) for k in counts)
        f = program.value(x)
        h = f * (1 - f)
        envelope = ProductEnvelope(n, counts, r=4, K=c["J"],
                                   scale=c["T"] * h * program.m ** 7)
        step = ElevationRace(
            program.coefficient_oracle(n, C, -1),
            program.coefficient_oracle(n, C, 1),
            program.coefficient_oracle(2 * n, C, -1).value(x),
            program.coefficient_oracle(2 * n, C, 1).value(x),
            envelope, F(4 * C) * h / n ** 3,
        )
        decision = step.sample(bits)
        event = 2 if decision is None else (0 if decision else 1)
        n *= 2
    return int(event == 0), calls
