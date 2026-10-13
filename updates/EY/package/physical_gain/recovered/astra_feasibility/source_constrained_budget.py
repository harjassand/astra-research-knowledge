#!/usr/bin/env python3
"""Source-linked two-component sensitivity model, not a qualified device.

A biexponential pump-probe decay does NOT uniquely imply static populations.
This calculation explicitly tests that interpretation; it does not infer a
unique generator or transfer measured hexane kinetics into hexadecane as fact.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.constants import Boltzmann as KB, elementary_charge as E, Avogadro as NA
from scipy.constants import epsilon_0 as EPS0, Planck as H, speed_of_light as C
from feasibility import mlj_log_rate_and_slope, rotating_chi, reaction_current_noise

T=298.15

def main() -> None:
    folder=Path(__file__).resolve().parent/'results'
    coupling=json.loads((folder/'coupling_results.json').read_text())
    mu=coupling['nominal']['terminal_dipole_e_nm']*E*1e-9
    gap=1.51
    aev=mlj_log_rate_and_slope(gap)[1]
    a=aev/E
    rates=np.array([.996e9,.219e9])
    weights=np.array([.44,.56])
    target=.01
    pump=brentq(lambda r:float(weights@(r/(r+rates)))-target,1.,1e10,xtol=1e-7)
    p=pump/(pump+rates)
    eta=3.0594e-3  # NBS 1958 Table1, 25C measured sample, not RF dielectric data.
    radius=2.05e-9
    tau=4*np.pi*eta*radius**3/(KB*T)
    rho=NA
    area,d=1e-8,1e-6
    epsh=coupling['nominal']['eps_host']; epsc=coupling['nominal']['eps_core']
    phi=rho*4*np.pi*radius**3/3
    epsr=epsh*(epsc+2*epsh+2*phi*(epsc-epsh))/(epsc+2*epsh-phi*(epsc-epsh))
    cap=EPS0*epsr*area/d
    def y(f: np.ndarray, rot_s: float) -> np.ndarray:
        s=2j*np.pi*f
        return sum(s*(area/d)*rotating_chi(s,rho*w,mu,float(pi),float(k),a,rot_s)
                   for w,pi,k in zip(weights,p,rates))
    freq=np.geomspace(1e5,5e8,1200)
    immobile=y(freq,0.)
    viscous=y(freq,1/tau)
    at90=y(np.array([90e6]),1/tau)[0]
    idx=int(np.argmin(viscous.real))
    passive_b=2*np.pi*90e6*cap
    gain90=-float(at90.real)
    pump_min=float(rho*area*d*np.dot(weights,p*rates)*H*C/600e-9)
    psd90=sum(reaction_current_noise(2*np.pi*90e6,rho*area*d*w,mu**2/(3*d*d),float(pi),float(k))
              for w,pi,k in zip(weights,p,rates))
    # PSD here is the immobile independent-population noise only; rotation adds noise.
    data={
       'status':'Conditional source-linked sensitivity, not measured gain or host-transfer validation',
       'interpretation':'Static two-subpopulation mixture is one possible interpretation, NOT uniquely inferred from biexponential data',
       'source_facts':{'decay_rates_s':rates.tolist(),'amplitude_weights':weights.tolist(),
                       'gap_ev':gap,'hexadecane_viscosity_25C_Pa_s':eta},
       'remaining_assumptions':['equal pump rates and equal field derivatives in two subpopulations',
          'same kinetics and MLJ parameters in proposed viscous host as source hexane sample: UNVERIFIED',
          'continuum effective dipole from coupling_model.py, not measured atomistic charge distribution',
          'no ground-state dipole; isotropic field-independent effective pump',
          'rigid hydrodynamic sphere; actual dipole orientation lifetime not acquired',
          '1 mM density, 1 percent total occupation, ideal uniform-field 1um gap',
          'real background from dilute Maxwell-Garnett mixture using same assumed core/host constants; passive loss unacquired'],
       'derived':{'mlj_slope_per_ev':aev,'effective_dipole_e_nm':mu/(E*1e-9),
           'pump_per_site_s':pump,'subpopulation_occupations':p.tolist(),
           'amplitude_average_rate_s':float(weights@rates),
           'weak_pump_effective_rate_s':float(1/(weights@(1/rates))),
           'kinetic_corner_frequencies_Hz':((pump+rates)/(2*np.pi)).tolist(),
           'rigid_sphere_rotation_time_s':tau,
           'individual_rotation_critical_times_s':(1/(rates*a*KB*T)).tolist(),
           'dot_volume_fraction':phi,'Maxwell_Garnett_real_permittivity':epsr,
           'capacitance_F':cap,'reaction_plus_orientation_Y_90MHz_real_S':float(at90.real),
           'reaction_plus_orientation_Y_90MHz_imag_S':float(at90.imag),
           'minimum_ReY_on_grid_S':float(viscous.real[idx]),'frequency_of_minimum_on_grid_Hz':float(freq[idx]),
           'immobile_ReY_90MHz_S':float(y(np.array([90e6]),0.)[0].real),
           'max_background_tan_delta_at_90MHz_if_no_other_loss':gain90/passive_b,
           'minimum_matched_LC_Q_at_90MHz_ideal_capacitance_only':passive_b/gain90,
           'Vpeak_for_probe_budget':.01,'incremental_RF_power_at_10mV_peak_W':gain90*.01**2/2,
           'minimum_absorbed_productive_pump_W':pump_min,
           'minimum_absorbed_pump_W_per_cm2':pump_min/area/1e4,
           'charge_dipole_model_validity':'local-field interaction corrections beyond dilute dielectric estimate are omitted',
           'immobile_population_current_noise_90MHz_A_per_sqrtHz':np.sqrt(psd90),
           'immobile_noise_to_gain_temperature_ratio_K':1/(KB*a),
           'minimum_phase_resolution_rad_for_20percent_signal':.2*gain90/passive_b},
       'rotation_controls':[]}
    for tn in [2.,5.,8.,12.,20.,40.,80.,160.]:
        z=y(np.array([90e6]),1/(tn*1e-9))[0]
        data['rotation_controls'].append({'tau_ns':tn,'ReY_90MHz_S':float(z.real)})
    checks={
        'mixture_weights_normalized':abs(sum(weights)-1)<1e-14,
        'total_occupation_target':abs(weights@p-target)<1e-10,
        'mixture_pump_recombination_balance':abs(pump*(1-weights@p)-weights@(p*rates))<1e-6,
        'viscous_hydrodynamic_time_exceeds_component_thresholds':bool(np.all(tau>1/(rates*a*KB*T))),
        'reaction_gain_in_selected_window':bool(np.any(viscous.real<0)),
        'fast_rotation_control_absorbs':bool(np.all(y(freq,1/(2e-9)).real>0)),
        'arithmetic_mean_differs_from_CW_rate':abs((weights@rates)/(1/(weights@(1/rates)))-1)>.5,
    }
    checks={key:bool(value) for key,value in checks.items()}
    data['checks']=checks;data['check_count']=len(checks);data['all_checks_pass']=all(checks.values())
    with (folder/'source_constrained_response.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['frequency_Hz','ReY_immobile_S','ImY_immobile_S','ReY_viscous_S','ImY_viscous_S'])
        writer.writerows(zip(freq,immobile.real,immobile.imag,viscous.real,viscous.imag))
    (folder/'source_constrained_results.json').write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))
    if not all(checks.values()): raise AssertionError('Source-linked diagnostic failed')

if __name__=='__main__':main()
