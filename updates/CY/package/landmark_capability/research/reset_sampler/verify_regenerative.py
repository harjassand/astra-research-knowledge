#!/usr/bin/env python3
"""Independent exact full-state comparator on small cases only."""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import time
import certified_solver as cs
import regenerative_solver as rs


def dense_exact_stationary(model):
    states = list(product((0, 1), repeat=model.n))
    index = {x:i for i,x in enumerate(states)}
    q = [[F(0) for _ in states] for _ in states]
    for x in states:
        i = index[x]
        for coordinate in range(model.n):
            rate = model.up[coordinate] if not x[coordinate] else model.down[coordinate]
            y = list(x)
            y[coordinate] ^= 1
            q[i][index[tuple(y)]] += rate
            q[i][i] -= rate
        for channel in range(model.k):
            rate = sum(model.hazards[channel][j][x[j]] for j in range(model.n))
            q[i][i] -= rate
            for y in states:
                prob = F(1)
                for j in range(model.n):
                    p = model.reset_one[channel][j]
                    prob *= p if y[j] else 1-p
                q[i][index[y]] += rate * prob
    a = [list(row) for row in zip(*q)]
    a[0] = [F(1) for _ in states]
    inv = cs.rational_inverse(a)
    pi = [row[0] for row in inv]
    assert sum(pi) == 1 and min(pi) > 0
    assert all(sum(pi[i]*q[i][j] for i in range(len(states))) == 0 for j in range(len(states)))
    return states, pi


def main():
    three = cs.make_fixture()
    # Three channels, including deterministic reset laws, test the cofactor
    # orientation and zero-support reset behavior beyond the two-channel case.
    small = cs.ResetModel(
        up=(F(2,3),F(3,5)), down=(F(4,5),F(7,9)),
        hazards=(((F(1,7),F(2,9)),(F(1,5),F(0))),
                 ((F(0),F(1,4)),(F(2,5),F(1,11))),
                 ((F(1,9),F(0)),(F(1,13),F(2,7)))),
        reset_one=((F(0),F(1)),(F(1),F(0)),(F(1,3),F(3,4))),
        initial_one=(F(1,2),F(1,2)))
    start = time.monotonic()
    checks = []
    for model in (three,small):
        states, pi = dense_exact_stationary(model)
        masks = [cs.event_mask_for_prefix((1,)*model.n, model.n),
                 cs.event_mask_for_prefix((0,), model.n)]
        intervals, detail = rs.stationary_intervals(model,masks,F(1,1<<32))
        for mask,(lo,hi) in zip(masks,intervals):
            value=sum(p for x,p in zip(states,pi) if all(mask[i][x[i]] for i in range(model.n)))
            assert lo<=value<=hi and hi-lo<=F(1,1<<32)
            checks.append({'n':model.n,'k':model.k,'exact':cs.frac(value),
                           'lower':cs.frac(lo),'upper':cs.frac(hi),'contained':True})
    result={'status':'all_exact_comparisons_pass','checks':checks,
            'elapsed_seconds':time.monotonic()-start,
            'scope':'Dense state enumeration occurs only in this small independent comparator'}
    Path(__file__).with_name('regenerative_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
