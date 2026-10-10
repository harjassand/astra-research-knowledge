"""Exact finite witness: (n-1)-wise independence does not fool parity."""
from fractions import Fraction
from itertools import product, combinations

n = 3
seeds = list(product((0, 1), repeat=n - 1))
outputs = [seed + (sum(seed) % 2,) for seed in seeds]
assert len(set(outputs)) == 2 ** (n - 1)
assert all(sum(x) % 2 == 0 for x in outputs)

pair_marginals = {}
for positions in combinations(range(n), 2):
    counts = {bits: 0 for bits in product((0, 1), repeat=2)}
    for x in outputs:
        counts[tuple(x[i] for i in positions)] += 1
    pair_marginals[positions] = {bits: Fraction(c, len(outputs)) for bits, c in counts.items()}
    assert set(pair_marginals[positions].values()) == {Fraction(1, 4)}

uniform_parity_one = Fraction(1, 2)
generator_parity_one = Fraction(0)
parity_gap = uniform_parity_one - generator_parity_one
support_gap = Fraction(1) - Fraction(len(set(outputs)), 2**n)

print("outputs:", sorted("".join(map(str, x)) for x in outputs))
print("every two-coordinate marginal:", pair_marginals)
print("parity-one probabilities: generator=", generator_parity_one, "uniform=", uniform_parity_one)
print("parity distinguisher gap:", parity_gap)
print("support-membership gap:", support_gap)
