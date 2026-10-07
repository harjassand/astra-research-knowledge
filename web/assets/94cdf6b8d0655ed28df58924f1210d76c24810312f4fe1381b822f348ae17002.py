"""Exact boundary-entry audit for rational p2 field gates.

This checks a finite family of 1-qubit products. It is deliberately not an
implementation or proof of the imported coefficient FPRAS.
"""
from fractions import Fraction as F
from itertools import product


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def field_gate(b, c, h):
    r = b + abs(c)
    A = [[r + c, b], [b, r - c]]
    A2 = mm(A, A)
    Fmat = [[F(int(i == j)) + h * A[i][j] + h*h*A2[i][j]/2
              for j in range(2)] for i in range(2)]
    return Fmat


def local_terms(Fmat, row, col, gate_id):
    """Lift monomials for x=row, y=1-col; return dummy set and coefficient."""
    v, d = Fmat[0]
    u = Fmat[1][1]
    x, y = row, 1 - col
    if (x, y) == (0, 0):
        return [(frozenset({2*gate_id, 2*gate_id+1}), d)]
    if (x, y) == (1, 1):
        return [(frozenset(), d)]
    if (x, y) == (1, 0):
        return [(frozenset({2*gate_id}), u/2),
                (frozenset({2*gate_id+1}), u/2)]
    return [(frozenset({2*gate_id}), v/2),
            (frozenset({2*gate_id+1}), v/2)]


def lifted_entry(gates, a, b):
    f = len(gates)
    delta = a - b
    p_dummy_rank = f - delta
    q_dummy_rank = f + delta
    assert 0 <= p_dummy_rank <= 2*f
    assert 0 <= q_dummy_rank <= 2*f

    total = F(0)
    # Internal wire values determine each gate's row/column pair. The fixed
    # outer row/column pins contribute 1+delta selected physical variables.
    for internal in product((0, 1), repeat=max(0, f-1)):
        path = (a,) + internal + (b,)
        choices = [local_terms(gates[j], path[j], path[j+1], j)
                   for j in range(f)]
        for chosen in product(*choices):
            dummy_set = frozenset().union(*(term[0] for term in chosen))
            if len(dummy_set) != p_dummy_rank:
                continue
            # The e_(f+delta) coefficient is one on the unique complement.
            assert 2*f - len(dummy_set) == q_dummy_rank
            coeff = F(1)
            for _, weight in chosen:
                coeff *= weight
            total += coeff
    return total


def direct_entry(gates, a, b):
    out = [[F(int(i == j)) for j in range(2)] for i in range(2)]
    for gate in gates:
        out = mm(out, gate)
    return out[a][b]


def main():
    inputs = [
        (F(1, 3), F(-1, 2), F(1, 5)),
        (F(2, 3), F(1, 4), F(1, 7)),
        (F(1), F(0), F(1, 3)),
    ]
    gates = [field_gate(*args) for args in inputs]
    cases = 0
    for length in (1, 2, 3):
        seq = gates[:length]
        for a, b in product((0, 1), repeat=2):
            got = lifted_entry(seq, a, b)
            want = direct_entry(seq, a, b)
            assert got == want, (length, a, b, got, want)
            cases += 1
    # Explicitly preserve a nonzero charge-changing entry and its rank shift.
    offdiag = lifted_entry(gates, 1, 0)
    assert offdiag == direct_entry(gates, 1, 0) and offdiag > 0
    assert len(gates) + (1 - 0) == 4
    print({"exact_fraction_entries": cases,
           "three_gate_10_entry": str(offdiag),
           "e_rank_for_10": len(gates) + 1,
           "status": "PASS; finite interface diagnostic only"})


if __name__ == "__main__":
    main()
