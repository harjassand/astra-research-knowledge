"""Finite numerical checks for PROOFS_AND_COMPARISONS.md.

These checks support debugging; the proofs carry the general claims. No source
matrix is made available to acquire_from_actions. All work and action counts
are recorded. Requires numpy and scipy. Run: python check_dissipative.py
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, eigh


def norm(a):
    return float(np.linalg.norm(a, 2))


def ortho(rng, n):
    return np.linalg.qr(rng.normal(size=(n, n)))[0]


def symmetric_sqrt(a, inverse=False, tol=1e-12):
    w, q = eigh((a + a.T) / 2)
    f = np.zeros_like(w)
    active = w > tol
    f[active] = 1 / np.sqrt(w[active]) if inverse else np.sqrt(w[active])
    return (q * f) @ q.T


class NoisySource:
    def __init__(self, matrix, delta, rng):
        self.__matrix = matrix.copy()
        self.__delta = delta
        self.__rng = rng
        self.calls = 0

    def action(self, v):
        self.calls += 1
        e = self.__rng.normal(size=v.size)
        e *= self.__delta * np.linalg.norm(v) / np.linalg.norm(e)
        return self.__matrix @ v + e


def acquire_from_actions(action, n, alpha, delta):
    y = np.column_stack([action(np.eye(n)[:, i]) for i in range(n)])
    h = (y + y.T) / 2
    eta = delta * np.sqrt(n) / alpha
    if eta >= 1:
        raise ValueError("No certified positive model at this source precision.")
    return h, eta


def noisy_acquisition_check(rng):
    n, k, alpha, delta = 12, 3, 0.05, 0.0001
    a, h, sources = [], [], []
    margins = []
    for j in range(k):
        q = ortho(rng, n)
        aj = (q * np.geomspace(alpha, 3.0, n)) @ q.T
        source = NoisySource(aj, delta, rng)
        hj, eta = acquire_from_actions(source.action, n, alpha, delta)
        ai = symmetric_sqrt(aj, inverse=True)
        relative_error = norm(ai @ (hj - aj) @ ai)
        assert relative_error <= eta + 1e-12
        margins.append(relative_error)
        a.append(aj)
        h.append(hj)
        sources.append(source)

    # Compare the same subsequent, independently drawn switched computation.
    u = np.eye(n)
    v = np.eye(n)
    max_error = 0.0
    max_refined_ratio = 0.0
    duration = 0.0
    steps = 600
    initial = rng.normal(size=n)
    initial /= np.linalg.norm(initial)
    x = initial.copy()
    xhat = initial.copy()
    for step in range(steps):
        j = int(rng.integers(k))
        dt = float(10.0 ** rng.uniform(-4, 0.0))
        rate = float(10.0 ** rng.uniform(-2, 2.0))
        r = rng.normal(size=(n, n))
        skew = (r - r.T) * 0.15
        p = expm((-rate * a[j] + skew) * dt)
        ph = expm((-rate * h[j] + skew) * dt)
        u, v = p @ u, ph @ v
        x, xhat = p @ x, ph @ xhat
        max_error = max(max_error, norm(v - u))
        loss = max(0.0, 1.0 - float(x @ x))
        lhs = float((xhat - x) @ (xhat - x))
        rhs = eta * eta * loss / (4 * (1 - eta))
        if rhs > 1e-26:
            max_refined_ratio = max(max_refined_ratio, lhs / rhs)
        assert lhs <= rhs + 2e-12
        duration += dt
    bound = eta / (2 * np.sqrt(1 - eta))
    assert max_error <= bound + 2e-12
    return {
        "n": n,
        "k": k,
        "source_actions": sum(s.calls for s in sources),
        "source_output_scalars": sum(s.calls for s in sources) * n,
        "delta": delta,
        "supplied_alpha": alpha,
        "certified_relative_eta": eta,
        "measured_relative_errors_checker_only": margins,
        "future_segments": steps,
        "future_source_actions": 0,
        "duration": duration,
        "maximum_operator_error": max_error,
        "uniform_operator_bound": bound,
        "maximum_refined_energy_inequality_ratio": max_refined_ratio,
    }


def discrete_defect_check(rng):
    n, k = 10, 4
    pairs = []
    gammas = []
    for j in range(k):
        q, r = ortho(rng, n), ortho(rng, n)
        singular = np.r_[1.0, 1.0, rng.uniform(0.5, 0.98, n - 2)]
        hs = singular.copy()
        hs[2:] += rng.uniform(-0.001, 0.001, n - 2)
        t = (q * singular) @ r.T
        h = (q * hs) @ r.T
        # Exact common singular vectors in this constructed check; zero defects
        # are genuinely unchanged, never inferred from small measured residuals.
        denominator = np.sqrt((1 - hs[2:]**2) * (1 - singular[2:]**2))
        gamma = float(np.max(np.abs(hs[2:] - singular[2:]) / denominator))
        pairs.append((t, h))
        gammas.append(gamma)
    gamma = max(gammas)
    w, wh = np.eye(n), np.eye(n)
    max_error, max_ratio = 0.0, 0.0
    steps = 2000
    for step in range(steps):
        t, h = pairs[int(rng.integers(k))]
        w, wh = t @ w, h @ wh
        err = norm(wh - w)
        max_error = max(max_error, err)
        assert err <= gamma + 2e-12
        for _ in range(2):
            u, v = rng.normal(size=n), rng.normal(size=n)
            left = abs(v @ (wh - w) @ u)
            right = gamma * np.sqrt(max(0.0, u @ u - (w @ u) @ (w @ u)))
            right *= np.sqrt(max(0.0, v @ v - (wh.T @ v) @ (wh.T @ v)))
            if right > 1e-26:
                max_ratio = max(max_ratio, float(left / right))
            assert left <= right + 2e-12
    return {
        "dimension": n,
        "primitive_count": k,
        "word_length": steps,
        "primitive_defect_gamma": gamma,
        "maximum_word_operator_error": max_error,
        "maximum_bilinear_inequality_ratio": max_ratio,
    }


def zero_mode_failure():
    rows = []
    for eta in [1e-2, 1e-4, 1e-8, 1e-12]:
        time = 1 / eta
        distance = 1 - np.exp(-eta * time)
        assert abs(distance - (1 - np.exp(-1))) < 1e-15
        rows.append({"generator_distance": eta,
                     "compatible_source_error": eta / 2,
                     "future_time": time,
                     "propagator_distance": float(distance),
                     "minimax_prediction_error_lower_bound": float(distance / 2)})
    return rows


def main():
    rng = np.random.default_rng(20261031)
    results = {
        "scope": "Synthetic finite checks; proofs carry generality; no practical or novelty claim.",
        "noisy_acquisition": noisy_acquisition_check(rng),
        "discrete_defect": discrete_defect_check(rng),
        "absolute_noise_failure": zero_mode_failure(),
        "status": "PASS",
    }
    path = Path(__file__).with_name("check_results.json")
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
