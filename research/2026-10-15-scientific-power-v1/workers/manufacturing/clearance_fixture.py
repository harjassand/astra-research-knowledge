#!/usr/bin/env python3
"""Bounded model calculations for temporary blind-channel clearance.

No laboratory parameters were acquired by this script. The results are model
arithmetic, not a performance simulation or a proof of manufacturing feasibility.
Only the Python standard library is required.
"""
import json
import math
from pathlib import Path


def rectangular_resistance(mu, length, width, height):
    """Fully developed Newtonian no-slip rectangular duct, odd series to 999.

    Omits entrances, turns, two-phase flow, gel rheology, deformation, slip and
    leaks. The small positive omitted series tail makes this a numerical
    approximation, not a certified interval enclosure.
    """
    a, b = sorted((width, height))
    series = sum(math.tanh(n * math.pi * b / (2 * a)) / n**5
                 for n in range(1, 1000, 2))
    correction = 1 - 192 * a * series / (math.pi**5 * b)
    return 12 * mu * length / (b * a**3 * correction)


def diffusion_mass_fraction(tau):
    """Mean residual: c_t=c_xx, c(0,t)=0, c_x(1,t)=0, c(x,0)=1.

    tau = D*t/L^2. The sum is sufficient near the 1% crossing. It is not a
    universal cleanup lower bound; convection, dissolution, phoresis and bubbles
    are absent.
    """
    return 8 / math.pi**2 * sum(
        math.exp(-(2 * n + 1)**2 * math.pi**2 * tau / 4)
        / (2 * n + 1)**2 for n in range(1000))


def diffusion_time_fraction(target):
    lo, hi = 0.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if diffusion_mass_fraction(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def two_face_dose(x, t, length, speed, concentration):
    return concentration * (max(t - x / speed, 0)
                            + max(t - (2 * length - x) / speed, 0))


def run():
    L, w, h, delta = 0.080, 500e-6, 500e-6, 25e-6
    lane_w = (w - delta) / 2
    cavity_volume = L * w * h
    wall_volume = L * delta * h
    loop_volume = cavity_volume - wall_volume
    pressure = 1000.0
    hydraulic = []
    for mu in [0.001, 0.01, 0.1, 1.0]:
        resistance = 2 * rectangular_resistance(mu, L, lane_w, h)
        flow = pressure / resistance
        hydraulic.append({
            'assumed_mu_Pa_s': mu,
            'resistance_Pa_s_per_m3': resistance,
            'flow_uL_per_s': flow * 1e9,
            'one_loop_volume_clock_s': loop_volume / flow,
            'ten_loop_volume_clock_s': 10 * loop_volume / flow,
            'ten_volume_ideal_pressure_work_J': 10 * pressure * loop_volume,
            'status': 'illustrative duct arithmetic; not measured clearance time'
        })
    # A fixed-fixed beam strip normal to the flow gives the small-deflection
    # alarm y_max = DeltaP*h^4/(32*E*delta^3). It is not a tested wall model.
    wall_alarms = []
    for E in [4500.0, 8100.0, 1e6, 69e9]:
        allowed_deflection = 50e-6
        pressure_at_deflection = (32 * E * delta**3
                                  * allowed_deflection / h**4)
        wall_alarms.append({
            'assumed_E_Pa': E,
            'pressure_at_50um_deflection_Pa': pressure_at_deflection,
            'status': 'ideal beam-strip screen; strength and adhesion absent'
        })
    tau_1pct = diffusion_time_fraction(0.01)
    diffusion = [{'assumed_D_m2_per_s': D,
                  'one_percent_time_days': tau_1pct * L**2 / D / 86400}
                 for D in [1e-9, 1e-10, 1e-11]]
    leakage = []
    for kL in [0, 0.1, 1, 2, 5, 10]:
        leakage.append({
            'kappa_times_L': kL,
            'distal_flow_over_intact_flow_fixed_pressure':
                1.0 if kL == 0 else kL / math.sinh(kL),
            'distal_flow_over_root_flow':
                1.0 if kL == 0 else 1 / math.cosh(kL)
        })
    # Independent reconstruction of root's ideal two-face dose observation.
    # Normalized c0=1, speed=1, L=1 gives full front transit T=2.
    dose_rows = []
    for t in [0.5, 1.0, 1.5, 2.0, 3.0]:
        values = [two_face_dose(i / 100, t, 1, 1, 1)
                  for i in range(101)]
        dose_rows.append({'time_L_over_u_units': t,
                          'minimum_dose_c0L_over_u_units': min(values),
                          'maximum_dose_c0L_over_u_units': max(values)})
    values_at_3 = [two_face_dose(i / 100, 3, 1, 1, 1)
                   for i in range(101)]
    assert max(abs(v - 4) for v in values_at_3) < 1e-12
    # Stoichiometry only: 2Al + 2OH- + 6H2O -> 2Al(OH)4- + 3H2.
    rho_Al, molar_Al = 2700.0, 0.0269815385
    mass_Al = rho_Al * wall_volume
    mol_Al = mass_Al / molar_Al
    R, T, p = 8.314462618, 298.15, 101325.0
    hydrogen_volume = 1.5 * mol_Al * R * T / p
    chemistry = {
        'status': 'stoichiometric maximum at complete reaction; not delivered gas',
        'Al_mass_mg': mass_Al * 1e6,
        'Al_moles': mol_Al,
        'minimum_OH_moles': mol_Al,
        'minimum_NaOH_mass_mg': mol_Al * 0.039997 * 1e6,
        'H2_moles': 1.5 * mol_Al,
        'ideal_H2_volume_mL_at_25C_1atm': hydrogen_volume * 1e6,
        'ideal_H2_cavity_volume_ratio': hydrogen_volume / cavity_volume,
        'minimum_1M_NaOH_volume_uL': mol_Al / 1000 * 1e9,
        'minimum_0p1M_NaOH_volume_uL': mol_Al / 100 * 1e9,
        'sealed_cavity_ideal_H2_pressure_at_25C_Pa':
            1.5 * mol_Al * R * T / cavity_volume,
        'reaction_heat_J': 'UNKNOWN: no calorimetry or thermochemical model acquired',
        'delivered_bubble_efficiency': 'UNKNOWN',
        'residual_aluminate_and_metal': 'UNKNOWN'
    }
    # Root/topology's localized-wall mutation. This uses an existing full-width
    # return path: a loop attached to the main line at a finite root chamber.
    loop_length, loop_side = 0.080, 1e-3
    root_side, root_height, root_wall_thickness = 3e-3, 1e-3, 0.5e-3
    e = root_wall_thickness / math.sqrt(2)
    root_wall_volume = (2 * root_side * e - e**2) * root_height
    local_loop_R = rectangular_resistance(0.001, loop_length,
                                         loop_side, loop_side)
    root_bypass_R = rectangular_resistance(0.001, root_side,
                                           root_side, root_height)
    loop_lobe = {
        'status': 'geometry and ideal hydraulic bookkeeping, not a fabricated part',
        'loop_length_mm': loop_length * 1000,
        'loop_section_mm': [1.0, 1.0],
        'loop_volume_uL': loop_length * loop_side**2 * 1e9,
        'root_chamber_mm': [3.0, 3.0, 1.0],
        'wall_normal_thickness_mm': root_wall_thickness * 1000,
        'wall_geometry': 'full-height diagonal strip |y-x|<=delta/sqrt(2), '
                         'inside square [-1.5,1.5]^2 mm',
        'wall_volume_uL': root_wall_volume * 1e9,
        'assumed_2pct_alginate_dry_mass_mg': root_wall_volume * 20 * 1e6,
        'Ca_max_moles_if_one_Ca_per_two_198g_mol_residues':
            root_wall_volume * 20 / 0.198 / 2,
        'minimum_100mM_EDTA_uL_ignoring_free_Ca':
            root_wall_volume * 20 / 0.198 / 2 / 100 * 1e9,
        'ideal_loop_R_water_Pa_s_per_m3': local_loop_R,
        'one_loop_PV_clock_at_1000Pa_water_s':
            loop_length * loop_side**2 / (1000 / local_loop_R),
        'one_loop_PV_clock_at_1000Pa_0p01Pa_s_s':
            10 * loop_length * loop_side**2 / (1000 / local_loop_R),
        'root_pressure_countermodel': {
            'status': 'mouths at different axial coordinates approximated by '
                      'parallel root and loop ducts, not a 3D flow solution',
            'R_loop_over_R_root': local_loop_R / root_bypass_R,
            'unpartitioned_loop_flow_fraction_at_fixed_total_Q':
                root_bypass_R / (root_bypass_R + local_loop_R),
            'conclusion': 'finite root pressure difference defeats absolute '
                          'no-flow inference from a point-vertex graph'
        }
    }
    # Coupled necessary screening constraints for a *long* Al separator:
    # deformation limit, one-preload OH capacity and ideal gas budget. These
    # bounds do not include cracking, oxide films, contact adhesion or kinetics.
    E_Al, max_y, C_OH = 69e9, 50e-6, 1000.0
    minimum_d = (pressure * h**4 / (32 * E_Al * max_y))**(1/3)
    maximum_d = C_OH * molar_Al * w / (rho_Al + C_OH * molar_Al)
    gas_minimum_d = 2 * molar_Al * w * p / (3 * rho_Al * R * T)
    foil_screen = {
        'status': 'nonempty necessary-constraint window is NOT feasibility',
        'assumed_pressure_Pa': pressure, 'assumed_OH_mol_per_m3': C_OH,
        'beam_limit_min_thickness_um': minimum_d * 1e6,
        'one_preload_OH_capacity_max_thickness_um': maximum_d * 1e6,
        'one_ideal_gas_PV_min_thickness_um': gas_minimum_d * 1e6,
        'kinetics_and_product_cleanup': 'UNKNOWN'
    }
    # Opposite-lane solid support volume need not all be mobile. A ten-PV rinse
    # convention is retained only as a volume/time planning quantity.
    return {
        'status': 'MODEL_ARITHMETIC_ONLY',
        'fixture': {'blind_length_mm': L * 1000, 'width_um': w * 1e6,
                    'height_um': h * 1e6, 'septum_thickness_um': delta * 1e6,
                    'single_lane_width_um': lane_w * 1e6,
                    'final_cavity_volume_uL': cavity_volume * 1e9,
                    'septum_volume_uL': wall_volume * 1e9,
                    'temporary_loop_volume_uL': loop_volume * 1e9,
                    'pressure_drop_Pa': pressure,
                    'endpoint': 'blind geometry + residual and use test, unperformed'},
        'hydraulic': hydraulic,
        'wall_deflection_alarms': wall_alarms,
        'blind_diffusion_dimensionless_1pct_time': tau_1pct,
        'blind_diffusion': diffusion,
        'leakage_starvation': leakage,
        'ideal_nonconsuming_two_face_dose': dose_rows,
        'erasure_countermodel': {
            'assumptions': 'wall instantly solubilizes everywhere; circuit then blind; '
                           'no mass removal during conversion; no subsequent advection',
            'secondary_mass_residual_fraction_immediately_after_conversion': 1.0,
            'conclusion': 'global activation and disappearance do not establish removal'},
        'Al_foil_mutation': chemistry,
        'Al_necessary_constraint_screen': foil_screen,
        'localized_loop_lobe_mutation': loop_lobe,
        'unacquired': ['core/host manufacturing yield', 'septum seal and strength',
                       'actual cold-core viscosity', 'dissolution kinetics and thermal load',
                       'pressure/bubble history', 'complete wall/product removal',
                       'drying below40C', 'functional endpoint', 'matched baseline win',
                       'novelty', 'apparatus energy', 'inference energy']
    }


if __name__ == '__main__':
    result = run()
    output = Path(__file__).with_name('CLEARANCE_FIXTURE.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
