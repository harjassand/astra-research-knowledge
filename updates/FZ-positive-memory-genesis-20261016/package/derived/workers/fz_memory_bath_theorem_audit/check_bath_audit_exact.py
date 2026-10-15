#!/usr/bin/env python3
"""Independent bounded diagnostics, not a stochastic lifetime certification.

Uses exact SymPy rational/Gaussian-rational matrix arithmetic. No constructor
check or constructor implementation is imported. Writes only beside this file.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
I2 = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
PAULIS = (I2, X, Y, Z)
checks = []


def eq(label, left, right):
    difference = (left - right).applyfunc(s.simplify)
    assert difference == s.zeros(*difference.shape), label
    checks.append({"label": label, "passed": True})


def tensor(*values):
    return s.kronecker_product(*values)


def qpauli(q, p):
    factors = [I2] * 4
    factors[q] = p
    return tensor(*factors)


def pt(matrix, left_dim, right_dim, trace_right=True):
    if trace_right:
        return s.Matrix(left_dim, left_dim, lambda a, b:
                        sum(matrix[a * right_dim + r, b * right_dim + r]
                            for r in range(right_dim)))
    return s.Matrix(right_dim, right_dim, lambda a, b:
                    sum(matrix[r * right_dim + a, r * right_dim + b]
                        for r in range(left_dim)))


def matrix_json(matrix):
    return [[str(matrix[a, b]) for b in range(matrix.cols)]
            for a in range(matrix.rows)]


def main():
    # [[4,2,2]] code. All Pauli errors at one designated erasure location have
    # different two-generator syndromes. The location changes after recovery.
    Vt = s.zeros(16, 4)
    for column, word in enumerate((0, 3, 5, 6)):
        Vt[word, column] = 1
        Vt[word ^ 15, column] = 1
    eq("unnormalized isometry Vt^dagger Vt=2I4", Vt.H * Vt, 2 * s.eye(4))
    GX, GZ = tensor(X, X, X, X), tensor(Z, Z, Z, Z)
    eq("XXXX fixes full code", GX * Vt, Vt)
    eq("ZZZZ fixes full code", GZ * Vt, Vt)
    projector = Vt * Vt.H / 2
    eq("full rank-four stabilizer projector", projector,
       (s.eye(16) + GX) * (s.eye(16) + GZ) / 4)

    def recovery(q):
        data = []
        for p in PAULIS:
            E = qpauli(q, p)
            syndrome = E * projector * E.H
            C = E.H * syndrome
            Dt = Vt.H * C
            data.append((E, syndrome, C, Dt))
        eq(f"q{q+1} syndrome projectors resolve physical identity",
           sum((r[1] for r in data), s.zeros(16)), s.eye(16))
        eq(f"q{q+1} correction proposal CPTP",
           sum((r[2].H * r[2] for r in data), s.zeros(16)), s.eye(16))
        eq(f"q{q+1} fixed decoder CPTP",
           sum((r[3].H * r[3] / 2 for r in data), s.zeros(16)), s.eye(16))
        for error_idx, E in enumerate(r[0] for r in data):
            for syndrome_idx, (_, _, _, Dt) in enumerate(data):
                eq(f"q{q+1} all-Pauli fixed recovery {error_idx}:{syndrome_idx}",
                   Dt * E * Vt / 2,
                   s.eye(4) if error_idx == syndrome_idx else s.zeros(4))
        return data

    c1 = recovery(0)
    d2 = recovery(1)
    # Two noncommuting bath coefficients and a shared bath at DISTINCT patches.
    def rotation(q, p, bath_p, a, b, denominator):
        return (a * s.eye(32) + s.I * b * tensor(qpauli(q, p), bath_p)) / denominator

    U1 = rotation(0, Z, X, 5, 12, 13) * rotation(0, X, Z, 3, 4, 5)
    U2 = rotation(1, X, Y, 8, 15, 17) * rotation(1, Z, X, 7, 24, 25)
    eq("first joint coherent interaction unitary", U1.H * U1, s.eye(32))
    eq("second joint coherent interaction unitary", U2.H * U2, s.eye(32))
    assert Z * X != X * Z
    checks.append({"label": "bath expansion coefficients do not commute", "passed": True})
    bath_kraus = (s.diag(1, s.Rational(3, 5)), s.Matrix([[0, s.Rational(4, 5)], [0, 0]]))
    eq("interposed bath-only channel CPTP",
       sum((K.H * K for K in bath_kraus), s.zeros(2)), I2)

    As, Bs = [], []
    Vjoint = tensor(Vt, I2)
    for cidx, (_, _, C, _) in enumerate(c1):
        for bidx, K in enumerate(bath_kraus):
            prefix = U2 * tensor(s.eye(16), K) * tensor(C, I2) * U1 * Vjoint
            for didx, (_, _, _, Dt) in enumerate(d2):
                A = (tensor(Dt, I2) * prefix / 2).applyfunc(s.simplify)
                B = A[:2, :2]
                eq(f"recovered record {cidx}:{bidx}:{didx} factors I4 tensor B", A,
                   tensor(s.eye(4), B))
                As.append(A)
                Bs.append(B)
    eq("recovered full joint channel CPTP",
       sum((A.H * A for A in As), s.zeros(8)), s.eye(8))
    eq("bath Kraus completeness after chronological summation",
       sum((B.H * B for B in Bs), s.zeros(2)), I2)

    # Arbitrary-joint-input implication receives a concrete entangled L-B-R
    # check. The operator factorization above is the full proof for all inputs.
    psi = s.zeros(16, 1)  # L dimension 4, bath 2, reference 2
    # One logical qubit is Bell-entangled with B; the other with R.
    for idx in (0, 5, 10, 15):
        psi[idx] = 1
    rho = psi * psi.H / 4
    output = sum((tensor(A, I2) * rho * tensor(A.H, I2) for A in As), s.zeros(16))

    def trace_bath_lbr(value):
        return s.Matrix(8, 8, lambda u, v:
                        sum(value[(u // 2) * 4 + bath * 2 + u % 2,
                                  (v // 2) * 4 + bath * 2 + v % 2]
                            for bath in range(2)))

    eq("initial L-B-R entanglement preserves reduced L-R exactly",
       trace_bath_lbr(output), trace_bath_lbr(rho))

    # Outcome rates: good-schedule bath measurement is NOT a TP conditioned
    # branch. It steers L when L and B start entangled.
    bell = s.Matrix([1, 0, 0, 1])
    bell_rho = bell * bell.H / 2
    p0, p1 = s.diag(1, 0), s.diag(0, 1)
    branch0 = tensor(I2, p0) * bell_rho * tensor(I2, p0)
    eq("bath outcome branch probability one half", s.Matrix([[s.trace(branch0)]]),
       s.Matrix([[s.Rational(1, 2)]]))
    eq("normalized bath outcome steers logical marginal", pt(2 * branch0, 2, 2), p0)
    avg = sum((tensor(I2, p) * bell_rho * tensor(I2, p) for p in (p0, p1)), s.zeros(4))
    eq("averaged bath measurement preserves logical marginal", pt(avg, 2, 2), I2 / 2)

    # The constant 2 in the averaged-channel bound can be attained.
    p_bad = s.Rational(1, 7)
    two_p_difference = (1 - p_bad) * p0 + p_bad * X * p0 * X - p0
    eq("mixture bound sharp on one input at p_bad=1/7",
       s.Matrix([[sum(abs(ev) * mult for ev, mult in two_p_difference.eigenvals().items())]]),
       s.Matrix([[2 * p_bad]]))

    # If schedule generation itself measures the data, apparent all-identity
    # conditional circuits omit the generating instrument. p_bad=0 is false
    # evidence for preservation: |+> dephases and trace distance is exactly 1.
    plus = s.Matrix([1, 1])
    plus_rho = plus * plus.H / 2
    dephased = p0 * plus_rho * p0 + p1 * plus_rho * p1
    delta = dephased - plus_rho
    eq("data-controlled clock countermodel squared difference", delta * delta, I2 / 4)
    eq("data-controlled clock fails at apparent p_bad zero",
       s.Matrix([[sum(abs(ev) * mult for ev, mult in delta.eigenvals().items())]]),
       s.Matrix([[1]]))

    # Pointwise support events cannot be promoted to a universal event.
    # N location histories: for each of N error labels exactly one schedule is
    # bad, but a schedule-aware label can make every schedule bad.
    N = 5
    bad = [[int(h == label) for label in range(N)] for h in range(N)]
    assert all(sum(bad[h][label] for h in range(N)) == 1 for label in range(N))
    assert sum(bad[h][h] for h in range(N)) == N
    checks.append({"label": "pointwise 1/N bad rates permit universal bad rate one", "passed": True})

    # Error-dependent inverses: I and Z individually invertible; their common
    # coherent span is not correctable on an unencoded logical qubit.
    eq("individual inverse I", I2.H * I2, I2)
    eq("individual inverse Z", Z.H * Z, I2)
    assert I2.H * Z != s.trace(Z) * I2 / 2
    checks.append({"label": "cross-error KL matrix Z is not scalar identity", "passed": True})
    # The literal expansion issue on a two-qubit patch: Z tensor Z does not
    # belong to the span of I and all weight-one Paulis.
    weight1 = [tensor(I2, I2)] + [tensor(p, I2) for p in (X, Y, Z)] + [tensor(I2, p) for p in (X, Y, Z)]
    assert all(s.trace(E.H * tensor(Z, Z)) == 0 for E in weight1)
    checks.append({"label": "all patch Paulis required; weight-two ZZ missing from weight-one span", "passed": True})

    # Memory-only depolarization has no Choi interior for joint A-B maps.
    # On u=Omega_A Omega_B, v=Z_A Omega_A Z_B Omega_B, the normalized Choi
    # of D_A tensor Id_B + epsilon[-i Z_A Z_B, .] has this principal block.
    epsilon = s.Symbol("epsilon", real=True)
    choi_block = s.Matrix([[s.Rational(1, 4), s.I * epsilon], [-s.I * epsilon, 0]])
    def joint_map(matrix):
        floor = tensor(I2 / 2, pt(matrix, 2, 2, trace_right=False))
        hamiltonian = tensor(Z, Z)
        return floor - s.I * epsilon * (hamiltonian * matrix - matrix * hamiltonian)

    choi = s.zeros(16)
    for row in range(4):
        for col in range(4):
            unit = s.zeros(4)
            unit[row, col] = 1
            choi += tensor(joint_map(unit), unit) / 4
    u = s.zeros(16, 1)
    for k in range(4):
        u[4 * k + k] = s.Rational(1, 2)
    v = tensor(tensor(Z, Z), s.eye(4)) * u
    compress = s.Matrix.hstack(u, v)
    eq("full joint Choi reconstructs asserted principal block",
       compress.H * choi * compress, choi_block)
    eq("memory-only floor joint Choi principal determinant negative",
       s.Matrix([[choi_block.det()]]), s.Matrix([[-epsilon**2]]))

    payload = {
        "status": "ALL_STATED_BOUNDED_EXACT_CHECKS_PASSED",
        "arithmetic": "SymPy exact integers, rationals and I; no floating-point tolerance",
        "independence": "No constructor program or result was imported or replayed",
        "code": "[[4,2,2]] with XXXX, ZZZZ; logical dimension 4; four physical qubits",
        "schedule": "joint fault q1-B; full syndrome correction using q1; bath-only amplitude damping; joint fault q2-B; same fixed q2 final decoder",
        "bath_dimension": 2,
        "recovered_kraus_records": len(As),
        "nonzero_recovered_kraus_records": sum(A != s.zeros(8) for A in As),
        "checks_count": len(checks),
        "checks": checks,
        "bath_kraus": [matrix_json(B) for B in Bs],
        "countermodels": {
            "postselected_bath_measurement": {"branch_probability": "1/2", "logical_marginal_before": "I/2", "logical_marginal_after_normalization": "|0><0|"},
            "data_controlled_schedule": {"apparent_p_bad": "0", "trace_distance_on_plus": "1", "missing_step": "schedule-generating data measurement"},
            "pointwise_good_sets": {"N": N, "bad_rate_each_fixed_label": "1/5", "bad_rate_schedule_aware_selection": "1"},
            "joint_choi_floor": {"principal_block": matrix_json(choi_block), "determinant": "-epsilon**2", "conclusion": "not CP for every nonzero real epsilon"},
        },
        "scope": "Finite operator diagnostics and countermodels only. No LSS/HT import proof, 4D decoder certification, stochastic lifetime, novelty, or physical validation.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path = HERE / "EXACT_CHECKS.json"
    output_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({key: payload[key] for key in ("status", "checks_count", "recovered_kraus_records", "nonzero_recovered_kraus_records", "scope")}, indent=2))


if __name__ == "__main__":
    main()
