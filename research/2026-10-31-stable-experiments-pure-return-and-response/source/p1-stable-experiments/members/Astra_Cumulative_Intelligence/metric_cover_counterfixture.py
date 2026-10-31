#!/usr/bin/env python3
"""Exact Gram-only comparison on two self-adjoint Markov reflections.

No third-party packages. All source responses and learner decisions use Fraction.
The hidden phase labels are private to the source simulator. Both learners access
only scalar gram(word_u, word_v), with physical cost len(u)+len(v).

This is an exact-moment diagnostic. It does not claim a finite-noise spectral
advantage; the discovered basis has condition number rho**(-2).
"""
from collections import deque
from fractions import Fraction as F
import csv
import json
from pathlib import Path


def solve(matrix, rhs):
    """Exact Gaussian elimination; small dimensions in this fixture."""
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(a)
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [x / divisor for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return [row[-1] for row in a]


class GramSource:
    """Private source: g_k(x)=sqrt(2)*cos(x-k*theta), theta=2*atan(rho)."""

    def __init__(self, rho):
        self.cosine = (1 - rho * rho) / (1 + rho * rho)
        self._cos_multiples = [F(1), self.cosine]
        self._phases = {"": 0}
        self._cache = {}
        self.queries = 0
        self.steps = 0
        self.max_pair_length = 0
        self.response_bits = 0

    def _phase(self, word):
        if word not in self._phases:
            phase = 0
            for letter in word:
                phase = -phase if letter == "a" else 1 - phase
            self._phases[word] = phase
        return self._phases[word]

    def gram(self, left, right):
        key = tuple(sorted((left, right)))
        if key in self._cache:
            return self._cache[key]
        k = abs(self._phase(left) - self._phase(right))
        while len(self._cos_multiples) <= k:
            self._cos_multiples.append(
                2 * self.cosine * self._cos_multiples[-1]
                - self._cos_multiples[-2]
            )
        value = self._cos_multiples[k]
        self._cache[key] = value
        self.queries += 1
        steps = len(left) + len(right)
        self.steps += steps
        self.max_pair_length = max(self.max_pair_length, steps)
        self.response_bits += (
            abs(value.numerator).bit_length() + value.denominator.bit_length()
        )
        return value

    def counters(self):
        return {
            "scalar_queries": self.queries,
            "primitive_word_steps": self.steps,
            "max_pair_length": self.max_pair_length,
            "total_exact_response_bits": self.response_bits,
        }


def metric_cover(gram, rho):
    centers = [""]
    transitions = {}
    cursor = 0
    threshold = F(3, 4) * rho * rho
    gram("", "")
    while cursor < len(centers):
        for letter in "ab":
            child = centers[cursor] + letter
            child_norm = gram(child, child)
            destination = None
            for j, center in enumerate(centers):
                squared_distance = (
                    child_norm + gram(center, center) - 2 * gram(child, center)
                )
                if squared_distance <= threshold:
                    destination = j
                    break
            if destination is None:
                destination = len(centers)
                centers.append(child)
            transitions[cursor, letter] = destination
        cursor += 1
    return centers, transitions


def exact_linear_learner(gram):
    """Discover a basis, certify exact closure, and fit operators from Gram only."""
    basis = [""]
    cursor = 0
    while cursor < len(basis):
        for letter in "ab":
            child = basis[cursor] + letter
            g = [[gram(u, v) for v in basis] for u in basis]
            cross = [gram(u, child) for u in basis]
            coefficients = solve(g, cross)
            residual_squared = gram(child, child) - sum(
                x * y for x, y in zip(cross, coefficients)
            )
            if residual_squared < 0:
                raise AssertionError("A valid exact Gram residual cannot be negative")
            if residual_squared > 0:
                basis.append(child)
        cursor += 1
    g = [[gram(u, v) for v in basis] for u in basis]
    operators = {}
    closure_residuals = []
    for letter in "ab":
        columns = []
        for word in basis:
            child = word + letter
            cross = [gram(u, child) for u in basis]
            column = solve(g, cross)
            columns.append(column)
            closure_residuals.append(
                gram(child, child) - sum(x * y for x, y in zip(cross, column))
            )
        operators[letter] = [list(row) for row in zip(*columns)]
    return basis, g, operators, closure_residuals


def predict(gram_matrix, operators, word):
    state = [F(1)] + [F(0)] * (len(gram_matrix) - 1)
    for letter in word:
        state = [sum(a * b for a, b in zip(row, state)) for row in operators[letter]]
    return sum(a * b for a, b in zip(gram_matrix[0], state))


def run():
    records = []
    model = None
    for inverse_rho in (8, 16, 32, 64):
        rho = F(1, inverse_rho)
        cover_source = GramSource(rho)
        centers, table = metric_cover(cover_source.gram, rho)

        linear_source = GramSource(rho)
        basis, gram_matrix, operators, residuals = exact_linear_learner(linear_source.gram)
        acquisition_counters = linear_source.counters()

        # Independent exact verification against new words; verification source
        # calls are separately counted and not folded into either acquisition bill.
        verification_source = GramSource(rho)
        test_words = [
            "", "a", "b", "ab", "ba", "aabb", "ab" * 31,
            "ba" * 47 + "b", "abbaba" * 19, "ab" * (2 * inverse_rho),
        ]
        errors = [
            predict(gram_matrix, operators, word) - verification_source.gram("", word)
            for word in test_words
        ]
        assert all(e == 0 for e in errors)
        assert all(e == 0 for e in residuals)
        assert len(basis) == 2
        assert operators["a"] == [[F(1), 2 * linear_source.cosine], [F(0), F(-1)]]
        assert operators["b"] == [[F(0), F(1)], [F(1), F(0)]]

        record = {
            "inverse_rho": inverse_rho,
            "rho": str(rho),
            "cover_centers": len(centers),
            "cover_transitions": len(table),
            "cover_max_word_length": max(map(len, centers)),
            **{"cover_" + k: v for k, v in cover_source.counters().items()},
            "linear_rank": len(basis),
            "linear_matrix_entries": sum(len(row) for a in operators.values() for row in a),
            **{"linear_" + k: v for k, v in acquisition_counters.items()},
            "gram_condition_number": inverse_rho ** 2,
            "checked_new_words": len(test_words),
            "exact_prediction_errors": [str(e) for e in errors],
            "verification_scalar_queries": verification_source.queries,
            "verification_primitive_word_steps": verification_source.steps,
        }
        records.append(record)
        model = {
            "rho": str(rho),
            "basis_words": basis,
            "gram_matrix": [[str(v) for v in row] for row in gram_matrix],
            "operator_a": [[str(v) for v in row] for row in operators["a"]],
            "operator_b": [[str(v) for v in row] for row in operators["b"]],
            "closure_residuals": [str(e) for e in residuals],
        }
        print(json.dumps(record))

    destination = Path(__file__).resolve().parent
    (destination / "metric_cover_counterfixture_results.json").write_text(
        json.dumps({"records": records, "last_learned_model": model}, indent=2) + "\n"
    )
    table_keys = [
        "inverse_rho", "cover_centers", "cover_scalar_queries",
        "cover_primitive_word_steps", "cover_max_pair_length",
        "linear_rank", "linear_scalar_queries", "linear_primitive_word_steps",
        "gram_condition_number",
    ]
    with (destination / "metric_cover_counterfixture_results.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=table_keys)
        writer.writeheader()
        writer.writerows({k: record[k] for k in table_keys} for record in records)


if __name__ == "__main__":
    run()
