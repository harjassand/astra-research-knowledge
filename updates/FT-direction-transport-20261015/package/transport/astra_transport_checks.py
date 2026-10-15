#!/usr/bin/env python3
"""Reproducible algebraic checks for an UNVALIDATED physical hypothesis.

Requires Python 3.10+ and NumPy. Run:
    python astra_transport_checks.py --output astra_transport_check_results.json

No material data, ab initio calculation, molecular dynamics, or experiment is
included. Every energetic/rate input below is deliberately synthetic. Passing
these tests checks finite-dimensional algebra, not novelty or physical feasibility.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np

KB_EV_K = 8.617333262145e-5


def barrier_shift(K: np.ndarray, b: np.ndarray, f_a: np.ndarray,
                  f_s: np.ndarray, kappa: float) -> tuple[float, float]:
    """Return direct and Sherman--Morrison barrier shifts."""
    if kappa < 0:
        raise ValueError('Passive stiffness kappa must be nonnegative.')
    np.linalg.cholesky(K)
    kb = np.linalg.solve(K, b)
    compliance = float(b @ kb)
    p_a, p_s = float(kb @ f_a), float(kb @ f_s)
    changed = K + kappa * np.outer(b, b)
    original_barrier_relax = -0.5 * (f_s @ np.linalg.solve(K, f_s)
                                    - f_a @ np.linalg.solve(K, f_a))
    changed_barrier_relax = -0.5 * (f_s @ np.linalg.solve(changed, f_s)
                                   - f_a @ np.linalg.solve(changed, f_a))
    formula = kappa * (p_s**2 - p_a**2) / (2 * (1 + kappa * compliance))
    return float(changed_barrier_relax - original_barrier_relax), float(formula)


def current(a_l: float, a_r: float, b_l: float, b_r: float) -> float:
    """Net left-to-right current in a two-state, single-occupancy pore."""
    rates = (a_l, a_r, b_l, b_r)
    if any(r < 0 for r in rates) or sum(rates) == 0:
        raise ValueError('Rates must be nonnegative with a positive total.')
    return (a_l*b_r - a_r*b_l)/sum(rates)


def absorbed_reward(a_l: float, a_r: float, b_l: float, b_r: float,
                    h: float) -> dict[str, float]:
    """Exact first-passage lifetime and net right-port reward before damage.

    Empty -> occupied via either reservoir; occupied -> empty via either
    reservoir. Occupied -> absorbing failed state has rate h. Right reservoir
    entry is reward -1; right exit reward +1. Failure has zero reward.
    There is NO damage from the empty state in this illustrative model.
    """
    A, B = a_l+a_r, b_l+b_r
    if A <= 0 or h <= 0:
        raise ValueError('Entry sum and failure rate must be positive.')
    T = np.array([[-A, A], [B, -(B+h)]], dtype=float)
    reward_rate = np.array([-a_r, b_r], dtype=float)
    lifetime_solve = float(np.linalg.solve(-T, np.ones(2))[0])
    reward_solve = float(np.linalg.solve(-T, reward_rate)[0])
    lifetime_exact = (A+B+h)/(A*h)
    reward_exact = (a_l*b_r-a_r*b_l)/(A*h)-a_r/A
    return dict(lifetime_solve=lifetime_solve, lifetime_exact=lifetime_exact,
                reward_solve=reward_solve, reward_exact=reward_exact)


def run_checks() -> dict:
    rng = np.random.default_rng(20261015)
    matrix_errors = []
    response_errors = []
    for _ in range(1000):
        n = int(rng.integers(2, 10))
        M = rng.normal(size=(n,n))
        K = M.T @ M + np.eye(n)
        b, f_a, f_s = rng.normal(size=(3,n))
        kappa = 10.0**float(rng.uniform(-4,3))
        direct, formula = barrier_shift(K,b,f_a,f_s,kappa)
        matrix_errors.append(abs(direct-formula))
        # Verify d/dkappa of the constrained-state barrier in the common-K model.
        t = float(rng.uniform(0.1,3.0))
        eps = 1e-5
        upper = barrier_shift(K,b,f_a,f_s,t+eps)[0]
        lower = barrier_shift(K,b,f_a,f_s,t-eps)[0]
        inverse_b = np.linalg.solve(K+t*np.outer(b,b), b)
        exact_derivative = 0.5*((inverse_b@f_s)**2-(inverse_b@f_a)**2)
        response_errors.append(abs((upper-lower)/(2*eps)-exact_derivative))
    assert max(matrix_errors) < 1e-10
    assert max(response_errors) < 1e-7

    T_K = 300.0
    kT = KB_EV_K*T_K
    # Accessible relaxation contributions R_s = p_s^2/(2*s_b), in eV.
    # These are hypothetical model values, NOT values for any named material.
    R_a, R_u, R_h = 0.12, 0.02, 0.20
    local = []
    for eta in (0.0, 0.1, 1.0, 10.0, math.inf):
        fraction = 1.0 if math.isinf(eta) else eta/(1+eta)
        d_u = fraction*(R_u-R_a)
        d_h = fraction*(R_h-R_a)
        local.append(dict(kappa_times_compliance='infinity' if math.isinf(eta) else eta,
                          useful_barrier_shift_eV=d_u,
                          useful_saddle_shift_relative_to_empty_eV=fraction*R_u,
                          entry_multiplier=math.exp(-fraction*R_u/kT),
                          harmful_barrier_shift_eV=d_h,
                          useful_escape_multiplier=math.exp(-d_u/kT),
                          harmful_escape_multiplier=math.exp(-d_h/kT),
                          branching_selectivity_multiplier=math.exp((d_h-d_u)/kT)))
    q = local[2]['useful_escape_multiplier']
    alpha = local[2]['entry_multiplier']
    r = local[2]['harmful_escape_multiplier']
    networks = []
    for label,a_l,a_r in [('dilute',0.001,0.0001),
                         ('partly_blocked',10.0,1.0),
                         ('highly_blocked',1000.0,100.0)]:
        b_l=b_r=1.0
        A,B=a_l+a_r,b_l+b_r
        j0=current(a_l,a_r,b_l,b_r)
        j1=current(alpha*a_l,alpha*a_r,q*b_l,q*b_r)
        gain=alpha*q*(A+B)/(alpha*A+q*B)
        assert math.isclose(j1/j0,gain,rel_tol=1e-12)
        networks.append(dict(label=label, a_left=a_l, a_right=a_r,
                             b_left=1.0,b_right=1.0,
                             current_before_per_s=j0,current_after_per_s=j1,
                             current_multiplier=j1/j0,
                             initial_occupied_fraction=A/(A+B),
                             clamped_occupied_fraction=alpha*A/(alpha*A+q*B),
                             unlimited_escape_gain_with_fixed_entry=(A+B)/B))
    # Exact damage-inclusive first-passage test; no rare-event approximation here.
    before = absorbed_reward(10,1,1,1,1e-3)
    after = absorbed_reward(alpha*10,alpha*1,q,q,r*1e-3)
    for vals in (before,after):
        assert math.isclose(vals['lifetime_solve'],vals['lifetime_exact'],rel_tol=1e-9)
        assert math.isclose(vals['reward_solve'],vals['reward_exact'],rel_tol=1e-9)

    # Detailed balance cycle affinity unchanged by multiplying both exit rates.
    affinity_before=math.log((10*1)/(1*1))
    affinity_after=math.log((alpha*10*q)/(alpha*1*q))
    assert math.isclose(affinity_before,affinity_after,abs_tol=1e-14)
    assert current(1,1,1,1)==0
    assert current(alpha,alpha,q,q)==0

    j_A_cm2=0.010
    L_cm=0.010
    sigma0_S_cm=0.001
    sigma1_S_cm=0.010
    power0=j_A_cm2**2*L_cm/sigma0_S_cm
    power1=j_A_cm2**2*L_cm/sigma1_S_cm
    W_hold_A=0.5*R_a + 0.5*kT*math.log(2)
    return dict(
        status='INTERNAL_ALGEBRAIC_CHECKS_ONLY_NO_PHYSICAL_VALIDATION',
        seed=20261015,
        samples=1000,
        max_matrix_identity_absolute_error=max(matrix_errors),
        max_response_derivative_absolute_error=max(response_errors),
        temperature_K=T_K,kBT_eV=kT,
        hypothetical_relaxation_energies_eV=dict(initial=R_a,useful_saddle=R_u,harmful_saddle=R_h),
        local_barrier_examples=local,network_examples=networks,
        occupancy_ratio_threshold_for_net_gain=q*(1-alpha)/(alpha*(q-1)),
        tenfold_local_rate_lowering_needed_eV=kT*math.log(10),
        exact_absorbing_process=dict(before=before,after=after,
             net_delivered_before_failure_multiplier=after['reward_exact']/before['reward_exact'],
             mean_time_to_failure_multiplier=after['lifetime_exact']/before['lifetime_exact']),
        cycle_affinity_nats_before=affinity_before,cycle_affinity_nats_after=affinity_after,
        fixed_configuration_quasistatic_clamping_work_eV=W_hold_A,
        electrical_power_example=dict(inputs_are_assumed_not_measured=True,
            current_density_A_cm2=j_A_cm2,thickness_cm=L_cm,
            conductivity_before_S_cm=sigma0_S_cm,conductivity_after_S_cm=sigma1_S_cm,
            loss_before_W_cm2=power0,loss_after_W_cm2=power1,saving_W_cm2=power0-power1))


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('astra_transport_check_results.json'))
    args=parser.parse_args()
    result=run_checks()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=='__main__':
    main()
