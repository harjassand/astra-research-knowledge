"""Tiny own exact checks of the central/filtered finite-bit sampler.

Only Q(i)/Fraction decisions. Imports own earlier Q helper, never peer code.
This is not a full general Haar, spectral-envelope or physical backend run.
"""
from fractions import Fraction as F
from itertools import product, combinations, permutations
from math import factorial, prod
from pathlib import Path
from time import perf_counter
import sys
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'spin_bridge'))
from white_repair_fixture import Q


def matmul(a, b):
    return [[sum((x*y for x, y in zip(row, col)), Q())
             for col in zip(*b)] for row in a]


def adj(a):
    return [[x.conjugate() for x in col] for col in zip(*a)]


def eye(d):
    return [[Q(int(i == j)) for j in range(d)] for i in range(d)]


def det(a):
    n = len(a)
    z = Q()
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = Q((-1)**inv)
        for i, j in enumerate(p):
            term = term*a[i][j]
        z = z+term
    return z


def dyad(x, q):
    scale = 1 << q
    return F((x*scale+F(1, 2)).numerator //
             (x*scale+F(1, 2)).denominator, scale)


def root_floor(x, r, q):
    assert 0 <= x <= 1 and r >= 1
    lo, hi, scale = 0, 1 << q, 1 << q
    while lo < hi:
        mid = (lo+hi+1)//2
        if F(mid, scale)**r <= x:
            lo = mid
        else:
            hi = mid-1
    ans = F(lo, scale)
    assert ans**r <= x
    assert lo == scale or F(lo+1, scale)**r > x
    return ans


def atan_series(x, k):
    return sum(((-1)**n*x**(2*n+1)/F(2*n+1) for n in range(k)), F())


def rational_phase(u, q=20):
    # Fixed tiny fixture accuracy; certified pi/series remainder checks.
    k = q+8
    pi = 16*atan_series(F(1, 5), k)-4*atan_series(F(1, 239), k)
    pi_error = 16*F(1, 5)**(2*k+1)/F(2*k+1)
    pi_error += 4*F(1, 239)**(2*k+1)/F(2*k+1)
    assert pi_error < F(1, 1 << (q+10)) and 3 < pi < 4
    theta = 2*pi*u
    terms = q+30
    s = sum(((-1)**n*theta**(2*n+1)/factorial(2*n+1)
             for n in range(terms)), F())
    c = sum(((-1)**n*theta**(2*n)/factorial(2*n)
             for n in range(terms)), F())
    assert F(8)**(2*terms)/factorial(2*terms) < F(1, 1 << (q+10))
    c, s = dyad(c, q+5), dyad(s, q+5)
    eta = 1 if c >= 0 else -1
    assert 1+eta*c >= 1
    t = dyad(eta*s/(1+eta*c), q)
    out = Q(eta*(1-t*t)/(1+t*t), eta*2*t/(1+t*t))
    assert out*out.conjugate() == Q(1)
    return out


def finite_unitary(d, cells, p=7, q=20):
    uniforms = iter(F(2*x+1, 1 << (p+1)) for x in cells)
    sections = []

    def rec(m):
        if m == 1:
            return [[rational_phase(next(uniforms), q)]]
        us = [next(uniforms) for _ in range(m-1)]
        ts = [1-root_floor(1-u, m-j-1, 2*q) for j, u in enumerate(us)]
        xs, rem = [], F(1)
        for t in ts:
            xs.append(t*rem)
            rem *= 1-t
        xs.append(rem)
        assert sum(xs) == 1 and min(xs) >= 0
        phases = [Q(1)]+[rational_phase(next(uniforms), q) for _ in range(m-1)]
        v = [phases[i]*root_floor(xs[i], 2, q) for i in range(m)]
        a = rational_phase(next(uniforms), q)
        lower = rec(m-1)
        w = v.copy()
        w[0] = w[0]+1
        norm = sum((z*z.conjugate() for z in w), Q())
        assert not norm.im and norm.re >= 1
        sections.append(norm.re)
        refl = [[Q(-int(i == j))+2*w[i]*w[j].conjugate()/norm
                 for j in range(m)] for i in range(m)]
        assert matmul(adj(refl), refl) == eye(m)
        block = [[Q() for _ in range(m)] for _ in range(m)]
        block[0][0] = a
        for i in range(m-1):
            for j in range(m-1):
                block[i+1][j+1] = lower[i][j]
        out = matmul(refl, block)
        assert matmul(adj(out), out) == eye(m)
        return out

    out = rec(d)
    try:
        next(uniforms)
        raise AssertionError('unused uniform')
    except StopIteration:
        pass
    return out, sections


def cluster_ray(a, h):
    d = len(a)
    ray = {}
    for rows in product(range(d), repeat=h):
        z = det([[a[row][col] for col in range(h)] for row in rows])
        if z:
            ray[rows] = z
    norm = sum((z*z.conjugate() for z in ray.values()), Q())
    assert not norm.im and norm.re >= 0
    if norm:
        density = {(x, y): a*b.conjugate()/norm
                   for x, a in ray.items() for y, b in ray.items()}
        assert sum((v for (x, y), v in density.items() if x == y), Q()) == Q(1)
        assert all(density[(y, x)] == z.conjugate()
                   for (x, y), z in density.items())
        # PSD is exact by the displayed outer product with positive norm.
    return ray, norm.re


def partitions(n, d, maxpart=None):
    if d == 0:
        if n == 0:
            yield ()
        return
    if maxpart is None:
        maxpart = n
    for a in range(min(n, maxpart), -1, -1):
        for tail in partitions(n-a, d-1, a):
            yield (a,)+tail


def weyl(lam):
    d = len(lam)
    z = prod(F(lam[i]-lam[j]+j-i, j-i)
             for i in range(d) for j in range(i+1, d))
    assert z.denominator == 1
    return int(z)


def specht(lam):
    hooks = []
    for i, row in enumerate(lam):
        for j in range(row):
            below = sum(x > j for x in lam[i+1:])
            hooks.append(row-j+below)
    z = F(factorial(sum(lam)), prod(hooks))
    assert z.denominator == 1
    return int(z)


def character(e, lam):
    d, n = len(e)-1, sum(lam)
    hs = [F(1)]
    for k in range(1, n+d+1):
        hs.append(sum(((-1)**(j-1)*e[j]*hs[k-j]
                       for j in range(1, min(d, k)+1)), F()))
    h = lambda k: hs[k] if k >= 0 else F(0)
    z = det([[Q(h(lam[i]-i+j)) for j in range(d)] for i in range(d)])
    assert not z.im
    return z.re


def elem(a):
    d = len(a)
    return [F(1)]+[sum((det([[a[i][j] for j in inds] for i in inds]).re
                         for inds in combinations(range(d), k)), F())
                  for k in range(1, d+1)]


def column_highest(lam):
    heights = [sum(x > j for x in lam) for j in range(lam[0])]
    states = {(): 1}
    for h in heights:
        nxt = {}
        for s, x in states.items():
            for p in permutations(range(h)):
                inv = sum(p[i] > p[j] for i in range(h) for j in range(i+1, h))
                nxt[s+p] = x*(-1)**inv
        states = nxt
    for s in states:
        assert tuple(s.count(i) for i in range(len(lam))) == lam
    for a in range(len(lam)):
        for b in range(a+1, len(lam)):
            raised = {}
            for s, x in states.items():
                for k, value in enumerate(s):
                    if value == b:
                        t = s[:k]+(a,)+s[k+1:]
                        raised[t] = raised.get(t, 0)+x
            assert not any(raised.values())
    cas = {}
    for s, x in states.items():
        for i in range(len(s)):
            for j in range(i+1, len(s)):
                t = list(s)
                t[i], t[j] = t[j], t[i]
                t = tuple(t)
                cas[t] = cas.get(t, 0)+x
    content = sum(j-i for i, row in enumerate(lam) for j in range(row))
    assert {k: v for k, v in cas.items() if v} == {
        k: content*v for k, v in states.items() if content*v}
    return len(states)


def dense_tensor(a, b):
    return [[x*y for x in ra for y in rb] for ra in a for rb in b]


def add_mats(ms, weights):
    d = len(ms[0])
    return [[sum((m[i][j]*w for m, w in zip(ms, weights)), Q())
             for j in range(d)] for i in range(d)]


def qubit_twirl_checks():
    pure = [
        [[Q(1), Q()], [Q(), Q()]],
        [[Q(), Q()], [Q(), Q(1)]],
        [[Q(F(1, 2)), Q(F(1, 2))], [Q(F(1, 2)), Q(F(1, 2))]],
        [[Q(F(1, 2)), Q(F(-1, 2))], [Q(F(-1, 2)), Q(F(1, 2))]],
        [[Q(F(1, 2)), Q(0, F(-1, 2))], [Q(0, F(1, 2)), Q(F(1, 2))]],
        [[Q(F(1, 2)), Q(0, F(1, 2))], [Q(0, F(-1, 2)), Q(F(1, 2))]],
    ]
    fixtures = []
    for n in (2, 3):
        ds = list(product(range(2), repeat=n))
        indices = {s: i for i, s in enumerate(ds)}
        psym = [[Q() for _ in ds] for _ in ds]
        for p in permutations(range(n)):
            for i, s in enumerate(ds):
                j = indices[tuple(s[k] for k in p)]
                psym[j][i] = psym[j][i]+F(1, factorial(n))
        powers = []
        for rho in pure:
            state = [[Q(1)]]
            for _ in range(n):
                state = dense_tensor(state, rho)
            powers.append(state)
        mean = add_mats(powers, [F(1, 6)]*6)
        assert mean == [[x/F(n+1) for x in row] for row in psym]
        fixtures.append({'d': 2, 'N': n, 'lambda': [n], 'exact': True})
        if n == 3:
            singlet = [[Q() for _ in range(4)] for _ in range(4)]
            singlet[1][1] = singlet[2][2] = Q(F(1, 2))
            singlet[1][2] = singlet[2][1] = Q(F(-1, 2))
            base = dense_tensor(singlet, [[Q(F(1, 2)), Q()], [Q(), Q(F(1, 2))]])
            terms = []
            for p in permutations(range(n)):
                perm = [indices[tuple(s[k] for k in p)] for s in ds]
                out = [[Q() for _ in ds] for _ in ds]
                for i in range(len(ds)):
                    for j in range(len(ds)):
                        out[perm[i]][perm[j]] = base[i][j]
                terms.append(out)
            mean = add_mats(terms, [F(1, 6)]*6)
            assert mean == [[(Q(int(i == j))-psym[i][j])/4
                             for j in range(8)] for i in range(8)]
            fixtures.append({'d': 2, 'N': 3, 'lambda': [2, 1], 'exact': True})
    return fixtures


def capped_first_accept_check():
    weights = [F(1, 4), F(1, 2), F(1, 4)]
    accepts = [F(1, 8), F(1, 2), F(3, 4)]
    mu = sum(w*a for w, a in zip(weights, accepts))
    k = 4
    final = [F()]*3
    fail = F(1)
    for _ in range(k):
        for j in range(3):
            final[j] += fail*weights[j]*accepts[j]
        fail *= 1-mu
    assert sum(final)+fail == 1
    assert [x/(1-fail) for x in final] == [w*a/mu for w, a in zip(weights, accepts)]
    return {'trials': k, 'conditional_law_exact': True, 'failure': str(fail)}


def main():
    start = perf_counter()
    units, rays, filters = [], [], []
    for d, cells in ((2, [0, 127, 64, 31]),
                     (2, [127, 0, 32, 96]),
                     (3, [0, 127, 64, 31, 96, 0, 127, 63, 65]),
                     (3, [127, 126, 1, 32, 96, 64, 0, 127, 33])):
        u, sections = finite_unitary(d, cells)
        assert matmul(adj(u), u) == eye(d)
        bits = max(x.numerator.bit_length()+x.denominator.bit_length()
                   for row in u for z in row for x in (z.re, z.im))
        units.append({'d': d, 'exact_unitary': True, 'min_section_norm': str(min(sections)),
                      'max_entry_bit_sum': bits})
        for h in range(1, d+1):
            ray, norm = cluster_ray(u, h)
            assert norm == factorial(h)
            rays.append({'d': d, 'h': h, 'norm_squared': str(norm),
                         'nonzero_coordinates': len(ray)})
        for diag in (([F(2), F(1)] if d == 2 else [F(3), F(2), F(1)]),
                     ([F(2), F(0)] if d == 2 else [F(2), F(1), F(0)]),
                     ([F(1), F(1, 1 << 18)] if d == 2 else [F(2), F(1), F(1, 1 << 18)])):
            g = [[Q(diag[i] if i == j else 0) for j in range(d)] for i in range(d)]
            e = matmul(adj(g), g)
            es = elem(e)
            gu = matmul(g, u)
            rank = sum(bool(x) for x in diag)
            m = es[rank]/es[rank-1]
            ai = [x*x for x in diag if x]
            assert m <= min(ai)
            for lam in partitions(3, d):
                chi = character(es, lam)
                rlam = weyl(lam)
                legal = sum(x > 0 for x in lam) <= rank
                assert (chi > 0) == legal
                if not legal:
                    assert chi == 0
                    continue
                M = prod(ai[i]**lam[i] for i in range(rank))
                upper = [x+m/F(16*3) for x in ai]
                B = prod(upper[i]**lam[i] for i in range(rank))
                assert M <= B < 2*M and M <= chi <= rlam*M
                t = F(1)
                for h in range(1, d+1):
                    nh = lam[h-1]-(lam[h] if h < d else 0)
                    if nh:
                        ray, norm = cluster_ray(gu, h)
                        t *= (norm/factorial(h))**nh
                assert 0 <= t <= M <= B
                p = t/B
                b = 9
                threshold = (p*(1 << b)).numerator//(p*(1 << b)).denominator
                pb = F(threshold, 1 << b)
                assert 0 <= p-pb < F(1, 1 << b)
                filters.append({'d': d, 'rank': rank, 'lambda': list(lam),
                                'exact_character_envelope_acceptance': True,
                                'positive_norm': bool(t),
                                'max_density_bits_charged': True})
    dimensions, highest = [], []
    for d in (2, 3):
        for n in range(1, 7):
            labels = list(partitions(n, d))
            assert sum(weyl(lam)*specht(lam) for lam in labels) == d**n
            dimensions.append({'d': d, 'N': n, 'labels': len(labels)})
            if n <= 5:
                for lam in labels:
                    highest.append({'d': d, 'N': n, 'lambda': list(lam),
                                    'support': column_highest(lam)})
    laws = []
    for j in range(2, 8):
        b = 5
        counts = [0]*j
        for v in range(1 << b):
            counts[j*v//(1 << b)] += 1
        tv = sum((abs(F(c, 1 << b)-F(1, j)) for c in counts), F())/2
        assert tv <= F(j, 1 << b)
        laws.append({'j': j, 'exact_tv': str(tv)})
    # Posterior weights include a singularly annihilated sector exactly.
    e = elem([[Q(4), Q()], [Q(), Q(0)]])
    q = {(3, 0): F(1, 3), (2, 1): F(2, 3)}
    zs = {lam: character(e, lam)/weyl(lam) for lam in q}
    Z = sum(q[lam]*zs[lam] for lam in q)
    posterior = {str(lam): str(q[lam]*zs[lam]/Z) for lam in q}
    assert posterior == {'(3, 0)': '1', '(2, 1)': '0'}
    out = {'status': 'PASS', 'arithmetic': 'exact Fraction/Q(i)',
           'scope': 'tiny identities only; no general spectral/Haar/hardware backend',
           'unitaries': units, 'cluster_rays': rays, 'filters': filters,
           'dimension_checks': dimensions, 'highest_weight_casimir_checks': highest,
           'qubit_twirl_checks': qubit_twirl_checks(),
           'bounded_first_accept': capped_first_accept_check(),
           'permutation_law_checks': laws, 'singular_posterior': posterior}
    out['runtime_seconds'] = perf_counter()-start
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'runtime_seconds': out['runtime_seconds'],
                      'unitaries': len(units), 'cluster_rays': len(rays),
                      'filtered_checks': len(filters), 'dimensions': len(dimensions),
                      'highest_weight_checks': len(highest), 'qubit_twirls': 3}))


if __name__ == '__main__':
    main()
