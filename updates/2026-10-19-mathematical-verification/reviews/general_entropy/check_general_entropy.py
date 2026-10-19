"""Independent finite checks of the fixed-observed-state entropy theorem.

This script does not import or run any supplied verification/audit program.
Exact rational identities use Python integers/Fraction; floating matrix checks
use NumPy and a Taylor scaling-and-squaring exponential written here.
Finite checks supplement the proof in report.md; they do not establish it.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import random
import sys

import numpy as np


def exact_cycle_search():
    grid = (1, 2, 4, 6, 8)  # a_i in {1/8, 1/4, 1/2, 3/4, 1}
    counts = {}
    smallest_ratio = float("inf")
    smallest_slack = None
    witness = None
    for size in range(3, 8):
        count = 0
        for a in product(grid, repeat=size):
            edge_sum = sum(a[i] * a[(i + 1) % size] for i in range(size))
            vertex_sum = sum(a)
            slack = vertex_sum ** 2 - 3 * edge_sum
            assert slack >= 0
            count += 1
            if smallest_slack is None or slack < smallest_slack:
                smallest_slack = slack
            ratio = F(vertex_sum ** 2, edge_sum)
            if ratio < smallest_ratio:
                smallest_ratio = ratio
                witness = list(a)
        counts[str(size)] = count
    return {
        "exact_rational_cases": sum(counts.values()),
        "cases_by_cycle_length": counts,
        "grid_denominator": 8,
        "minimum_integer_slack": smallest_slack,
        "minimum_clique_ratio": str(smallest_ratio),
        "minimum_ratio_cycle_grid_numerators": witness,
        "counterexamples": 0,
    }


def exact_stationary_flux_search():
    rng = random.Random(20261019012)
    minimum = {"cycle_conversion_ratio": float("inf"),
               "entropy_circulation_ratio": float("inf"),
               "entropy_two_smallest_ratio": float("inf")}
    count = 0
    for size in range(3, 9):
        edges = [(i, j) for i in range(size) for j in range(i + 1, size)]
        for _ in range(100):
            weights = [rng.randint(1, 1000) for i in range(size)]
            p = [F(w, sum(weights)) for w in weights]
            current = {e: F(0) for e in edges}
            for _ in range(rng.randint(1, 2 * size)):
                cycle = rng.sample(range(size), rng.randint(3, size))
                amplitude = F(rng.randint(1, 9), 7)
                for i, j in zip(cycle, cycle[1:] + cycle[:1]):
                    current[min(i, j), max(i, j)] += amplitude * (1 if i < j else -1)
            divergence = [F(0) for i in range(size)]
            for (i, j), z in current.items():
                divergence[i] += z
                divergence[j] -= z
            assert divergence == [F(0)] * size
            traffic = {e: abs(z) + F(rng.randint(1, 9), 9)
                       for e, z in current.items()}
            total_exit = F(0)
            traffic_identity = F(0)
            n_norm = F(0)
            sigma = 0.0
            ell = 0.0
            kappa = F(0)
            for i, j in edges:
                z, c = current[i, j], traffic[i, j]
                a, b = (c + z) / 2, (c - z) / 2
                h = (p[i] + p[j]) / (2 * p[i] * p[j])
                total_exit += a / p[i] + b / p[j]
                traffic_identity += h * c
                n_norm += z * z / (p[i] * p[j])
                ell += abs(float(z)) * math.sqrt(float(h))
                sigma += float(z) * math.log(float(a / b))
                kappa = max(kappa, c / (2 * p[i] * p[j]))
            assert total_exit == traffic_identity
            s = sum(sorted(p)[:2])
            assert kappa <= total_exit / s
            if not n_norm:
                continue
            m = min(p)
            ratios = {
                "cycle_conversion_ratio": ell ** 2 / float(3 * m * n_norm),
                "entropy_circulation_ratio": sigma * float(total_exit) / float(6 * m * n_norm),
                "entropy_two_smallest_ratio": sigma * float(total_exit) / float(s * n_norm),
            }
            for key, value in ratios.items():
                assert value >= 1 - 1e-12, (key, value)
                minimum[key] = min(minimum[key], value)
            count += 1
    sharpness = []
    for k in range(1, 7):
        epsilon = 10.0 ** (-k)
        # Uniform three-state cycle, q_forward=1+eps, q_back=1-eps.
        ratio = (math.log1p(epsilon) - math.log1p(-epsilon)) / (2 * epsilon)
        assert ratio >= 1
        sharpness.append({"epsilon": epsilon, "entropy_conversion_ratio": ratio})
    return {"rational_stationary_cases": count,
            "exact_identities": ["divergence zero", "T=sum h*c", "kappa<=T/s"],
            "smallest_numeric_ratios": minimum,
            "uniform_triangle_sharpness": sharpness,
            "counterexamples": 0}


def matrix_exp(x):
    norm = float(np.linalg.norm(x, ord=np.inf))
    scaling = max(0, math.ceil(math.log2(max(norm, 0.25) / 0.25)))
    y = x / (2 ** scaling)
    term = np.eye(len(x))
    answer = term.copy()
    for k in range(1, 201):
        term = term @ y / k
        answer += term
        if float(np.linalg.norm(term, ord=np.inf)) < 1e-18:
            break
    else:
        raise AssertionError("Taylor exponential did not converge")
    for _ in range(scaling):
        answer = answer @ answer
    return answer


def entropy(q, p):
    out = 0.0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            a, b = p[i] * q[i, j], p[j] * q[j, i]
            if a == b == 0:
                continue
            if a <= 0 or b <= 0:
                return float("inf")
            out += (a - b) * math.log(a / b)
    return out


def matrix_cases():
    a0, b0 = 8 * math.log(2), 18 * math.log(2)
    v = np.array([1, -1, 0, 0]) / math.sqrt(2)
    u = np.array([1, 1, -1, -1]) / 2
    w = np.array([0, 0, 1, -1]) / math.sqrt(2)
    stationary = np.ones((4, 4)) / 4
    h0 = -a0 * np.outer(v, v) - b0 * (np.outer(u, u) + np.outer(w, w))
    alpha0 = 2 * math.pi / math.sqrt(7)
    r0 = math.sqrt(alpha0 ** 2 + 4 * math.pi ** 2)
    results = []

    def check(q, h, pmat, p, tau, branch_square_sum, label):
        a = np.sqrt(p)[:, None] * q / np.sqrt(p)[None, :]
        symmetric = (a + a.T) / 2
        skew = (a - a.T) / 2
        defect = symmetric - h
        k2 = float(np.sum(skew ** 2))
        u2 = float(np.sum(defect ** 2))
        neg = np.minimum(h - np.diag(np.diag(h)), 0)
        d2 = float(np.sum(neg ** 2))
        branch_term = 4 * math.pi ** 2 / tau ** 2 * branch_square_sum
        trace_error = abs(k2 - u2 - branch_term)
        exp_error = float(np.max(np.abs(matrix_exp(tau * q) - pmat)))
        stat_error = float(np.max(np.abs(p @ q)))
        row_error = float(np.max(np.abs(q.sum(axis=1))))
        total_exit = -float(np.trace(q))
        offdiag = q[~np.eye(len(q), dtype=bool)]
        positive = offdiag[offdiag > 0]
        sig = entropy(q, p)
        rhs = max(12 * min(p), 2 * sum(sorted(p)[:2])) / total_exit * (d2 + 8 * math.pi ** 2 / tau ** 2)
        assert min(offdiag) >= -1e-12
        assert exp_error < 1e-11
        assert stat_error < 1e-11 and row_error < 1e-11
        assert trace_error < 1e-9 * max(1, k2 + u2 + branch_term)
        assert k2 >= d2 + 8 * math.pi ** 2 / tau ** 2 - 1e-9
        assert sig >= rhs
        return {"label": label, "n": len(p), "tau": tau,
                "p": p.tolist(), "T": total_exit, "d_squared": d2,
                "sigma": sig, "main_lower_bound": rhs,
                "branch_integer_square_sum": branch_square_sum,
                "trace_identity_absolute_error": trace_error,
                "exp_max_absolute_error": exp_error,
                "stationarity_max_absolute_error": stat_error,
                "smallest_positive_offdiagonal_rate": float(min(positive)),
                "nonnormal_commutator_frobenius": float(np.linalg.norm(a @ a.T - a.T @ a))}

    for winding in (1, 2, 3):
        pmat = stationary + 2.0 ** (-8 * winding) * np.outer(v, v) + 2.0 ** (-18 * winding) * (np.outer(u, u) + np.outer(w, w))
        for eta in (-0.04, 0.0, 0.04):
            qbase = (h0 + alpha0 * (np.outer(u, u) - np.outer(w, w))
                     + r0 * math.exp(eta) * np.outer(u, w)
                     - r0 * math.exp(-eta) * np.outer(w, u))
            for tau in (0.25, 1.0, 2.5):
                results.append(check(winding / tau * qbase,
                                     winding / tau * h0,
                                     pmat, np.ones(4) / 4,
                                     tau, 2 * winding ** 2,
                                     f"four_state_k{winding}_eta{eta}"))

    # Reducible observations: the stationary block mixture is deliberately
    # nonunique, but the specified full-support p must stay stationary for Q.
    qbase = h0 + alpha0 * (np.outer(u, u) - np.outer(w, w)) + r0 * (np.outer(u, w) - np.outer(w, u))
    pmat4 = stationary + 2.0 ** -8 * np.outer(v, v) + 2.0 ** -18 * (np.outer(u, u) + np.outer(w, w))
    for p in (np.array([0.125] * 4 + [0.1, 0.4]),
              np.array([0.249975] * 4 + [0.0001])):
        n = len(p)
        q, h, pmat = np.zeros((n, n)), np.zeros((n, n)), np.eye(n)
        q[:4, :4], h[:4, :4], pmat[:4, :4] = qbase, h0, pmat4
        results.append(check(q, h, pmat, p, 1.0, 2, "reducible_full_support"))
    return {"compatible_nonnormal_cases": len(results), "cases": results,
            "all_passed": True,
            "scope": "Four-state witness formula is taken from supplied proof; all numerical implementation and tests are newly written."}


def main():
    out = {"python": sys.version.split()[0], "numpy": np.__version__,
           "random_seed": 20261019012,
           "cycle_search": exact_cycle_search(),
           "stationary_flux_search": exact_stationary_flux_search(),
           "matrix_checks": matrix_cases(),
           "interpretation": "Scoped finite checks, not proof, certified interval bounds, originality, or physical validation."}
    target = Path(__file__).with_name("checks.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"output": str(target),
                      "rational_cycle_cases": out["cycle_search"]["exact_rational_cases"],
                      "rational_flux_cases": out["stationary_flux_search"]["rational_stationary_cases"],
                      "compatible_matrix_cases": out["matrix_checks"]["compatible_nonnormal_cases"],
                      "all_passed": True}, indent=2))


if __name__ == "__main__":
    main()
