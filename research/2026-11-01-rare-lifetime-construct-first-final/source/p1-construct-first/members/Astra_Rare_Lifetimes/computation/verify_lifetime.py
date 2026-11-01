"""Numerical checks of the imaginary-frequency and full-lifetime certificate.

These finite checks are independent support, not proof or an accuracy
guarantee on arbitrary floating-point phase-type calculations.  Every tested
generator has symmetric-part gap at least one by explicit domination of
the complete-refresh chain with invariant distribution pi.
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm


def run_case(seed, p, circulation):
    rng = np.random.default_rng(seed)
    n, k = 8, 2
    pi = rng.uniform(0.5, 1.5, n)
    pi[:k] *= p / pi[:k].sum()
    pi[k:] *= (1.0 - p) / pi[k:].sum()
    a = rng.uniform(1.0, 4.0, (n, n))
    a = (a + a.T) / 2.0
    flow = pi[:, None] * pi[None, :] * a
    np.fill_diagonal(flow, 0.0)
    if circulation:
        # Nonnegative directed cycles preserve the prescribed pi and cannot
        # decrease the symmetric energy.  Their coefficients scale with p
        # only for cycles involving rare states, keeping all rates bounded.
        for cycle, coeff in [([0, 2, 1, 4, 5], p / 3),
                             ([2, 3, 5, 6, 7], 0.08)]:
            for i, j in zip(cycle, cycle[1:] + cycle[:1]):
                flow[i, j] += coeff
    Q = flow / pi[:, None]
    np.fill_diagonal(Q, -Q.sum(axis=1))
    L = -Q
    B = np.arange(k, n)
    LB = L[np.ix_(B, B)]
    one = np.ones(len(B))
    def centered_potential(Lop, s):
        # The ordinary killed solve becomes poorly conditioned as p shrinks.
        # Solve directly for the affine mean-zero potential and capacity.
        mat = np.zeros((len(B) + 1, len(B) + 1), dtype=complex)
        mat[:-1, :-1] = Lop[np.ix_(B, B)] + s*np.eye(len(B))
        mat[:-1, -1] = one
        mat[-1, :-1] = pi[B]
        rhs = np.concatenate((-Lop[np.ix_(B, np.arange(k))].sum(axis=1), [-p]))
        sol = np.linalg.solve(mat, rhs)
        h = np.ones(n, dtype=complex)
        h[B] = sol[:-1]
        return h, sol[-1]

    h0, C0complex = centered_potential(L, 0)
    C0 = float(C0complex.real)
    mu = 1.0 / C0
    gap = 1.0
    delta = C0 / gap
    assert delta <= 0.25

    Lstar = L.T * pi[None, :] / pi[:, None]
    hstar, Cstar = centered_potential(Lstar, 0)
    assert abs(Cstar / C0 - 1) < 1e-8
    freq_records = []
    max_identity_error = 0.0
    for x in np.geomspace(1e-3, 1.0 / (2.0 * delta), 140):
        s = 1j * C0 * x
        h, Cs = centered_potential(L, s)
        m = Cs / (Cs + s)
        energy = np.vdot(h * pi, (L + s * np.eye(n)) @ h)
        perturb = s * np.dot(hstar * pi, h)
        scale = max(abs(Cs), C0)
        identity_error = max(abs(energy - Cs), abs(Cs - C0 - perturb)) / scale
        max_identity_error = max(max_identity_error, float(identity_error))
        assert identity_error <= 2e-5
        z = Cs / C0
        q = C0 * x / gap
        disk_lhs = abs(z - 1.0)**2
        disk_rhs = q*q*z.real
        assert disk_lhs <= disk_rhs * (1 + 5e-5) + 1e-13, \
            (seed, p, circulation, x, disk_lhs, disk_rhs, z)
        assert z.real >= 0.5 - 1e-8
        denominator = abs(z + 1j*x)
        assert denominator >= 0.5 * math.sqrt(1.0 + x*x) - 1e-8
        discrepancy = abs(m - 1.0 / (1.0 + 1j*x))
        bound = 4 * delta * x*x / (1.0 + x*x)
        assert discrepancy <= bound * (1 + 5e-4) + 1e-10
        freq_records.append((float(x), float(discrepancy), float(bound)))

    certified = (4 * delta / math.pi) * math.log1p(1 / (4 * delta**2)) \
                + 48 * delta / math.pi
    ys = np.unique(np.concatenate(([0.0], np.geomspace(1e-7, 0.5, 60),
                                   np.linspace(0.5, 12.0, 90))))
    observed = 0.0
    conditional_observed = 0.0
    for y in ys:
        survival = float(pi[B] @ expm(-LB * mu * y) @ one)
        observed = max(observed, abs(survival - math.exp(-y)))
        conditional_observed = max(conditional_observed,
                                   abs(survival / (1-p) - math.exp(-y)))
    assert observed <= certified + 2e-8
    assert conditional_observed <= (certified + p) / (1-p) + 2e-8
    return {
        "seed": seed, "p": p, "nonreversible": circulation,
        "mean_stationary": mu, "delta": delta,
        "certified_CDF_bound": certified,
        "observed_grid_CDF_distance": observed,
        "observed_grid_conditional_CDF_distance": conditional_observed,
        "max_relative_complex_identity_residual": max_identity_error,
        "frequency_checks": len(freq_records), "CDF_grid_checks": len(ys),
        "first_frequency": freq_records[0], "last_frequency": freq_records[-1]
    }


if __name__ == "__main__":
    cases = [run_case(1700 + i, p, directed)
             for i, p in enumerate((1e-2, 1e-3, 1e-5, 1e-7))
             for directed in (False, True)]
    report = {"checks": len(cases), "all_passed": True,
              "scope": "floating-point finite fixtures; analytic proof separate",
              "cases": cases}
    path = Path(__file__).with_name("lifetime_checks.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"all_passed": True, "cases": len(cases),
                      "frequency_checks": sum(c["frequency_checks"] for c in cases),
                      "CDF_grid_checks": sum(c["CDF_grid_checks"] for c in cases),
                      "output": str(path.resolve())}, indent=2))
