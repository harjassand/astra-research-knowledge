"""Adversarial numerical checks of the acquired latent alignment certificate.

This is an audit, not an experiment-acquisition demonstration. Matrices are
available to this checker. The root construction separately acquires their
coefficients from charged scalar energy reports and validates rational bounds.

Convention: E_h(x) = .5*x.T@A@x + (b+h).T@x, x in {-1,+1}^n.
Run from the project root with Python 3 and NumPy.
"""

from itertools import product
from pathlib import Path
import json
import numpy as np


def indicators(sizes):
    n = sum(sizes)
    p = np.zeros((n, len(sizes)))
    start = 0
    for a, size in enumerate(sizes):
        p[start:start + size, a] = 1.0
        start += size
    return p


def signs(n):
    return np.asarray(list(product((-1.0, 1.0), repeat=n)))


def quantities(a, b, h_bound, p, remove_coarse_diagonal=True):
    sizes = p.sum(axis=0)
    w = (p / sizes) @ p.T
    normal = np.eye(len(b)) - w
    c = p.T @ a @ p
    if remove_coarse_diagonal:
        # A diagonal change is a constant on the physical Boolean cube.
        shifts = p @ (np.diag(c) / sizes)
        a = a - np.diag(shifts)
        c = p.T @ a @ p
    evals, evecs = np.linalg.eigh(normal)
    v = evecs[:, evals > 0.5]
    gamma = float(np.linalg.eigvalsh(v.T @ a @ v)[0]) - 1e-10
    f = w @ a @ normal
    d2 = float(np.linalg.norm(f, ord=2) ** 2)
    g_reduced = p.T @ a @ normal @ a @ p
    invsqrt = np.diag(1.0 / np.sqrt(sizes))
    d2_reduced = float(np.linalg.eigvalsh(invsqrt @ g_reduced @ invsqrt)[-1])
    off_abs = np.abs(c).sum(axis=1) - np.abs(np.diag(c))
    alpha = float(np.max((np.maximum(np.diag(c), 0.0) + off_abs) / sizes))
    beta = float(np.max(np.abs(b)) + h_bound)
    g = gamma - 2 * alpha - 2 * beta
    # General formula works for negative g too; rational certification can use
    # t >= 0, g+t >= 0, and t*(g+t) >= d2, with loss = n*t/2.
    loss_per_spin = (np.hypot(g, 2 * np.sqrt(d2)) - g) / 4
    return a, c, w, gamma, alpha, beta, g, d2, d2_reduced, loss_per_spin


def audit_case(a, b, h_bound, p, rng):
    n = len(b)
    original_a = a.copy()
    a, c, w, gamma, alpha, beta, g, d2, d2_reduced, per_spin = quantities(
        a, b, h_bound, p
    )
    x = signs(n)
    means = x @ p / p.sum(axis=0)
    rounded = np.where(means >= 0.0, 1.0, -1.0) @ p.T
    delta = x - rounded
    minority = np.count_nonzero(delta, axis=1)
    residual = x @ (np.eye(n) - w)
    residual2 = np.sum(residual ** 2, axis=1)
    # This chooses the worst allowed field separately for each x/round(x).
    # Checking it is stronger than sampling many common future fields.
    actual_change = (
        .5 * np.einsum("bi,ij,bj->b", x, a, x)
        - .5 * np.einsum("bi,ij,bj->b", rounded, a, rounded)
        + delta @ b - h_bound * np.abs(delta).sum(axis=1)
    )
    direct_bound = g * minority - 2 * np.sqrt(d2 * n * minority)
    sharp_bound = (
        .5 * g * residual2
        - np.sqrt(d2 * np.maximum(0.0, residual2 * (n - residual2)))
    )
    assert np.min(actual_change - direct_bound) >= -2e-8
    assert np.min(actual_change - sharp_bound) >= -2e-8
    assert np.min(actual_change) >= -n * per_spin - 2e-8
    assert abs(d2 - d2_reduced) <= 2e-8 * max(1.0, d2)
    strict = g > 0 and g * g > 4 * n * d2
    if strict:
        assert np.min(actual_change[minority > 0]) > 0
    # Block-constant diagonal changes preserve every binary energy difference.
    shift = .5 * np.einsum("bi,ij,bj->b", x, original_a - a, x)
    assert np.ptp(shift) < 2e-8
    # The scalar spectral proposal may be changed later, but the certificate
    # itself is tested against the full Boolean set in these small audits.
    latent = signs(p.shape[1]) @ p.T
    max_regret = 0.0
    for _ in range(12):
        h = rng.uniform(-h_bound, h_bound, n)
        full_e = .5 * np.einsum("bi,ij,bj->b", x, a, x) + x @ (b + h)
        latent_e = .5 * np.einsum("bi,ij,bj->b", latent, a, latent) + latent @ (b + h)
        regret = float(latent_e.min() - full_e.min())
        assert regret <= n * per_spin + 2e-8
        max_regret = max(max_regret, regret)
    return dict(
        n=n, clusters=p.shape[1], full_states=len(x), gamma=gamma,
        alpha=alpha, beta=beta, g=g, d2=d2,
        uniform_regret_bound=n * per_spin,
        strict_alignment_certified=bool(strict),
        sampled_field_max_regret=max_regret,
        worst_pointwise_rounding_loss=max(0.0, float(-actual_change.min())),
        smallest_sharp_inequality_slack=float(np.min(actual_change - sharp_bound)),
    )


def run():
    rng = np.random.default_rng(77194)
    records = []
    for sizes in ((2, 2, 2), (3, 1, 2), (2, 3, 3), (4, 2, 2)):
        p = indicators(sizes)
        n, r = p.shape
        w = (p / p.sum(axis=0)) @ p.T
        normal = np.eye(n) - w
        for trial in range(20):
            raw = rng.normal(size=(n, n)) / np.sqrt(n)
            curvature = (0.2, 2.0, 10.0, 40.0)[trial % 4]
            a_normal = normal @ (raw.T @ raw + curvature * np.eye(n)) @ normal
            coarse = rng.normal(size=(r, r))
            coarse = (coarse + coarse.T) / 2
            np.fill_diagonal(coarse, 0.0)
            lift = p / p.sum(axis=0)
            a_coarse = lift @ coarse @ lift.T
            cross = w @ rng.normal(size=(n, n)) @ normal
            cross_scale = (0.0, 0.05, 0.5, 3.0)[(trial // 4) % 4]
            a = a_normal + a_coarse + cross_scale * (cross + cross.T)
            # The root acquisition fixes this observable diagonal gauge first.
            a = a - np.diag(a.sum(axis=1))
            b = rng.normal(scale=0.1, size=n)
            records.append(audit_case(a, b, 0.15, p, rng))
    # Deliberate failure: positive normal curvature alone does not align spins.
    p = indicators((2, 2))
    w = (p / p.sum(axis=0)) @ p.T
    normal = np.eye(4) - w
    u = np.array([1.0, 1.0, -1.0, -1.0]) / 2
    v = np.array([1.0, -1.0, 0.0, 0.0]) / np.sqrt(2)
    a = normal + np.outer(u, v) + np.outer(v, u)
    counterexample = audit_case(a, np.zeros(4), 0.0, p, rng)
    assert counterexample["g"] > 0
    assert counterexample["sampled_field_max_regret"] > 0.4
    result = dict(
        role="Numerical adversarial audit; acquisition is not simulated here.",
        cases=len(records),
        checked_full_assignments=sum(r["full_states"] for r in records),
        checked_future_fields=12 * len(records),
        strict_alignment_acceptances=sum(r["strict_alignment_certified"] for r in records),
        positive_gap_cases=sum(r["g"] > 0 for r in records),
        maximum_recorded_rounding_loss=max(r["worst_pointwise_rounding_loss"] for r in records),
        worst_sharp_inequality_slack=min(r["smallest_sharp_inequality_slack"] for r in records),
        positive_gap_insufficient_counterexample=counterexample,
        records=records,
    )
    path = Path(__file__).with_name("latent_alignment_audit_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2))


if __name__ == "__main__":
    run()
