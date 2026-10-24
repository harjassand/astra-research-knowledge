"""Exact finite witness to failure of indecomposable reciprocal finiteness.

No external packages, floating point, or random search.  Integers encode F2
vectors.  The fixed support below was acquired as the first fundamental
degree-two inverse-graph circuit in ascending F128 order; verification only
uses the support, exact ranks, and the abstract doubling lemma in the note.
"""

import json

MODULUS = 0x83  # x^7 + x + 1
SUPPORT = [
    1, 2, 3, 6, 7, 9, 11, 15, 16, 17, 18, 19, 21, 22, 23, 25,
    30, 31, 32, 36, 37, 40, 43, 46, 48, 49, 50, 51, 53, 54, 55, 56,
]


def multiply(a, b):
    answer = 0
    while b:
        if b & 1:
            answer ^= a
        a <<= 1
        if a & 128:
            a ^= MODULUS
        b >>= 1
    return answer


def power(a, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = multiply(answer, a)
        a = multiply(a, a)
        exponent >>= 1
    return answer


def row_basis(rows):
    pivots = {}
    for value in rows:
        while value:
            position = value.bit_length() - 1
            if position not in pivots:
                pivots[position] = value
                break
            value ^= pivots[position]
    return list(pivots.values())


def null_basis(rows, width):
    rows = list(row_basis(rows))
    pivot_columns = []
    at = 0
    for column in range(width):
        found = next((j for j in range(at, len(rows))
                      if (rows[j] >> column) & 1), None)
        if found is None:
            continue
        rows[at], rows[found] = rows[found], rows[at]
        for j in range(len(rows)):
            if j != at and (rows[j] >> column) & 1:
                rows[j] ^= rows[at]
        pivot_columns.append(column)
        at += 1
    result = []
    for column in range(width):
        if column in pivot_columns:
            continue
        value = 1 << column
        for pivot, row in zip(pivot_columns, rows):
            if (row >> column) & 1:
                value |= 1 << pivot
        result.append(value)
    assert all((r & v).bit_count() % 2 == 0 for r in rows for v in result)
    return result


def main():
    # Every nonzero quotient element has an inverse, certifying that the
    # 128-element quotient by MODULUS is a field, not assuming irreducibility.
    assert all(multiply(u, power(u, 126)) == 1 for u in range(1, 128))
    assert len(SUPPORT) == len(set(SUPPORT)) == 32
    inverse = [power(u, 126) for u in SUPPORT]
    points = [u | (v << 7) for u, v in zip(SUPPORT, inverse)]
    width = len(SUPPORT)
    rows = [(1 << width) - 1]
    rows += [sum(((x >> bit) & 1) << j for j, x in enumerate(points))
             for bit in range(14)]
    d_basis = row_basis(rows)
    degree_two_rows = rows + [a & b for i, a in enumerate(rows[1:])
                             for b in rows[1:][i + 1:]]
    # Sum of all columns is zero; rank w-1 makes this the only nonzero
    # dependency, hence a minimal circuit (every proper subset independent).
    assert all(row.bit_count() % 2 == 0 for row in degree_two_rows)
    assert len(row_basis(degree_two_rows)) == width - 1 == 31
    assert len(d_basis) == 14 < width / 2
    assert all((a & b).bit_count() % 2 == 0 for a in d_basis for b in d_basis)
    perpendicular = null_basis(d_basis, width)
    assert len(perpendicular) == width - len(d_basis) == 18
    # C_D = {(u+d,u): d in D, u in Dperp}, in first/second-copy order.
    doubled = d_basis + [u | (u << width) for u in perpendicular]
    assert len(row_basis(doubled)) == width == 32
    assert all((a & b).bit_count() % 2 == 0 for a in doubled for b in doubled)
    # Each copy of every bit-plane of v and v^-1 lies in C_D.  Together
    # these give (v,tv) and its reciprocal for arbitrary nonzero scalar t.
    for row in rows:
        assert len(row_basis(doubled + [row])) == width
        assert len(row_basis(doubled + [row << width])) == width
    result = {
        "field_modulus": "x^7+x+1",
        "support": SUPPORT,
        "length_D": width,
        "dimension_D": len(d_basis),
        "dimension_D_perp": len(perpendicular),
        "rank_degree_two_lift": len(row_basis(degree_two_rows)),
        "D_generators_hex": [hex(row) for row in d_basis],
        "doubled_length": 2 * width,
        "doubled_dimension": len(row_basis(doubled)),
        "status": "PASS: exact circuit and self-dual doubling identities",
        "scope": "Indecomposability and curve follow from the companion proof; "
                 "no prime-extension sampler failure is inferred.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
