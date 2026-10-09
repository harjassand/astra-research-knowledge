#!/usr/bin/env python3
"""Exact-frequency TEST DOUBLE checks; generates no conditional samples."""
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path
import json
from verify_reduction import graph_from_mask, pm_count, remove_pair
from oracle_reduction import count_via_conditional_sampler, BudgetExceeded


def exact_frequency_test_double(B, eta, size):
    n = len(B)-2
    A = tuple(tuple(int(B[i][j]>0) for j in range(n)) for i in range(n))
    u = next(i for i in range(n) if B[i][n])
    v = next(i for i in range(n) if B[i][n+1])
    p = F(pm_count(remove_pair(A,u,v)),pm_count(A))
    R = B[u][n]**2/F(1,4*n)
    q = R**2*p**2/(1+R**2*p**2)
    return round(size*q)


def run():
    records = []
    for n in (2,4,6,8):
        A = graph_from_mask(n,2**(n*(n-1)//2)-1)
        z,stats = count_via_conditional_sampler(
            A, exact_frequency_test_double, lambda G:pm_count(G)>0,
            F(1,10),F(1,100))
        assert abs(z-Decimal(pm_count(A))) < Decimal('0.00001')
        records.append({'n':n,'answer':str(z),'truth':pm_count(A),
                        'schedule_only':stats})
    try:
        count_via_conditional_sampler(A,exact_frequency_test_double,
                                     lambda G:pm_count(G)>0,
                                     F(1,10),F(1,100),max_samples=1)
        raise AssertionError('Budget guard failed')
    except BudgetExceeded:
        pass
    zero = graph_from_mask(4,0)
    z,stats = count_via_conditional_sampler(zero,exact_frequency_test_double,
                                           lambda G:pm_count(G)>0,
                                           F(1,10),F(1,100))
    assert z == 0 and stats['sample_calls'] == 0
    payload = {
        'status':'PASS',
        'scope':'Exact-frequency TEST DOUBLE; no conditional samples generated. '
                'Tests control flow, zero/existence callback, telescope, integer '
                'budget and rounding only. Exponential PM counters used only '
                'in test double.',
        'cases':records,
    }
    Path(__file__).with_name('ORACLE_CONTROL_CHECKS.json').write_text(
        json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))


if __name__ == '__main__':
    run()
