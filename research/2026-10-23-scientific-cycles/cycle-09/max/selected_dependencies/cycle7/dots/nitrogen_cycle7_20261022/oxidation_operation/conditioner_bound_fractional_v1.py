"""Exact-rational finite-volume bounds under an evaluated ambient reaction model.
Endpoint monotonicity bounds each transformed integration panel. No ODE solver.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,resource,hashlib,math
start=time.perf_counter();p=Path(__file__).parent; inp=json.loads((p/'input.json').read_text())
T=F(inp['T_K']);R=F(inp['R_J_mol_K']);P=F(inp['pressure_Pa']);NA=F(inp['Avogadro'])
k=F(inp['event_k_cm6_molecule2_s'])*NA**2/F(10**12)
flow=F(inp['standard_flow_L_min'])/F(inp['declared_standard_molar_volume_L_mol'])/60
C=P/(R*T)
def f(u,a,b,s):
 x=1-1/u
 return (1-s*a*x)**3/(b-a*x/2)
def integrate_bounds(a,b,s,X,n):
 # d[(1-saX)^3/(b-aX/2)]/dX has sign .5-3sb+saX.
 d0=F(1,2)-3*s*b;d1=d0+s*a*X
 assert d0*d1>0
 U=1/(1-X);du=(U-1)/n
 vals=[f(1+i*du,a,b,s) for i in range(n+1)]
 low=du*sum(min(vals[i],vals[i+1]) for i in range(n))
 high=du*sum(max(vals[i],vals[i+1]) for i in range(n))
 return low,high
rows=[]
for point in inp['points']:
 a=F(point['initial_NO_fraction']);b=F(inp['oxygen_feed_fraction'])-a/2
 for xs in inp['conversion_targets']:
  X=F(xs);pref=flow/(2*k*C**3*a)
  allD=integrate_bounds(a,b,F(1),X,inp['quadrature_intervals'])
  noD=integrate_bounds(a,b,F(1,2),X,inp['quadrature_intervals'])
  # Dimer extent may vary arbitrarily along the flow. Pointwise total-flow bracket suffices.
  lower=pref*allD[0];upper=pref*noD[1]
  finerD=integrate_bounds(a,b,F(1),X,2*inp['quadrature_intervals']);finer0=integrate_bounds(a,b,F(1,2),X,2*inp['quadrature_intervals'])
  assert lower<=pref*finerD[0]<=pref*finer0[1]<=upper
  cstr=[pref*X*(1-s*a*X)**3/((1-X)**2*(b-a*X/2)) for s in [F(1),F(1,2)]]
  assert cstr[0]>upper
  # Report reliability sensitivity, NOT an exact rational enclosure for the exponential.
  factor=10**.2
  rows.append({**point,'conversion':float(X),'inlet_O2_fraction':float(b),'PFR_volume_L_evaluated_k_bracket':[float(1000*lower),float(1000*upper)],'dimer_model_relative_spread_upper':float(upper/lower-1),'quadrature_enclosure_relative_width_no_dimer':float(noD[1]/noD[0]-1),'quadrature_enclosure_relative_width_all_dimer':float(allD[1]/allD[0]-1),'CSTR_volume_L_evaluated_k_bracket':[float(1000*v) for v in cstr],'PFR_volume_L_IUPAC_reliability_sensitivity':[float(1000*lower)/factor,float(1000*upper)*factor],'oxidized_N_mol_s':float(flow*a*X),'unreacted_NO_mol_s':float(flow*a*(1-X)),'outlet_NO_fraction_bound':[float(a*(1-X)/(1-a*X/2)),float(a*(1-X)/(1-a*X))]})
# Same model at new pressure would give V~P^-3, but no high-pressure model admission.
# Reversible isothermal compression of all cooled original gas, NOT jets or sample stream.
compress={str(r):float(flow*R*T)*math.log(r) for r in [1.1,1.5,2,5,10]}
out={'scope':inp['scope'],'inputs_sha256':hashlib.sha256((p/'input.json').read_bytes()).hexdigest(),'F_original_mol_s':float(flow),'k_event_m6_mol2_s':float(k),'rate_convention':'NO sink=2*k*c_NO^2*c_O2','rows':rows,'conditional_reversible_isothermal_compression_W':compress,'compression_scope':'Model lower work, all postreactor20SLM, no expander credit, real work greater; high pressure kinetics and pressure vessel unqualified','elapsed_s':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(p/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
