"""Bounded independent saved-path audit: no time integration or trajectory write.
Full finite-face Soret + Dufour entropy on 81 sampled saved states per grid.
Strictly nonpositive endpoints are excluded from the finite-log check, not floored.
"""
from pathlib import Path
import hashlib, importlib.util, json, sys, time
import numpy as np
START=time.monotonic(); OUT=Path(__file__).resolve().parent; D=OUT.parent; ROOT=D.parent
p=ROOT/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py'
spec=importlib.util.spec_from_file_location('independent_signed',p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m); K=m.SignedTrialKernel()
sys.path.insert(0,str(D/'transport')); from molecular_transport import BinaryDiffusion, maxwell_stefan_flux
sys.path.insert(0,str(D/'transport/soret_extension')); from soret_dufour import schur_ratio
sys.path.insert(0,str(ROOT/'nitrogen_finite_cycle_20261021/thermo_helper')); from validate import native_corrected
gas=native_corrected(K);gas.transport_model='multicomponent';bd=BinaryDiffusion();P=101325.;Ri=K.R/K.W;Wmol=K.W/1000
sources=[p,ROOT/'nitrogen_finite_cycle_20261021/thermo_helper/helper.py', ROOT/'nitrogen_finite_cycle_20261021/thermo_helper/cache.npz', ROOT/'nitrogen_finite_cycle_20261021/thermo_helper/manifest.json', D/'resolve_lamella.py',D/'transport/molecular_transport.py',D/'transport/soret_extension/soret_dufour.py',D/'exact_endpoint_certificate.py',D/'exact_endpoint_certificate.json']
hotp=ROOT/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz';coldp=ROOT/'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz';sources +=[hotp,coldp]
yh=np.load(hotp)['hot_Y'];yc=np.maximum(np.load(coldp)['return_Y'],0);yc/=yc.sum()
nh=float(np.sum(yh[4:]/Wmol[4:]));nc=float(.85*np.sum(yc[4:]/Wmol[4:])); packet=nh+nc
out={'scope':__doc__,'fresh_hot_NOx_mol_kg_fresh':nh,'returned_NOx_mol_kg_fresh':nc,'initial_packet_NOx_mol_kg_fresh':packet,'rows':[]}
for N in [24,48]:
 path=D/f'restored_cross_width400um_N{N}_trajectory.npz';sources.append(path);z=np.load(path);t=z['t'];s=z['state'];mu=z['mu'];mh=float(z['hot_mass_per_area']);yy=s[:5*N].reshape(5,N,-1);Y=np.concatenate([(1-yy.sum(0))[None],yy]);T=s[5*N:];X=Y/K.W[:,None,None];X/=X.sum(0);mx=T.max(0); nox=((Y[4:]/Wmol[4:,None,None])*mu[None,:,None]).sum((0,1))/mh; radical=((Y[2:4]/Wmol[2:4,None,None])*mu[None,:,None]).sum(1)/mh
 nonnegative=np.all(Y>=0,axis=(0,1));positive=np.all(Y>0,axis=(0,1));below=np.flatnonzero(mx<=1700)
 rowsel={'last_above_before_window':below[0]-1,'first_saved_below':below[0],'saved_minimum_max_T':int(mx.argmin()),'last_saved_below':below[-1],'first_above_after_window':below[-1]+1,'last_saved':len(t)-1}
 snapshots={name:{'index':int(i),'t_s':float(t[i]),'max_T_K':float(mx[i]),'packet_NOx_mol_kg_fresh':float(nox[i]),'packet_NOx_minus_input_return_mol_kg_fresh':float(nox[i]-nc),'N_radical_mol_kg_fresh':float(radical[0,i]),'O_radical_mol_kg_fresh':float(radical[1,i])} for name,i in rowsel.items()}
 entropy=np.full(t.size,np.nan)
 for k in np.flatnonzero(nonnegative):
  _,_,s0=K.thermochemistry(T[:,k]);logs=np.zeros_like(X[:,:,k]);np.log(X[:,:,k],out=logs,where=X[:,:,k]>0);entropy[k]=float(np.sum(mu*np.sum(Y[:,:,k]*Ri[:,None]*(s0-logs),axis=0)))
 pairgood=nonnegative[:-1]&nonnegative[1:];ds=np.diff(entropy)[pairgood]
 samples=np.unique(np.linspace(0,len(t)-1,81,dtype=int));sigmas=[];sigscale=[];ratios=[];skips=0;negative=[];raw_negative=[]
 for k in samples:
  x=X[:,:,k];tt=T[:,k];y=Y[:,:,k];width=mu*(Ri@y)*tt/P;dx=.5*(width[:-1]+width[1:]);xf=.5*(x[:,:-1]+x[:,1:]);tf=.5*(tt[:-1]+tt[1:]);gx=(x[:,1:]-x[:,:-1])/dx;gx[0]=-gx[1:].sum(0)
  valid=np.all(x[:,:-1]>0,axis=0)&np.all(x[:,1:]>0,axis=0);skips += int((~valid).sum())
  if not valid.any():continue
  d=bd.binary_diffusivities(tf[valid],P);rf=P*(K.W@xf[:,valid])/(K.R*tf[valid]);jms=maxwell_stefan_flux(xf[:,valid],gx[:,valid],d,rf,K.W)['j']
  for local,f in enumerate(np.flatnonzero(valid)):
   gas.TPX=float(tf[f]),P,xf[:,f];lam=float(gas.thermal_conductivity);dt=gas.thermal_diff_coeffs;dt*=xf[:,f]/np.maximum(xf[:,f],1e-20);dt[int(np.argmax(xf[:,f]))]-=dt.sum();gt=(tt[f+1]-tt[f])/dx[f];j=jms[:,local]-dt*gt/tf[f];qdufour=-tf[f]*np.dot(dt*Ri,gx[:,f]/xf[:,f]);q=-lam*gt+qdufour;db=(tt[f]-tt[f+1])/(tt[f]*tt[f+1]);relative=(x[:,f+1]-x[:,f])/x[:,f];dl=np.log(x[:,f+1])-np.log(x[:,f]);near=np.abs(relative)<.5;dl[near]=np.log1p(relative[near]);thermal=q*db;species=-np.dot(j*Ri,dl);sigma=float(thermal+species);scale=float(abs(thermal)+np.sum(abs(j*Ri*dl)));sigmas.append(sigma);sigscale.append(scale);ratios.append(schur_ratio(tf[f],xf[:,f],d[:,:,local],rf[local],K.W,dt,lam))
   if sigma<0:raw_negative.append(sigma)
   if sigma < -1e-12*max(scale,1.):negative.append({'saved_index':int(k),'face':int(f),'sigma_W_m2_K':sigma,'term_L1_scale':scale})
 row={'N':N,'saved_count':len(t),'negative_saved_state_count':int((~nonnegative).sum()),'minimum_saved_Y':float(Y.min()),'first_strict_positive_saved_t_s':float(t[np.flatnonzero(positive)[0]]),'all_below_saved_count':len(below),'snapshots':snapshots,'last_packet_NOx_retention':float(nox[-1]/packet),'last_net_of_input_return_retention_relative_hot':float((nox[-1]-nc)/nh),'entropy_nonnegative_saved_state_count':int(nonnegative.sum()),'entropy_initial_J_m2_K':float(entropy[0]),'entropy_final_J_m2_K':float(entropy[-1]),'minimum_entropy_increment_over_adjacent_nonnegative_saved_states_J_m2_K':float(ds.min()),'sampled_saved_indices':samples.tolist(),'finite_positive_face_count':len(sigmas),'excluded_nonpositive_endpoint_face_count':skips,'minimum_full_cross_finite_face_entropy_W_m2_K':float(min(sigmas)),'maximum_restored_local_Schur_ratio':float(max(ratios)),'raw_negative_face_count':len(raw_negative),'negative_flag_threshold':'sigma < -1e-12 * max(term_L1_scale, 1 W/m2/K); reporting tolerance only, not a rigorous roundoff bound','material_negative_full_cross_finite_face_cases':negative}
 out['rows'].append(row)
exact=json.loads((D/'exact_endpoint_certificate.json').read_text());out['exact_certificate_recorded_hashes_match_current_files']=all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in exact['input_sources'].items());out['source_binding_limitation']='Hashes below bind this audit to current bytes; original trajectory NPZ/JSON does not save generating-code hashes. Exact certificate input_sources omits the thermo manifest from which it reads R. These are reproducibility metadata gaps, not demonstrated altered physics.'
out['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources};out['wall_s']=time.monotonic()-START
(OUT/'saved_path_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['source_sha256','scope']},indent=2))
