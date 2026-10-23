"""Read-only independent node-ledger audit; no BVP or vector-kernel imports.
Cantera thermochemistry is a common source, not independent physical validation.
"""
from pathlib import Path
import hashlib, json, time, resource, sys
import numpy as np
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parent/'nitrogen_quench_recovery_20261021'))
from paper_model import gas_model
OUT=Path(__file__).resolve().parent
start=time.monotonic();g=gas_model();W=g.molecular_weights
ind=[g.species_index(s) for s in ['O2','N','O','NO','NO2']];nit=g.species_index('N2')
A=np.array([[g.n_atoms(i,e)*g.atomic_weight(e)/W[i] for i in range(6)] for e in range(g.n_elements)])
files=[BASE/'reactive_geometry_vector_checkpoint.npz']+sorted(BASE.glob('hot_*_checkpoint.npz'))+sorted(BASE.glob('radiating_*_checkpoint.npz'))
source_names=['reactive_geometry_vector.py','reactive_geometry_scalar_matched.py','reactive_average.py','hot_continuation.py','cold_end_radiation.py']
pins={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files+[BASE/s for s in source_names]}
rows=[]
for p in files:
 d=np.load(p);x=d['x'];z=d['y'];hs=[];rho=[];raws=[];elements=[];moles=[];cp=[];mu=[];kg=[]
 for off in [0,6]:
  Y=np.zeros((6,len(x)));Y[ind]=z[off:off+5];Y[nit]=1-Y.sum(axis=0);raws.append(Y);elements.append(A@Y)
  hh=[];rr=[];nn=[];cc=[];mm=[];kk=[]
  for j in range(len(x)):
   g.TPY=z[off+5,j]*1000,101325,Y[:,j]
   hh.append(g.enthalpy_mass);rr.append(g.density);cc.append(g.cp_mass);mm.append(g.viscosity);kk.append(g.thermal_conductivity)
   nn.append(sum(1000*g.Y[g.species_index(s)]/W[g.species_index(s)] for s in ['NO','NO2']))
  hs.append(np.array(hh));rho.append(np.array(rr));moles.append(np.array(nn));cp.append(np.array(cc));mu.append(np.array(mm));kg.append(np.array(kk))
 # x oriented hot flow; q_s=1e6 z[13], positive along x. G=1.
 invariant=hs[0]-hs[1]+2e6*z[13]
 duty=hs[0][0]-hs[1][0];retained=moles[0][-1]
 POR=.4;DP=.009525;G=1.
 dp=[];adv=[]
 for ph in range(2):
  # Ergun with superficial u=G/rho; gas holdup / mass flux, not a full cycle.
  grad=150*mu[ph]*(1-POR)**2/(POR**3*DP**2)*G/rho[ph]+1.75*(1-POR)/(POR**3*DP)*G**2/rho[ph]
  dp.append(float(np.trapezoid(grad,x)));adv.append(float(np.trapezoid(POR*rho[ph]/G,x)))
 rows.append({'checkpoint':p.name,'nodes':len(x),'hot_in_K':float(z[5,0]*1000),'hot_out_K':float(z[5,-1]*1000),'cold_out_K':float(z[11,0]*1000),'solid_peak_at_saved_nodes_K':float(z[12].max()*1000),'all_six_raw_Y_min':float(min(q.min() for q in raws)), 'raw_normalization_max_abs_error':float(max(abs(q.sum(axis=0)-1).max() for q in raws)),'N_O_mass_fraction_drift_max':float(max(abs(e-e[:,[0]]).max() for e in elements)),'local_energy_invariant_max_drift_J_kg':float(abs(invariant-invariant[0]).max()),'endpoint_energy_residual_with_axial_flux_J_kg':float(hs[0][0]-hs[0][-1]-hs[1][0]+hs[1][-1]-2e6*(z[13,-1]-z[13,0])), 'axial_flux_pair_export_J_kg':float(2e6*(z[13,-1]-z[13,0])),'heater_duty_J_kg':float(duty),'retained_NOx_mol_per_kg_fresh_feed':float(retained),'heater_MJ_per_mol_outlet_NOx':float(duty/retained/1e6),'hot_cold_gas_holdup_time_s':adv,'hot_cold_ergun_dp_Pa':dp,'holdup_scope':'One bed per phase; no purge model or valve/header dead volume. Ergun is an independent diagnostic at constant nominal pressure, not pressure-coupled rerun.'})
result={'source_hashes':pins,'equation_identity':'G*(h_hot-h_cold)+2*q_s is constant; equal hot/cold phase durations and zero end q_s imply hot enthalpy loss = cold enthalpy gain. Formation enthalpies included.','rows':rows,'wall_s':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'not_done':['No full BVP rerun','No finite-period reacting cycle','No captured-product or electrical SEC calculation','No independent physical thermochemistry validation']}
(OUT/'saved_ledgers.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
