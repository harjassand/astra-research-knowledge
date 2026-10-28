#!/usr/bin/env python3
"""Exact verification of the two-live-state single-action obstruction.

Only Python's standard library is used. Fractions are exact. The conjugacy
identities prove equality at every repetition length; finite word calculations
then exhibit both mixed-response and program-order differences.
"""

from fractions import Fraction as F
import json


def scaled(rows, denominator):
    return tuple(tuple(F(x, denominator) for x in row) for row in rows)


def mul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def sub(left, right):
    return tuple(tuple(left[i][j] - right[i][j] for j in range(2)) for i in range(2))


def det(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def survives(actions, word):
    """Word letters are chronological; start is (1/2, 1/2), readout is (1,1)."""
    product = scaled(((1, 0), (0, 1)), 1)
    for letter in word:
        product = mul(actions[letter], product)
    return sum(sum(row) for row in product) / 2


def stringify(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: stringify(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [stringify(item) for item in value]
    return value


def main():
    identity = scaled(((1, 0), (0, 1)), 1)
    swap = scaled(((0, 1), (1, 0)), 1)
    a = scaled(((10, 2), (2, 2)), 16)
    b_plus = scaled(((8, 1), (1, 2)), 16)
    b_minus = scaled(((2, 1), (1, 8)), 16)
    families = {"plus": {"A": a, "B": b_plus}, "minus": {"A": a, "B": b_minus}}

    # Together with swap * 1 = 1, these establish all-horizon equality.
    assert mul(swap, swap) == identity
    assert tuple(sum(row) for row in swap) == (1, 1)
    assert mul(mul(swap, b_plus), swap) == b_minus
    assert mul(mul(swap, a), swap) != a

    properties = {}
    for name, matrix in (("A", a), ("B_plus", b_plus), ("B_minus", b_minus)):
        assert all(entry > 0 for row in matrix for entry in row)
        assert matrix[0][1] == matrix[1][0]
        row_sums = tuple(sum(row) for row in matrix)
        assert max(row_sums) < 1
        assert matrix[0][0] > 0 and det(matrix) > 0
        properties[name] = {"matrix": matrix, "row_sums": row_sums, "determinant": det(matrix)}

    # Cayley-Hamilton gives an exact recurrence for all survival moments.
    recurrences = {}
    for label, matrix in (("A", a), ("B", b_plus)):
        trace = matrix[0][0] + matrix[1][1]
        determinant = det(matrix)
        polynomial = sub(sub(mul(matrix, matrix), tuple(tuple(trace * x for x in row) for row in matrix)),
                         tuple(tuple(-determinant * x for x in row) for row in identity))
        assert polynomial == scaled(((0, 0), (0, 0)), 1)
        recurrences[label] = {"s0": F(1), "s1": sum(sum(row) for row in matrix) / 2,
                              "trace": trace, "determinant": determinant,
                              "rule": "s[n+2] = trace*s[n+1] - determinant*s[n]"}

    words = ("AB", "BA", "AAB", "ABA", "BAA")
    responses = {name: {word: survives(family, word) for word in words}
                 for name, family in families.items()}
    assert responses["plus"]["AB"] == F(15, 64)
    assert responses["minus"]["AB"] == F(9, 64)
    mixed_gap = responses["plus"]["AB"] - responses["minus"]["AB"]
    assert mixed_gap == F(3, 32)
    order_gaps = {name: values["AAB"] - values["ABA"] for name, values in responses.items()}
    assert order_gaps == {"plus": F(-1, 256), "minus": F(5, 256)}
    commutators = {name: sub(mul(a, family["B"]), mul(family["B"], a))
                   for name, family in families.items()}
    assert all(matrix != scaled(((0, 0), (0, 0)), 1) for matrix in commutators.values())
    for family in families.values():
        for word in words:
            assert survives(family, word) == survives(family, word[::-1])

    print(json.dumps(stringify({"properties": properties, "all_horizon_recurrences": recurrences,
                               "responses": responses, "mixed_gap": mixed_gap,
                               "order_gaps_AAB_minus_ABA": order_gaps,
                               "commutators_AB_minus_BA": commutators}), indent=2))


if __name__ == "__main__":
    main()
