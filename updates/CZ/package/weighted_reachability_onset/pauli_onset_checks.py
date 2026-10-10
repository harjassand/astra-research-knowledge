"""Exact finite checks for decisive_applications.md; no external packages."""
from fractions import Fraction as F
import json
from itertools import product
from math import prod


def syndrome(columns, subset):
    result = 0
    for j, h in enumerate(columns):
        if subset >> j & 1:
            result ^= h
    return result


def syndrome_data(columns, rows):
    length = len(columns)
    minimum = [length + 1] * (1 << rows)
    multiplicity = [0] * (1 << rows)
    for subset in range(1 << length):
        g, weight = syndrome(columns, subset), subset.bit_count()
        if weight < minimum[g]:
            minimum[g], multiplicity[g] = weight, 1
        elif weight == minimum[g]:
            multiplicity[g] += 1
    assert max(minimum) <= length
    return minimum, multiplicity


def probability(columns, rows, q):
    length = len(columns)
    result = [F(0)] * (1 << rows)
    for subset in range(1 << length):
        weight = subset.bit_count()
        result[syndrome(columns, subset)] += q ** weight * (1-q) ** (length-weight)
    assert sum(result) == 1
    return result


def harmonic_deficit(probabilities):
    labels = len(probabilities)
    return F(labels ** 2, 1) / sum(1/p for p in probabilities)


# H=[e1,e2,e3,e1+e2+e3] defines the binary repetition code of length 4.
H = [1, 2, 4, 7]
ell, counts = syndrome_data(H, 3)
radius = max(ell)
assert radius == 2
deep = [g for g in range(8) if ell[g] == radius]
assert len(deep) == 3 and all(counts[g] == 2 for g in deep)

# H direct-sum H gives X-type and Z-type jumps on three qubits.
A = H + [h << 3 for h in H]
ell_A, counts_A = syndrome_data(A, 6)
assert max(ell_A) == 2 * radius == 4
deep_A = [g for g in range(64) if ell_A[g] == 4]
leading = F(8**4, 1) / sum(F(1, counts_A[g]) for g in deep_A)
assert len(deep_A) == 9 and leading == F(16384, 9)

# Pauli eigenvalues of L are -2 times the count of anticommuting jumps.
def symplectic_pair(a, b, n):
    mask = (1 << n) - 1
    ax, az = a & mask, a >> n
    bx, bz = b & mask, b >> n
    return ((ax & bz).bit_count() + (az & bx).bit_count()) % 2

gap = min(2 * sum(symplectic_pair(g, h, 3) for h in A) for g in range(1, 64))
assert gap == 4

# Exact factorization beta(H direct-sum H)=beta(H)^2 at rational parity q.
for q in (F(1, 10), F(1, 4), F(2, 5)):
    p = probability(H, 3, q)
    p_A = probability(A, 6, q)
    assert p_A == [p[g & 7] * p[g >> 3] for g in range(64)]
    assert harmonic_deficit(p_A) == harmonic_deficit(p) ** 2

# Exact #SAT reduction, including both endpoint counts.
sat_checks = 0
for variables in range(1, 9):
    for satisfying in range(2**variables + 1):
        q = F(satisfying, 2**variables)
        p = [(2-q)/4, F(1,4), F(1,4), q/4]
        beta = F(0) if not q else harmonic_deficit(p)
        r = q * (2-q)
        assert beta == 2*r/(1+r)
        assert (1-q)**2 == 1-beta/(2-beta)
        sat_checks += 1

print(json.dumps({"syndrome_radius": radius, "pauli_onset_exponent": max(ell_A),
       "leading_beta_coefficient": str(leading), "liouvillian_gap": gap,
       "exact_sat_count_checks": sat_checks, "probability_factorizations": 3,
       "status": "all exact finite checks passed"}, indent=2))
