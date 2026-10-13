#!/usr/bin/env python3
"""Experimental-curve cylindrical transport model.

Data: Lin, Ness, Cates, Sun, Cohen (2016), DOI10.7488/ds/1445, CC-BY4.0.
Modified by monotone log-space pooling/interpolation and plateau clipping.
Use as a local cycle-averaged pipe law remains an unvalidated assumption.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import math
import time

import numpy as np
from scipy.linalg import solve_banded
from scipy.special import iv
from scipy.optimize import brentq
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator
from scipy.optimize import isotonic_regression
from functools import lru_cache


@dataclass(frozen=True)
class Parameters:
    empirical_amplitude: str = "1.0"
    radius: float = 0.0625
    length: float = 20.0
    density: float = 1700.0
    eta_high: float = 500.0
    eta_low: float = 5.0
    eta_low_cross: float = 8.0
    chi_parallel: float = 0.55
    chi_cross: float = 0.35
    exponent_parallel: float = 1.8
    exponent_cross: float = 1.7
    steel_thickness: float = 0.0077
    steel_density: float = 7850.0
    pump_efficiency: float = 0.70
    actuator_efficiency: float = 0.60
    structural_quality: float = 20.0
    max_material_strain: float = 0.05


@lru_cache(maxsize=32)
def raw_curve(amplitude,kind,high):
    path=(Path(__file__).parent/'sources/biaxial_raw/biaxial_repository/fig1d'/
          f'fig1d_{amplitude}_{kind}.csv')
    data=np.loadtxt(path,delimiter=',')
    # Pool noisy local reversals without a tunable parametric viscosity law.
    log_eta=np.log(data[:,1])
    fit=isotonic_regression(log_eta,increasing=False).x
    eta=np.minimum(np.exp(fit),high)
    # Under-range values return to the measured unperturbed approximate
    # plateau over one decade, rather than extrapolating a drop to chi=0.
    x=np.r_[np.log(data[0,0]/10),np.log(data[:,0])]
    y=np.r_[np.log(high),np.log(eta)]
    f=PchipInterpolator(x,y,extrapolate=False)
    return f,data,eta


def empirical_viscosity(chi,p,kind):
    f,data,eta=raw_curve(p.empirical_amplitude,kind,p.eta_high)
    x=np.log(np.maximum(chi,1e-100))
    clipped=np.clip(x,np.log(data[0,0]/10),np.log(data[-1,0]))
    return np.exp(f(clipped))


def curve_diagnostics(amplitude,p):
    result={}
    for kind in ('primary','OSP'):
        f,data,eta=raw_curve(amplitude,kind,p.eta_high)
        result[kind]={'points':len(data),'chi_min':float(data[0,0]),
          'chi_max':float(data[-1,0]),'endpoint_eta':float(eta[-1]),
          'max_log_adjustment_from_raw':float(np.max(np.abs(np.log(eta/data[:,1])))),
          'assumed_perturbation_free_viscosity':p.eta_high,
          'modification':'PAVA decreasing log-viscosity; clip to stated baseline; PCHIP log-log; conservative constant upper-chi endpoint; lower-chi bridge over one decade.'}
    return result


def cross_solve(eta_faces, omega, velocity, p):
    """Finite volume for (r^3 eta v')' = i omega rho r^3 v, w=r*v.

    Face angular velocity gradient is the physical shear / r. Thus rigid
    rotation has exactly zero shear, unlike a planar approximation w'.
    """
    n=len(eta_faces)-1
    dr=p.radius/n
    faces=np.linspace(0,p.radius,n+1)
    volume=(faces[1:]**4-faces[:-1]**4)/4
    conductance=faces**3*eta_faces/dr
    left=conductance[:-1].copy()
    right=conductance[1:].copy()
    right[-1]*=2
    band=np.zeros((3,n),dtype=complex)
    band[1]=left+right+1j*omega*p.density*volume
    band[0,1:]=-right[:-1]
    band[2,:-1]=-left[1:]
    rhs=np.zeros(n,dtype=complex)
    rhs[-1]=right[-1]*velocity/p.radius
    angular=solve_banded((1,1),band,rhs)
    gradient=np.zeros(n+1,dtype=complex)
    gradient[1:-1]=np.diff(angular)/dr
    gradient[-1]=(velocity/p.radius-angular[-1])/(dr/2)
    shear=faces*gradient
    # Surface stress times velocity; average of real sinusoidal products.
    fluid_power=math.pi*p.radius*p.length*np.real(eta_faces[-1]*shear[-1]*velocity)
    # Independent volume dissipation of the discrete finite-volume system.
    # Each interior edge is counted once; outer Dirichlet half-cell included.
    edge_diff=np.r_[0,np.diff(angular),velocity/p.radius-angular[-1]]
    edge_g=conductance.copy();edge_g[-1]*=2
    discrete_power=math.pi*p.length*np.sum(edge_g*np.abs(edge_diff)**2)
    relative_balance=abs(fluid_power-discrete_power)/max(1e-30,fluid_power)
    assert fluid_power >= -1e-12 and discrete_power >=0
    # At very small frequency, the real part of wall stress is obtained by
    # subtracting almost rigid rotations and loses relative precision. The
    # strictly positive volume form is the stable power evaluation used below.
    assert abs(fluid_power-discrete_power)<1e-6*max(1.,discrete_power)
    return shear,float(discrete_power),angular,relative_balance


def axial_from_cross(shear, pressure_gradient, p):
    n=len(shear)-1
    r=np.linspace(0,p.radius,n+1)
    stress=pressure_gradient*r/2
    s=np.abs(shear)
    low=stress/p.eta_high
    high=stress/p.eta_low
    for _ in range(55):
        gamma=(low+high)/2
        chi=np.divide(s,gamma,out=np.zeros_like(s),where=gamma>0)
        eta=empirical_viscosity(chi,p,"primary")
        too_low=gamma*eta<stress
        low=np.where(too_low,gamma,low)
        high=np.where(too_low,high,gamma)
    gamma=(low+high)/2
    chi=np.divide(s,gamma,out=np.zeros_like(s),where=gamma>0)
    eta_parallel=empirical_viscosity(chi,p,"primary")
    eta_cross=empirical_viscosity(chi,p,"OSP")
    # Q/pi = integral r^2 gamma(r) dr, hence mean velocity = integral/R^2.
    # Simpson integrates the constant-viscosity cubic integrand exactly. This
    # prevents an O(grid^-2) fake gain against the analytic Poiseuille control.
    mean_velocity=simpson(r*r*gamma,x=r)/(p.radius*p.radius)
    return mean_velocity,eta_parallel,eta_cross,gamma,chi


def coupled(pressure_gradient,omega,velocity,p,n=128,initial='high',tol=1e-8):
    eta=np.full(n+1,p.eta_high if initial=='high' else p.eta_low_cross)
    converged=False
    for count in range(600):
        shear,power,angular,balance=cross_solve(eta,omega,velocity,p)
        mean,eta_parallel,target,gamma,chi=axial_from_cross(shear,pressure_gradient,p)
        error=np.max(np.abs(np.log(target/eta)))
        if error<tol:
            converged=True
            break
        eta=np.exp(0.75*np.log(eta)+0.25*np.log(target))
    flow=math.pi*p.radius*p.radius*mean
    axial_power=pressure_gradient*p.length*flow
    outer=p.radius+p.steel_thickness
    inertia=0.5*math.pi*p.steel_density*p.length*(outer**4-p.radius**4)
    wall_kinetic=0.5*inertia*(velocity/p.radius)**2
    structural_power=omega*wall_kinetic/p.structural_quality
    electrical=axial_power/p.pump_efficiency+(power+structural_power)/p.actuator_efficiency
    return {'converged':converged,'iterations':count+1,'fixed_point_error':float(error),
      'pressure_gradient':pressure_gradient,'omega':omega,'wall_velocity':velocity,
      'mean_velocity':float(mean),'flow_m3_s':float(flow),
      'axial_power':float(axial_power),'cross_fluid_power':float(power),
      'wall_structural_loss':float(structural_power),'electrical_total':float(electrical),
      'wall_peak_kinetic_energy':float(wall_kinetic),
      'material_strain_max':float(np.max(np.abs(shear))/omega),
      'material_strain_admissible':bool(np.max(np.abs(shear))/omega <=p.max_material_strain),
      'wall_displacement_amplitude_m':velocity/omega,
      'surface_power_balance_relative_error':float(balance),
      'eta_parallel_wall':float(eta_parallel[-1]),'eta_cross_wall':float(eta[-1]),
      'chi_wall':float(chi[-1]),'chi_max':float(np.max(chi)),
      'chi_above_experimental_max':bool(np.max(chi)>raw_curve(p.empirical_amplitude,'primary',p.eta_high)[1][-1,0]),
      'eta_cross':eta,'shear':shear,
      'gamma_axial':gamma,'eta_parallel':eta_parallel,'chi':chi}


def matched_mean(target,omega,velocity,p,n=128):
    baseline_gradient=8*p.eta_high*target/(p.radius*p.radius)
    def residual(g):
        row=coupled(g,omega,velocity,p,n=n)
        if not row['converged']:
            raise RuntimeError('Nonconverged constitutive fixed point')
        return row['mean_velocity']-target
    gradient=brentq(residual,baseline_gradient*p.eta_low/p.eta_high/2,
                    baseline_gradient*1.01,xtol=1e-8,rtol=1e-9)
    row=coupled(gradient,omega,velocity,p,n=n)
    row['baseline_pressure_gradient']=baseline_gradient
    row['baseline_electrical']=baseline_gradient*p.length*math.pi*p.radius**2*target/p.pump_efficiency
    row['energy_ratio']=row['electrical_total']/row['baseline_electrical']
    row['pressure_ratio']=gradient/baseline_gradient
    headroom=p.actuator_efficiency*(row['baseline_electrical']-row['axial_power']/p.pump_efficiency)-row['cross_fluid_power']
    row['minimum_structural_quality_for_energy_gain']=(omega*row['wall_peak_kinetic_energy']/headroom if headroom>0 else None)
    return row


def clean(row):
    return {key:value for key,value in row.items() if not isinstance(value,np.ndarray)}


def check_exact_solution():
    p=Parameters()
    results=[]
    for omega in (0.01,1,10,100):
        errors=[]
        for n in (64,128,256):
            eta=np.full(n+1,500.0)
            shear,power,angular,balance=cross_solve(eta,omega,0.01,p)
            r=(np.arange(n)+.5)*p.radius/n
            k=np.sqrt(1j*omega*p.density/500.0)
            exact=0.01*iv(1,k*r)/iv(1,k*p.radius)/r
            relative=float(np.max(np.abs(angular-exact))/np.max(np.abs(exact)))
            exact_wall=0.01*k*iv(2,k*p.radius)/iv(1,k*p.radius)
            wall_error=abs(shear[-1]-exact_wall)/abs(exact_wall)
            errors.append({'grid':n,'relative_angular_error':relative,
                          'relative_wall_shear_error':float(wall_error),
                          'power_balance_error':balance})
        assert errors[-1]['relative_angular_error']<errors[0]['relative_angular_error']/10
        results.append({'omega':omega,'grids':errors})
    return results


def main():
    from dataclasses import replace
    tic=time.perf_counter()
    p=Parameters()
    target=.2*p.radius/4
    fixed=[]
    for amplitude in ('0.5','0.7','1.0','1.5','2.0','3.0'):
        for plateau in (450.,500.,550.):
            model=replace(p,empirical_amplitude=amplitude,eta_high=plateau)
            try:
                row=clean(matched_mean(target,100.,.01,model,n=96))
            except RuntimeError as error:
                row={'converged':False,'error':str(error)}
            row.update(amplitude_percent=amplitude,baseline_viscosity=plateau)
            fixed.append(row)
    grids=[clean(matched_mean(target,100.,.01,p,n=n))|{'grid':n} for n in (64,128,256)]
    scan=[];failures=[]
    for omega in (30.,60.,100.,200.,300.):
        for velocity in np.geomspace(.001,.03,12):
            try:
                scan.append(clean(matched_mean(target,omega,float(velocity),p,n=64)))
            except RuntimeError as error:
                failures.append({'omega':omega,'wall_velocity':float(velocity),'error':str(error)})
    admissible=[r for r in scan if r['material_strain_admissible'] and not r['chi_above_experimental_max']]
    best=min(admissible,key=lambda r:r['energy_ratio']) if admissible else None
    result={'status':'measured viscosity curves; conditional local pipe closure and assumed mechanics',
      'data_attribution':'Lin, Ness, Cates, Sun, Cohen2016, DOI10.7488/ds/1445, CC-BY4.0; modified interpolation described below.',
      'data_archive_sha256':'9eb8ebcb1a188099a0a30cc2530294ab2e850236ad0e9058399828ff399963b3',
      'parameters':asdict(p),'curves':{a:curve_diagnostics(a,p) for a in ('0.5','0.7','1.0','1.5','2.0','3.0')},
      'fixed_candidate_data_sensitivity':fixed,'fixed_candidate_grid_convergence':grids,
      'scan':scan,'nonconvergence':failures,'best_in_range':best,
      'gate_caveats':['Complex OSP viscosity magnitude is treated as a real dissipative coefficient; phase unavailable.',
          'Spatially varying pipe primary rate differs from fixed0.2/s source rheometry.',
          'Each amplitude curve is a sensitivity model, not a measured local material amplitude law.',
          'Whole-pipe support, seal, driver idle, density and quality factor are not measured.'],
      'seconds':time.perf_counter()-tic}
    Path(__file__).with_name('empirical_transport.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('scan','curves')},indent=2))


if __name__=='__main__':
    main()
