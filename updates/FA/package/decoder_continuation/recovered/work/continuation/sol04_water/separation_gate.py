#!/usr/bin/env python3
"""Bounded material route plus a single gas-free electrophoresis pivot.

All device coefficients are labelled supplied or source-reported in output.
No physical measurement is made. Run from this directory with numpy/scipy.
Outputs only beside this script. No inherited file is modified.
"""
from __future__ import annotations

import hashlib
import json
import math
import pathlib
import platform
import time

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.sparse import diags

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = pathlib.Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')
F = 96485.33212
Rgas = 8.314462618
TEMP = 298.15
DP = 5.4e-12
MU = 3.0e-8  # SUPPLIED electrophoretic mobility, NOT measured for 80nm PS here.
WIDTH = 50e-6
LENGTH = .055
REC = .95
LEAK = 1e-4
KS = 3.3464052287581706e-4
KG = 1.025e-6


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def water_fraction(y):
    return 3*y*y - 2*y*y*y


def bernoulli(x):
    x = np.asarray(x)
    return np.where(np.abs(x) < 1e-5, 1-x/2+x*x/12-x**4/720,
                    x / np.expm1(x))


def stationary_ratio(pe, cut):
    # Normalise n to conserved axial particle flux, not transverse number.
    fun = lambda y: 6*y*(1-y)*math.exp(pe*(y-1))
    total = quad(fun, 0, 1, epsabs=1e-17, epsrel=1e-12)[0]
    product = quad(fun, 0, cut, epsabs=1e-21, epsrel=1e-12)[0]
    return product / total / REC


def electric_case(pe, cells):
    y = (np.arange(cells)+.5)/cells
    u = 6*y*(1-y)
    u /= u.mean()
    # State p_i is axial particle-flux fraction in each finite-volume cell.
    # Dimensionless time tau = Dp*t/W^2. No-flux particle boundaries.
    forward = cells*cells*float(bernoulli(np.array(-pe/cells)))
    backward = cells*cells*float(bernoulli(np.array(pe/cells)))
    aa = np.full(cells-1, forward)
    bb = np.full(cells-1, backward)
    A = diags([aa, -np.r_[aa,0]-np.r_[0,bb], bb], [-1,0,1], format='csc')
    B = A @ diags(1/u, 0, format='csc')
    p0 = u / u.sum()
    water = np.r_[0, np.cumsum(p0)]
    edges = np.linspace(0,1,cells+1)
    # Use exact same numerical water cut for target and transport.
    cut = float(np.interp(REC, water, edges))
    cell_count = cut*cells
    nwhole = int(cell_count)
    frac = cell_count - nwhole
    weights = np.zeros(cells)
    weights[:nwhole] = 1
    if nwhole < cells:
        weights[nwhole] = frac
    def event(t,p):
        return float(weights @ p - REC*LEAK)
    event.terminal = True
    event.direction = -1
    out = solve_ivp(lambda t,p:B@p, (0,2.0), p0, method='BDF', jac=B,
                    events=event, rtol=2e-9, atol=2e-14)
    assert out.success
    assert np.max(np.abs(out.y.sum(axis=0)-1)) < 2e-7
    assert out.y.min() > -1e-10
    p_eq = u*np.exp(pe*(y-1)); p_eq /= p_eq.sum()
    eq_residual = float(np.max(np.abs(B @ p_eq)))
    eq_scale = float(np.max(abs(B) @ p_eq))
    eq_relative = eq_residual/eq_scale
    assert eq_relative < 2e-12
    row = dict(Pe=pe,cells=cells,target_met=len(out.t_events[0])>0,
               max_particle_mass_residual=float(np.max(np.abs(out.y.sum(axis=0)-1))),
               minimum_particle_flux_cell=float(out.y.min()),
               stationary_generator_residual=eq_residual,
               stationary_generator_relative_residual=eq_relative,
               numerical_water_cut=cut)
    if not row['target_met']:
        return row
    tau=float(out.t_events[0][0]); p=out.y_events[0][0]
    t = tau*WIDTH*WIDTH/DP
    field=pe*DP/(MU*WIDTH)
    electrode_charge_per_sigma = field*t/(WIDTH*REC)
    joule_per_sigma = field*field*t/REC
    dp=12*.001*LENGTH*LENGTH/(t*WIDTH*WIDTH)
    row.update(tau=tau,mean_residence_s=t,field_V_m=field,
               liquid_voltage_V=field*WIDTH,
               exposure_mu_E_t_over_W=pe*tau,
               product_particle_concentration_over_feed=float(weights @ p/REC),
               product_L_m2_onewall_h=REC*WIDTH/t*3.6e6,
               product_L_m2_twoplate_h=REC*WIDTH/t*1.8e6,
               electrode_charge_C_m3_product_per_S_m=electrode_charge_per_sigma,
               Joule_J_m3_product_per_S_m=joule_per_sigma,
               liquid_pressure_drop_Pa=dp,
               liquid_pumping_kWh_m3_at_70pct=dp/(.7*REC*3.6e6))
    return row


def main():
    start=time.perf_counter()
    pin_names=[
        'outputs/ASTRA_GENESIS_HANDOFF.txt', 'outputs/STRONGEST_VERIFIED_RESULT.txt',
        'work/phase5/water_separation/HANDOFF.txt',
        'work/phase5/water_separation/interface_assay_best50_results.json',
        'work/phase5/water_separation/inputs.json',
        'work/phase5/water_separation/diffusiophoresis_bounds.xml',
        'work/phase5/water_separation/unbuffered_CO2_1977.xml',
        'work/phase5/capital_synthesis/HANDOFF.txt',
        'work/phase5/capital_synthesis/WATER_SKIN_RESULT.txt',
    ]
    pins=[dict(path=str(SOURCE/p),sha256=sha(SOURCE/p)) for p in pin_names]
    assay=json.loads((SOURCE/'work/phase5/water_separation/interface_assay_best50_results.json').read_text())
    # GPU from the primary definition, 1cm^3STP =1e-6 m^3 and 1cmHg=1333.22Pa.
    gpu=1e-6*1e-6/1e-4/1333.22/.022414
    site_mol=8.0e15/6.02214076e23
    source_wall=assay['walls'][0]
    henry=29.5/115125
    material=dict(
        scope='Fu2018 primary humid gas membrane, not an acquired water-contact wall',
        measured_best_GPU=2600,
        measured_best_permeance_mol_m2_s_Pa=2600*gpu,
        measured_best_over_required_permeance=2600*gpu/KG,
        enzyme_sites_per_m2=8e15,
        site_loading_mol_m2=site_mol,
        required_specificity_M_inv_s_inv=1000*KS/site_mol,
        source_gross_forward_per_site_s=KS*source_wall['C_CO2_mol_m3']/site_mol,
        source_net_per_site_s=source_wall['pair_flux_into_water_mol_m2_s']/site_mol,
        two_faces_ten_ions_per_site_full_release_uM=2*site_mol*10/WIDTH*1000,
        max_release_fraction_for_added_0p1uM=1e-4/(2*site_mol*10/WIDTH),
        adsorption_barrier_sensitivity=[],
        protective_CO2_layer_cases=[],
    )
    kads=assay['slit_adsorption_refinement'][-1]['equal_two_wall_kads_max_for_1pct_irreversible_loss_m_s']
    for access_distance in (10e-9,40e-9,1e-6):
        collision_velocity=DP/access_distance
        material['adsorption_barrier_sensitivity'].append(dict(
            scope='phenomenological kads=(Dp/access_distance)*exp(-barrier/kBT), not a measured potential',
            supplied_access_distance_m=access_distance,
            collision_velocity_m_s=collision_velocity,
            inherited_kads_ceiling_m_s=kads,
            required_barrier_over_kBT=math.log(collision_velocity/kads)))
    for delta in (10e-9,50e-9,100e-9,500e-9,1e-6):
        cap=2e-9*henry/delta
        series=1/(1/(2600*gpu)+1/cap)
        material['protective_CO2_layer_cases'].append(dict(
            assumed_layer_m=delta,assumed_D_CO2_m2_s=2e-9,
            assumed_unit_partition=True,coating_permeance_mol_m2_s_Pa=cap,
            total_permeance_mol_m2_s_Pa=series,
            total_over_required=series/KG))

    cut=brentq(lambda y:water_fraction(y)-REC,0,1)
    pe_min=brentq(lambda pe:stationary_ratio(pe,cut)-LEAK,1,300)
    rows=[electric_case(pe,400) for pe in (96.,128.,192.,256.)]
    rows.extend(electric_case(pe,800) for pe in (512.,1024.))
    # Refinement is fixed in advance; not adaptive selection of a favorable row.
    refinements=[electric_case(128.,n) for n in (200,800)]
    selected_refinements=[electric_case(256.,n) for n in (800,1600)]
    refinement512=[next(r for r in rows if r['Pe']==512)]
    refinement512.extend(electric_case(512.,n) for n in (1600,3200))
    rows=[refinement512[-1] if r['Pe']==512 else r for r in rows]
    best=min((r for r in rows if r['target_met']),
             key=lambda r:r['electrode_charge_C_m3_product_per_S_m'])
    # Conductivity scenarios use Nernst-Einstein; source/sink compositions are
    # inherited model predictions, not measured FFE feed conductivities.
    lam_H=F*F*9.3e-9/(Rgas*TEMP)
    lam_B=F*F*1.18e-9/(Rgas*TEMP)
    scenarios=[('ultrapure limiting-conductivity fixture',5.5e-6),
               ('air-equilibrated-water fixture',1.0e-4),
               ('inherited source-wall local composition',
                lam_H*source_wall['H_mol_m3']+lam_B*source_wall['HCO3_mol_m3'])]
    budgets=[]
    for label,sigma in scenarios:
        charge=best['electrode_charge_C_m3_product_per_S_m']*sigma
        joule=best['Joule_J_m3_product_per_S_m']*sigma
        faradaic=1.23*charge
        budgets.append(dict(label=label,conductivity_S_m_SUPPLIED=sigma,
            charge_C_m3_product=charge,
            electrode_reaction_equivalents_uM=charge/F*1000,
            Joule_kWh_m3=joule/3.6e6,
            water_electrolysis_1p23V_kWh_m3=faradaic/3.6e6,
            Joule_plus_electrolysis_plus_liquid_pump_kWh_m3=
                (faradaic+joule)/3.6e6+best['liquid_pumping_kWh_m3_at_70pct'],
            deterministic_lower_charge_C_m3=sigma*(1-LEAK)/MU,
            deterministic_lower_electrolysis_kWh_m3=1.23*sigma*(1-LEAK)/MU/3.6e6,
            electrode_budget_excludes='overpotential, membranes, reservoir pumping, reset, electrode/ion renewal'))
    uf_pressure=4000
    uf_hydraulic=uf_pressure/(.7*REC*3.6e6)
    # Exact width scaling within this supplied parabolic model lets us compare
    # at the external GDM area productivity, rather than advertise unequal area.
    matched_area=[]
    for area_flux in (4.,10.):
        for label,sigma in scenarios:
            candidates=[]
            for row in rows:
                width=WIDTH*row['product_L_m2_twoplate_h']/area_flux
                pump=row['liquid_pumping_kWh_m3_at_70pct']*(WIDTH/width)**4
                charge=row['electrode_charge_C_m3_product_per_S_m']*sigma
                joule=row['Joule_J_m3_product_per_S_m']*sigma
                candidates.append(dict(Pe=row['Pe'],cells=row['cells'],width_m=width,
                    residence_s=row['mean_residence_s']*(width/WIDTH)**2,
                    liquid_pump_kWh_m3=pump,charge_C_m3_product=charge,
                    electrode_reaction_equivalents_uM=charge/F*1000,
                    water_electrolysis_plus_Joule_plus_liquid_pump_kWh_m3=
                        (1.23*charge+joule)/3.6e6+pump))
            picked=min(candidates,key=lambda a:a['water_electrolysis_plus_Joule_plus_liquid_pump_kWh_m3'])
            picked['maximum_unrecovered_electrode_pair_voltage_to_match_UF_V']=(
                (uf_hydraulic-picked['liquid_pump_kWh_m3'])*3.6e6/
                picked['charge_C_m3_product']-picked['Pe']*DP/MU)
            matched_area.append(dict(total_two_plate_productivity_L_m2_h=area_flux,
                                     conductivity_label=label,conductivity_S_m=sigma,
                                     best_sampled=picked,all_sampled=candidates))
    # Linear double-layer screening diagnostic for smooth blocking electrodes.
    # It is explicitly local/linear; porous capacitive deionisation can violate
    # these geometric capacitance assumptions but needs its own ion balance.
    cw=source_wall['H_mol_m3']; bw=source_wall['HCO3_mol_m3']
    sigma_source=scenarios[-1][1]
    ionic_strength=(cw+bw)/2
    eps_water=6.95e-10
    debye=math.sqrt(eps_water*Rgas*TEMP/(2*F*F*ionic_strength))
    cseries=eps_water/(2*debye)
    rc=WIDTH/sigma_source*cseries
    diagnostic=next(r for r in rows if r['Pe']==128)
    blocking=dict(scope='linear small-voltage smooth blocking-plate diagnostic, supplied source-wall solution',
        Debye_length_m=debye,series_double_layer_F_m2=cseries,
        RC_screening_time_s=rc,
        voltage_V=diagnostic['liquid_voltage_V'],
        integrated_initial_field_displacement_m=MU*diagnostic['field_V_m']*rc,
        native_cation_inventory_uM=cw*1000,
        target_95pct_4log_electrode_equivalents_uM=
            diagnostic['electrode_charge_C_m3_product_per_S_m']*sigma_source/F*1000,
        full_cation_capture_capacity_C_m3_feed=F*cw,
        caveat='large porous electrode, Faradaic water dissociation, or reservoir injection changes this interface')
    result=dict(status='CONDITIONAL FLOAT MODEL + RECONSTRUCTED ZERO-DIFFUSION CHARGE BOUND; NO NEW DEVICE',
        source_pins=pins,script_sha256=sha(pathlib.Path(__file__)),
        supplied_contract=dict(Dp_m2_s=DP,mobility_m2_V_s=MU,width_m=WIDTH,length_m=LENGTH,
            recovery=REC,product_feed_particle_ratio=LEAK,
            boundaries='no particle flux, no adsorption, constant uniform electric field',
            chemistry='fixed homogeneous conductivity; no electroosmosis; no concentration polarization'),
        material=material,exact_stationary_water_cut=cut,
        minimum_stationary_Pe_float=pe_min,
        deterministic_bound_exposure=REC*(1-LEAK),
        electric_sweep=rows,refinements_Pe128=refinements,
        refinements_Pe256=selected_refinements,
        refinements_Pe512=refinement512,
        smallest_charge_sampled_case=best,electrode_budgets=budgets,
        matched_total_area_productivity=matched_area,smooth_blocking_electrode_diagnostic=blocking,
        primary_feed_loading_diagnostic=dict(
            source_reported_feed_volume_fraction=1.5e-4,
            inherited_wall_outlet_enrichment=assay['slit_adsorption_refinement'][-1]['outlet_wall_concentration_over_feed'][1],
            implied_point_particle_wall_volume_fraction=1.5e-4*assay['slit_adsorption_refinement'][-1]['outlet_wall_concentration_over_feed'][1],
            sphere_close_packing_fraction=math.pi/(3*math.sqrt(2)),
            feed_volume_fraction_for_wall_fraction_below_0p01=
                .01/assay['slit_adsorption_refinement'][-1]['outlet_wall_concentration_over_feed'][1],
            warning='mathematical wall is inaccessible to 40nm-radius centers; not a universal packing no-go; finite-size/crowding transport must replace point tail'),
        gravity_UF_control=dict(pressure_Pa=uf_pressure,recovery=REC,pump_efficiency=.7,
            hydraulic_kWh_m3=uf_hydraulic,
            reported_GDM_flux_range_L_m2_h=[4,10],
            same_80nm_4log_95pct_recovery_validation='NOT ACQUIRED; report does not claim proof of this comparator performance',
            same_input_ideal_sieve_fixture=dict(
                pore_diameter_m=15e-9,porosity=.1,active_thickness_m=1e-6,
                water_viscosity_Pa_s=.001,rigid_particle_diameter_m=80e-9,
                permeability_m_Pa_s=.1*(7.5e-9)**2/(8*.001*1e-6),
                ideal_flux_L_m2_h=.1*(7.5e-9)**2/(8*.001*1e-6)*4000*3.6e6,
                status='supplied defect-free parallel-cylinder model; not a measured module; steric rejection exact for supplied rigid spheres'),
            conditional_UF_dominates_50um_FFE_plant_energy_when_conductivity_exceeds_S_m=
              max(0,uf_hydraulic-best['liquid_pumping_kWh_m3_at_70pct'])*3.6e6/
              (1.23*best['electrode_charge_C_m3_product_per_S_m']+best['Joule_J_m3_product_per_S_m'])),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                     elapsed_s=time.perf_counter()-start))
    out=HERE/'GATE_RESULTS.json';out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'file':str(out),'stationary_Pe':pe_min,
        'selected_Pe':best['Pe'],'selected_residence_s':best['mean_residence_s'],
        'selected_product_L_m2_twoplate_h':best['product_L_m2_twoplate_h'],
        'source_composition_case':budgets[-1],
        'uf_hydraulic':uf_hydraulic,'elapsed_s':result['runtime']['elapsed_s']},indent=2))


if __name__=='__main__':
    main()
