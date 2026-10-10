#!/usr/bin/env python3
"""Small exact checks for the frozen H19 valuation-isolation claim."""
from itertools import combinations, product


def v2(z: int) -> int:
    if z == 0:
        raise ValueError("v2(0) is infinite")
    return (abs(z) & -abs(z)).bit_length() - 1


def cost(alpha, b, weights):
    return b + sum(a * w for a, w in zip(alpha, weights))


def evaluate(terms, weights):
    return sum(c * (1 << sum(a * w for a, w in zip(alpha, weights)))
               for alpha, c in terms)


# Exhaustively check the isolation bound for all supports of size <=3 in [0,2]^2,
# all coefficient valuations b in {0,1,2,3}, and all weights in [0,8]^2.
# Here D=d_1+d_2=4, so the claimed upper bound on tie probability is 4/9.
grid = list(product(range(3), repeat=2))
W = 8
D = 4
weight_vectors = list(product(range(W + 1), repeat=2))
scenarios = 0
for size in range(1, 4):
    for support in combinations(grid, size):
        for offsets in product(range(4), repeat=size):
            tie_count = 0
            for weights in weight_vectors:
                costs = [cost(alpha, b, weights)
                         for alpha, b in zip(support, offsets)]
                if costs.count(min(costs)) > 1:
                    tie_count += 1
                else:
                    # Give each coefficient the requested 2-adic valuation and
                    # an odd part; a unique adjusted minimum must survive.
                    terms = [(alpha, (1 if i % 2 == 0 else -3) * (1 << b))
                             for i, (alpha, b) in enumerate(zip(support, offsets))]
                    value = evaluate(terms, weights)
                    assert value != 0
                    assert v2(value) == min(costs)
            assert tie_count * (W + 1) <= D * len(weight_vectors), (
                support, offsets, tie_count, len(weight_vectors), D, W
            )
            scenarios += 1

# Exact falsifiers for the tempting unadjusted variants.
assert evaluate([((1,), 1), ((0,), -1)], (0,)) == 0  # tie in exponent weight
assert evaluate([((1,), 2), ((0,), -4)], (1,)) == 0  # coefficient valuation offsets tie

# Cost witness: an O(s)-gate repeated-squaring circuit can have degree 2^s.
s = 12
D_circuit = 1 << s
w = 1
large_value_bits = ((1 << (w * D_circuit)) + 1).bit_length()
assert large_value_bits == w * D_circuit + 1

print(f"exhaustive scenarios checked: {scenarios}")
print(f"isolation bound checked: tie probability <= {D}/{W + 1}")
print("unique adjusted minimum implies exact nonzero evaluation and matching v2")
print("two unadjusted variants have exact zero counterexamples")
print(f"degree-2^{s} circuit example: evaluation bit length = {large_value_bits}")
