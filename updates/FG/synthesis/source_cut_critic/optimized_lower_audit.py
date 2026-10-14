#!/usr/bin/env python3
"""Audit rationalized root trial fields without importing root scientific code.

The source matrices are reconstructed from the supplied four-bit law, exact
field energies are evaluated directly, and every distinct full-box vertex is
compared with all sixteen-coordinate threshold prefixes.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import time

from independent_audit import check_spd, invert, mv, dot, quad, lower_scan

BASE = Path(__file__).resolve().parent
ROOT_INPUT = BASE.parent / "FG-root" / "OPTIMIZED_LOWER_CERTIFICATES.json"
SOURCE_SCRIPT = BASE.parent / "FG-sources" / "compact" / "conditional_envelope.py"


def source_form(feature, R):
    n, N = 4, 16
    q, softness = F(1, 26), F(1, 10000)
    mass = [q ** state.bit_count() * (1 - q) ** (n - state.bit_count())
            for state in range(N)]
    def feature_value(state):
        if feature == "all_open":
            return int(state == N - 1)
        if feature == "first_open":
            return state & 1
        if feature == "all_closed":
            return int(state == 0)
        raise ValueError(feature)
    weight = [F(1 + (R - 1) * feature_value(state)) for state in range(N)]
    Aplus = [[F(0) for _ in range(N)] for _ in range(N)]
    for state in range(N):
        reaction_factor = F(1) if state & 8 else softness
        Aplus[state][state] += mass[state] * weight[state] * q * reaction_factor
        for bit in range(n):
            if state & (1 << bit):
                continue
            other = state | (1 << bit)
            gate_factor = F(1) if bit == 0 or state & (1 << (bit - 1)) else softness
            conductance = mass[state] * q * gate_factor * min(weight[state], weight[other])
            Aplus[state][state] += conductance
            Aplus[other][other] += conductance
            Aplus[state][other] -= conductance
            Aplus[other][state] -= conductance
    check_spd(Aplus)
    ell = mass
    u = [x * y for x, y in zip(mass, weight)]
    return Aplus, ell, u


def audit_row(row, prior):
    feature, R = row["feature"], row["R"]
    Aplus, ell, u = source_form(feature, R)
    v = [F(x["exact"]) for x in row["dyadic_field"]]
    assert len(v) == len(ell) == row["retained_states"] == 16
    assert all(x.denominator & (x.denominator - 1) == 0 for x in v)
    energy = quad(Aplus, v)
    assert energy == F(row["exact_energy"]["exact"])
    L, prefix_witness, best_prefix = lower_scan(ell, u, v, energy)
    assert L == F(row["optimized_trial_lower"]["exact"])
    # Independently evaluate all n+1 prefixes directly, not by scan updates.
    order = sorted(range(16), key=lambda i: (2 * v[i], i))
    prefix_values = []
    for k in range(17):
        selected = set(order[:k])
        s = [u[i] if i in selected else ell[i] for i in range(16)]
        prefix_values.append((2 * dot(s, v) - energy) / sum(s))
    assert min(prefix_values) == L
    # Fixed-width coordinates create only duplicates in a 2^16 enumeration.
    # Enumerating the uncertain coordinates covers every distinct box vertex.
    active = [i for i in range(16) if ell[i] != u[i]]
    vertex_values = []
    direct_witnesses = []
    for bits in product((0, 1), repeat=len(active)):
        s = list(ell)
        for i, bit in zip(active, bits):
            if bit:
                s[i] = u[i]
        value = (2 * dot(s, v) - energy) / sum(s)
        vertex_values.append(value)
        if value == L:
            direct_witnesses.append(list(map(str, s)))
    assert min(vertex_values) == L
    assert list(map(str, prefix_witness)) in direct_witnesses
    threshold_residual = -energy + sum((min((2 * vi - L) * lo, (2 * vi - L) * hi)
        for vi, lo, hi in zip(v, ell, u)), F(0))
    assert threshold_residual == 0
    # Recompute the fallback field energy and lower bound from Aplus itself.
    baseline_v = mv(invert(Aplus), ell)
    baseline_energy = quad(Aplus, baseline_v)
    assert baseline_energy == dot(ell, baseline_v)
    baseline_L, _, _ = lower_scan(ell, u, baseline_v, baseline_energy)
    assert baseline_L == F(row["original_fixed_trial_lower"]["exact"])
    assert baseline_L == F(prior["fixed_trial_lower"])
    accepted = max(L, baseline_L)
    assert accepted == F(row["accepted_lower"]["exact"])
    upper = F(prior["upper"])
    assert upper == F(row["cut_upper"]["exact"])
    ratio = upper / accepted
    assert ratio == F(row["accepted_ratio"]["exact"])
    return {"feature": feature, "R": R, "retained_states": 16,
        "uncertain_sources": len(active), "distinct_vertices_checked": len(vertex_values),
        "all_coordinate_prefixes_checked": len(prefix_values),
        "exact_field_energy": str(energy), "exact_optimized_trial_lower": str(L),
        "exact_baseline_lower": str(baseline_L), "exact_accepted_lower": str(accepted),
        "exact_cut_upper": str(upper), "exact_accepted_ratio": str(ratio),
        "accepted_ratio_decimal": float(ratio), "accepted_lower_decimal": float(accepted),
        "accepted_field": "optimized_rational" if L > baseline_L else "original_exact",
        "optimized_minus_original": str(L - baseline_L),
        "exact_threshold_residual": str(threshold_residual),
        "best_prefix_length": best_prefix, "source_witness": list(map(str, prefix_witness)),
        "all_direct_prefix_ratios": list(map(str, prefix_values)),
        "positive_field_entries": all(x >= 0 for x in v),
        "field_max_numerator_bits": max(abs(x.numerator).bit_length() for x in v),
        "field_max_denominator_bits": max(x.denominator.bit_length() for x in v),
        "scope": "Exact valid rational variational lower certificate; no exact convex optimality claim."}


def main(root_input=ROOT_INPUT, source_script=SOURCE_SCRIPT):
    started = time.time()
    input_bytes = root_input.read_bytes()
    root = json.loads(input_bytes)
    prior_path = BASE / "independent_results.json"
    prior_bytes = prior_path.read_bytes()
    prior = {(x["feature"], x["R"]): x for x in json.loads(prior_bytes)["source_cases"]}
    rows = [audit_row(row, prior[row["feature"], row["R"]]) for row in root["rows"]]
    assert len(rows) == 6
    report = {"status": "PASS", "input_path": str(root_input),
        "input_sha256": sha256(input_bytes).hexdigest(),
        "source_script_sha256": sha256(source_script.read_bytes()).hexdigest() if source_script.exists() else None,
        "prior_critic_results_sha256": sha256(prior_bytes).hexdigest(),
        "rows_checked": len(rows),
        "exact_field_energies_checked": len(rows),
        "all_coordinate_prefixes_checked": sum(x["all_coordinate_prefixes_checked"] for x in rows),
        "distinct_box_vertices_checked": sum(x["distinct_vertices_checked"] for x in rows),
        "equivalent_unreduced_vertex_evaluations": len(rows) * (1 << 16),
        "accepted_optimized_fields": sum(x["accepted_field"] == "optimized_rational" for x in rows),
        "accepted_exact_fallback_fields": sum(x["accepted_field"] == "original_exact" for x in rows),
        "optimizer_float_values_used_as_premises": False,
        "elapsed_seconds": time.time() - started,
        "scope": "Exact finite rational energy, source normalization, prefix minimum, exhaustive distinct vertices, fallback selection and ratio verification.",
        "rows": rows}
    (BASE / "OPTIMIZED_LOWER_AUDIT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
    print(json.dumps([{k: x[k] for k in ("feature", "R", "accepted_field", "accepted_lower_decimal", "accepted_ratio_decimal")}
        for x in rows], indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificates", type=Path, default=ROOT_INPUT)
    parser.add_argument("--source-script", type=Path, default=SOURCE_SCRIPT)
    args = parser.parse_args()
    main(args.certificates, args.source_script)
