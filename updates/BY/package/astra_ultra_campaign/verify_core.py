#!/usr/bin/env python3
"""Exact finite diagnostics; these do not certify the universal EPnI proof."""
from fractions import Fraction as F
import json


def rplus(r, v):
    assert v != 0
    t = ((r + 1) / r) ** v
    return v * t / (t - 1)


def rminus(r, v):
    assert v != 0
    t = ((r + 1) / r) ** v
    return v / (t - 1)


def fdown(r, v):
    assert v not in (0, 1)
    return (rminus(r, v) - r * v) / (1 - v)


def stirling(n, j):
    if n == 0:
        return int(j == 0)
    if j <= 0 or j > n:
        return 0
    return j * stirling(n - 1, j) + stirling(n - 1, j - 1)


def falling(n, j):
    v = 1
    for i in range(j):
        v *= n - i
    return v


def main():
    r = F(1)
    src_rp = rplus(r, 10) + rplus(r, -10)
    src_rm = rminus(r, 10) + rminus(r, -10)
    assert src_rp >= 2 * rplus(r, -4)
    assert src_rm >= 2 * rminus(r, -4)
    src_f = fdown(r, 10) + fdown(r, -10)
    dst_f = 2 * fdown(r, -4)
    assert src_f == F(296650, 101277)
    assert dst_f == F(248, 75)
    assert src_f < dst_f
    # Constant weights also agree: source two coordinates vs target weight 2.
    assert 2 * r == 2 and 2 * (r + 1) == 4

    ri, wa, wb = F(1, 10), F(7, 4), F(3, 4)
    assert (wa + wb) * rplus(ri, -2) <= rplus(r, -5)
    assert (wa + wb) * rminus(ri, -2) <= rminus(r, -5)
    assert wa * ri + wb * (ri + 1) == r
    assert wa * (ri + 1) + wb * ri == r + 1
    correct = wa * fdown(ri, -2) + wb * fdown(ri, 2)
    wrong = (wa + wb) * fdown(ri, -2)
    source = fdown(r, -5)
    assert (correct, source, wrong) == (F(103, 72), F(105, 62), F(133, 72))
    assert correct <= source < wrong

    for k in range(9):
        for m in range(41):
            assert (m + 1) ** k == sum(stirling(k + 1, j + 1) * falling(m, j)
                                      for j in range(k + 1))
    for gain in (F(3, 2), F(2), F(3), F(10)):
        for variance in (F(1, 10), F(1), F(5)):
            marginal_a = (gain - 1) * variance
            marginal_b = gain * variance
            output = gain - 1
            invalid_bound = gain * marginal_a + (gain - 1) * (marginal_b + 1)
            assert invalid_bound - output == 2 * gain * (gain - 1) * variance > 0

    print(json.dumps({
        'status': 'PASS',
        'arithmetic': 'exact Python fractions and integers',
        'invariance_counterexample': {'source': str(src_f), 'target': str(dst_f)},
        'reversal_counterexample': {'correct': str(correct), 'source': str(source),
                                   'wrong_all_down': str(wrong)},
        'stirling_number_identity_cases': 9 * 41,
        'correlated_coherent_scope_checks': 12,
        'scope': 'Finite diagnostics and exact counterexamples; not a proof of amplifier EPnI'
    }, indent=2))


if __name__ == '__main__':
    main()
