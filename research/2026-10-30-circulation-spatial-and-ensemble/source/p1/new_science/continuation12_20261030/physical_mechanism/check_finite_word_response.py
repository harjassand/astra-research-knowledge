"""Finite-word FDT acquisition, real finite-step validation, and exact boundary.

Synthetic hidden-state operation supplier; no laboratory claim.
The learner sees only four-valued visible boundary records. Hidden states
persist during each word. Independent stationary preparation is paid per word.
Population matrices are used only for supplier construction and independent
verification, never by the direction-selection or confidence calculation.
"""
from pathlib import Path
import hashlib
import itertools
import json
import math

import numpy as np
from scipy.linalg import expm, expm_frechet

OUT = Path(__file__).resolve().parent
RECORDS = OUT / "response_records_final"
RECORDS.mkdir(exist_ok=True)
RNG = np.random.default_rng(2026103013)

states = np.array(list(itertools.product((-1.0, 1.0), repeat=3)))
visible = ((states[:, 0] > 0).astype(np.uint8) * 2
           + (states[:, 1] > 0).astype(np.uint8))
vstates = np.array(list(itertools.product((-1.0, 1.0), repeat=2)))
Bvis = np.stack((vstates[:, 0], vstates[:, 1],
                 vstates[:, 0] * vstates[:, 1]))
Fvis = 0.6 * vstates[:, 0] + 0.4 * vstates[:, 1]
Fs = Fvis[visible]
U = (0.25 * states[:, 0] * states[:, 2]
     + 0.4 * states[:, 1] * states[:, 2]
     + 0.15 * states[:, 0] * states[:, 1]
     + 0.17 * states[:, 0] + 0.11 * states[:, 2])
pi = np.exp(-U)
pi /= pi.sum()
times = np.array((0.2, 0.35, 0.6))


def operation(k, h=0.0):
    """Unknown reciprocal prefactor changes with h as well as Gibbs energy."""
    q = np.zeros((8, 8))
    dq = np.zeros_like(q)
    B = Bvis[k, visible]
    for i in range(8):
        for j in range(i + 1, 8):
            pref = 0.10 + 0.025 * (((i + 1) * (j + 1) + 3 * k) % 11)
            eta = 0.2 * math.cos((i + j + 1) * (k + 1))
            for x, y in ((i, j), (j, i)):
                score = eta + (B[y] - B[x]) / 2
                q[x, y] = pref * math.exp((U[x] - U[y]) / 2 + h * score)
                dq[x, y] = q[x, y] * score
    np.fill_diagonal(q, -q.sum(axis=1))
    np.fill_diagonal(dq, -dq.sum(axis=1))
    P, dP = expm_frechet(times[k] * q, times[k] * dq)
    return q, P, dP


def kernel_only(k, h):
    return operation(k, h)[1]


ops = [operation(k) for k in range(3)]
P0 = [z[1] for z in ops]
dP0 = [z[2] for z in ops]


def word_matrix(h):
    W = np.eye(8)
    for k in range(3):
        W = W @ kernel_only(k, h[k])
    return W


def sample_visible_word(kernels, n):
    x = RNG.choice(8, size=n, p=pi)
    Y = np.empty((n, 4), dtype=np.uint8)
    Y[:, 0] = visible[x]
    for k, P in enumerate(kernels):
        assert P.min() > -1e-12
        cdf = np.cumsum(P[x], axis=1)
        cdf[:, -1] = 1.0
        x = (RNG.random(n)[:, None] > cdf).sum(axis=1)
        Y[:, k + 1] = visible[x]
    return Y


def save_record(name, Y, h):
    p = RECORDS / name
    np.savez_compressed(p, visible_boundary_labels=Y,
                        prescribed_controls=np.asarray(h),
                        stage_durations=times)
    return {"path": str(p.relative_to(OUT)),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "bytes": p.stat().st_size,
            "episodes": len(Y), "native_calls": 3 * len(Y),
            "visible_label_reads": 4 * len(Y)}


gradient = []
correlation_gradient = []
for k in range(3):
    prefix = np.eye(8)
    suffix = np.eye(8)
    for j in range(k):
        prefix = prefix @ P0[j]
    for j in range(k + 1, 3):
        suffix = suffix @ P0[j]
    gradient.append(float(pi @ prefix @ dP0[k] @ suffix @ Fs))
    B = Bvis[k, visible]
    correlation_gradient.append(
        float((pi * B) @ (np.eye(8) - P0[k]) @ suffix @ Fs))
gradient = np.array(gradient)
correlation_gradient = np.array(correlation_gradient)
identity_error = float(np.max(np.abs(gradient - correlation_gradient)))
assert identity_error < 2e-14
stationarity_error = max(float(np.max(np.abs(pi @ P - pi))) for P in P0)
reciprocity_error = max(float(np.max(np.abs(pi[:, None] * P
                                          - P.T * pi[None, :]))) for P in P0)
commutator = float(np.linalg.norm(P0[0] @ P0[1] - P0[1] @ P0[0]))
assert commutator > 1e-3

# Complete actual boundary records supply all three gradients.
pilot_n = 100_000
alpha_pilot = 0.005
pilot = sample_visible_word(P0, pilot_n)
Z = np.column_stack([
    Fvis[pilot[:, -1]] * (Bvis[k, pilot[:, k + 1]] - Bvis[k, pilot[:, k]])
    for k in range(3)])
ghat = Z.mean(axis=0)
radius = math.sqrt(8 * math.log(2 * 3 / alpha_pilot) / pilot_n)
selected = int(np.argmax(np.abs(ghat)))
direction = np.zeros(3)
direction[selected] = -np.sign(ghat[selected])
descent_lower = float(-ghat @ direction - radius)
assert descent_lower > 0
records = [save_record("pilot_visible.npz", pilot, np.zeros(3))]

# Actual independent finite-amplitude trials, no counterfactual copying.
validation = []
alpha_val = 0.005
for j in range(1, 9):
    lam = 2.0 ** (-j)
    h = lam * direction
    sum_difference = 0.0
    val_n = 0
    # Confidence is simultaneous over both amplitude rounds and precision
    # looks. Stop early if a finite decrease is already certified; otherwise
    # obtain the declared shrinking precision before reducing the amplitude.
    for look in range(1, 15):
        batch_n = 50_000 * 2 ** (look - 1)
        ref = sample_visible_word(P0, batch_n)
        candidate = sample_visible_word(
            [kernel_only(k, h[k]) for k in range(3)], batch_n)
        sum_difference += float((Fvis[candidate[:, -1]] - Fvis[ref[:, -1]]).sum())
        val_n += batch_n
        alpha_j = (36 * alpha_val /
                   (math.pi ** 4 * j ** 2 * look ** 2))
        rad_j = math.sqrt(8 * math.log(2 / alpha_j) / val_n)
        estimate = sum_difference / val_n
        accepted = estimate + rad_j < -descent_lower * lam / 4
        records.append(save_record(
            f"validation_{j}_look_{look}_reference.npz", ref, np.zeros(3)))
        records.append(save_record(
            f"validation_{j}_look_{look}_candidate.npz", candidate, h))
        validation.append({
            "round": j, "precision_look": look, "cumulative_episodes_per_arm": val_n,
            "lambda": lam, "controls": h.tolist(),
            "difference_estimate": estimate, "confidence_radius": rad_j,
            "certified_decrease": max(0.0, -estimate - rad_j),
            "acceptance_threshold": -descent_lower * lam / 4,
            "accepted": bool(accepted),
            "population_difference_for_check_only": float(pi @ word_matrix(h) @ Fs - pi @ Fs)})
        if accepted or rad_j <= descent_lower * lam / 8:
            break
    if accepted:
        break
assert validation[-1]["accepted"]

# Concrete failure of extension to retained histories/second order.
x = np.array((-1.0, 1.0))
c0, amplitude, frequency, t = 0.7, 0.2, 11.0, 0.8
cpp = amplitude * frequency
q = np.array(((-c0, c0), (c0, -c0)))
dq = np.zeros((2, 2))
for i in range(2):
    dq[i, 1-i] = cpp - c0 * x[i]
    dq[i, i] = -dq[i, 1-i]
Pt, dPt = expm_frechet(t * q, t * dq)
uniform = np.array((0.5, 0.5))
endpoint_derivative = float(uniform @ dPt @ x)
path_derivative = float((uniform * x) @ dPt @ x)
formula_endpoint = 1 - math.exp(-2 * c0 * t)
formula_path = -2 * cpp * t * math.exp(-2 * c0 * t)
conditional = dPt @ x
formula_conditional = formula_endpoint - 2 * x * cpp * t * math.exp(-2 * c0 * t)
assert abs(endpoint_derivative - formula_endpoint) < 1e-14
assert abs(path_derivative - formula_path) < 1e-14
assert np.max(np.abs(conditional - formula_conditional)) < 1e-14
assert abs(path_derivative) > 1

result = {
    "scope": "Synthetic operation sampling and population checks, not a physical assay.",
    "supplier": {"microscopic_states": 8, "visible_labels": 4,
                 "hidden_states_per_visible_label": 2,
                 "actual_stage_durations": times.tolist(),
                 "word_duration": float(times.sum()),
                 "unknown_h_dependent_reciprocal_prefactors": True},
    "population_checks": {
        "stationarity_error": stationarity_error,
        "reciprocity_error": reciprocity_error,
        "noncommutation_frobenius_norm": commutator,
        "frechet_derivative_gradient": gradient.tolist(),
        "chronological_correlation_gradient": correlation_gradient.tolist(),
        "identity_error": identity_error},
    "acquired": {"pilot_episodes": pilot_n,
                 "gradient_estimate": ghat.tolist(),
                 "simultaneous_radius": radius,
                 "pilot_failure_budget": alpha_pilot,
                 "selected_direction": direction.tolist(),
                 "certified_directional_descent_lower": descent_lower,
                 "validation_failure_budget": alpha_val,
                 "validation": validation},
    "boundary": {"c0": c0, "c_prime_0": cpp, "time": t,
                 "endpoint_first_derivative": endpoint_derivative,
                 "two_time_record_first_derivative": path_derivative,
                 "endpoint_second_derivative": 4 * cpp * t * math.exp(-2 * c0 * t),
                 "conditional_endpoint_derivatives": conditional.tolist(),
                 "all_static_biased_laws_same_for_c_plus_and_c_minus": True},
    "records": records,
    "total_cost": {
        "warranted_baseline_preparations": sum(r["episodes"] for r in records),
        "native_stage_calls": sum(r["native_calls"] for r in records),
        "visible_label_reads": sum(r["visible_label_reads"] for r in records),
        "summed_native_elapsed_time": float(times.sum()) * sum(r["episodes"] for r in records),
        "unpriced_actual_costs": [
            "baseline preparation implementation/time/work",
            "physical sensing/backaction and calibration",
            "clocks, randomness, controller memory, thermal noise and switching"]}}
(OUT / "FINITE_WORD_RESPONSE_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
