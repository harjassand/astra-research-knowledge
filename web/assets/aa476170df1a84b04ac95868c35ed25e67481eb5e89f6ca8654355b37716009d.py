"""Exact finite diagnostics for the independently derived block proof.

These checks verify state arithmetic and selected rational inequalities; they do
not certify the infinite probability/holding-time argument or endotacticity.
"""
from fractions import Fraction as F
from math import isqrt
import json

V = ((2, 0), (2, 1), (1, 2), (-2, -3))
GOOD = (1, 2, 3)
STALL = (1, 2, 2, 3, 2, 3, 2, 3)


def ff(n, m):
    out = 1
    for j in range(m):
        out *= max(n-j, 0)
    return out


def rates(x, b, ks):
    k0, k1, k2, k3 = ks
    return (k0, k1*ff(x, 2), k2*ff(x, 4)*b,
            k3*ff(x, 5)*ff(b, 3))


def word(a, sequence, ks):
    state = (a, 0)
    states = [state]
    probability = F(1)
    for reaction in sequence:
        x, b = state
        rs = rates(x, b, ks)
        assert rs[reaction] > 0
        probability *= rs[reaction]/sum(rs)
        dx, db = V[reaction]
        state = (x+dx, b+db)
        states.append(state)
        assert state[0] >= 0 and state[1] >= 0
    assert all(b > 0 for x, b in states[1:-1])
    return state, probability, states


def ceil(q):
    return -(-q.numerator//q.denominator)


def ceil_sqrt(q):
    n = isqrt(q.numerator//q.denominator)
    return n if F(n*n) == q else n+1


parameter_sets = [
    tuple(map(F, (1, 1, 1, 1))),
    (F(10**6), F(1), F(1, 10**6), F(1, 10**3)),
    (F(1), F(10**6), F(1, 10**6), F(10**6)),
    (F(1, 10**6), F(1, 10**3), F(10**6), F(1)),
]
records = []
for ks in parameter_sets:
    k0, k1, k2, k3 = ks
    cb = 2*k0/k1
    cl = (16*k0+4*k1)/k2
    cr = k2/k3
    ch = (16*k0+4*k1)/(3*k3)
    m = max(F(1), cb, cl, cr, ch)
    d_bound = 3*m+8*m*m
    threshold = max(8, ceil(8*m), 2*ceil_sqrt(d_bound))
    levels = sorted(set([8, 16, 64, 1024, threshold, threshold+1,
                         2*threshold+3]))
    for a in levels:
        good_end, q, good_states = word(a, GOOD, ks)
        stall_end, s, stall_states = word(a, STALL, ks)
        assert good_end == (a+1, 0)
        assert stall_end == (a, 0)
        d = 1-q-s
        assert d >= 0
        assert q >= 1-m/a-3*m/(a*a)
        assert s <= m/a
        assert d <= d_bound/(a*a)
        for x, b in good_states[:-1] + stall_states[:-1]:
            rs = rates(x, b, ks)
            assert sum(rs) >= k1*a*(a-1)
            if b == 0:
                assert (1-rs[1]/sum(rs)) <= m/(a*a)
            elif b in (1, 2):
                assert (1-rs[2]/sum(rs)) <= m/(a*a)
            elif b >= 3:
                assert rs[2]/sum(rs) <= m/a
                assert (rs[0]+rs[1])/sum(rs) <= m/(a*a*a)
        if a >= threshold:
            assert q >= F(1, 2)
            assert s <= F(1, 8)
            assert 2*d_bound/(a*a) <= F(1, 2)
            h = q/(q+d)
            assert 1-h <= 2*d_bound/(a*a)
        records.append({"k": list(map(str, ks)), "a": a,
                        "q": str(q), "s": str(s), "d": str(d),
                        "at_or_above_threshold": a >= threshold})

print(json.dumps({"status": "PASS", "arithmetic": "exact rational",
                  "parameter_sets": len(parameter_sets),
                  "levels_checked": len(records),
                  "checks": ["legal words and endpoints", "one-step bounds",
                             "q,s,d bounds", "threshold", "rate lower bound"]},
                 indent=2))
