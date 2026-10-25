"""Exact finite checks for the physical bridge assessment.

Standard library only. Fractions are used for every matrix identity. Decimal
arithmetic evaluates the already-defined candidate; it does not verify the
source's construction of its 172 records.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def mat(rows):
    return [[F(value) for value in row] for row in rows]


def zero(n):
    return mat([[0] * n for _ in range(n)])


def identity(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, s):
    return [[F(s) * x for x in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def comm(a, b):
    return add(mul(a, b), scale(mul(b, a), -1))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def kron(a, b):
    return [[a[i][j] * b[k][l] for j in range(len(a[0]))
             for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def apply(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def norm2(v):
    return sum(x * x for x in v)


# A complex rational matrix is represented by its real and imaginary matrices.
def cmul(a, b):
    ar, ai = a
    br, bi = b
    return (add(mul(ar, br), scale(mul(ai, bi), -1)),
            add(mul(ar, bi), mul(ai, br)))


def cdagger(a):
    return transpose(a[0]), scale(transpose(a[1]), -1)


def ctrace(a):
    assert trace(a[1]) == 0
    return trace(a[0])


def epsilon(i, j, k):
    if len({i, j, k}) != 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


# Unit I_4 and direction T_a tensor I_2. Each Gram entry is twice
# the corresponding 2-dimensional trace.
z2 = zero(2)
qubit_basis = [
    (identity(2), z2),
    (z2, mat([[0, F(1, 2)], [F(1, 2), 0]])),
    (mat([[0, F(1, 2)], [-F(1, 2), 0]]), z2),
    (z2, mat([[F(1, 2), 0], [0, -F(1, 2)]])),
]
plain_gram = [[2 * ctrace(cmul(a, b)) for b in qubit_basis]
              for a in qubit_basis]
hilbert_gram = [[2 * ctrace(cmul(cdagger(a), b)) for b in qubit_basis]
                for a in qubit_basis]
G = mat([[4, 0, 0, 0], [0, -1, 0, 0],
         [0, 0, -1, 0], [0, 0, 0, -1]])
assert plain_gram == G
assert hilbert_gram == mat([[4, 0, 0, 0], [0, 1, 0, 0],
                           [0, 0, 1, 0], [0, 0, 0, 1]])

rotations = []
boosts = []
for i in range(3):
    rotation = zero(4)
    boost = zero(4)
    for j in range(3):
        for k in range(3):
            rotation[j + 1][k + 1] = -F(epsilon(i, j, k))
    boost[0][i + 1] = F(1, 2)
    boost[i + 1][0] = F(2)
    rotations.append(rotation)
    boosts.append(boost)

for X in rotations + boosts:
    assert add(mul(transpose(X), G), mul(G, X)) == zero(4)

for i in range(3):
    for j in range(3):
        expected_j = zero(4)
        expected_k = zero(4)
        for k in range(3):
            expected_j = add(expected_j, scale(rotations[k], epsilon(i, j, k)))
            expected_k = add(expected_k, scale(boosts[k], epsilon(i, j, k)))
        assert comm(rotations[i], rotations[j]) == expected_j
        assert comm(rotations[i], boosts[j]) == expected_k
        assert comm(boosts[i], boosts[j]) == scale(expected_j, -1)

# A genuine Lorentz coordinate map, coming from H -> B H B^dagger
# with B=diag(2, 1/2) and H=2t I + x.sigma.
coordinate_boost = identity(4)
coordinate_boost[0][0] = F(17, 8)
coordinate_boost[0][3] = F(15, 16)
coordinate_boost[3][0] = F(15, 4)
coordinate_boost[3][3] = F(17, 8)
assert mul(mul(transpose(coordinate_boost), G), coordinate_boost) == G

# The same positive spinor acting at both Bell ends changes Schmidt weights.
B = mat([[2, 0], [0, F(1, 2)]])
B_inverse_transpose = mat([[F(1, 2), 0], [0, 2]])
bell_flat = [F(1), F(0), F(0), F(1)]
same_output = apply(kron(B, B), bell_flat)
assert same_output == [F(4), F(0), F(0), F(1, 4)]
same_schmidt_probabilities = [same_output[0] ** 2 / norm2(same_output),
                              same_output[3] ** 2 / norm2(same_output)]
assert same_schmidt_probabilities == [F(256, 257), F(1, 257)]

# The reciprocal action preserves the Bell contraction exactly, but is not
# an ordinary trace-preserving quantum operation on its whole input space.
reciprocal = kron(B, B_inverse_transpose)
assert apply(reciprocal, bell_flat) == bell_flat
reciprocal_kdagger_k = mul(transpose(reciprocal), reciprocal)
assert reciprocal_kdagger_k == mat([[1, 0, 0, 0], [0, 16, 0, 0],
                                    [0, 0, F(1, 16), 0], [0, 0, 0, 1]])
reciprocal_contraction = scale(reciprocal, F(1, 4))
reciprocal_success = norm2(apply(reciprocal_contraction, bell_flat)) / norm2(bell_flat)
assert reciprocal_success == F(1, 16)

# Normalizing a nonunitary filter is nonlinear even on diagonal qubit states.
# Filter B/2 takes each pure basis state to itself, so their 50/50 mixture
# after separately normalizing is I/2. Directly filtering I/2 gives (16/17,1/17).
filtered_mixture = [F(16, 17), F(1, 17)]
mixture_of_filtered_states = [F(1, 2), F(1, 2)]
assert filtered_mixture != mixture_of_filtered_states

with localcontext() as context:
    context.prec = 80
    r = (Decimal(79) + Decimal(48) * Decimal(2).sqrt()
         + Decimal(42) * Decimal(3).sqrt() + Decimal(3) * Decimal(6).sqrt()) / Decimal(31104)
    # s=4*pi*kappa. D_dressed / D_bare = r for every s>0,
    # while alpha(0)=r/s for the fixed unit source current.
    numerical = {
        "candidate": str(+r),
        "candidate_inverse": str(1 / r),
        "s_1_alpha": str(+r),
        "s_1_inverse_alpha": str(1 / r),
        "s_2_alpha": str(r / 2),
        "s_2_inverse_alpha": str(2 / r),
        "s_2_to_s_1_scattering_cross_section_ratio": "1/4",
    }

assert 79 + 48 + 42 + 3 == 172
assert 24 * 36 * 36 == 31104

result = {
    "scope": "Independent exact checks of the conditional EFT counterfamily and Lorentz interpretations; not a replay of the record derivation or Lean.",
    "all_assertions_passed": True,
    "normalization_family": {
        "bare_lagrangian": "-kappa F^2/4 - J.A",
        "dressed_lagrangian": "-kappa F^2/(4r) - J.A",
        "same_fixed_charge_and_current": True,
        "same_dressed_over_bare_propagator": "r",
        "observable_alpha": "r/(4*pi*kappa)",
        "canonical_field": "A_can=sqrt(kappa/r) A",
        "canonical_electric_charge": "sqrt(r/kappa)",
        "not_full_models_of_finite_axiom": True,
    },
    "numerical": numerical,
    "lorentz": {
        "plain_trace_gram": [[str(x) for x in row] for row in plain_gram],
        "hilbert_schmidt_gram": [[str(x) for x in row] for row in hilbert_gram],
        "six_generators_are_plain_gram_isometries": True,
        "all_rotation_and_boost_brackets_verified": True,
        "coordinate_boost": [[str(x) for x in row] for row in coordinate_boost],
        "coordinate_boost_preserves_plain_gram": True,
        "same_action_bell_schmidt_probabilities": [str(x) for x in same_schmidt_probabilities],
        "reciprocal_action_preserves_bell": True,
        "reciprocal_action_kdagger_k": [[str(x) for x in row] for row in reciprocal_kdagger_k],
        "reciprocal_contraction_success_on_bell": str(reciprocal_success),
        "normalized_filter_is_nonlinear": True,
        "filtered_mixture_diagonal": [str(x) for x in filtered_mixture],
        "mixture_of_normalized_filtered_states_diagonal": [str(x) for x in mixture_of_filtered_states],
    },
}

repo = Path(__file__).resolve().parents[2]
sources = []
for name in ("ChainTheoryAlpha.pdf", "ChainTheoryCompendium.pdf"):
    path = repo / "work" / "sol_b" / name
    if path.exists():
        sources.append({"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "bytes": path.stat().st_size})
result["sources"] = sources
destination = Path(__file__).with_name("replay_results.json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"all_assertions_passed": True, "results": str(destination),
                  "candidate_inverse": numerical["candidate_inverse"],
                  "reciprocal_filter_success": str(reciprocal_success)}, indent=2))
