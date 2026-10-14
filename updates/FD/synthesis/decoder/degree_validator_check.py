"""Independent exact finite check of the later degree-promised model validator.

The underlying proof is producer work in persistent_wave/p_s01c_witness_compiler/
promise_recognition/PROOF.txt section 8, not a new discovery of this audit.
"""
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def anf_degree(values, n):
    coeff = list(values)
    for i in range(n):
        for x in range(1 << n):
            if x >> i & 1:
                coeff[x] ^= coeff[x ^ (1 << i)]
    return max((x.bit_count() for x, c in enumerate(coeff) if c), default=0)


def rejection(order, h, n):
    score = Fraction(0)
    for i in range(h):
        size = 1 << (n - i - 1)
        inversions = 0
        for p in range(1 << i):
            base = p << (n - i)
            for x in range(base, base + size):
                for y in range(base + size, base + 2 * size):
                    inversions += order[x] > order[y]
        score += Fraction(inversions, h * (1 << i) * size * size)
    return score


def main():
    n, d = 3, 2
    minimum = {h: Fraction(1) for h in range(1, n + 1)}
    wrong = {h: 0 for h in range(1, n + 1)}
    cases = 0
    for order in permutations(range(1 << n)):
        # Every permutation coordinate on F2^3 is balanced and hence degree<=2.
        assert all(anf_degree([(rank >> j) & 1 for rank in order], n) <= d
                   for j in range(n))
        for h in range(1, n + 1):
            mismatch = any((rank >> (n - h)) != (x >> (n - h))
                           for x, rank in enumerate(order))
            rejection_probability = rejection(order, h, n)
            if mismatch:
                wrong[h] += 1
                assert rejection_probability >= Fraction(1, h * 4 ** d)
                minimum[h] = min(minimum[h], rejection_probability)
            else:
                assert rejection_probability == 0
        cases += 1
    result = dict(n=n, d=d, permutation_count=cases,
                  wrong_prefix_counts=wrong,
                  minimum_wrong_rejection={h: str(v) for h, v in minimum.items()},
                  theorem_bound={h: str(Fraction(1, h * 4 ** d)) for h in minimum},
                  exact_bound_attained=all(minimum[h] == Fraction(1, h * 4 ** d)
                                           for h in minimum),
                  status='PASS',
                  scope='Exact finite population; degree promise remains supplied')
    (HERE / 'degree_validator_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
