#!/usr/bin/env python3
"""Material/measurement screens; no hardware or acquired material coefficients.

All frequency computations use angular omega = 2*pi*f in SI. Paper THz labels
are preserved as reported when quoting their dimensionless Eq.10 estimate.
"""
import json
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent
KB = 1.380649e-23
HBAR = 1.054571817e-34
E = 1.602176634e-19
EPS0 = 8.8541878128e-12


def eta_from_symmetric_unloaded_ratio(r):
    assert 0 <= r <= 1
    return r*r/(1+math.sqrt(1-r*r))**2


def bose(omega, temperature):
    return 1/math.expm1(HBAR*omega/(KB*temperature))


def mode_moments(modes, temperature=300.0):
    heat, friction = 0.0, 0.0
    for q, f_hz, transmission, measure in modes:
        w = 2*math.pi*f_hz
        nb = bose(w, temperature)
        heat += measure*transmission*(HBAR*w)**2/(KB*temperature**2)*nb*(nb+1)
        friction += measure*transmission*HBAR**2*q*q/(2*KB*temperature)*nb*(nb+1)
    return heat, friction


def check_spectral_identity():
    modes = [(1e8, 0.3e12, .2, 1.0), (7e8, 2e12, .4, .7), (2e9, 20e12, .1, .4)]
    T = 300.0
    heat, friction = mode_moments(modes,T)
    weighted_moment = 0.0
    for q,f,tr,m in modes:
        w=2*math.pi*f
        n=bose(w,T)
        heat_weight = m*tr*(HBAR*w)**2/(KB*T*T)*n*(n+1)
        weighted_moment += heat_weight*(q/w)**2
    expected = T*weighted_moment/2
    assert abs(friction-expected) <= 1e-14*friction
    dt, du = 1e-3, 1e-3
    heat_fd, friction_fd = 0.,0.
    for q,f,tr,m in modes:
        w=2*math.pi*f
        heat_fd += m*tr*HBAR*w*(bose(w,T+dt/2)-bose(w,T-dt/2))/dt
        # Two directions with qx=+/-q/sqrt(2), equal quadrature weights.
        for sign in (-1,1):
            qx=sign*q/math.sqrt(2)
            friction_fd += m*tr/2*HBAR*qx*(bose(w-qx*du/2,T)-bose(w+qx*du/2,T))/du
    herror=abs(heat_fd/heat-1)
    lerror=abs(friction_fd/friction-1)
    assert herror<1e-7 and lerror<1e-7
    one=[(1e6,1e12,.1,1)]
    two=[(1e9,1e12,.1,1)]
    h1,l1=mode_moments(one,T)
    h2,l2=mode_moments(two,T)
    assert h1==h2 and abs(l2/l1-1e6)<1e-8
    return {'identity_relative_error':abs(expected/friction-1),
            'temperature_finite_difference_relative_error':herror,
            'Doppler_finite_difference_relative_error':lerror,
            'equal_heat_different_q_friction_ratio':l2/l1,
            'scope':'same_kernel_equilibrium_isotropic_Landauer_model_only'}


def main():
    rng=random.Random(20261015)
    pressure_gate=[]
    for donor,load in [(1e5,2e4),(1e4,1e3),(100,20)]:
        span=donor+load
        optimum_offset=span/2
        pressure_gate.append({'donor_pressure_drop_Pa':donor,'opposing_receiver_pressure_Pa':load,
            'minimum_possible_maximum_transverse_pressure_Pa':span/2,
            'minimizing_left_endpoint_difference_Pa':optimum_offset})
        for _ in range(100):
            offset=rng.uniform(-3*span,3*span)
            assert max(abs(offset),abs(offset-span))>=span/2*(1-1e-14)
        assert max(abs(optimum_offset),abs(optimum_offset-span))==span/2
    ratio_table=[{'unloaded_ratio_r':r,'maximum_work_efficiency_fraction':eta_from_symmetric_unloaded_ratio(r),
                  'maximum_work_efficiency_percent':100*eta_from_symmetric_unloaded_ratio(r)}
                 for r in (.01,.1,.3,.4,.9)]
    carbon_scaling=[]
    for d in (2,5,10,20):
        for prefactor in (1.0,.5):
            r=prefactor*math.exp(-1-d/4)
            carbon_scaling.append({'wall_thickness_nm':d,'assumed_gamma_tau':1,
                'paper_discussion_ell_nm':4,'assumed_prefactor':prefactor,
                'predicted_unloaded_r':r,'conditional_eta_max_percent':100*eta_from_symmetric_unloaded_ratio(r),
                'scope':'paper_asymptotic_scaling_ansatz_not_real_material_bound'})

    # Long-wave, finite-temperature monolayer Drude diagnostic. Not a nonlocal
    # band-structure bound and not an acquired wall dielectric constant.
    T=300.; f_target=.3e12; omega=2*math.pi*f_target; vf=1e6; qsim=2.5e9
    e_thermal=2*KB*T*math.log(2)
    D=E*E*e_thermal/(math.pi*HBAR*HBAR)
    graphene=[]
    for er in (2.,5.,10.,80.):
        q_res=2*EPS0*er*omega**2/D
        formal_f=math.sqrt(D*qsim/(2*EPS0*er))/(2*math.pi)
        required_E=2*EPS0*er*math.pi*HBAR**2*omega**2/(E*E*qsim)
        graphene.append({'diagnostic_permittivity_not_material_assignment':er,
            'T_K':T,'target_f_THz':f_target/1e12,'thermal_Drude_energy_meV':e_thermal/E*1e3,
            'resonant_q_m_inverse_local_model':q_res,
            'resonant_q_nm_inverse_local_model':q_res/1e9,
            'locality_parameter_q_vF_over_omega_at_resonance':q_res*vf/omega,
            'simulator_q_nm_inverse':qsim/1e9,
            'locality_parameter_at_simulator_q':qsim*vf/omega,
            'formal_local_f_at_simulator_q_THz_not_a_valid_high_q_prediction':formal_f/1e12,
            'Drude_energy_required_at_simulator_q_meV':required_E/E*1e3,
            'scope':'reject_arbitrary_low_frequency_high_q_Drude_substitution_not_graphite_or_MXene_flow_tunnelling'})

    # Compliance calibration example only. Not a proposed fabricated membrane.
    radius=0.5e-6; tension=.1; pressure=1e5
    compliance=math.pi*radius**4/(8*tension)
    compliance_example={'scope':'illustrative_small_slope_tension_membrane_calibration_only',
        'radius_m':radius,'tension_N_m':tension,'normal_pressure_Pa':pressure,
        'volume_compliance_m3_Pa':compliance,
        'pressure_step_volume_fL':compliance*pressure/1e-18,
        'central_deflection_nm':pressure*radius**2/(4*tension)*1e9,
        'stored_elastic_energy_J':.5*compliance*pressure**2,
        'pressure_times_total_displaced_volume_J':compliance*pressure**2,
        'small_slope_parameter_w0_over_radius':pressure*radius/(4*tension)}
    assert math.isclose(compliance*pressure/(math.pi*radius**2),pressure*radius**2/(8*tension),rel_tol=1e-14)
    glycerol={'scope':'identity_only_not_fitted_glycerol_advantage',
        'slit_Q_per_width':'h^3 DeltaP/(12 L)*(1/eta+6/(h lambda))',
        'point':'100fold_slip_length_does_not_imply_100fold_permeance_when_viscosity_changes'}

    results={'status':'source_derived_unreviewed_conditional_internal_material_audit',
        'hardware_validation':False,'historical_originality':'UNKNOWN',
        'no_favorable_measured_material_parameters_assigned':True,
        'symmetric_channel_unloaded_ratio_to_work':ratio_table,
        'loaded_parallel_channel_normal_pressure_gate':pressure_gate,
        'published_carbon_scaling_loaded_screen':carbon_scaling,
        'graphene_finite_T_locality_diagnostic':graphene,
        'compliance_energy_calibration_example':compliance_example,
        'glycerol_pivot_screen':glycerol,
        'spectral_identity_checks':check_spectral_identity()}
    (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'toy_r_0_1_eta_max_percent':ratio_table[1]['maximum_work_efficiency_percent'],
        '10nm_carbon_ansatz_upper_prefactor_eta_percent':[x for x in carbon_scaling if x['wall_thickness_nm']==10 and x['assumed_prefactor']==1][0]['conditional_eta_max_percent'],
        'spectral_checks':results['spectral_identity_checks'],
        '300K_thermal_Drude_energy_meV':e_thermal/E*1e3,
        'locality_parameter_at_q_2_5nm_f_0_3THz':qsim*vf/omega},indent=2))


if __name__=='__main__':main()
