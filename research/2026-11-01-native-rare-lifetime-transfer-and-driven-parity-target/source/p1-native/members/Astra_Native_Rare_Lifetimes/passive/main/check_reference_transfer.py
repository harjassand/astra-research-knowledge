"""Exact finite audits of the new reference transfer.

Generators, stationary probabilities, killed solves and mixed capacity
identities use Fraction. Transcendental bounds are diagnostics evaluated with
Python math, not machine-checked interval proofs. The ordinary proofs carry
the real-number inequalities. No Monte Carlo or physical source is used here.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import math
import time


def solve(a, b):
    n = len(b)
    z = [[F(x) for x in row] + [F(v)] for row, v in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if z[i][k])
        z[k], z[p] = z[p], z[k]
        d = z[k][k]
        z[k] = [x / d for x in z[k]]
        for i in range(n):
            if i != k:
                d = z[i][k]
                if d:
                    z[i] = [x - d*y for x, y in zip(z[i], z[k])]
    return [row[-1] for row in z]


def stationary(q):
    n = len(q)
    a = [[q[i][j] for i in range(n)] for j in range(n)]
    a[-1] = [F(1)] * n
    p = solve(a, [F(0)]*(n-1)+[F(1)])
    assert all(x > 0 for x in p) and sum(p) == 1
    assert all(sum(p[i]*q[i][j] for i in range(n)) == 0 for j in range(n))
    return p


def hit(q, p, target):
    bset = [i for i in range(len(q)) if i not in target]
    t = [F(0)]*len(q)
    vals = solve([[-q[i][j] for j in bset] for i in bset], [F(1)]*len(bset))
    for i, v in zip(bset, vals):
        t[i] = v
    b = sum(p[i] for i in bset)
    mu = sum(p[i]*t[i] for i in bset)
    return mu/b, mu, [1-v/mu for v in t], b


def make(n, eta, variant, product_reference=False):
    size = 1 << n
    q0 = [[F(0) for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for i in range(n):
            q0[x][x ^ (1 << i)] += 1
        for i in range(0 if product_reference else n-1):
            c = (x >> i) & 3
            nxt = ([1, 3, 2, 0] if i % 2 == 0 else [3, 0, 2, 1])[c]
            y = (x & ~(3 << i)) | (nxt << i)
            if y != x:
                q0[x][y] += F(1, 4)
    q = [[F(0) for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            if x == y or not q0[x][y]:
                continue
            mask = x ^ y
            i = (mask & -mask).bit_length()-1
            left = (x >> max(0, i-1)) & 1
            right = (x >> min(n-1, i+1)) & 1
            mid = (x >> i) & 1
            if variant == 0:
                sign = F((2*mid-1)*(1+left*right), 2)
            else:
                sign = F((2*left-1)*(2*right-1) + (1-2*mid), 2)
            assert abs(sign) <= 1
            q[x][y] = q0[x][y]*(1+eta*sign)
        q0[x][x] = -sum(q0[x])
        q[x][x] = -sum(q[x])
    assert all(sum(q0[x][y] for x in range(size)) == 0 for y in range(size))
    return q0, q


def targets(n):
    size = 1 << n
    if n == 3:
        return [frozenset(x for x in range(size) if mask & (1 << x))
                for mask in range(1, (1 << size)-1)]
    out = set()
    for k in range(1, n+1):
        for sites in combinations(range(n), k):
            for bits in product(range(2), repeat=k):
                out.add(frozenset(x for x in range(size)
                                 if all(((x >> i) & 1) == b for i, b in zip(sites, bits))))
    out.add(frozenset(x for x in range(size) if x.bit_count() % 2))
    out.add(frozenset(x for x in range(size) if 1 <= x.bit_count() <= n-1))
    return sorted(out, key=lambda a: (len(a), tuple(a)))


def bilinear(a, d, b):
    return sum(a[i]*sum(d[i][j]*b[j] for j in range(len(b))) for i in range(len(a)))


def audit(n, eta, variant, product_reference=False):
    q0, q = make(n, eta, variant, product_reference)
    size = len(q)
    p0 = [F(1, size)]*size
    p = stationary(q)
    assert p != p0
    # A non-neighbour odds ratio conditioned on all other bits. Failure of this
    # equality certifies that the actual stationary law is not a path Gibbs law.
    non_path_gibbs = p[0]*p[5] != p[1]*p[4]
    lam = max(-q0[x][x] for x in range(size))
    g = F(2)
    a0 = float(eta*lam/(1-eta))
    beta = a0/(1+a0)
    r = math.log(4*(n-1)/beta)/2
    u_met = 2*float(eta*lam)*r/(1-float(eta))-math.log1p(-beta)
    t_infinity = (math.log(4*(n-1))+2)/4
    contraction_a = 2*float(eta*lam)*t_infinity
    choices = [(u_met, 'Metzler')]
    if contraction_a < 0.5:
        choices.append((math.log((1-contraction_a)/(1-2*contraction_a)), 'resolvent'))
    if product_reference and contraction_a < 1:
        zz = n*float(eta)/(1-contraction_a)
        if zz < 1:
            choices.append((-math.log1p(-zz), 'product forcing'))
    u, u_method = min(choices)
    v = u-math.log1p(-float(eta))
    kglobal = math.sqrt(float(2*lam/g))
    logfactor = 2*math.asinh(kglobal*math.sinh(v/2))
    actual_u = max(abs(math.log(float(x/y))) for x, y in zip(p, p0))
    assert actual_u <= u
    d0 = [[-p0[i]*q0[i][j] for j in range(size)] for i in range(size)]
    d = [[-p[i]*q[i][j] for j in range(size)] for i in range(size)]
    dd = [[d[i][j]-d0[i][j] for j in range(size)] for i in range(size)]
    qd = [[-d[i][j]/p0[i] for j in range(size)] for i in range(size)]
    q0adj = [[p0[j]*q0[j][i]/p0[i] for j in range(size)] for i in range(size)]
    assert all(sum(d[i][j] for i in range(size)) == 0 for j in range(size))
    assert all((1-eta)*q0[x][y] <= q[x][y] <= (1+eta)*q0[x][y]
               for x in range(size) for y in range(size) if x != y)
    rows = []
    worst = 0.0
    selected = targets(n)
    for atarget in selected:
        m0, mu0, h0, b0 = hit(q0, p0, atarget)
        m, mu, h, b = hit(q, p, atarget)
        md, mud, hd, bd = hit(qd, p0, atarget)
        ma, mua, ha, ba = hit(q0adj, p0, atarget)
        assert mu0 == mua and ba == b0 == bd
        c0, cd = 1/mu0, 1/mud
        assert cd-c0 == bilinear(ha, dd, hd)
        assert bilinear(ha, d0, ha) == c0
        assert bilinear(hd, d, hd) == cd
        wr_min = min(p[i]/p0[i] for i in range(size))
        wr_max = max(p[i]/p0[i] for i in range(size))
        assert wr_min**2*b0/b <= m/md <= wr_max**2*b0/b
        ratio = float(m/m0)
        coarse_lo = math.exp(-3*u-logfactor)
        coarse_hi = math.exp(3*u+logfactor)
        assert coarse_lo <= ratio <= coarse_hi
        ptarget0 = float(1-b0)
        bminus = 1-math.exp(u)*ptarget0
        bplus = 1-math.exp(-u)*ptarget0
        if bminus > 0:
            lo = math.exp(-2*u-logfactor)*float(b0)/bplus
            hi = math.exp(2*u+logfactor)*float(b0)/bminus
            assert lo <= ratio <= hi
        else:
            lo, hi = coarse_lo, coarse_hi
        if product_reference:
            kappa = kglobal*math.expm1(v)
            rev_lo = math.exp(-3*u-v)/(1+kappa**2)
            rev_hi = math.exp(3*u+v)
            if bminus > 0:
                rev_lo = math.exp(-2*u-v)*float(b0)/(bplus*(1+kappa**2))
                rev_hi = math.exp(2*u+v)*float(b0)/bminus
            assert rev_lo <= ratio <= rev_hi
            lo, hi = max(lo, rev_lo), min(hi, rev_hi)
        worst = max(worst, abs(math.log(ratio)))
        if atarget in (frozenset([0]), frozenset(range(size//2))):
            rows.append(dict(target=sorted(atarget), exact_reference_mean=str(m0),
                             exact_actual_mean=str(m), ratio=ratio,
                             transferred_ratio_lower=lo, transferred_ratio_upper=hi))
    return dict(n=n, eta=str(eta), variant=variant, target_count=len(selected),
                product_reference=product_reference, stationary_method=u_method,
                stationary_Metzler_bound=u_met, resolvent_T_infinity=t_infinity,
                resolvent_contraction_a=contraction_a,
                stationary_law_nonuniform=True,
                violates_path_gibbs_conditional_identity=non_path_gibbs,
                actual_stationary_log_error=actual_u, certified_u=u,
                reference_max_exit=str(lam), beta=beta, relative_mix_time=r,
                K=kglobal, log_F=logfactor,
                generic_log_mean_factor=3*u+logfactor,
                largest_observed_log_mean_error=worst,
                actual_gap_lower=(1-float(eta))*math.exp(-2*u)*float(g),
                exact_capacity_identity_checks=len(selected), examples=rows)


def main():
    start = time.monotonic()
    rows = [audit(n, eta, variant, prod)
            for prod in (False, True) for n in (3, 4)
            for eta in (F(1, 1000), F(1, 100), F(1, 20))
            for variant in range(2)]
    out = dict(all_checks_passed=True, models=len(rows),
               target_checks=sum(r['target_count'] for r in rows),
               models_with_non_path_gibbs_stationarity=sum(
                   r['violates_path_gibbs_conditional_identity'] for r in rows),
               wall_seconds=time.monotonic()-start, results=rows,
               numerical_note='Fraction algebra exact; transcendental bound evaluations are floating diagnostics.')
    path = Path(__file__).with_name('reference_transfer_checks.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='results'}, indent=2))


if __name__ == '__main__':
    main()
