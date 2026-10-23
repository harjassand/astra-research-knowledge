"""Read-only regime/entropy/Soret diagnostics on one actual resolved lamella.
No ODE replay. Estimates and omitted-physics samples are not applicability proof.
"""
import time
START=time.monotonic()
from pathlib import Path
import sys,os,json,resource
import numpy as np
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));tag=os.environ.get('CASE','isobaric_arithmetic_N24');p=D/(tag+'_trajectory.npz');z=np.load(p);os.environ['CELLS']=str(int(z['N']));os.environ['MODE']=str(z['mode']);os.environ['WIDTH']=str(float(z['L0']))
import resolve_lamella as m
mu=z['mu'];assert np.allclose(mu,m.MU,rtol=1e-13,atol=0);ts=z['t'];ss=z['state'];rows=[];surfaces=[]
for t,s in zip(ts,ss.T):
 Y,T=m.unpack(s);d=m.evaluate(t,s);dY=np.vstack([-d[:5*m.N].reshape(5,m.N).sum(0),d[:5*m.N].reshape(5,m.N)]);Td=d[5*m.N:];cp_i,h_i,s_i=m.thermo(T);cp=np.sum(Y*cp_i,0);rm=m.K.R*np.sum(Y/m.K.W[:,None],0);rd=m.K.R*np.sum(dY/m.K.W[:,None],0);v=rm*T/m.P0;width=mu*v;dx=.5*(width[:-1]+width[1:]);vd=(rm*Td+T*rd)/m.P0;uf=np.r_[0,np.cumsum(mu*vd)];uf-=uf[-1]/2;c=np.sqrt(cp/(cp-rm)*rm*T);cf=np.r_[c[0],np.minimum(c[:-1],c[1:]),c[-1]];mach=float(np.max(abs(uf)/cf))
 X=Y/m.K.W[:,None];X/=X.sum(0);Xp=np.maximum(X,0);Xp/=Xp.sum(0);xf=.5*(Xp[:,:-1]+Xp[:,1:]);gr=(X[:,1:]-X[:,:-1])/dx;gr[0]=-gr[1:].sum(0);tf=.5*(T[:-1]+T[1:]);rf=m.P0*(m.K.W@xf)/(m.K.R*tf);dif=m.BD.binary_diffusivities(tf,m.P0,allow_below_300=True);J=m.maxwell_stefan_flux(xf,gr,dif,rf,m.K.W)['j'];_,lam=m.K.pure_transport(tf);kf=.5*(np.sum(xf*lam,0)+1/np.sum(xf/lam,0));q=-kf*(T[1:]-T[:-1])/dx;db=1/T[1:]-1/T[:-1]
 positive=(X[:,:-1]>0).all(0)&(X[:,1:]>0).all(0);sigma=np.full(m.N-1,np.nan)
 sigma[positive]=q[positive]*db[positive]-np.sum(J[:,positive]*(m.K.R/m.K.W[:,None])*np.log(X[:,1:][:,positive]/X[:,:-1][:,positive]),0)
 prop=m.K.evaluate(T,np.maximum(Y,0)/np.maximum(Y,0).sum(0),m.P0);meanfree=prop['viscosity']/m.P0*np.sqrt(np.pi*rm*T/2);kn=meanfree/width
 rows.append({'t_s':float(t),'max_Mach_estimate':mach,'max_meanfree_over_cellwidth_estimate':float(kn.max()),'min_finite_face_entropy_W_m2_K':float(np.nanmin(sigma)) if positive.any() else None,'max_T_K':float(T.max()),'T_span_K':float(np.ptp(T))});surfaces.append((T,Y,xf,tf,gr,dx,J))
# Native thermal-diffusion coefficients at actual face states, without evolving them.
sys.path.insert(0,str(D.parent/'nitrogen_finite_cycle_20261021/thermo_helper'));from validate import native_corrected
g=native_corrected(m.K);g.transport_model='multicomponent';indices=sorted(set([0,int(np.argmax([r['max_Mach_estimate'] for r in rows])),int(np.argmin([r['max_T_K'] for r in rows])),int(np.argmin(abs(ts-1e-4)))]));soret=[]
for ix in indices:
 T,Y,xf,tf,gr,dx,J=surfaces[ix]
 for j in np.argsort(abs(np.diff(T)/dx))[-2:]:
  g.TPX=float(tf[j]),m.P0,xf[:,j];dt=g.thermal_diff_coeffs;js=-dt*(T[j+1]-T[j])/(tf[j]*dx[j]);soret.append({'t_s':float(ts[ix]),'face':int(j),'T_left_right_K':[float(T[j]),float(T[j+1])],'ordinary_j_kg_m2_s':J[:,j].tolist(),'omitted_Soret_j_kg_m2_s':js.tolist(),'Soret_norm_over_ordinary_norm':float(np.linalg.norm(js)/max(1e-300,np.linalg.norm(J[:,j]))),'ordinary_vs_multicomponent_conductivity_relative':float((g.thermal_conductivity-(.5*(np.sum(xf[:,j]*m.K.pure_transport(np.array([tf[j]]))[1][:,0])+1/np.sum(xf[:,j]/m.K.pure_transport(np.array([tf[j]]))[1][:,0]))))/g.thermal_conductivity)})
below=np.array([r['max_T_K']<=1700 for r in rows]);intervals=[]
for group in np.split(np.arange(len(ts)),np.where(np.diff(below.astype(int))!=0)[0]+1):
 if below[group[0]]:intervals.append([float(ts[group[0]]),float(ts[group[-1]])])
result={'scope':__doc__,'N':m.N,'saved_step_count':len(ts),'all_gas_below1700_saved_intervals_s':intervals,'max_induced_Mach_estimate':max(r['max_Mach_estimate'] for r in rows),'max_cell_Kn_estimate':max(r['max_meanfree_over_cellwidth_estimate'] for r in rows),'min_finite_observed_face_entropy_W_m2_K':min(r['min_finite_face_entropy_W_m2_K'] for r in rows if r['min_finite_face_entropy_W_m2_K'] is not None),'negative_face_entropy_times_below_minus1e-7':[r['t_s'] for r in rows if r['min_finite_face_entropy_W_m2_K'] is not None and r['min_finite_face_entropy_W_m2_K'] < -1e-7],'Soret_native_samples':soret,'limits':['Soret samples do not bound its trajectory effect; omission not admitted as negligible','Viscosity mean-free-path estimate is a kinetic scale, not species-resolved rarefaction proof','Cell Kn is resolution-dependent; physical gradient lengths and initial discontinuity also matter','Low-Mach estimate omits acoustic initial layer and axial shear/injection','Positive sampled face entropy is not the logface universal proof','Packet NOx includes returned inventory and is not net product'],'total_wall_s':time.monotonic()-START,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/(tag+'_regime_result.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result))
