"""Finite-bit low-k hard-BCS counts and row/column Born self-reduction.

Attribution: the random-sign Pfaffian estimator is c03_l10's; positive
forced-row projection and row/column sampling are c03_l06's.  c03_s02
sharpened the BCS moment bound to a central binomial coefficient.  This is
an independent implementation, including an elementary Hellinger budget
which uses eta=O(epsilon/sqrt(n)), rather than epsilon/n.

Arithmetic is exact Q(i); per-sign production work uses Gaussian integers
and Newton traces.  A zero randomized estimate is NOT an exact zero test.
The sampler's TV guarantee is on the promise c_k(F)>0.  Small sign cubes
may be exhausted exactly, but enumeration is explicitly capped.
"""
from cutrank_bcs import C, Q, ZERO, ONE, eye, zeros, dagger, mm, inverse, determinant, pivot_cols
from dataclasses import dataclass
import itertools
import math
import random


def ceilq(x):
    x = Q(x)
    return -(-x.numerator // x.denominator)


def ceil_log2_reciprocal(x):
    x = Q(x)
    if not 0 < x <= 1:
        raise ValueError('probability budget must be in (0,1]')
    h = 0
    while (x.numerator << h) < x.denominator:
        h += 1
    return h


def clear_complex(a):
    d = 1
    for row in a:
        for z in row:
            d = math.lcm(d, z.re.denominator, z.im.denominator)
    return [[(int(z.re*d), int(z.im*d)) for z in row] for row in a], d


def iadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def imul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def imm(a, b):
    z = [[(0, 0) for _ in b[0]] for _ in a]
    for i in range(len(a)):
        for h in range(len(b)):
            if a[i][h] != (0, 0):
                for j in range(len(b[0])):
                    if b[h][j] != (0, 0):
                        z[i][j] = iadd(z[i][j], imul(a[i][h], b[h][j]))
    return z


def skew_norm_coefficient(a, r):
    """[t^r] sqrt(det(I+t A* A)); O(r*m^3) integer operations."""
    m = len(a)
    if r == 0:
        return 1
    if 2*r > m:
        return 0
    adj = [[(a[j][i][0], -a[j][i][1]) for j in range(m)] for i in range(m)]
    b = imm(adj, a)
    power, traces, detco, rootco = b, [0], [1], [1]
    for degree in range(1, r+1):
        tr = (sum(power[i][i][0] for i in range(m)),
              sum(power[i][i][1] for i in range(m)))
        if tr[1]:
            raise ArithmeticError('Hermitian power has nonreal trace')
        traces.append(tr[0])
        num = sum((-1)**(j-1)*detco[degree-j]*traces[j]
                  for j in range(1, degree+1))
        if num % degree:
            raise ArithmeticError('Newton coefficient was not integral')
        detco.append(num//degree)
        num = detco[degree]-sum(rootco[j]*rootco[degree-j] for j in range(1, degree))
        if num % 2 or num < 0:
            raise ArithmeticError('skew norm coefficient was not nonnegative integral')
        rootco.append(num//2)
        if degree < r:
            power = imm(power, b)
    return rootco[r]


def hermitian_coefficient(b, q):
    """[t^q] det(I+t B) by rational Newton traces."""
    m = len(b)
    if q == 0:
        return Q(1)
    if q > m:
        return Q(0)
    power, traces, co = b, [Q(0)], [Q(1)]
    for degree in range(1, q+1):
        tr = sum((power[i][i] for i in range(m)), ZERO)
        if tr.im:
            raise ArithmeticError('nonreal Gram trace')
        traces.append(tr.re)
        co.append(sum((-1)**(j-1)*co[degree-j]*traces[j]
                      for j in range(1, degree+1))/degree)
        if degree < q:
            power = mm(power, b)
    if co[q] < 0:
        raise ArithmeticError('negative Gram coefficient')
    return co[q]


def gram_projection(c, m):
    """Return det(C*C) and exact orthogonal projector off span(C)."""
    if not c or not c[0]:
        return Q(1), eye(m)
    g = mm(dagger(c), c)
    d = determinant(g)
    if d.im or d.re < 0:
        raise ArithmeticError('Gram determinant not nonnegative real')
    if not d.re:
        return Q(0), None
    cg = mm(mm(c, inverse(g)), dagger(c))
    p = eye(m)
    for i in range(m):
        for j in range(m):
            p[i][j] = p[i][j]-cg[i][j]
    return d.re, p


@dataclass
class RowPrefix:
    n: int
    remaining_pairs: int
    free_sites: tuple
    integer_vectors: list
    factor: Q
    moment_bound: int
    exact_mass: object = None

    def sign_value(self, signs):
        if self.exact_mass is not None:
            return Q(self.exact_mass)
        if len(signs) != len(self.free_sites) or any(s not in (-1, 1) for s in signs):
            raise ValueError('one +/-1 sign is required per free site')
        a = [[(0, 0) for _ in range(self.n)] for _ in range(self.n)]
        v = self.integer_vectors
        for h, s in enumerate(signs):
            for i in range(self.n):
                for j in range(i+1, self.n):
                    x = imul(v[i][2*h], v[j][2*h+1])
                    y = imul(v[i][2*h+1], v[j][2*h])
                    z = (s*(x[0]-y[0]), s*(x[1]-y[1]))
                    a[i][j] = iadd(a[i][j], z)
                    a[j][i] = (-a[i][j][0], -a[i][j][1])
        return self.factor*skew_norm_coefficient(a, self.remaining_pairs)


class BudgetExceeded(RuntimeError):
    pass


class LowKCounter:
    def __init__(self, f, k, exact_sign_cap=256, sign_budget=1000000):
        self.f = [[C.of(z) for z in row] for row in f]
        self.n, self.k = len(f), k
        if any(len(row) != self.n for row in f) or not isinstance(k, int) or not 0 <= 2*k <= self.n:
            raise ValueError('square F and 0 <= 2k <= n required')
        self.exact_sign_cap, self.sign_budget = exact_sign_cap, sign_budget
        self.stats = {'prefix_calls': 0, 'sign_evaluations': 0, 'sign_random_bits': 0,
                      'exact_cube_calls': 0, 'randomized_calls': 0, 'exact_base_calls': 0}

    def prefix(self, selected=(), excluded=()):
        a, b = set(selected), set(excluded)
        n, k = self.n, self.k
        if a & b or not a | b <= set(range(n)):
            raise ValueError('invalid disjoint row constraints')
        free = tuple(i for i in range(n) if i not in a | b)
        r = k-len(a)
        bound = math.comb(2*k-len(a), r) if 0 <= r <= 2*k-len(a) else 1
        if 0 <= r <= len(free):
            bound = min(bound, math.comb(len(free), r))
        if r < 0 or len(free) < r:
            return RowPrefix(n, max(0, r), free, [], Q(1), 1, Q(0))
        if k == 0:
            return RowPrefix(n, r, free, [], Q(1), 1, Q(1))
        if k == 1:
            rows = a if a else set(free)
            mass = sum(self.f[i][j].abs2() for i in rows for j in range(n) if i != j)
            return RowPrefix(n, r, free, [], Q(1), 1, mass)
        allv = [[z for i in range(n) for z in (C(int(h == i)), self.f[i][h])]
                for h in range(n)]
        c = [[row[j] for i in sorted(a) for j in (2*i, 2*i+1)] for row in allv]
        d, p = gram_projection(c, n)
        if not d or r == 0:
            return RowPrefix(n, r, free, [], Q(1), 1, d)
        v = [[row[j] for i in free for j in (2*i, 2*i+1)] for row in allv]
        v = mm(p, v)
        integer, denom = clear_complex(v)
        return RowPrefix(n, r, free, integer, d/Q(denom**(4*r)), bound)

    def estimate(self, selected=(), excluded=(), eta=Q(1, 4), delta=Q(1, 16), rng=None, mode='auto'):
        eta, delta = Q(eta), Q(delta)
        if not 0 < eta < 1 or not 0 < delta < 1 or mode not in ('auto', 'random', 'enumerate'):
            raise ValueError('invalid relative accuracy/confidence/mode')
        rng = rng or random.SystemRandom()
        p = self.prefix(selected, excluded)
        self.stats['prefix_calls'] += 1
        if p.exact_mass is not None:
            self.stats['exact_base_calls'] += 1
            return Q(p.exact_mass), {'kind': 'EXACT_BASE', 'moment_bound': 1}
        if p.moment_bound == 1:
            self.stats['sign_evaluations'] += 1
            value = p.sign_value([1]*len(p.free_sites))
            return value, {'kind': 'EXACT_POINTWISE', 'moment_bound': 1}
        size = len(p.free_sites)
        batch = ceilq(4*(p.moment_bound-1)/(eta*eta))
        groups = 8*ceil_log2_reciprocal(delta)+1
        cube = 1 << size
        exhaustive = mode == 'enumerate' or (mode == 'auto' and cube <= self.exact_sign_cap and cube <= batch*groups)
        cost = cube if exhaustive else batch*groups
        if exhaustive and cube > self.exact_sign_cap:
            raise BudgetExceeded('exact sign cube exceeds explicit enumeration cap')
        if self.sign_budget is not None and self.stats['sign_evaluations']+cost > self.sign_budget:
            raise BudgetExceeded(f'needed {cost} additional sign evaluations; configured run budget exceeded')
        if exhaustive:
            total = sum((p.sign_value(s) for s in itertools.product((-1, 1), repeat=size)), Q(0))
            self.stats['sign_evaluations'] += cube
            self.stats['exact_cube_calls'] += 1
            return total/cube, {'kind': 'EXACT_CUBE', 'sign_evaluations': cube, 'moment_bound': p.moment_bound}
        means = []
        for _ in range(groups):
            total = Q(0)
            for _ in range(batch):
                word = rng.getrandbits(size)
                total += p.sign_value([1 if word >> i & 1 else -1 for i in range(size)])
            means.append(total/batch)
        self.stats['sign_evaluations'] += cost
        self.stats['sign_random_bits'] += cost*size
        self.stats['randomized_calls'] += 1
        means.sort()
        return means[len(means)//2], {'kind': 'RANDOMIZED_RELATIVE', 'eta': str(eta), 'delta': str(delta),
                    'batch': batch, 'groups': groups, 'sign_evaluations': cost,
                    'moment_bound': p.moment_bound,
                    'zero_report': 'zero estimate is not exact zero certification'}

    def column_mass(self, rows, selected=(), excluded=()):
        rows, s, b = tuple(sorted(rows)), set(selected), set(excluded)
        if len(rows) != self.k or len(set(rows)) != self.k or s & b or (s | b) & set(rows):
            raise ValueError('invalid column constraints')
        labels = [j for j in range(self.n) if j not in set(rows)]
        if not s | b <= set(labels):
            raise ValueError('column label outside allowed complement')
        q = self.k-len(s)
        remain = [j for j in labels if j not in s | b]
        if q < 0 or len(remain) < q:
            return Q(0)
        c = [[self.f[i][j] for j in sorted(s)] for i in rows]
        d, p = gram_projection(c, self.k)
        if not d or q == 0:
            return d
        m = [[self.f[i][j] for j in remain] for i in rows]
        pm = mm(p, m)
        return d*hermitian_coefficient(mm(pm, dagger(pm)), q)

    def sample(self, epsilon=Q(1, 10), rng=None, mode='auto'):
        """TV <= epsilon on positive sector; at most 2*n dyadic branch draws."""
        epsilon = Q(epsilon)
        if not 0 < epsilon <= 1:
            raise ValueError('epsilon must be in (0,1]')
        rng = rng or random.SystemRandom()
        n, k = self.n, self.k
        if not n:
            return (), (), {'status': 'EXACT_VACUUM', 'branch_random_bits': 0}
        s = math.isqrt(n)
        if s*s < n:
            s += 1
        eta, delta = epsilon/(16*s), epsilon/(8*n)
        bits = ceil_log2_reciprocal(epsilon/(8*n))
        grid = 1 << bits
        used, a, b, trace = 0, set(), set(), []

        def branch(w0, w1):
            nonlocal used
            if w0 < 0 or w1 < 0:
                raise ArithmeticError('negative branch mass')
            if not w0+w1:
                return None
            scaled = grid*w1/(w0+w1)
            threshold = scaled.numerator // scaled.denominator
            if threshold == 0:
                return False
            if threshold == grid:
                return True
            used += bits
            return rng.getrandbits(bits) < threshold

        for i in range(n):
            if len(a) == k:
                b.update(range(i, n))
                break
            if k-len(a) == n-i:
                a.update(range(i, n))
                break
            w0, r0 = self.estimate(a, b | {i}, eta, delta, rng, mode)
            w1, r1 = self.estimate(a | {i}, b, eta, delta, rng, mode)
            pick = branch(w0, w1)
            trace.append({'site': i, 'mass_out': str(w0), 'mass_in': str(w1),
                          'out_engine': r0['kind'], 'in_engine': r1['kind']})
            if pick is None:
                # Only a charged estimator failure is possible on the positive promise.
                return tuple(range(k)), tuple(range(k, 2*k)), {
                    'status': 'BAD_EVENT_FALLBACK', 'positive_sector_promise': True,
                    'branch_random_bits': used, 'trace': trace}
            (a if pick else b).add(i)
        rows = tuple(sorted(a))
        cols, excluded = set(), set()
        labels = [j for j in range(n) if j not in a]
        for index, j in enumerate(labels):
            if len(cols) == k:
                break
            if k-len(cols) == len(labels)-index:
                cols.update(labels[index:])
                break
            w0 = self.column_mass(rows, cols, excluded | {j})
            w1 = self.column_mass(rows, cols | {j}, excluded)
            pick = branch(w0, w1)
            if pick is None:
                return tuple(range(k)), tuple(range(k, 2*k)), {
                    'status': 'BAD_EVENT_FALLBACK', 'positive_sector_promise': True,
                    'branch_random_bits': used, 'trace': trace}
            (cols if pick else excluded).add(j)
        return rows, tuple(sorted(cols)), {
            'status': 'OK_TV', 'positive_sector_promise': True, 'epsilon': str(epsilon),
            'eta': str(eta), 'per_call_failure': str(delta), 'grid': grid,
            'branch_random_bits': used, 'branch_random_bits_upper_bound': 2*n*bits,
            'trace': trace, 'zero_boundary': 'no exact zero-sector oracle implemented'}
