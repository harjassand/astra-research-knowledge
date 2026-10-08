"""Exact finite arithmetic diagnostics, not certification of the infinite proof."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json

V = ((2, 0), (2, 1), (1, 1), (0, 1), (-2, -2))
WORDS = [(1, f, 4) for f in (2, 3)]
WORDS += [(1, f1, f2, 4, f3, 4)
          for f1, f2, f3 in product((2, 3), repeat=3)]


def ff(n, m):
    r = 1
    for j in range(m):
        r *= max(n-j, 0)
    return r


def rates(x, b, ks):
    k0, k1, k2, k3, k4 = ks
    return (k0, k1*ff(x, 2), k2*ff(x, 4)*b,
            k3*ff(x, 4)*b, k4*ff(x, 5)*ff(b, 2))


def word(a, sequence, ks):
    state = (a, 0)
    probability = F(1)
    states = [state]
    for reaction in sequence:
        x, b = state
        rs = rates(x, b, ks)
        assert rs[reaction] > 0
        probability *= rs[reaction]/sum(rs)
        dx, db = V[reaction]
        state = (x+dx, b+db)
        states.append(state)
    assert all(b > 0 for x, b in states[1:-1])
    assert states[-1][1] == 0
    assert all(a <= x <= a+4 for x, b in states[:-1])
    assert -2 <= states[-1][0]-a <= 1
    return states[-1][0]-a, probability, states


def ceil(q):
    return -(-q.numerator//q.denominator)


def ceil_sqrt(q):
    n = isqrt(q.numerator//q.denominator)
    return n if F(n*n) == q else n+1


parameter_sets = [
    tuple(map(F, (1, 1, 1, 1, 1))),
    (F(10**6), F(1), F(1, 10**6), F(10**3), F(1, 10**3)),
    (F(1), F(10**6), F(1, 10**6), F(1, 10**6), F(10**6)),
    (F(1, 10**6), F(1, 10**3), F(10**6), F(1, 10**6), F(1)),
]
cases = 0
for ks in parameter_sets:
    k0, k1, k2, k3, k4 = ks
    aggregate = k2+k3
    theta = k2/aggregate
    eps = theta/16
    m = max(F(1), 2*k0/k1, (16*k0+4*k1)/aggregate,
            2*aggregate/k4, (16*k0+4*k1)/k4)
    db = 3*m+5*m*m
    threshold = max(8, ceil(8*m), 2*ceil_sqrt(db), ceil(32*m/theta))
    assert 4*eps+8*eps/2+(1-9*eps) == 1-eps
    for a in sorted(set([8, 16, 64, 1024, threshold,
                         threshold+1, 2*threshold+3])):
        endpoints = {v: F(0) for v in (-2, -1, 0, 1)}
        q = None
        for sequence in WORDS:
            delta, probability, states = word(a, sequence, ks)
            endpoints[delta] += probability
            if sequence == (1, 2, 4):
                q = probability
            for x, b in states[:-1]:
                rs = rates(x, b, ks)
                total = sum(rs)
                assert total >= k1*a*(a-1)
                if b == 0:
                    assert 1-rs[1]/total <= m/(a*a)
                elif b == 1:
                    assert 1-(rs[2]+rs[3])/total <= m/(a*a)
                    assert rs[2]/(rs[2]+rs[3]) == theta
                else:
                    assert (rs[2]+rs[3])/total <= m/a
                    assert (rs[0]+rs[1])/total <= m/(a*a*a)
        accepted = sum(endpoints.values())
        d = 1-accepted
        assert d >= 0
        assert q >= theta*(1-m/a-3*m/(a*a))
        assert d <= db/(a*a)
        assert endpoints[-2]+endpoints[-1] <= m/a
        if a >= threshold:
            assert q >= theta/2
            assert d <= F(1, 4)
            negative = (endpoints[-2]+endpoints[-1])/accepted
            plus = endpoints[1]/accepted
            assert negative <= eps
            assert plus >= 8*eps
            assert endpoints[-2]/accepted <= eps
            assert 1-plus <= 1-8*eps
        cases += 1

print(json.dumps({"status": "PASS", "arithmetic": "exact rational",
                  "parameter_sets": len(parameter_sets), "macro_states": cases,
                  "accepted_words_per_state": len(WORDS),
                  "checks": ["all ten legal paths", "endpoint range",
                             "one-step rate bounds", "abort bound",
                             "conditional stochastic dominance",
                             "random-walk exponential moment"]}, indent=2))
