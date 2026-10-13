#!/usr/bin/env python3
"""Bounded checks for source transfer, full mechanical gates, passive controls.

Only reads the hash-pinned inherited copies and writes this directory.
No standing-mode search or assumed-Q optimization is repeated.
"""
from pathlib import Path
from dataclasses import replace
import hashlib
import json
import math
import platform
import sys
import time

import numpy as np
from scipy.integrate import simpson
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'inherited'))
import nonlinear_transport as model
import strong_controls


def transfer_window(omega, maximum):
    """C1 nonnegative response-surface witness; not an acquired material law."""
    x = np.clip((np.asarray(omega) - maximum) / maximum, 0.0, 1.0)
    return 1.0 - x*x*(3.0 - 2.0*x)


def main():
    tic = time.perf_counter()
    p = model.Parameters()
    standing = json.loads((HERE/'inherited/standing_mode.json').read_text())
    preferred = min((c for c in standing['cases'] if not c['any_OSP_chi_extrapolation']),
                    key=lambda c: c['total_electric_before_idle_W'])
    base = HERE/'inherited/sources/biaxial_raw/biaxial_repository'
    source_rates = []
    for amp in ('0.5', '0.7', '1.0', '1.5', '2.0', '3.0', '5.0'):
        curve = np.loadtxt(base/f'fig1d/fig1d_{amp}_primary.csv', delimiter=',')
        a = float(amp)/100.0
        omega = curve[:, 0]*0.2/a
        source_rates.append({'strain_amplitude': a, 'points': len(curve),
                             'omega_min_rad_s': float(omega.min()),
                             'omega_max_rad_s': float(omega.max()),
                             'chi_min': float(curve[:, 0].min()),
                             'chi_max': float(curve[:, 0].max())})
    direct = np.loadtxt(base/'fig1c/fig1c_primary.csv', delimiter=',')
    omega_max = max(direct[:, 0].max(), max(r['omega_max_rad_s'] for r in source_rates))
    assert np.max(np.abs(direct[:, 0]*0.01/0.2 -
               np.loadtxt(base/'fig1d/fig1d_1.0_primary.csv', delimiter=',')[:, 0])) < 1e-12
    q = preferred['flow_L_min']/60000.0
    volume0 = math.pi*p.radius**2*p.length
    passive_receipts = []
    # Within the inherited real-viscous torsion model, the fluid's added
    # inertia cannot exceed rigid rotation. Positive ground springs and loss
    # cannot create a driving-point zero-reactance below a positive-definite
    # stiffness-minus-inertia matrix. This gate is independent of Q/support k.
    J = math.pi*((p.radius+p.steel_thickness)**4-p.radius**4)/2
    G = 79e9
    is_steel = p.steel_density*J
    is_fluid_rigid = p.density*math.pi*p.radius**4/2
    is_arms = 2*(.099+.5/3)*(.5**2)
    denominator = (is_steel+is_fluid_rigid)*p.length**2/math.pi**2 + is_arms*p.length/4
    lower_hz = math.sqrt(G*J/denominator)/(2*math.pi)
    necessary_extra_point_inertia = max(0.,4/p.length*(G*J/omega_max**2-
                               (is_steel+is_fluid_rigid)*p.length**2/math.pi**2)-is_arms)
    aa=(is_steel+is_fluid_rigid)/math.pi**2
    bb=is_arms/4
    necessary_length = (-bb+math.sqrt(bb*bb+4*aa*G*J/omega_max**2))/(2*aa)
    nz = preferred['axial_nodes']
    h = p.length/(nz-1)
    k = G*J/h*(np.diag(np.full(nz-2,2.))+np.diag(np.full(nz-3,-1.),1)+np.diag(np.full(nz-3,-1.),-1))
    mi = np.full(nz-2,(is_steel+is_fluid_rigid)*h)
    mi[(nz-2)//2] += is_arms
    normalized = k/np.sqrt(mi[:,None]*mi[None,:])
    discrete_rigid_lower_hz = math.sqrt(np.linalg.eigvalsh(normalized)[0])/(2*math.pi)
    assert lower_hz > omega_max/(2*math.pi)
    assert discrete_rigid_lower_hz > omega_max/(2*math.pi)

    def passive(diameter):
        radius = diameter/2
        mean = q/(math.pi*radius**2)
        g, power = model.unactuated_matched(mean, replace(p, radius=radius))
        return {'ID_m': diameter, 'pressure_gradient_Pa_m': g, 'electric_W': power,
                'inventory_L': 1000*math.pi*radius**2*p.length,
                'mean_residence_min': math.pi*radius**2*p.length/q/60,
                'inventory_factor': (radius/p.radius)**2}

    active = preferred['total_electric_before_idle_W']
    dmatch = brentq(lambda d: passive(d)['electric_W'] - active, .125, .161, xtol=1e-13)
    for d in (.125, .128, .130, .132, .134, .136, .140, .14348279661344573, .161, dmatch):
        passive_receipts.append(passive(d))
    inventory250_diameter = math.sqrt(4*.250/(math.pi*p.length))
    passive250 = passive(inventory250_diameter)
    film_match = brentq(lambda delta: strong_controls.wall_film(q/(math.pi*p.radius**2), delta, p)['electric_W']-active,
                       0.0, 20e-6, xtol=1e-16)
    film_controls = [strong_controls.wall_film(q/(math.pi*p.radius**2), delta, p)
                     for delta in (film_match, 2e-6, 5e-6, 10e-6, 20e-6)]

    # Direct plant impedance includes *all* loaded fluid, structural and
    # support torques. This is measurable and needs no guessed Q or spring k.
    # T_pk=Z*Omega_pk; two identical coils at lever ell give
    # Pcu = Rc*Omega_pk^2*|Z|^2/(4*ell^2*Kf^2).
    Omega = preferred['wall_velocity_peak']/p.radius
    Rc, Kf, ell, inductance = 11.5, 27.8, .5, .0045
    a = .5*Omega**2
    b = Rc*Omega**2/(4*ell**2*Kf**2)
    axial = preferred['axial_fluid_power_W']/p.pump_efficiency
    z_real = 2*preferred['drive_mechanical_power_W']/Omega**2
    torque = 2*ell*preferred['actuator_peak_force_N']
    z_abs = torque/Omega
    z_imag_abs = math.sqrt(max(0., z_abs*z_abs-z_real*z_real))
    gates = []
    for comparator in (passive(.125), passive250, passive(dmatch), passive(.161)):
        headroom = comparator['electric_W']-axial
        xmax = (-a + math.sqrt(a*a+4*b*headroom))/(2*b) if headroom > 0 else None
        gates.append({'comparator_ID_m': comparator['ID_m'],
                      'comparator_inventory_L': comparator['inventory_L'],
                      'comparator_W': comparator['electric_W'],
                      'headroom_for_plant_copper_driver_W': headroom,
                      'measured_gate': 'a*Re(Z)+b*abs(Z)^2+P_extra < headroom; Re(Z)>=0. P_extra includes driver idle/conversion and non-fundamental copper losses.',
                      'a': a, 'b': b,
                      'maximum_resonant_ReZ_if_driver_extra_zero': xmax,
                      'driver_extra_budget_at_saved_model_Z_W': headroom-a*z_real-b*z_abs*z_abs})
    ipk = torque/(2*ell*Kf)
    # Coil voltage check assumes saved near-resonant in-phase force/velocity.
    vpk = abs((Rc+1j*preferred['omega']*inductance)*ipk + Kf*ell*Omega)

    # Re-evaluate only the five frozen local fluid states, not mode iteration.
    local = []
    for saved in preferred['local_rows'][:5]:
        row = model.coupled(saved['pressure_gradient'], preferred['omega'], saved['wall_velocity'],
                            replace(p, length=1.0), n=48)
        assert row['converged']
        rr = np.linspace(0,p.radius,len(row['gamma']))
        amp = np.abs(row['shear'])/preferred['omega']
        flux_integrand = rr*rr*row['gamma']
        total_flux = simpson(flux_integrand, x=rr)
        amp_mask = amp >= .005
        rate_mask = np.abs(row['gamma']/.2-1) <= .1
        local.append({'wall_velocity_m_s': saved['wall_velocity'],
                      'amplitude_min': float(amp.min()), 'amplitude_max': float(amp.max()),
                      'primary_rate_max_s_inv': float(row['gamma'].max()),
                      'flux_fraction_amp_at_least_0_5pct': float(simpson(np.where(amp_mask,flux_integrand,0),x=rr)/total_flux),
                      'flux_fraction_primary_rate_within_10pct_of_source': float(simpson(np.where(rate_mask,flux_integrand,0),x=rr)/total_flux),
                      'all_local_points_outside_source_frequency': bool(preferred['omega'] > omega_max),
                      'flux_fraction_with_all_frequency_rate_amplitude_conditions': 0.0,
                      'note': 'Quadrature diagnostic on the inherited conditional state; masks at cell faces are not rigorously integrated interfaces.'})

    all_source_omegas = np.concatenate([np.loadtxt(base/f'fig1d/fig1d_{amp}_primary.csv',delimiter=',')[:,0]*.2/(float(amp)/100)
                                      for amp in ('0.5','0.7','1.0','1.5','2.0','3.0','5.0')])
    witness_check = {'class': 'frequency-dependent cycle-averaged dissipative response surfaces',
                     'not_claimed': 'A validated causal particle model or impossibility of all active devices',
                     'q_at_every_used_raw_source_frequency_exactly_one': bool(np.all(transfer_window(all_source_omegas,omega_max)==1)),
                     'q_at_all_standing_modes_exactly_zero': bool(np.all(transfer_window(np.array([c['omega'] for c in standing['cases']]),omega_max)==0)),
                     'source_max_omega_rad_s': float(omega_max),
                     'source_max_hz': float(omega_max/(2*math.pi)),
                     'standing_preferred_frequency_factor_outside_source': preferred['omega']/omega_max,
                     'convexity_proof': 'eta_B=(1-q)*eta_0+q*eta_A; both eta_A,eta_0>=0 and 0<=q<=1 imply eta_B>=0.',
                     'no_suppression_active_hydraulic_W': preferred['baseline_electric_W'],
                     'no_suppression_total_W_lower_bound': preferred['baseline_electric_W'],
                     'strict_inequality_if_nonzero_actuation': True}
    sample = np.linspace(0,3*omega_max,2001)
    assert np.all((transfer_window(sample,omega_max)>=0)&(transfer_window(sample,omega_max)<=1))

    low = model.unactuated_matched(.003125,p)[1]
    assert abs(low-.1980373215478359) < 1e-10
    assert abs(a*z_real+b*z_abs*z_abs+axial-active)<1e-10
    assert abs(passive(dmatch)['electric_W']-active)<1e-8
    assert abs(film_controls[0]['electric_W']-active)<1e-7
    result = {'status': 'bounded numerical diagnostics and internally reconstructed gates; no acquired pipe/material response',
              'corrected_low_flow_passive_W': low,
              'preferred_saved_case': {k:v for k,v in preferred.items() if k not in ['local_rows','history']},
              'source_frequency_contract': source_rates,
              'mechanical_frequency_gate': {'scope':'Fixed-end inherited tube dimensions/G/densities/drive arm inertia, real positive frozen cross viscosity, no added external inertia, nonnegative grounded support stiffness. Elastic fluid resonances or added hardware fall outside this bound.',
                     'continuum_lower_bound_first_zero_reactance_hz':lower_hz,
                     'discrete_max_fluid_inertia_eigenfrequency_hz':discrete_rigid_lower_hz,
                     'unloaded_steel_first_mode_hz':math.sqrt(G/p.steel_density)/(2*p.length),
                     'steel_inertia_per_length':is_steel,'rigid_fluid_inertia_per_length':is_fluid_rigid,
                     'arm_and_mover_point_inertia':is_arms,
                     'necessary_extra_midpoint_inertia_to_permit_source_band_kg_m2':necessary_extra_point_inertia,
                     'necessary_length_to_permit_source_band_same_tube_m':necessary_length,
                     'bound_formula':'omega^2 >= GJ / [ (Isteel+Ifluid_rigid)*L^2/pi^2 + Iarm*L/4 ]; independent of guessed Q or positive support stiffness.'},
              'passive_controls_at_same_flow': passive_receipts,
              'passive_matching_active': passive(dmatch),
              'passive_at_250L_inventory_cap': passive250,
              'same_carrier_film_controls': film_controls,
              'impedance_gate': {'Omega_peak_rad_s': Omega, 'saved_model_ReZ': z_real,
                                'saved_model_absZ': z_abs, 'saved_model_absImZ': z_imag_abs,
                                'coil_peak_current_A': ipk, 'conditional_coil_voltage_peak_V': vpk,
                                'coil_inductive_reactance_ohm': preferred['omega']*inductance,
                                'scope':'Sinusoidal prescribed central angular velocity; Z is measured fundamental loaded torque/velocity at actual amplitude. Higher torque harmonics increase copper loss and must be charged in P_extra, or measured RMS currents used directly. The zero-extra ellipse is necessary, not sufficient, without those measurements.',
                                'acceptance_gates': gates},
              'frozen_local_source_compatibility': local,
              'data_nonidentifiability_witness': witness_check,
              'seconds': time.perf_counter()-tic,
              'runtime': {'python':sys.version,'platform':platform.platform()}}
    (HERE/'decisive_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    receipt = {'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'result_sha256': hashlib.sha256((HERE/'decisive_checks.json').read_bytes()).hexdigest(),
               'seconds': result['seconds'], 'assertions': 'passed',
               'no_physical_validation': True}
    (HERE/'COMPUTATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'low_passive_W':low,'passive_matching_active':passive(dmatch),
                      'film_match_m':film_match,'source_max_hz':float(omega_max/(2*math.pi)),
                      'model_Z':z_real,'impedance_gates':gates,'seconds':result['seconds']},indent=2))


if __name__ == '__main__':
    main()
