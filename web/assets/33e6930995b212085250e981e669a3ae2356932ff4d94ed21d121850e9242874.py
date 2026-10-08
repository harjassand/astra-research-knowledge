"""Exact finite convention checks; these do not validate the all-N proof."""
from collections import Counter, defaultdict
from fractions import Fraction
from math import factorial
from pathlib import Path
import itertools
import json


def partitions(n):
    p = [1] + [0] * n
    for j in range(1, n + 1):
        for s in range(j, n + 1):
            p[s] += p[s-j]
    return p


def full_mass(N, x):
    K = 1 + sum(partitions(N-1))
    ones = [i+1 for i, z in enumerate(x) if z]
    if not ones:
        return Fraction(1, K)
    c = Counter(b-a for a,b in zip(ones,ones[1:]))
    S = ones[-1]-ones[0]
    num = 1
    for u in c.values():
        num *= factorial(u)
    return Fraction(num, K*(N-S)*factorial(len(ones)-1))


def marginal(N, x):
    t = len(x)
    p = partitions(N-1)
    K = 1 + sum(p)
    ones = [i+1 for i,z in enumerate(x) if z]
    if not ones:
        return (1 + sum((Fraction(p[S]*max(N-S-t,0),N-S)
                         for S in range(N)), Fraction())) / K
    a = ones[0]
    b = t-ones[-1]
    c = Counter(v-u for u,v in zip(ones,ones[1:]))
    r = len(ones)-1
    dp = {(0,0):(1,0)}
    for j in range(1,N):
        nxt = defaultdict(lambda: [0,0])
        for u in range(c[j], (N-1)//j+1):
            w = factorial(u)//factorial(u-c[j])
            ell = u-c[j] if j>b else 0
            for (S,R),(A,B) in dp.items():
                if S+j*u<=N-1:
                    dst = nxt[S+j*u,R+u]
                    dst[0] += w*A
                    dst[1] += w*(B+ell*A)
        dp = nxt
    ans = Fraction()
    for (S,R),(A,B) in dp.items():
        if S>N-a or R<r:
            continue
        falling = factorial(R)//factorial(R-r)
        if R==r:
            ans += Fraction(A,(N-S)*falling)
        else:
            ans += Fraction(B,(N-S)*falling*(R-r))
    return ans/K


def stationary_renewal_mass(p,x):
    N = len(x)
    mu = sum(j*pj for j,pj in p.items())
    ones = [i+1 for i,z in enumerate(x) if z]
    if not ones:
        return sum(max(j-N,0)*pj for j,pj in p.items())/mu
    a = ones[0]
    b = N-ones[-1]
    v = (sum(pj for j,pj in p.items() if j>=a)/mu
         *sum(pj for j,pj in p.items() if j>b))
    for u,w in zip(ones,ones[1:]):
        v *= p.get(w-u,0)
    return v


def main():
    fixtures = 0
    conditional_checks = 0
    regret_checks = 0
    laws = [{1:Fraction(1)}, {2:Fraction(1)},
            {1:Fraction(1,3),3:Fraction(2,3)},
            {2:Fraction(2,7),5:Fraction(5,7)},
            {1:Fraction(1,17),20:Fraction(16,17)}]
    for N in range(1,10):
        brute = defaultdict(Fraction)
        strings = list(itertools.product((0,1),repeat=N))
        K = 1+sum(partitions(N-1))
        for x in strings:
            q = full_mass(N,x)
            for t in range(N+1):
                brute[x[:t]] += q
            for law in laws:
                assert stationary_renewal_mass(law,x) <= K*N*q
                regret_checks += 1
        assert brute[()]==1
        for law in laws:
            assert sum(stationary_renewal_mass(law,x) for x in strings)==1
        for x,q in brute.items():
            assert marginal(N,x)==q, (N,x,marginal(N,x),q)
            fixtures += 1
            if len(x)<N:
                assert brute[x+(0,)]+brute[x+(1,)]==q
                conditional_checks += 1
    out = dict(status="passed",max_N=9,prefix_marginals=fixtures,
               conditional_normalizations=conditional_checks,
               stationary_law_regret_checks=regret_checks,
               arithmetic="exact Fraction",
               scope="Finite DP/brute-force convention and regret fixtures only; not all-N proof or novelty.")
    Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':
    main()
