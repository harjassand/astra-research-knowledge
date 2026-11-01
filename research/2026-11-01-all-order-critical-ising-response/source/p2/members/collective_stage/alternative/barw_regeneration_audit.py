"""Independent all-odd BARW regeneration and Doob-h variance audit.

Finite exact translation orbits are used only to check the proposed stochastic
algorithms and compute their moments, not as the intended large-n backend.
All odd particle sectors are retained; there is no particle-number truncation.
Linear solves use float64 and are explicitly numerical evidence, not certificates.
"""

from __future__ import annotations

import json
import time
from functools import lru_cache
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla


def build(n, b=1/3):
    t = (n-1)/(n+1)
    gamma = (n*n-1)/(n*n+1)
    a = gamma*(1-b)/2
    kappa = (1-b)*(1-gamma)
    mask = (1 << n)-1

    @lru_cache(None)
    def canon(s):
        smallest = s
        for _ in range(n-1):
            s = ((s << 1) & mask) | (s >> (n-1))
            smallest = min(smallest, s)
        return smallest

    states = sorted({canon(s) for s in range(1, mask+1) if s.bit_count() % 2 and s.bit_count() >= 3})
    index = {s: i for i, s in enumerate(states)}
    rows, columns, values = [], [], []
    number, potential, reward = [], [], []

    def even_correlation(s):
        positions = [i for i in range(n) if (s >> i) & 1]
        distance = sum(positions[j+1]-positions[j] for j in range(0, len(positions), 2))
        return (t**distance+t**(n-distance))/(1+t**n)

    v1 = sum(even_correlation(1 ^ (1 << i)) for i in range(n))
    for row, s in enumerate(states):
        positions = [i for i in range(n) if (s >> i) & 1]
        count = len(positions)
        number.append(count)
        gaps = [positions[(i+1) % count]-positions[i] for i in range(count)]
        gaps[-1] += n
        hnum = sum(gaps[i]*gaps[j]*gaps[k] for i, j, k in combinations(range(count), 3)
                   if (j-i) % 2 and (k-j) % 2)
        potential.append(hnum/n)
        reward.append(sum(even_correlation(s ^ (1 << i)) for i in range(n))/v1)
        rows.append(row)
        columns.append(row)
        values.append(count)
        for i in positions:
            left, right = (i-1) % n, (i+1) % n
            for destination, rate in ((s ^ (1 << i) ^ (1 << left), a),
                                      (s ^ (1 << i) ^ (1 << right), a),
                                      (s ^ (1 << left) ^ (1 << right), b)):
                if destination.bit_count() == 1:
                    continue
                rows.append(row)
                columns.append(index[canon(destination)])
                values.append(-rate)
    matrix = sp.coo_matrix((values, (rows, columns)), shape=(len(states), len(states))).tocsc()
    number, potential, reward = map(np.asarray, (number, potential, reward))
    triple = index[canon(7)]
    return matrix, number, potential, reward, triple, v1, a, b, kappa


def audit(n):
    started = time.perf_counter()
    hmat, number, h, v, start, v1, a, b, kappa = build(n)
    g = a*(number-1)-b*(1-2*number/n)
    hh = g+kappa*number*h
    drift_error = float(np.max(np.abs(hmat@h-hh)))
    assert drift_error < 1e-10
    solve = sla.factorized(hmat)
    u = solve(number)
    r = solve(v)
    response_ratio = (1+b*r[start])/((1-b)*(1+b*u[start]))
    # Second moments of the direct excursion discounted integrals.
    h2 = hmat+sp.diags(kappa*number)
    solve2 = sla.factorized(h2)
    u2 = solve2(number)
    uu = 2*(u[start]-u2[start])/kappa
    rr = 2*solve2(v*r)[start]
    ur = solve2(number*r+v*u)[start]
    variance_u = uu-u[start]**2
    variance_r = rr-r[start]**2
    covariance = ur-u[start]*r[start]
    # Delta-method variance per independent excursion for q=(1+b R)/(1+b U).
    q = (1+b*r[start])/(1+b*u[start])
    ratio_variance = b*b*(variance_r+q*q*variance_u-2*q*covariance)/(1+b*u[start])**2
    # Exact second moment / expected step identities for Doob-h terminal scores.
    h0 = h[start]
    z_uu = h0*solve(number**2/hh)[start]
    z_rr = h0*solve(v*v/hh)[start]
    z_ur = h0*solve(number*v/hh)[start]
    doob_steps = solve(number*h)[start]/h0
    doob_ratio_variance = b*b*((z_rr-r[start]**2)+q*q*(z_uu-u[start]**2)
                              -2*q*(z_ur-u[start]*r[start]))/(1+b*u[start])**2
    theta0 = (a+2*b/n)/(a+b)
    w_terminal = h0*(v-theta0*number)/hh+h0/(a+b)
    w_mean = r[start]-theta0*u[start]+h0/(a+b)
    w_second = solve(hh*w_terminal*w_terminal)[start]/h0
    assert np.min(w_terminal) > -1e-11
    assert np.max(w_terminal) <= h0/(a+b)+1e-11
    # Ordinary excursion event count: transitions occur at (1-kappa)*N.
    dmat = hmat-sp.diags(kappa*number)
    ordinary_solve = sla.factorized(dmat)
    particle_time = ordinary_solve(number)[start]
    duration = ordinary_solve(np.ones(len(number)))[start]
    events = (1-kappa)*particle_time
    c = (2*a-b+6*b/n)/3
    record = {
        "n": n,
        "all_odd_translation_orbits_except_singletons": len(number),
        "kappa": kappa,
        "response_divided_by_Glauber_response": float(response_ratio),
        "E_discounted_particle_time_U": float(u[start]),
        "E_discounted_reward_R_over_V1": float(r[start]),
        "E_unweighted_excursion_time": float(duration),
        "E_ordinary_excursion_events": float(events),
        "ordinary_event_upper_bound_from_h": float((1-kappa)*h0/c),
        "direct_U_variance": float(variance_u),
        "direct_R_variance": float(variance_r),
        "direct_normalized_response_asymptotic_relative_variance": float(ratio_variance/(q*q)),
        "doob_U_variance": float(z_uu-u[start]**2),
        "doob_R_variance": float(z_rr-r[start]**2),
        "doob_expected_steps": float(doob_steps),
        "doob_normalized_response_asymptotic_relative_variance": float(doob_ratio_variance/(q*q)),
        "theta": float(q),
        "theta0": float(theta0),
        "exact_all_sector_E_W": float(w_mean),
        "exact_all_sector_Var_W": float(w_second-w_mean*w_mean),
        "min_W_over_all_states": float(np.min(w_terminal)),
        "max_W_over_all_states": float(np.max(w_terminal)),
        "max_Doob_U_score_bound": float(h0/c),
        "max_Doob_R_score_bound": float(h0*n/(3*c*v1)),
        "drift_identity_max_abs_error": drift_error,
        "Poisson_residual_U_max_abs": float(np.max(np.abs(hmat@u-number))),
        "elapsed_seconds": time.perf_counter()-started,
    }
    print(json.dumps(record), flush=True)
    return record


def physical_check(n):
    """Independent physical spin-space Poisson equation, not Walsh algebra."""
    started = time.perf_counter()
    size = 1 << n
    states = np.arange(size, dtype=np.int64)
    spin = np.array([2*((states >> i) & 1)-1 for i in range(n)], dtype=float)
    walls = np.sum(spin != np.roll(spin, -1, axis=0), axis=0)
    probability = np.power(float(n), -walls)
    probability /= np.sum(probability)
    ground = np.sqrt(probability)
    gamma = (n*n-1)/(n*n+1)
    diagonal = np.zeros(size)
    rows, columns, values = [], [], []
    for i in range(n):
        left, right = spin[(i-1) % n], spin[(i+1) % n]
        rate = (1-left*right/3)*(1-gamma*spin[i]*(left+right)/2)/2
        destination = states ^ (1 << i)
        rows.append(states)
        columns.append(destination)
        values.append(-rate*ground/ground[destination])
        diagonal += rate
    rows.append(states)
    columns.append(states)
    values.append(diagonal)
    matrix = sp.coo_matrix((np.concatenate(values), (np.concatenate(rows), np.concatenate(columns))), shape=(size, size)).tocsr()
    symmetry_error = np.max(np.abs((matrix-matrix.T).data)) if (matrix-matrix.T).nnz else 0
    magnetization = np.sum(spin, axis=0)
    source = ground*magnetization
    operator = sla.LinearOperator(matrix.shape, matvec=lambda x: matrix@x+ground*(ground@x))
    solution, info = sla.cg(operator, source, rtol=2e-12, atol=0)
    assert info == 0
    chi = source@solution
    chi0 = (source@source)/(1-gamma)
    record = {
        "n": n,
        "physical_configurations": size,
        "direct_response": float(chi),
        "direct_response_over_Glauber": float(chi/chi0),
        "symmetry_error": float(symmetry_error),
        "relative_Poisson_residual": float(np.linalg.norm(operator@solution-source)/np.linalg.norm(source)),
        "elapsed_seconds": time.perf_counter()-started,
    }
    print(json.dumps(record), flush=True)
    return record


if __name__ == "__main__":
    results = [audit(n) for n in (6, 8, 10, 12, 14, 16)]
    physical = [physical_check(n) for n in (6, 8, 10, 12, 14, 16)]
    assert all(abs(a["response_divided_by_Glauber_response"]-b["direct_response_over_Glauber"]) < 1e-9
               for a, b in zip(results, physical))
    Path(__file__).with_name("barw_regeneration_audit_results.json").write_text(
        json.dumps({"warning": "Float64 full dual and physical checks, not certified output", "results": results,
                    "independent_physical_checks": physical}, indent=2)+"\n")
