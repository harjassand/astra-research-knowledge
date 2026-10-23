"""Small exact-rational diagnostics of inventory/energy closure, not a bed solver."""
from fractions import Fraction as F
from pathlib import Path
import json, time, resource, hashlib
P=Path(__file__).resolve().parent
start=time.monotonic()
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def ser(x):
 if isinstance(x,F):return {'fraction':str(x),'float':float(x)}
 if isinstance(x,dict):return {k:ser(v) for k,v in x.items()}
 if isinstance(x,list):return [ser(v) for v in x]
 return x
# Fixed pressure/volume, two-species A2/A model. R_i=(1,2), cv_i=(3,4).
m=F(2);T=F(100);Y=[F(1,2),F(1,2)];Ri=[F(1),F(2)];cvi=[F(3),F(4)];ufi=[F(0),F(5)]
u=[a*T+b for a,b in zip(cvi,ufi)];h=[a+r*T for a,r in zip(u,Ri)]
R=dot(Y,Ri);cv=dot(Y,cvi);cp=cv+R;um=dot(Y,u);hm=dot(Y,h)
Fin=F(1);Yin=[F(1),F(0)];hin=h[0];Q=F(100);omega=[-F(1,5),F(1,5)]
dY=[(Fin*(a-b)+w)/m for a,b,w in zip(Yin,Y,omega)]
dT=(Fin*(hin-hm)+Q-m*dot(h,dY))/(m*cp)
dm=-m*(dT/T+dot(Ri,dY)/R);Fout=Fin-dm
species_res=[dm*y+m*dy-(Fin*yi-Fout*y+w) for y,dy,yi,w in zip(Y,dY,Yin,omega)]
dU=um*dm+m*cv*dT+m*dot(u,dY);flux=Fin*hin-Fout*hm+Q
pressure_rate=dm/m+dT/T+dot(Ri,dY)/R
wrong_T=(Fin*(hin-hm)+Q)/(m*cp);wrong_dm=-m*(wrong_T/T+dot(Ri,dY)/R);wrong_out=Fin-wrong_dm
wrong_energy=um*wrong_dm+m*cv*wrong_T+m*dot(u,dY)-(Fin*hin-wrong_out*hm+Q)
wrong_pressure_if_equal_flow=F(300)*(dT/T+dot(Ri,dY)/R)
iso={'mass_kg':m,'temperature_K':T,'dY_dt':dY,'dT_dt_K_s':dT,'dm_dt_kg_s':dm,'outlet_mass_flow_kg_s':Fout,'species_residual_kg_s':species_res,'energy_storage_rate_W':dU,'boundary_plus_heat_W':flux,'energy_residual_W':dU-flux,'relative_pressure_derivative_s_inv':pressure_rate,'wrong_equal_flow_pressure_derivative_Pa_s':wrong_pressure_if_equal_flow,'wrong_omitted_composition_enthalpy_energy_residual_W':wrong_energy}
assert all(v==0 for v in species_res) and dU==flux and pressure_rate==0
assert Fout!=Fin and wrong_energy!=0 and wrong_pressure_if_equal_flow!=0
# Two fixed-volume gas cells + two solids. Signed interior flow must use donor.
# Species A2,B2,AB; reaction mass sources [-2r,-4r,+6r] conserve A/B atoms.
Y0=[F(1,2),F(1,4),F(1,4)];Y1=[F(1,4),F(1,2),F(1,4)]
Yleft=[F(1,3)]*3;Yright=[F(1,2),F(1,3),F(1,6)]
h0=F(13);h1=F(29);hleft=F(7);hright=F(5)
left=F(2,3);right=F(1,2);heat=[F(17),-F(11)];solidflux=F(9);external_solid_loss=F(3)
network=[]
for middle in [F(1,3),-F(1,3)]:
 donorY,donorh=(Y0,h0) if middle>=0 else (Y1,h1)
 rs=[F(1,7),F(1,11)];sources=[[-2*r,-4*r,6*r] for r in rs]
 ds0=[left*a-middle*b+w for a,b,w in zip(Yleft,donorY,sources[0])]
 ds1=[middle*a-right*b+w for a,b,w in zip(donorY,Y1,sources[1])]
 dUg0=left*hleft-middle*donorh+heat[0];dUg1=middle*donorh-right*h1+heat[1]
 dHs0=-heat[0]-solidflux;dHs1=-heat[1]+solidflux-external_solid_loss
 Etot=dUg0+dUg1+dHs0+dHs1;Eport=left*hleft-right*h1-external_solid_loss
 massres=sum(ds0)+sum(ds1)-(left-right)
 A=[F(1),F(0),F(1,3)];B=[F(0),F(1,2),F(1,3)]
 element_res=[dot(a,[x+y for x,y in zip(ds0,ds1)])-(left*dot(a,Yleft)-right*dot(a,Y1)) for a in [A,B]]
 assert Etot==Eport and massres==0 and element_res==[0,0]
 # A common bug: use wrong enthalpy on only one side of an interface.
 bad_internal_flux_res=middle*(h1-h0)
 network.append({'interior_signed_mass_flow':middle,'energy_residual':Etot-Eport,'mass_residual':massres,'element_residuals':element_res,'wrong_inconsistent_internal_enthalpy_flux_residual':bad_internal_flux_res})
# Analytic constant-P fixed-V heated vent, zero inflow, constant composition/cp.
# m*T=C; k=Q/(C*cp); T=T0 exp(k t),m=m0 exp(-k t).
# U=m cv T=C cv is constant, whereas Fout*h=Q exactly.
C=F(100);cp0=F(5);cv0=F(4);Q0=F(10);k=Q0/(C*cp0)
vent={'C_mT_kg_K':C,'rate_k_s_inv':k,'constant_internal_energy':C*cv0,'outflow_enthalpy_W':k*C*cp0,'heater_W':Q0,'identity_residual_W':k*C*cp0-Q0}
assert vent['identity_residual_W']==0
r={'scope':__doc__,'isobaric_cell':iso,'signed_interface_network':network,'analytic_heated_vent':vent,'all_exact_rational_gates_pass':True,'wall_s':time.monotonic()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cost_scope':'Python process only; CPU and host overhead unavailable; no numerical bed evolution or property package.'}
(P/'conservation_diagnostic.json').write_text(json.dumps(ser(r),indent=2)+'\n')
print(json.dumps(ser(r),indent=2))
