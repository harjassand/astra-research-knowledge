#!/usr/bin/env python3
"""Static noisy-majority regenerator: finite checks, not a uniform proof.

Run: python noisy_interface_work/classical_tree_regenerator.py

The ideal reference leaves exist only in the coupling. Every actual wire and
voter is noisy. A separately paid FT fanout supplies the stated LS(q) raw copies.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
Q, E, V, BAR = 0.01, 0.001, 0.001, 0.02
MAX_HEIGHT = 20


def F(u: float) -> float:
    y = E + (1 - 2 * E) * u
    return V + (1 - 2 * V) * (3 * y * y - 2 * y * y * y)


def iid_errors(m: int, p: float) -> np.ndarray:
    return np.array([p ** s.bit_count() * (1 - p) ** (m - s.bit_count())
                     for s in range(1 << m)])


def correlated_errors(m: int) -> np.ndarray:
    """E=A OR B, with A LS(q/2), independent paired flags B LS(q/2)."""
    assert m % 2 == 0
    a = Q / 2
    pair = [(1 - a * a) * (1 - a) ** 2,
            (1 - a * a) * a * (1 - a),
            (1 - a * a) * a * (1 - a),
            a * a + (1 - a * a) * a * a]
    return np.array([math.prod(pair[(s >> j) & 3] for j in range(0, m, 2))
                     for s in range(1 << m)])


def mixed_ratio(joint: np.ndarray, m: int, d: float, u: float) -> float:
    states = np.arange(1 << m)
    difference = states[:, None] ^ states[None, :]
    union = states[:, None] | states[None, :]
    maximum = 0.0
    for choice in itertools.product(range(3), repeat=m):
        A = sum(1 << i for i, value in enumerate(choice) if value == 1)
        B = sum(1 << i for i, value in enumerate(choice) if value == 2)
        if not (A | B):
            continue
        event = ((difference & A) == A) & ((union & B) == B)
        ratio = float(joint[event].sum()) / (d ** A.bit_count() * u ** B.bit_count())
        maximum = max(maximum, ratio)
    return maximum


def exact_correlated_check() -> dict:
    """Enumerate six correlated actual leaves, ideal reference, two voters."""
    actual = correlated_errors(6)
    reference = np.zeros(64)
    reference[0] = 1
    joint = actual[:, None] * reference[None, :]
    states = np.arange(64)
    max_ls = max(float(actual[(states & s) == s].sum()) / Q ** s.bit_count()
                 for s in range(1, 64))
    initial_mixed = mixed_ratio(joint, 6, Q, Q)
    majority = np.array([int((s & 7).bit_count() >= 2)
                         | (int(((s >> 3) & 7).bit_count() >= 2) << 1)
                         for s in states])
    wire_probs, vote_probs = iid_errors(6, E), iid_errors(2, V)
    parents = np.zeros((4, 4))
    # Pair (2,3) crosses the two parent subtrees: this is a joint check,
    # not an independent-input marginal calculation.
    for A in states:
        weights = actual[A] * wire_probs
        parent_A, parent_B = majority[A ^ states], majority[states]
        for votes in range(4):
            indices = (parent_A ^ votes) * 4 + (parent_B ^ votes)
            parents += np.bincount(indices, weights=weights * vote_probs[votes],
                                   minlength=16).reshape(4, 4)
    d1 = (3 * V + 6 * (Q + E)) * Q
    u1 = V + 3 * (Q + E) ** 2
    final_mixed = mixed_ratio(parents, 2, d1, u1)
    reference_residual = float(np.linalg.norm(parents.sum(axis=0) - iid_errors(2, F(0)), 1))
    assert max_ls <= 1 + 1e-12 and initial_mixed <= 1 + 1e-12
    assert final_mixed <= 1 + 1e-12 and reference_residual < 1e-12
    return {"leaves": 6, "parents": 2,
            "initial_ls_max_nonempty_ratio": max_ls,
            "initial_mixed_max_nonempty_ratio": initial_mixed,
            "parent_mixed_max_nonempty_ratio": final_mixed,
            "reference_product_BSC_l1_residual": reference_residual,
            "parent_joint_distribution_actual_reference": parents.tolist(),
            "scope": "All support events checked for this explicit correlated input. Not an enumeration of every LS distribution."}


def exact_pair_step(joint: np.ndarray) -> np.ndarray:
    """Exact pair recursion when distinct child pairs are independent."""
    wire = (1 - E) * joint + E * joint[::-1]
    output = np.zeros(4)
    for a, b, c in itertools.product(range(4), repeat=3):
        x = int((a >> 1) + (b >> 1) + (c >> 1) >= 2)
        y = int((a & 1) + (b & 1) + (c & 1) >= 2)
        output[2 * x + y] += wire[a] * wire[b] * wire[c]
    result = (1 - V) * output + V * output[::-1]
    # Tensoring three child distributions otherwise triples normalization
    # roundoff at every level; restore the mathematically unit mass.
    return result / result.sum()


def sufficient_bounds() -> dict:
    assert Q <= BAR and V + 3 * (BAR + E) ** 2 <= BAR
    alpha = 3 * V + 6 * (BAR + E)
    universal_alpha = 0.21
    assert alpha <= universal_alpha < 1
    a = Q / 2
    actual_marginal = a + (1 - a) * a * a
    pair = np.array([1 - actual_marginal, 0.0, actual_marginal, 0.0])
    d, d_direct, u, reference_error = Q, Q, Q, 0.0
    rows = []
    for level in range(MAX_HEIGHT + 1):
        exact_d = float(pair[1] + pair[2])
        assert exact_d <= d_direct * (1 + 1e-9) + 1e-90
        assert d_direct <= d * (1 + 1e-12)
        assert d <= Q * universal_alpha ** level * (1 + 1e-12)
        assert abs(float(pair[1] + pair[3]) - reference_error) < 1e-12
        rows.append({"height": level, "reference_BSC_r_L": reference_error,
                     "union_ls_bound": u, "generic_mixed_disagreement_bound": d,
                     "direct_flip_mixed_disagreement_bound": d_direct,
                     "universal_geometric_bound": Q * universal_alpha ** level,
                     "exact_sampled_law_disagreement": exact_d,
                     "exact_sampled_law_actual_error": float(pair[2] + pair[3])})
        d, d_direct, u = ((3 * V + 6 * (u + E)) * d,
                         6 * (u + E) * d_direct,
                         V + 3 * (u + E) ** 2)
        reference_error = F(reference_error)
        pair = exact_pair_step(pair)
    outputs, tolerance = 1000, 1e-6
    uniform_height = math.ceil(math.log(outputs * Q / tolerance) / -math.log(universal_alpha))
    iterated_height = next(row["height"] for row in rows
                           if outputs * row["generic_mixed_disagreement_bound"] <= tolerance)
    return {"initial_d0_equals_u0": Q, "union_basin": BAR,
            "union_basin_image_bound": V + 3 * (BAR + E) ** 2,
            "parameter_specific_generic_alpha": alpha,
            "universal_alpha_for_q_e_v_at_most_0_01": universal_alpha,
            "polynomial_leaf_exponent": math.log(3) / math.log(1 / universal_alpha),
            "rows": rows,
            "resource_example": {"outputs": outputs, "global_coupling_tolerance": tolerance,
                                 "height_from_universal_bound": uniform_height,
                                 "leaves_per_output_from_universal_bound": 3 ** uniform_height,
                                 "height_from_iterated_bound": iterated_height,
                                 "leaves_per_output_from_iterated_bound": 3 ** iterated_height,
                                 "scope": "Only raw input-copy counts. Upstream FT fanout, gates, wires, buffers, and reset remain paid."}}


def simulate_forest() -> dict:
    seed, repetitions, roots, height = 20261105, 100, 4096, 5
    rng = np.random.default_rng(seed)
    a, leaves = Q / 2, 3 ** height
    names = ["actual_error", "reference_error", "disagreement", "union_error"]
    means = {name: np.zeros((repetitions, height + 1)) for name in names}
    counts = {name: np.zeros(height + 1, dtype=np.int64) for name in names}
    for rep in range(repetitions):
        actual = rng.random((roots, leaves)) < a
        pair_flags = rng.random((roots // 2, leaves)) < a * a
        actual |= np.repeat(pair_flags, 2, axis=0)
        reference = np.zeros_like(actual)
        for level in range(height + 1):
            for name, array in zip(names, [actual, reference, actual ^ reference, actual | reference]):
                count = int(array.sum())
                counts[name][level] += count
                means[name][rep, level] = count / array.size
            if level == height:
                break
            wire = rng.random(actual.shape) < E
            actual ^= wire
            reference ^= wire
            actual = actual.reshape(roots, -1, 3).sum(axis=2) >= 2
            reference = reference.reshape(roots, -1, 3).sum(axis=2) >= 2
            vote = rng.random(actual.shape) < V
            actual ^= vote
            reference ^= vote
    rows = []
    for level in range(height + 1):
        row = {"height": level, "observed_nodes": repetitions * roots * 3 ** (height - level)}
        for name in names:
            row[name + "_count"] = int(counts[name][level])
            row[name + "_mean"] = float(means[name][:, level].mean())
            row[name + "_monte_carlo_se"] = float(means[name][:, level].std(ddof=1) / math.sqrt(repetitions))
        rows.append(row)
    return {"seed": seed, "independent_repetitions": repetitions,
            "roots_per_repetition": roots, "height": height, "leaves_per_root": leaves,
            "initial_law": "A OR B: iid A Bern(q/2), with each paired all-flip flag B Bern((q/2)^2) shared by corresponding leaves of two distinct output trees. This correlated law is LS(q).",
            "reference_law": "Exact reference leaves only in the coupling; every subsequent wire/voter is noisy and shared with the actual computation.",
            "uncertainty": "Standard errors use independent repetition means and respect correlations inside each forest.",
            "scope": "Finite estimates for one explicitly correlated LS law. Zero observed disagreements do not certify a rare-event rate or the uniform theorem.",
            "rows": rows}


def main() -> None:
    fixed_point = brentq(lambda u: F(u) - u, 0, BAR, xtol=5e-16, rtol=1e-14)
    mp.mp.dps = 80
    ee, vv = mp.mpf(str(E)), mp.mpf(str(V))
    def ff(u):
        y = ee + (1 - 2 * ee) * u
        return vv + (1 - 2 * vv) * (3 * y * y - 2 * y * y * y)
    precise_fixed_point = mp.findroot(lambda u: ff(u) - u, (vv, 2 * vv))
    exact = exact_correlated_check()
    bounds = sufficient_bounds()
    experiment = simulate_forest()
    result = {"title": "Static classical regenerator with ideal comparison leaves",
              "command": "python noisy_interface_work/classical_tree_regenerator.py",
              "scope": "Finite algebra, exhaustive small correlated-input checks, and scoped Monte Carlo. The uniform theorem is the mixed-LS proof, not an empirical inference. No actual ideal classical port is assumed.",
              "parameters": {"initial_ls_q": Q, "wire_BSC_e": E, "voter_flip_v": V,
                             "reference_rule": "r_0=0; r_(l+1)=F(r_l)",
                             "optional_fixed_point": fixed_point,
                             "optional_fixed_point_80_digit": mp.nstr(precise_fixed_point, 55)},
              "all_deterministic_checks_passed": True,
              "exact_correlated_check": exact, "sufficient_recursions": bounds,
              "finite_forest_experiment": experiment}
    (OUT / "classical_tree_regenerator.json").write_text(json.dumps(result, indent=2) + "\n")
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.7), constrained_layout=True)
    rows = bounds["rows"]
    levels = [row["height"] for row in rows]
    for key, color, style, label in [
        ("universal_geometric_bound", "#6f7681", "--", "Uniform bound q (0.21)^L"),
        ("generic_mixed_disagreement_bound", "#156b55", "-", "Iterated mixed-LS bound"),
        ("exact_sampled_law_disagreement", "#9c3c25", "-", "Exact recursion for the sampled input law")]:
        axes[0].semilogy(levels, [row[key] for row in rows], color=color,
                         ls=style, lw=2, label=label)
    axes[0].set(xlabel="Tree height L", ylabel="Coupling disagreement probability",
                title="Correlated incoming history is forgotten", xlim=(0, MAX_HEIGHT))
    axes[0].legend(frameon=False, fontsize=8, loc="upper right")
    axes[0].grid(alpha=0.18)
    sample = experiment["rows"]
    for key, color, label in [("actual_error", "#9c3c25", "Correlated LS input: finite forest mean"),
                              ("reference_error", "#156b55", "Noisy reference with ideal comparison leaves")]:
        selected = sample if key == "actual_error" else sample[1:]
        h = np.array([r["height"] for r in selected])
        mean = np.array([r[key + "_mean"] for r in selected])
        se = np.array([r[key + "_monte_carlo_se"] for r in selected])
        axes[1].semilogy(h, mean, marker="o", color=color, lw=1.8, label=label)
        axes[1].fill_between(h, mean - 2 * se, mean + 2 * se, color=color, alpha=0.15)
    axes[1].semilogy(levels[1:6], [rows[l]["reference_BSC_r_L"] for l in range(1, 6)],
                     ls="--", color="#6f7681", lw=1.2, label="Known remaining noise r_L")
    axes[1].set(xlabel="Tree height L", ylabel="Marginal bit-error probability",
                title="A known nonzero endpoint error remains", xlim=(0, experiment["height"]))
    axes[1].text(0.04, 0.58, "100 independent forests; 4,096 outputs each\nShading: ±2 Monte Carlo standard errors",
                 transform=axes[1].transAxes, fontsize=8.5)
    axes[1].legend(frameon=False, fontsize=7.8, loc="upper right")
    axes[1].grid(alpha=0.18)
    fig.suptitle("Static noisy-majority regeneration — fixed component errors", fontsize=13, fontweight="bold")
    fig.savefig(OUT / "classical_tree_regenerator.png", dpi=200)
    fig.savefig(OUT / "classical_tree_regenerator.pdf")
    plt.close(fig)
    print(json.dumps({"deterministic_checks_passed": True,
                      "exact_checks": {key: value for key, value in exact.items()
                                       if key not in ("parent_joint_distribution_actual_reference", "scope")},
                      "resource_example": bounds["resource_example"],
                      "root_reference_BSC_r_L": rows[experiment["height"]]["reference_BSC_r_L"],
                      "finite_root_statistics": sample[-1]}, indent=2))


if __name__ == "__main__":
    main()
