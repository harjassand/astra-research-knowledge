#!/usr/bin/env python3
"""Corrected unactuated control and a conditional nonlinear OSP pipe closure.

Unactuated stress/rate law is digitised from primary SI Fig6. OSP reduction
factors use author-deposited Fig1d data. Their multiplicative contact-viscosity
combination away from the measured primary rate is an ASSUMPTION, explicitly
different from measured validation. Complex-viscosity phase is swept separately.
"""
from dataclasses import dataclass,replace,asdict
from functools import lru_cache
from pathlib import Path
import json
import math
import time

import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator
from scipy.linalg import solve_banded
from scipy.optimize import brentq,isotonic_regression

import empirical_transport as empirical


@dataclass(frozen=True)
class Parameters(empirical.Parameters):
    rate_scale: float = 1.0
    phase_angle: float = math.pi/2
    hydrodynamic_parallel: float = 9.0
    hydrodynamic_cross: float = 7.0


@lru_cache(maxsize=1)
def unactuated_curve():
    data=np.loadtxt(Path(__file__).parent/'sources/lin_fig6_digitised.csv',
                    delimiter=',',skiprows=1)
    rate=np.exp(isotonic_regression(np.log(data[:,2]),increasing=True).x)
    f=PchipInterpolator(np.log(data[:,0]),np.log(rate),extrapolate=False)
    return f,data,rate


def unactuated_rate(stress,p):
    f,data,rate=unactuated_curve()
    stress=np.asarray(stress)
    low_eta=data[0,0]/rate[0]
    high_eta=data[-1,0]/rate[-1]
    result=np.exp(f(np.log(np.clip(stress,data[0,0],data[-1,0]))))
    result=np.where(stress<data[0,0],stress/low_eta,result)
    result=np.where(stress>data[-1,0],stress/high_eta,result)
    return p.rate_scale*result


def unactuated_mean(gradient,p,n=512):
    r=np.linspace(0,p.radius,n+1)
    gamma=unactuated_rate(gradient*r/2,p)
    return simpson(r*r*gamma,x=r)/p.radius**2


def unactuated_matched(target,p):
    gradient=brentq(lambda g:unactuated_mean(g,p)-target,1e-9,1e7,xtol=1e-10)
    flow=math.pi*p.radius**2*target
    return gradient,gradient*p.length*flow/p.pump_efficiency


def axial_from_cross(shear,gradient,p):
    r=np.linspace(0,p.radius,len(shear))
    stress=gradient*r/2
    s=np.abs(shear)
    # Parameterise by equivalent unperturbed stress h; this handles the steep
    # DST graph without inventing a single-valued inverse rate/stress curve.
    low=np.zeros_like(stress)
    high=np.maximum(stress*200,2000.)
    for _ in range(52):
        h=(low+high)/2
        gamma=unactuated_rate(h,p)
        eta0=np.divide(h,gamma,out=np.full_like(h,p.eta_high),where=gamma>0)
        chi=np.divide(s,gamma,out=np.zeros_like(s),where=gamma>0)
        measured=empirical.empirical_viscosity(chi,p,'primary')
        fraction=np.clip((measured-p.hydrodynamic_parallel)/
                         (p.eta_high-p.hydrodynamic_parallel),0,1)
        eta_parallel=p.hydrodynamic_parallel+(eta0-p.hydrodynamic_parallel)*fraction
        stress_model=gamma*eta_parallel
        low=np.where(stress_model<stress,h,low)
        high=np.where(stress_model<stress,high,h)
    h=(low+high)/2
    gamma=unactuated_rate(h,p)
    eta0=np.divide(h,gamma,out=np.full_like(h,p.eta_high),where=gamma>0)
    chi=np.divide(s,gamma,out=np.zeros_like(s),where=gamma>0)
    para=empirical.empirical_viscosity(chi,p,'primary')
    cross=empirical.empirical_viscosity(chi,p,'OSP')
    fp=np.clip((para-p.hydrodynamic_parallel)/(p.eta_high-p.hydrodynamic_parallel),0,1)
    fc=np.clip((cross-p.hydrodynamic_cross)/(p.eta_high-p.hydrodynamic_cross),0,1)
    ep=p.hydrodynamic_parallel+(eta0-p.hydrodynamic_parallel)*fp
    ec=p.hydrodynamic_cross+(eta0-p.hydrodynamic_cross)*fc
    mean=simpson(r*r*gamma,x=r)/p.radius**2
    return mean,ep,ec,gamma,chi,h


def cross_solve(eta_magnitude,omega,velocity,p):
    # For strain proportional to sin(omega*t), phase delta between stress and
    # strain gives eta*=|eta*|(sin(delta)-i*cos(delta)). Re eta* is passive.
    eta=eta_magnitude*(math.sin(p.phase_angle)-1j*math.cos(p.phase_angle))
    n=len(eta)-1
    dr=p.radius/n
    faces=np.linspace(0,p.radius,n+1)
    volume=np.diff(faces**4)/4
    conductance=faces**3*eta/dr
    left=conductance[:-1].copy()
    right=conductance[1:].copy();right[-1]*=2
    band=np.zeros((3,n),dtype=complex)
    band[1]=left+right+1j*omega*p.density*volume
    band[0,1:]=-right[:-1];band[2,:-1]=-left[1:]
    rhs=np.zeros(n,dtype=complex);rhs[-1]=right[-1]*velocity/p.radius
    angular=solve_banded((1,1),band,rhs)
    gradient=np.zeros(n+1,dtype=complex)
    gradient[1:-1]=np.diff(angular)/dr
    gradient[-1]=(velocity/p.radius-angular[-1])/(dr/2)
    shear=faces*gradient
    edge_diff=np.r_[0,np.diff(angular),velocity/p.radius-angular[-1]]
    edge_g=conductance.copy();edge_g[-1]*=2
    power=float(math.pi*p.length*np.sum(edge_g.real*np.abs(edge_diff)**2))
    torque=2*math.pi*p.radius**2*p.length*eta[-1]*shear[-1]
    surface=float(.5*np.real(torque*velocity/p.radius))
    assert power>=0 and abs(power-surface)<1e-7*max(1,power)
    return shear,power,torque,angular


def coupled(gradient,omega,velocity,p,n=96,initial='high',tol=1e-7):
    eta=np.full(n+1,p.eta_high if initial=='high' else p.hydrodynamic_cross)
    converged=False
    for count in range(750):
        shear,power,torque,angular=cross_solve(eta,omega,velocity,p)
        mean,ep,ec,gamma,chi,h=axial_from_cross(shear,gradient,p)
        error=float(np.max(np.abs(np.log(ec/eta))))
        if error<tol:
            converged=True;break
        eta=np.exp(.8*np.log(eta)+.2*np.log(ec))
    flow=math.pi*p.radius**2*mean
    angular_velocity=velocity/p.radius
    impedance=torque/angular_velocity if angular_velocity else 0j
    added_inertia=impedance.imag/omega
    axial=gradient*p.length*flow
    return {'converged':converged,'iterations':count+1,'fixed_point_error':error,
      'pressure_gradient':float(gradient),'omega':omega,'wall_velocity':velocity,
      'mean_velocity':float(mean),'flow_L_min':float(flow*60000),
      'axial_fluid_power':float(axial),'cross_fluid_power':power,
      'fluid_added_inertia':float(added_inertia),
      'fluid_torque_real':float(torque.real),'fluid_torque_imag':float(torque.imag),
      'material_strain_max':float(np.max(np.abs(shear))/omega),
      'chi_max':float(np.max(chi)),'primary_rate_wall':float(gamma[-1]),
      'equivalent_unactuated_stress_max':float(np.max(h)),
      'outside_unactuated_stress_data':bool(np.max(h)>unactuated_curve()[1][-1,0]),
      'outside_OSP_chi_data':bool(np.max(chi)>empirical.raw_curve(p.empirical_amplitude,'primary',p.eta_high)[1][-1,0]),
      'eta_cross':eta,'eta_parallel':ep,'shear':shear,'gamma':gamma,'chi':chi}


def matched_mean(target,omega,velocity,p,n=96):
    base,base_power=unactuated_matched(target,p)
    if velocity==0:
        row=coupled(base,omega,velocity,p,n=n)
    else:
        def residual(g):
            row=coupled(g,omega,velocity,p,n=n)
            if not row['converged']:
                raise RuntimeError('Nonconverged nonlinear constitutive fixed point')
            return row['mean_velocity']-target
        g=brentq(residual,base*1e-5,base*1.01,xtol=1e-8,rtol=1e-8)
        row=coupled(g,omega,velocity,p,n=n)
    row['baseline_pressure_gradient']=base
    row['baseline_electric']=base_power
    row['pressure_ratio']=row['pressure_gradient']/base
    return row


def clean(row):
    return {key:value for key,value in row.items() if not isinstance(value,np.ndarray)}


def rigid_resonator(row,p,lever=.5,arm_mass_each=.5,quality=20.,detuning=0.):
    """A hypothetical globally rotating pipe on torsional flexures, not a retrofit.

    Two H2W NCC05-18-060-2X moving coils: Kf27.8N/A,R11.5ohm,m99g.
    Arm mass assumes uniform radial bars; bearing/seal/driver idle still absent.
    Include fluid reactive loading in spring energy and detuning torque.
    """
    outer=p.radius+p.steel_thickness
    steel_inertia=.5*math.pi*p.steel_density*p.length*(outer**4-p.radius**4)
    arm_inertia=2*(.099+arm_mass_each/3)*lever**2
    inertia=steel_inertia+arm_inertia+row['fluid_added_inertia']
    omega=row['omega'];vel=row['wall_velocity'];Omega=vel/p.radius
    kinetic=.5*inertia*Omega**2
    structural=omega*kinetic/quality
    mechanical=row['cross_fluid_power']+structural
    dissipative_torque=2*mechanical/Omega
    reactive_torque=abs(2*detuning*inertia*omega*Omega)
    peak_torque=math.hypot(dissipative_torque,reactive_torque)
    peak_force=peak_torque/(2*lever)
    current_rms=peak_force/(27.8*math.sqrt(2))
    copper=2*current_rms**2*11.5
    electric=row['axial_fluid_power']/p.pump_efficiency+mechanical+copper
    return {'architecture':'Assumed soft torsional flexures and flexible fluid connections; not demonstrated.',
      'lever_m':lever,'arm_mass_each_kg_assumed':arm_mass_each,
      'mechanical_quality_assumed':quality,'frequency_detuning_fraction':detuning,
      'steel_inertia':steel_inertia,'arm_and_mover_inertia':arm_inertia,
      'fluid_added_inertia':row['fluid_added_inertia'],
      'torsional_spring_stiffness_Nm_rad':inertia*omega**2,
      'spring_peak_energy':kinetic,'structural_loss':structural,
      'copper_loss':copper,'actuator_peak_force_N':peak_force,
      'actuator_rms_current_A':current_rms,
      'actuator_stroke_amplitude_m':lever*vel/(omega*p.radius),
      'actuator_force_within_continuous_rms_rating':bool(peak_force/math.sqrt(2)<27),
      'total_electric_before_idle_and_seal':electric,
      'electric_ratio':electric/row['baseline_electric'],
      'maximum_extra_idle_seal_support_W':row['baseline_electric']-electric,
      'mechanical_caveat':'Required flexure, couplings, gravity supports, dynamic Q, driver losses and fatigue are unmeasured.'}


def main():
    tic=time.perf_counter();p=Parameters();target=.003125
    rows=[];fail=[]
    for factor in (1.,1.5,2.,3.):
        for velocity in (.005,.01,.02,.04):
            try:
                row=matched_mean(target*factor,100.,velocity,p,n=64)
                c=clean(row);c['throughput_factor']=factor
                c['rigid_resonator']=rigid_resonator(row,p)
                rows.append(c)
            except RuntimeError as error:
                fail.append({'factor':factor,'velocity':velocity,'error':str(error)})
            print('checkpoint',factor,velocity,flush=True)
            Path(__file__).with_name('nonlinear_transport.json').write_text(json.dumps({
              'status':'conditional source-based nonlinear closure; no attained performance',
              'parameters':asdict(p),'rows':rows,'failures':fail,
              'seconds':time.perf_counter()-tic},indent=2)+'\n')
    print('complete',len(rows),'failures',len(fail),flush=True)


if __name__=='__main__':
    main()
