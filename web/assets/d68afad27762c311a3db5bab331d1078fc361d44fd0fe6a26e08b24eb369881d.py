"""Exact tiny check of composing higher-spin projectors with rational p2 gates.

Independent standard-library Fraction implementation. This checks one
spin-1 / spin-1/2 embedded trace network and the projector commutator; it does
not run the Chen--Liu FPRAS or certify an asymptotic theorem.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json
from pathlib import Path


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def mscale(c, a):
    return [[c * z for z in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def p2(a, t):
    return madd(madd(eye(len(a)), mscale(t, a)),
                mscale(t * t / 2, mm(a, a)))


def edge_shifted(alpha, gamma):
    alpha, gamma = F(alpha), F(gamma)
    return [[3*alpha+gamma, 0, 0, 0],
            [0, 3*alpha-gamma, 2*alpha, 0],
            [0, 2*alpha, 3*alpha-gamma, 0],
            [0, 0, 0, 3*alpha+gamma]]


def projector(q):
    d = 1 << q
    return [[F(1, comb(q, r.bit_count())) if r.bit_count() == c.bit_count()
             else F(0) for c in range(d)] for r in range(d)]


def make_gate(kind, qubits, matrix, q=None):
    return {"kind": kind, "qubits": tuple(qubits), "matrix": matrix, "q": q}


def gate_entry(g, row, col):
    if g["kind"] == "projector":
        return F(1, comb(g["q"], row.bit_count())) if row.bit_count() == col.bit_count() else F(0)
    return g["matrix"][row][col]


def embed(g, nqubits):
    dim = 1 << nqubits
    qset = set(g["qubits"])
    local_n = len(g["qubits"])
    out = [[F(0) for _ in range(dim)] for _ in range(dim)]
    for r in range(dim):
        lr = sum(((r >> q) & 1) << j for j, q in enumerate(g["qubits"]))
        for c in range(dim):
            if any(((r >> q) & 1) != ((c >> q) & 1)
                   for q in range(nqubits) if q not in qset):
                continue
            lc = sum(((c >> q) & 1) << j for j, q in enumerate(g["qubits"]))
            out[r][c] = gate_entry(g, lr, lc)
    return out


def exact_trace(gates, nqubits):
    out = eye(1 << nqubits)
    for g in gates:
        out = mm(out, embed(g, nqubits))
    return trace(out)


def compile_and_count(gates, nqubits):
    factors, timeline, cursor, dummy = [], [[] for _ in range(nqubits)], 0, []
    for g in gates:
        k = len(g["qubits"])
        rows = tuple(range(cursor, cursor+k)); cursor += k
        cols = tuple(range(cursor, cursor+k)); cursor += k
        dums = tuple(range(cursor, cursor+2)) if g["kind"] == "field" else ()
        cursor += len(dums); dummy.extend(dums)
        degree = g["q"] if g["kind"] == "projector" else 2
        coords = rows + cols + dums
        choices = []
        for picked in combinations(coords, degree):
            chosen = set(picked)
            row = sum(((u in chosen) << j) for j,u in enumerate(rows))
            col = sum(((u not in chosen) << j) for j,u in enumerate(cols))
            value = gate_entry(g, row, col)
            if g["kind"] == "field" and row == col:
                value /= 2
            if value:
                mask = sum(1 << u for u in picked)
                choices.append((mask, value))
        factors.append(choices)
        for j,q in enumerate(g["qubits"]):
            timeline[q].append((rows[j], cols[j]))

    wires = []
    for visits in timeline:
        for i, (row, col) in enumerate(visits):
            wires.append((visits[i-1][1], row))
    f = len(dummy) // 2
    universe = (1 << cursor) - 1
    total, terms = F(0), 0
    for local in product(*factors):
        mask, weight = 0, F(1)
        for m,w in local:
            mask |= m; weight *= w
        complement = universe ^ mask
        if any(((complement >> a) & 1) + ((complement >> b) & 1) != 1
               for a,b in wires):
            continue
        if sum((complement >> u) & 1 for u in dummy) != f:
            continue
        total += weight; terms += 1
    return total, cursor, terms


def main():
    # Physical spins S_0=1 and S_1=1/2; q=(2,1). One edge, alpha=1,
    # gamma=-1/2, no fields. Embed two constituent-qubit interactions with
    # alpha'=alpha/4 and gamma'=gamma/4.
    q0, q1 = 2, 1
    alpha, gamma = F(1), F(-1, 2)
    alpha_p, gamma_p = alpha/4, gamma/4
    t = F(1, 2)  # beta/(2m) for beta=1,m=1
    p2a = p2(edge_shifted(alpha_p, gamma_p), t)
    p2g0 = make_gate("edge", (0, 2), p2a)
    p2g1 = make_gate("edge", (1, 2), p2a)
    pi0 = make_gate("projector", (0, 1), None, q=q0)
    pi1 = make_gate("projector", (2,), None, q=q1)
    # Tr(Pi W W* Pi), with W=F_0 F_1 and F_i symmetric.
    gates = [pi0, pi1, p2g0, p2g1, p2g1, p2g0, pi0, pi1]
    dense = exact_trace(gates, 3)
    coeff, variables, accepted = compile_and_count(gates, 3)
    assert dense == coeff

    # The embedded shifted Hamiltonian commutes with the spin-1 projector.
    h0 = embed(make_gate("edge", (0, 2), edge_shifted(alpha_p, gamma_p)), 3)
    h1 = embed(make_gate("edge", (1, 2), edge_shifted(alpha_p, gamma_p)), 3)
    k = madd(h0, h1)
    pi = mm(embed(pi0, 3), embed(pi1, 3))
    assert mm(pi, k) == mm(k, pi)
    # p2 edge table is complement invariant in the row/complement-column lift.
    table = {}
    for picked in combinations(range(4), 2):
        chosen = set(picked)
        row = sum(((u in chosen) << j) for j,u in enumerate((0,1)))
        col = sum(((u not in chosen) << j) for j,u in enumerate((2,3)))
        table[sum(1 << u for u in picked)] = p2a[row][col]
    for mask, val in table.items():
        assert table[((1 << 4)-1) ^ mask] == val

    report = {
        "status": "PASS_EXACT_TINY_HIGHER_SPIN_P2_LIFT",
        "physical_spin_labels": ["1", "1/2"],
        "q": [q0, q1],
        "alpha": str(alpha), "gamma": str(gamma), "beta": "1", "m": 1,
        "compressed_p2_trace": str(dense),
        "homogeneous_coefficient": str(coeff),
        "ground_variables": variables,
        "accepted_local_contractions": accepted,
        "embedded_shifted_hamiltonian_commutes_with_projector": True,
        "p2_edge_signature_complement_invariant": True,
        "scope": "one exact finite fixture; no FPRAS, no all-size gap or error proof",
    }
    target = Path(__file__).with_name("higher_spin_p2_check.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
