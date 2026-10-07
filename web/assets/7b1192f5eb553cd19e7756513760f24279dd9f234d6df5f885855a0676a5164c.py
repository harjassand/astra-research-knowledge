#!/usr/bin/env python3
"""Bounded exact audit of c10 Sol initial claims plus the l10 extension.

The c10_s01 and c10_s03 source files are executed in fresh namespaces by
compile/exec, with their __main__ blocks disabled; this avoids writing to peer
directories. c10_s02 identities and the new collision family are implemented
independently below. Exact finite checks are diagnostics, not proof substitutes.
"""

from fractions import Fraction as F
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]


def load_source_functions(relpath):
    path = ROOT / relpath
    ns = {"__name__": "_audit_only", "__file__": str(path)}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


def audit_s01():
    ns = load_source_functions("work/cycle6/c10_s01/two_layer_certificate.py")
    report = ns["verify"]()
    assert report["status"] == "EXACT_FINITE_DIAGNOSTIC_PASSED"
    assert report["checked_states"] == 1548
    assert report["zero_catalyst_states"] == 48
    assert report["boundary_example_LV_at_0_60"] == -27
    assert report["exponential_V_counterexample_drift_ratio"] > 0
    return {
        "status": report["status"],
        "checked_states": report["checked_states"],
        "zero_catalyst_states": report["zero_catalyst_states"],
        "boundary_LV": str(report["boundary_example_LV_at_0_60"]),
        "exp_V_witness_ratio": str(report["exponential_V_counterexample_drift_ratio"]),
        "scope": "author checker replayed read-only; finite fixtures do not prove the all-state inequalities",
    }


def s02_reactions():
    # Source/product pairs for A+C <-> A+B <-> B and C <-> 0.
    return [
        ((1, 0, 1), (1, 1, 0)), ((1, 1, 0), (1, 0, 1)),
        ((1, 1, 0), (0, 1, 0)), ((0, 1, 0), (1, 1, 0)),
        ((0, 0, 1), (0, 0, 0)), ((0, 0, 0), (0, 0, 1)),
    ]


def ff(x, y):
    out = 1
    for a, b in zip(x, y):
        if a < b:
            return 0
        out *= factorial(a) // factorial(a - b)
    return out


def residual(x, y):
    if any(a < b for a, b in zip(x, y)):
        return None
    return factorial(x[0] - y[0]) * factorial(x[1] - y[1]) * factorial(x[2] - y[2])


def exp_factorial_potential(x):
    complexes = sorted({z for r in s02_reactions() for z in r})
    return min(residual(x, y) for y in complexes if residual(x, y) is not None)


def audit_s02():
    rs = s02_reactions()
    factorial_cases = 0
    zray_cases = 0
    edge_balances = 0
    component_checks = 0
    for a in range(2, 121):
        x = (a, 0, 1)
        v = exp_factorial_potential(x)
        assert v == factorial(a - 1)
        jumps = []
        for y, yp in rs:
            rate = ff(x, y)
            if rate:
                xnew = tuple(q - r + p for q, r, p in zip(x, y, yp))
                jumps.append((rate, xnew, F(exp_factorial_potential(xnew), v)))
        assert jumps == [
            (a, (a, 1, 0), F(1)),
            (1, (a, 0, 0), F(a)),
            (1, (a, 0, 2), F(1)),
        ]
        assert sum(rate * (ratio - 1) for rate, _, ratio in jumps) == a - 1
        factorial_cases += 1
    for n in range(1, 121):
        x = (0, n, 0)
        jumps = []
        for y, yp in rs:
            rate = ff(x, y)
            if rate:
                xnew = tuple(q - r + p for q, r, p in zip(x, y, yp))
                jumps.append((rate, xnew))
        assert jumps == [(n, (1, n, 0)), (1, (0, n, 1))]
        assert all(exp_factorial_potential(z) == exp_factorial_potential(x) for _, z in jumps)
        zray_cases += 1
    # Exact detailed balance for the product-Poisson weight on bounded states.
    def weight(x):
        return F(1, factorial(x[0]) * factorial(x[1]) * factorial(x[2]))

    for x in product(range(9), repeat=3):
        for y, yp in rs:
            rate = ff(x, y)
            if not rate:
                continue
            z = tuple(a - b + c for a, b, c in zip(x, y, yp))
            assert weight(x) * rate == weight(z) * ff(z, yp)
            assert (x[0] + x[1] == 0) == (z[0] + z[1] == 0)
            edge_balances += 1
            component_checks += 1
    return {
        "factorial_witness_cases": factorial_cases,
        "zero_A_B_ray_cases": zray_cases,
        "bounded_exact_edge_balance_checks": edge_balances,
        "component_invariance_checks": component_checks,
        "scope": "finite checks support exact formulas; deterministic convergence and concave no-go remain symbolic arguments",
    }


def audit_s03():
    ns = load_source_functions("work/cycle6/c10_s03/initial/compiler.py")
    all_counts = {
        "global_drift_states_checked": 0,
        "rate_vertex_states_checked": 0,
        "drain_paths_checked": 0,
        "production_dominance_checked": 0,
    }
    results = {}
    for name, reactions in ns["fixtures"]().items():
        cert = ns["compile_certificate"](reactions)
        results[name] = cert["status"]
        if cert["status"] == "CERTIFIED":
            extent = 12 if cert["dimension"] == 1 else 7
            diag = ns["exact_diagnostics"](reactions, cert, extent=extent)
            for k, value in diag.items():
                all_counts[k] += value
    assert results == {
        "nonlinear_assembly": "CERTIFIED",
        "autocatalytic": "CERTIFIED",
        "balanced_cross_rejection": "NO_CERTIFICATE_IN_ADMITTED_FOSTER_CLASS",
    }
    assert all_counts == {
        "global_drift_states_checked": 525,
        "rate_vertex_states_checked": 3459,
        "drain_paths_checked": 30,
        "production_dominance_checked": 30,
    }
    return {"fixture_statuses": results, "diagnostics": all_counts,
            "scope": "author compiler/check functions replayed read-only; rejection means only no certificate in the stated class"}


def collision_certificate(d):
    def drift_ratio(n):
        return F(2 * d) - F(1, 2) * comb(n, 2)

    nstar = next(n for n in range(1, 100000) if drift_ratio(n) <= -1)
    # The drift ratio decreases for n>=1, so outside nstar it is <= -1.
    B = max(F(2**n) * drift_ratio(n) for n in range(nstar))
    return nstar, B


def audit_collision_family():
    endpoint_states = 0
    endpoint_rate_vectors = 0
    by_d = {}
    for d, nmax in ((1, 8), (2, 8), (3, 6)):
        channels = ["birth"] * d + ["pair"] * (d * (d + 1) // 2)
        checked_states = checked_vectors = 0
        for x in product(range(nmax + 1), repeat=d):
            n = sum(x)
            if n > nmax:
                continue
            # Exhaust the exact endpoints of each independent rate interval.
            for endpoints in product((0, 1), repeat=len(channels)):
                iend = 0
                drift = F(0)
                for i in range(d):
                    lam = 1 + endpoints[i]
                    drift += lam  # birth increases n by one, so W'/W-1 = 1
                iend = d
                for i in range(d):
                    for j in range(i, d):
                        mu = 1 + 3 * endpoints[iend]
                        iend += 1
                        propensity = comb(x[i], 2) if i == j else x[i] * x[j]
                        drift -= F(1, 2) * mu * propensity
                upper = F(2 * d) - F(1, 2) * comb(n, 2)
                assert drift <= upper, (d, x, endpoints, drift, upper)
                checked_vectors += 1
            checked_states += 1
        nstar, B = collision_certificate(d)
        by_d[str(d)] = {
            "states_checked": checked_states,
            "rate_endpoint_vectors_checked": checked_vectors,
            "nstar": nstar,
            "exact_global_generator_upper_B": str(B),
        }
        endpoint_states += checked_states
        endpoint_rate_vectors += checked_vectors

    d, n0, T, eps = 2, 2, 100, F(1, 100)
    nstar, B = collision_certificate(d)
    N = n0 + 1
    while F(2**n0 + B * T, 2**N) > eps:
        N += 1
    previous_bound = F(2**n0 + B * T, 2 ** (N - 1))
    exit_bound = F(2**n0 + B * T, 2**N)
    retained = comb(N - 1 + d, d)
    max_total_intensity = 2 * d + 4 * comb(N - 1, 2)
    assert (nstar, B, N, retained, max_total_intensity) == (5, F(20), 18, 171, 548)
    assert previous_bound > eps and exit_bound <= eps
    return {
        "rate_interval": {"birth": [1, 2], "pairwise_competition": [1, 4]},
        "endpoint_states_checked": endpoint_states,
        "endpoint_rate_vectors_checked": endpoint_rate_vectors,
        "by_dimension": by_d,
        "d2_example": {
            "nstar": nstar,
            "core": "{x: ||x||_1 < 5}",
            "global_LW_bound_B": str(B),
            "start": [1, 1],
            "horizon": T,
            "target_error": str(eps),
            "minimal_cutoff_N": N,
            "retained_states": retained,
            "exit_probability_bound": str(exit_bound),
            "previous_cutoff_bound": str(previous_bound),
            "max_total_intensity_inside_cutoff": max_total_intensity,
        },
        "scope": "exact finite arithmetic plus a direct symbolic all-state proof in the accompanying report; no finite-state HJB/CTMDP solver run",
    }


def main():
    peer_paths = {
        "c10_s01_INITIAL": ROOT / "work/cycle6/c10_s01/INITIAL.txt",
        "c10_s02_INITIAL": ROOT / "work/cycle6/c10_s02/INITIAL.txt",
        "c10_s03_INITIAL": ROOT / "work/cycle6/c10_s03/INITIAL.txt",
    }
    peer_hashes = {k: hashlib.sha256(v.read_bytes()).hexdigest() for k, v in peer_paths.items()}
    assert peer_hashes == {
        "c10_s01_INITIAL": "d079448f084850567851bd59f0ff7a141822549f2edfd685d135aa5ff2674adf",
        "c10_s02_INITIAL": "14d1817522a7de31dba58a8a3ec318c1a6726260cdb0ab9295311876690f3989",
        "c10_s03_INITIAL": "30a72c0206ef4ef5162a39dfbaab61fcfef794733daadad9fa62b9f5b481e3f6",
    }
    out = {
        "peer_initial_sha256": peer_hashes,
        "c10_s01": audit_s01(),
        "c10_s02": audit_s02(),
        "c10_s03": audit_s03(),
        "l10_pairwise_competition_extension": audit_collision_family(),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
