"""Admission calculation for recuperated, optically gated frontal polymerization.
All outputs are model predictions, not measurements of photoinhibited resin.
Kinetics: https://par.nsf.gov/servlets/purl/10435013 Table 1.
"""
import math, json
from scipy.integrate import quad
A, E, R = 8.55e15, 110750.0, 8.314462618
kappa, rho, cp, H = .15, 980., 1600., 350000.
n, m, C, ac = 1.72, .77, 14.48, .41
f=lambda a:(1-a)**n*a**m/(1+math.exp(C*(a-ac)))
F=lambda lo,hi:quad(lambda a:1/f(a),lo,hi,epsabs=1e-10,epsrel=1e-10)[0]
k=lambda T:A*math.exp(-E/(R*T))
a0,a_off,a_on=.05,.06,.90
I_off,I_on=F(a0,a_off),F(a0,a_on)
Tf=473.15
hold=100.
rows=[]
for TbC in (25,60,80,100,120,150,180,200):
 Tb=TbC+273.15
 off_time=I_off/k(Tb)
 rows.append(dict(bath_C=TbC,seconds_to_1_percent_unwanted_cure=off_time,
                  inhibition_factor_for_100s=max(1.,hold/off_time),
                  thermal_rate_contrast=k(Tf)/k(Tb),
                  startup_heat_J_per_liter=rho*cp*(Tb-298.15)*.001))
alpha=kappa/(rho*cp)
diffusion=[]
for a_um in (1,10,100,1000):
 a=a_um*1e-6
 diffusion.append(dict(feature_um=a_um,thermal_equilibration_seconds=a*a/alpha,
                       maximum_inhibitor_diffusivity_for_90pct_modulation_at_100s=-math.log(.9)*a*a/(math.pi**2*hold),
                       voxels_in_10cm_cube=round((.1/a)**3),minimum_binary_pattern_bytes=round((.1/a)**3)/8))
out=dict(parameters=dict(A=A,E=E,kappa=kappa,rho=rho,cp=cp,reaction_enthalpy_J_per_kg=H,
                          initial_cure=a0,off_cure_limit=a_off,on_cure_target=a_on,front_temperature_K=Tf),
         cure_coordinate_on=I_on,cure_coordinate_off=I_off,
         minimum_coheated_inhibition_factor=I_on/I_off,
         maximum_inhibitor_diffusivity_at_10um_for_same_0p51s_coheated_cure=-math.log(.9)*(10e-6)**2/(math.pi**2*(I_on/k(Tf))),
         on_cure_time_at_200C=I_on/k(Tf),thermal_diffusivity=alpha,
         chemical_heat_J_per_liter=rho*H*.001,
         preinhibition_optical_dose_J_per_cm2=.030*180,
         photoinhibition_energy_J_per_liter_at_1p3mm_thickness=.030*180/(.13)*1000,
         photoinhibition_energy_J_per_liter_at_10um_and_half_volume_inhibited=.030*180/.001*1000*.5,
         slice_thickness_m_where_half_volume_inhibition_equals_reaction_heat=(.030*180*1e4*.5)/(rho*H),
         bath_sweep=rows,resolution_sweep=diffusion)
print(json.dumps(out,indent=2))
with open(__import__('pathlib').Path(__file__).with_name('results.json'),'w') as f: json.dump(out,f,indent=2)
