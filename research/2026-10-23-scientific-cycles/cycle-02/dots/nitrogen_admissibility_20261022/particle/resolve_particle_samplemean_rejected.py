"""Conditional finite grain response to frozen actual model histories.
Not a new coupled process, material qualification, or periodic-cycle result.
"""
from pathlib import Path
import json,time,resource,hashlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import block_diag,diags
P=Path(__file__).resolve().parent
K_T=np.arange(300,1701,200);K_V=np.array([2.04,1.97,1.90,1.84,1.79,1.74,1.68,1.62])
def run(n,z):
 t=z['t'];tg=z['Tg'];hh=z['h'];gg=z['g_other'];R=float(z['R']);cv=float(z['cv']);nc=tg.shape[1]
 edge=np.linspace(0,R,n+1);r=(edge[1:]+edge[:-1])/2;v=np.diff(edge**3)/(3*R**2);a=(edge/R)**2
 def at(t0):return [np.array([np.interp(t0,t,x[:,j]) for j in range(nc)]) for x in [tg,hh,gg]]
 def rhs(t0,y):
  temp=y[:n*nc].reshape(nc,n);Tg,h,g=at(t0);k=np.interp(temp,K_T,K_V);kf=2/(1/k[:,:-1]+1/k[:,1:]);f=np.zeros((nc,n+1));f[:,1:n]=-kf*a[None,1:n]*(temp[:,1:]-temp[:,:-1])/(R/n)
  heff=1/(1/h+(R-r[-1])/k[:,-1]);f[:,-1]=heff*(temp[:,-1]-Tg-g/h)
  return np.r_[((f[:,:-1]-f[:,1:])/(cv*v)).ravel(),-f[:,-1]]
 J=block_diag([diags([np.ones(n-1),np.ones(n),np.ones(n-1)],[-1,0,1])]*nc,format='lil');N=n*nc
 from scipy.sparse import lil_matrix
 JJ=lil_matrix((N+nc,N+nc));JJ[:N,:N]=J
 for j in range(nc):JJ[N+j,(j+1)*n-1]=1
 y0=np.r_[np.repeat(z['Ts'][0],n),np.zeros(nc)];st=time.monotonic()
 sol=solve_ivp(rhs,[t[0],t[-1]],y0,method='BDF',rtol=2e-8,atol=np.r_[np.full(N,2e-6),np.full(nc,1e-5)],jac_sparsity=JJ.tocsr(),t_eval=t,max_step=.01)
 assert sol.success,sol.message
 temp=sol.y[:N].T.reshape(len(t),nc,n);surface=[]
 for j,time0 in enumerate(t):
  Tg,h,g=at(time0);k=np.interp(temp[j,:,-1],K_T,K_V);f=(temp[j,:,-1]-Tg-g/h)/(1/h+(R-r[-1])/k);surface.append(temp[j,:,-1]-f*(R-r[-1])/k)
 surface=np.array(surface);mean=temp@(v/(R/3));energy=cv*np.sum((temp[-1]-temp[0])*v,axis=1);ledger=sol.y[N:,-1]
 np.savez_compressed(P/f'radial_{n}.npz',t=t,ids=z['ids'],surface=surface,mean=mean,center=temp[:,:,0],energy_J_m2_particle=ledger)
 return {'n_radial':n,'success':sol.success,'wall_s':time.monotonic()-st,'nfev':sol.nfev,'nlu':sol.nlu,'max_surface_minus_mean_abs_K':float(np.max(abs(surface-mean))),'max_surface_minus_original_lumped_abs_K':float(np.max(abs(surface-z['Ts']))),'max_mean_minus_original_lumped_abs_K':float(np.max(abs(mean-z['Ts']))),'temperature_min_K':float(min(temp.min(),surface.min())),'temperature_max_K':float(max(temp.max(),surface.max())),'max_energy_ledger_error_J_m2_particle':float(max(abs(energy-ledger))),'final_heat_J_m2_particle':ledger.tolist()}
def harmonic(z):
 R=float(z['R']);cv=float(z['cv']);w=np.pi;k=np.interp(z['Ts'].mean(0),K_T,K_V);h=z['h'].mean(0);q=np.sqrt(1j*w*cv/k)*R;Z=k/R*(q/np.tanh(q)-1);Y=h*Z/(h+Z);Zl=1j*w*cv*R/3;Yl=h*Zl/(h+Zl)
 return {'period_s':2.,'scope':'Exact linear spherical conduction frequency response at local mean k,h; not periodic reacting model','Bi_radius_min_max':[float(min(h*R/k)),float(max(h*R/k))],'Fo_one_second_min_max':[float(min(k/cv/R**2)),float(max(k/cv/R**2))],'surface_amplitude_fraction_min_max':[float(min(abs(h/(h+Z)))),float(max(abs(h/(h+Z))))],'lumped_heat_admittance_ratio_min_max':[float(min(abs(Y/Yl))),float(max(abs(Y/Yl)))],'phase_difference_degrees_min_max':[float(min(np.angle(Y/Yl)*180/np.pi)),float(max(np.angle(Y/Yl)*180/np.pi))]}
if __name__=='__main__':
 st=time.monotonic();z=np.load(P/'forcing.npz');out={'scope':__doc__,'forcing_sha256':hashlib.sha256((P/'forcing.npz').read_bytes()).hexdigest(),'harmonic':harmonic(z),'runs':[run(n,z) for n in [16,32,64]]}
 a=np.load(P/'radial_32.npz');b=np.load(P/'radial_64.npz');out['refinement_32_64']={key:float(np.max(abs(a[key]-b[key]))) for key in ['surface','mean','energy_J_m2_particle']};out['wall_s']=time.monotonic()-st;out['rss_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 (P/'result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
