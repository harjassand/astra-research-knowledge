#!/usr/bin/env python3
"""Voltage-marked post-formation pulse calibration; NOT a power-gain test.

Create charge pairs at zero field. After formation, apply +/-V and subtract a
matched dark-step trace. This model predicts the slower population displacement
only; real instrumental bandwidth, state polarizability and formation tails
must be acquired separately. The step source supplies electrical energy.
"""
from pathlib import Path
import json,csv
import numpy as np
from scipy.integrate import solve_ivp
from scipy.constants import Boltzmann as KB, elementary_charge as E, Avogadro as NA
from feasibility import mlj_log_rate_and_slope


def main():
    out=Path(__file__).resolve().parent/'results'
    c=json.loads((out/'coupling_results.json').read_text())
    v=json.loads((out/'source_constrained_results.json').read_text())
    mu=c['nominal']['terminal_dipole_e_nm']*E*1e-9
    k=np.array([.996e9,.219e9]); w=np.array([.44,.56]); beta=1/(KB*298.15)
    a=mlj_log_rate_and_slope(1.51)[1]/E
    rho,area,d,pcreated=NA,1e-8,1e-6,.01
    wait=.3e-9
    p0=pcreated*np.exp(-k*wait)
    tau=v['derived']['rigid_sphere_rotation_time_s'];b=1/tau
    B=area/d*rho*mu**2*w*p0/3
    t=np.linspace(0,30e-9,6001)
    factors=(b*beta-k*a)/b
    def q_per_v(times):
        tt=np.asarray(times)
        diff=np.exp(-k[:,None]*tt[None,:])*(-np.expm1(-b*tt[None,:]))
        return np.sum(B[:,None]*factors[:,None]*diff,axis=0)
    q=q_per_v(t)
    current=np.sum(B[:,None]*factors[:,None]*(-k[:,None]*np.exp(-k[:,None]*t)
                       +(k+b)[:,None]*np.exp(-(k+b)[:,None]*t)),axis=0)
    # Independent integration for each component, normalized time to ns.
    kn=k*1e-9;bn=b*1e-9
    forcing=B*(b*beta-k*a)*1e-9
    sol=solve_ivp(lambda tn,z:-(kn+bn)*z+forcing*np.exp(-kn*tn),[0,30],np.zeros(2),
                  t_eval=t*1e9,method='DOP853',rtol=1e-10,atol=1e-28)
    response_sum=sol.y.sum(axis=0)
    idx=int(np.argmin(q))
    # Whole integrated displacement is zero as time tends to infinity, not net DC work.
    end=q_per_v(np.array([300e-9]))[0]
    bsmall=1e-3
    lim=np.sum(B[:,None]*(-k*a)[:,None]*t[None,:]*np.exp(-k[:,None]*t),axis=0)
    approx=np.sum(B[:,None]*((bsmall*beta-k*a)/bsmall)[:,None]*np.exp(-k[:,None]*t)*(-np.expm1(-bsmall*t))[None,:],axis=0)
    checks={
      'zero_initial_population_displacement':abs(q[0])<1e-28,
      'return_to_zero_after_reset':abs(end)<1e-28,
      'linear_ODE_matches_closed_form':float(np.max(abs(response_sum-q)))<1e-25,
      'initial_slope_negative_in_scoped_inverted_model':bool(current[0]<0),
      'slow_rotation_limit':float(np.max(abs(approx-lim)))<1e-25
    }
    checks={name:bool(value) for name,value in checks.items()}
    data={'status':'Proposed calibration transient, not measured and not autonomous power',
          'scope':'same mixture/host assumptions as final budget; ideal step and instantaneous completed formation',
          'created_occupation':pcreated,'wait_after_ideal_creation_s':wait,
          'recombination_survival_at_step':float(np.dot(w,np.exp(-k*wait))),
          'maximum_voltage_for_example_V':1.,
          'predicted_peak_charge_per_volt_C_per_V':float(q[idx]),
          'predicted_peak_time_after_step_s':float(t[idx]),
          'predicted_initial_current_per_volt_A_per_V':float(current[0]),
          'linearization_parameter_a_mu_E_at_1V':float(a*mu/d),
          'checks':checks,'check_count':len(checks),'all_checks_pass':all(checks.values()),
          'limitations':['electrical step is an external energy source: this is calibration only',
             'source multiexponential formation is not instantaneous; use acquired convolution and wait dependence',
             'prompt polarization and state-dependent electronic polarizability require separate subtraction/model',
             'rotational diffusion and postformation hole hopping are not interchangeable',
             'instrument step response/readout needs subnanosecond bandwidth and matched-reference control']}
    (out/'pulse_calibration_results.json').write_text(json.dumps(data,indent=2))
    with (out/'pulse_calibration.csv').open('w',newline='') as f:
        z=csv.writer(f);z.writerow(['time_after_step_s','population_charge_per_volt_C_per_V','population_current_per_volt_A_per_V'])
        z.writerows(zip(t,q,current))
    print(json.dumps(data,indent=2))
    if not all(checks.values()):raise AssertionError('Pulse calibration check failed')
if __name__=='__main__':main()
