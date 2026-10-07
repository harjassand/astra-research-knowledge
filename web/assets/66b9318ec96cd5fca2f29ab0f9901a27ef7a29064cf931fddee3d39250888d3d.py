"""Exact finite checks for the 271-to-ROUND stability transfer obstruction.

The universal argument is in reasoning_methods.md. No numerical root finder,
optimization solver, or external package is used here.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path


def rank(rows):
    rows = [[F(x) for x in row] for row in rows]
    rr = 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(rr, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rr], rows[pivot] = rows[pivot], rows[rr]
        v = rows[rr][col]
        rows[rr] = [x / v for x in rows[rr]]
        for i in range(len(rows)):
            if i != rr:
                c = rows[i][col]
                rows[i] = [a - c * b for a, b in zip(rows[i], rows[rr])]
        rr += 1
        if rr == len(rows):
            break
    return rr


def solve(matrix, rhs):
    rows = [[F(x) for x in row] + [F(b)] for row, b in zip(matrix, rhs)]
    n = len(matrix)
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        v = rows[col][col]
        rows[col] = [x / v for x in rows[col]]
        for i in range(n):
            if i != col:
                c = rows[i][col]
                rows[i] = [a - c * b for a, b in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


class Gaussian:
    """Exact Q(i), enough for every isolated two-monomial root."""

    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(self, other):
        if not isinstance(other, Gaussian):
            other = Gaussian(other)
        return Gaussian(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __mul__(self, other):
        if not isinstance(other, Gaussian):
            other = Gaussian(other)
        return Gaussian(self.a * other.a - self.b * other.b,
                        self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def is_zero(self):
        return not self.a and not self.b


original = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
lifted = [v + tuple(1 - x for x in v) for v in original]
weights = solve([[1] * 4] + [[v[j] for v in original] for j in range(3)],
                [1, F(1, 2), F(1, 2), F(1, 2)])
assert weights == [F(1, 4)] * 4
assert rank([[1] + list(v) for v in original]) == 4
assert rank([[1] + list(v) for v in lifted]) == 4
assert {sum(a != b for a, b in zip(v, w))
        for v, w in combinations(original, 2)} == {2}
assert {sum(a != b for a, b in zip(v, w))
        for v, w in combinations(lifted, 2)} == {4}
assert {sum(v) for v in lifted} == {3}


def expectation(vertices, fn):
    return sum(p * fn(v) for p, v in zip(weights, vertices))


pair_covariances = []
for i, j in combinations(range(3), 2):
    covariance = expectation(original, lambda v: v[i] * v[j]) - F(1, 4)
    assert covariance == 0
    pair_covariances.append(str(covariance))
or_mean = expectation(original, lambda v: int(v[1] or v[2]))
or_covariance = expectation(original, lambda v: v[0] * int(v[1] or v[2])) - F(1, 2) * or_mean
assert or_covariance == F(1, 8)

presence = (1, 2, 3)  # x_2, x_3, 1-x_1 in zero-based lifted indexing.
joint = expectation(lifted, lambda v: int(all(v[i] for i in presence)))
product = F(1)
for i in presence:
    product *= expectation(lifted, lambda v: v[i])
assert joint == F(1, 4) and product == F(1, 8)
assert {max(abs(F(x) - F(1, 2)) for x in v) for v in lifted} == {F(1, 2)}

# A four-atom control remains within ROUND's support bound on every product:
# sample one lifted vertex and repeat it, rather than using 4^r atoms.
product_controls = []
for blocks in (1, 2, 5):
    control = [v * blocks for v in lifted]
    assert len(control) == 4 <= 3 * blocks + 1
    assert all(expectation(control, lambda v, j=j: v[j]) == F(1, 2)
               for j in range(6 * blocks))
    assert {sum(v) for v in control} == {3 * blocks}
    assert {max(abs(F(x) - F(1, 2)) for x in v) for v in control} == {F(1, 2)}
    product_controls.append({'blocks': blocks, 'atoms': len(control),
                             'mean': 'all 1/2', 'discrepancy': '1/2'})

# In the original law, diagonal specialization uses z^2=-1/3 exactly.
assert weights[0] + sum(weights[1:]) * F(-1, 3) == 0

# Universal two-atom obstruction for the lifted support: each pair shares
# one coordinate; setting the opposite pair's shared coordinate to zero
# eliminates precisely those two other atoms. Give the two exclusive pairs
# values (1+i,q(1+i)) and (-1+i,p(-1+i)), respectively. The two weighted
# monomials cancel for every positive p,q. We check all six support patterns
# and several rational p,q; the p,q identity is proved symbolically in notes.
isolations = []
for a, b in combinations(range(4), 2):
    others = [j for j in range(4) if j not in (a, b)]
    supports = [{i for i, bit in enumerate(v) if bit} for v in lifted]
    common = supports[a] & supports[b]
    killed = supports[others[0]] & supports[others[1]]
    assert len(common) == len(killed) == 1
    kill = next(iter(killed))
    assert kill not in supports[a] | supports[b]
    exclusive_a = sorted(supports[a] - common)
    exclusive_b = sorted(supports[b] - common)
    assert len(exclusive_a) == len(exclusive_b) == 2
    for p, q in [(F(1, 7), F(3, 5)), (F(1, 4), F(1, 4)), (F(17, 19), F(2, 31))]:
        values = [Gaussian(0, 1) for _ in range(6)]
        values[kill] = Gaussian(0)
        values[exclusive_a[0]] = Gaussian(1, 1)
        values[exclusive_a[1]] = Gaussian(q, q)
        values[exclusive_b[0]] = Gaussian(-1, 1)
        values[exclusive_b[1]] = Gaussian(-p, p)
        assert all(z.b > 0 for i, z in enumerate(values) if i != kill)
        atom_weights = [F(0)] * 4
        atom_weights[a], atom_weights[b] = p, q
        # Arbitrary positive masses on the killed atoms have no effect.
        atom_weights[others[0]], atom_weights[others[1]] = F(5, 11), F(7, 13)
        value = Gaussian()
        for atom_weight, support in zip(atom_weights, supports):
            term = Gaussian(atom_weight)
            for i in support:
                term *= values[i]
            value += term
        assert value.is_zero()
    isolations.append({'atoms': [a, b], 'kill_coordinate': kill + 1})

result = {
    'status': 'PASS exact finite discriminator; universal proof is separate',
    'original_vertices': original,
    'lifted_vertices': lifted,
    'unique_exact_mean_weights': list(map(str, weights)),
    'original_edge_support': 2,
    'lifted_edge_support': 4,
    'lifted_atom_cardinality': 3,
    'discrepancy_for_identity_features': '1/2',
    'original_pair_covariances': pair_covariances,
    'original_coordinate_vs_OR_covariance': str(or_covariance),
    'lifted_joint_presence_probability': str(joint),
    'lifted_product_of_presence_probabilities': str(product),
    'four_atom_product_controls': product_controls,
    'original_diagonal_root_relation': 'z=i/sqrt(3); G(z,z,z)=0 exactly',
    'lifted_pair_isolations': isolations,
    'exact_two_atom_root_checks': 18,
    'stable_lifted_law_classification': 'only point masses, by closure and two-atom root proof',
    'stable_lifted_minimum_marginal_Linfty_error': '1/2',
    'stable_lifted_minimum_TV_from_exact_mean_law': '3/4',
    'scope': 'finite support verification; not a headline release proof or novelty certificate'
}
dest = Path(__file__).with_suffix('.json')
dest.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
