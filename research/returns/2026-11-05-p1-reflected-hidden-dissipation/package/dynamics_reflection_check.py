"""Reproduce the explicit CTMC, reflection witness, and triple-law audit.

Run: python3 dynamics_reflection_check.py
Requires NumPy and SciPy. Numerical verification complements the analytic proof.
"""

from itertools import product
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ONE = np.ones(4)
F = np.array([1.0, 1.0, -1.0, -1.0])
H = np.array([1.0, -1.0, 1.0, -1.0])
K = F * H
PI = ONE / 4
REVERSAL = np.eye(4)[[0, 1, 3, 2]]


def generator(a, epsilon):
    if not (a > 0 and 0 < epsilon < a / 2):
        raise ValueError("Need a>0 and 0<epsilon<a/2")
    return -a * (np.eye(4) - np.ones((4, 4)) / 4) + (
        epsilon / 4
    ) * (np.outer(H, F) + np.outer(F, K))


def word_probability(q, word, gaps):
    row = PI * (F == word[0])
    for gap, symbol in zip(gaps, word[1:]):
        row = (row @ expm(q * gap)) * (F == symbol)
    return float(row.sum())


def entropy_rate(q):
    return sum(
        (q[i, j] - q[j, i]) / 4 * math.log(q[i, j] / q[j, i])
        for i in range(4)
        for j in range(i + 1, 4)
    )


def check_instance(a=1.0, epsilon=0.4, t=0.5):
    q = generator(a, epsilon)
    np.testing.assert_allclose(q.sum(axis=0), 0, atol=1e-14)
    np.testing.assert_allclose(q.sum(axis=1), 0, atol=1e-14)
    assert np.all(q[np.triu_indices(4, 1)] > 0)
    assert np.all(q[np.tril_indices(4, -1)] > 0)
    np.testing.assert_allclose(q.T, REVERSAL @ q @ REVERSAL, atol=1e-14)
    np.testing.assert_allclose(q @ F, -a * F + epsilon * H, atol=1e-14)
    np.testing.assert_allclose(q @ H, -a * H, atol=1e-14)
    np.testing.assert_allclose(q @ K, -a * K + epsilon * F, atol=1e-14)

    r = math.exp(-a * t)
    m = r * r * (epsilon * t) ** 2
    probabilities = []
    c_measured = 0.0
    chi2 = 0.0
    triple_error = 0.0
    for u, v, w in product([1, -1], repeat=3):
        p = word_probability(q, (u, v, w), (t, t))
        p_formula = (1 + r * (u * v + v * w) + r * r * u * w + m * u * v * w) / 8
        p_null = (1 + r * (u * v + v * w) + r * r * u * w) / 8
        triple_error = max(triple_error, abs(p - p_formula))
        chi2 += (p - p_null) ** 2 / p_null
        score = float(v == -1) * (u + r) * (w + r)
        c_measured += p * score
        probabilities.append({"word": [u, v, w], "probability": p})
    assert triple_error < 1e-13
    np.testing.assert_allclose(c_measured, -m / 2, atol=1e-14)
    np.testing.assert_allclose(chi2, m * m / (1 - r * r) ** 2, rtol=1e-11)

    # Multiple unequal gaps and five-symbol words test the exact path-reversal
    # symmetry independently of the equal-gap triple formula.
    gaps = [0.13 / a, 0.31 / a, 0.47 / a, 0.73 / a]
    reversal_error = 0.0
    for word in product([1, -1], repeat=5):
        forward = word_probability(q, word, gaps)
        backward = word_probability(q, word[::-1], gaps[::-1])
        reversal_error = max(reversal_error, abs(forward - backward))
    assert reversal_error < 1e-13

    # All-lag pair law is checked at unrelated times rather than inferred from
    # the triple probabilities used above.
    pair_error = 0.0
    for lag in [0.03 / a, 0.2 / a, 0.9 / a, 2.7 / a, 10.0 / a]:
        for u, v in product([1, -1], repeat=2):
            p = word_probability(q, (u, v), (lag,))
            expected = (1 + u * v * math.exp(-a * lag)) / 4
            pair_error = max(pair_error, abs(p - expected))
    assert pair_error < 1e-13

    sigma = entropy_rate(q)
    sigma_formula = epsilon / 2 * math.log((a + 2 * epsilon) / (a - 2 * epsilon))
    np.testing.assert_allclose(sigma, sigma_formula, rtol=1e-13)
    lower_linear = m / t
    lower_nonlinear = epsilon * r * math.atanh(epsilon * t * r)
    assert 0 < lower_linear <= lower_nonlinear <= sigma

    return {
        "a": a,
        "epsilon": epsilon,
        "t": t,
        "Q": q.tolist(),
        "r": r,
        "m": m,
        "reflection_score_mean": c_measured,
        "conditional_covariance": -m,
        "entropy_rate": sigma,
        "lower_bound_linear": lower_linear,
        "lower_bound_nonlinear": lower_nonlinear,
        "chi_square_triple_vs_equilibrium": chi2,
        "maximum_triple_formula_error": triple_error,
        "maximum_five_symbol_reversal_error": reversal_error,
        "maximum_two_time_law_error": pair_error,
        "triple_probabilities": probabilities,
    }


def make_figure(a=1.0, epsilon=0.4):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    q = generator(a, epsilon)
    times = np.linspace(0.0, 3.0 / a, 401)
    r = np.exp(-a * times)
    m = r**2 * (epsilon * times) ** 2
    sigma = entropy_rate(q)
    linear = epsilon**2 * times * r**2
    nonlinear = epsilon * r * np.arctanh(epsilon * times * r)
    sample_times = np.linspace(0, 3.0 / a, 13)
    numerical_pairs = [float(F @ expm(q * t) @ F / 4) for t in sample_times]

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10.5,
        "axes.titlesize": 12,
        "axes.labelsize": 10.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.facecolor": "white",
    })
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.45))
    blue, orange, purple = "#2563eb", "#d97706", "#7c3aed"

    ax = axes[0]
    ax.plot(times, r, color=blue, linewidth=2.5, label="Equilibrium telegraph: $e^{-at}$")
    ax.plot(sample_times, numerical_pairs, "o", markerfacecolor="white",
            markeredgecolor="#111827", markersize=5, label="Four-state model (computed)")
    ax.set(xlabel="Lag $t$", ylabel=r"$\mathbb{E}[Y_0Y_t]$",
           title="A  Every two-time law agrees", ylim=(-0.02, 1.05))
    ax.legend(loc="upper right", fontsize=8.7, frameon=False)
    ax.grid(axis="y", alpha=0.16)

    ax = axes[1]
    ax.axhline(0, color="#6b7280", linestyle="--", linewidth=1.4,
               label="Equilibrium lower limit")
    ax.plot(times, -m, color=orange, linewidth=2.6,
            label=r"$-\epsilon^2t^2e^{-2at}$")
    ax.fill_between(times, -m, 0, color=orange, alpha=0.12)
    ax.set(xlabel="Half-window $t$", ylabel="Conditional covariance",
           title="B  Three-time context reveals driving")
    ax.text(0.98, 0.14, r"$\mathrm{Cov}(Y_{-t},Y_t\mid Y_0=-1)$",
            ha="right", va="center", transform=ax.transAxes, fontsize=10)
    ax.legend(loc="upper right", fontsize=8.7, frameon=False)
    ax.grid(axis="y", alpha=0.16)

    ax = axes[2]
    ax.axhline(sigma, color="#111827", linewidth=1.8,
               label=f"Actual rate: {sigma:.4f}")
    ax.plot(times[1:], linear[1:], color=blue, linewidth=2.6,
            label="Linear certificate")
    ax.plot(times[1:], nonlinear[1:], color=purple, linestyle="--", linewidth=1.8,
            label="Nonlinear certificate")
    ax.set(xlabel="Half-window $t$", ylabel="Entropy rate (log scale)",
           title="C  Guaranteed floor, not exact cost", yscale="log",
           ylim=(5e-4, 0.8))
    ax.legend(loc="center right", fontsize=8.7, frameon=False)
    ax.grid(axis="y", which="major", alpha=0.16)

    fig.suptitle("Hidden driving can be invisible to all two-time data and the observed time arrow",
                 fontsize=14, fontweight="bold", x=0.035, ha="left", y=0.995)
    fig.text(0.035, 0.045,
             "Exact four-state CTMC, a = 1 and ε = 0.4. "
             "The full observed path law is time-reversal symmetric. "
             "Entropy claims assume all microscopic variables are even.",
             fontsize=9.4, color="#4b5563", ha="left")
    fig.tight_layout(rect=(0.018, 0.095, 0.997, 0.925), w_pad=2.1)
    output = Path(__file__).with_name("reflection_results.png")
    fig.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return str(output)


if __name__ == "__main__":
    result = check_instance()
    # Scaling regimes catch convention and rate-rescaling mistakes.
    for a, relative_epsilon, relative_t in [
        (0.2, 0.01, 0.7),
        (1.0, 0.25, math.log(2)),
        (3.7, 0.49, 0.2),
    ]:
        check_instance(a, a * relative_epsilon, relative_t / a)
    result["figure"] = make_figure()
    print(json.dumps(result, indent=2))
