"""Finite heat-pulse identification: exact moments and a continuous one-path run.

This is a finite Gaussian OU simulation, not a hardware experiment. Every pulse
and post-pulse interval is sampled with its exact integrated covariance. The
simulator knows A,D to generate data; recover_unknown() only receives the tagged
output moment, n, pulse calibration and timing. No state reset occurs between
cycles. SciPy matrix functions are floating point, not interval-certified.
"""

from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import (expm, logm, solve_continuous_lyapunov,
                          solve_discrete_lyapunov)
from scipy.integrate import quad_vec
from scipy.signal import lfilter


def sym(x):
    return (x + x.T) / 2


def pulse_operator(a, h, eta):
    n = a.shape[0]
    ell = np.kron(a, np.eye(n)) + np.kron(np.eye(n), a)
    ident = np.eye(n * n)
    omega = 2 * np.pi / h
    # All functions of ell commute; solve avoids an explicit inverse.
    rhs = eta * omega**2 * (expm(h * ell) - ident)
    denom = ell @ (ell @ ell + omega**2 * ident)
    return np.linalg.solve(denom.T, rhs.T).T


def pulse_covariance(a, d, h, eta):
    n = len(a)
    return sym((pulse_operator(a, h, eta) @ d.ravel()).reshape(n, n))


def invert_pulse_covariance(a, s, h, eta):
    """One Stein solve and three Lyapunov-map applications; O(n^3) algebra."""
    f = expm(a * h)
    u = solve_discrete_lyapunov(f, s, method="bilinear")
    ell1 = a @ u + u @ a.T
    ell2 = a @ ell1 + ell1 @ a.T
    ell3 = a @ ell2 + ell2 @ a.T
    omega = 2 * np.pi / h
    return sym(-(ell3 + omega**2 * ell1) / (eta * omega**2))


def entropy_rate(a, d):
    covariance = sym(solve_continuous_lyapunov(a, -2 * d))
    current = a @ covariance + d
    entropy = np.trace(current.T @ np.linalg.solve(d, current)
                       @ np.linalg.inv(covariance))
    return float(np.real(entropy)), covariance


def observability(a, c, delta, length):
    return np.stack([c @ expm(a * j * delta) for j in range(length)])


def recover_unknown(v, n, h, eta, delta):
    h0 = sym(v[:n, :n])
    h1 = v[1:n + 1, :n]
    f = np.linalg.solve(h0.T, h1.T).T
    a = np.real_if_close(logm(f) / delta, tol=1000)
    if np.iscomplexobj(a):
        return {"valid_real_log": False,
                "minimum_eigenvalue_H0": float(np.linalg.eigvalsh(h0)[0])}
    d = invert_pulse_covariance(a, h0, h, eta)
    eigen_d = np.linalg.eigvalsh(d)
    stable = bool(np.max(np.linalg.eigvals(a).real) < 0)
    if not stable or eigen_d[0] <= 0:
        return {"valid_real_log": True, "stable": stable,
                "minimum_eigenvalue_D": float(eigen_d[0]),
                "minimum_eigenvalue_H0": float(np.linalg.eigvalsh(h0)[0])}
    sigma, covariance = entropy_rate(a, d)
    return {"valid_real_log": True, "stable": stable, "entropy_rate": sigma,
            "minimum_eigenvalue_H0": float(np.linalg.eigvalsh(h0)[0]),
            "minimum_eigenvalue_D": float(eigen_d[0]),
            "minimum_eigenvalue_covariance": float(np.linalg.eigvalsh(covariance)[0]),
            "A_in_observation_coordinates": a.tolist(),
            "D_in_observation_coordinates": d.tolist()}


def run_one_path(a, d, c, h, eta, delta, cycles, seed=913, batch_size=20000):
    """No-reset run, vectorized using diagonalization only for the simulator."""
    rng = np.random.default_rng(seed)
    n = len(a)
    _, covariance = entropy_rate(a, d)
    fh = expm(a * h)
    fd = expm(a * delta)
    s = pulse_covariance(a, d, h, eta)
    qh0 = sym(covariance - fh @ covariance @ fh.T)
    qh1 = sym(qh0 + s)
    qd = sym(covariance - fd @ covariance @ fd.T)
    lh0, lh1, ld = (np.linalg.cholesky(x) for x in (qh0, qh1, qd))
    vals, eigenvectors = np.linalg.eig(a.astype(complex))
    inv_vectors = np.linalg.inv(eigenvectors)
    rho = np.exp(vals * (h + n * delta))
    powers = [expm(a * j * delta) for j in range(n + 1)]
    state = rng.multivariate_normal(np.zeros(n), covariance)
    total = np.zeros((n + 1, n + 1))
    total_hot = 0
    max_end_mismatch = 0.
    for start in range(0, cycles, batch_size):
        m = min(batch_size, cycles - start)
        signs = rng.integers(0, 2, m) * 2 - 1
        raw = rng.standard_normal((m, n + 1, n))
        noises = np.empty_like(raw)
        noises[:, 0] = raw[:, 0] @ lh0.T
        hot = signs == 1
        noises[hot, 0] = raw[hot, 0] @ lh1.T
        for j in range(1, n + 1):
            noises[:, j] = raw[:, j] @ ld.T
        end_noise = sum(noises[:, j] @ powers[n - j].T
                        for j in range(n + 1))
        modal_noise = end_noise @ inv_vectors.T
        modal_initial = inv_vectors @ state
        modal_starts = np.empty_like(modal_noise)
        modal_end = np.empty(n, complex)
        for j in range(n):
            ends, _ = lfilter([1.], [1., -rho[j]], modal_noise[:, j],
                              zi=[rho[j] * modal_initial[j]])
            modal_starts[:, j] = np.r_[modal_initial[j], ends[:-1]]
            modal_end[j] = ends[-1]
        starts = (modal_starts @ eigenvectors.T).real
        x = starts @ fh.T + noises[:, 0]
        z = np.empty((m, n + 1))
        z[:, 0] = x @ c
        for j in range(1, n + 1):
            x = x @ fd.T + noises[:, j]
            z[:, j] = x @ c
        state = (eigenvectors @ modal_end).real
        max_end_mismatch = max(max_end_mismatch, float(np.linalg.norm(x[-1] - state)))
        total += (z.T * (2 * signs)) @ z
        total_hot += int(hot.sum())
    return sym(total / cycles), total_hot, max_end_mismatch


def main():
    h, eta, delta = 1., 1., .5
    a = -np.array([[2., -1., 0.], [-1., 2., -1.], [0., -1., 2.]])
    c = np.array([1., 0., 0.])
    o = observability(a, c, delta, 4)
    warm = []
    for t in (0., .1, .2):
        d = np.array([[1., 0., 0.], [0., 1., t], [0., t, 1 - 4 * t]])
        s = pulse_covariance(a, d, h, eta)
        s_quad, quad_err = quad_vec(lambda u: 2 * eta * np.sin(np.pi * u / h)**2
                                  * expm(a * u) @ d @ expm(a.T * u), 0, h,
                                  epsabs=1e-12, epsrel=1e-12)
        v = o @ s @ o.T
        sigma, covariance = entropy_rate(a, d)
        recovered = recover_unknown(v, 3, h, eta, delta)
        d_recovered = sym(np.linalg.solve(pulse_operator(a, h, eta),
                         (np.linalg.inv(o[:3]) @ v[:3, :3]
                          @ np.linalg.inv(o[:3]).T).ravel()).reshape(3, 3))
        warm.append({"t": t, "true_entropy_rate": sigma,
                     "formula_entropy_rate": 4 * t * t / (1 - 4 * t - t * t),
                     "native_output_variance": float(c @ covariance @ c),
                     "tagged_covariance": v.tolist(),
                     "pulse_formula_quadrature_error": float(np.linalg.norm(s - s_quad)),
                     "quadrature_reported_error": float(quad_err),
                     "known_A_D_error": float(np.linalg.norm(d_recovered - d)),
                     "unknown_A_recovery": recovered})
    # A better-conditioned rotation example demonstrates the stochastic protocol.
    a2 = np.array([[-1., -3.], [3., -1.]])
    d2 = np.diag([1., 2.])
    c2 = np.array([1., 0.])
    h2, delta2, eta2, cycles = .5, np.pi / 6, 1., 1_000_000
    o2 = observability(a2, c2, delta2, 3)
    s2 = pulse_covariance(a2, d2, h2, eta2)
    v2 = o2 @ s2 @ o2.T
    vhat, hot_count, mismatch = run_one_path(a2, d2, c2, h2, eta2, delta2,
                                            cycles, seed=913)
    sigma2, sigma_cov2 = entropy_rate(a2, d2)
    trace_bound = 3 * (1 + eta2) * float(c2 @ sigma_cov2 @ c2)
    alpha = .05
    conservative_radius = np.sqrt(12 * trace_bound**2 / (cycles * alpha))
    tmin = float(np.linalg.svd(pulse_operator(a2, h2, eta2), compute_uv=False)[-1])
    omin = float(np.linalg.svd(o2, compute_uv=False)[-1])
    required_known_A_D_01 = int(np.ceil(12 * trace_bound**2 /
                              (alpha * tmin**2 * omin**4 * .1**2)))
    result = {
        "scope": "Floating-point numerical execution, not experimental hardware or formal interval arithmetic.",
        "warm_3d_family": warm,
        "warm_3d_observability_condition_number": float(np.linalg.cond(o[:3])),
        "warm_3d_pulse_operator_min_singular_value": float(np.linalg.svd(pulse_operator(a, h, eta), compute_uv=False)[-1]),
        "one_path_example": {
            "A": a2.tolist(), "D": d2.tolist(), "C": c2.tolist(),
            "pulse_duration": h2, "pulse_amplitude": eta2,
            "maximum_temperature_slew": eta2 * np.pi / h2,
            "observation_spacing": delta2, "cycles": cycles,
            "scalar_observations": cycles * 3, "hot_pulses": hot_count,
            "simulated_physical_time": cycles * (h2 + 2 * delta2),
            "hidden_state_resets_between_cycles": 0,
            "finite_population_tagged_covariance": v2.tolist(),
            "empirical_tagged_covariance": vhat.tolist(),
            "empirical_tagged_covariance_Frobenius_error": float(np.linalg.norm(vhat - v2)),
            "true_entropy_rate": sigma2,
            "population_recovery": recover_unknown(v2, 2, h2, eta2, delta2),
            "empirical_recovery": recover_unknown(vhat, 2, h2, eta2, delta2),
            "simulator_cycle_end_consistency_error": mismatch,
            "conservative_95_percent_Frobenius_moment_radius": float(conservative_radius),
            "certified_known_A_D_error_0point1_cycle_budget": required_known_A_D_01,
            "warning": "The empirical entropy estimate is illustrative. The conservative moment radius is not claimed to certify its displayed error."
        }
    }
    out = Path(__file__).parent / "heat_pulse_execution.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"warm_population_entropy": [r["unknown_A_recovery"].get("entropy_rate") for r in warm],
                      "empirical_true_entropy": sigma2,
                      "empirical_recovered_entropy": result["one_path_example"]["empirical_recovery"].get("entropy_rate"),
                      "tagged_moment_error": float(np.linalg.norm(vhat - v2)),
                      "conservative_moment_radius": float(conservative_radius),
                      "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
