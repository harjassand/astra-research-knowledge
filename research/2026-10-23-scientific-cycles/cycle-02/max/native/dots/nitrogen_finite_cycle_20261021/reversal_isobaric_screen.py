"""Inventory-conserving isobaric one-way cascade admissibility at reversal.
Negative face flow invalidates this one-way upwind closure; it is not physical
impossibility. Actual transient may backflow or change pressure.
"""
import sys,json,time,resource
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent;S=R.parent/'nitrogen_regenerator_20261021';sys.path.insert(0,str(S/'vector_kernel'));from kernel import Kernel
K=Kernel();W=K.W if hasattr(K,'W') else np.array([28.014,31.998,14.007,15.999,30.006,46.005])
# pin native molecular weights and input ordering
sys.path.insert(0,str(R.parent/'nitrogen_quench_recovery_20261021'));from paper_model import gas_model
g=gas_model();W=g.molecular_weights;idx=[g.species_index(s) for s in ['O2','N','O','NO','NO2']];ni=g.species_index('N2')
g.TPX=300,101325,{'N2':.79,'O2':.21};Yfeed=g.Y;hfeed=g.enthalpy_mass;g.TPY=2700,101325,Yfeed;g.equilibrate('TP');Yhot=g.Y;hhot=g.enthalpy_mass
z=np.load(S/'radiating_2700_checkpoint.npz');N=80;L=.1;dx=L/N;x=(np.arange(N)+.5)*dx;y=np.array([np.interp(x,z['x'],r) for r in z['y']]);Ts=1000*y[12];por=.4;dp=.009525

def full(v):
 a=np.zeros((6,v.shape[1]));a[idx]=v;a[ni]=1-v.sum(0);return a

def phase(Y,T,solid,Yin,hin):
 r=K.evaluate(T,Y);rho=r['rho'];cp=r['cp'];hs=r['h_species'];h=r['enthalpy'];mu=r['viscosity'];kg=r['conductivity'];Pr=cp*mu/kg
 # Frozen flow G1 films only for admissibility diagnostic; actual model must use local flow.
 Uv=(2+1.1*(dp/mu)**.6*Pr**(1/3))*kg/dp*6*(1-por)/dp
 flows=[1.];dY=np.zeros_like(Y);dT=np.zeros(N);drho=np.zeros(N);bad=[]
 for j in range(N):
  Gin=flows[-1];yu=Yin if j==0 else Y[:,j-1];hu=hin if j==0 else h[j-1]
  dY[:,j]=Gin/(por*dx*rho[j])*(yu-Y[:,j])+r['mass_production'][:,j]/rho[j]
  dh=Gin/(por*dx*rho[j])*(hu-h[j])+Uv[j]*(solid[j]-T[j])/(por*rho[j])
  dT[j]=(dh-np.dot(hs[:,j],dY[:,j]))/cp[j]
  drho[j]=-rho[j]*(dT[j]/T[j]+np.sum(dY[:,j]/W)/np.sum(Y[:,j]/W))
  flows.append(Gin-por*dx*drho[j])
  if flows[-1]<0:bad.append(j)
 species_storage=por*dx*np.sum(rho*dY+Y*drho,axis=1)
 balance=Yin-flows[-1]*Y[:,-1]+por*dx*r['mass_production'].sum(axis=1)
 energy_storage=por*dx*np.sum(drho*h+rho*(cp*dT+(hs*dY).sum(axis=0)))
 external=hin-flows[-1]*h[-1]+dx*np.sum(Uv*(solid-T))
 return {'face_flows':list(map(float,flows)),'negative_faces':bad,'outflow_kg_m2_s':float(flows[-1]),'min_flow':float(min(flows)),'max_flow':float(max(flows)),'species_ledger_max_abs':float(max(abs(species_storage-balance))),'energy_ledger_abs_W_m2':float(abs(energy_storage-external)),'mass_storage_kg_m2_s':float(por*dx*drho.sum()),'max_abs_temperature_rate_K_s':float(max(abs(dT)))}
t=time.monotonic();YH=full(y[:5]);YC=full(y[6:11]);out={
'hot_profile_under_hot_flow':phase(YH,1000*y[5],Ts,Yhot,hhot),
'cold_profile_under_cold_flow':phase(YC[:,::-1],1000*y[11,::-1],Ts[::-1],Yfeed,hfeed),
'previous_hot_bed_becomes_cold':phase(YH[:,::-1],1000*y[5,::-1],Ts[::-1],Yfeed,hfeed),
'previous_cold_bed_becomes_hot':phase(YC,1000*y[11],Ts,Yhot,hhot)}
r={'scope':__doc__,'N':N,'rows':out,'wall_s':time.monotonic()-t,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(R/'reversal_isobaric_screen.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:{f:v for f,v in v.items() if f!='face_flows'} for k,v in out.items()},indent=2))
