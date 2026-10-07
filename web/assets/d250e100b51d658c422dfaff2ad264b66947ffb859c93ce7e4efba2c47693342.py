"""Exact rational checks of the homogeneous field lift and trace identity.

This enumerates finite fixtures. It does not implement the imported FPRAS.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def det(matrix):
    a = [row[:] for row in matrix]
    value = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[pivot], a[i] = a[i], a[pivot]
            value = -value
        p = a[i][i]
        value *= p
        for j in range(i + 1, len(a)):
            scale = a[j][i] / p
            for k in range(i + 1, len(a)):
                a[j][k] -= scale * a[i][k]
    return value


def field(s, b, c):
    r = abs(b) + abs(c)
    d, u, v = s * b, 1 + s * (r + c), 1 + s * (r - c)
    return [[u, d], [d, v]], (d, u, v)


def edge(s, alpha, gamma):
    a, b, c = 1 + s * (3 * alpha + gamma), 1 + s * (3 * alpha - gamma), 2 * s * alpha
    return [[a, F(0), F(0), F(0)], [F(0), b, c, F(0)],
            [F(0), c, b, F(0)], [F(0), F(0), F(0), a]]


def bits(i, n):
    return tuple((i >> (n - 1 - j)) & 1 for j in range(n))


def index(bs):
    value = 0
    for b in bs:
        value = 2 * value + b
    return value


def embed(local, qubits, n):
    size = 2 ** n
    out = [[F(0)] * size for _ in range(size)]
    for i, j in product(range(size), repeat=2):
        rb, cb = bits(i, n), bits(j, n)
        if any(rb[q] != cb[q] for q in range(n) if q not in qubits):
            continue
        out[i][j] = local[index([rb[q] for q in qubits])][index([cb[q] for q in qubits])]
    return out


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(a))), F(0))
             for j in range(len(a))] for i in range(len(a))]


def trace_product(gates, n):
    a = [[F(i == j) for j in range(2 ** n)] for i in range(2 ** n)]
    for qubits, local in gates:
        a = matmul(embed(local, qubits, n), a)
    return sum((a[i][i] for i in range(len(a))), F(0))


def lifted_count(gates, n):
    next_id = 0
    occurrences = {q: [] for q in range(n)}
    physical = []
    field_number = 0
    for qubits, local in gates:
        k = len(qubits)
        ids = list(range(next_id, next_id + 2 * k))
        next_id += 2 * k
        # One-qubit order x=complemented column, y=row;
        # two-qubit order row(q0),row(q1),column(q1),column(q0).
        if k == 1:
            row_ids, col_ids = [ids[1]], [ids[0]]
            dummy_no = field_number
            field_number += 1
        else:
            row_ids, col_ids = ids[:2], [ids[3], ids[2]]
            dummy_no = None
        for q, ri, ci in zip(qubits, row_ids, col_ids):
            occurrences[q].append((ri, ci))
        physical.append((qubits, local, row_ids, col_ids, dummy_no))

    num_physical = next_id
    term_lists = []
    for qubits, local, row_ids, col_ids, dummy_no in physical:
        terms = []
        for ri, ci in product(range(2 ** len(qubits)), repeat=2):
            weight = local[ri][ci]
            if not weight:
                continue
            selected = {v for v, b in zip(row_ids, bits(ri, len(qubits))) if b}
            selected.update(v for v, b in zip(col_ids, bits(ci, len(qubits))) if not b)
            if dummy_no is None:
                assert len(selected) == 2
                terms.append((frozenset(selected), weight))
            else:
                z = [num_physical + 2 * dummy_no, num_physical + 2 * dummy_no + 1]
                if len(selected) == 0:
                    terms.append((frozenset(selected | set(z)), weight))
                elif len(selected) == 1:
                    for zi in z:
                        terms.append((frozenset(selected | {zi}), weight / 2))
                else:
                    terms.append((frozenset(selected), weight))
        term_lists.append(terms)

    wires = []
    isolated = 0
    for chain in occurrences.values():
        if not chain:
            isolated += 1
            continue
        for i, (_, ci) in enumerate(chain):
            wires.append((ci, chain[(i + 1) % len(chain)][0]))

    total, accepted, tested, compensating = F(0), 0, 0, 0
    for choice in product(*term_lists):
        tested += 1
        selected = frozenset().union(*(item[0] for item in choice))
        assert len(selected) == 2 * len(gates)
        if not all((u in selected) + (v in selected) == 1 for u, v in wires):
            continue
        num_dummies = sum(v >= num_physical for v in selected)
        assert num_dummies == field_number
        # The uniform-matroid Q factor has coefficient one on this complement.
        weight = F(1)
        for _, local_weight in choice:
            weight *= local_weight
        total += weight
        accepted += 1
        field_degrees = [sum(v < num_physical for v in choice[i][0])
                         for i, item in enumerate(physical) if item[-1] is not None]
        if 0 in field_degrees and 2 in field_degrees:
            compensating += 1
    return total * 2 ** isolated, tested, accepted, compensating


def main():
    num_fields, num_nonzero_fields = 0, 0
    for s, b, c in product([F(0), F(1, 100), F(1, 2), F(2)],
                           [F(0), F(1, 3), F(2)],
                           [F(-2), F(-1, 2), F(0), F(3, 2)]):
        _, (d, u, v) = field(s, b, c)
        assert u > 0 and v > 0 and u * v > d ** 2
        h = [[F(0), d, u / 2, u / 2], [d, F(0), v / 2, v / 2],
             [u / 2, v / 2, F(0), d], [u / 2, v / 2, d, F(0)]]
        assert det([row[:2] for row in h[:2]]) == -d ** 2
        assert det([row[:3] for row in h[:3]]) == d * u * v / 2
        assert det(h) == d ** 2 * (d ** 2 - u * v)
        if d:
            num_nonzero_fields += 1
            # Inertia through the nonsingular x,y block (one +, one -).
            schur = [[-u * v / (2 * d), d - u * v / (2 * d)],
                     [d - u * v / (2 * d), -u * v / (2 * d)]]
            assert det(schur) == u * v - d ** 2
            assert schur[0][0] < 0 and det(schur) > 0
        num_fields += 1

    fixtures = []
    for s in [F(1, 100), F(1, 7), F(1, 2)]:
        for gamma in [F(-1), F(-1, 4), F(0), F(1, 3), F(1)]:
            e = edge(s, F(1), gamma)
            f0, _ = field(s, F(2, 3), F(-1, 2))
            f1, _ = field(s, F(1, 5), F(3, 2))
            f2, _ = field(s, F(0), F(-2))
            cases = [
                (1, [((0,), f0)]),
                (1, [((0,), f0), ((0,), f1)]),
                (2, [((0, 1), e)]),
                (2, [((0, 1), e), ((0,), f0), ((1,), f1)]),
                (3, [((0, 1), e), ((1, 2), e), ((2, 0), e), ((1,), f0)]),
                (3, [((0, 1), e), ((0,), f0), ((1, 2), e), ((1,), f1),
                     ((2, 0), e), ((2,), f2)]),
            ]
            for n, gates in cases:
                trace = trace_product(gates, n)
                count, tested, accepted, compensating = lifted_count(gates, n)
                assert trace == count
                fixtures.append({"n": n, "gates": len(gates), "s": str(s),
                                 "gamma": str(gamma), "trace": str(trace),
                                 "tested_monomial_products": tested,
                                 "accepted_monomial_products": accepted,
                                 "compensating_degree_zero_and_two_field_products": compensating})
    report = {"field_parameter_fixtures": num_fields,
              "nonzero_field_inertia_fixtures": num_nonzero_fields,
              "trace_lift_fixtures": len(fixtures),
              "total_monomial_products": sum(x["tested_monomial_products"] for x in fixtures),
              "compensating_degree_zero_and_two_field_products":
                  sum(x["compensating_degree_zero_and_two_field_products"] for x in fixtures),
              "all_passed": True, "fixtures": fixtures,
              "scope": "Exact finite checks only; no FPRAS implemented."}
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != "fixtures"}))


if __name__ == '__main__':
    main()
