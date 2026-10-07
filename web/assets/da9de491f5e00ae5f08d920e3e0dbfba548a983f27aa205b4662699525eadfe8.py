"""Exact rational BCS MPS acquisition, local filtered counts, and Born samples.

No numerical rank threshold, floating arithmetic, or norm/count oracle.
Site mode order is up_0, down_0, up_1, down_1, ... .
This is a deliberately small reference implementation, not a high performance
tensor package. Cost is exponential in ordered bidirectional cut rank.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from math import gcd
import random


@dataclass(frozen=True)
class C:
    re: Q = Q(0)
    im: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, 're', Q(self.re))
        object.__setattr__(self, 'im', Q(self.im))

    @staticmethod
    def of(x):
        return x if isinstance(x, C) else C(Q(x))

    def __add__(self, y):
        y = C.of(y)
        return C(self.re + y.re, self.im + y.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, y):
        return self + (-C.of(y))

    def __rsub__(self, y):
        return C.of(y) + (-self)

    def __mul__(self, y):
        y = C.of(y)
        return C(self.re*y.re - self.im*y.im,
                 self.re*y.im + self.im*y.re)

    __rmul__ = __mul__

    def conj(self):
        return C(self.re, -self.im)

    def abs2(self):
        return self.re*self.re + self.im*self.im

    def __truediv__(self, y):
        y = C.of(y)
        z = self*y.conj()
        d = y.abs2()
        if not d:
            raise ZeroDivisionError
        return C(z.re/d, z.im/d)

    def __bool__(self):
        return bool(self.re or self.im)


ZERO, ONE = C(), C(1)


def zeros(a, b):
    return [[ZERO for _ in range(b)] for _ in range(a)]


def eye(n):
    a = zeros(n, n)
    for i in range(n):
        a[i][i] = ONE
    return a


def transpose(a):
    return [list(x) for x in zip(*a)] if a and a[0] else []


def dagger(a):
    return [[x.conj() for x in row] for row in transpose(a)]


def mm(a, b):
    if not a or not b:
        raise ValueError('empty matrix multiplication')
    d, h, w = len(a), len(b), len(b[0])
    assert len(a[0]) == h
    z = zeros(d, w)
    for i in range(d):
        for k in range(h):
            if a[i][k]:
                for j in range(w):
                    if b[k][j]:
                        z[i][j] = z[i][j] + a[i][k]*b[k][j]
    return z


def add_scaled(a, b, w):
    w = C.of(w)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if b[i][j]:
                a[i][j] = a[i][j] + w*b[i][j]


def pivot_cols(a):
    if not a or not a[0]:
        return []
    b = [[C.of(x) for x in row] for row in a]
    out, r = [], 0
    for j in range(len(b[0])):
        p = next((i for i in range(r, len(b)) if b[i][j]), None)
        if p is None:
            continue
        b[r], b[p] = b[p], b[r]
        v = b[r][j]
        b[r] = [x/v for x in b[r]]
        for i in range(r+1, len(b)):
            v = b[i][j]
            if v:
                b[i] = [x-v*y for x, y in zip(b[i], b[r])]
        out.append(j)
        r += 1
        if r == len(b):
            break
    return out


def inverse(a):
    n = len(a)
    assert n and all(len(row) == n for row in a)
    b = [list(row)+ident for row, ident in zip(a, eye(n))]
    for j in range(n):
        p = next((i for i in range(j, n) if b[i][j]), None)
        if p is None:
            raise ValueError('singular pivot-amplitude matrix')
        b[j], b[p] = b[p], b[j]
        v = b[j][j]
        b[j] = [x/v for x in b[j]]
        for i in range(n):
            if i != j and b[i][j]:
                v = b[i][j]
                b[i] = [x-v*y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def determinant(a):
    n = len(a)
    if not n:
        return ONE
    b = [list(row) for row in a]
    z = ONE
    for j in range(n):
        p = next((i for i in range(j, n) if b[i][j]), None)
        if p is None:
            return ZERO
        if p != j:
            b[j], b[p] = b[p], b[j]
            z = -z
        v = b[j][j]
        z = z*v
        for i in range(j+1, n):
            if b[i][j]:
                w = b[i][j]/v
                for k in range(j+1, n):
                    b[i][k] = b[i][k]-w*b[j][k]
    return z


def exterior_sign(a, b):
    if a & b:
        return 0
    parity = 0
    while b:
        j = (b & -b).bit_length()-1
        parity ^= (a >> (j+1)).bit_count() & 1
        b &= b-1
    return -1 if parity else 1


def multiply_linear(poly, vals):
    out = {}
    for mask, coeff in poly.items():
        for j, val in enumerate(vals):
            if not val:
                continue
            sg = exterior_sign(mask, 1 << j)
            if sg:
                key = mask | (1 << j)
                out[key] = out.get(key, ZERO) + sg*coeff*val
    return {m: v for m, v in out.items() if v}


@dataclass
class CutBasis:
    p: int
    up: list
    down: list
    pivots: list

    @property
    def rank(self):
        return (len(self.up[0]) if self.up else 0) + \
               (len(self.down[0]) if self.down else 0)

    @property
    def dim(self):
        return 1 << self.rank


def acquire_cut(F, p):
    n = len(F)
    U0 = [row[p:] for row in F[:p]]
    D0 = [[F[j][i] for j in range(p, n)] for i in range(p)]
    uc, dc = pivot_cols(U0), pivot_cols(D0)
    U = [[row[j] for j in uc] for row in U0]
    D = [[row[j] for j in dc] for row in D0]
    ur, dr = pivot_cols(transpose(U)), pivot_cols(transpose(D))
    pivots = sorted([2*i for i in ur] + [2*i+1 for i in dr])
    return CutBasis(p, U, D, pivots)


def basis_amplitude(F, basis, occupation, label):
    """Coefficient of e^(G_left) times selected cross-cut linear forms.

    Restriction to the queried occupation erases all other creation modes.
    At construction time at most c_previous+2 physical modes are queried.
    """
    occupation = sorted(occupation)
    m = len(occupation)
    if label.bit_count() > m or (m-label.bit_count()) & 1:
        return ZERO
    a = len(basis.up[0]) if basis.up else 0
    b = len(basis.down[0]) if basis.down else 0
    poly = {0: ONE}
    for j in range(a+b):
        if label & (1 << j):
            vals = []
            for mode in occupation:
                site, spin = divmod(mode, 2)
                if j < a:
                    vals.append(basis.up[site][j] if spin == 0 else ZERO)
                else:
                    vals.append(basis.down[site][j-a] if spin == 1 else ZERO)
            poly = multiply_linear(poly, vals)
            if not poly:
                return ZERO
    for i, ui in enumerate(occupation):
        if ui & 1:
            continue
        for j, dj in enumerate(occupation):
            if not dj & 1 or not F[ui//2][dj//2]:
                continue
            mask = (1 << i) | (1 << j)
            w = F[ui//2][dj//2]*(1 if i < j else -1)
            old = list(poly.items())
            for oldmask, val in old:
                sg = exterior_sign(oldmask, mask)
                if sg:
                    key = oldmask | mask
                    poly[key] = poly.get(key, ZERO) + sg*val*w
    return poly.get((1 << m)-1, ZERO)


def occupation_of_pivots(pivots, mask):
    return [v for j, v in enumerate(pivots) if mask & (1 << j)]


def pivot_matrix(F, basis):
    return [[basis_amplitude(F, basis,
                            occupation_of_pivots(basis.pivots, y), z)
             for z in range(basis.dim)] for y in range(basis.dim)]


@dataclass
class BCSMPS:
    F: list
    tensors: list
    cuts: list

    @property
    def max_cutrank(self):
        return max(x.rank for x in self.cuts)

    def amplitude(self, states):
        v = [[ONE]]
        for A, x in zip(self.tensors, states):
            v = mm(v, A[x])
        return v[0][0]


def acquire_mps(F, max_dimension=256):
    F = [[C.of(x) for x in row] for row in F]
    n = len(F)
    if not all(len(row) == n for row in F):
        raise ValueError('F must be square')
    cuts = [acquire_cut(F, p) for p in range(n+1)]
    if max(c.dim for c in cuts) > max_dimension:
        raise ValueError('explicit resource cap exceeded; no approximation made')
    tensors = []
    for p in range(1, n+1):
        prev, cur = cuts[p-1], cuts[p]
        Kinv = inverse(pivot_matrix(F, prev))
        A = []
        for x in range(4):
            H = []
            local = ([2*(p-1)] if x & 1 else []) + \
                    ([2*(p-1)+1] if x & 2 else [])
            for y in range(prev.dim):
                occ = occupation_of_pivots(prev.pivots, y)+local
                H.append([basis_amplitude(F, cur, occ, z)
                          for z in range(cur.dim)])
            A.append(mm(Kinv, H))
        tensors.append(A)
    return BCSMPS(F, tensors, cuts)


def local_weights(n, t=None, allowed=None):
    t = [Q(0)]*n if t is None else [Q(x) for x in t]
    if len(t) != n or any(x < 0 for x in t):
        raise ValueError('nonnegative squared onsite filters required')
    allowed = [set(range(4)) for _ in range(n)] if allowed is None else allowed
    return [[(t[i] if x == 3 else Q(1)) if x in allowed[i] else Q(0)
             for x in range(4)] for i in range(n)]


def suffix_counts(mps, weights):
    n = len(mps.tensors)
    B = [None]*(n+1)
    B[n] = {0: [[ONE]]}
    for i in range(n-1, -1, -1):
        dim = mps.cuts[i].dim
        cur = {}
        for x in range(4):
            w = weights[i][x]
            if not w:
                continue
            A = mps.tensors[i][x]
            Ad = dagger(A)
            for k, E in B[i+1].items():
                j = k+(x & 1)
                val = mm(mm(A, E), Ad)
                if j not in cur:
                    cur[j] = zeros(dim, dim)
                add_scaled(cur[j], val, w)
        B[i] = cur
    return B


def real_nonnegative(z):
    if z.im or z.re < 0:
        raise AssertionError('exact positivity/reality invariant failed')
    return z.re


def counts(mps, t=None, allowed=None):
    weights = local_weights(len(mps.F), t, allowed)
    B = suffix_counts(mps, weights)
    return [real_nonnegative(B[0].get(k, [[ZERO]])[0][0])
            for k in range(len(mps.F)+1)]


def integer_choice(weights, rng):
    denominator = 1
    for w in weights:
        denominator = denominator*w.denominator//gcd(denominator, w.denominator)
    ws = [w.numerator*(denominator//w.denominator) for w in weights]
    total = sum(ws)
    if total <= 0:
        raise ValueError('no positive conditional completion')
    bits = total.bit_length()
    while True:
        z = rng.getrandbits(bits)
        if z < total:
            break
    for i, w in enumerate(ws):
        if z < w:
            return i
        z -= w
    raise AssertionError('unreachable')


def sample(mps, k, t=None, allowed=None, rng=None):
    rng = random.Random() if rng is None else rng
    weights = local_weights(len(mps.F), t, allowed)
    B = suffix_counts(mps, weights)
    if not real_nonnegative(B[0].get(k, [[ZERO]])[0][0]):
        raise ValueError('zero requested sector')
    v, remain, states = [[ONE]], k, []
    for i, A in enumerate(mps.tensors):
        candidate, qs = [], []
        for x in range(4):
            vx = mm(v, A[x])
            candidate.append(vx)
            E = B[i+1].get(remain-(x & 1))
            if not weights[i][x] or E is None:
                qs.append(Q(0))
            else:
                z = mm(mm(vx, E), dagger(vx))[0][0]*weights[i][x]
                qs.append(real_nonnegative(z))
        x = integer_choice(qs, rng)
        states.append(x)
        v = candidate[x]
        remain -= x & 1
    assert remain == 0 and v[0][0]
    return states


def direct_amplitude(F, states):
    I = [i for i, x in enumerate(states) if x & 1]
    J = [i for i, x in enumerate(states) if x & 2]
    if len(I) != len(J):
        return ZERO
    k = len(I)
    sg = (-1)**(k*(k-1)//2 + sum(i > j for i in I for j in J))
    return sg*determinant([[C.of(F[i][j]) for j in J] for i in I])
