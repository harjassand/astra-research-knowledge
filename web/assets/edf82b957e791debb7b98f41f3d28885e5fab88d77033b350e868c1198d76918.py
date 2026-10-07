# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=2.0", "cvxpy>=1.6"]
# ///
"""Small transcription checks for the isotropic fourth-moment SDP.

The optimizer interface receives only the coefficient tensor. Hidden frames and
couplings are confined to fixture generation and retrospective assessment.
Floating-point solver status is not a universal proof or an exact certificate.
"""
from __future__ import annotations

import itertools
import json
import resource
import time
from pathlib import Path

import cvxpy as cp
import numpy as np


def tensor_from_coupling(g, u):
    n = len(g)
    t = np.zeros((n,) * 4)
    for i in range(n):
        t[i, i, i, i] = g[i, i]
        for j in range(i):
            for p in set(itertools.permutations((i, i, j, j))):
                t[p] = g[i, j] / 3
    return np.einsum("ai,bj,ck,dl,ijkl->abcd", u, u, u, u, t)


def axis_moment(u):
    return np.einsum("ai,bi,ci,di->abcd", u, u, u, u) / len(u)


def sphere_moment(n):
    eye = np.eye(n)
    return (
        np.einsum("ij,kl->ijkl", eye, eye)
        + np.einsum("ik,jl->ijkl", eye, eye)
        + np.einsum("il,jk->ijkl", eye, eye)
    ) / (n * (n + 2))


def recover_moment(observed_t):
    """No hidden frame, coupling matrix, or margin is passed to this function."""
    n = len(observed_t)
    monomials = list(itertools.combinations_with_replacement(range(n), 4))
    lookup = {p: i for i, p in enumerate(monomials)}
    pairs = list(itertools.combinations_with_replacement(range(n), 2))
    weights = np.array([1 if i == j else np.sqrt(2) for i, j in pairs])
    y = cp.Variable(len(monomials))
    objective_coefficients = np.zeros(len(monomials))
    for p in itertools.product(range(n), repeat=4):
        objective_coefficients[lookup[tuple(sorted(p))]] += observed_t[p]
    cat_index = np.zeros((len(pairs), len(pairs)), dtype=int)
    cat_weight = weights[:, None] * weights[None, :]
    for a, p in enumerate(pairs):
        for b, q in enumerate(pairs):
            cat_index[a, b] = lookup[tuple(sorted(p + q))]
    c_expr = cp.bmat([
        [weights[a] * weights[b] * y[lookup[tuple(sorted(p + q))]]
         for b, q in enumerate(pairs)]
        for a, p in enumerate(pairs)
    ])
    contraction = np.zeros((len(pairs), len(monomials)))
    target = np.zeros(len(pairs))
    for a, (i, j) in enumerate(pairs):
        target[a] = (1 / n) if i == j else 0
        for k in range(n):
            contraction[a, lookup[tuple(sorted((i, j, k, k)))]] += 1
    psd = c_expr >> 0
    equality = contraction @ y == target
    problem = cp.Problem(cp.Maximize(objective_coefficients @ y), [psd, equality])
    started = time.perf_counter()
    problem.solve(solver="CLARABEL", tol_gap_abs=1e-10, tol_gap_rel=1e-10,
                  tol_feas=1e-10, max_iter=300)
    elapsed = time.perf_counter() - started
    if y.value is None:
        raise RuntimeError(f"No solver output: {problem.status}")

    # A numerical affine projection and inward mix protect the audit from tiny
    # equality/PSD residuals. These are not exact rational certificates.
    values = np.asarray(y.value).copy()
    values += contraction.T @ np.linalg.lstsq(
        contraction @ contraction.T, target - contraction @ values, rcond=None
    )[0]
    c_val = cat_weight * values[cat_index]
    raw_min_eigenvalue = float(np.linalg.eigvalsh(c_val)[0])
    sph = sphere_moment(n)
    sph_values = np.array([sph[p] for p in monomials])
    sph_min = 2 / (n * (n + 2))
    mix = max(0.0, (1e-12 - raw_min_eigenvalue) / (sph_min - raw_min_eigenvalue))
    values = (1 - mix) * values + mix * sph_values
    c_val = cat_weight * values[cat_index]
    out = np.empty((n,) * 4)
    for p in itertools.product(range(n), repeat=4):
        out[p] = values[lookup[tuple(sorted(p))]]

    # Numerical dual upper estimate: project the dual PSD matrix, then bound its
    # stationarity error using ||y||_2 <= ||Y||_F <= trace(C_Y) = 1.
    dual_psd = np.asarray(psd.dual_value)
    ev, vec = np.linalg.eigh(dual_psd)
    dual_psd = (vec * np.maximum(ev, 0)) @ vec.T
    dual_eq = np.asarray(equality.dual_value)
    psd_adjoint = np.bincount(
        cat_index.ravel(), weights=(dual_psd * cat_weight).ravel(),
        minlength=len(monomials),
    )
    stationarity = objective_coefficients + psd_adjoint - contraction.T @ dual_eq
    upper = float(target @ dual_eq + np.linalg.norm(stationarity))
    observed_value = float(np.einsum("ijkl,ijkl", observed_t, out))
    audit = {
        "status": problem.status,
        "solver_seconds": elapsed,
        "raw_min_eigenvalue": raw_min_eigenvalue,
        "inward_mix": mix,
        "output_min_eigenvalue": float(np.linalg.eigvalsh(c_val)[0]),
        "contraction_max_residual": float(np.max(np.abs(contraction @ values - target))),
        "observed_objective": observed_value,
        "numerical_dual_upper_estimate": upper,
        "numerical_dual_gap_estimate": max(0.0, upper - observed_value),
        "dual_stationarity_l2": float(np.linalg.norm(stationarity)),
        "psd_block_dimension": len(pairs),
        "moment_variables": len(monomials),
    }
    return out, audit


def retrospective_axis_error(y, u, seed):
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(len(u), len(u)))
    a = (a + a.T) / 2
    _, v = np.linalg.eigh(np.einsum("ijkl,kl->ij", y, a))
    match = np.abs(u.T @ v)
    # Small-fixture matching, never used by the learner/rounding procedure.
    best = max(min(match[i, perm[i]] for i in range(len(u)))
               for perm in itertools.permutations(range(len(u))))
    return float(np.sqrt(max(0, 1 - best * best)))


def main():
    started = time.perf_counter()
    rng = np.random.default_rng(7401)
    fixtures = [
        ("coupled_pd", np.array([[2., .5, -.25], [.5, 3., .2], [-.25, .2, 4.]]), 0.),
        ("near_radial_equal_diagonal", np.ones((4, 4)) + .05 * np.eye(4), 0.),
        ("indefinite_positive_contrasts", np.array([[1., .5, .5], [.5, 1., -3.5], [.5, -3.5, 1.]]), 0.),
        ("additive_tensor_noise", np.ones((4, 4)) + .1 * np.eye(4), 1e-4),
        ("negative_contrast_control", np.array([[1., 2.], [2., 1.]]), 0.),
        ("zero_contrast_control", np.ones((3, 3)), 0.),
    ]
    rows = []
    for case, g, sigma in fixtures:
        n = len(g)
        u, _ = np.linalg.qr(rng.normal(size=(n, n)))
        true = tensor_from_coupling(g, u)
        noise = np.zeros_like(true)
        if sigma:
            for p in itertools.combinations_with_replacement(range(n), 4):
                value = rng.normal()
                for q in set(itertools.permutations(p)):
                    noise[q] = value
            noise *= sigma / np.linalg.norm(noise)
        out, audit = recover_moment(true + noise)
        target = axis_moment(u)
        true_objective = float(np.einsum("ijkl,ijkl", true, out))
        gap = float(np.trace(g) / n - true_objective)
        r = float(np.linalg.norm(out - target))
        gamma = min(g[i, i] + g[j, j] - 2 * g[i, j]
                    for i in range(n) for j in range(i))
        row = {
            "case": case, "n": n,
            "min_coupling_eigenvalue": float(np.linalg.eigvalsh(g)[0]),
            "gamma": float(gamma), "noise_frobenius": float(np.linalg.norm(noise)),
            "moment_error_frobenius": r, "true_objective_gap": gap,
            "axis_error_max_sine": retrospective_axis_error(out, u, 137),
            **audit,
        }
        if gamma > 0:
            row["growth_bound_rhs"] = max(0., 4 * gap / gamma)
            row["growth_bound_lhs"] = r * r
            row["growth_inequality_with_roundoff"] = bool(r * r <= 4 * gap / gamma + 1e-8)
            delta_est = max(1e-8, audit["numerical_dual_gap_estimate"])
            row["noise_bound_with_numerical_delta"] = 4 * sigma / gamma + 2 * np.sqrt(delta_est / gamma)
            row["noise_inequality_with_roundoff"] = bool(r <= row["noise_bound_with_numerical_delta"] + 1e-8)
        rows.append(row)

    result = {
        "scope": "Six small floating-point SDP transcription checks; no universal proof or exact certification.",
        "optimizer_input": "Only the observed fourth coefficient tensor.",
        "solver": "CVXPY + CLARABEL", "fixtures": rows,
        "body_seconds": time.perf_counter() - started,
        "process_peak_rss_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    destination = Path(__file__).with_name("optimization_sdp_check.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
