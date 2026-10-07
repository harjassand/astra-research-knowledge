"""Finite diagnostics for the d=3, (2,1)-block encoder.

Uses the exact binomial count law and exact qubit Schur/coherent/jitter
moments. It does not simulate the complete channel or prove the asymptotic
trace-distance theorem. Source states have unknown block weight q and unknown
inner polarization r. Rotating that polarization does not change these
covariant moment checks.
"""
import json
import math
from pathlib import Path

import numpy as np


def normalized_logweights(logw):
    logw = np.asarray(logw, dtype=float)
    p = np.exp(logw - np.max(logw))
    return p / p.sum()


def qubit_moments(k, r, n):
    """Return mean z coordinate and raw second moments of x,z.

    Coordinates use sigma_i/sqrt(2) in Hilbert--Schmidt convention,
    and already include the block scaling sqrt(k/n).
    """
    if k == 0:
        return 0.0, 0.0, 0.0
    pplus, pminus = (1 + r) / 2, (1 - r) / 2
    logratio = math.log(pminus / pplus)
    spins = list(range(k % 2, k + 1, 2))
    logweights, vals = [], []
    for ell in spins:
        low = (k - ell) // 2
        high = (k + ell) // 2
        logm = (
            math.lgamma(k + 1)
            - math.lgamma(low + 1)
            - math.lgamma(high + 1)
            + math.log(ell + 1)
            - math.log(high + 1)
        )
        one_minus_t = -math.expm1((ell + 1) * logratio)
        logs = (
            low * math.log(pplus * pminus)
            + (ell + 1) * math.log(pplus)
            + math.log(one_minus_t)
            - math.log(r)
        )
        logweights.append(logm + logs)
        d2d1 = (1 + r) * (-math.expm1((ell + 2) * logratio)) / one_minus_t
        d3d1 = (1 + r) ** 2 * (-math.expm1((ell + 3) * logratio)) / one_minus_t
        ez = ((ell + 1) / (ell + 2) * d2d1 - 1) / r
        ez2 = (
            (ell + 1) / (ell + 3) * d3d1
            - 2 * (ell + 1) / (ell + 2) * d2d1
            + 1
        ) / (r * r)
        assert -1e-7 <= ez2 <= 1 + 1e-7, (k, ell, r, ez2)
        eg = ell + 1
        eg2 = eg * eg + 1 / 3
        vals.append((eg * ez / math.sqrt(2 * n), eg2 * (1 - ez2) / (4 * n), eg2 * ez2 / (2 * n)))
    weights = normalized_logweights(logweights)
    return tuple(weights @ np.asarray(vals))


def row(n, w=0.7):
    q = w + 0.08 * n ** -0.25
    r = 0.4 * n ** -0.25
    ks = np.arange(n + 1)
    logw = [
        math.lgamma(n + 1) - math.lgamma(int(k) + 1) - math.lgamma(n - int(k) + 1)
        + int(k) * math.log(q) + (n - int(k)) * math.log1p(-q)
        for k in ks
    ]
    weights = normalized_logweights(logw)
    means = np.zeros(n + 1)
    second_x = np.zeros(n + 1)
    second_z = np.zeros(n + 1)
    ignored_mass = 0.0
    for k, weight in enumerate(weights):
        if weight < 1e-18:
            ignored_mass += float(weight)
            continue
        means[k], second_x[k], second_z[k] = qubit_moments(k, r, n)
    meanz = float(weights @ means)
    target_mean = math.sqrt(n) * q * r / math.sqrt(2)
    varx = float(weights @ second_x)
    varz = float(weights @ second_z) - meanz * meanz
    count_variance = 1.5 * (q * (1 - q) + 1 / (12 * n))
    target_count_variance = 1.5 * w * (1 - w)
    covariance = float(weights @ ((ks - n * q) / math.sqrt(n) * means)) * math.sqrt(1.5)
    delta = max(abs(q * (1 + r) / 2 - w / 2), abs(q * (1 - r) / 2 - w / 2), abs(w - q))
    errors = [abs(meanz - target_mean), abs(varx - w / 2), abs(varz - w / 2), abs(count_variance - target_count_variance), abs(covariance)]
    return {
        "n": n,
        "q": q,
        "r": r,
        "delta_operator": delta,
        "mean_inner_z": meanz,
        "gaussian_target_mean_inner_z": target_mean,
        "variance_inner_x": varx,
        "variance_inner_z": varz,
        "gaussian_target_variance_inner": w / 2,
        "count_variance_hs": count_variance,
        "gaussian_target_count_variance_hs": target_count_variance,
        "count_inner_z_covariance": covariance,
        "max_displayed_moment_error": max(errors),
        "error_over_delta_plus_n_minus_half": max(errors) / (delta + n ** -0.5),
        "omitted_count_mass": ignored_mass,
    }


def covariance_matrix(rho0, basis):
    means = [np.trace(rho0 @ h).real for h in basis]
    return np.asarray([
        [np.trace(rho0 @ h @ g).real - means[i] * means[j] for j, g in enumerate(basis)]
        for i, h in enumerate(basis)
    ])


def check_covariance():
    rho0 = np.diag([0.35, 0.35, 0.3])
    sx = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], complex) / math.sqrt(2)
    sy = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], complex) / math.sqrt(2)
    sz = np.diag([1, -1, 0]) / math.sqrt(2)
    hc = np.diag([1, 1, -2]) / math.sqrt(6)
    covariance = covariance_matrix(rho0, [sx, sy, sz, hc])
    expected = np.diag([0.35, 0.35, 0.35, 0.315])
    assert np.max(np.abs(covariance - expected)) < 1e-14
    # A resolved interblock mode has nonzero CCR form, with no collision
    # singularity inside the equal-eigenvalue block.
    x13 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], complex) / math.sqrt(2)
    y13 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], complex) / math.sqrt(2)
    omega13 = (-1j * np.trace(rho0 @ (x13 @ y13 - y13 @ x13))).real
    omega12 = (-1j * np.trace(rho0 @ (sx @ sy - sy @ sx))).real
    assert abs(omega13 - 0.05) < 1e-14
    assert abs(omega12) < 1e-14
    return {"covariance_hs": covariance.tolist(), "interblock_symplectic": omega13, "intrablock_symplectic": omega12}


def check_rounding():
    rng = np.random.default_rng(20261007)
    counts = rng.multinomial(37, [0.2, 0.35, 0.45], size=1000)
    jitter = rng.uniform(-0.5, 0.5, size=(1000, 2))
    first = counts[:, :2] + jitter
    rounded_first = np.floor(first + 0.5).astype(int)
    rounded = np.column_stack([rounded_first, 37 - rounded_first.sum(axis=1)])
    assert np.array_equal(rounded, counts)
    return {"fixtures": 1000, "rounding_errors": 0, "scope": "finite first-coordinate cube jitter only"}


if __name__ == "__main__":
    result = {
        "status": "FINITE_FLOATING_POINT_DIAGNOSTICS_ONLY",
        "covariance": check_covariance(),
        "rounding": check_rounding(),
        "block_encoder_exact_moments": [row(n) for n in [16, 64, 256, 1024, 4096]],
        "limits": "Moment convergence is not TV convergence or a proof certificate. Counts below floating threshold are reported as omitted mass. No full circuit is constructed.",
    }
    path = Path(__file__).with_name("block_moment_diagnostics.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
