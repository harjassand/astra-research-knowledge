"""Finite initial energy admission using actual heterodyne accept/abort.

The initial mean bound is used for acceptance/availability and a once-only
startup comparison; the physical acceptance instrument earns an exponential
moment for the accepted reference. It does not infer high moments from a mean.
All numbers below use analytic envelope bounds, with wide margins.
"""
from pathlib import Path
import json, math

HERE=Path(__file__).resolve().parent

def main():
    nb=.1; k0lo=9e-5; k0hi=1.1e-4
    krlo=3.996; krhi=4.004
    deteta=.5; deteta_max=1.; mean0=100.; ures=1e-7
    precool=1.2; observe=.8; ramp=.1; final=.05
    theta=.8; t=math.expm1(theta); c=1.; radius=4.
    adc_step=32/(2**16)
    radial_error=math.sqrt(2)*adc_step/2
    Rplus=radius+radial_error; Rminus=radius-radial_error
    # sin^2 on/off ramps integrate to one total ramp duration.
    Kmin=(krlo*(observe-ramp)+k0lo*observe)
    rmax=math.exp(-Kmin)
    # Central flat part only, discarding the positive contribution of both ramps.
    # The actual complex phase has |Delta t|<=1e-6*T.
    rate_hi=krhi+k0hi; detmax=1e-6
    integral_lower=math.sqrt(krlo)*math.exp(krhi*ramp/4)*(
        math.exp(-rate_hi*ramp/2)-math.exp(-rate_hi*(observe-ramp)/2)
    )/(rate_hi/2)*math.cos(detmax*observe)
    # mu=|<uniform filter,h_old>|^2/(1-r). Denominator<=1 suffices.
    mu_min=integral_lower**2/observe
    eta0=deteta*c/(1+c)
    mismatch_A_min=1/(1+eta0*(1-mu_min)*nb)
    eta_min=eta0*mu_min*mismatch_A_min
    lhs=t*(rmax+nb*eta_min)
    rhs=eta_min*(1-rmax)
    # A<=1, and the thermal Schur determinant>=1-nb*t.
    logK_observed=c*Rplus**2-math.log1p(c)-math.log1p(-nb*t)
    finalization_log_cost=-math.log1p(-nb*(-math.expm1(-k0hi*final))*t)
    logK=logK_observed+finalization_log_cost
    # A state-independent bounded residual drive during startup is compared
    # once with the force-off reference. This generous energy envelope covers
    # actual prefixes, all ramps, both windows and finalization.
    epsilon=1e-5
    stationary=.14
    intrinsic_stationary=(k0hi*nb+ures**2/epsilon)/(k0lo-epsilon)
    flat_stationary=((krhi+k0hi)*nb+ures**2/epsilon)/(krlo+k0lo-epsilon)
    assert stationary>max(intrinsic_stationary,flat_stationary)
    precool_decay=krlo*(precool-ramp)+(k0lo-epsilon)*precool
    mean_pre=stationary+(mean0-stationary)*math.exp(-precool_decay)
    heterodyne_second_moment=1+deteta_max*(mean_pre+nb)
    p_accept_lower=1-heterodyne_second_moment/(Rminus**2)
    logM_cond=logK-math.log(p_accept_lower)
    whole_startup=precool+observe+final
    def force_integral_upper(pretime):
        # Ignore cooling in the first ramp; use the exact flat rate floor.
        # sqrt(stationary+a exp(-kt))<=sqrt(stationary)+sqrt(a) exp(-kt/2).
        kflat=krlo+k0lo-epsilon
        flat=pretime-2*ramp
        opening=ramp*(math.sqrt(mean0)+math.sqrt(mean0+1))
        active=(math.sqrt(stationary)+math.sqrt(stationary+1))*flat
        active+=4*math.sqrt(mean0-stationary)/kflat*(-math.expm1(-kflat*flat/2))
        end_mean=stationary+(mean0-stationary)*math.exp(-kflat*flat)
        remaining=(ramp+observe+final)*(math.sqrt(end_mean)+math.sqrt(end_mean+1))
        return opening+active+remaining
    force_amplitude=ures*force_integral_upper(precool)
    normalized_startup_distance=2*force_amplitude/(p_accept_lower-force_amplitude)
    # Mean-envelope contribution during the final decision slot is harmless
    # for the ideal force-off reference's already earned moment. It is included
    # in the actual force-comparison time above.
    checks={
        'uniform_overlap_positive':0<mu_min<1,
        'uniform_tilted_effect_contracts':lhs<rhs,
        'accepted_reference_meets_main_boundary':logM_cond<20,
        'acceptance_lower_above_point84':p_accept_lower>.84,
        'initial_thermal_moment_condition':nb*t<1,
    }
    assert all(checks.values()),checks
    out={
      'model':{'initial_mean_energy_max':mean0,'thermal_occupation_max':nb,
        'detection_efficiency_range':[deteta,deteta_max],'intrinsic_rate':[k0lo,k0hi],
        'readout_port_rate':[krlo,krhi],'detuning_max':detmax,
        'residual_force_max':ures,'pre_cooling_time':precool,
        'heterodyne_time':observe,'ramp_time':ramp,'finalization_time':final,
        'total_startup_time':whole_startup,
        'receiver':'uniform analog integration of both quadratures; two16-bit ADCs on[-16,16]; integer disk radius4; saturation aborts'},
      'actual_threshold':{'adc_step':adc_step,'radial_rounding_bound':radial_error,
         'outer_radius':Rplus,'inner_radius':Rminus},
      'uniform_bounds':{'retained_transmissivity_max':rmax,
         'old_response_integral_min':integral_lower,'selected_mode_overlap_min':mu_min,
         'effective_noclick_strength_min':eta_min,
         'tilted_effect_left_side':lhs,'tilted_effect_right_side':rhs,
         'accepted_unnormalized_log_moment_before_finalization':logK_observed,
         'finalization_log_moment_cost':finalization_log_cost,
         'accepted_unnormalized_log_moment_max':logK,
         'mean_before_filter_max':mean_pre,
         'heterodyne_second_moment_max':heterodyne_second_moment,
         'acceptance_probability_min_reference':p_accept_lower,
         'accepted_normalized_logM_point8_max':logM_cond,
         'once_only_startup_force_half_trace_bound':force_amplitude,
         'conditioned_startup_force_distance_bound':normalized_startup_distance},
      'checks':checks,
      'scope':['The finite accept/abort CP instrument earns the exponential tail; the initial mean alone does not.',
        'Both-quadrature heterodyne is an explicit added physical receiver capability, available equally to competitors.',
        'The force comparison is paid once before subsequent actual noisy evolution, not reused to infer an actual high moment.',
        'Detector calibration, analog integration, ADC/controller faults, startup switch outages and any extra waiting require their own physical terms.',
        'No physical upper photon-number projector or perfect flag is used.',
        'This is a model certificate, not a measured startup success rate.']}
    # A separate parallel array startup, without multiplying conditional
    # acceptances of potentially correlated initial modes. The complete
    # initial-to-readout channel has intensity <=r0 and thermal noise <=nb.
    # Its loss-then-amplifier decomposition gives fail <=thermal_tail+r0*E.
    arr=[]; precool_array=3.3
    r0=math.exp(-krlo*(precool_array-ramp)-k0lo*precool_array)
    vacuum_thermal_tail=math.exp(-Rminus**2/(1+nb))
    for modules in [40,217]:
        pab=modules*(vacuum_thermal_tail+r0*mean0)
        pgood=1-pab
        old_peak_distance=modules*(precool_array+observe+final)*ures*(math.sqrt(mean0)+math.sqrt(mean0+1))
        init_distance=modules*ures*force_integral_upper(precool_array)
        arr.append({'modules':modules,'parallel_startup_time':precool_array+observe+final,
            'pre_cooling_time':precool_array,'pre_cooling_transmissivity_max':r0,
            'all_accept_probability_lower_reference':pgood,
            'each_accepted_log_moment_max':logK-math.log(pgood),
            'startup_force_integral_bound_per_module':force_integral_upper(precool_array),
            'previous_peak_energy_comparison_diagnostic':old_peak_distance,
            'global_startup_force_half_trace_bound':init_distance,
            'conditional_force_distance_bound':2*init_distance/(pgood-init_distance),
            'counting_note':'An illustrative apparatus count, not a recompiled protected-CNOT resource advantage.'})
        assert pgood>.9 and logK-math.log(pgood)<20
    out['parallel_correlated_array_startup']=arr
    (HERE/'finite_heterodyne_admission_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
