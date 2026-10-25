"""Received-only replay, output integrity and paired information-gain check."""
from fractions import Fraction as F
from hashlib import sha256
from math import log
from pathlib import Path
import json
import sys
import numpy as np
from adaptive_terminal_observer import replay

HERE = Path(__file__).resolve().parent
COMMUNICATION = HERE.parent / "communication"
sys.path.insert(0, str(COMMUNICATION))
from observe_transmission import CHAR, popcount, tail


def main():
    protocol_path = HERE / "adaptive_transmission_protocol.json"
    model_path = COMMUNICATION / "acquired_soft_weights.json"
    record_path = HERE / "received_adaptive_validation.npz"
    protocol = json.loads(protocol_path.read_text())
    model = json.loads(model_path.read_text())
    assert protocol["calibration_weight_sha256"] == sha256(model_path.read_bytes()).hexdigest()
    epsilon = F(protocol["remaining_perfect_information_epsilon"])
    with np.load(record_path) as record:
        final, first, reasons, gaps = replay(record, model, epsilon, protocol["max_inner_read_rounds"])
        rounds = record["read_rounds"].copy()
        axis = record["axis"].copy()
        positions = record["payload_positions"].copy()
        accepted_record = record["accepted"].copy()
        outer_length = protocol["validation_audit_length"]
        pre = 1 - 2 * (popcount(record["pre_words"]) > outer_length // 2).astype(np.int8)
        post = 1 - 2 * (popcount(record["post_words"]) > outer_length // 2).astype(np.int8)
    block = protocol["packet_length"]
    audit = np.ones((len(positions), block), dtype=bool)
    audit[np.arange(len(positions)), positions] = False
    accepted = np.all((pre == post).reshape(len(positions), block) | ~audit, axis=1)
    assert np.array_equal(accepted, accepted_record)
    audit = audit.ravel()
    n = int(audit.sum())
    raw = pre * post * CHAR[final, axis]
    paired = ((CHAR[final, axis] - CHAR[first, axis]) * raw // 2)[audit]
    assert np.all(np.isin(paired, [-1, 0, 1]))
    signed_sum = int(paired.astype(np.int64).sum())
    squares = int(np.dot(paired.astype(np.int64), paired.astype(np.int64)))
    eta = F(protocol["eta"])
    gamma = (1 - 2 * tail(eta, outer_length)) ** 2
    a = (1 + gamma) / 2
    b = (1 - gamma / 3) / 2
    assert b / a <= F(1, 2)
    sharp_weight = a ** (block - 1) / block
    lambdas = [F(1, 2 ** power) for power in range(1, 9)]
    bounds = [(F(3, 2) / (gamma * n)) * (signed_sum - lam * squares - F(67, 10) / lam)
              for lam in lambdas]
    selected = max(range(len(lambdas)), key=lambda index: bounds[index])
    rational_lower = bounds[selected]
    short_lower = F((rational_lower * 10000).__floor__(), 10000)
    exact_modeled_regret = epsilon + 6 * tail(eta, protocol["max_inner_read_rounds"])
    result = {
        "record_only": True,
        "native_model_hidden_errors_or_memory_read": False,
        "exact_control_replayed_calls": len(final),
        "unperformed_observations_used": False,
        "all_noncap_stops_satisfy_exact_value_test": True,
        "capped_calls": int(reasons.sum()),
        "largest_remaining_modeled_value_on_noncap_calls": float(gaps[reasons == 0].max()),
        "largest_remaining_modeled_value_on_cap_calls": float(gaps[reasons != 0].max()) if np.any(reasons) else None,
        "actual_inner_weak_marks": 6 * int(rounds.sum()),
        "mean_inner_weak_marks_exact": str(F(6 * int(rounds.sum()), len(final))),
        "mean_inner_weak_marks_display": 6 * int(rounds.sum()) / len(final),
        "modeled_perfect_syndrome_excess_risk_bound_exact": str(exact_modeled_regret),
        "modeled_perfect_syndrome_excess_risk_bound_display": float(exact_modeled_regret),
        "modeled_bound_scope": "For any fixed positive task-weight model and declared terminal QND kernel. It is not a bound on an unknown future physical memory's conditional error.",
        "fresh_output_integrity": {
            "attempted_payloads": len(positions),
            "accepted_payloads": int(accepted.sum()),
            "accepted_error_weight_upper_exact": str(F(1, block)),
            "sharp_weight_display": float(sharp_weight),
            "conditioning_rule": "Accepted error weight, not conditional1/64 error. Divide by actual acceptance probability only under the governing independent-input/reference scope; no fine-word certainty."},
        "received_only_first_round_vs_final_gain": {
            "audited_calls": n,
            "payloads_excluded": len(positions),
            "audit_calls_with_different_actions": int(np.count_nonzero((final != first)[audit])),
            "signed_sum": signed_sum,
            "sum_squares": squares,
            "gain_estimate": 3 * signed_sum / (2 * float(gamma) * n),
            "first_round_risk_estimate": .75 * (1 - float(np.mean((raw * CHAR[first, axis])[audit])) / float(gamma)),
            "final_risk_estimate": .75 * (1 - float(np.mean((raw * CHAR[final, axis])[audit])) / float(gamma)),
            "failure_probability": "1/100",
            "predeclared_lambda_count": 8,
            "selected_lambda": str(lambdas[selected]),
            "rational_log_800_upper": "67/10",
            "exact_gain_lower": str(rational_lower),
            "gain_lower_display": float(rational_lower),
            "short_gain_lower_exact": str(short_lower),
            "short_gain_lower_display": float(short_lower),
            "scope": "Mean predictable first-round-minus-final risk on actual audited histories. The first-round rule uses only an actually received prefix; no missing readout is invented. No payload-specific or future-history gain follows."},
        "strong_conventional_comparator": "An equally informed conventional active Bayesian observer uses the same exact weights, stop criterion and physical operations and makes identical decisions.",
        "probe_budget_comparison_scope": "The uniform15/35 figures are nominal probe budgets for this many calls, not counterfactual outcomes computed from unperformed measurements.",
        "received_record_sha256": sha256(record_path.read_bytes()).hexdigest(),
        "protocol_sha256": sha256(protocol_path.read_bytes()).hexdigest(),
        "acquired_weight_sha256": sha256(model_path.read_bytes()).hexdigest(),
    }
    (HERE / "adaptive_received_certificate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
