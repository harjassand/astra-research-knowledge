#!/usr/bin/env python3
"""Coupled finite-volume radial slurry / fixed-end whole-pipe torsional model.

The steel tube ends do not rotate. A central drive excites its first loaded
torsional mode. The material law is the explicitly conditional nonlinear law
in nonlinear_transport.py. Intermediate gravity supports are represented by
stated rotational stiffness and loss, not silently omitted.
"""
from dataclasses import replace,asdict
from pathlib import Path
import json
import math
import time

import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq

import nonlinear_transport as model


def mechanical_matrix(omega,inertia,fluid_damping,stiffness,quality):
    n=len(inertia)
    band=np.zeros((3,n),dtype=complex)
    diagonal=stiffness.diagonal()
    band[1]=(1+1j/quality)*diagonal-omega**2*inertia+1j*omega*fluid_damping
    band[0,1:]=(1+1j/quality)*np.diag(stiffness,1)
    band[2,:-1]=(1+1j/quality)*np.diag(stiffness,-1)
    return band


def solve_mode(target,Vpeak,p,nz=11,nr=48,lever=.5,quality=20.,support_k=100.,max_steps=12):
    assert nz%2==1
    z=np.linspace(0,p.length,nz);h=z[1]-z[0]
    center=(nz-2)//2
    outer=p.radius+p.steel_thickness
    J=math.pi*(outer**4-p.radius**4)/2
    Isteel=p.steel_density*J
    Gsteel=79e9 # Design assumption, not measured on this proposed pipe.
    stiffness=Gsteel*J/h*(np.diag(np.full(nz-2,2.))+
       np.diag(np.full(nz-3,-1.),1)+np.diag(np.full(nz-3,-1.),-1))
    # One ideal rotationally compliant gravity support at every interior node.
    # A separate loss quality is not supplied; quality20 applies also to these
    # ground springs. Their actual loaded stiffness and loss remain a gate.
    stiffness+=np.eye(nz-2)*support_k
    steel_mass=np.full(nz-2,Isteel*h)
    drive_arm_inertia=2*(.099+.5/3)*lever**2
    steel_mass[center]+=drive_arm_inertia
    rhs=np.zeros(nz-2,dtype=complex);rhs[center]=1
    omega=math.pi*math.sqrt(Gsteel/p.steel_density)/p.length
    shape=np.sin(math.pi*z[1:-1]/p.length).astype(complex)
    rows=[];history=[];converged=False
    for count in range(max_steps):
        local_p=replace(p,length=1.)
        # Symmetry halves the costly source-based nonlinear fluid solves.
        half=[]
        for j in range(center+1):
            v=Vpeak*abs(shape[j])
            half.append(model.matched_mean(target,omega,v,local_p,n=nr))
        rows=half+half[-2::-1]
        fluid_inertia=np.array([r['fluid_added_inertia'] for r in rows])*h
        Omega=Vpeak*np.abs(shape)/p.radius
        fluid_damping=np.array([r['fluid_torque_real'] for r in rows])/Omega*h
        inertia=steel_mass+fluid_inertia
        def response(w):
            return solve_banded((1,1),mechanical_matrix(w,inertia,fluid_damping,stiffness,quality),rhs)
        def reactance(w):
            return (1/response(w)[center]).real
        newomega=brentq(reactance,omega*.7,omega*1.3,xtol=1e-8)
        trial=response(newomega)
        newshape=trial/trial[center]
        err=max(abs(newomega/omega-1),float(np.max(np.abs(newshape-shape))))
        history.append({'iteration':count+1,'omega':float(newomega),'shape_frequency_error':err})
        print('mode',Vpeak,count+1,newomega,err,flush=True)
        if err<2e-4:
            shape=newshape;omega=newomega;converged=True;break
        shape=.4*shape+.6*newshape;omega=.4*omega+.6*newomega
    # Recompute the final fluid state, then solve the linear mechanical system
    # at this frozen state. This ensures exact discrete energy bookkeeping.
    half=[]
    for j in range(center+1):
        half.append(model.matched_mean(target,omega,Vpeak*abs(shape[j]),replace(p,length=1.),n=nr))
    rows=half+half[-2::-1]
    fluid_inertia=np.array([r['fluid_added_inertia'] for r in rows])*h
    Omega=Vpeak*np.abs(shape)/p.radius
    fluid_damping=np.array([r['fluid_torque_real'] for r in rows])/Omega*h
    inertia=steel_mass+fluid_inertia
    band=mechanical_matrix(omega,inertia,fluid_damping,stiffness,quality)
    response=solve_banded((1,1),band,rhs)
    theta0=Vpeak/(p.radius*omega)
    torque=theta0/response[center]
    theta=torque*response
    shape_error=float(np.max(np.abs(theta/theta[center]-shape)))
    fluid_power=float(.5*omega**2*np.sum(fluid_damping*np.abs(theta)**2))
    structural=float(.5*omega/quality*np.vdot(theta,stiffness@theta).real)
    drive_power=float(.5*np.real(torque*np.conj(1j*omega*theta[center])))
    balance=abs(drive_power-fluid_power-structural)/max(1e-30,drive_power)
    assert balance<1e-9
    # Lumped axial integration includes half-cell regions at the clamped ends,
    # where local wall velocity vanishes and the unactuated gradient applies.
    baseline_g,baseline=model.unactuated_matched(target,p)
    gradients=np.r_[baseline_g,[r['pressure_gradient'] for r in rows],baseline_g]
    pressure=float(np.trapezoid(gradients,x=z))
    flow=math.pi*p.radius**2*target
    axial=pressure*flow
    force=abs(torque)/(2*lever)
    current=force/(27.8*math.sqrt(2))
    copper=2*11.5*current**2
    electric=axial/p.pump_efficiency+drive_power+copper
    theta_with_ends=np.r_[0,theta,0]
    twist=np.diff(theta_with_ends)/h
    shear_stress_peak=Gsteel*outer*float(np.max(np.abs(twist)))
    linear_weight=(p.steel_density*math.pi*(outer**2-p.radius**2)+
                   p.density*math.pi*p.radius**2)*9.81
    # Beam estimate: steel only provides bending stiffness; supports at h.
    bending_I=J/2;E=200e9
    support_deflection=5*linear_weight*h**4/(384*E*bending_I)
    support_bending_stress=linear_weight*h**2/8*outer/bending_I
    return {'converged_mode_iteration':converged,'history':history,
      'axial_nodes':nz,'radial_cells':nr,'support_spacing_m':h,
      'assumed_support_rotational_stiffness_Nm_rad':support_k,
      'assumed_structural_quality':quality,'steel_shear_modulus_assumed_Pa':Gsteel,
      'frequency_hz':omega/(2*math.pi),'omega':omega,'wall_velocity_peak':Vpeak,
      'center_wall_displacement_m':Vpeak/omega,'center_angle_rad':theta0,
      'flow_L_min':flow*60000,'axial_pressure_drop_Pa':pressure,
      'baseline_electric_W':baseline,'axial_fluid_power_W':axial,
      'cross_fluid_power_W':fluid_power,'structural_loss_W':structural,
      'actuator_copper_loss_W':copper,'drive_mechanical_power_W':drive_power,
      'total_electric_before_idle_W':electric,'electric_ratio':electric/baseline,
      'maximum_extra_idle_support_W':baseline-electric,
      'actuator_peak_force_N':force,'actuator_rms_current_A':current,
      'actuator_stroke_amplitude_m':lever*theta0,
      'actuator_continuous_rating_met':bool(force/math.sqrt(2)<27),
      'steel_torsional_stress_peak_Pa':shear_stress_peak,
      'support_static_load_N':linear_weight*h,
      'span_bending_deflection_m':support_deflection,
      'span_bending_stress_Pa':support_bending_stress,
      'linearized_mechanical_power_balance_error':balance,
      'final_shape_self_consistency_error':shape_error,
      'maximum_material_strain':max(r['material_strain_max'] for r in rows),
      'maximum_chi':max(r['chi_max'] for r in rows),
      'any_OSP_chi_extrapolation':any(r['outside_OSP_chi_data'] for r in rows),
      'any_unactuated_extrapolation':any(r['outside_unactuated_stress_data'] for r in rows),
      'local_rows':[model.clean(r) for r in rows],
      'physical_gate':'End rotation is zero, avoiding torsional fluid couplings. Actual gravity-support stiffness/loss, actuator driver loss, material dynamics and fatigue remain unmeasured.'}


def main():
    tic=time.perf_counter();p=model.Parameters();out=[];fail=[]
    for v in (.006,.01,.016):
        try:
            out.append(solve_mode(.00625,v,p))
        except (RuntimeError,ValueError) as error:
            fail.append({'wall_velocity':v,'error':str(error)})
        Path(__file__).with_name('standing_mode.json').write_text(json.dumps({
          'status':'Conditional coupled radial fluid/whole-pipe mechanical construction; not demonstrated',
          'parameters':asdict(p),'cases':out,'failures':fail,
          'seconds':time.perf_counter()-tic},indent=2)+'\n')


if __name__=='__main__':
    main()
