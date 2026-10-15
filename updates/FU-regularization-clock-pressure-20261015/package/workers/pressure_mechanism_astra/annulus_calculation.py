"""Electromagnetic design calculation only; no Hg material performance is assumed.
Run with bundled Python (numpy). Units are SI except reported output labels.
"""
from pathlib import Path
import json, math
import numpy as np

OUT=Path(__file__).resolve().parent
MU0=4e-7*math.pi
A_IN,A_OUT,THICK=20e-6,40e-6,20e-6
J_GOAL=1e9  # proposed 1000 A/mm2 acceptance value, NOT measured material input
I_GOAL=J_GOAL*(A_OUT-A_IN)*THICK


def loop_field(points, radii, zs, currents, nphi=192):
    """Biot-Savart from circular filaments; numerically integrate azimuth."""
    phi=(np.arange(nphi)+.5)*(2*math.pi/nphi)
    co,si=np.cos(phi),np.sin(phi)
    rr=np.array(radii)[:,None]
    zz=np.array(zs)[:,None]
    xx=rr*co; yy=rr*si; zp=np.broadcast_to(zz,xx.shape)
    src=np.stack((xx,yy,zp),axis=-1).reshape(-1,3)
    dl=np.stack((-rr*si,rr*co,np.zeros_like(xx)),axis=-1)*(2*math.pi/nphi)
    weighted=dl*np.asarray(currents)[:,None,None]
    weighted=weighted.reshape(-1,3)
    result=[]
    for p in points:
        displacement=p-src
        distance=np.linalg.norm(displacement,axis=1)
        result.append(MU0/(4*math.pi)*np.sum(np.cross(weighted,displacement)/distance[:,None]**3,axis=0))
    return np.asarray(result)


def contour(rlo,rhi,zlo,zhi,n=120):
    corners=np.array([[rlo,0,zlo],[rhi,0,zlo],[rhi,0,zhi],[rlo,0,zhi]])
    pts=[];dls=[]
    for i in range(4):
        a,b=corners[i],corners[(i+1)%4]
        delta=(b-a)/n
        pts.extend(a+(np.arange(n)[:,None]+.5)*delta)
        dls.extend(np.tile(delta,(n,1)))
    return np.array(pts),np.array(dls)


def integrate_current(field,dls):
    # Orientation chosen below yields current magnitude with negative sign.
    return -float(np.sum(field*dls))/MU0

rlo,rhi,zlo,zhi=10e-6,50e-6,-20e-6,20e-6
pts,dls=contour(rlo,rhi,zlo,zhi)
perimeter=float(np.linalg.norm(dls,axis=1).sum())
# Uniform rectangular cross section discretized as parallel circular filaments.
ng=20
r=A_IN+(np.arange(ng)+.5)*(A_OUT-A_IN)/ng
z=-THICK/2+(np.arange(ng)+.5)*THICK/ng
rr,zz=np.meshgrid(r,z,indexing='ij')
rr,zz=rr.ravel(),zz.ravel()
cur=np.full(ng*ng,I_GOAL/(ng*ng))
field=loop_field(pts,rr,zz,cur)
center=loop_field(np.array([[0.,0.,0.],[0.,0.,15e-6]]),rr,zz,cur)
reconstructed=integrate_current(field,dls)
# Counterflow can yield a sizable center signal despite zero net winding current.
local_field=loop_field(pts,[25e-6,35e-6],[0.,0.],[.4,-.4])
local_center=loop_field(np.array([[0.,0.,0.]]),[25e-6,35e-6],[0.,0.],[.4,-.4])
# Uniform applied magnetic field makes exactly zero closed-contour contribution.
background=np.tile(np.array([0.,0.,.1]),(len(pts),1))
# Thin round-wire expression is only an inductance scale estimate for this thick ring.
rmean=(A_IN+A_OUT)/2
awire=math.sqrt(((A_OUT-A_IN)*THICK)/math.pi)
l_scale=MU0*rmean*(math.log(8*rmean/awire)-2)
ell=2*math.pi*rmean
vol=math.pi*(A_OUT*A_OUT-A_IN*A_IN)*THICK
facts={
 'scope':'Design calculation and identity sanity check, not experimental validation or material prediction.',
 'geometry_um':{'inner_radius':A_IN*1e6,'outer_radius':A_OUT*1e6,'thickness':THICK*1e6},
 'gross_cross_section_mm2':(A_OUT-A_IN)*THICK*1e6,
 'volume_nL':vol*1e12,
 'target_J_A_per_mm2':J_GOAL/1e6,
 'required_current_A':I_GOAL,
 'center_B_uniform_J_mT':float(center[0,2])*1e3,
 'B_5um_above_top_uniform_J_mT':float(center[1,2])*1e3,
 'ampere_contour_perimeter_um':perimeter*1e6,
 'ampere_reconstructed_A':reconstructed,
 'relative_discretization_error':abs(reconstructed-I_GOAL)/I_GOAL,
 'ampere_reconstructed_with_0p1T_A':integrate_current(field+background,dls),
 'zero_net_counterflow_center_mT':float(local_center[0,2])*1e3,
 'zero_net_counterflow_ampere_A':integrate_current(local_field,dls),
 '10uT_pointwise_field_error_current_bound_mA':perimeter*10e-6/MU0*1e3,
 '50uT_pointwise_field_error_current_bound_mA':perimeter*50e-6/MU0*1e3,
 'L_round_wire_scale_pH_not_calibration':l_scale*1e12,
 'loop_length_um':ell*1e6,
 'loop_voltage_at_1uV_per_cm_nV':ell*1e-4*1e9,
 'J_if_10pct_area_upper_uncertainty_A_per_mm2':I_GOAL/(1.1*(A_OUT-A_IN)*THICK)/1e6,
 'I_needed_with_10pct_area_upper_uncertainty_A':I_GOAL*1.1,
 'bound_avg_stress_Pa_if_total_support_force_3uN':A_OUT*3e-6/vol,
 'tomita_retained_fraction_of_baseline':.031/1.291,
 'tomita_retained_fraction_of_pressure_gain':.031/.156,
}
# This huge voltage sensitivity is CONDITIONAL on a calibrated, time-invariant L,
# fixed applied flux and no hidden coupled-current reservoirs. It is not claimed as
# an experimental bound from the paper or as a pointwise electric-field bound.
L_conservative=1e-9
loss=.01*I_GOAL
hold=86400.
facts['conditional_1nH_1pct_decay_24h']={
 'mean_loop_voltage_V':L_conservative*loss/hold,
 'mean_loop_E_V_per_m':L_conservative*loss/hold/ell,
 'linear_R_upper_ohm':L_conservative*math.log(1/.99)/hold,
 'warning':'Only lumped fixed-state circuit inference; direct persistence result is separate.'}
(OUT/'DESIGN_CALCULATION.json').write_text(json.dumps(facts,indent=2)+'\n')
print(json.dumps(facts,indent=2))
