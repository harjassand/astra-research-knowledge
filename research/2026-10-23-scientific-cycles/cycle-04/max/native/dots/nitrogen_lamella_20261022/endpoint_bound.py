"""Conditional thermochemical endpoint ceiling, not a quench-kinetics theorem.
Closed form stable-species ceiling at a maximum T; no fitted mixing parameter.
"""
from pathlib import Path
import sys,importlib.util,json,time,resource,hashlib
import numpy as np
from scipy.optimize import brentq
st=time.monotonic();R=Path(__file__).resolve().parent;root=R.parent
p=root/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py';sp=importlib.util.spec_from_file_location('signed_bound',p);mm=importlib.util.module_from_spec(sp);sp.loader.exec_module(mm);K=mm.SignedTrialKernel()
hotpath=root/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz';coldpath=root/'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz'
yh=np.load(hotpath)['hot_Y'];ycraw=np.load(coldpath)['return_Y'];yc=np.maximum(ycraw,0);yc/=yc.sum();ratio=.85;P0=101325.;W=K.W/1000;Rg=K.R/1000

def therm(T):
 c,h,s=K.thermochemistry(np.array([T]));hi=h[:,0]*Rg*T;return hi,hi-Rg*T

def energy(T,Y,kind):return float((Y/W)@therm(T)[kind])
n=(yh+ratio*yc)/W;mass=1+ratio;Y=n*W/mass;atoms=np.array([[2,0,1,0,1,1],[0,2,0,1,1,2]])@n
ns=n.copy();ns[0]+=.5*ns[2];ns[1]+=.5*ns[3];ns[2:4]=0;Ys=ns*W/mass;nox=n[4:6].sum();Tc=1700.;rows=[]
for kind,name in enumerate(['prescribed_pressure_enthalpy','rigid_volume_internal_energy']):
 target=energy(2700,yh,kind)+ratio*energy(300,yc,kind);tf=brentq(lambda T:mass*energy(T,Y,kind)-target,300,3000);ts=brentq(lambda T:mass*energy(T,Ys,kind)-target,300,3000)
 ei=therm(Tc)[kind];base=.5*atoms[0]*ei[0]+.5*atoms[1]*ei[1];a=ei[4]-.5*ei[0]-.5*ei[1];b=ei[5]-ei[4]-.5*ei[1]
 assert a>0 and b<0
 cases=[]
 for fac in [1.,1.01,1.05,1.1]:
  xmax=min(fac*nox,atoms.min());maxe=base+xmax*a;cases.append({'max_NOx_fraction_of_initial_packet':fac,'maximum_stable_energy_J_per_kg_fresh_at_1700':float(maxe),'minimum_required_heat_export_J_per_kg_fresh':float(max(0,target-maxe))})
 rows.append({'contract':name,'initial_energy_J_kg_fresh':target,'frozen_composition_mixed_T_K':tf,'radicals_recombined_without_NOx_loss_T_K':ts,'NO_formation_increment_J_mol':float(a),'NO2_increment_relative_to_NO_J_mol':float(b),'NOx_required_mol_per_kg_fresh_for_zero_heat_export_stable_cap':float((target-base)/a),'initial_packet_NOx_mol_per_kg_fresh':float(nox),'required_fractional_NOx_increase':float((target-base)/a/nox-1),'ceilings':cases})
# Initial fixed-volume packet and frozen final pressure of the rigid model.
v0=K.R/P0*(2700*np.sum(yh/K.W)+ratio*300*np.sum(yc/K.W));pf=Rg*rows[1]['frozen_composition_mixed_T_K']*n.sum()/v0
out={'scope':__doc__,'ratio':ratio,'initial_packet_atoms_mol_kg_fresh':atoms.tolist(),'initial_radical_moles_kg_fresh':n[2:4].tolist(),'cold_roundoff_projection_L1':float(sum(abs(yc-ycraw))),'rigid_frozen_final_pressure_Pa':float(pf),'rows':rows,'proof':'For stable species N2,O2,NO,NO2, set x=nNO+nNO2,z=nNO2. At Tcap energy=Ebase+a*x+b*z; a>0,b<0. Thus max occurs at largest admitted x and z=0, subject to atom feasibility. Positive species heat capacity makes any field with T<=Tcap no larger. This ceiling is conditional on radical caps and NOx amount; it does not forbid additional useful NO formation or stored radicals.','limitations':['Molecular/kinetic transport and real hardware not solved here.','Both pressure-work contracts explicit; not interchangeable.','N2O absent; if admitted the feasible species set and ceiling must be rebuilt.','No radical inventory is permitted in stable-species ceiling; finite radical tolerance needs its own extension.','Coefficients evaluated in float64 from pinned NASA source, not outward-rounded formal interval arithmetic.'],'inputs':{str(hotpath.relative_to(root)):hashlib.sha256(hotpath.read_bytes()).hexdigest(),str(coldpath.relative_to(root)):hashlib.sha256(coldpath.read_bytes()).hexdigest()},'wall_s':time.monotonic()-st,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(R/'endpoint_bound.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
