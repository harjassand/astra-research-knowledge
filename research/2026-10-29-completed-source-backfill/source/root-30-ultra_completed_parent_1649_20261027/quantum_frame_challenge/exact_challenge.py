#!/usr/bin/env python3
"""Exact qubit channel/instrument/process counterexamples and frame-size costs.

Stdlib Fraction only; no parent theorem/compiler imported.  Real Pauli J is
(-i)Y, whose conjugation is identical to that of Y.  Testing all real matrix
units also tests the complex-linear map on every complex input.
"""
from fractions import Fraction as F
from math import isqrt, ceil
from pathlib import Path
import json
import time


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def zero(n):
    return mat([[0] * n for _ in range(n)])


def ident(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def trans(a):
    return tuple(zip(*a))


def scale(q, a):
    return tuple(tuple(q * x for x in row) for row in a)


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(a, b))


def mul(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(r, col))
                       for col in trans(b)) for r in a)


def conj(u, a):
    return mul(mul(u, a), trans(u))


def kron(a, b):
    return tuple(tuple(a[i][j] * b[k][l]
                       for j in range(len(a)) for l in range(len(b)))
                 for i in range(len(a)) for k in range(len(b)))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def units(n):
    for i in range(n):
        for j in range(n):
            yield mat([[int(k == i and l == j) for l in range(n)]
                       for k in range(n)])


I = ident(2)
X = mat([[0, 1], [1, 0]])
J = mat([[0, -1], [1, 0]])
Z = mat([[1, 0], [0, -1]])
PAULI = (I, X, J, Z)


def probs(c, depolarizing=False):
    s = 1 / (2 * c - 1)
    p = [(1 - s) / 4] * 4
    p[0 if depolarizing else 2] = (1 + 3 * s) / 4
    assert sum(p) == 1 and min(p) >= 0
    return p


def mix(a, p):
    out = zero(len(a))
    for w, u in zip(p, PAULI):
        out = add(out, scale(w, conj(u, a)))
    return out


def mix2(a, p):
    out = zero(4)
    for i, u in enumerate(PAULI):
        for j, v in enumerate(PAULI):
            out = add(out, scale(p[i] * p[j], conj(kron(u, v), a)))
    return out


def phi_direct(a, c):
    return scale(1 / (2 * c - 1),
                 add(scale(c * trace(a), I), scale(-1, trans(a))))


def depol_direct(a, s):
    return add(scale(s, a), scale((1 - s) * trace(a) / 2, I))


def pt_b(a):
    return mat([[a[2 * i + l][2 * k + j]
                 for k in range(2) for l in range(2)]
                for i in range(2) for j in range(2)])


V = mat([[F(3, 5), 0, 0, -F(4, 5)],
         [0, 1, 0, 0], [0, 0, 1, 0],
         [F(4, 5), 0, 0, F(3, 5)]])
assert mul(V, trans(V)) == ident(4)
RHO0 = mat([[int(i == j == 0) for j in range(4)] for i in range(4)])
RHO = conj(V, RHO0)
SINGLET = mat([[0, 0, 0, 0], [0, F(1, 2), -F(1, 2), 0],
               [0, -F(1, 2), F(1, 2), 0], [0, 0, 0, 0]])
XX = kron(X, X)


def expectation(a, observable):
    return trace(mul(a, observable))


def exact_process_case(c, eta):
    p = probs(c)
    s = 1 / (2 * c - 1)
    for a in units(2):
        assert mix(a, p) == phi_direct(a, c)
        assert mix(a, p) == conj(J, depol_direct(a, s))
    # Completely observed Pauli branch plus inverse correction restores the
    # unknown input.  Equality on matrix units proves the whole channel.
    for a in units(2):
        corrected = zero(2)
        for w, u in zip(p, PAULI):
            corrected = add(corrected, scale(w, conj(trans(u), conj(u, a))))
        assert corrected == a
    # A five-outcome instrument: unobserved (?, weight1-eta), or one of four
    # Pauli flags (weight eta*p_j). Erasing all flags gives exactly Phi_c.
    for a in units(2):
        erased = scale(1 - eta, mix(a, p))
        for w, u in zip(p, PAULI):
            erased = add(erased, scale(eta * w, conj(u, a)))
        assert erased == mix(a, p)
    # Both flags known and locally corrected, retaining their union.  This
    # subnormalized outcome has input-independent probability eta^2.
    both = zero(4)
    for i, u in enumerate(PAULI):
        for j, v in enumerate(PAULI):
            uv = kron(u, v)
            branch = conj(uv, RHO)
            # No physical correction is needed for the obstruction: each
            # individually flagged branch is already entangled.
            rotated_witness = conj(uv, SINGLET)
            assert expectation(pt_b(branch), rotated_witness) == -F(12,25)
            restored = conj(trans(uv), branch)
            both = add(both, scale(eta * eta * p[i] * p[j], restored))
    assert both == scale(eta * eta, RHO)
    witness = expectation(pt_b(both), SINGLET)
    assert witness == -F(12, 25) * eta * eta < 0
    # Pauli labels repeated once, then reset. Their classical memory is not
    # exposed.  The same exact pair cancels on every unknown two-qubit input.
    for a in units(4):
        echo = zero(4)
        for i, u in enumerate(PAULI):
            for j, v in enumerate(PAULI):
                uv = kron(u, v)
                echo = add(echo, scale(p[i] * p[j], conj(uv, conj(uv, a))))
        assert echo == a
    fresh = mix2(mix2(RHO, p), p)
    echo_xx = expectation(RHO, XX)
    fresh_xx = expectation(fresh, XX)
    assert echo_xx == F(24, 25)
    assert fresh_xx == F(24, 25) * s**4
    # A one-qubit two-call Z diagnostic requires no entangling preparation.
    z0 = mat([[1, 0], [0, 0]])
    fresh_z = expectation(mix(mix(z0, p), p), Z)
    assert fresh_z == s * s
    # Partial flags after undoing the deterministic J and correcting observed
    # D_s Pauli errors: the averaged corrected channel is D_q.
    pd = probs(c, depolarizing=True)
    q = eta + (1 - eta) * s
    for a in units(2):
        corrected = add(scale(eta, a), scale(1 - eta, mix(a, pd)))
        assert corrected == depol_direct(a, q)
    lam = (1 - 3 * s * s) / 4
    assert lam > 0
    return {
        "c": str(c), "s": str(s), "eta": str(eta),
        "phi_pauli_probabilities_I_X_Y_Z": [str(x) for x in p],
        "flagged_branch_probability": str(trace(both)),
        "flagged_subnormalized_PT_witness": str(witness),
        "conditional_PT_witness": "-12/25",
        "every_individually_flagged_branch_entangled_without_feedback": True,
        "both_I_flag_probability_without_correction": str(eta*eta*p[0]*p[0]),
        "both_I_subnormalized_PT_witness": str(-F(12,25)*eta*eta*p[0]*p[0]),
        "expected_both_flag_attempts": str(1 / (eta * eta)),
        "fresh_two_call_XX": str(fresh_xx),
        "repeated_error_two_call_XX": str(echo_xx),
        "XX_expectation_gap": str(echo_xx - fresh_xx),
        "fresh_two_call_Z": str(fresh_z), "echo_two_call_Z": "1",
        "one_qubit_Z_expectation_gap": str(1 - fresh_z),
        "partial_flag_corrected_depolarizing_q": str(q),
        "corrected_averaged_EA_by_exact_q2_test": 3 * q * q <= 1,
        "isotropic_PT_minimum_lambda": str(lam),
        "universal_product_vertices_lower_bound": ceil(1 / (2 * lam)),
        "whole_channel_matrix_unit_checks": True,
    }


def near_threshold(bits):
    # c0=(1+sqrt3)/2.  This dyadic is strictly above c0, at distance<2^-bits.
    den = 1 << bits
    h = 1 << (bits - 1)
    root_floor = isqrt(3 * h * h)
    assert root_floor * root_floor < 3 * h * h < (root_floor + 1)**2
    c = F(h + root_floor + 1, den)
    assert (2 * c - 1)**2 > 3
    lam = (1 - 3 / (2 * c - 1)**2) / 4
    m = ceil(1 / (2 * lam))
    n = isqrt(m)
    n += n * n < m
    return {"dyadic_fractional_bits": bits, "c": str(c), "lambda": str(lam),
            "physical_product_vertices_M_at_least": m,
            "cartesian_equal_local_cardinality_N_at_least": n,
            "log2_M_floor": m.bit_length() - 1,
            "description_numerator_bits": c.numerator.bit_length(),
            "description_denominator_bits": c.denominator.bit_length()}


def instrument_data(c, eta):
    p = probs(c)
    branches = [{"label": "?", "map": "(1-eta)*Phi_c", "weight": str(1-eta)}]
    branches += [{"label": name, "map": "weight*Ad_P", "weight": str(eta*w),
                  "real_unitary": [[str(x) for x in row] for row in u]}
                 for name, w, u in zip(("I", "X", "Y", "Z"), p, PAULI)]
    return {"schema": "rational qubit instrument and two-use memory1",
            "c": str(c), "eta": str(eta),
            "rational_entangling_V": [[str(x) for x in row] for row in V],
            "input": "|00><00|", "branches": branches,
            "two_use_memory": {
                "per_active_qubit_classical_labels": 4,
                "clock_phase_labels": 2,
                "first_step": "draw P~p, store P, apply Ad_P",
                "second_step": "apply stored Ad_P, then reset label",
                "known_operation_schedule": "arbitrary rational U, identity",
                "net_channel": "Ad_U on every input, including external references",
                "fresh_environment_not_satisfied": True}}


def main():
    start = time.perf_counter()
    cases = [exact_process_case(c, F(1, 100)) for c in
             (F(3, 2), F(9, 5), F(2), F(10))]
    costs = [near_threshold(b) for b in (4, 8, 16, 32, 64, 128)]
    # Finite Bernoulli streams with at mostK fair bits have dyadic output
    # probabilities.  The exact rational1/3 example rules out bounded worst
    # random-bit cost; this is independent of physical realizability.
    assert F(1, 3).denominator & (F(1, 3).denominator - 1) != 0
    result = {"status": "exact abstract constructions; no physical acquisition",
              "source_theorem_used": "Lami-Huber2016 Thm7; not rediscovered",
              "process_cases": cases, "near_threshold_output_size": costs,
              "initial_state": "pure product; no external reference used by witness",
              "entangling_gate_has_only_rational_entries": True,
              "flag_access_and_memory_are_outside_root_compiler_model": True,
              "elapsed_seconds": time.perf_counter() - start}
    folder = Path(__file__).resolve().parent
    (folder / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    (folder / "INSTRUMENT.json").write_text(json.dumps(instrument_data(F(9, 5), F(1,100)), indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
