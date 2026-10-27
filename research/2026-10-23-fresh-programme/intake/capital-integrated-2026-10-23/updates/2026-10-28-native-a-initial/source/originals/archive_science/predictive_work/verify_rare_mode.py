"""Exact rational full-law checks for RARE_MODE_CONFIDENCE_THEOREM.txt.

No inference of TV from empirical moments. No private parameter enters the
zero-count learner. Python 3 standard library only.
"""
from fractions import Fraction as F
from math import comb, expm1, log
from pathlib import Path
import random


def coupling(q1, q2, e, delta):
    g = 1-delta
    lo, hi = sorted((q1, q2))
    num = g*(hi-lo) + g*g*lo*e
    u0 = num / (delta*(1+g*lo)+num)
    u1 = g*(e+(1-e)*u0)
    return u0, u1


def binomial_tv(n, p, p2):
    return sum(F(comb(n, k)) * abs(p**k*(1-p)**(n-k)
                - p2**k*(1-p2)**(n-k)) for k in range(n+1))/2


def exact_stopped_tv_interval(q, p, p2, delta, terms=40):
    g = 1-delta
    r = g*g*q/(delta+g*q)
    total = sum((1-r)*r**k*binomial_tv(k, p, p2)
                for k in range(terms+1))
    return total, total+r**(terms+1), r


def zero_count_learner(trials, successes, alpha, delta):
    # Function receives only legal counts, confidence, and a chosen clock.
    if successes:
        return None
    q_upper = -expm1(log(alpha)/trials)
    gamma = 1-delta
    bound = gamma*q_upper/(delta+gamma*q_upper)
    return q_upper, bound, gamma


def run():
    output = []
    grid = [F(0), F(1,100), F(1,10), F(1,2), F(1)]
    cases = 0
    for q1 in grid:
        for q2 in grid:
            for e in grid:
                for delta in [F(1,10), F(1,3), F(4,5)]:
                    g = 1-delta
                    lo, hi = sorted((q1,q2))
                    u0,u1 = coupling(q1,q2,e,delta)
                    assert u0 == g*(hi-lo+lo*u1+(1-hi)*u0)
                    assert u1 == g*(e+(1-e)*u0)
                    assert 0 <= u0 <= 1 and 0 <= u1 <= 1
                    assert u0 >= g*u0 and u1 >= g*u1
                    cases += 1
    output.append(f'Exact rational Bellman/positivity checks: {cases} PASS')

    # Verify rectangle extrema by exhaustive rational interior pairs.
    for low,high in [(F(0),F(1,10)),(F(1,100),F(1,2))]:
        for emax in [F(1,10),F(1,2),F(1)]:
            top,_ = coupling(low,high,emax,F(1,10))
            points = [low+(high-low)*F(k,8) for k in range(9)]
            for q1 in points:
                for q2 in points:
                    for e in [F(0),emax/2,emax]:
                        val,_ = coupling(q1,q2,e,F(1,10))
                        assert val <= top
    output.append('Exact rational confidence-rectangle extremum checks: PASS')

    for q,delta,p,p2 in [
        (F(1,1000),F(1,20),F(1,4),F(3,4)),
        (F(1,100),F(1,10),F(2,5),F(3,5)),
        (F(1,10),F(1,5),F(0),F(1)),
    ]:
        low,high,r = exact_stopped_tv_interval(q,p,p2,delta)
        bound,_ = coupling(q,q,abs(p-p2),delta)
        assert low <= bound
        if p == 0 and p2 == 1:
            assert low <= bound <= high
            assert bound == r
        output.append('Full-law exact-series check: '
          f'q={float(q):.6g}, delta={float(delta):.6g}, '
          f'theta=({float(p):.6g},{float(p2):.6g}), '
          f'TV=[{float(low):.14g},{float(high):.14g}], '
          f'analytic tail<={float(high-low):.3g}, '
          f'coupling bound={float(bound):.14g}')

    # At a rare q, the old core is ill conditioned but the observable norm
    # remains bounded. Check all rational cube-grid vectors exactly.
    for i in range(-10,11):
        for j in range(-10,11):
            x0,x1 = F(i,10),F(j,10)
            norm = abs(x0-x1)+abs(x1)
            inf = max(abs(x0),abs(x1))
            assert inf <= norm <= 3*inf
    output.append('Observable norm cube checks, no q dependence: PASS')

    # Separate synthetic plant block. Only its resulting counts are passed
    # to the learner; q and theta are not legal learner inputs.
    plant_q = 1e-6
    trials = 5000
    rng = random.Random(20261027)
    observed_successes = sum(rng.random()<plant_q for _ in range(trials))
    result = zero_count_learner(trials,observed_successes,.01,.1)
    output.append(f'Synthetic paid acquisition: {trials} resets and triggers; '
                  f'observed successes={observed_successes}')
    assert result is not None
    upper,bound0,bound1 = result
    assert bound0 < .01 and bound1 == .9
    output.append(f'Count-only zero-success return: q_upper={upper:.14g}, '
                  f'all-policy actual-start TV<={bound0:.14g}, '
                  f'normalized-state-1 bound={bound1:.14g}')
    output.append('All results are theoretical model checks with synthetic '
                  'counts, not physical measurements or a general CP learner.')
    text='\n'.join(output)+'\n'
    print(text,end='')
    Path(__file__).with_name('CHECK_RESULTS.txt').write_text(text)


if __name__ == '__main__':
    run()
