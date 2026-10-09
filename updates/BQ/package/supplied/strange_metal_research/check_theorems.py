#!/usr/bin/env python3
"""Finite-network checks of conditional local-thermal noise statements.

These are synthetic numerical checks, NOT experimental validation and NOT a
formal proof. The accompanying RESEARCH_NOTE.md supplies the proofs and scope.
Requires Python 3.10+, numpy, scipy. Outputs JSON; no network access required.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import root

Array = NDArray[np.float64]
SEED = 20261009


def incidence(n: int, edges: list[tuple[int, int]]) -> Array:
    """Oriented E x N incidence; node n-1 is the grounded terminal."""
    D = np.zeros((len(edges), n))
    for e, (i, j) in enumerate(edges):
        D[e, i] = 1.0
        D[e, j] = -1.0
    return D


def electrical(D: Array, r: Array) -> dict[str, Any]:
    """Solve for unit terminal current, without graph-library dependencies."""
    if np.any(r <= 0):
        raise ValueError("All resistances must be positive.")
    Dr = D[:, :-1]
    g = 1.0 / r
    L = Dr.T @ (g[:, None] * Dr)
    source = np.zeros(L.shape[0]); source[0] = 1.0
    potential = np.r_[np.linalg.solve(L, source), 0.0]
    R = float(potential[0])
    j = (D @ potential) * g
    # Electrical current response to an additive edge voltage source.
    M = ((g[:, None] * Dr) @ np.linalg.solve(L, Dr.T * g[None, :])
         - np.diag(g))
    return {"R": R, "j": j, "potential": potential, "M": M}


def random_graph(rng: np.random.Generator, n: int) -> Array:
    # The chain makes connectivity certain. Extra edges need not be planar.
    edges = [(i, i + 1) for i in range(n - 1)]
    edges += [(i, j) for i in range(n) for j in range(i + 2, n)
              if rng.random() < 0.18]
    return incidence(n, edges)


def static_check(D: Array, geom: Array, a: float, b: float,
                 T: Array, Tlo: float, Thi: float) -> dict[str, float]:
    """Common local resistance law r_e=geom_e*(a+b*T_e)."""
    net = electrical(D, geom * (a + b * T))
    baseline = electrical(D, geom)
    R = net['R']; G = 1.0 / R; K0 = 1.0 / baseline['R']
    v = net['potential'] / R
    v0 = baseline['potential'] / baseline['R']
    k = 1.0 / geom
    drop = D @ v
    E = float(np.sum(k * (D @ (v - v0))**2))
    TN = float(np.sum(T * drop**2 / (geom * (a + b * T))) / G)
    TR = (R * K0 - a) / b
    residual = R * E / b
    upper = TR + b * (TR - Tlo) * (Thi - TR) / (a + b * TR)
    # For b>0, TR is the lower bound. For b<0 the order reverses.
    low_bound, high_bound = sorted([TR, upper])
    return {
        'R': R, 'TN': TN, 'TR': TR, 'residual': residual,
        'identity_error': abs(TN - TR - residual),
        'lower_margin': TN - low_bound,
        'upper_margin': high_bound - TN,
    }


def thermal_matrix(rng: np.random.Generator, m: int) -> tuple[Array, Array, Array]:
    """Reciprocal conductances, positive bath leaks, positive heat capacities."""
    W = rng.uniform(0.0, 0.3, (m, m))
    W = np.triu(W, 1); W = W + W.T
    leak = rng.uniform(0.4, 1.5, m)
    A = np.diag(W.sum(axis=1) + leak) - W
    C = np.diag(rng.uniform(0.3, 2.0, m))
    return A, C, W


def finite_bias_noise(D: Array, geom: Array, a: float, b: float,
                      Tb: float, A: Array, C: Array, W: Array,
                      I: float, omega: float) -> dict[str, Any]:
    """Explicit electrothermal Langevin model; k_B is set to 1.

    Thermal law: A(T-Tb)=local Joule power. Independent thermal-link noise
    has one-sided PSD 2*g*(T_left**2+T_right**2). Only its equilibrium
    4*Tb**2*A value is required for the weak-bias theorem.
    """
    m = len(geom)
    beta = geom * b
    baseline = electrical(D, geom * (a + b * Tb))
    q0 = geom * (a + b * Tb) * baseline['j']**2
    guess = Tb + I**2 * np.linalg.solve(A, q0)

    def heat_equation(T: Array) -> Array:
        r = geom * (a + b * T)
        if np.any(r <= 0):
            return 1e12 * (T - guess)
        e = electrical(D, r)
        return A @ (T - Tb) - I**2 * r * e['j']**2

    sol = root(heat_equation, guess, method='hybr', options={'xtol': 1e-11})
    if np.linalg.norm(heat_equation(sol.x), ord=np.inf) > 1e-9:
        raise RuntimeError(f"Steady heat solve did not converge: {sol.message}")
    T = sol.x
    r = geom * (a + b * T)
    e = electrical(D, r)
    R = e['R']; j = e['j']; i = I * j; M = e['M']
    dRdT = beta * j**2
    K = 2.0 * np.diag(r * i) @ M + np.diag(i)
    Jp = (np.diag(i**2) + 2.0 * np.diag(r * i) @ M @ np.diag(i)) @ np.diag(beta)
    H = np.linalg.inv(A - Jp + 1j * omega * C)
    hQ = I * dRdT @ H
    he = j + hQ @ K
    Ce = np.diag(4.0 * T * r)
    leak = np.diag(A) - W.sum(axis=1)
    CQ = np.diag(2.0 * leak * (T**2 + Tb**2))
    for p in range(m):
        for q in range(p + 1, m):
            vec = np.zeros(m); vec[p] = 1.0; vec[q] = -1.0
            CQ += 2.0 * W[p, q] * (T[p]**2 + T[q]**2) * np.outer(vec, vec)
    S = float(np.real(he @ Ce @ he.conj() + hQ @ CQ @ hQ.conj()))
    Z = R + 2.0 * I**2 * dRdT @ H @ (r * j**2)
    return {'T': T, 'R': R, 'Z': Z, 'S': S, 'R0': baseline['R']}


def main() -> None:
    rng = np.random.default_rng(SEED)
    max_identity = 0.0
    min_lower = float('inf'); min_upper = float('inf')
    static_cases = 1500
    for _ in range(static_cases):
        n = int(rng.integers(2, 22)); D = random_graph(rng, n)
        geom = np.exp(rng.uniform(-2.0, 2.0, D.shape[0]))
        Tlo = float(rng.uniform(0.2, 4.0)); Thi = Tlo + float(rng.uniform(1.0, 40.0))
        a = float(rng.uniform(0.1, 10.0)); b = float(rng.uniform(0.2, 3.0))
        T = rng.uniform(Tlo, Thi, D.shape[0])
        z = static_check(D, geom, a, b, T, Tlo, Thi)
        max_identity = max(max_identity, z['identity_error'] / (1 + abs(z['TN'])))
        min_lower = min(min_lower, z['lower_margin'])
        min_upper = min(min_upper, z['upper_margin'])
    assert max_identity < 1e-10 and min_lower > -1e-9 and min_upper > -1e-9

    series = static_check(incidence(3, [(0, 1), (1, 2)]), np.array([0.7, 0.3]),
                          2.0, 3.0, np.array([1.0, 10.0]), 1.0, 10.0)
    parallel = static_check(incidence(2, [(0, 1), (0, 1)]), np.array([0.7, 0.3]),
                            2.0, 3.0, np.array([1.0, 10.0]), 1.0, 10.0)
    assert abs(series['upper_margin']) < 1e-12
    assert abs(parallel['lower_margin']) < 1e-12

    # Deliberately leave the material-law hypothesis: rho(T)=T^2 in parallel.
    convex_TN = (1.0 + 0.1) / 1.01
    convex_TR = np.sqrt(2.0 / 1.01)
    assert convex_TN < convex_TR
    # A constant-resistance cold contact invalidates common fractional slope.
    contact = {'TR_from_terminal_calibration': 10.0,
               'actual_TN': (10.0 * 1.0 + 10.0 * 10.0) / 20.0}

    # Weak-bias identity using independently assembled finite-bias covariances.
    mchecks = []
    for _ in range(20):
        n = int(rng.integers(3, 7)); D = random_graph(rng, n)
        geom = np.exp(rng.uniform(-0.4, 0.4, D.shape[0]))
        a = 2.0; b = 0.7; Tb = 1.3
        A, C, W = thermal_matrix(rng, len(geom))
        baseline = electrical(D, geom * (a + b * Tb))
        R0 = baseline['R']; c = b / (a + b * Tb)
        q = geom * (a + b * Tb) * baseline['j']**2
        H0 = float(q @ np.linalg.solve(A, q)); R2 = c * H0
        for omega in [0.0, 0.7, 7.0]:
            Hw = q @ np.linalg.solve(A + 1j * omega * C, q)
            phi = float(np.real(Hw) / H0)
            assert -1e-12 <= phi <= 1.0 + 1e-12
            predicted_S2 = 4.0 * R2 * (1.0 / c + Tb + (2.0 * Tb + c * Tb**2) * phi)
            errors = []
            for I in [0.004, 0.002]:
                z = finite_bias_noise(D, geom, a, b, Tb, A, C, W, I, omega)
                measured_S2 = (z['S'] - 4.0 * Tb * R0) / I**2
                errors.append(abs(measured_S2 - predicted_S2) / max(1.0, abs(predicted_S2)))
                eliminated = 4.0 * ((Tb + 1.0/c) * (z['R'] - R0)
                                   + (Tb + 0.5*c*Tb**2) * (np.real(z['Z']) - z['R']))
                assert abs((z['S'] - 4.0*Tb*R0) - eliminated) < 1e-6
            mchecks.append({'phi': phi, 'relative_error_I_0p004': errors[0],
                            'relative_error_I_0p002': errors[1]})
    assert max(x['relative_error_I_0p002'] for x in mchecks) < 1e-4

    # Explicit finite-bias failure of applying the frozen theorem at zero frequency.
    # Two parallel branches: cold r=2,T=1, hot r=18,T=100, same affine material law.
    Tb = 1.0; Th = 100.0; rc = 2.0; rh = 18.0
    beta_h = 18.0 / 101.0; V = 1.0; ih = V / rh
    gh = 1.0/rh; gc = 1.0/rc
    Gth = ih**2 * rh / (Th - Tb)
    loop = ih**2 * beta_h / Gth
    attenuation = 1.0/(1.0 + loop)
    Y = gc + gh * (1.0-loop)/(1.0+loop)
    johnson_current = 4.0*(Tb*gc + Th*gh*attenuation**2)
    heat_current = ((ih*beta_h/rh) / (Gth*(1.0+loop)))**2 * 2.0*Gth*(Th**2+Tb**2)
    actual_S = (johnson_current + heat_current) / Y**2
    R = 1.0 / (gc + gh); TN_frozen = (Tb*gc + Th*gh)/(gc+gh)
    actual_TN = actual_S/(4.0*R)
    assert actual_TN < TN_frozen

    out = {
        'status': 'Synthetic numerical checks only; no empirical validation or formal proof.',
        'seed': SEED,
        'static': {'cases': static_cases, 'maximum_scaled_identity_error': max_identity,
                   'minimum_lower_margin': min_lower, 'minimum_upper_margin': min_upper,
                   'series_upper_saturation': series, 'parallel_lower_saturation': parallel},
        'scope_counterexamples': {
            'convex_material_parallel': {'TN': convex_TN, 'TR': float(convex_TR)},
            'cold_different_material_contact': contact,
            'finite_bias_electrothermal_parallel': {
                'R': R, 'Z_zero_frequency': 1.0/Y, 'hot_temperature': Th,
                'cold_temperature': Tb, 'local_loop_gain_hot': loop,
                'frozen_TN_equals_TR': TN_frozen, 'actual_effective_TN': actual_TN,
                'actual_noise_over_frozen_noise': actual_TN / TN_frozen,
                'assumed_heat_link_PSD': '2*k_B*G*(T_hot^2+T_bath^2)',
                'note': 'Ordinary specified Langevin countermodel; not a model fitted to YbRh2Si2.'}},
        'weak_bias': {'network_frequency_cases': len(mchecks),
                      'maximum_relative_S2_error_at_I_0p002': max(x['relative_error_I_0p002'] for x in mchecks),
                      'median_error_ratio_halving_I': float(np.median([x['relative_error_I_0p004']/max(x['relative_error_I_0p002'],1e-15) for x in mchecks])),
                      'checks': mchecks}}
    dest = Path(__file__).resolve().parent / 'results' / 'synthetic_checks.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'weak_bias'}, indent=2))
    print(json.dumps({k:v for k,v in out['weak_bias'].items() if k != 'checks'}, indent=2))


if __name__ == '__main__':
    main()
