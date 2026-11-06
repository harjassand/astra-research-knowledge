#!/usr/bin/env python3
"""Exact rational finite-block bounds; this is not a capacity stopping algorithm.

Only the Python standard library is required. The default invocation checks the
entropy calculation and physical one-block examples. --plan prints the explicit
covering costs. The exhaustive optimizer is implemented but not run by default.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
import sys


@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def of(x):
        if isinstance(x, G):
            return x
        return G(F(x), F(0))

    def __add__(self, other):
        other = G.of(other)
        return G(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + -G.of(other)

    def __rsub__(self, other):
        return G.of(other) + -self

    def __mul__(self, other):
        other = G.of(other)
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = G.of(other)
        den = other.re**2 + other.im**2
        if not den:
            raise ZeroDivisionError
        return G((self.re * other.re + self.im * other.im) / den,
                 (self.im * other.re - self.re * other.im) / den)

    def conj(self):
        return G(self.re, -self.im)

    def __bool__(self):
        return bool(self.re or self.im)


def zeros(r, c=None):
    c = r if c is None else c
    return [[G() for _ in range(c)] for _ in range(r)]


def eye(d):
    z = zeros(d)
    for i in range(d):
        z[i][i] = G.of(1)
    return z


def mm(x, y):
    out = zeros(len(x), len(y[0]))
    for i, row in enumerate(x):
        for k, xik in enumerate(row):
            if xik:
                for j, ykj in enumerate(y[k]):
                    if ykj:
                        out[i][j] = out[i][j] + xik * ykj
    return out


def kron(x, y):
    out = zeros(len(x) * len(y), len(x[0]) * len(y[0]))
    for i, row in enumerate(x):
        for j, xij in enumerate(row):
            if xij:
                for k, yrow in enumerate(y):
                    for l, ykl in enumerate(yrow):
                        out[i * len(y) + k][j * len(y[0]) + l] = xij * ykl
    return out


def tr_real(x):
    t = sum((x[i][i] for i in range(len(x))), G())
    assert t.im == 0
    return t.re


def ceil(q):
    q = F(q)
    return -(-q.numerator // q.denominator)


def ln2_bounds(target):
    """2 atanh(1/3), with an exact rational geometric tail."""
    target = F(target)
    assert target > 0
    total = F(0)
    j = 0
    while True:
        total += F(2, (2 * j + 1) * 3**(2 * j + 1))
        j += 1
        tail = F(9, 4 * (2 * j + 1) * 3**(2 * j + 1))
        if tail <= target:
            return total, total + tail


def entropy_bounds(x, eps):
    """Return rational lower/upper bounds for S(x), width at most eps.

    x is promised a rational-complex positive semidefinite trace-one matrix.
    S_nat(x) = sum_{k>=1} tr[x (I-x)^k]/k.
    The tail after m terms is <= d/(m+1), including singular x.
    """
    d = len(x)
    eps = F(eps)
    assert eps > 0 and tr_real(x) == 1
    m = ceil(F(8 * d, 1) / eps)
    lo_log, hi_log = ln2_bounds(eps / (16 * d))
    y = eye(d)
    for i in range(d):
        for j in range(d):
            y[i][j] = y[i][j] - x[i][j]
    power = x
    partial = F(0)
    tail = F(d, m + 1)
    used = 0
    for k in range(1, m + 1):
        power = mm(power, y)
        used = k
        if not any(any(row) for row in power):
            tail = F(0)
            break
        tk = tr_real(power)
        assert tk >= 0
        partial += tk / k
    low = partial / hi_log
    high = (partial + tail) / lo_log
    assert high - low <= eps
    return low, high, used


def blocks_from_choi(j, a, b):
    """Normalized Choi convention: N(|i><j|)_{bc}=a J_{ib,jc}."""
    assert len(j) == a * b
    return [[[[a * G.of(j[i*b+k][l*b+m]) for m in range(b)]
              for k in range(b)] for l in range(a)] for i in range(a)]


def choi_from_blocks(blocks):
    a, b = len(blocks), len(blocks[0][0])
    out = zeros(a * b)
    for i in range(a):
        for j in range(a):
            for k in range(b):
                for l in range(b):
                    out[i*b+k][j*b+l] = blocks[i][j][k][l] / a
    return out


def blocks_from_kraus(ks):
    b, a = len(ks[0]), len(ks[0][0])
    out = [[zeros(b) for _ in range(a)] for _ in range(a)]
    for i in range(a):
        for j in range(a):
            for r in range(b):
                for s in range(b):
                    out[i][j][r][s] = sum((k[r][i] * k[s][j].conj()
                                             for k in ks), G())
    for i in range(a):
        for j in range(a):
            assert tr_real(out[i][j]) == int(i == j)
    return out


def tensor_blocks(x, y):
    ax, ay = len(x), len(y)
    return [[kron(x[i // ay][j // ay], y[i % ay][j % ay])
             for j in range(ax * ay)] for i in range(ax * ay)]


def channel_power(blocks, n):
    assert n >= 1
    out = blocks
    for _ in range(1, n):
        out = tensor_blocks(out, blocks)
    return out


def output_from_purification(blocks, v):
    """v is an arbitrary nonzero rational-complex vector on R*A, dim R=dim A.

    Normalization is at the density-matrix level, so no irrational square root
    enters the channel output.
    """
    a, b = len(blocks), len(blocks[0][0])
    assert len(v) == a * a
    v = [G.of(x) for x in v]
    norm2 = sum((z.re**2 + z.im**2 for z in v), F(0))
    assert norm2 > 0
    rb = zeros(a * b)
    for r in range(a):
        for s in range(a):
            for i in range(a):
                for j in range(a):
                    coeff = v[r*a+i] * v[s*a+j].conj() / norm2
                    if coeff:
                        for k in range(b):
                            for l in range(b):
                                rb[r*b+k][s*b+l] = (rb[r*b+k][s*b+l]
                                                    + coeff * blocks[i][j][k][l])
    bob = zeros(b)
    for k in range(b):
        for l in range(b):
            bob[k][l] = sum((rb[r*b+k][r*b+l] for r in range(a)), G())
    assert tr_real(rb) == tr_real(bob) == 1
    return bob, rb


def coherent_bounds(blocks, v, entropy_eps):
    bob, rb = output_from_purification(blocks, v)
    lb, ub, kb = entropy_bounds(bob, entropy_eps)
    lr, ur, kr = entropy_bounds(rb, entropy_eps)
    return lb - ur, ub - lr, (kb, kr)


def mesh_plan(a, b, n, eta):
    """Explicit cover for a per-use finite-block interval of width <= eta."""
    eta = F(eta)
    assert a >= 1 and b >= 1 and n >= 1 and eta > 0
    la, lb = (a - 1).bit_length(), (b - 1).bit_length()
    c = la + 2 * lb
    da, db = a**n, b**n
    dcomplex = da * da
    if c == 0:
        return dict(a_n=da, b_n=db, complex_coordinates=dcomplex,
                    trace_distance=F(1, 4), integer_radius=1,
                    grid_log2_count_upper=4)
    delta = eta / 2
    t = min(F(1, 4), delta / (2 * c), (delta / 12)**2)
    # sqrt(2D)/K <= t follows from K >= 2D/t.
    k = ceil(F(2 * dcomplex, 1) / t)
    return dict(a_n=da, b_n=db, complex_coordinates=dcomplex,
                trace_distance=t, integer_radius=k,
                # Count is (2K+1)^(2D)-1. This is a safe integer bit bound.
                grid_log2_count_upper=2*dcomplex*(2*k+1).bit_length())


def finite_block_enclosure(j, a, b, n, eta):
    """Exhaustive terminating procedure for f_n; prohibitively expensive.

    Returns a rational interval [L,U] containing
      f_n=max_rho I_c(rho,N^n)/n
    of width <= eta. There is deliberately no claim that n is sufficient for Q.
    """
    eta = F(eta)
    plan = mesh_plan(a, b, n, eta)
    if a == 1:
        return F(0), F(0)
    blocks = channel_power(blocks_from_choi(j, a, b), n)
    d, k = plan['complex_coordinates'], plan['integer_radius']
    best_low = None
    best_high = None
    for coords in product(range(-k, k+1), repeat=2*d):
        if not any(coords):
            continue
        v = [G(F(coords[2*i]), F(coords[2*i+1])) for i in range(d)]
        low, high, _ = coherent_bounds(blocks, v, n*eta/8)
        best_low = low if best_low is None else max(best_low, low)
        best_high = high if best_high is None else max(best_high, high)
    low = max(F(0), best_low/n)
    high = min(F((a-1).bit_length()), best_high/n + eta/2)
    assert low <= high and high-low <= eta
    return low, high


def fixture_channels():
    identity = blocks_from_kraus([eye(2)])
    dephase = []
    for i in range(2):
        k = zeros(2)
        k[i][i] = G.of(1)
        dephase.append(k)
    dephase = blocks_from_kraus(dephase)
    ks = []
    for _ in range(2):
        k = zeros(3, 2)
        k[0][0] = k[1][1] = G.of(F(1, 2))
        ks.append(k)
    for i in range(2):
        for _ in range(2):
            k = zeros(3, 2)
            k[2][i] = G.of(F(1, 2))
            ks.append(k)
    half_erase = blocks_from_kraus(ks)
    ks = []
    for i in range(2):
        k = zeros(1, 2)
        k[0][i] = G.of(1)
        ks.append(k)
    complete_erase = blocks_from_kraus(ks)
    return dict(identity=identity, dephasing=dephase,
                half_erasure=half_erase, complete_erasure=complete_erase)


def countermodel_checks():
    """Finite checks of analytic identities, not a test of undecidability."""
    events = [None, 1, 3, 8]
    count = 0
    for halting_time in events:
        h = lambda n: F(int(halting_time is not None and halting_time <= n))
        true_q = F(int(halting_time is not None))
        for n in range(1, 15):
            for m in range(1, 15):
                assert (n+m)*h(n+m) >= n*h(n)+m*h(m)
                for rate in (F(0), F(1, 4), F(3, 4), F(5, 4)):
                    exp_n = max(F(0), n*(rate-h(n)))
                    exp_m = max(F(0), m*(rate-h(m)))
                    exp_nm = max(F(0), (n+m)*(rate-h(n+m)))
                    assert exp_nm <= exp_n+exp_m
                    if rate > true_q:
                        assert exp_n >= n*(rate-true_q)
                    count += 1
    return dict(checked_inequalities=count,
                scope='finite fixtures support the proved algebraic identities only')


def checks():
    results = {}
    for name, blocks in fixture_channels().items():
        j = choi_from_blocks(blocks)
        assert blocks_from_choi(j, 2, len(blocks[0][0])) == blocks
        for label, v, expected in [
                ('maximally_mixed_input', [1, 0, 0, 1],
                 dict(identity=F(1), dephasing=F(0),
                      half_erasure=F(0), complete_erasure=F(-1))[name]),
                ('pure_input', [1, 0, 0, 0], F(0))]:
            low, high, terms = coherent_bounds(blocks, v, F(1, 8))
            assert low <= expected <= high
            results[f'{name}/{label}'] = dict(
                expected=str(expected), lower=float(low), upper=float(high),
                rational_lower=str(low), rational_upper=str(high),
                entropy_terms=terms,
                exact_interval_contains_expected=True)
    # This separately exercises genuinely complex rational purification entries.
    blocks = fixture_channels()['identity']
    low, high, terms = coherent_bounds(blocks, [G.of(1), G(), G(), G(F(0), F(1))], F(1, 8))
    assert low <= 1 <= high
    results['identity/complex_purification'] = dict(
        lower=float(low), upper=float(high), entropy_terms=terms,
        exact_interval_contains_expected=True)
    results['countermodel'] = countermodel_checks()
    results['grid_plan_qubit_1block_eta_1_4'] = {
        k: str(v) if isinstance(v, F) else v
        for k, v in mesh_plan(2, 2, 1, F(1, 4)).items()}
    return results


if __name__ == '__main__':
    if '--plan' in sys.argv:
        p = mesh_plan(2, 2, 1, F(1, 4))
        print(json.dumps({k: str(v) if isinstance(v, F) else v for k, v in p.items()}, indent=2))
    else:
        print(json.dumps(checks(), indent=2))
