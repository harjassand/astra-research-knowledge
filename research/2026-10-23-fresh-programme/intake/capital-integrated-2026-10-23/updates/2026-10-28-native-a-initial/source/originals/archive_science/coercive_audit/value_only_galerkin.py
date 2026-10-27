"""Owned value-only scalar acquisition diagnostic.

The learner receives only an h-value callback and a supplied Lipschitz bound.
Exact source mean/derivatives/canonical K occur only in the separate evaluator
after the rational polynomial coefficients have been frozen on disk.
Numerical quadrature results are diagnostics until independently certified.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite_e import hermegauss
from numpy.polynomial.legendre import leggauss
from scipy.special import roots_genlaguerre


ROOT = Path(__file__).resolve().parent
DEGREE = 10
TRAIN_GH = 48
RHO_ORDER = 32
RADIAL_ORDER = 24
LIPSCHITZ = 7 / 20
DYADIC_BITS = 60


class ValueOracle:
    def __init__(self, function):
        self.function = function
        self.calls = 0

    def __call__(self, x):
        a = np.asarray(x, dtype=float)
        self.calls += a.size
        return self.function(a)


def gaussian_rule(order):
    x, w = hermegauss(order)
    return x, w / math.sqrt(2 * math.pi)


def normalized_hermites(x, degree):
    x = np.asarray(x)
    result = np.empty((len(x), degree + 1))
    result[:, 0] = 1
    if degree:
        result[:, 1] = x
    for k in range(1, degree):
        result[:, k + 1] = (x * result[:, k] - math.sqrt(k) * result[:, k - 1]) / math.sqrt(k + 1)
    return result


def basis_data(g, z, indices):
    degree = max(i + j for i, j in indices)
    hg = normalized_hermites(g, degree)
    hz = normalized_hermites(z, degree)
    arrays = [np.zeros((len(g), len(indices))) for _ in range(6)]
    p, pg, pz, pgg, pgz, pzz = arrays
    for col, (i, j) in enumerate(indices):
        p[:, col] = hg[:, i] * hz[:, j]
        if i:
            pg[:, col] = math.sqrt(i) * hg[:, i - 1] * hz[:, j]
        if j:
            pz[:, col] = math.sqrt(j) * hg[:, i] * hz[:, j - 1]
        if i > 1:
            pgg[:, col] = math.sqrt(i * (i - 1)) * hg[:, i - 2] * hz[:, j]
        if i and j:
            pgz[:, col] = math.sqrt(i * j) * hg[:, i - 1] * hz[:, j - 1]
        if j > 1:
            pzz[:, col] = math.sqrt(j * (j - 1)) * hg[:, i] * hz[:, j - 2]
    return arrays


def acquired_k_values(oracle, gnodes):
    """Deterministic cubature of the source's legal two-value secant."""
    rho, wrho = leggauss(RHO_ORDER)
    rho, wrho = (rho + 1) / 2, wrho / 2
    t, wt = roots_genlaguerre(RADIAL_ORDER, 0.5)
    radial = np.sqrt(2 * t)
    wt = wt / math.gamma(1.5)
    centers = gnodes[:, None, None] * rho[None, :, None]
    radius = np.sqrt(1 - rho * rho)[None, :, None] * radial[None, None, :]
    plus = oracle(centers + radius)
    minus = oracle(centers - radius)
    secant = (plus - minus) / (2 * radius)
    return np.einsum("ijk,j,k->i", secant, wrho, wt)


def acquire_polynomial(oracle):
    """No true mean, h derivative or exact K is available in this function."""
    nodes, wg = gaussian_rule(TRAIN_GH)
    hnodes = oracle(nodes)
    mu_fit = float(wg @ hnodes)
    knodes = acquired_k_values(oracle, nodes)
    g, z = np.meshgrid(nodes, nodes, indexing="ij")
    weights = np.outer(wg, wg).ravel()
    g, z = g.ravel(), z.ravel()
    h = np.repeat(hnodes, TRAIN_GH)
    k = np.repeat(knodes, TRAIN_GH)
    indices = [(i, total - i) for total in range(DEGREE + 1) for i in range(total + 1)]
    p, pg, pz, *_ = basis_data(g, z, indices)
    u = p * (h + z - mu_fit)[:, None] - pg * k[:, None] - pz
    whh = weights * h * (h - mu_fit)
    wkh = weights * k * h
    gram = u.T @ (weights[:, None] * u)
    gram += p.T @ (weights[:, None] * p)
    gram += p.T @ (whh[:, None] * p)
    gram -= pg.T @ (wkh[:, None] * p) + p.T @ (wkh[:, None] * pg)
    gram = (gram + gram.T) / 2
    rhs = -p.T @ whh + pg.T @ wkh
    coeff = np.linalg.solve(gram, rhs)

    # Freeze an ordinary exact rational polynomial in unnormalized He_i He_j.
    # The fixed small-coefficient threshold is a learner choice, not truth fitting.
    denom = 2**DYADIC_BITS
    frozen = []
    normalized = []
    for (i, j), value in zip(indices, coeff):
        if abs(value) < 1e-12:
            value = 0.0
        unnormalized = value / math.sqrt(math.factorial(i) * math.factorial(j))
        numerator = round(unnormalized * denom)
        frozen.append((i, j, numerator, denom))
        normalized.append(numerator / denom * math.sqrt(math.factorial(i) * math.factorial(j)))
    with (ROOT / "galerkin_S_rational.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["hermite_G_degree", "hermite_Z_degree", "numerator", "denominator"])
        writer.writerows(frozen)
    with (ROOT / "galerkin_acquired_values.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["G_node", "quadrature_weight", "h_value", "K_value_cubature"])
        writer.writerows(zip(nodes, wg, hnodes, knodes))
    eigenvalues = np.linalg.eigvalsh(gram)
    info = {
        "dimension": len(indices),
        "query_count": oracle.calls,
        "mean_fit": mu_fit,
        "smallest_gram_eigenvalue": float(eigenvalues[0]),
        "gram_condition": float(eigenvalues[-1] / eigenvalues[0]),
        "linear_solve_residual": float(np.linalg.norm(gram @ coeff - rhs)),
    }
    return indices, np.asarray(normalized), info


def evaluate_truth_after_freeze(indices, coeff, order):
    """Post-fit evaluator: analytic cosine information is explicitly allowed here."""
    nodes, w = gaussian_rule(order)
    g, z = np.meshgrid(nodes, nodes, indexing="ij")
    weights = np.outer(w, w).ravel()
    g, z = g.ravel(), z.ravel()
    rho, wrho = leggauss(128)
    rho, wrho = (rho + 1) / 2, wrho / 2
    kval = -LIPSCHITZ * (
        np.sin(nodes[:, None] * rho[None, :])
        * np.exp(-(1 - rho**2) / 2)[None, :]
    ) @ wrho
    k = np.repeat(kval, order)
    h = LIPSCHITZ * np.cos(g)
    hp = -LIPSCHITZ * np.sin(g)
    mu = LIPSCHITZ * math.exp(-0.5)
    s, sg, sz, sgg, sgz, szz = (a @ coeff for a in basis_data(g, z, indices))
    u = s * (h + z - mu) - k * sg - sz
    residual = k * hp
    full_error = (
        2 * s + z * sz - szz + (1 + 2 * s) * k * hp
        + (z * sg - 2 * sgz) * k + 2 * sg * k * (h - mu)
        - (g * sg + sgg) * k * k + sz * (h - mu)
    )
    norm = lambda value: math.sqrt(float(weights @ (value * value)))
    en, rn, un, sn, sgn = map(norm, [full_error, residual, u, s, sg])
    random_var_bound = LIPSCHITZ**2 * (sn**2 + sgn**2)
    moment_bound = un**2 + random_var_bound
    c2 = math.log(2) / math.sqrt(2)
    c3 = math.sqrt(6) * (1 - math.pi / 4)
    c4 = math.sqrt(2) / 2
    phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
    sharp_c2 = phi(1) * math.log(2)
    sharp_c3 = (phi(0) + 4 * phi(math.sqrt(3))) * (1 - math.pi / 4)
    sharp_c4 = phi(1)
    return {
        "quadrature_order": order,
        "full_equation_residual_L2": en,
        "initial_R_L2": rn,
        "true_u_L2": un,
        "S_L2": sn,
        "S_G_L2": sgn,
        "four_query_variance_upper_bound": random_var_bound,
        "four_query_second_moment_upper_bound": moment_bound,
        "conservative_TV_expression": c2 * en + c3 * rn * un + c4 * moment_bound,
        "sharp_scalar_TV_expression": sharp_c2 * en + sharp_c3 * rn * un + sharp_c4 * moment_bound,
    }


def four_query_runtime(oracle, indices, coeff, size, seed=20261027):
    rng = np.random.default_rng(seed)
    g, z, gp, noise = rng.normal(size=(4, size))
    hg, hgp = oracle(g), oracle(gp)
    uniform_seeds = rng.normal(size=(3, size))
    seed_norm = np.linalg.norm(uniform_seeds, axis=0)
    ratio = np.divide(uniform_seeds[0], seed_norm,
                      out=np.zeros_like(seed_norm), where=seed_norm > 0)
    rho = np.clip((1 + ratio) / 2, 0, 1)
    radial = np.sqrt(np.maximum(0, 1 - rho * rho)) * np.linalg.norm(
        rng.normal(size=(3, size)), axis=0)
    difference = oracle(rho * g + radial) - oracle(rho * g - radial)
    # Fixed null-event convention; retain exactly four calls even at radius 0.
    jhat = np.divide(difference, 2 * radial,
                     out=np.zeros_like(radial), where=radial > 0)
    s, sg, sz, *_ = (a @ coeff for a in basis_data(g, z, indices))
    uhat = s * (hg - hgp + z) - sg * jhat - sz
    return hg + z + uhat + noise, uhat


def main():
    oracle = ValueOracle(lambda x: LIPSCHITZ * np.cos(x))
    indices, coeff, info = acquire_polynomial(oracle)
    # Both truth evaluation and runtime explicitly reload the same frozen file
    # read by the exact rational verifier. Floating normalization is diagnostic;
    # the ideal program uses its rational unnormalized Hermite coefficients.
    with (ROOT / "galerkin_S_rational.csv").open() as inp:
        frozen_rows = list(csv.DictReader(inp))
    indices = [(int(r["hermite_G_degree"]), int(r["hermite_Z_degree"])) for r in frozen_rows]
    coeff = np.asarray([
        int(r["numerator"]) / int(r["denominator"])
        * math.sqrt(math.factorial(i) * math.factorial(j))
        for r, (i, j) in zip(frozen_rows, indices)
    ])
    # This separation is deliberate: the evaluator starts after S is frozen.
    evaluations = [evaluate_truth_after_freeze(indices, coeff, order) for order in [64, 96, 128]]
    with (ROOT / "galerkin_full_residual_quadrature.csv").open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=evaluations[0].keys())
        writer.writeheader()
        writer.writerows(evaluations)
    runtime_oracle = ValueOracle(lambda x: LIPSCHITZ * np.cos(x))
    outputs, corrections = four_query_runtime(runtime_oracle, indices, coeff, 100000)
    assert runtime_oracle.calls == 4 * len(outputs)
    report = ["VALUE-ONLY GALERKIN DIAGNOSTIC", "Training used only charged h values."]
    report += [f"{key}: {value}" for key, value in info.items()]
    report += [f"{key}: {value}" for key, value in evaluations[-1].items()]
    report += [
        f"runtime_outputs: {len(outputs)}",
        f"runtime_h_queries: {runtime_oracle.calls}",
        f"diagnostic_output_mean: {outputs.mean()}",
        f"diagnostic_output_variance: {outputs.var()}",
        f"diagnostic_correction_second_moment: {np.mean(corrections**2)}",
        "The output moments are floating-point execution checks, not full-law TV certificates.",
        "The mathematical law certificate concerns exact Gaussian seeds and exact h values.",
        "Finite-bit output must instead be compared to a commonly rounded target; no bit-error budget is supplied here.",
        "The integral values above remain numerical until separate tail/roundoff certification.",
        "No query-efficiency or advantage over scalar FORS/direct integration is claimed.",
    ]
    result = "\n".join(report) + "\n"
    (ROOT / "VALUE_ONLY_GALERKIN_RESULTS.txt").write_text(result)
    print(result, end="")


if __name__ == "__main__":
    main()
