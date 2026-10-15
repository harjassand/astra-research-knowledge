#!/usr/bin/env python3
"""Independent exact checks. Writes only beside this script; no root code is used."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import time

import sympy as s

OUT = Path(__file__).resolve().parent
I = s.I
R = s.Rational
PAULI = {
    "I": s.eye(2),
    "X": s.Matrix([[0, 1], [1, 0]]),
    "Y": s.Matrix([[0, -I], [I, 0]]),
    "Z": s.diag(1, -1),
}


def clean(a):
    return a.applyfunc(s.simplify) if isinstance(a, s.MatrixBase) else s.simplify(a)


def assert_zero(a):
    a = clean(a)
    assert a == (s.zeros(*a.shape) if isinstance(a, s.MatrixBase) else 0), a


def pauli(word):
    a = s.ones(1)
    for letter in word:
        a = s.kronecker_product(a, PAULI[letter])
    return a


def ket(a):
    # (A tensor I)|Phi_d>, with output index first and input index second.
    d = a.rows
    return s.Matrix([a[i, j] / s.sqrt(d) for i in range(d) for j in range(d)])


def choi(d, operation):
    # Construct directly on matrix units, not from the claimed block formula.
    answer = s.zeros(d * d)
    for i in range(d):
        for j in range(d):
            unit = s.zeros(d)
            unit[i, j] = 1
            answer += s.kronecker_product(operation(unit), unit) / d
    return clean(answer)


def parts(words):
    matrices = [pauli(word) for word in words]
    d = matrices[0].rows
    j_id = choi(d, lambda a: a)
    j_h = [choi(d, lambda a, p=p: -I * (p * a - a * p)) for p in matrices]
    j_d = [choi(d, lambda a, p=p: p * a * p - a) for p in matrices]
    return matrices, j_id, j_h, j_d


def check_rate(words, h, gamma, precomputed=None):
    matrices, j_id, j_h, j_d = precomputed or parts(words)
    d = matrices[0].rows
    eye_ket = ket(s.eye(d))
    translated = [ket(p) for p in matrices]
    columns = s.Matrix.hstack(eye_ket, *translated)
    assert_zero(columns.conjugate().T * columns - s.eye(len(words) + 1))
    rate = sum(gamma) + sum(a * a / b for a, b in zip(h, gamma))
    j_rate = rate * j_id
    for a, b, j1, j2 in zip(h, gamma, j_h, j_d):
        j_rate += a * j1 + b * j2
    positive_gram = s.zeros(d * d)
    null_ket = eye_ket.copy()
    for a, b, p_ket in zip(h, gamma, translated):
        v = a / b * eye_ket - I * p_ket
        positive_gram += b * v * v.conjugate().T
        null_ket += I * a / b * p_ket
    assert_zero(j_rate - positive_gram)
    assert_zero(j_rate * null_ket)
    # Every tested rate has r_min >= 1/2, so the lower rate remains positive.
    delta = R(1, 4)
    assert rate > delta
    lower_choi = j_rate - delta * j_id
    negative_certificate = clean((null_ket.conjugate().T * lower_choi * null_ket)[0])
    assert negative_certificate == -delta
    return rate


def check_unitary(h, gamma, word):
    p = pauli(word)
    d = p.rows
    u = (h * s.eye(d) - I * gamma * p) / s.sqrt(h * h + gamma * gamma)
    rate = gamma + h * h / gamma
    assert_zero(u.conjugate().T * u - s.eye(d))
    for i in range(d):
        for j in range(d):
            a = s.zeros(d)
            a[i, j] = 1
            lhs = rate * (u * a * u.conjugate().T - a)
            rhs = -I * h * (p * a - a * p) + gamma * (p * a * p - a)
            assert_zero(lhs - rhs)


def principal_block(j, vectors):
    v = s.Matrix.hstack(*vectors)
    return clean(v.conjugate().T * j * v)


def run():
    started = time.monotonic()
    result = {
        "scope": "Exact finite algebra only; not an asymptotic memory proof or hardware validation",
        "python": platform.python_version(),
        "sympy": s.__version__,
    }
    frame = ["X", "Y", "Z"]
    cached = parts(frame)
    number = 0
    rates = set()
    for h in itertools.product((R(-1), R(0), R(1)), repeat=3):
        for gamma in itertools.product((R(1, 2), R(1), R(2)), repeat=3):
            rates.add(check_rate(frame, h, gamma, cached))
            number += 1
    result["one_qubit_exhaustion"] = {
        "cases": number,
        "h_values_per_coordinate": ["-1", "0", "1"],
        "gamma_values_per_coordinate": ["1/2", "1", "2"],
        "positive_Gram_certificate_at_threshold": True,
        "negative_quadratic_certificate_at_threshold_minus_quarter": True,
        "distinct_exact_rates": len(rates),
    }
    unitary_cases = 0
    for word in ("X", "Y", "Z", "XY"):
        for h, gamma in ((R(0), R(1)), (R(1), R(1)), (R(-1), R(2)), (R(3, 5), R(4, 5))):
            check_unitary(h, gamma, word)
            unitary_cases += 1
    result["direct_unitary_identities"] = unitary_cases

    multiqubit = []
    frames = [
        (["XI", "IZ"], [R(1), R(-1)], [R(1), R(2)]),
        (["XI", "ZI"], [R(3, 5), R(4, 5)], [R(3, 5), R(4, 5)]),
        (["XX", "ZZ"], [R(2), R(3)], [R(1), R(3)]),
        (["XY", "YX", "ZI"], [R(1), R(-2), R(0)], [R(2), R(1), R(1, 2)]),
    ]
    full = ["".join(x) for x in itertools.product("IXYZ", repeat=2) if x != ("I", "I")]
    frames.append((full, [R((i % 3) - 1, 2) for i in range(15)], [R(1 + i % 2) for i in range(15)]))
    for words, h, gamma in frames:
        rate = check_rate(words, h, gamma)
        multiqubit.append({"frame": words, "rate": str(rate), "frame_size": len(words)})
    result["two_qubit_cases"] = multiqubit
    spectator = check_rate(["X", "Z"], [R(3, 5), R(4, 5)], [R(3, 5), R(4, 5)])
    assert spectator == R(14, 5) == R(multiqubit[1]["rate"])
    result["spectator_tensor_factor_preserves_rate"] = str(spectator)

    r = s.Symbol("r", positive=True)
    z = PAULI["Z"]
    j_pure = choi(2, lambda a: r * a - I * (z * a - a * z))
    block_pure = principal_block(j_pure, [ket(s.eye(2)), ket(z)])
    assert clean(block_pure.det()) == -1
    wrong_floor = choi(2, lambda a: r * a - I * (PAULI["X"] * a - a * PAULI["X"]) + z * a * z - a)
    block_wrong = principal_block(wrong_floor, [ket(s.eye(2)), ket(PAULI["X"])])
    assert clean(block_wrong.det()) == -1
    p, h_bath = pauli("ZI"), pauli("ZZ")
    j_bath = choi(4, lambda a: r * a - I * (h_bath * a - a * h_bath) + p * a * p - a)
    block_bath = principal_block(j_bath, [ket(s.eye(4)), ket(h_bath)])
    assert clean(block_bath.det()) == -1
    damping = s.Matrix([[0, 1], [0, 0]])
    n = damping.conjugate().T * damping
    j_damping = choi(2, lambda a: r * a + damping * a * damping.conjugate().T - (n * a + a * n) / 2)
    damping_minor = clean(j_damping.extract([0, 3], [0, 3]).det())
    assert damping_minor == -R(1, 16)
    result["singular_countermodels"] = {
        "pure_H_Z_principal_determinant_of_rJ": str(clean(block_pure.det())),
        "H_X_with_Z_floor_principal_determinant_of_rJ": str(clean(block_wrong.det())),
        "H_Z_tensor_Z_with_only_Z_tensor_I_floor_principal_determinant_of_rJ": str(clean(block_bath.det())),
        "amplitude_damping_principal_determinant_of_rJ": str(damping_minor),
        "all_are_negative_for_every_finite_positive_r": True,
    }
    # Repeated directions must be merged; h=1 and h=-1 cancel exactly.
    duplicate_actual = check_rate(["Z"], [R(0)], [R(2)])
    duplicate_naive = R(1) + R(1) + R(1) + R(1)
    assert duplicate_actual == 2 and duplicate_naive == 4
    result["dependent_frame_countermodel"] = {"actual_rate": str(duplicate_actual), "unmerged_formula": str(duplicate_naive)}

    t = s.Symbol("t", positive=True)
    paths = [t**2 + 1, 2 * t**2, t**4 + t**-2]
    assert [s.limit(x, t, 0, dir="+") for x in paths] == [1, 0, s.oo]
    result["joint_zero_limits"] = [
        {"h": "t", "gamma": "t^2", "rate_limit": "1"},
        {"h": "t^2", "gamma": "t^2", "rate_limit": "0"},
        {"h": "t", "gamma": "t^4", "rate_limit": "infinity"},
    ]

    eps = [R(3), R(4)]
    box_vertices = list(itertools.product((-1, 1), repeat=2))
    box_rates = [sum(eps) + sum((sg * e)**2 / e for sg, e in zip(signs, eps)) for signs in box_vertices]
    assert box_rates == [14] * 4
    test_floors = [[R(1), R(2)], [R(3), R(4)], [R(9, 5), R(16, 5)], [R(8), R(3, 2)]]
    for gamma in test_floors:
        worst = sum(gamma) + sum(e * e / g for e, g in zip(eps, gamma))
        gap = sum((g - e)**2 / g for e, g in zip(eps, gamma))
        assert clean(worst - 14 - gap) == 0
    result["robust_box"] = {"epsilon": ["3", "4"], "optimal_floors": ["3", "4"], "exact_worst_rate": "14", "vertices_checked": 4}

    b, big_b = eps, R(5)
    floors = [x * x / big_b for x in b]
    ellipsoid_points = [[R(3), R(0)], [R(0), R(4)], [R(9, 5), R(16, 5)], [R(-9, 5), R(16, 5)], [R(0), R(0)]]
    ellipsoid_rates = []
    for h in ellipsoid_points:
        normalized = sum((x / y)**2 for x, y in zip(h, b))
        rate = sum(floors) + sum(x * x / g for x, g in zip(h, floors))
        assert rate == big_b * (1 + normalized)
        ellipsoid_rates.append(str(rate))
    for gamma in test_floors:
        zmax = max(x * x / g for x, g in zip(b, gamma))
        worst = sum(gamma) + zmax
        assert worst >= 10
        assert sum(gamma) >= 25 / zmax
    result["robust_ellipsoid"] = {"axes": ["3", "4"], "B": "5", "optimal_floors": ["9/5", "16/5"], "exact_worst_rate": "10", "point_rates": ellipsoid_rates}

    h_op = R(3, 5) * PAULI["X"] + R(4, 5) * PAULI["Z"]
    assert_zero(h_op * h_op - s.eye(2))
    result["operator_norm_countermodel"] = {"H": "(3X+4Z)/5", "operator_norm": "1", "coefficient_l1": "7/5", "best_diagonal_floor_rate_for_this_H": "14/5", "invalid_2_operator_norm_substitution": "2"}
    for n_qubits in range(1, 6):
        for weight in range(1, min(n_qubits, 3) + 1):
            count = sum(1 for word in itertools.product("IXYZ", repeat=n_qubits) if 1 <= sum(a != "I" for a in word) <= weight)
            formula = sum(3**w * s.binomial(n_qubits, w) for w in range(1, weight + 1))
            assert count == formula
    result["catalog_counts"] = {"n=6,k=2": 153, "n=6,unrestricted_nonidentity": 4095, "enumeration_checked_for_n_up_to": 5}
    # Separate supports: optimizing one block's total is not optimizing max cell hazard.
    optimized_total_touch = [floors[i] + b[i]**2 / floors[i] for i in range(2)]
    alternative_touch = [2 * x for x in b]
    assert max(optimized_total_touch) == R(41, 5) > max(alternative_touch)
    result["incidence_objective_counterexample"] = {"disjoint_support_axes": ["3", "4"], "total_optimal_floors_touch_rates": list(map(str, optimized_total_touch)), "floors_equal_axes_touch_rates": list(map(str, alternative_touch)), "conclusion": "Single-block total-rate optimum need not minimize maximum spatial touching rate"}
    result["checks_passed"] = True
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    (OUT / "EXACT_CASES.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks_passed": True, "one_qubit_cases": number, "unitary_cases": unitary_cases, "two_qubit_cases": len(multiqubit), "elapsed_seconds": result["elapsed_seconds"]}, indent=2))


if __name__ == "__main__":
    run()
