"""Steady-flow algebraic nozzle/reset screen, NOT a flow or chemical-kinetic trajectory.
Declared ideal-gas NASA frozen-COMPOSITION, internally equilibrated caloric
reference. Actual rapid expansion need not maintain mode equilibrium.
"""
from pathlib import Path
import sys,json,time,resource,hashlib
import numpy as np
from scipy.optimize import brentq,linprog
D=Path(__file__).resolve().parent;ROOT=D.parents[1]
sys.path.insert(0,str(ROOT/'nitrogen_finite_cycle_20261021/thermo_helper'))
from helper import ThermoKernel
K=ThermoKernel();start=time.monotonic();P0=101325.;T0=2700.;cap=1700.
src=ROOT/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz'
Y=np.load(src)['hot_Y'];W=K.W/1000.; R=K.R*np.sum(Y/K.W)
def props(T):
 cp,h,s=K.thermochemistry(np.array([T]));return float(Y@(cp[:,0]*K.R/K.W)),float(Y@(h[:,0]*K.R*T/K.W)),float(Y@(s[:,0]*K.R/K.W))
h0=props(T0)[1];s0=props(T0)[2];hc=props(cap)[1];rows=[]
for Ts in [1700.,1200.,1000.,800.,500.]:
 cp,hs,ss=props(Ts);Ps=P0*np.exp((ss-s0)/R);u=np.sqrt(2*(h0-hs));rho=Ps/(R*Ts);j=rho*u;mom=Ps+j*u;mach=u/np.sqrt(cp/(cp-R)*R*Ts)
 # Fixed-composition normal shock: mass/momentum/total enthalpy conserved.
 def temp(v):return (mom/j-v)*v/R
 def energy(v):return props(temp(v))[1]+v*v/2-h0
 # Find subsonic root other than incoming u, keep thermochemistry >=200K.
 grid=np.linspace(.02*u,.999999*u,1000);brackets=[]
 for a,b in zip(grid[:-1],grid[1:]):
  if min(temp(a),temp(b))>=200 and max(temp(a),temp(b))<=3500 and energy(a)*energy(b)<0:brackets.append((a,b))
 if not brackets:raise RuntimeError('No admissible shock root')
 v2=brentq(energy,*brackets[0]);T2=temp(v2);P2=mom-j*v2
 # Isentropic total pressure from state after normal shock. Real diffuser loss >=0.
 P02=P2*np.exp((props(T0)[2]-props(T2)[2])/R)
 recovery=[]
 for r in [.85,.89]:
  hr=hs+r*(h0-hs);Tr=brentq(lambda t:props(t)[1]-hr,Ts,T0)
  recovery.append({'r':r,'adiabatic_recovery_temperature_K':Tr})
 rows.append({'static_T_K':Ts,'static_P_Pa':Ps,'velocity_m_s':u,'Mach_caloric_reference':mach,'kinetic_J_kg':u*u/2,'normal_shock_T_K':T2,'normal_shock_P_Pa':P2,'postshock_total_P_Pa':P02,'normal_shock_energy_residual_J_kg':energy(v2),'normal_shock_entropy_increase_J_kgK':props(T2)[2]-ss-R*np.log(P2/Ps),'r_max_for_passive_wall_at_cap':(hc-hs)/(h0-hs),'recovery_temperature_examples':recovery,'cold_compress_cost_if_cool_at_static_pressure_J_kg':R*300*np.log(P0/Ps),'cold_compress_cost_if_ideal_diffuse_after_shock_J_kg':R*300*np.log(P0/P02)})
# Complete reset endpoint LP: moles/kg fresh, atoms exact per saved float.
A=np.array([[2,0,1,0,1,1],[0,2,0,1,1,2]],float);n0=Y/W;atoms=A@n0;Nhot=n0[4]+n0[5]
_,hh,_=K.thermochemistry(np.array([cap]));hmol=hh[:,0]*(K.R/1000)*cap
C=np.array([[0,0,0,0,1,1],[0,0,0,0,-1,-1]],float);b=np.array([1.01*Nhot,-.99*Nhot])
bounds=[(0,None),(0,None),(0,1e-7),(0,.003),(0,None),(0,None)]
lp=linprog(-hmol,A_ub=C,b_ub=b,A_eq=A,b_eq=atoms,bounds=bounds,method='highs');assert lp.success
min_export=h0+lp.fun
# Free pressure is not assumed: two different routes, not additive bills.
result={'scope':__doc__,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'initial_hot_Y':Y.tolist(),'hot_T_K':T0,'hot_P_Pa':P0,'Rmix_J_kgK':R,'hot_enthalpy_J_kgfresh':h0,'same_composition_relaxed_cap_enthalpy_J_kgfresh':hc,'same_composition_min_stagnation_heat_or_work_export_J_kgfresh':h0-hc,'nozzle_rows':rows,'endpoint_lp':{'contract':'Six species N2,O2,N,O,NO,NO2. One kg original fresh; same N/O atom totals; final all modes relaxed, negligible kinetic energy; T<=1700 K; NO+NO2 between99% and101% hot count; N<=1e-7mol/kgfresh, O<=.003mol/kgfresh. Species and radiation/work exported otherwise must be explicitly counted.','initial_NOx_mol_kgfresh':Nhot,'final_mol_kgfresh':lp.x.tolist(),'max_final_enthalpy_at_1700_J_kgfresh':-lp.fun,'minimum_total_heat_plus_shaft_work_export_before_rest_J_kgfresh':min_export,'atom_residual':(A@lp.x-atoms).tolist(),'primal_objective':lp.fun,'equality_dual':lp.eqlin.marginals.tolist(),'inequality_dual':lp.ineqlin.marginals.tolist(),'lower_dual':lp.lower.marginals.tolist(),'upper_dual':lp.upper.marginals.tolist(),'enthalpy_J_mol':hmol.tolist(),'atom_matrix':A.tolist(),'atom_rhs':atoms.tolist(),'count_matrix':C.tolist(),'count_rhs':b.tolist()},'limits':['No nozzle geometry, kinetics, heat transfer coefficient, wall cooling system, finite area or useful NO retention is admitted.','The ideal-gas equilibrium internal-mode algebraic path is not a justified rapid nonequilibrium path. It provides a transparent ordinary gas-dynamic reference only.','Recovery factors .85 and .89 are low-temperature air illustrative correlations, not measured reacting-air bounds. The r threshold, not transplanting those correlations, is the reusable admission test.','Normal shock plus ideal diffuser/cold compressor and cooling at static pressure are distinct hypothetical routes. Do not add the two listed compressor costs or treat either as a universal lower bound over all cooling/diffuser designs.','Steady-flow stagnation-enthalpy transfer inequality is closure-independent within stated reset/species/inventory assumptions; it is not irrecoverable loss. A closed batch requires internal energy plus all boundary work. Numerical NASA coefficients and LP floating arithmetic are not rigorous physical uncertainty intervals.','No net electrical or fertilizer SEC, no new NO production and no physical exclusion of cooled nozzles/regeneration established.'],'elapsed_s':time.monotonic()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
