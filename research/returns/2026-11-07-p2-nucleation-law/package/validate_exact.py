"""Finite exact checks; no claim of a scalable two-dimensional solver.

The 3x3 calculation enumerates all 512 microscopic configurations and uses
only genuine graph automorphisms for an exact orbit quotient. All generator,
Poisson, soft-source, moment and inequality checks use Fraction arithmetic.
The stripe-family check exhaustively computes local pattern histograms for
selected finite r. Its general proof is in the report.
"""

from fractions import Fraction as F
from itertools import permutations, product
from collections import Counter
from pathlib import Path
import json
import time

from residence_law import make_record, cdf_interval, jsonable, exp_minus_interval


def solve(a, b):
    """Exact dense elimination, intended only for small validation matrices."""
    n = len(b)
    c = [[F(x) for x in row] + [F(bi)] for row, bi in zip(a, b)]
    for j in range(n):
        pivot = next(k for k in range(j, n) if c[k][j])
        c[j], c[pivot] = c[pivot], c[j]
        z = c[j][j]
        c[j] = [v / z for v in c[j]]
        for k in range(n):
            if k != j and c[k][j]:
                z = c[k][j]
                c[k] = [v - z * w for v, w in zip(c[k], c[j])]
    x = [c[i][-1] for i in range(n)]
    assert all(sum((a[i][j] * x[j] for j in range(n)), F(0)) == b[i]
               for i in range(n))
    return x


def torus3_orbits():
    maps = []
    for p, q, swap in product(permutations(range(3)), permutations(range(3)), (0, 1)):
        maps.append([q[j] * 3 + p[i] if swap else p[i] * 3 + q[j]
                     for i in range(3) for j in range(3)])
    rep, orbits = {}, {}
    for s in range(512):
        if s in rep:
            continue
        orb = {sum(((s >> i) & 1) << perm[i] for i in range(9)) for perm in maps}
        a = min(orb)
        orbits[a] = sorted(orb)
        for x in orb:
            rep[x] = a
    return rep, orbits


def ising_check(u, v, kappa):
    start = time.perf_counter()
    rep, orbits = torus3_orbits()
    ds = sorted(a for a in orbits if a.bit_count() <= 4)
    idx = {a: i for i, a in enumerate(ds)}
    neighbors = []
    for i, j in product(range(3), repeat=2):
        neighbors.append([((i + d) % 3) * 3 + j for d in (-1, 1)] +
                         [i * 3 + (j + d) % 3 for d in (-1, 1)])
    edges = [(i, j) for i in range(9) for j in neighbors[i] if i < j]
    m = len(ds)
    h = [[F(0) for _ in ds] for _ in ds]
    w = []
    for a in ds:
        i = idx[a]
        spins = [1 if (a >> j) & 1 else -1 for j in range(9)]
        disagree = sum(spins[j] != spins[k] for j, k in edges)
        w.append(F(len(orbits[a])) * u ** disagree * v ** (9 - a.bit_count()))
        for j in range(9):
            ratio = u ** (spins[j] * sum(spins[k] for k in neighbors[j])) * v ** spins[j]
            rate = ratio / (1 + ratio)
            h[i][i] += rate
            b = a ^ (1 << j)
            if b.bit_count() <= 4:
                h[i][idx[rep[b]]] -= rate
    assert all(w[i] * h[i][j] == w[j] * h[j][i] for i in range(m) for j in range(m))
    means = solve(h, [F(1)] * m)
    seconds = solve(h, [2 * z for z in means])
    t = means[idx[0]]
    assert max(means) == t
    assert max(seconds) == seconds[idx[0]]
    d = 1 - seconds[idx[0]] / (2 * t * t)
    core = [i for i, a in enumerate(ds) if a.bit_count() <= 1]
    za = sum((w[i] for i in core), F(0))
    d0 = t - sum((w[i] * means[i] for i in core), F(0)) / za
    hk = [row[:] for row in h]
    for i in core:
        hk[i][i] += kappa
    vv = solve(hk, [kappa if i in core else F(0) for i in range(m)])
    assert all(0 <= z <= 1 for z in vv)
    cap = kappa * sum((w[i] * (1 - vv[i]) for i in core), F(0))
    nn = sum((w[i] * vv[i] for i in range(m)), F(0))
    na = sum((w[i] * vv[i] for i in core), F(0))
    assert na == za - cap / kappa
    q = nn / cap
    nu = [kappa * w[i] * (1 - vv[i]) / cap if i in core else F(0) for i in range(m)]
    assert sum(nu, F(0)) == 1
    assert sum((nu[i] * means[i] for i in range(m)), F(0)) == q
    assert sum((nu[i] * seconds[i] for i in range(m)), F(0)) == 2 * sum((w[i] * vv[i] * means[i] for i in range(m)), F(0)) / cap
    assert q <= t <= (1 + kappa * d0) * q + d0
    eta = (nn - na) / nn
    rho = cap / za
    rec = make_record(q, q, d0, rho, kappa, eta, bits=64)
    assert d <= rec['defect_upper']
    assert rec['mean_lower'] <= t <= rec['mean_upper']
    record = {
        'input': {'u':u, 'v':v, 'kappa':kappa, 'L':3, 'target':'at least 5 plus spins', 'core':'at most 1 plus spin'},
        'microscopic_states':512, 'killed_states':256, 'killed_orbits':m,
        'mean':t, 'second_moment':seconds[idx[0]], 'actual_defect':d,
        'd0':d0, 'normalized_capacity':rho, 'residence_fraction':eta,
        'certificate':rec, 'cdf_interval_at_exact_mean':cdf_interval(rec,t,64),
        'elapsed_seconds':time.perf_counter()-start,
        'scope':'finite exact identity check, not polynomial evidence for growing boxes',
    }
    return record


def stripe_check(r, u, v, repeat=1):
    m, length = 2*r+1, 10*(2*r+1)*repeat
    x = ([1]*m + [-1]*(3*m) + [1]*(3*m) + [-1]*(3*m))*repeat
    y = ([1]*(2*m) + [-1]*(3*m) + [1]*(2*m) + [-1]*(3*m))*repeat
    def histogram(seq):
        return Counter(tuple(seq[(j+k) % length] for k in range(-r,r+1)) for j in range(length))
    assert histogram(x) == histogram(y)
    def decrement_rates(seq):
        ans = Counter()
        for j, spin in enumerate(seq):
            if spin != 1:
                continue
            # Number of all-plus horizontal m-windows containing this column.
            k = sum(all(seq[(a+h) % length] == 1 for h in range(m))
                    for a in range(j-m+1,j+1))
            if not k:
                continue
            total_neighbors = 2 + seq[(j-1)%length] + seq[(j+1)%length]
            ratio = u ** total_neighbors * v
            rate = ratio / (1 + ratio)
            ans[m*k] += length * rate
        return ans
    rx, ry = decrement_rates(x), decrement_rates(y)
    q4 = u**4*v/(1+u**4*v)
    diff = (m-2)*repeat*length*q4
    assert rx[m]-ry[m] == diff
    d = diff/(length*length)
    return {'r':r,'repeat':repeat,'side_length':length,'states_outside_target':True,
            'pattern_histograms_equal':True,'minus_m_jump_rate_difference':diff,
            'per_site_rate_difference':d,'comparison_time':d/(2*length*length),
            'total_variation_separation_lower':d*d/4,
            'scope':'failure of exact local-histogram lumping, not a first-passage lower bound'}


def two_stage(e):
    h = [[e,-e],[-e*e,e+e*e]]
    m = solve(h,[F(1),F(1)])
    sec = solve(h,[2*z for z in m])
    d = 1-sec[0]/(2*m[0]*m[0])
    assert m[0] == (2+e)/e
    assert d == 1/(2+e)**2
    return {'epsilon':e,'mean':m[0],'defect':d,'exterior_residence_fraction':1/(2+e),
            'scope':'reversible ordered birth-death family, not an Ising embedding'}


def main():
    output = {
        'ising_exact':[ising_check(F(1,4),F(3,4),F(1,16)),
                       ising_check(F(1,8),F(15,16),F(1,64))],
        'local_histogram_checks':[stripe_check(r,F(1,4),F(3,4)) for r in (1,2,3,5,8)] +
                                 [stripe_check(r,F(1,4),F(3,4),3) for r in (1,2)],
        'two_stage_checks':[two_stage(F(1,2**k)) for k in (2,4,8,16)],
    }
    rec = make_record(7,7,0,F(1,8),1,0,64)
    assert rec['mean_lower']==rec['mean_upper']==7
    assert rec['defect_upper']==0
    lo,hi=cdf_interval(rec,F(7,2),64)
    a,b=exp_minus_interval(F(1,2),64)
    assert (lo,hi)==(1-b,1-a)
    output['one_stage_check']={'record':rec,'cdf_at_half_mean':[lo,hi],
                               'huge_time_cdf':cdf_interval(rec,2**4096,64)}
    path=Path(__file__).with_name('VALIDATION.json')
    path.write_text(json.dumps(jsonable(output),indent=2)+'\n')
    for rec in output['ising_exact']:
        print(json.dumps({'u':str(rec['input']['u']),'orbits':rec['killed_orbits'],
                          'mean':float(rec['mean']),'defect':float(rec['actual_defect']),
                          'defect_bound':float(rec['certificate']['defect_upper']),
                          'CDF_error_bound':float(rec['certificate']['kolmogorov_upper']),
                          'seconds':rec['elapsed_seconds']}))
    print('All exact checks passed. '+str(path))


if __name__=='__main__':
    main()
