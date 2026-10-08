#!/usr/bin/env python3
"""Exact rational fixtures for finite-n Schur-Weyl memory boundaries.

This script checks algebraic identities and selected exact examples only.  It
does not prove a uniform memory theorem, the HCIZ comparison, or the
entanglement-breaking lower bound quoted from the source report.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
import json
import math
from pathlib import Path


def collision_product(n: int, p: list[F]) -> F:
    """B_n(p)=product_{i<j}(1+n(p_i-p_j)^2), exactly."""
    out = F(1)
    for i, j in combinations(range(len(p)), 2):
        out *= 1 + n * (p[i] - p[j]) ** 2
    return out


def schur_multiplicity(n: int, k: int) -> int:
    """dim S^(n-k,k) = C(n,k)-C(n,k-1), with C(n,-1)=0."""
    return math.comb(n, k) - (math.comb(n, k - 1) if k else 0)


def qubit_joint_schur_excitation(n: int, p: F) -> dict[tuple[int, int], F]:
    """Joint law of Schur defect k and within-spin excitation ell.

    For diag(1-p,p)^tensor n, t=n-2k and
    Pr(k,ell)=m_(n,k)(1-p)^(n-k-ell) p^(k+ell).
    """
    out: dict[tuple[int, int], F] = {}
    for k in range(n // 2 + 1):
        t = n - 2 * k
        m = schur_multiplicity(n, k)
        for ell in range(t + 1):
            out[(k, ell)] = F(m) * (1 - p) ** (n - k - ell) * p ** (k + ell)
    return out


def binomial(n: int, x: int, p: F) -> F:
    return F(math.comb(n, x)) * p**x * (1 - p) ** (n - x)


def local_pure_torus_spectrum(n: int, s: F) -> list[F]:
    """Exact spectrum of the phase-averaged local pure-qubit cap.

    Each input is ((|0>+sqrt(s/n)e^{i theta}|1>)/sqrt(1+s/n))^tensor n.
    """
    return [F(math.comb(n, k)) * (s / n) ** k / (1 + s / n) ** n
            for k in range(n + 1)]


def main() -> None:
    # Partial qutrit collision: n=m^4; gaps are 2/m^3 and 3/m-1/m^3.
    # Thus one pair is below n^-1/2 while the other two are resolved at
    # scale n^-1/4.  Every entry and B_n is an exact rational.
    partial = []
    for m in (8, 16, 32, 64, 128):
        n = m**4
        p = [F(1, 3) + F(1, m) + F(1, m**3),
             F(1, 3) + F(1, m) - F(1, m**3),
             F(1, 3) - F(2, m)]
        assert sum(p, F(0)) == 1 and p[0] >= p[1] >= p[2] > 0
        b = collision_product(n, p)
        closed = (1 + F(4, m**2)) * (9*m**2 + 7 + F(1, m**2)) * (9*m**2 - 5 + F(1, m**2))
        assert b == closed
        partial.append({
            "m": m,
            "n": n,
            "spectrum": [str(x) for x in p],
            "pair_gaps": [str(p[0] - p[1]), str(p[1] - p[2]), str(p[0] - p[2])],
            "B_n_exact": str(b),
            "log2_B_over_log2_n": math.log2(float(b)) / math.log2(n),
            "asymptotic_exponent": "1",
        })

    # Critical qubit gaps: n=k^2 and p_+-p_-=1/k, so B_n=2 exactly.
    critical = []
    for k in (2, 4, 8, 16, 32, 64):
        n = k**2
        gap = F(1, k)
        p = [F(1, 2) + gap / 2, F(1, 2) - gap / 2]
        b = collision_product(n, p)
        assert b == 2
        critical.append({"k": k, "n": n, "gap": str(gap), "B_n_exact": str(b)})

    # Fixed nontracial qutrit orbit: a pairwise N39 bound has a positive
    # limiting EB floor.  The arithmetic here evaluates its displayed
    # expression; it does not prove that source theorem.
    p_fixed = [F(1, 2), F(1, 3), F(1, 6)]
    n_fixed = 1024
    w = p_fixed[0] + p_fixed[2]
    gap = p_fixed[0] - p_fixed[2]
    delta = gap / w
    kappa = F(n_fixed) * gap**2 / w
    eb_displayed = delta / 20 - F(2) / kappa
    fixed_nontracial = {
        "n": n_fixed,
        "spectrum": [str(x) for x in p_fixed],
        "B_n_exact": str(collision_product(n_fixed, p_fixed)),
        "pair": [0, 2],
        "w_exact": str(w),
        "delta_exact": str(delta),
        "kappa_exact": str(kappa),
        "N39_displayed_lower_bound_exact": str(eb_displayed),
        "N39_displayed_lower_bound_decimal": float(eb_displayed),
        "scope": "evaluation of source formula only; not an independent proof",
    }
    assert kappa >= 64 and eb_displayed > 0

    # Pure rank boundary: B_n=n+1 for the full pure-state orbit, while a
    # fixed local cap has an excitation spectrum approaching a fixed Poisson
    # law.  This is a mismatch of interfaces, not a contradiction: the full
    # orbit and local cap are different parameter sets.
    rank_boundary = []
    for n in (8, 16, 64, 256, 1024):
        b = collision_product(n, [F(1), F(0)])
        spectrum = local_pure_torus_spectrum(n, F(1, 4))
        assert b == n + 1
        assert sum(spectrum, F(0)) == 1
        top4 = sorted(spectrum, reverse=True)[:4]
        rank_boundary.append({
            "n": n,
            "full_pure_orbit_B_n": str(b),
            "local_cap_s": "1/4",
            "local_cap_top4_average_eigenmass_exact": str(sum(top4, F(0))),
            "local_cap_top4_average_eigenmass_decimal": float(sum(top4, F(0))),
            "local_cap_spectrum_sum_exact": "1",
        })

    # Rank-changing qubit: with unknown lambda=1/2 and small eigenvalue
    # lambda/n, B_n is still order n although the N23 branch law is order
    # h_epsilon.  Check the finite Schur joint law and the exact binomial
    # coupling k+ell ~ Bin(n,p) for many rational instances.
    schur_cases = []
    for n in range(1, 17):
        for lam in (F(0), F(1, 2), F(1)):
            if n < 4 * lam:
                continue
            p_small = lam / n
            joint = qubit_joint_schur_excitation(n, p_small)
            assert sum(joint.values(), F(0)) == 1
            for x in range(n + 1):
                actual = sum((mass for (k, ell), mass in joint.items() if k + ell == x), F(0))
                assert actual == binomial(n, x, p_small), (n, lam, x)
            schur_cases.append({"n": n, "lambda": str(lam), "p": str(p_small), "joint_sum": "1",
                                "binomial_coupling": "exact"})

    lam = F(1, 2)
    rank_change = []
    for n in (8, 16, 64, 256, 1024):
        p_small = lam / n
        b = collision_product(n, [1 - p_small, p_small])
        closed = n - 1 + F(1, n)
        assert b == closed
        rank_change.append({"n": n, "lambda": "1/2", "B_n_exact": str(b),
                            "closed_form": str(closed)})

    out = {
        "status": "PASS: exact rational identities and finite fixtures; source theorems remain source-scoped",
        "partial_qutrit_gap_sequence": partial,
        "critical_qubit_sequence": critical,
        "fixed_nontracial_qutrit": fixed_nontracial,
        "pure_rank_boundary": rank_boundary,
        "rank_changing_qubit_B_n": rank_change,
        "exact_qubit_schur_binomial_cases": len(schur_cases),
        "schur_cases": schur_cases,
        "scope": [
            "Does not establish the HCIZ comparison or the B_n memory theorem.",
            "Does not prove the N39 entanglement-breaking lower bound.",
            "Does not prove finite-n optimal total dimension for N23.",
            "Exact rational checks are convention checks, not external validation.",
        ],
    }
    path = Path(__file__).with_name("finite_n_schur_weyl_checks.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "status": out["status"],
        "partial_qutrit_exponents": [round(x["log2_B_over_log2_n"], 6) for x in partial],
        "critical_B": [x["B_n_exact"] for x in critical],
        "fixed_nontracial_EB_bound": fixed_nontracial["N39_displayed_lower_bound_exact"],
        "pure_rank_boundary_B": [x["full_pure_orbit_B_n"] for x in rank_boundary],
        "rank_changing_B": [x["B_n_exact"] for x in rank_change],
        "exact_schur_cases": len(schur_cases),
        "output": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
