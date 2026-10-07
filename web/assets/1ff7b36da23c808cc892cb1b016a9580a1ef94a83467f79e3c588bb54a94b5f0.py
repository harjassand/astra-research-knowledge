"""Finite diagnostics for the causal-inference scout; no theorem certification.

Run with python3 work/scouts/causal_inference_check.py.
Only NumPy and the standard library are required.
"""

from itertools import combinations, permutations
from math import comb
import json
from pathlib import Path
import numpy as np


def norm(a):
    return float(np.linalg.norm(a, 2))


def projector(a, tol=1e-8):
    vals, vecs = np.linalg.eigh((a + a.T) / 2)
    u = vecs[:, np.abs(vals) > tol]
    return u @ u.T


def code_targets(d):
    k = 2
    while comb(k, k // 2) < d:
        k += 1
    codes = list(combinations(range(k), k // 2))[:d]
    return [np.array([i for i, code in enumerate(codes) if e in code])
            for e in range(k)]


def covariances(b, a, d1, d2, omega, targets):
    p, d = b.shape
    out = []
    for target in [np.array([], dtype=int), *targets]:
        ak = a.copy()
        ak[target, :] = 0
        gk = np.eye(d) - ak
        invg = np.linalg.inv(gk)
        pair = []
        for diag in (d1, d2):
            diagk = diag.copy()
            diagk[target] = 0
            sz = invg @ np.diag(diagk) @ invg.T
            pair.append(b @ sz @ b.T + omega)
        out.append(pair)
    return out


def one_trial(seed, d):
    rng = np.random.default_rng(seed)
    p = d + 2
    b = rng.normal(size=(p, d))
    b /= np.linalg.norm(b, axis=0)
    a = np.tril(rng.uniform(-0.7, 0.7, (d, d)), -1)
    d1 = rng.uniform(1.0, 1.5, d)
    shifts = rng.uniform(0.35, 0.9, d) * np.where(np.arange(d) % 2, -1, 1)
    d2 = d1 + shifts
    q = rng.normal(size=(p, p))
    omega = q @ q.T + np.eye(p)
    targets = code_targets(d)
    covs = covariances(b, a, d1, d2, omega, targets)
    projs = [projector(pair[0] - pair[1]) for pair in covs[1:]]
    lines = []
    min_gap = float("inf")
    k = len(targets)
    for size in range(1, k + 1):
        for ts in combinations(range(k), size):
            h = sum((np.eye(p) - projs[t] for t in ts), start=np.zeros((p, p)))
            vals, vecs = np.linalg.eigh((h + h.T) / 2)
            positives = vals[vals > 1e-8]
            if len(positives):
                min_gap = min(min_gap, float(positives.min()))
            zeros = vecs[:, np.abs(vals) < 1e-8]
            if zeros.shape[1] == 1:
                v = zeros[:, 0]
                pp = np.outer(v, v)
                if all(norm(pp - np.outer(u, u)) > 1e-6 for u in lines):
                    lines.append(v)
    assert len(lines) == d, (seed, d, len(lines))
    raw = np.column_stack(lines)
    perm = max(permutations(range(d)), key=lambda pp: sum(abs(b[:, i] @ raw[:, j]) for i, j in enumerate(pp)))
    bh = raw[:, perm]
    bh *= np.sign(np.sum(b * bh, axis=0))
    mix_error = norm(bh - b)
    what = np.linalg.pinv(bh)
    guessed_targets = [np.array([i for i in range(d) if norm((np.eye(p) - pr) @ bh[:, i:i+1]) > 1e-6])
                       for pr in projs]
    assert all(np.array_equal(t, th) for t, th in zip(targets, guessed_targets))
    proxy = [[what @ sx @ what.T for sx in pair] for pair in covs]
    psi = np.zeros((d, d))
    for i in range(d):
        ki = next(kj for kj, tt in enumerate(guessed_targets) if i in tt)
        psi[i] = proxy[ki + 1][0][i]
    psi = (psi + psi.T) / 2
    sz1, sz2 = [x - psi for x in proxy[0]]
    omega_hat = covs[0][0] - bh @ sz1 @ bh.T
    s, u = np.linalg.eigh(sz2)
    invsqrt = (u * (s ** -0.5)) @ u.T
    lam, evec = np.linalg.eigh(invsqrt @ sz1 @ invsqrt)
    rows = (invsqrt @ evec).T
    row_perm = next(pp for pp in permutations(range(d))
                    if all(abs(rows[pp[i], i]) > 1e-6 for i in range(d)))
    gh = rows[list(row_perm), :]
    gh /= np.diag(gh)[:, None]
    ah = np.eye(d) - gh
    kappa = np.linalg.cond(b)
    assert min_gap + 1e-8 >= kappa ** -2
    return {
        "seed": seed, "d": d, "p": p, "K": k,
        "mixing_error": mix_error,
        "sensor_covariance_error": norm(omega_hat - omega),
        "causal_matrix_error": norm(ah - a),
        "minimum_sum_projector_gap": min_gap,
        "proved_gap_lower_bound": float(kappa ** -2),
    }


def drift_counterexample():
    theta = 0.4
    r = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    profiles = [np.array([0.01, 0.014]), np.array([0.021, 0.032]),
                np.array([0.013, 0.015])]
    targets = [np.array([0]), np.array([1])]
    old = []
    same = []
    drift_size = 0.0
    minimum_noise_eigenvalue = 1.0
    for ki, target in enumerate([np.array([], dtype=int), *targets]):
        pair = []
        old_pair = []
        for ell, diag in enumerate(profiles):
            diagk = diag.copy()
            diagk[target] = 0
            signal_old = np.diag(diagk)
            signal_new = r @ signal_old @ r.T
            noise_new = np.eye(2) + signal_old - signal_new
            drift_size = max(drift_size, norm(noise_new - np.eye(2)))
            minimum_noise_eigenvalue = min(minimum_noise_eigenvalue, float(np.linalg.eigvalsh(noise_new).min()))
            pair.append(signal_new + noise_new)
            old_pair.append(signal_old + np.eye(2))
        same.append(pair)
        old.append(old_pair)
    return {
        "representation_rotation_radians": theta,
        "maximum_sensor_covariance_drift": drift_size,
        "minimum_sensor_covariance_eigenvalue": minimum_noise_eigenvalue,
        "maximum_observed_covariance_difference": max(norm(old[k][l] - same[k][l]) for k in range(3) for l in range(3)),
        "baseline_contrast_ratios": ((profiles[2] - profiles[0]) / (profiles[1] - profiles[0])).tolist(),
        "interpretation": "Two distinct latent coordinate systems produce identical centered Gaussian observed laws when sensor noise may vary by environment and variance regime.",
    }


def confounded_three_profile_trial(seed, d):
    """Unknown B, dense sensor noise, dense confounding, both varying by k."""
    rng = np.random.default_rng(1000 + seed)
    p = d + 2
    b = rng.normal(size=(p, d))
    b /= np.linalg.norm(b, axis=0)
    a = np.tril(rng.uniform(-0.7, 0.7, (d, d)), -1)
    targets = code_targets(d)
    profiles = [np.zeros(d), rng.uniform(0.5, 1.5, d), rng.uniform(0.5, 1.5, d)]
    covs = []
    for target in [np.array([], dtype=int), *targets]:
        ak = a.copy()
        ak[target, :] = 0
        ig = np.linalg.inv(np.eye(d) - ak)
        q = rng.normal(size=(d, d))
        background = q @ q.T + np.eye(d)
        background[target, :] = 0
        background[:, target] = 0
        qsensor = rng.normal(size=(p, p))
        omega = qsensor @ qsensor.T + np.eye(p)
        covs.append([])
        for profile in profiles:
            diag = profile.copy()
            diag[target] = 0
            sz = ig @ (background + np.diag(diag)) @ ig.T
            covs[-1].append(b @ sz @ b.T + omega)
    projs = [projector(triple[1] - triple[0]) for triple in covs[1:]]
    lines = []
    k = len(targets)
    for size in range(1, k + 1):
        for ts in combinations(range(k), size):
            h = sum((np.eye(p) - projs[t] for t in ts), start=np.zeros((p, p)))
            vals, vecs = np.linalg.eigh((h + h.T) / 2)
            zeros = vecs[:, np.abs(vals) < 1e-8]
            if zeros.shape[1] == 1:
                v = zeros[:, 0]
                if all(norm(np.outer(v, v) - np.outer(u, u)) > 1e-6 for u in lines):
                    lines.append(v)
    assert len(lines) == d
    raw = np.column_stack(lines)
    perm = max(permutations(range(d)), key=lambda pp: sum(abs(b[:, i] @ raw[:, j]) for i, j in enumerate(pp)))
    bh = raw[:, perm]
    bh *= np.sign(np.sum(b * bh, axis=0))
    what = np.linalg.pinv(bh)
    c1 = what @ (covs[0][1] - covs[0][0]) @ what.T
    c2 = what @ (covs[0][2] - covs[0][0]) @ what.T
    s, u = np.linalg.eigh(c1)
    invsqrt = (u * (s ** -0.5)) @ u.T
    lam, evec = np.linalg.eigh(invsqrt @ c2 @ invsqrt)
    rows = (invsqrt @ evec).T
    row_perm = next(pp for pp in permutations(range(d))
                    if all(abs(rows[pp[i], i]) > 1e-6 for i in range(d)))
    gh = rows[list(row_perm), :]
    gh /= np.diag(gh)[:, None]
    return {"seed": seed, "d": d, "p": p, "K": k,
            "mixing_error": norm(bh - b),
            "causal_matrix_error": norm((np.eye(d) - gh) - a)}


if __name__ == "__main__":
    trials = [one_trial(seed, 2 + seed % 5) for seed in range(50)]
    confounded_trials = [confounded_three_profile_trial(seed, 2 + seed % 5) for seed in range(50)]
    result = {
        "status": "finite_diagnostic_passed_not_proof",
        "trials": trials,
        "max_errors": {key: max(x[key] for x in trials) for key in
                       ["mixing_error", "sensor_covariance_error", "causal_matrix_error"]},
        "drift_counterexample": drift_counterexample(),
        "confounded_three_profile_trials": confounded_trials,
        "confounded_max_errors": {key: max(x[key] for x in confounded_trials) for key in
                                  ["mixing_error", "causal_matrix_error"]},
    }
    path = Path(__file__).with_name("causal_inference_check.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "max_errors": result["max_errors"],
                      "confounded_max_errors": result["confounded_max_errors"],
                      "drift_counterexample": result["drift_counterexample"]}, indent=2))
