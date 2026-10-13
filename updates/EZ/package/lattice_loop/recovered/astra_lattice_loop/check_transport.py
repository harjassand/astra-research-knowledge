#!/usr/bin/env python3
"""Algebra checks for a conditional two-sublattice stochastic pump.

This is NOT a simulation of beta-alumina, LLTO, or any identified material.
Units: k_B T = 1, cell length a = 1. The baseline occupation relaxation rate
lambda0 sets the time unit. No material coupling, optical efficiency, or
experimental signal is predicted by these tests.

Requires Python >= 3.10, NumPy, SciPy.
Run: python check_transport.py --output checks.json
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

TWOPI = 2.0 * math.pi


def rates(u: float, v: float, k: float) -> tuple[float, float, float, float]:
    """A_n->B_n, B_n->A_n, B_n->A_(n+1), A_(n+1)->B_n."""
    return (k * math.exp(-v-u/2), k * math.exp(-v+u/2),
            k * math.exp(v+u/2), k * math.exp(v-u/2))


def cycle(u0: float, U: float, V: float, omega: float, phi: float,
          lambda0: float = 1.0) -> dict[str, float]:
    if omega <= 0 or lambda0 <= 0:
        raise ValueError('omega and lambda0 must be positive')
    k = lambda0 / (4 * math.cosh(u0/2))
    def controls(theta: float) -> tuple[float, float, float, float]:
        u, v = u0+U*math.cos(theta), V*math.cos(theta+phi)
        lam = 4*k*math.cosh(v)*math.cosh(u/2)
        peq = 1/(1+math.exp(u))
        return u, v, lam/omega, peq
    def affine_rhs(theta: float, y: np.ndarray) -> list[float]:
        _, _, alpha, peq = controls(theta)
        return [alpha*(peq-y[0]), alpha]
    opts = dict(rtol=2e-11, atol=2e-13, max_step=TWOPI/300)
    affine = solve_ivp(affine_rhs, (0, TWOPI), [0, 0], **opts)
    if not affine.success:
        raise RuntimeError(affine.message)
    b, integral = affine.y[:, -1]
    p_init = b/(-math.expm1(-integral))
    def rhs(theta: float, y: np.ndarray) -> list[float]:
        u, v, alpha, peq = controls(theta)
        pprime = alpha*(peq-y[0])
        r1p, r1m, r2p, r2m = rates(u, v, k)
        J1 = r1p*(1-y[0])-r1m*y[0]
        J2 = r2p*y[0]-r2m*(1-y[0])
        dx_direct = (J1+J2)/(2*omega)
        dx_identity = -0.5*math.tanh(v)*pprime
        return [pprime, dx_direct, dx_identity]
    sol = solve_ivp(rhs, (0, TWOPI), [p_init, 0, 0], **opts)
    if not sol.success:
        raise RuntimeError(sol.message)
    peq0 = 1/(1+math.exp(u0))
    d2 = (math.pi/2 * peq0*(1-peq0)*U*V
          * lambda0/(lambda0**2+omega**2)
          * (lambda0*math.sin(phi)+omega*math.cos(phi)))
    return dict(u0=u0,U=U,V=V,omega=omega,phi=phi,
                delta_x_over_a=float(sol.y[1,-1]),
                identity_value=float(sol.y[2,-1]),
                perturbative_value=d2,
                periodic_residual=float(sol.y[0,-1]-p_init))


def run() -> dict:
    cases=[]
    for u0 in (0.,0.7):
        for omega in (.1,1.,10.):
            for phi in (math.pi/2,-math.pi/2,0.,math.pi/3,-math.pi/3):
                row=cycle(u0,.03,.025,omega,phi)
                assert abs(row['delta_x_over_a']-row['identity_value']) < 2e-11
                assert abs(row['periodic_residual']) < 2e-10
                assert math.isclose(row['delta_x_over_a'],row['perturbative_value'],
                                    rel_tol=0.002,abs_tol=2e-10)
                cases.append(row)
    nulls=[]
    for U,V in ((0.,.4),(.4,0.)):
        row=cycle(.2,U,V,1.,math.pi/2)
        assert abs(row['delta_x_over_a']) < 2e-11
        nulls.append(row)
    for u,v in ((-.4,.8),(.4,-.2),(0.,0.)):
        ap,am,bp,bm=rates(u,v,.7)
        assert abs(math.log(ap/am)+u) < 1e-12
        assert abs(math.log(bp/bm)-u) < 1e-12
        assert abs(math.log(ap*bp/(am*bm))) < 1e-12
    for plus in cases:
        if plus['phi'] <= 0:
            continue
        minus=next(x for x in cases if x['u0']==plus['u0']
                   and x['omega']==plus['omega'] and x['phi']==-plus['phi'])
        # Isolate the orientation-odd part. The complete finite-rate current
        # also has a phase-even term; phi=0 cases above check that term.
        odd=.5*(plus['delta_x_over_a']-minus['delta_x_over_a'])
        p0=1/(1+math.exp(plus['u0']))
        expected=(math.pi/2*p0*(1-p0)*.03*.025
                  /(1+plus['omega']**2)*math.sin(plus['phi']))
        assert math.isclose(odd,expected,rel_tol=.002,abs_tol=2e-10)
    # Joint-control elastic-energy identity; dimensionless algebra only.
    # K and A here are synthetic test fixtures, NOT measured crystal data.
    rng=np.random.default_rng(1427)
    energy_checks=[]
    for _ in range(8):
        R=rng.normal(size=(5,5))
        K=R.T@R+np.eye(5)
        A=rng.normal(size=(2,5))
        y=rng.normal(size=2)
        KiAt=np.linalg.solve(K,A.T)
        M=A@KiAt
        Qstar=KiAt@np.linalg.solve(M,y)
        energy_direct=float(Qstar@K@Qstar/2)
        energy_bound=float(y@np.linalg.solve(M,y)/2)
        assert np.linalg.norm(A@Qstar-y) < 1e-11
        assert abs(energy_direct-energy_bound) < 1e-10
        # Add a nullspace displacement; it cannot lower the energy.
        z=rng.normal(size=5)
        z-=A.T@np.linalg.solve(A@A.T,A@z)
        assert (Qstar+z)@K@(Qstar+z)/2 >= energy_direct-1e-10
        energy_checks.append(dict(constraint_residual=float(np.linalg.norm(A@Qstar-y)),
                                  minimum_energy=energy_direct))
    kB_eV=8.617333262145e-5
    T=300.
    # Explicitly stipulated engineering targets, NOT measured material values.
    target_pattern_m=10e-9
    target_keep_s=3600.
    target_fraction=.9
    diffusion_ceiling=(-math.log(target_fraction)*target_pattern_m**2
                       /(4*math.pi**2*target_keep_s))
    # Single loading/unloading cycle, each excursion sharing fidelity equally.
    target_step_fraction=.99
    s=math.sqrt(target_step_fraction)
    u_amplitude_eV=2*kB_eV*T*math.atanh(s)
    v_amplitude_eV=kB_eV*T*math.atanh(s)
    # Paper numbers used only for an explicitly conditional duty-cycle test.
    eis_fraction=.0078
    pulse_rate_Hz=250.
    tail_s=1.03e-9
    equivalent_peak=eis_fraction/(pulse_rate_Hz*tail_s)
    # Pump output conversion; this is NOT wall-plug efficiency.
    optical_to_THz=6e-6/4.2e-3
    return dict(status='Algebra checks passed; no material prediction or physical validation.',
                assumptions='Independent ions; translation-invariant periodic chain; Markov hopping; common attempt scale; no external force during model cycle.',
                cases=cases,nulls=nulls,joint_control_energy_checks=energy_checks,
                target_calculations=dict(T_K=T,
                  ninety_percent_10nm_sinusoid_retained_one_hour_D_max_m2_s=diffusion_ceiling,
                  ninety_nine_percent_step_U_balanced_bound_threshold_eV=u_amplitude_eV,
                  ninety_nine_percent_step_V_balanced_bound_threshold_eV=v_amplitude_eV,
                  conditional_EIS_fast_only_peak_fraction=equivalent_peak,
                  conditional_EIS_pulse_rate_Hz=pulse_rate_Hz,
                  conditional_EIS_tail_s=tail_s,
                  optical_output_to_THz_output_fraction=optical_to_THz),
                numerical_limits='Floating-point SciPy DOP853, not interval certified. Perturbation checks at dimensionless small amplitudes. EIS calculation requires a same-observable linear-response correspondence that is NOT established across published instruments.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('checks.json'))
    args=parser.parse_args()
    result=run()
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],
                      'target_calculations':result['target_calculations'],
                      'largest_periodic_residual':max(abs(x['periodic_residual']) for x in result['cases'])},indent=2))
