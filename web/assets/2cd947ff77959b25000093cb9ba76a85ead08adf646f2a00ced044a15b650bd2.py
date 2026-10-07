#!/usr/bin/env python3
"""Finite projected-binomial witnesses and an explicit coherent projector circuit.

Standard-library only; floating point output is numerical evidence, not an
interval certificate. The mathematical bounds are in energy_constructive.md.
Run: python3 work/deep/energy_constructive.py
"""
from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
import json
import math
from pathlib import Path


SQRT13 = math.sqrt(13.0)
ALPHA = (10.0 + 2.0 * SQRT13) / 3.0
P = (23.0 + 6.0 * SQRT13) / 61.0
S = (9.0 + 5.0 * SQRT13) / 61.0
H = (52.0 - 5.0 * SQRT13) / 61.0
ELL = (130.0 + 18.0 * SQRT13) / 61.0
V = 9.0 * P * (1.0 - P)
MU = (5.0 + 4.0 * SQRT13) / 3.0
DEPTH_C = min(MU * V / 216.0, 2.0 / 3.0 * math.log1p(V / 18.0))


def logsumexp(values):
    values = list(values)
    if not values:
        return -math.inf
    peak = max(values)
    if peak == -math.inf:
        return peak
    return peak + math.log(math.fsum(math.exp(x - peak) for x in values))


def binomial_logpmf(n, p=P):
    """O(n) stable recurrence, normalized in log space; no lgamma cancellation."""
    mode = min(n, int(math.floor((n + 1) * p)))
    logs = [-math.inf] * (n + 1)
    logs[mode] = 0.0
    odds = math.log(p / (1.0 - p))
    for k in range(mode, n):
        logs[k + 1] = logs[k] + math.log((n - k) / (k + 1)) + odds
    for k in range(mode, 0, -1):
        logs[k - 1] = logs[k] + math.log(k / (n - k + 1)) - odds
    normalization = logsumexp(logs)
    return [x - normalization for x in logs]


def interval(n, one_sided=False):
    tau = math.sqrt(2.0 * n * math.log(max(n, 2)))
    a = max(0, math.ceil(n * P - tau))
    b = n if one_sided else min(n, math.floor(n * P + tau))
    return a, b, tau


def witness(n, one_sided=False, save_state=False):
    a, b, tau = interval(n, one_sided)
    logs = binomial_logpmf(n)
    log_eta = logsumexp(logs[a:b + 1])
    log_fail = logsumexp(logs[:a] + logs[b + 1:])
    eta = math.exp(log_eta)
    prev = binomial_logpmf(n - 1)
    log_boundary_terms = []
    if b <= n - 1:
        log_boundary_terms.append(math.log1p(-P) + prev[b])
    if a > 0:
        log_boundary_terms.append(math.log(P) + prev[a - 1])
    log_boundary = logsumexp(log_boundary_terms)
    boundary_over_eta = math.exp(log_boundary - log_eta)
    cost = n * (H + S * boundary_over_eta)
    log_a = -n + logsumexp(logs[k] - 3.0 * k for k in range(a, b + 1)) - log_eta
    ratio = -log_a / cost
    delta_bound = (1.0 if one_sided else 2.0) * math.exp(-2.0 * tau * tau / n)
    m_ratio = max(P / (1.0 - P), (1.0 - P) / P)
    cost_per_site_upper = H + S * m_ratio * delta_bound / (1.0 - delta_bound)
    rate_lower = max(0.0, (ELL - 3.0 * tau / n) / cost_per_site_upper)
    record = {
        "n": n, "interval": [a, b], "type_coefficients": b - a + 1,
        "one_sided": one_sided, "tau": tau, "success_probability": eta,
        "log_failure_probability": log_fail, "failure_hoeffding_upper": delta_bound,
        "cost": cost, "cost_per_site": cost / n, "log_vacuum_overlap": log_a,
        "exponent_per_mean_cost": ratio, "alpha_minus_ratio": ALPHA - ratio,
        "rigorous_formula_lower_bound_evaluated_in_float": rate_lower,
        "minimum_L_eigenvalue": n + 3 * a,
    }
    if save_state:
        record["dicke_coefficients"] = [
            {"k": k, "real_amplitude": (-1.0 if k % 2 else 1.0) *
             math.exp(0.5 * (logs[k] - log_eta))}
            for k in range(a, b + 1)
        ]
        record["basis"] = "D^n_k is the normalized uniform sum of all excited-basis strings with k weight-4 symbols"
    return record


def controlled_counter_gates(n, counter, scratch):
    """Exact reversible popcount. Carry ancillas return to zero per increment."""
    m = len(counter)
    gates = []
    for data in range(n):
        carry = [data] + scratch[:m - 1]
        for j in range(m - 1):
            gates.append(("CCX", carry[j], counter[j], carry[j + 1]))
        for j in range(m):
            gates.append(("CX", carry[j], counter[j]))
        for j in range(m - 2, -1, -1):
            gates.append(("X", counter[j]))
            gates.append(("CCX", carry[j], counter[j], carry[j + 1]))
            gates.append(("X", counter[j]))
    return gates


def ge_threshold_gates(counter, scratch, output, threshold):
    """Compute output ^= (counter >= threshold), preserving input and scratch."""
    m = len(counter)
    if threshold <= 0:
        return [("X", output)]
    if threshold >= 1 << m:
        return []
    addend = (1 << m) - threshold
    carry = []
    for j in range(m):
        bit = (addend >> j) & 1
        if j == 0:
            if bit:
                carry.append(("CX", counter[0], scratch[0]))
        elif bit:
            carry.extend([
                ("CX", counter[j], scratch[j]),
                ("CX", scratch[j - 1], scratch[j]),
                ("CCX", counter[j], scratch[j - 1], scratch[j]),
            ])
        else:
            carry.append(("CCX", counter[j], scratch[j - 1], scratch[j]))
    return carry + [("CX", scratch[m - 1], output)] + list(reversed(carry))


def projector_circuit(n, a, b):
    m = max(1, n.bit_length())
    counter = list(range(n, n + m))
    scratch = list(range(n + m, n + 2 * m))
    ga, gb, accept = n + 2 * m, n + 2 * m + 1, n + 2 * m + 2
    count = controlled_counter_gates(n, counter, scratch)
    g_a = ge_threshold_gates(counter, scratch, ga, a)
    g_b = ge_threshold_gates(counter, scratch, gb, b + 1)
    membership = g_a + g_b + [
        ("X", gb), ("CCX", ga, gb, accept), ("X", gb)
    ] + list(reversed(g_b)) + list(reversed(g_a))
    classical_gates = count + membership + list(reversed(count))
    gate_counts = {
        kind: sum(g[0] == kind for g in classical_gates)
        for kind in ("X", "CX", "CCX")
    }
    return {
        "n": n, "interval": [a, b], "counter_bits": m,
        "clean_ancilla_qubits": 2 * m + 3, "register_qubits": n + 2 * m + 3,
        "data_qubits": list(range(n)), "counter_qubits": counter,
        "scratch_qubits": scratch, "accept_qubit": accept,
        "count_gates": count, "membership_gates": membership,
        "after_membership": "Measure only accept; on success apply reversed(count_gates). Never measure counter.",
        "reversible_gate_counts_including_count_uncompute": gate_counts,
        "initial_rotations": n,
    }


def apply_gates(bits, gates):
    for gate in gates:
        if gate[0] == "X":
            bits[gate[1]] ^= 1
        elif gate[0] == "CX":
            bits[gate[2]] ^= bits[gate[1]]
        elif gate[0] == "CCX":
            bits[gate[3]] ^= bits[gate[1]] & bits[gate[2]]
        else:
            raise ValueError(gate)


def validate_counter_and_membership():
    checked = 0
    for n in range(1, 11):
        a, b, _ = interval(n)
        # Nontrivial thresholds ensure that all comparator branches are tested,
        # including intervals not used by the wide small-n typical window.
        for a, b in {(a, b), (0, n), (n // 3, 2 * n // 3), (n, n)}:
            circ = projector_circuit(n, a, b)
            for word in range(1 << n):
                bits = [(word >> j) & 1 for j in range(n)] + [0] * circ["clean_ancilla_qubits"]
                k = word.bit_count()
                apply_gates(bits, circ["count_gates"])
                actual = sum(bits[q] << j for j, q in enumerate(circ["counter_qubits"]))
                assert actual == k
                apply_gates(bits, circ["membership_gates"])
                assert bits[circ["accept_qubit"]] == (a <= k <= b)
                assert all(bits[q] == 0 for q in circ["scratch_qubits"])
                apply_gates(bits, reversed(circ["count_gates"]))
                assert all(bits[q] == 0 for q in range(n, circ["register_qubits"]) if q != circ["accept_qubit"])
                assert bits[:n] == [(word >> j) & 1 for j in range(n)]
                checked += 1
    return checked


def validate_full_vectors():
    max_cost_error = max_log_overlap_error = 0.0
    checked = 0
    for n in range(1, 11):
        for one_sided in (False, True):
            rec = witness(n, one_sided)
            a, b = rec["interval"]
            eta = rec["success_probability"]
            vec = [
                (-1.0 if word.bit_count() % 2 else 1.0) *
                math.sqrt((1.0 - P) ** (n - word.bit_count()) * P ** word.bit_count() / eta)
                if a <= word.bit_count() <= b else 0.0
                for word in range(1 << n)
            ]
            assert abs(math.fsum(x * x for x in vec) - 1.0) < 1e-12
            overlap = math.fsum(x * x * math.exp(-n - 3 * word.bit_count()) for word, x in enumerate(vec))
            cost = n + 0.5 * math.fsum(
                vec[word] * vec[word ^ (1 << j)]
                for word in range(1 << n) for j in range(n)
            )
            max_cost_error = max(max_cost_error, abs(cost - rec["cost"]))
            max_log_overlap_error = max(max_log_overlap_error, abs(math.log(overlap) - rec["log_vacuum_overlap"]))
            checked += 1
    assert max_cost_error < 2e-11
    assert max_log_overlap_error < 2e-11
    return {"cases": checked, "max_cost_error": max_cost_error,
            "max_log_overlap_error": max_log_overlap_error}


def decimal_reference(n):
    with localcontext() as ctx:
        ctx.prec = 80
        d = Decimal
        sqrt13 = d(13).sqrt()
        p = (d(23) + d(6) * sqrt13) / d(61)
        s = (d(9) + d(5) * sqrt13) / d(61)
        a, b, _ = interval(n)
        binom = [d(math.comb(n, k)) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
        eta = sum(binom[a:b + 1], d(0))
        gamma = sum((d(math.comb(n - 1, k)) * p ** k * (1 - p) ** (n - 1 - k)
                     for k in range(a, min(b, n))), d(0))
        cost = d(n) * (1 - s * gamma / eta)
        overlap = sum((binom[k] * (-d(n + 3 * k)).exp() for k in range(a, b + 1)), d(0)) / eta
        return {"n": n, "precision_decimal_digits": 80,
                "cost": str(cost), "log_vacuum_overlap": str(overlap.ln()),
                "exponent_per_mean_cost": str(-overlap.ln() / cost)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    constants = {"alpha": ALPHA, "p": P, "s": S, "h": H, "ell": ELL,
                 "variance_v": V, "gap_mu": MU, "depth_gap_constant_c": DEPTH_C,
                 "ell_minus_alpha_h": ELL - ALPHA * H}
    table = [witness(n) for n in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
                                  1024, 2048, 4096, 16384, 65536, 262144]]
    decimal = [decimal_reference(n) for n in (16, 64, 128)]
    for ref in decimal:
        rec = witness(ref["n"])
        assert abs(float(ref["cost"]) - rec["cost"]) < 2e-11
        assert abs(float(ref["log_vacuum_overlap"]) - rec["log_vacuum_overlap"]) < 2e-11
    validations = {
        "classical_counter_and_membership_basis_cases": validate_counter_and_membership(),
        "full_excited_state_vectors": validate_full_vectors(),
        "decimal_reference": decimal,
        "scope": "Checks validate formulas and exact reversible classical gate action; no quantum hardware run or universal rotation compiler is claimed.",
    }
    result = {"constants": constants, "witness_table": table, "validation": validations}
    (args.outdir / "energy_constructive_results.json").write_text(json.dumps(result, indent=2) + "\n")
    state = witness(256, save_state=True)
    (args.outdir / "energy_constructive_witness_n256.json").write_text(json.dumps(state, indent=2) + "\n")
    a, b, _ = interval(16)
    circuit = projector_circuit(16, a, b)
    (args.outdir / "energy_constructive_projector_n16.json").write_text(json.dumps(circuit, indent=2) + "\n")
    print(json.dumps(constants, indent=2))
    print("n       coeffs   ratio             gap               log_overlap")
    for row in table:
        print(f'{row["n"]:<7d} {row["type_coefficients"]:<8d} '
              f'{row["exponent_per_mean_cost"]:.12f}  '
              f'{row["alpha_minus_ratio"]:.6g}  {row["log_vacuum_overlap"]:.6g}')
    print(json.dumps(validations, indent=2))


if __name__ == "__main__":
    main()
