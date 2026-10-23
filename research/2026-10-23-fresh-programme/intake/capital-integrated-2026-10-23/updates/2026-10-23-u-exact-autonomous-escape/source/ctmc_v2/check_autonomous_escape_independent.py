"""Root's independent exact verifier; never imports the construction code.

The rational polynomial check, rather than a floating matrix exponential,
establishes the common half-period on the invariant subspace.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import math

BASE = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("certificate", nargs="?", type=Path,
                    default=BASE / "interface_invention/AUTONOMOUS_ESCAPE_RATIONAL_CERTIFICATE.json")
args = parser.parse_args()
path = args.certificate.resolve()
raw = path.read_bytes()
data = json.loads(raw)
q = [[Fraction(x) for x in row] for row in data["Q"]]
u = [[Fraction(x) for x in row] for row in data["U"]]
k = [[Fraction(x) for x in row] for row in data["K"]]
a = Fraction(data["a"])
n = len(q)
assert n == data["n"] == 48
assert all(len(row) == n for row in q)
assert len(u) == n and all(len(row) == 4 for row in u)
assert len(k) == 4 and all(len(row) == 4 for row in k)
assert 0 < a < 1
assert data["T"] == "pi"

zero = Fraction(0)
assert all(sum(row, zero) == 0 for row in q)
assert all(sum((q[i][j] for i in range(n)), zero) == 0 for j in range(n))
off_diagonal = [q[i][j] for i in range(n) for j in range(n) if i != j]
assert min(off_diagonal) > 0
z = [row[0] for row in u]
assert z == [Fraction(1)] * 24 + [Fraction(-1)] * 24
assert all(sum((u[i][j] for i in range(n)), zero) == 0 for j in range(4))

# Verify the 48x4 intertwining identity directly entry by entry.
for i in range(n):
    for j in range(4):
        lhs = sum((q[i][r] * u[r][j] for r in range(n)), zero)
        rhs = sum((u[i][r] * k[r][j] for r in range(4)), zero) - a * u[i][j]
        assert lhs == rhs, (i, j)

def product(left, right):
    return [[sum((left[i][r] * right[r][j] for r in range(len(right))), zero)
             for j in range(len(right[0]))] for i in range(len(left))]

def determinant(matrix):
    rows = [row[:] for row in matrix]
    value = Fraction(1)
    for j in range(len(rows)):
        pivot = next((i for i in range(j, len(rows)) if rows[i][j]), None)
        if pivot is None:
            return zero
        if pivot != j:
            rows[j], rows[pivot] = rows[pivot], rows[j]
            value = -value
        coefficient = rows[j][j]
        value *= coefficient
        for i in range(j + 1, len(rows)):
            ratio = rows[i][j] / coefficient
            for r in range(j + 1, len(rows)):
                rows[i][r] -= ratio * rows[j][r]
    return value

gram = [[sum((u[r][i] * u[r][j] for r in range(n)), zero)
         for j in range(4)] for i in range(4)]
assert determinant(gram) > 0
k2 = product(k, k)
k4 = product(k2, k2)
assert all(k4[i][j] + 10 * k2[i][j] + (9 if i == j else 0) == 0
           for i in range(4) for j in range(4))
# Roots of x^4+10x^2+9 are distinct and equal to +/-i,+/-3i.
# The exponential at pi equals -1 at all four roots. Hence exp(pi K)=-I.
# QU=U(K-aI) then gives exp(pi Q)z=-exp(-pi a)z exactly.

vectors = [[Fraction(1), zero, zero, zero]]
for _ in range(3):
    vectors.append([sum((k[i][j] * vectors[-1][j] for j in range(4)), zero)
                    for i in range(4)])
krylov = [[vectors[j][i] for j in range(4)] for i in range(4)]
assert determinant(krylov) != 0
# A nonzero diagonal of the commutator already proves nonnormality.
commutator_diagonal = [sum((q[i][j] ** 2 - q[j][i] ** 2 for j in range(n)), zero)
                       for i in range(n)]
assert any(commutator_diagonal)

result = {
    "status": "ROOT_INDEPENDENT_EXACT_CHECK_PASSED",
    "certificate_sha256": hashlib.sha256(raw).hexdigest(),
    "dimension": n,
    "memory_states_per_bit": n // 2,
    "a_exact": str(a),
    "strict_gap_1_minus_a_exact": str(1 - a),
    "strict_positive_offdiagonals": True,
    "both_balance_identities_exact": True,
    "intertwining_exact": True,
    "K_polynomial_x4_plus_10x2_plus_9_exact": True,
    "both_alias_pairs_contribute": True,
    "nonnormal_exact": True,
    "return_identity": "exp(pi Q) z = -exp(-pi a) z",
    "population_channel": "flip probability (1+exp(-pi a))/2; uniform memory returns independently",
    "strict_comparison": "0<a<1 implies exp(-pi a)>exp(-pi); no numerical exponential needed",
    "approximate_success_gain": (math.exp(-math.pi * float(a)) - math.exp(-math.pi)) / 2,
    "scope": "exact finite classical population construction; no physical implementation, novelty or utility established",
}
suffix = "_v2" if "V2" in path.name else ""
destination = Path(__file__).with_name(f"autonomous_escape_independent{suffix}_results.json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
