#!/usr/bin/env python3
"""Introduced uniform laminated beam: finite shear stiffness is not clutch strength.

No source parameter fit and no producer execution. NumPy only, bounded serial work.
All states are small-deflection, intact, constant-coefficient, common-transverse-
displacement beams. Interfacial contact, activation, normal restraint and fatigue
are NOT constructed. Dielectric gaps add height and mass but their axial/bending
stiffness is neglected. The optional G is an INTRODUCED tangent shear modulus
AFTER contact, not a measurement from an electroadhesive paper.

Energy = 1/2 integral[EA*sum(u_i'^2) + B0*theta'^2
          + ks*sum(u_(i+1)-u_i+h*theta)^2] dx - F*integral(theta) dx.
u_i(0)=theta(0)=0; free axial forces and moment at x=L. h=t+d.
Spatial linear finite elements; layer eigenmodes permit a small exact modal solve.
"""
import json
from pathlib import Path
import numpy as np

E = 200e9
b = 0.020
t = 25e-6
d = 20e-6
n = 100
length = 0.300
force = 5.0
rho_metal = 7800.0
rho_gap = 1000.0
h = t + d
EA = E*b*t
B0 = n*E*b*t**3/12.0
y = (np.arange(n)-(n-1)/2.0)*h
B_full = B0+EA*float(y@y)
height = n*t+(n-1)*d
D = np.zeros((n-1,n))
for k in range(n-1):
    D[k,k] = -1
    D[k,k+1] = 1
lam, V = np.linalg.eigh(D.T@D)
keep = lam>1e-10
lam = lam[keep]
V = V[:,keep]
c = D.T@np.ones(n-1)
ck = V.T@c
mode_identity = float(np.sum(ck**2/lam))
radius = length/(np.pi/2)
curvature = 1/radius

def solve(G, elements=100):
    dx = length/elements
    weights = np.full(elements, dx)
    weights[-1] *= .5
    A = np.diag(np.r_[np.full(elements-1,2.),1.])
    A += np.diag(np.full(elements-1,-1.),1)
    A += np.diag(np.full(elements-1,-1.),-1)
    root_w = np.sqrt(weights)
    spatial = A/dx/root_w[:,None]/root_w[None,:]
    p, Q = np.linalg.eigh(spatial)
    loads = Q.T@root_w
    if G is None:
        B_eff = np.full(elements,B_full)
        U = None
        ks = None
    elif G == 0:
        B_eff = np.full(elements,B0)
        U = np.zeros((n,elements))
        ks = 0.
    else:
        ks = G*b/d
        # Stable form avoids subtracting nearly equal large foundation terms.
        fraction = ks*lam[:,None]/(EA*p[None,:]+ks*lam[:,None])
        B_eff = B0+EA*h*h*np.sum(
            (ck**2/lam**2)[:,None]*fraction,axis=0)
        theta_modes = force*loads/(B_eff*p)
        U = V@((-ks*h*ck[:,None]/(
            EA*p[None,:]+ks*lam[:,None]))*theta_modes[None,:])
    theta_modes = force*loads/(B_eff*p)
    theta_free = (Q@theta_modes)/root_w
    theta = np.r_[0.,theta_free]
    tip = float(weights@theta_free)
    bending_gradient = np.diff(theta)/dx
    if G is None:
        axial = -y[:,None]*theta[None,:]
    else:
        axial = np.column_stack((np.zeros(n),(U@Q.T)/root_w[None,:]))
    slips = D@axial+h*theta[None,:]
    if ks is not None:
        q = ks*slips
    else:
        # Full-stick reaction obtained from layer axial force equilibrium.
        # V=F constant in this point-loaded, perfectly composite reference.
        q0 = force*EA*np.cumsum(y)[:-1]/B_full
        q = np.repeat(q0[:,None],elements+1,axis=1)
    strain = np.diff(axial,axis=1)/dx
    max_sigma = float(E*np.max(np.abs(strain)+(
        t/2*np.abs(bending_gradient))[None,:]))
    total_moment_at_first_element = float(
        -EA*y@strain[:,0]+B0*bending_gradient[0])
    layer_length = np.sqrt(EA/(G*b/d)) if G and G>0 else None
    lowest_length = layer_length/np.sqrt(lam[0]) if layer_length else None
    return {
        "G_Pa_introduced": G,
        "elements": elements,
        "tip_deflection_m":tip,
        "apparent_EI_N_m2":force*length**3/(3*tip),
        "ratio_to_perfect_reference_deflection":tip/(
            force*length**3/(3*B_full)),
        "max_interfacial_shear_Pa":float(np.max(np.abs(q))/b),
        "max_abs_rotation_rad":float(np.max(np.abs(theta))),
        "introduced_small_rotation_screen_abs_theta_le_0p1":bool(
            np.max(np.abs(theta))<=.1),
        "max_contact_slip_m": None if G is None else float(
            np.max(np.abs(slips))),
        "max_foil_axial_plus_local_bending_stress_Pa":max_sigma,
        "root_moment_at_first_element_N_m":total_moment_at_first_element,
        "root_expected_at_element_center_N_m":force*(length-dx/2),
        "slowest_axial_transfer_length_m":lowest_length,
        "status": "LINEAR_DIAGNOSTIC_ONLY; NOT_QUALIFIED_OR_SHEAR_FAILURE_SOLVE",
    }

states = [solve(g) for g in [0.,1e4,1e5,1.5e6,1e8,None]]
# Check discretization and physics identities meaningful to the model.
closed_form_tip = force*length**3/(3*B_full)
assert abs(mode_identity-(n-1))<1e-7
assert abs(B_full-(B0+EA*h*h*np.sum(ck**2/lam**2)))<1e-7
assert abs(states[-1]["tip_deflection_m"]/closed_form_tip-
           (1-1/(4*100**2)))<1e-8
assert all(states[j]["tip_deflection_m"]>=states[j+1][
    "tip_deflection_m"] for j in range(len(states)-1))
for s in states:
    assert abs(s["root_moment_at_first_element_N_m"]-s[
        "root_expected_at_element_center_N_m"])<1e-6
convergence = [solve(1.5e6,m) for m in [50,100,200]]
# Perfect-composite shear is determined by the HALF-section axial force.
qmax = force*EA*np.max(np.abs(np.cumsum(y)[:-1]))/B_full
tau = qmax/b
vacuum_dp = 100000.
mu = .3
ideal_friction_tau = mu*vacuum_dp
ideal_friction_force_limit = force*ideal_friction_tau/tau
# Conditional modulus needed by THIS fixed geometry, not a material result.
g_lo, g_hi = 1.5e6, 1e8
for _ in range(28):
    g_mid = (g_lo+g_hi)/2
    if solve(g_mid)["tip_deflection_m"]>.003:
        g_lo = g_mid
    else:
        g_hi = g_mid
clamp_pitch = .020
collar_normal = qmax*clamp_pitch/mu
result = {
  "scope": "INTRODUCED, uniform, straight, small-deflection laminate. No "
     "construction, fitted contact law, source recovery or physical experiment.",
  "inputs": {"layers":n,"E_Pa":E,"width_m":b,"foil_t_m":t,
    "gap_d_m":d,"length_m":length,"tip_load_N":force},
  "section": {"overall_height_m":height,"metal_mass_kg":n*rho_metal*b*t*length,
    "gap_mass_kg":(n-1)*rho_gap*b*d*length,
    "free_EI_N_m2":B0,"perfect_EI_N_m2":B_full,
    "ideal_stiffness_ratio":B_full/B0},
  "states": states,
  "conditional_G_for_3mm_tip_deflection_Pa":g_hi,
  "convergence_1p5MPa": [{
    "elements":s["elements"],"tip_deflection_m":s["tip_deflection_m"],
    "max_interfacial_shear_Pa":s["max_interfacial_shear_Pa"]}
    for s in convergence],
  "separate_perfect_stick_strength_screen":{
    "max_shear_flow_N_per_m":float(qmax),
    "max_interfacial_shear_Pa":float(tau),
    "introduced_mu":mu,"introduced_pressure_difference_Pa":vacuum_dp,
    "ideal_friction_capacity_Pa":ideal_friction_tau,
    "tip_force_limit_for_full_stick_N":float(ideal_friction_force_limit),
    "pitch_m":clamp_pitch,"collar_normal_force_at_critical_interface_N":
      float(collar_normal),
    "warning":"Capacity exceedance invalidates perfect stick; not a "
      "computed failed shape or an obstruction to other clamps/geometries."},
  "separate_low_force_forming_screen":{
    "unlocked_quarter_turn_radius_m":radius,
    "foil_outer_fiber_strain":t/(2*radius),
    "foil_outer_fiber_stress_Pa":E*t/(2*radius),
    "outer_minus_inner_foil_required_length_difference_m":
      float((y[-1]-y[0])*(np.pi/2)),
    "free_foil_forming_moment_N_m":B0*curvature,
    "free_foil_forming_elastic_energy_J":.5*B0*curvature**2*length,
    "warning":"No actual yield, wrinkling, edge, feed, end-slip, cross-section "
      "restraint, torsion, normal-contact, memory or life qualification."},
  "fourier_dimension_check":{
    "integral_abs_position_fourier_squared_df_dimensions":"length^2*time",
    "energy_in_joules_follows_without_calibration_and_mass_model":False,
    "scope":"Only a dimensional observation about the displayed squared-position "
      "spectrum integral, not a reanalysis of uncollected data or a rejection of "
      "the paper's measured static forces/displacements."},
  "not_supplied":[
    "Actual friction/cohesive tangent, fracture envelope or whole-contact gap",
    "Autonomous shape writing, three-dimensional load-bearing shape memory",
    "Holding-power loss safety, fault diagnosis, normal restraint or fatigue",
    "Common tools, preparation, capital or full-cycle manufacturing advantage"],
}
target=Path(__file__).with_suffix(".json")
target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"output":str(target),"states":[{
    "G_Pa":s["G_Pa_introduced"],"tip_mm":1000*s["tip_deflection_m"],
    "tau_kPa":s["max_interfacial_shear_Pa"]/1000}for s in states],
    "capacity_N":ideal_friction_force_limit,"collar_normal_N":collar_normal,
    "identities":"PASS","convergence_mm":[1000*s["tip_deflection_m"]
    for s in convergence]},sort_keys=True))
