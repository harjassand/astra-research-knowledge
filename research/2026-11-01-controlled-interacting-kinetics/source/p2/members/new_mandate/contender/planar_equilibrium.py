"""Independent Kac--Ward implementation and discriminating field tests.

No external research code is incorporated. The exact identity is conventional:
Lis (2016), A short proof of the Kac--Ward formula, DOI 10.4171/AIHPD/24.
Only open planar square grids, zero magnetic field, pairwise Ising couplings.
Double-precision LU is numerical evaluation of an exact algebraic identity;
it is not a certified interval calculation or a generic exact arithmetic solver.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix, eye
from scipy.sparse.linalg import splu
from scipy.special import logsumexp


def square_grid(side: int):
    positions = np.array([(x, y) for y in range(side) for x in range(side)])
    edges = []
    for y in range(side):
        for x in range(side):
            u = y * side + x
            if x + 1 < side:
                edges.append((u, u + 1))
            if y + 1 < side:
                edges.append((u, u + side))
    return positions, np.array(edges, dtype=np.int64)


def permutation_sign(perm):
    seen = np.zeros(len(perm), dtype=bool)
    cycles = 0
    for i in range(len(perm)):
        if seen[i]:
            continue
        cycles += 1
        j = i
        while not seen[j]:
            seen[j] = True
            j = int(perm[j])
    return -1 if (len(perm) - cycles) % 2 else 1


def kw_log_partition(positions, edges, K):
    """Return log Z, determinant phase residual, and LU nonzero count.

    T[e,f] = tanh(K_e) exp(i turn(e,f)/2), for head(e)=tail(f)
    and f != reverse(e). Source-edge weighting follows Lis (2016).
    Planarity is an input condition, not automatically established here.
    """
    directed = []
    bond = []
    outgoing = [[] for _ in positions]
    for k, (u, v) in enumerate(edges):
        for a, b in [(u, v), (v, u)]:
            outgoing[a].append(len(directed))
            directed.append((int(a), int(b)))
            bond.append(k)
    rows, cols, values = [], [], []
    weights = np.tanh(K)
    for e, (u, v) in enumerate(directed):
        vec_e = positions[v] - positions[u]
        for f in outgoing[v]:
            _, w = directed[f]
            if w == u:
                continue
            vec_f = positions[w] - positions[v]
            cross = vec_e[0]*vec_f[1] - vec_e[1]*vec_f[0]
            dot = np.dot(vec_e, vec_f)
            turn = np.arctan2(cross, dot)
            rows.append(e)
            cols.append(f)
            values.append(weights[bond[e]] * np.exp(0.5j * turn))
    dimension = len(directed)
    T = coo_matrix((values, (rows, cols)), shape=(dimension, dimension)).tocsc()
    A = eye(dimension, dtype=complex, format="csc") - T
    factor = splu(A)
    diagonal = factor.U.diagonal()
    log_abs = np.log(np.abs(diagonal)).sum()
    phase = np.angle(diagonal).sum()
    if permutation_sign(factor.perm_r) * permutation_sign(factor.perm_c) < 0:
        phase += np.pi
    phase_residual = float(abs(np.angle(np.exp(1j * phase))))
    # For physical real K, Z>0 and det(I-T) is a positive real square.
    log_cosh = np.logaddexp(K, -K) - np.log(2.0)
    result = len(positions)*np.log(2.0) + log_cosh.sum() + 0.5*log_abs
    return float(result), phase_residual, int(factor.L.nnz + factor.U.nnz)


def enumerated_ensemble(n, edges, K):
    if n > 20:
        raise ValueError("Enumeration deliberately restricted to at most 20 spins")
    integers = np.arange(1 << n, dtype=np.uint64)
    bits = (integers[:, None] >> np.arange(n, dtype=np.uint64)) & 1
    spins = 2*bits.astype(np.int8) - 1
    log_weights = (spins[:, edges[:, 0]] * spins[:, edges[:, 1]]) @ K
    magnetization = spins.sum(axis=1)
    return log_weights, magnetization


def field_statistics(logw, M, h):
    z = logsumexp(logw + h*M)
    p = np.exp(logw + h*M - z)
    return float(z), float(p @ M), float(p @ (M*M) - (p @ M)**2)


def conditional_gaussian_phase_prediction(logw, M, h):
    """Conventional two-phase resummation, with parameters EARNED by enumeration.

    M=0 is split evenly between the positive and negative components. The two
    components' full means/variances are computed, rather than assuming +/-N.
    Gaussian conditional cumulant truncation is an approximation.
    """
    z0 = logsumexp(logw)
    p = np.exp(logw-z0)
    phases = []
    for sign in [-1, 1]:
        mask = (sign*M > 0).astype(float) + 0.5*(M == 0)
        mass = np.dot(p, mask)
        mu = np.dot(p*mask, M) / mass
        var = np.dot(p*mask, (M-mu)**2) / mass
        phases.append((mass, mu, var))
    log_terms = np.array([np.log(w)+h*mu+0.5*h*h*var for w, mu, var in phases])
    f = logsumexp(log_terms)
    phase_weights = np.exp(log_terms-f)
    m = sum(w*(mu+h*var) for w, (_, mu, var) in zip(phase_weights, phases))
    return float(z0+f), float(m), phases


def run():
    rng = np.random.default_rng(27012026)
    results = {"seed": 27012026, "validation": [], "large_cases": [], "field_response": []}
    for side in [2, 3, 4]:
        positions, edges = square_grid(side)
        for label, J in [
            ("ferromagnetic", np.ones(len(edges))),
            ("signed_disorder", rng.choice([-1.0, 1.0], len(edges))),
            ("continuous_disorder", rng.uniform(-1, 1, len(edges))),
        ]:
            for beta in [0.2, 0.6, 1.2]:
                K = beta*J
                logw, _ = enumerated_ensemble(len(positions), edges, K)
                exact = float(logsumexp(logw))
                kw, phase, nnz = kw_log_partition(positions, edges, K)
                results["validation"].append(dict(side=side, kind=label, beta=beta,
                    logZ_enumeration=exact, logZ_KW=kw, absolute_error=abs(exact-kw),
                    determinant_phase_residual=phase))
    for side in [8, 16, 32, 64]:
        positions, edges = square_grid(side)
        K = 0.6*rng.choice([-1.0, 1.0], len(edges))
        start = time.perf_counter()
        kw, phase, nnz = kw_log_partition(positions, edges, K)
        elapsed = time.perf_counter()-start
        results["large_cases"].append(dict(side=side, sites=len(positions), edges=len(edges),
            matrix_dimension=2*len(edges), logZ_KW=kw, determinant_phase_residual=phase,
            lu_nonzeros=nnz, wall_seconds=elapsed, independent_exact_validation=False))

    positions, edges = square_grid(4)
    n = len(positions)
    logw, M = enumerated_ensemble(n, edges, np.full(len(edges), 0.8))
    z0, _, var0 = field_statistics(logw, M, 0)
    for h in [0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4]:
        z, m, var = field_statistics(logw, M, h)
        zmix, mmix, phases = conditional_gaussian_phase_prediction(logw, M, h)
        results["field_response"].append(dict(sites=n, betaJ=0.8, dimensionless_field=h,
            field_times_volume=h*n, exact_logZ_change=z-z0, exact_m_per_site=m/n,
            global_linear_m_per_site=h*var0/n,
            global_second_order_logZ_change=0.5*h*h*var0,
            phase_gaussian_m_per_site=mmix/n,
            phase_gaussian_logZ_change=zmix-z0,
            phase_parameters=phases))

    # A deliberately frustrated single plaquette: the exact even-subgraph
    # polynomial is 1 - tanh(beta)^4, exposing cancellation at low temperature.
    positions, edges = square_grid(2)
    J = np.ones(len(edges)); J[0] = -1
    results["cold_frustrated_plaquette"] = []
    for beta in [1, 5, 10, 15, 20, 30]:
        logw, _ = enumerated_ensemble(4, edges, beta*J)
        exact = float(logsumexp(logw))
        try:
            kw, phase, _ = kw_log_partition(positions, edges, beta*J)
            record = dict(beta=beta, exact=exact, kw=kw, error=abs(exact-kw), phase=phase)
        except (RuntimeError, ValueError) as exc:
            record = dict(beta=beta, exact=exact, failure=type(exc).__name__+": "+str(exc))
        results["cold_frustrated_plaquette"].append(record)

    # This is exact as a two-state model, not a proof of finite-temperature
    # two-dimensional phase structure. It isolates the nonuniform response.
    results["two_state_collective_scaling"] = []
    for n in [16, 64, 256, 1024, 4096]:
        h = 0.01
        results["two_state_collective_scaling"].append(dict(sites=n, h=h,
            exact_m_per_site=float(np.tanh(n*h)), linear_m_per_site=n*h,
            first_complex_zero_distance=np.pi/(2*n)))

    out = Path(__file__).with_name("planar_results.json")
    out.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({"max_validation_abs_logZ_error":max(x["absolute_error"] for x in results["validation"]),
        "large_cases":results["large_cases"], "field_response":results["field_response"],
        "cold_frustrated_plaquette": results["cold_frustrated_plaquette"]}, indent=2))


if __name__ == "__main__":
    run()
