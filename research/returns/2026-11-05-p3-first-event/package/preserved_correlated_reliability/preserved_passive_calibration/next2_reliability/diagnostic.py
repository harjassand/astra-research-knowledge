"""Executed diagnostic for the new full-CDF construction.

This is a small symmetric model, so an ordinary lumped exact solver is
better than the generic theorem's Monte Carlo preprocessing. The script
checks the rare boundary-Palm operation, short reverse statistic,
outward finite arithmetic, spectral tail bound, and changing-mass bound.
It is not a generic Karger implementation or a laboratory experiment.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction as F
from math import comb, lcm
from pathlib import Path
from random import Random
from time import perf_counter

import mpmath as mp
import numpy as np
from scipy.linalg import expm

from finite_arithmetic import (
    Interval, IntegerDistribution, ceil_fraction, ceil_log2,
    dyadic_sqrt_upper, failure_exp_interval, failure_power_interval,
    poisson_table, geometric_grid,
)

mp.mp.dps = 120


def mpr(x):
    if isinstance(x, F):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x)


def decimal(x, digits=18):
    return mp.nstr(mpr(x), digits)


def fractional_distribution(row):
    denominator = 1
    for x in row:
        denominator = lcm(denominator, x.denominator)
    return IntegerDistribution([x.numerator * (denominator // x.denominator)
                                for x in row])


def lumped_refresh_model(m=24, q=F(1, 10)):
    """Parallel edges; mixture of single-bit and two-bit heat baths."""
    single = pair = F(1, 4)
    P = [[F(0) for _ in range(m+1)] for _ in range(m+1)]
    for i in range(m+1):
        P[i][i] += 1-single-pair
        for old in (0, 1):
            old_probability = F(i if old else m-i, m)
            if not old_probability:
                continue
            for new, new_probability in ((0, 1-q), (1, q)):
                P[i][i-old+new] += single*old_probability*new_probability
        for old in range(3):
            if old > i or 2-old > m-i:
                continue
            old_probability = F(comb(i, old)*comb(m-i, 2-old), comb(m, 2))
            for new in range(3):
                new_probability = comb(2, new)*q**new*(1-q)**(2-new)
                P[i][i-old+new] += pair*old_probability*new_probability
    pi = [comb(m, i)*q**i*(1-q)**(m-i) for i in range(m+1)]
    for i in range(m+1):
        assert sum(P[i]) == 1
        for j in range(m+1):
            assert pi[i]*P[i][j] == pi[j]*P[j][i]
    # All product-coordinate heat-bath projections commute. The smallest
    # nonzero eigenvalue is on a one-coordinate centered observable.
    g = (single+2*pair)/m
    return P, pi, g


def spectral_data(P, pi):
    size = len(P)-1
    roots = [mp.sqrt(mpr(pi[i])) for i in range(size)]
    K = mp.matrix(size)
    for i in range(size):
        for j in range(size):
            K[i, j] = ((1 if i == j else 0)-mpr(P[i][j]))*roots[i]/roots[j]
    values, vectors = mp.eigsy(K)
    a = 1-mpr(pi[-1])
    alpha = []
    for k in range(size):
        overlap = sum(roots[j]*vectors[j, k] for j in range(size))
        alpha.append(overlap**2/a)
    total = mp.fsum(alpha)
    normalization_residual = total-1
    assert abs(normalization_residual) < mp.mpf("1e-100")
    alpha = [value/total for value in alpha]
    def cdf(u):
        u = mpr(u)
        value = mp.fsum(alpha[i]*(-mp.expm1(-values[i]*u))
                        for i in range(size))
        return min(mp.mpf(1), max(mp.mpf(0), value))
    return values, alpha, cdf, normalization_residual


def exact_palm_checks(P, pi):
    """Compare the actually forced finite path law to the stationary law."""
    m = len(P)-1
    p, a = pi[-1], 1-pi[-1]
    c = 1-P[m][m]
    j = p*c
    def continuations(start, steps):
        if not steps:
            yield (start,), F(1)
            return
        for nxt, probability in enumerate(P[start]):
            if probability:
                for path, weight in continuations(nxt, steps-1):
                    yield (start,)+path, probability*weight
    checks = []
    for n in range(1, 5):
        forced = {}
        for x in range(m):
            if not P[m][x]:
                continue
            pair_weight = P[m][x]/c
            for position in range(1, n+1):
                for backward, left_weight in continuations(x, position-1):
                    for forward, right_weight in continuations(m, n-position):
                        path = tuple(reversed(backward))+forward
                        forced[path] = forced.get(path, F(0)) + (
                            pair_weight*left_weight*right_weight/n)
        assert sum(forced.values()) == 1
        mu = F(0)
        for path, forced_probability in forced.items():
            crossings = sum(path[k] < m and path[k+1] == m for k in range(n))
            stationary_probability = pi[path[0]]
            for k in range(n):
                stationary_probability *= P[path[k]][path[k+1]]
            assert forced_probability == crossings*stationary_probability/(j*n)
            if path[0] < m:
                mu += forced_probability/crossings
        killed = [pi[x]/a for x in range(m)]
        for _ in range(n):
            killed = [sum(killed[x]*P[x][y] for x in range(m))
                      for y in range(m)]
        probability = 1-sum(killed)
        assert a*probability == j*n*mu
        checks.append({"steps": n, "forced_paths": len(forced),
                       "identity_exact_in_rational_arithmetic": True})
    return checks


def mean_interval(total, count, events=5, confidence=F(1, 100),
                  deterministic_bias=F(0)):
    estimate = total/count
    logarithm = ceil_log2(F(2*events)/confidence)
    radius = dyadic_sqrt_upper(F(logarithm, 2*count))+deterministic_bias
    return Interval(max(F(0), estimate-radius), min(F(1), estimate+radius))


def main():
    started = perf_counter()
    directory = Path(__file__).resolve().parent
    seed = 31052026
    rng = Random(seed)
    P, pi, g = lumped_refresh_model()
    m = len(P)-1
    p, a = pi[-1], 1-pi[-1]
    c = 1-P[m][m]
    transitions = [fractional_distribution(row) for row in P]
    values, alpha, cdf, normalization_residual = spectral_data(P, pi)
    lam = values[0]
    r = 1-alpha[0]
    mean = sum(alpha[i]/values[i] for i in range(m))
    report = {
        "scope": "Synthetic symmetric 24-component model; a small lumped finite-state solver is better. No laboratory data or generic Karger execution.",
        "seed": seed,
        "components": m,
        "full_state_count": str(2**m),
        "lumped_state_count": m+1,
        "stationary_failure_probability": str(p),
        "certified_gap_g": str(g),
        "boundary_acceptance_c": str(c),
        "killed_lambda": decimal(lam),
        "mean_first_failure_uniformized_units": decimal(mean),
        "fast_mass_over_lambda": decimal(r/lam),
        "proved_bound_1_over_ag": decimal(1/(a*g)),
        "spectral_reference_decimal_precision": mp.mp.dps,
        "spectral_weight_sum_residual_before_normalization": decimal(normalization_residual),
        "spectral_reference_scope": "High-precision numerical diagonalization, normalized and clipped to the probability range; not machine-certified eigenvalue enclosures.",
        "exact_path_checks": exact_palm_checks(P, pi),
        "monte_carlo": [],
    }
    assert r/lam <= mpr(1/(a*g))*(1+mp.mpf("1e-90"))

    trials = 12000
    tolerance = F(1, 10**10)
    c_success = sum(transitions[m].draw(rng) < m for _ in range(trials))
    c_ci = mean_interval(F(c_success), trials)
    assert c_ci.lower <= c <= c_ci.upper
    report["c_estimate"] = str(F(c_success, trials))
    report["c_interval"] = [decimal(c_ci.lower), decimal(c_ci.upper)]
    report["trials_per_observable"] = trials

    for u in (F(1, 4), F(2), F(20)):
        pois = poisson_table(u, tolerance)
        inverse_counts = Counter()
        attempts = updates = 0
        for _ in range(trials):
            while True:
                attempts += 1
                x = transitions[m].draw(rng)
                if x < m:
                    break
            other_steps = pois.draw(rng)
            position = rng.randrange(other_steps+1)
            backward = [x]
            for _ in range(position):
                backward.append(transitions[backward[-1]].draw(rng))
            path = list(reversed(backward))+[m]
            for _ in range(other_steps-position):
                path.append(transitions[path[-1]].draw(rng))
            updates += other_steps+1
            crossings = sum(path[i] < m and path[i+1] == m
                            for i in range(len(path)-1))
            assert crossings >= 1
            if path[0] < m:
                inverse_counts[crossings] += 1
        total = sum((F(number, crossings)
                     for crossings, number in inverse_counts.items()), F(0))
        mu_ci = mean_interval(total, trials, deterministic_bias=tolerance)
        exact_f = cdf(u)
        exact_mu = mpr(a)*exact_f/(mpr(p*c*u))
        lo = p*c_ci.lower*u*mu_ci.lower/a
        hi = p*c_ci.upper*u*mu_ci.upper/a
        assert mpr(lo) <= exact_f <= mpr(hi)
        assert mpr(mu_ci.lower) <= exact_mu <= mpr(mu_ci.upper)
        report["monte_carlo"].append({
            "u": str(u),
            "estimated_mu": str(total/trials),
            "reference_mu_120d": decimal(exact_mu),
            "reference_F_120d": decimal(exact_f),
            "F_interval": [decimal(lo), decimal(hi)],
            "interval_ratio": decimal(hi/lo),
            "boundary_attempts": attempts,
            "simulated_updates": updates,
            "ordinary_P_draws": attempts+updates-trials,
            "poisson_cutoff": len(pois.weights)-1,
        })

    xi = F(1, 100)
    ell = ceil_fraction(F(ceil_log2(4/(g*xi)))/g)
    zpois = poisson_table(F(ell), tolerance)
    z_success = z_updates = 0
    for _ in range(trials):
        x = transitions[m].draw(rng)
        if x == m:
            continue
        count = zpois.draw(rng)
        survived = True
        for _ in range(count):
            z_updates += 1
            x = transitions[x].draw(rng)
            if x == m:
                survived = False
                break
        z_success += survived
    z_ci = mean_interval(F(z_success), trials, deterministic_bias=tolerance)
    exact_z = (mpr(a)/mpr(p) *
               sum(alpha[i]*values[i]*mp.exp(-values[i]*ell)
                   for i in range(m)))
    lam_lo = p*z_ci.lower/(a*(1+xi))
    lam_hi = p*z_ci.upper/(a*(1-2*xi))
    assert mpr(lam_lo) <= lam <= mpr(lam_hi)
    report["reverse_window"] = {
        "ell": ell,
        "estimated_Z": str(F(z_success, trials)),
        "reference_Z_120d": decimal(exact_z),
        "lambda_interval": [decimal(lam_lo), decimal(lam_hi)],
        "lambda_interval_ratio": decimal(lam_hi/lam_lo),
        "simulated_updates": z_updates,
        "poisson_cutoff": len(zpois.weights)-1,
    }
    horizon = max(ceil_fraction(2/(g*xi)), ell+1)
    tail_queries = []
    for u in (F(horizon), F(10**24), F(10**26), F(2**512, 10**100)):
        lower = failure_exp_interval(lam_lo*u, xi).lower
        upper = min(F(1), (1+xi)*failure_exp_interval(lam_hi*u, xi).upper)
        exact = cdf(u)
        assert mpr(lower) <= exact <= mpr(upper)
        tail_queries.append({
            "u_binary_bits": u.numerator.bit_length()+u.denominator.bit_length(),
            "u": str(u),
            "reference_F_120d": decimal(exact),
            "interval": [decimal(lower), decimal(upper)],
            "interval_ratio": decimal(upper/lower),
        })
    report["tail_queries"] = tail_queries

    # Independent high-precision checks of both outward evaluators,
    # spanning tiny probabilities and binary deadlines beyond trajectories.
    arithmetic_cases = []
    for x in (F(1, 10**100), F(1, 100), F(1, 2), F(1), F(17, 2),
              F(100), F(2**1024)):
        bracket = failure_exp_interval(x, xi)
        exact = -mp.expm1(-mpr(x))
        assert mpr(bracket.lower) <= exact <= mpr(bracket.upper)
        arithmetic_cases.append({
            "x_bits": x.numerator.bit_length()+x.denominator.bit_length(),
            "ratio": decimal(bracket.ratio),
        })
    for la, n in ((F(1, 10**80), 1), (F(1, 10**80), 10**60),
                  (F(1, 10**80), 10**80), (F(1, 3), 2**512)):
        bracket = failure_power_interval(la, n, xi)
        exact = -mp.expm1(mp.mpf(n)*mp.log1p(-mpr(la)))
        assert mpr(bracket.lower) <= exact <= mpr(bracket.upper)
        arithmetic_cases.append({
            "discrete_n_bits": n.bit_length(),
            "ratio": decimal(bracket.ratio),
        })
    report["outward_arithmetic_checks"] = arithmetic_cases
    grid = geometric_grid(xi, F(horizon))
    maximum_ratio = max(grid[i+1]/grid[i] for i in range(len(grid)-1))
    assert maximum_ratio <= (1+xi)/(1-xi)
    report["finite_grid"] = {
        "horizon": horizon, "nodes": len(grid),
        "maximum_adjacent_ratio": str(maximum_ratio),
        "maximum_node_bit_length": max(x.numerator.bit_length()+
                                        x.denominator.bit_length() for x in grid),
    }

    # Changing-mass theorem: noncommuting killed conductance matrices.
    M0 = np.diag([0.35, 0.25, 0.20])
    M1 = np.diag([0.33, 0.27, 0.19])
    edges0 = [(0, 1, 0.020), (1, 2, 0.015), (0, 2, 0.004)]
    edges1 = [(0, 1, 0.021), (1, 2, 0.014), (0, 2, 0.006)]
    def laplacian(edges, killing):
        L = np.diag(killing).astype(float)
        for i, j, cedge in edges:
            L[i, i] += cedge
            L[j, j] += cedge
            L[i, j] -= cedge
            L[j, i] -= cedge
        return L
    L0 = laplacian(edges0, [0.0004, 0.0008, 0.0002])
    L1 = laplacian(edges1, [0.00042, 0.00075, 0.00023])
    ev, U = np.linalg.eigh(L0)
    inverse_root = (U/np.sqrt(ev))@U.T
    generalized = np.linalg.eigvalsh(inverse_root@L1@inverse_root)
    eta = float(max(abs(np.log(generalized))))
    Delta = float(max(abs(np.log(np.diag(M1)/np.diag(M0)))))
    bound = np.exp(eta+2*Delta)
    mass_ratios = []
    for t in np.logspace(-3, 6, 40):
        one = np.ones(3)
        h0 = one@M0@(one-expm(-t*np.linalg.solve(M0, L0))@one)
        h1 = one@M1@(one-expm(-t*np.linalg.solve(M1, L1))@one)
        ratio = (h1/np.trace(M1))/(h0/np.trace(M0))
        assert 1/bound*(1-1e-8) <= ratio <= bound*(1+1e-8)
        mass_ratios.append(ratio)
    report["changing_mass_check"] = {
        "eta": eta, "Delta": Delta, "proved_ratio_bound": bound,
        "observed_ratio_range": [float(min(mass_ratios)), float(max(mass_ratios))],
        "times_checked": len(mass_ratios),
        "norm_commutator_L0_L1": float(np.linalg.norm(L0@L1-L1@L0)),
        "scope": "Double-precision numerical check, not directed-arithmetic validation.",
    }

    # Explicit adverse budget: the proved conservative preprocessing bound
    # is not the small diagnostic sample count.
    epsilon, confidence = F(1, 10), F(1, 100)
    bx = epsilon/40
    bell = ceil_fraction(F(ceil_log2(4/(g*bx)))/g)
    bH = max(ceil_fraction(2/(g*bx)), bell+1)
    bg = geometric_grid(bx, F(bH))
    G = len(bg)
    beta = confidence/(8*(G+2))
    N = ceil_fraction(F(384)*ceil_log2(2/beta)/((g/4)*bx*bx))
    Nall = N*(G+2)
    capB = ceil_fraction((4/g)*ceil_log2(8*Nall/confidence))
    tauP = bx*(g/4)/64
    Kmax = 2*bH+ceil_log2(1/tauP)
    report["literal_conservative_preprocessing_budget"] = {
        "epsilon": str(epsilon), "delta": str(confidence),
        "horizon": bH, "grid_nodes": G,
        "trials_per_observable": str(N),
        "total_bounded_trials_upper": str(Nall),
        "boundary_attempt_cap_per_trial": str(capB),
        "path_update_upper_before_boundary_and_factory_cost": str(Nall*(Kmax+1)),
        "not_executed": True,
        "reason": "The theorem's conservative worst-case budget is far larger than the executed diagnostic. No practical speedup is claimed.",
    }
    report["ordinary_P_draws_executed"] = (
        2*trials+z_updates+
        sum(row["ordinary_P_draws"] for row in report["monte_carlo"]))
    report["wall_seconds_for_diagnostic"] = perf_counter()-started
    output = directory/"results.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({
        "output": str(output),
        "p": decimal(p),
        "mean": decimal(mean),
        "MC_intervals_contained_high_precision_references": True,
        "reverse_lambda_ratio": decimal(lam_hi/lam_lo),
        "grid_nodes": len(grid),
        "arithmetic_cases": len(arithmetic_cases),
        "mass_check_ratio_bound": bound,
        "conservative_total_trials_not_run": str(Nall),
    }, indent=2))


if __name__ == "__main__":
    main()
