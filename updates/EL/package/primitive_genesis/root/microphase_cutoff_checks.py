"""Independent checks of the integration cell's one-binomial cutoff.

Exact assertions concern integer stage inversion. Sampling is floating point.
"""
from itertools import product
import json
from pathlib import Path
import random
from sparse_clock import sparse_clock
import math


def invert_microphases(completed, markers):
    answer = completed
    for index, extra in markers:
        if index >= answer:
            break
        answer = max(index, answer - extra)
    return answer


def microphase_cutoff(rng, total, k, markers, remaining):
    if remaining >= total:
        return k
    shape = k + sum(g for _, g in markers)
    completed = rng.binomialvariate(shape - 1, remaining / total)
    return invert_microphases(completed, markers)


def main():
    assertions = 0
    fixtures = 0
    for k in range(1, 7):
        for extras in product(range(4), repeat=k):
            fixtures += 1
            markers = [(i, g) for i, g in enumerate(extras) if g]
            endpoints = [0]
            for g in extras:
                endpoints.append(endpoints[-1] + 1 + g)
            for completed in range(endpoints[-1]):
                reference = max(j for j, endpoint in enumerate(endpoints)
                                if endpoint <= completed)
                assert invert_microphases(completed, markers) == reference
                assertions += 1
    rng = random.Random(1210202607)
    n, k, horizon, trials = 70, 20, 0.003, 20000
    rate = lambda i: math.comb(n + i, 2)
    lower, upper = rate(0), rate(k-1)
    compiled, sequential = [0] * (k+1), [0] * (k+1)
    joint_compiled = joint_sequential = 0
    for _ in range(trials):
        total, markers, _, _ = sparse_clock(rng, k, rate, lower, upper)
        count = microphase_cutoff(rng, total, k, markers, horizon)
        compiled[count] += 1
        joint_compiled += count <= 7 and total <= 0.006
        clock, count = 0.0, 0
        for i in range(k):
            clock += rng.expovariate(rate(i))
            count += clock <= horizon
        sequential[count] += 1
        joint_sequential += count <= 7 and clock <= 0.006
    result = dict(status="EXACT_INVERSION_AND_FLOAT_DISTRIBUTION_DIAGNOSTICS",
                  integer_assertions=assertions,integer_fixtures=fixtures,
                  trials_per_method=trials,n=n,k=k,horizon=horizon,
                  compiled_counts=compiled,sequential_counts=sequential,
                  empirical_tv=sum(abs(a-b) for a,b in zip(compiled,sequential))/(2*trials),
                  joint_event="count<=7 and root<=0.006",
                  joint_compiled=joint_compiled/trials,
                  joint_sequential=joint_sequential/trials)
    Path(__file__).with_name('microphase_cutoff_results.json').write_text(
        json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
