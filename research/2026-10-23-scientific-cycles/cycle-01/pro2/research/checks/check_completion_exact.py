"""Exact Fraction checks of the common-action completion formulas.

Tiny deterministic fixtures only: no old spectral experiment is rerun.
The mathematical proof is notes/completion_challenge.md.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import resource
import time


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def tr(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = tr(b)
    return [[sum((x*y for x, y in zip(row, col)), F(0)) for col in bt]
            for row in a]


def add(a, b, c=F(1)):
    return [[x+c*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def inv(a):
    n = len(a)
    b = [row[:] + eye(n)[i] for i, row in enumerate(a)]
    for i in range(n):
        j = next(j for j in range(i, n) if b[j][i])
        b[i], b[j] = b[j], b[i]
        p = b[i][i]
        b[i] = [x/p for x in b[i]]
        for j in range(n):
            if j != i:
                p = b[j][i]
                b[j] = [x-p*y for x, y in zip(b[j], b[i])]
    return [row[n:] for row in b]


def inertia(a):
    """Congruence elimination, including zero-diagonal 2-by-2 pivots."""
    a = [row[:] for row in a]
    neg = zero = pos = 0
    while a:
        n = len(a)
        inds = [i for i in range(n) if a[i][i]]
        if inds:
            i = inds[0]
            inds = [i] + [j for j in range(n) if j != i]
            a = [[a[i][j] for j in inds] for i in inds]
            p = a[0][0]
            neg += p < 0
            pos += p > 0
            a = [[a[i][j]-a[i][0]*a[0][j]/p for j in range(1,n)]
                 for i in range(1,n)]
        else:
            pairs = [(i,j) for i in range(n) for j in range(i+1,n) if a[i][j]]
            if not pairs:
                zero += n
                break
            i,j = pairs[0]
            inds = [i,j] + [k for k in range(n) if k not in (i,j)]
            a = [[a[i][j] for j in inds] for i in inds]
            p = a[0][1]
            neg += 1
            pos += 1
            a = [[a[i][j]-(a[i][0]*a[1][j]+a[i][1]*a[0][j])/p
                  for j in range(2,n)] for i in range(2,n)]
    return (neg, zero, pos)


def cdf_count(a, t):
    ni = inertia(add(a, eye(len(a)), -t))
    return ni[0]+ni[1]


def check_fixture(name, a, x, lower, upper, strict):
    n, d = len(a), len(x[0])
    I = eye(n)
    y = mm(a,x)
    g,t,h = mm(tr(x),x),mm(tr(x),y),mm(tr(y),y)
    hl,hu = add(t,g,-lower),add(scale(g,upper),t,F(-1))
    assert inertia(g) == (0,0,d)
    assert inertia(hl) == inertia(hu) == (0,0,d)
    assert t == tr(t)
    zl,zu = add(y,x,-lower),add(scale(x,upper),y,F(-1))
    bl = add(scale(I,lower),mm(mm(zl,inv(hl)),tr(zl)))
    bu = add(scale(I,upper),mm(mm(zu,inv(hu)),tr(zu)),F(-1))
    assert mm(bl,x) == mm(bu,x) == y
    delta = add(bu,bl,F(-1))
    assert inertia(delta)[0] == 0
    assert mm(delta,x) == [[F(0)]*d for _ in range(n)]
    assert inertia(add(bl,I,-lower))[0] == 0
    assert inertia(add(scale(I,upper),bu,F(-1)))[0] == 0
    assert inertia(add(a,bl,F(-1)))[0] == 0
    assert inertia(add(bu,a,F(-1)))[0] == 0
    N = add(add(scale(t,lower+upper),g,-lower*upper),h,F(-1))
    assert inertia(N)[0] == 0
    q = inertia(delta)[2]
    if strict:
        assert inertia(add(a,I,-lower)) == (0,0,n)
        assert inertia(add(scale(I,upper),a,F(-1))) == (0,0,n)
        assert inertia(N) == (0,0,d)
        assert q == n-d
    assert cdf_count(bl,lower)-cdf_count(bu,lower) == q
    records = []
    thresholds = [lower+(upper-lower)*F(j,8) for j in range(9)]
    thresholds += [lower-F(1), upper+F(1)]
    for threshold in thresholds:
        nl,nu = cdf_count(bl,threshold),cdf_count(bu,threshold)
        assert 0 <= nl-nu <= q
        if lower <= threshold < upper:
            kl = add(add(h,t,-(threshold+lower)),g,lower*threshold)
            ku = add(add(h,t,-(threshold+upper)),g,upper*threshold)
            il,iu = inertia(kl),inertia(ku)
            assert nl == n-d+il[0]+il[1]
            assert nu == iu[2]+iu[1]
            assert nl-nu >= max(0,n-2*d)
        for w in [F(0),F(1,7),F(1,2),F(6,7),F(1)]:
            b = add(bl,delta,w)
            assert mm(b,x) == y
            assert nu <= cdf_count(b,threshold) <= nl
        records.append({'t':str(threshold),'min_count':nu,'max_count':nl})
    return {'name':name,'n':n,'d':d,'strict_interior':strict,
            'rank_interval_difference':q,'all_checks_pass':True,
            'tested_thresholds':records}


def main():
    started, cpu = time.perf_counter(),time.process_time()
    a = mat([[0,F(1,2),0,0],[F(1,2),0,F(1,3),0],
             [0,F(1,3),0,F(1,4)],[0,0,F(1,4),0]])
    b = mat([[F(1,4),F(1,8),0,0,0],[F(1,8),F(-1,4),F(1,8),0,0],
             [0,F(1,8),F(1,3),F(1,8),0],[0,0,F(1,8),F(-1,3),F(1,8)],
             [0,0,0,F(1,8),F(1,5)]])
    fixtures = [
        ('nonorthogonal_n4_d2',a,mat([[1,0],[1,1],[0,1],[0,0]]),F(-2),F(2),True),
        ('nonorthogonal_n5_d2',b,mat([[1,0],[1,1],[0,1],[1,-1],[0,1]]),F(-1),F(1),True),
        ('boundary_unique',mat([[-1,0],[0,1]]),mat([[1],[1]]),F(-1),F(1),False),
        ('boundary_partial',mat([[-1,0,0],[0,1,0],[0,0,0]]),mat([[1],[1],[0]]),F(-1),F(1),False),
    ]
    results = [check_fixture(*f) for f in fixtures]
    receipt = {'PASS':True,'arithmetic':'fractions.Fraction only',
               'fixtures':results,'wall_seconds':time.perf_counter()-started,
               'cpu_seconds':time.process_time()-cpu,
               'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
               'scope':'Finite exact fixtures complement, not replace, the universal proof.'}
    out=Path(__file__).resolve().parents[1]/'results/completion_exact_checks.json'
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__ == '__main__':
    main()
