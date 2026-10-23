"""Independent saved-state conservation/reset receipt. No trajectory integration."""
from pathlib import Path
import numpy as np, json, hashlib, time, resource, sys
start=time.monotonic(); root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'thermo_helper'))
from helper import ThermoKernel
K=ThermoKernel(); out={}; hashes={}
def load(name):
 p=root/name; hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest(); return np.load(p)
N=12; M=25; H=12; dx=.1/N; v=np.full(M,.4*dx); v[H]=.1; C=2.5e6
W=K.W; yf=np.r_[.79*W[0],.21*W[1],0,0,0,0];yf/=yf.sum(); ei=K.evaluate(2700,yf)['e_species'][:,0]
def quantities(s):
 q=s[:6*M].reshape(6,M); mass=q@v; gas=float(s[6*M:7*M]@v); solid=float(C*dx*1000*s[7*M:7*M+2*N].sum()/1e6)
 return mass,gas,solid
states={}
for name in ['reacting_inventory_checkpoint.npz','reacting_inventory_resume_T4_checkpoint.npz']:
 z=load(name);s=z['state']; s0=z['initial'];states[float(z['t'])]=s
 mass,gas,solid=quantities(s); m0,g0,so0=quantities(s0);l=s[-9:]
 out[name]={'time_s':float(z['t']),'mass_kg_m2':mass.tolist(),'gas_energy_MJ_m2':gas,'solid_energy_MJ_m2':solid,'energy_residual_MJ_m2':gas+solid-g0-so0-l[0]+l[1]-l[2]+l[3],'mass_residual_kg_m2':float(sum(mass-m0)-l[4]),'header_energy_residual_J_m3':float(s[6*M+H]*1e6-s[:6*M].reshape(6,M)[:,H]@ei),'hostile_omit_solid_storage_energy_residual_MJ_m2':float(gas-g0-l[0]+l[1]-l[2]+l[3]),'hostile_omit_radiation_residual_MJ_m2':float(gas+solid-g0-so0-l[0]+l[1]-l[2])}
s=states[4.];old=states[2.];a=quantities(s);b=quantities(old);d=s[-9:]-old[-9:]
out['matching_phase_t2_t4']={'solid_reset_max_K':float(np.max(abs(s[7*M:7*M+2*N]-old[7*M:7*M+2*N]))*1000),'pointwise_species_density_reset_max_kg_m3':float(np.max(abs(s[:6*M]-old[:6*M]))),'pointwise_gas_energy_density_reset_max_J_m3':float(np.max(abs(s[6*M:7*M]-old[6*M:7*M]))*1e6),'aggregate_species_reset_max_kg_m2':float(np.max(abs(a[0]-b[0]))),'gas_energy_change_MJ_m2':a[1]-b[1],'solid_energy_change_MJ_m2':a[2]-b[2],'positive_heater_MJ_m2':float(d[0]),'net_export_NOx_mol_m2':float(d[5]),'heat_MJ_per_export_mol':float(d[0]/d[5])}
# Read only completed immutable blow files at this finite checkpoint.
for phase in [4,5]:
 name=f'reacting_inventory_raw_T8_blow_{phase}.npz'
 if not (root/name).exists(): continue
 z=load(name);pmin=1e99;pmax=-1e99; inletback=0;maxneg=0;clamps=0; hdr=0
 for t,s in zip(z['t'],z['state'].T):
  q=s[:6*M].reshape(6,M); rho=q.sum(0);u=s[6*M:7*M].copy()*1e6;u[H]=q[:,H]@ei
  r=K.evaluate_rho_u(rho,u,q/rho,trial_clamp=True);P=r['pressure'];pmin=min(pmin,float(min(P)));pmax=max(pmax,float(max(P)));clamps+=np.count_nonzero(r['diagnostics']['energy_clamped']);hdr=max(hdr,abs(s[6*M+H]*1e6-u[H]))
  target=phase%2;alpha=(1-target)+(2*target-1)*min(1,max(0,(float(t)-phase)/.02))
  # Ambient ingress possible iff connected outlet cell is subambient.
  inletback+=bool((alpha>0 and P[0]<101325-1e-7) or (alpha<1 and P[-1]<101325-1e-7))
 out[name]={'accepted_states':len(z['t']),'pressure_min_Pa':pmin,'pressure_max_Pa':pmax,'ambient_backflow_states':inletback,'energy_clamps':int(clamps),'min_species_density_kg_m3':float(z['state'][:6*M].min()),'header_energy_residual_max_J_m3':float(hdr)}
for name in ['reacting_inventory.py','reacting_inventory_clipped_transport.py','reacting_inventory_first_two_blows.py','thermo_helper/helper.py','independent_formulation/REPORT.md']:
 hashes[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
out['resources']={'wall_seconds':time.monotonic()-start,'peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'no_trajectory_replayed':True,'cost_boundary':'Process wall/RSS only; no CPU or host overhead measured.'}
out['source_sha256']=hashes
(root/'independent_transient_check/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
