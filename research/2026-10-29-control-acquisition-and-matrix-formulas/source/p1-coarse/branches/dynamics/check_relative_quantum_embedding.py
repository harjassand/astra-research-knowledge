"""Exact CPTP coherence embedding checks for the root relative-defect example.

The root owns the main 3D fixture and compiler. This checks the independently
constructed four-level quantum realization and fixed scalar measurement.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_block_geometry import eye, mul, outer, scale, trace, transpose


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def matvec(a, x):
    return tuple(sum((v * w for v, w in zip(row, x)), F(0)) for row in a)


def coherence(v):
    result = [[F(0) for _ in range(4)] for _ in range(4)]
    for i, x in enumerate(v, start=1):
        result[0][i] = result[i][0] = x
    return tuple(map(tuple, result))


def matrix_unit(i, j, d=4):
    return tuple(tuple(F(r == i and c == j) for c in range(d))
                 for r in range(d))


def make_channel(e, sign, gamma):
    delta = e * e
    eta = e ** 10
    u = (sign * delta, F(1), sign * e)
    s = sum(x * x for x in u)
    p = scale(1 / s, outer(u, u))
    reflection = add(eye(3), scale(F(-2), p))
    unitary = tuple(
        tuple(F(i == j) if i == 0 or j == 0 else reflection[i - 1][j - 1]
              for j in range(4))
        for i in range(4))
    assert transpose(unitary) == unitary
    assert mul(unitary, unitary) == eye(4)
    restricted = scale(1 - eta, add(eye(3), scale(-(1 - gamma), p)))

    def channel(x):
        dephased = scale(F(1, 2), add(x, mul(unitary, mul(x, unitary))))
        smoothed = add(scale(gamma, x), scale(1 - gamma, dephased))
        depolarized = scale(trace(x) / 4, eye(4))
        return add(scale(1 - eta, smoothed), scale(eta, depolarized))

    assert channel(eye(4)) == eye(4)
    for i, j in product(range(4), repeat=2):
        x = matrix_unit(i, j)
        assert trace(channel(x)) == trace(x)
    for k in range(3):
        v = tuple(F(i == k) for i in range(3))
        assert channel(coherence(v)) == coherence(matvec(restricted, v))
    return channel, restricted


def check_case(e, gamma):
    b = (F(1), F(0), F(0))
    rho = scale(F(1, 4), add(eye(4), coherence(b)))
    assert trace(rho) == 1
    channels = []
    matrices = []
    for sign in (1, -1):
        channel, restricted = make_channel(e, sign, gamma)
        channels.append(channel)
        matrices.append(restricted)
    words_checked = 0
    greatest_centering_identity_error = F(0)
    for length in range(6):
        for word in product(range(2), repeat=length):
            state = rho
            vector = b
            for i in word:
                state = channels[i](state)
                vector = matvec(matrices[i], vector)
            probability = trace(mul(rho, state))
            assert trace(state) == 1
            assert 0 <= probability <= 1
            error = 8 * probability - 2 - vector[0]
            assert error == 0
            greatest_centering_identity_error = max(
                greatest_centering_identity_error, abs(error))
            words_checked += 1
    return {
        "epsilon": str(e),
        "eta": str(e ** 10),
        "gamma": str(gamma),
        "words_checked": words_checked,
        "coherence_basis_actions_checked": 6,
        "matrix_unit_trace_checks": 32,
        "identity_preservation_checks": 2,
        "centering_identity_error_exact": str(
            greatest_centering_identity_error),
        "all_assertions_exact": True,
    }


def main():
    cases = []
    for e in (F(1, 2), F(1, 3), F(1, 5)):
        for gamma in (F(0), e ** 10):
            cases.append(check_case(e, gamma))
    result = {
        "purpose": "Exact quantum embedding of the relative-defect obstruction",
        "complete_positivity_warrant": (
            "Each primitive is a convex mixture of identity, conjugation by "
            "an exact Hermitian unitary, and complete depolarization."
        ),
        "preparation_receiver_eigenvalues": ["1/2", "1/4", "1/4", "0"],
        "scalar_relation": "f(word) = 8 p(word) - 2",
        "cases": cases,
        "total_words_checked": sum(c["words_checked"] for c in cases),
        "total_coherence_actions_checked": sum(
            c["coherence_basis_actions_checked"] for c in cases),
        "total_matrix_unit_trace_checks": sum(
            c["matrix_unit_trace_checks"] for c in cases),
        "all_checks_passed": True,
    }
    destination = Path(__file__).with_name(
        "RELATIVE_QUANTUM_EMBEDDING_RESULTS.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "all_checks_passed": True,
        "words_checked": result["total_words_checked"],
        "coherence_actions_checked": result["total_coherence_actions_checked"],
        "matrix_unit_trace_checks": result["total_matrix_unit_trace_checks"],
        "output": str(destination),
    }, indent=2))


if __name__ == "__main__":
    main()
