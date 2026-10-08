#!/usr/bin/env python3
"""Small finite diagnostics for sol_xy_critical cycle 2 (not proof checks)."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


def configs(n_sites: int, particles: int):
    return list(itertools.combinations(range(n_sites), particles))


def sector_matrix(L: int, particles: int, interaction: float, J: float = 1.0,
                  lam: float = 0.0) -> np.ndarray:
    """Physical open-chain matrix; L=N_sites+1, hopping coefficient -2J."""
    n_sites = L - 1
    basis = configs(n_sites, particles)
    index = {xs: j for j, xs in enumerate(basis)}
    H = np.zeros((len(basis), len(basis)), dtype=float)
    for col, xs in enumerate(basis):
        occ = set(xs)
        adjacent = sum(1 for i in range(n_sites - 1)
                       if i in occ and i + 1 in occ)
        H[col, col] = (4.0 * J - lam / L**2) * particles + interaction * adjacent
        for i in range(n_sites - 1):
            if (i in occ) == (i + 1 in occ):
                continue
            moved = set(occ)
            if i in moved:
                moved.remove(i)
                moved.add(i + 1)
            else:
                moved.remove(i + 1)
                moved.add(i)
            row = index[tuple(sorted(moved))]
            H[row, col] += -2.0 * J
    return H


def scaled_sector_traces(L: int, particles: int, interaction: float,
                         tau: float = 0.7, J: float = 1.0,
                         lam: float = 0.2):
    H0 = sector_matrix(L, particles, 0.0, J, lam)
    Ha = sector_matrix(L, particles, interaction, J, lam)
    n_sites = L - 1
    hard_basis = [xs for xs in configs(n_sites, particles)
                  if all(xs[j + 1] - xs[j] >= 2
                         for j in range(particles - 1))]
    if hard_basis:
        full_basis = configs(n_sites, particles)
        full_index = {xs: j for j, xs in enumerate(full_basis)}
        ix = [full_index[xs] for xs in hard_basis]
        Hhc = H0[np.ix_(ix, ix)]
        zhc = float(np.exp(-tau * L**2 * np.linalg.eigvalsh(Hhc)).sum())
    else:
        zhc = 0.0
    z0 = float(np.exp(-tau * L**2 * np.linalg.eigvalsh(H0)).sum())
    za = float(np.exp(-tau * L**2 * np.linalg.eigvalsh(Ha)).sum())
    return z0, za, zhc


def hardrod_formula(L: int, particles: int, tau: float = 0.7,
                    J: float = 1.0, lam: float = 0.2) -> float:
    n_compressed = L - particles
    if particles == 0:
        return 1.0
    if n_compressed < particles:
        return 0.0
    energies = [4.0 * tau * J * L**2
                * (1.0 - math.cos(math.pi * k / (n_compressed + 1)))
                - tau * lam for k in range(1, n_compressed + 1)]
    return float(sum(math.exp(-sum(energies[k - 1] for k in ks))
                     for ks in itertools.combinations(range(1, n_compressed + 1),
                                                      particles)))


def scattering_residual(a: float, K: float, q: float, J: float = 1.0) -> float:
    A = 4.0 * J * math.cos(K / 2.0)
    delta = math.atan2(-a * math.sin(q), A + a * math.cos(q))
    phi = lambda r: math.sin(q * r + delta)
    E = -2.0 * A * math.cos(q)
    return abs(E * phi(1) - a * phi(1) + A * phi(2))


def born_w(L: int, k: int = 1, ell: int = 2) -> float:
    def phi(mode: int, site: int) -> float:
        return math.sqrt(2.0 / L) * math.sin(math.pi * mode * site / L)
    return sum((phi(k, i) * phi(ell, i + 1)
                - phi(ell, i) * phi(k, i + 1)) ** 2
               for i in range(1, L - 1))


def critical_graph_matrix(L: int, particles: int, J: float = 1.0) -> np.ndarray:
    """Killed SSEP graph Laplacian for Hcrit in the m-particle sector."""
    n_sites = L - 1
    basis = configs(n_sites, particles)
    index = {xs: j for j, xs in enumerate(basis)}
    H = np.zeros((len(basis), len(basis)), dtype=float)
    for col, xs in enumerate(basis):
        occ = set(xs)
        for i in range(n_sites - 1):
            if (i in occ) == (i + 1 in occ):
                continue
            moved = set(occ)
            if i in moved:
                moved.remove(i)
                moved.add(i + 1)
            else:
                moved.remove(i + 1)
                moved.add(i)
            row = index[tuple(sorted(moved))]
            H[col, col] += 2.0 * J
            H[row, col] -= 2.0 * J
        H[col, col] += 2.0 * J * (int(0 in occ) + int(n_sites - 1 in occ))
    return H


def main() -> None:
    traces = []
    max_order_violation = 0.0
    max_squeeze_error = 0.0
    for L in range(4, 9):
        for m in range(0, min(L - 1, 4) + 1):
            z0, za, zhc = scaled_sector_traces(L, m, interaction=1.3 * L)
            max_order_violation = max(max_order_violation, za - z0, zhc - za)
            max_squeeze_error = max(max_squeeze_error,
                                    abs(zhc - hardrod_formula(L, m)))
            traces.append({"L": L, "m": m, "z_free": z0,
                           "z_repulsive": za, "z_hardrod": zhc})

    born = []
    for L in (16, 32, 64, 128):
        born.append({"L": L, "L3_W_12": L**3 * born_w(L)})

    scattering = []
    for a, K, q in ((0.0, 0.3, 0.2), (3.0, 0.2, 0.4), (100.0, 0.1, 0.25)):
        scattering.append({"a": a, "K": K, "q": q,
                           "boundary_residual": scattering_residual(a, K, q)})

    max_ssep_error = 0.0
    run_bound_violations = 0
    high_density_trace_violations = 0
    tau, J, gmin = 0.7, 1.0, 0.9
    for L in range(3, 9):
        n_sites = L - 1
        for m in range(n_sites + 1):
            Hcrit = sector_matrix(L, m, interaction=-4.0 * J, J=J)
            Hgraph = critical_graph_matrix(L, m, J)
            max_ssep_error = max(max_ssep_error,
                                  float(np.max(np.abs(Hcrit - Hgraph))))
            for xs in configs(n_sites, m):
                occ = set(xs)
                W = sum(1 for i in range(n_sites - 1)
                        if i in occ and i + 1 in occ)
                runs = sum(1 for i in xs
                           if i == 0 or i - 1 not in occ)
                run_bound_violations += int(
                    W != m - runs or W < max(0, 2 * m - L))
            if m > L / 2:
                Hres = sector_matrix(L, m, interaction=-4.0 * J + gmin / L,
                                     J=J)
                z = float(np.exp(-tau * L**2 * np.linalg.eigvalsh(Hres)).sum())
                rhs = (math.comb(n_sites, m)
                       * math.exp(-tau * gmin * L * max(0, 2 * m - L)))
                high_density_trace_violations += int(z > rhs * (1.0 + 1e-10))

    result = {
        "scope": "finite diagnostics only; no theorem validation",
        "sector_partition_order_max_positive_violation": max(0.0, max_order_violation),
        "hardrod_squeeze_max_trace_error": max_squeeze_error,
        "two_particle_born_limit_target": 5.0 * math.pi**2,
        "two_particle_born_values": born,
        "scattering_boundary_residuals": scattering,
        "critical_ssep_max_matrix_error": max_ssep_error,
        "run_count_bound_violations": run_bound_violations,
        "high_density_trace_bound_violations": high_density_trace_violations,
        "sector_samples": traces,
    }
    out = Path(__file__).with_name("checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k != "sector_samples"}, indent=2))


if __name__ == "__main__":
    main()
