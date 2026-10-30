#!/usr/bin/env python3
"""Simulated chronological echoes and retained-history qualification.

The learner receives scalar reports only. Hidden matrices enter the synthetic
supplier and a separately labelled population check. Every arm starts afresh.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent


def main():
    states = np.asarray(list(itertools.product([-1.0, 1.0], repeat=3)))
    nstate = len(states)
    a = states[:, 0]
    label = (a > 0).astype(np.int64)
    raw_g = label.astype(float)
    f = 2.0 * raw_g
    mu = np.ones(nstate) / nstate
    lookup = {tuple(s.astype(int)): i for i, s in enumerate(states)}

    def involution(change):
        perm = []
        for s in states.astype(int):
            t = s.copy()
            change(t)
            perm.append(lookup[tuple(t)])
        mat = np.eye(nstate)[perm]
        assert np.array_equal(mat, mat.T)
        return mat

    swap = involution(lambda x: x.__setitem__([0, 1], x[[1, 0]]))
    cnot = involution(lambda x: x.__setitem__(1, x[1] * x[2]))
    tag_cnot = involution(lambda x: x.__setitem__(1, x[1] * x[0]))
    flip_a = involution(lambda x: x.__setitem__(0, -x[0]))
    flip_b = involution(lambda x: x.__setitem__(1, -x[1]))
    flip_c = involution(lambda x: x.__setitem__(2, -x[2]))
    eye = np.eye(nstate)
    pmat = {
        "S": swap, "C": cnot, "T": tag_cnot,
        "A": expm(0.83 * (flip_a - eye)),
        "B": expm(0.31 * (flip_b - eye) + 0.17 * (flip_c - eye)),
        "D": expm(0.53 * (flip_b - eye) + 0.29 * (cnot - eye)),
    }
    for p in pmat.values():
        assert np.max(np.abs(p - p.T)) < 2e-15
        assert np.min(p) >= -1e-15
        assert np.max(np.abs(p.sum(axis=1) - 1)) < 2e-15
    prefix = ("S", "C", "A", "T")
    reference = {0: ("D", "B", "D", "B", "D", "A"),
                 1: ("B", "D", "B", "D", "B", "A")}
    specs = [
        ("passive_wait_2", ("A",) * 2, ("A",) * 2),
        ("passive_wait_4", ("A",) * 4, ("A",) * 4),
        ("B_A", ("B", "A"), ("B", "A")),
        ("D_A", ("D", "A"), ("D", "A")),
        ("BB_A", ("B", "B", "A"), ("B", "B", "A")),
        ("DD_A", ("D", "D", "A"), ("D", "D", "A")),
        ("BD_A", ("B", "D", "A"), ("B", "D", "A")),
        ("DB_A", ("D", "B", "A"), ("D", "B", "A")),
        ("history_BD_DB", ("B", "D", "A"), ("D", "B", "A")),
        ("history_DB_BD", ("D", "B", "A"), ("B", "D", "A")),
        ("BDB_A", ("B", "D", "B", "A"), ("B", "D", "B", "A")),
        ("DBD_A", ("D", "B", "D", "A"), ("D", "B", "D", "A")),
        ("history_BDB_DBD", ("B", "D", "B", "A"), ("D", "B", "D", "A")),
        ("reference", reference[0], reference[1]),
    ]
    policies = {name: {0: w0, 1: w1} for name, w0, w1 in specs}
    costs = {name: len(w0) for name, w0, w1 in specs}
    assert all(len(w0) == len(w1) for _, w0, w1 in specs)
    q = np.asarray([0.5, 0.5])
    cdf = {name: np.cumsum(p, axis=1) for name, p in pmat.items()}
    for c in cdf.values():
        c[:, -1] = 1.0
    ledger = {"baseline_preparations": 0, "kernel_calls": 0,
              "visible_readings": 0, "echo_trials": 0,
              "normalization_trials": 0}

    def execute(x, word, rng):
        x = x.copy()
        for op in word:
            u = rng.random(len(x))
            x = np.sum(u[:, None] > cdf[op][x], axis=1)
            ledger["kernel_calls"] += len(x)
        return x

    def execute_policy(x, retained_r, policy, rng, reverse=False):
        out = x.copy()
        for r in (0, 1):
            idx = np.flatnonzero(retained_r == r)
            word = tuple(reversed(policy[r])) if reverse else policy[r]
            out[idx] = execute(x[idx], word, rng)
        return out

    def echo_report(policy_u, policy_v, n, rng):
        x0 = rng.integers(0, nstate, size=n)
        first = raw_g[x0]
        x = execute(x0, prefix, rng)
        retained_r = label[x].copy()
        x = execute_policy(x, retained_r, policy_u, rng)
        x = execute_policy(x, retained_r, policy_v, rng, reverse=True)
        match = (label[x] == retained_r)
        x = execute(x, tuple(reversed(prefix)), rng)
        report = first * match * raw_g[x] / q[retained_r]
        ledger["baseline_preparations"] += n
        ledger["visible_readings"] += 4 * n
        ledger["echo_trials"] += n
        assert report.min() >= 0 and report.max() <= 2
        return float(report.mean())

    # Pilot selection receives samples only; it has no confidence claim.
    pilot_rng = np.random.default_rng(2026103001201)
    pilot_n = 12000
    pilot_target = echo_report(reference, reference, pilot_n, pilot_rng)
    pilot = []
    for name, policy in policies.items():
        diag = echo_report(policy, policy, pilot_n, pilot_rng)
        cross = echo_report(policy, reference, pilot_n, pilot_rng)
        raw_distance = diag + pilot_target - 2 * cross
        pilot.append({"name": name, "cost_calls_after_prefix": costs[name],
                      "raw_D_estimate": raw_distance,
                      "nominal_D_estimate": 4 * raw_distance})
    pilot_qualified = [p for p in pilot if p["nominal_D_estimate"] <= 0.030]
    selected_row = min(pilot_qualified,
                       key=lambda p: (p["cost_calls_after_prefix"],
                                      p["nominal_D_estimate"]))
    selected_name = selected_row["name"]
    selected = policies[selected_name]
    pilot_ledger = ledger.copy()

    # Fresh validation, including an acquired visible normalizer.
    val_rng = np.random.default_rng(2026103001202)
    normalization_n = 200000
    zs = val_rng.integers(0, nstate, size=normalization_n)
    zhat = float(raw_g[zs].mean())
    ledger["baseline_preparations"] += normalization_n
    ledger["visible_readings"] += normalization_n
    ledger["normalization_trials"] += normalization_n
    alpha_total = 0.01
    alpha_each = alpha_total / 4
    z_radius = math.sqrt(math.log(2 / alpha_each) / (2 * normalization_n))
    z_lower = zhat - z_radius
    assert z_lower > 0
    validation_n = 1200000
    val_uu = echo_report(selected, selected, validation_n, val_rng)
    val_tt = echo_report(reference, reference, validation_n, val_rng)
    val_ut = echo_report(selected, reference, validation_n, val_rng)
    raw_dhat = val_uu + val_tt - 2 * val_ut
    entry_radius = 2.0 * math.sqrt(math.log(2 / alpha_each) / (2 * validation_n))
    raw_upper = max(0.0, raw_dhat + 4 * entry_radius)
    d_upper = raw_upper / z_lower**2
    tv_upper = min(1.0, math.sqrt(d_upper) / 2)
    requested_tv = 0.16
    certificate_passed = bool(tv_upper <= requested_tv)

    # The learner has stopped. Hidden matrices are used only in this
    # separately labelled population assessment, never to choose the word.
    def product(word):
        ans = eye.copy()
        for op in word:
            ans = ans @ pmat[op]
        return ans

    pp = product(prefix)
    project = {r: np.diag((label == r).astype(float)) for r in (0, 1)}
    branch = {r: pp @ project[r] for r in (0, 1)}
    raw_input = {r: branch[r].T @ raw_g for r in (0, 1)}

    def output(policy):
        return {r: product(policy[r]).T @ (2 * raw_input[r]) for r in (0, 1)}

    target_output = output(reference)

    def true_error(policy):
        out = output(policy)
        delta = {r: out[r] - target_output[r] for r in (0, 1)}
        d_joint = sum(float(np.mean(delta[r]**2)) / q[r] for r in (0, 1))
        tv = sum(float(np.mean(np.abs(delta[r]))) / 2 for r in (0, 1))
        return d_joint, tv

    true_selected_d, true_selected_tv = true_error(selected)
    population = []
    identity_residual = 0.0
    witness_residual = 0.0
    witness_scale = 4.0
    for name, policy in policies.items():
        out = output(policy)
        d, tv = true_error(policy)
        echo_distance = 0.0
        witness_gap = 0.0
        for r in (0, 1):
            u, v, ar = product(policy[r]), product(reference[r]), branch[r]
            kuu = float(mu @ (np.diag(f) @ ar @ u @ u.T @ ar.T @ f)) / q[r]
            ktt = float(mu @ (np.diag(f) @ ar @ v @ v.T @ ar.T @ f)) / q[r]
            kut = float(mu @ (np.diag(f) @ ar @ u @ v.T @ ar.T @ f)) / q[r]
            echo_distance += kuu + ktt - 2 * kut
            phi = 0.5 + (out[r] - target_output[r]) / (2 * witness_scale * q[r])
            assert phi.min() >= -1e-14 and phi.max() <= 1 + 1e-14
            witness_gap += float(np.mean((out[r] - target_output[r]) * phi))
        identity_residual = max(identity_residual, abs(d - echo_distance))
        witness_residual = max(witness_residual, abs(witness_gap - d / (2 * witness_scale)))
        population.append({"name": name, "joint_D_q": d, "true_joint_TV": tv,
                           "cost_calls_after_prefix": costs[name]})
    selected_output = output(selected)
    withheld_gap = sum(float(np.mean(np.maximum(selected_output[r] - target_output[r], 0)))
                       for r in (0, 1))
    assert abs(withheld_gap - true_selected_tv) < 1e-14
    assert identity_residual < 2e-13
    assert witness_residual < 2e-13

    result = {
        "scope": "Simulated chronological observations plus separate population checks; no hardware acquisition or total apparatus advantage.",
        "seed_pilot": 2026103001201,
        "seed_fresh_validation": 2026103001202,
        "state_count_in_supplier_only": nstate,
        "visible_label_count": 2,
        "retained_prefix": list(prefix),
        "candidate_count": len(policies),
        "learner_data": "Raw scalar echo means and baseline normalization samples only; no hidden state, matrix, density or exact-error access.",
        "pilot": pilot,
        "selected_policy": selected_name,
        "selected_words": {str(r): list(selected[r]) for r in (0, 1)},
        "reference_words": {str(r): list(reference[r]) for r in (0, 1)},
        "validation": {
            "trials_per_echo_entry": validation_n,
            "normalization_trials": normalization_n,
            "normalizer_estimate": zhat,
            "normalizer_lower_bound": z_lower,
            "raw_entries": {"uu": val_uu, "tt": val_tt, "ut": val_ut},
            "raw_distance_estimate": raw_dhat,
            "entry_radius": entry_radius,
            "normalized_distance_upper": d_upper,
            "joint_all_future_TV_upper": tv_upper,
            "requested_TV": requested_tv,
            "confidence": 1 - alpha_total,
            "passed": certificate_passed,
        },
        "population_check_after_selection": {
            "true_selected_joint_D_q": true_selected_d,
            "true_selected_joint_TV": true_selected_tv,
            "withheld_full_state_receiver_gap": withheld_gap,
            "echo_identity_max_residual": identity_residual,
            "literal_witness_max_residual": witness_residual,
            "all_candidates": population,
        },
        "ledger_pilot": pilot_ledger,
        "ledger_total": ledger,
        "ledger_limits": "Native calls are supplied fixed operations. Preparation/reset work, hardware sensing errors, communication, clocks and thermal-source capacity are not experimentally priced.",
        "retained_key_failure": {
            "one_use_marginal_TV": 0.0, "one_use_joint_TV": 0.5,
            "eight_use_joint_TV": 1 - 2**(-8),
            "marginal_squared_error": 0.0, "key_squared_error": 1.0},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT / "ENSEMBLE_ECHO_LEARNING_CHECK_RESULTS.json").write_text(
        json.dumps(result, indent=2) + "\n")
    summary = {"selected": selected_name, "validation": result["validation"],
               "true_joint_TV": true_selected_tv,
               "echo_identity_residual": identity_residual,
               "witness_residual": witness_residual,
               "ledger_total": ledger}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
