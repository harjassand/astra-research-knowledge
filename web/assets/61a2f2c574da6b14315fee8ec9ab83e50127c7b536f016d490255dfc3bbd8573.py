"""Owned, independent exact Gaussian-rational paired-volume primitives.

No peer imports, no output writes, no sampler/counting oracle. Small diagnostics
use brute sums; estimator_sample does not enumerate pair or row subsets.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from math import ceil


@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))

    def __add__(self, other):
        z = asq(other)
        return Q(self.re + z.re, self.im + z.im)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-asq(other))

    def __rsub__(self, other):
        return asq(other) + (-self)

    def __mul__(self, other):
        z = asq(other)
        return Q(self.re*z.re-self.im*z.im, self.re*z.im+self.im*z.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        z = asq(other)
        d = z.re*z.re+z.im*z.im
        if not d:
            raise ZeroDivisionError
        return Q((self.re*z.re+self.im*z.im)/d,
                 (self.im*z.re-self.re*z.im)/d)

    def __bool__(self):
        return bool(self.re or self.im)

    def conj(self):
        return Q(self.re, -self.im)

    def abs2(self):
        return self.re*self.re+self.im*self.im


def asq(z):
    if isinstance(z, Q):
        return z
    if isinstance(z, tuple):
        return Q(*z)
    return Q(z)


def mat(rows):
    return [[asq(z) for z in row] for row in rows]


def eye(m):
    return [[Q(int(i == j)) for j in range(m)] for i in range(m)]


def zeros(m, n):
    return [[Q() for _ in range(n)] for _ in range(m)]


def adj(A):
    return [[A[j][i].conj() for j in range(len(A))]
            for i in range(len(A[0]))]


def mul(A, B):
    m, k, n = len(A), len(B), len(B[0])
    assert all(len(row) == k for row in A)
    ans = zeros(m, n)
    for i in range(m):
        for t in range(k):
            if A[i][t]:
                for j in range(n):
                    if B[t][j]:
                        ans[i][j] = ans[i][j]+A[i][t]*B[t][j]
    return ans


def sub(A, B):
    return [[a-b for a, b in zip(ar, br)] for ar, br in zip(A, B)]


def det(A):
    n = len(A)
    if not n:
        return Q(1)
    B = [row[:] for row in A]
    out = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if B[i][j]), None)
        if pivot is None:
            return Q()
        if pivot != j:
            B[j], B[pivot] = B[pivot], B[j]
            out = -out
        z = B[j][j]
        out = out*z
        for i in range(j+1, n):
            if B[i][j]:
                fac = B[i][j]/z
                for t in range(j+1, n):
                    B[i][t] = B[i][t]-fac*B[j][t]
                B[i][j] = Q()
    return out


def inverse(A):
    n = len(A)
    B = [row[:] + erow for row, erow in zip(A, eye(n))]
    for j in range(n):
        pivot = next((i for i in range(j, n) if B[i][j]), None)
        if pivot is None:
            raise ValueError('singular')
        B[j], B[pivot] = B[pivot], B[j]
        z = B[j][j]
        B[j] = [v/z for v in B[j]]
        for i in range(n):
            if i != j and B[i][j]:
                fac = B[i][j]
                B[i] = [a-fac*b for a, b in zip(B[i], B[j])]
    return [row[n:] for row in B]


def columns(A, inds):
    return [[row[i] for i in inds] for row in A]


def paired_columns(V, labels):
    return columns(V, [j for i in labels for j in (2*i, 2*i+1)])


def gram_weight(V, labels):
    if not labels:
        return F(1)
    C = paired_columns(V, labels)
    z = det(mul(adj(C), C))
    assert z.im == 0 and z.re >= 0
    return z.re


def canonical(Fmat):
    m = len(Fmat)
    V = zeros(m, 2*m)
    for i in range(m):
        V[i][2*i] = Q(1)
        for j in range(m):
            V[j][2*i+1] = Fmat[i][j]
    return V


def brute_weights(V, k):
    N = len(V[0])//2
    return {S: gram_weight(V, S) for S in combinations(range(N), k)}


def skew_lift(V, xs):
    m = len(V)
    assert len(V[0]) == 2*len(xs)
    A = zeros(m, m)
    for i, x in enumerate(xs):
        for p in range(m):
            for q in range(p+1, m):
                z = x*(V[p][2*i]*V[q][2*i+1]
                       -V[p][2*i+1]*V[q][2*i])
                A[p][q] = A[p][q]+z
                A[q][p] = -A[p][q]
    return A


def estimator_sample(V, k, xs):
    """[t^k] sqrt det(I+t A_x^* A_x), O(k m^3) rational arithmetic.

    Newton identities compute determinant coefficients, then a formal square
    root. The result is nonnegative even for complex rational inputs.
    """
    if k == 0:
        return F(1)
    m = len(V)
    if 2*k > m or k > len(xs):
        return F(0)
    A = skew_lift(V, xs)
    H = mul(adj(A), A)
    power = eye(m)
    traces = [Q()]
    coeffs = [Q(1)]
    for j in range(1, k+1):
        power = mul(power, H)
        traces.append(sum((power[i][i] for i in range(m)), Q()))
        coeffs.append(sum(((-1)**(t-1)*coeffs[j-t]*traces[t]
                           for t in range(1, j+1)), Q())/j)
    roots = [Q(1)]
    for j in range(1, k+1):
        roots.append((coeffs[j]-sum((roots[t]*roots[j-t]
                       for t in range(1, j)), Q()))/2)
    z = roots[k]
    assert z.im == 0 and z.re >= 0
    return z.re


def force_project(V, forced, excluded=()):
    """Return exact forced factor and remaining pairs projected off its span."""
    m, N = len(V), len(V[0])//2
    forced, excluded = set(forced), set(excluded)
    assert forced.isdisjoint(excluded)
    remaining = sorted(set(range(N))-forced-excluded)
    if not forced:
        return F(1), paired_columns(V, remaining), remaining
    C = paired_columns(V, sorted(forced))
    G = mul(adj(C), C)
    d = det(G)
    assert d.im == 0 and d.re >= 0
    if not d:
        return F(0), None, remaining
    P = sub(eye(m), mul(mul(C, inverse(G)), adj(C)))
    return d.re, mul(P, paired_columns(V, remaining)), remaining


def mandatory_core_pit(V, k, delta, rng):
    """Bounded-error support/core acquisition using N+1 grid evaluations.

    With ideal uniform independent grid draws, probability of any false-zero
    is <= delta by Schwartz-Zippel and union bound. No false positives. The
    seeded Python RNG used in diagnostics is not a physical-randomness claim.
    """
    m, N = len(V), len(V[0])//2
    if k == 0:
        return {'status': 'POSITIVE', 'core': [], 'residual': 0, 'grid': 1}
    if 2*k > m or k > N:
        return {'status': 'ZERO', 'core': [], 'residual': None, 'grid': 1}
    assert 0 < delta < 1
    bound = F(k*(N+1))/delta
    grid_bits = (ceil(bound)-1).bit_length()
    grid = 1 << grid_bits

    def zero_test(W):
        xs = [rng.getrandbits(grid_bits) for _ in range(len(W[0])//2)]
        return estimator_sample(W, k, xs) == 0

    if zero_test(V):
        return {'status': 'ZERO_WITH_CONFIDENCE', 'core': [],
                'residual': None, 'grid': grid}
    core = []
    for i in range(N):
        labels = [j for j in range(N) if j != i]
        W = paired_columns(V, labels)
        if not labels or zero_test(W):
            core.append(i)
    if len(core) > k or gram_weight(V, core) == 0:
        return {'status': 'UNKNOWN', 'core': core,
                'residual': None, 'grid': grid}
    return {'status': 'POSITIVE', 'core': core,
            'residual': k-len(core), 'grid': grid,
            'random_bits_upper_bound': N*N*grid_bits}


def bit_height(V):
    return max((max(z.re.numerator.bit_length(), z.re.denominator.bit_length(),
                    z.im.numerator.bit_length(), z.im.denominator.bit_length())
                for row in V for z in row), default=0)
