"""Exact finite algebra checks for the independently reconstructed CL gate.

These are not execution of the FPRAS and do not establish a universal theorem.
Only the Python standard library is needed.
"""
from fractions import Fraction as F
from itertools import permutations
import json
import random


def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def det2(A):
    r = len(A)
    answer = (F(0), F(0))
    for p in permutations(range(r)):
        sign = -1 if sum(p[i] > p[j] for i in range(r) for j in range(i+1, r)) % 2 else 1
        term = (F(sign), F(0))
        for i in range(r):
            term = cmul(term, A[i][p[i]])
        answer = (answer[0]+term[0], answer[1]+term[1])
    return answer[0]**2 + answer[1]**2


def coefficients(A):
    n, r = len(A), len(A[0])
    result = {}
    for s in range(1 << n):
        if s.bit_count() == r:
            value = det2([A[i] for i in range(n) if s >> i & 1])
            if value:
                result[s] = value
    assert result
    return result


def submasks(s):
    t = s
    while True:
        yield t
        if not t:
            break
        t = (t-1) & s


def zproduct(s, z):
    result = F(1)
    for i, zi in enumerate(z):
        if s >> i & 1:
            result *= zi
    return result


def extension(mu, z):
    answer = {}
    for s, v in mu.items():
        for h in submasks(s):
            answer[h] = answer.get(h, F(0)) + v
    return {s: v*zproduct(s, z) for s, v in answer.items()}


def audit_case(mu, nu, n, z, t, rng):
    full = (1 << n)-1
    mh, nh = extension(mu, z), extension(nu, z)
    states = [s | (h << n) for s in mh for h in nh]
    w = {x: mh[x & full]*nh[x >> n] for x in states}
    psi = {x: zproduct((x & full) & (x >> n), t) for x in states}
    norm = sum(w[x]*psi[x] for x in states)
    pi = {x: w[x]*psi[x]/norm for x in states}
    d = 2*n
    rates = {}
    for x in states:
        row = {}
        for u in range(d):
            y = x ^ (1 << u)
            if y in w:
                row[y] = psi[y]/psi[x] if x >> u & 1 else w[y]/w[x]
        rates[x] = row
    # Detailed balance, now that every row has been created.
    for x in states:
        for y, q in rates[x].items():
            assert pi[x]*q == pi[y]*rates[y][x]
    for repeat in range(5):
        f = {x: F(rng.randint(-12, 12)) for x in states}
        Lf = {x: sum(q*(f[x]-f[y]) for y, q in rates[x].items()) for x in states}
        dirichlet = sum(pi[x]*f[x]*Lf[x] for x in states)
        lhs = sum(pi[x]*Lf[x]**2 for x in states)-dirichlet
        rhs = F(0)
        for x in states:
            up = [u for u in range(d) if not x >> u & 1]
            down = [u for u in range(d) if x >> u & 1]
            for u in up:
                xu = x | (1 << u)
                gu = f.get(xu, F(0))-f[x]
                bu = w.get(xu, F(0))/w[x]
                for v in up:
                    xv = x | (1 << v)
                    gv = f.get(xv, F(0))-f[x]
                    bv = w.get(xv, F(0))/w[x]
                    curvature = bu**2 if u == v else bu*bv-w.get(xu | (1 << v), F(0))/w[x]
                    rhs += pi[x]*curvature*gu*gv
            for u in down:
                xu = x & ~(1 << u)
                gu = f[x]-f[xu]
                bu = psi[xu]/psi[x]
                for v in down:
                    xv = x & ~(1 << v)
                    gv = f[x]-f[xv]
                    bv = psi[xv]/psi[x]
                    curvature = bu**2-bu if u == v else bu*bv-psi[xu & ~(1 << v)]/psi[x]
                    rhs += pi[x]*curvature*gu*gv
            for u in up:
                for v in up:
                    if u == v:
                        continue
                    y = x | (1 << u) | (1 << v)
                    if y in w:
                        delta = f[y]-f[x | (1 << u)]-f[x | (1 << v)]+f[x]
                        rhs += w[y]*psi[x]/norm * delta**2
        assert lhs == rhs, (n, lhs, rhs)
        assert lhs >= 0

    pairs = [(s, h) for s in mu for h in nu]
    pw = {(s,h): mu[s]*nu[h]*zproduct(s & h, t)*zproduct(s,z)*zproduct(h,z) for s,h in pairs}
    pnorm = sum(pw.values())
    pp = {x: v/pnorm for x,v in pw.items()}
    qrates = {}
    for s, h in pairs:
        row = {}
        for which, current, other, values in [(0,s,h,mu),(1,h,s,nu)]:
            for u in range(n):
                if not current >> u & 1:
                    continue
                deleted = current & ~(1 << u)
                denominator = sum(z[v]*values.get(deleted | (1 << v), F(0)) for v in range(n) if not deleted >> v & 1)
                assert denominator > 0
                for v in range(n):
                    if current >> v & 1:
                        continue
                    replaced = deleted | (1 << v)
                    value = values.get(replaced, F(0))
                    if value:
                        y = (replaced,h) if which == 0 else (s,replaced)
                        rate = z[v]*value/denominator
                        if other >> u & 1:
                            rate /= t[u]
                        row[y] = row.get(y, F(0))+rate
        qrates[(s,h)] = row
    for x in pairs:
        for y,q in qrates[x].items():
            assert pp[x]*q == pp[y]*qrates[y][x]
    for repeat in range(5):
        f = {x: F(rng.randint(-12,12)) for x in pairs}
        mean = sum(pp[x]*f[x] for x in pairs)
        variance = sum(pp[x]*(f[x]-mean)**2 for x in pairs)
        energy = sum(pp[x]*sum(q*(f[x]-f[y])**2 for y,q in qrates[x].items()) for x in pairs)/2
        assert energy >= variance
    # The tilt/complement local inequality for uniform penalties.
    if len(set(t)) == 1:
        scalar = t[0]
        for u in range(n):
            p = [F(0),F(0),F(0)]
            for (s,h),v in pp.items():
                p[(s >> u & 1)+(h >> u & 1)] += v
            assert p[0]*p[2] <= 4*scalar*p[1]**2
    return len(states), len(pairs)


def main():
    rng = random.Random(630507)
    sizes = []
    for index in range(8):
        n = 3+index % 2
        a = n//2
        b = n-a
        def matrix(r):
            return [[(F(rng.randint(-3,3),rng.randint(1,3)), F(rng.randint(-2,2),rng.randint(1,3))) for j in range(r)] for i in range(n)]
        mu,nu = coefficients(matrix(a)),coefficients(matrix(b))
        z = [F(2)**rng.randint(-10,10) for i in range(n)]
        t = [F(1,256*n*n)]*n if index % 2 == 0 else [F(rng.randint(1,3),rng.randint(4,9)) for i in range(n)]
        sizes.append(audit_case(mu,nu,n,z,t,rng))
    # Full-column-rank but empty single-occupancy projection.
    A = [[(F(1),F(0)),(F(0),F(0))],[(F(0),F(0)),(F(1),F(0))],[(F(0),F(0)),(F(0),F(0))],[(F(0),F(0)),(F(0),F(0))]]
    weights = coefficients(A)
    assert sum(value for s,value in weights.items() if (s&3).bit_count()==1 and ((s>>2)&3).bit_count()==1)==0
    print(json.dumps({"status":"PASS","rational_complex_instances":8,"exact_bochner_identities":40,"exchange_dirichlet_checks":40,"uniform_penalty_local_tilt_checks":12,"empty_projected_support_examples":1,"state_sizes":sizes,"full_fpras_executed":False},indent=2))


if __name__ == "__main__":
    main()
