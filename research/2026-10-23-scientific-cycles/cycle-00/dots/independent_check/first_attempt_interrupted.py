"""Independent conserved-enthalpy Radau audit of one counterflow case.
Uses only original air.yaml thermochemical source, not original solver functions.
X is measured along hot flow; cold flows toward decreasing X.
State is hot mass fractions, Q [J/kg], friction drops [Pa], hot residence [s].
h_hot=h_quench-Q and h_cold=h_cold_out-Q enforce energy conservation algebraically.
"""
from pathlib import Path
import sys,json,time,hashlib
import numpy as np
import cantera as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
P=ct.one_atm; T0=300.; TH=3100.; TQ=2400.; D=.001; G=1.; L=.02; BETA=1e8
RTOL=1e-9; start=time.monotonic()
def gas():
 g=ct.Solution(str(ROOT/'sources/air.yaml')); g.transport_model='mixture-averaged';return g
g=gas(); c=gas(); g.TPX=T0,P,{'N2':.79,'O2':.21}; feed=g.Y.copy(); h0=g.enthalpy_mass; W=g.molecular_weights; ns=g.n_species
g.TP=TH,P;g.equilibrate('TP');Y0=g.Y.copy(); h_hot0=g.enthalpy_mass
ix=[g.species_index(s) for s in ['NO','NO2']]
no=lambda Y:float(1000*np.sum(Y[ix]/W[ix]))
# Independent high-accuracy Radau quench at the same prescribed cooling rate.
def quench_rhs(t,Y):
 g.TPY=TH-BETA*t,P,Y
 return g.net_production_rates*W/g.density
qsol=solve_ivp(quench_rhs,(0,(TH-TQ)/BETA),Y0,method='Radau',rtol=1e-10,atol=1e-14,max_step=(TH-TQ)/BETA/100)
assert qsol.success,qsol.message
Yq=qsol.y[:,-1];g.TPY=TQ,P,Yq;hq=g.enthalpy_mass
calls=[]
def integrate(Tcout):
 c.TPY=Tcout,P,feed; hc_out=c.enthalpy_mass
 def rhs(x,z):
  Y=z[:ns];Q=z[ns]
  g.HPY=hq-Q,P,Y;c.HPY=hc_out-Q,P,feed
  U=1/(D/(3.66*g.thermal_conductivity)+D/(3.66*c.thermal_conductivity))
  qprime=4*U*(g.T-c.T)/(D*G)
  return np.r_[g.net_production_rates*W/G,qprime,32*g.viscosity*G/(g.density*D**2),32*c.viscosity*G/(c.density*D**2),g.density/G]
 sol=solve_ivp(rhs,(0,L),np.r_[Yq,0.,0.,0.,0.],method='Radau',rtol=RTOL,atol=np.r_[np.full(ns,1e-14),1e-5,1e-7,1e-7,1e-12],dense_output=True,max_step=L/200)
 assert sol.success,sol.message
 residual=hc_out-sol.y[ns,-1]-h0
 calls.append({'Tcout_K':Tcout,'residual_J_kg':float(residual),'steps':len(sol.t)})
 return sol,residual,hc_out
# Narrow bracket centered on source output, but no imported RHS or states.
Tcout=brentq(lambda T:integrate(T)[1],2565.,2575.,xtol=1e-9,rtol=1e-13)
sol,residual,hco=integrate(Tcout)
xx=np.linspace(0,L,1001);z=sol.sol(xx);Th=[];Tc=[];Reh=[];Rec=[];flowc=[];balances=[];press_acc=[]
for k in range(xx.size):
 g.HPY=hq-z[ns,k],P,z[:ns,k];c.HPY=hco-z[ns,k],P,feed
 Th.append(g.T);Tc.append(c.T);Reh.append(G*D/g.viscosity);Rec.append(G*D/c.viscosity);flowc.append(c.density/G)
 balances.append(g.enthalpy_mass-c.enthalpy_mass-(hq-hco));press_acc.append(G**2/g.density)
Th=np.array(Th);Tc=np.array(Tc)
g.HPY=hq-z[ns,-1],P,z[:ns,-1];Yout=g.Y.copy();hout=g.enthalpy_mass
# Downstream uncredited cooling to contract delivery temperature, one stated rate.
TAIL_RATE=1e5; Ttail=g.T
if Ttail>T0:
 def tail_rhs(t,Y):
  g.TPY=Ttail-TAIL_RATE*t,P,Y
  return g.net_production_rates*W/g.density
 tail=solve_ivp(tail_rhs,(0,(Ttail-T0)/TAIL_RATE),Yout,method='Radau',rtol=RTOL,atol=1e-14,max_step=(Ttail-T0)/TAIL_RATE/100)
 assert tail.success,tail.message
 Ydel=tail.y[:,-1]
else:Ydel=Yout
# One-way consistency check: react cold feed along the calculated frozen T profile.
# This is not a fully coupled replacement and receives no energy/yield credit.
cold=gas()
def cold_rhs(s,Y):
 T=float(np.interp(L-s,xx,Tc));cold.TPY=T,P,Y
 return cold.net_production_rates*W/G
coldsol=solve_ivp(cold_rhs,(0,L),feed,method='Radau',rtol=1e-9,atol=1e-14,max_step=L/300)
assert coldsol.success,coldsol.message
cold.TPY=Tcout,P,coldsol.y[:,-1];cold_dh=cold.enthalpy_mass-hco
cold_eq=gas();cold_eq.HPY=hco,P,feed;cold_eq.equilibrate('HP')
baseline=json.loads((ROOT/'results/counterflow.json').read_text())
base=next(r for r in baseline['rows'] if r['Tq_K']==TQ and r['length_m']==L)
r={'method':'independent conserved enthalpy; Radau; not imported counterflow or cool',
 'scope':'one-case numerical audit, same favorable zero-wall-R model, no hardware validation',
 'cantera':ct.__version__,'rtol':RTOL,'Tq_K':TQ,'D_m':D,'G_kg_m2_s':G,'L_m':L,
 'quench_Y':dict(zip(g.species_names,map(float,Yq))),'quench_enthalpy_J_kg':hq,
 'Thout_K':float(Th[-1]),'Tc_out_K':float(Tcout),'cold_inlet_K':float(Tc[-1]),
 'cold_inlet_residual_K':float(Tc[-1]-T0),'cold_inlet_residual_J_kg':residual,
 'max_enthalpy_invariant_residual_J_kg':float(np.max(np.abs(balances))),
 'heat_balance_residual_J_kg':float((hq-hout)-(hco-h0)),
 'maximum_hot_temperature_K':float(Th.max()),'min_gap_K':float((Th-Tc).min()),
 'retained_mol_NOx_kg_exchanger_outlet':no(Yout),'retained_mol_NOx_kg_at_300K':no(Ydel),
 'uncredited_tail_cooling_K_s':TAIL_RATE,'recuperator_survival':no(Yout)/no(Yq),
 'gross_J_kg':h_hot0-h0,'recovered_J_kg':hco-h0,
 'net_gas_heat_MJ_mol_at_300K':(h_hot0-hco)/no(Ydel)/1e6,
 'pressure_drop_hot_friction_only_Pa':float(z[ns+1,-1]),'pressure_drop_cold_friction_only_Pa':float(z[ns+2,-1]),
 'hot_momentum_acceleration_correction_Pa':float(press_acc[-1]-press_acc[0]),
 'hot_residence_s':float(z[ns+3,-1]),'cold_residence_s':float(np.trapezoid(flowc,xx)),
 'hot_Re_range':[float(min(Reh)),float(max(Reh))],'cold_Re_range':[float(min(Rec)),float(max(Rec))],
 'min_hot_Y':float(z[:ns].min()),'hot_mass_drift':float(np.abs(z[:ns].sum(0)-1).max()),
 'cold_one_way_test':{'description':'React initially fresh feed along frozen cold temperature profile, no coupling or claimed output credit',
 'outlet_mol_NOx_kg':no(coldsol.y[:,-1]),'max_abs_mass_fraction_change':float(np.max(np.abs(coldsol.y[:,-1]-feed))),
 'extra_outlet_enthalpy_at_fixed_T_J_kg':float(cold_dh),'extra_enthalpy_fraction_of_recovery':float(cold_dh/(hco-h0)),
 'Y_out':dict(zip(cold.species_names,map(float,coldsol.y[:,-1]))),'adiabatic_equilibrium_T_at_same_h_K':float(cold_eq.T)},
 'source_comparison':{k:{'original':base[k],'independent':v,'difference':v-base[k]} for k,v in {
 'Thout_K':float(Th[-1]),'Tc_out_K':Tcout,'retained_mol_NOx_kg':no(Yout),'net_gas_heat_MJ_mol':(h_hot0-hco)/no(Yout)/1e6,
 'recovered_J_kg':hco-h0,'pressure_drop_hot_Pa':float(z[ns+1,-1])}.items()},
 'shooting_calls':calls,'wall_seconds':time.monotonic()-start,
 'profile':{'x_m':xx.tolist(),'Th_K':Th.tolist(),'Tc_K':Tc.tolist(),'Q_J_kg':z[ns].tolist(),'NOx_mol_kg':[no(y) for y in z[:ns].T]}}
(OUT/'one_case_result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['profile','shooting_calls','quench_Y']},indent=2))
