"""Finite-inventory two-bed model with an isothermal uniform-pressure heater chain.
A chain approaches plug flow without discarding heater storage; not new invention.
Conditional engineering model, not an experimentally qualified nitrogen process.
Explicit continuous-NASA variant; isothermal finite-volume central heater;
quasi-static Ergun momentum, no acoustic/kinetic-energy resolution.
"""
import numpy as np,json,time,resource,os,sys,hashlib
from pathlib import Path
from scipy.integrate import solve_ivp
from scipy.sparse import lil_matrix
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'thermo_helper'));from helper import ThermoKernel
K=ThermoKernel();N=int(os.environ.get('CELLS','12'));NH=int(os.environ.get('HEATER_CELLS','4'));M=2*N+NH;H=N;HI=np.arange(N,N+NH);ns=6
L=.1;dx=L/N;por=.4;dp=.009525;P0=101325.;TH=2700.;T0=300.;VH=.1;CS=2.5e6
KR=1.4161997074001969e-9*.2;sig=5.670374419e-8;vol=np.full(M,por*dx);vol[HI]=VH/NH;ids=np.r_[np.arange(N),np.arange(N+NH,M)]
A=150*(1-por)**2/(por**3*dp**2);B=1.75*(1-por)/(por**3*dp);dist=np.full(M+1,dx);dist[[0,N,N+NH,M]]=dx/2
Yfeed=np.zeros(6);Yfeed[:2]=np.array([.79,.21])*K.W[:2];Yfeed/=Yfeed.sum();feed=K.evaluate(300,Yfeed);hfeed=float(feed['enthalpy'][0]);rhofeed=float(feed['rho'][0]);Rfeed=float(feed['Rmix'][0]);eiH=K.evaluate(TH,Yfeed)['e_species'][:,0]
NOidx=[4,5];ngas=7*M;nsolid=2*N;nc=9
ledger_names=['heater_positive_MJ_m2','heater_removal_MJ_m2','boundary_enthalpy_MJ_m2','radiation_MJ_m2','boundary_mass_kg_m2','export_NOx_mol_m2','feed_mass_kg_m2','reversible_feed_pump_MJ_m2','export_mass_kg_m2']

def flux(dP,rho,mu,d):
 a=A*mu/rho;b=B/rho;v=abs(dP)/d;return np.sign(dP)*2*v/(a+np.sqrt(a*a+4*b*v))

def props(s):
 q=s[:6*M].reshape(6,M);rho=q.sum(0);Y=q/np.maximum(rho,1e-12);U=s[6*M:7*M]*1e6
 # Isothermal header constraint is an exact invariant; use its algebraic expression
 # for property evaluation, but retain and audit stored header energy separately.
 U=U.copy();U[HI]=eiH@q[:,HI]
 r=K.evaluate_rho_u(np.maximum(rho,1e-9),U,Y,trial_clamp=True)
 return q,rho,U,r

def evaluate(t,s,alpha,details=False):
 # Raw conservative Y is used for linear donor transport, including tiny negative
 # trial concentrations. Kinetics/properties retain explicitly checked clipping.
 # Clipping donor fluxes instead traps negative trace states and corrupts Jacobians.
 q,rho,U,r=props(s);Y=q/rho;T=r['T'];P=r['pressure'].copy();P[HI]=np.mean(P[HI]);h=r['enthalpy'];Ts=np.maximum(200,s[ngas:ngas+nsolid]*1000)
 F=np.zeros(M+1);E=np.zeros(M+1);S=np.zeros((6,M+1))
 F[1:M]=flux(P[:-1]-P[1:],.5*(rho[:-1]+rho[1:]),.5*(r['viscosity'][:-1]+r['viscosity'][1:]),dist[1:M]);donor=np.where(F[1:M]>=0,np.arange(M-1),np.arange(1,M));E[1:M]=F[1:M]*h[donor];S[:,1:M]=F[1:M]*Y[:,donor]
 gl=flux(P0-P[0],.5*(rhofeed+rho[0]),.5*(float(feed['viscosity'][0])+r['viscosity'][0]),dist[0]);gr=flux(P[-1]-P0,.5*(rhofeed+rho[-1]),.5*(float(feed['viscosity'][0])+r['viscosity'][-1]),dist[-1])
 F[0]=(1-alpha)+alpha*gl;F[-1]=(1-alpha)*gr-alpha
 E[0]=(1-alpha)*hfeed+alpha*gl*(hfeed if gl>=0 else h[0]);E[-1]=(1-alpha)*gr*(h[-1] if gr>=0 else hfeed)-alpha*hfeed
 S[:,0]=(1-alpha)*Yfeed+alpha*gl*(Yfeed if gl>=0 else Y[:,0]);S[:,-1]=(1-alpha)*gr*(Y[:,-1] if gr>=0 else Yfeed)-alpha*Yfeed
 MW=1/np.sum(Y/K.W[:,None],axis=0)
 molL=F[N]/MW[N-1 if F[N]>=0 else N];molR=F[N+NH]/MW[N+NH-1 if F[N+NH]>=0 else N+NH]
 molsource=np.sum(r['mass_production'][:,HI]/K.W[:,None],axis=0)
 cprime=(molL-molR+np.dot(vol[HI],molsource))/VH
 mol=molL
 for j in range(NH-1):
  mol+=vol[N+j]*(molsource[j]-cprime);face=N+j+1;don=N+j if mol>=0 else N+j+1
  F[face]=mol*MW[don];S[:,face]=F[face]*Y[:,don];E[face]=F[face]*h[don]
 dq=(S[:,:-1]-S[:,1:])/vol+r['mass_production'];dU=(E[:-1]-E[1:])/vol
 Gmid=.5*(abs(F[:-1])+abs(F[1:]));mu=r['viscosity'][ids];kg=r['conductivity'][ids];Pr=r['cp'][ids]*mu/kg;Nu=2+1.1*(Gmid[ids]*dp/mu)**.6*Pr**(1/3);Uv=Nu*kg/dp*6*(1-por)/dp
 Q=Uv*(Ts-T[ids]);dU[ids]+=Q/por
 qs=np.zeros(2*N+2);left=Ts[:N];right=Ts[N:]
 qs[1:N]=-KR/4*(left[1:]**4-left[:-1]**4)/dx;qs[0]=-sig*(left[0]**4-T0**4);qs[N]=0
 qs[N+2:2*N+1]=-KR/4*(right[1:]**4-right[:-1]**4)/dx;qs[N+1]=0;qs[-1]=sig*(right[-1]**4-T0**4)
 div=np.r_[np.diff(qs[:N+1]),np.diff(qs[N+1:])]/dx;dTs=(-Q-div)/CS
 dU[HI]=eiH@dq[:,HI];heater_cells=vol[HI]*dU[HI]-(E[HI]-E[HI+1]);heater=float(heater_cells.sum())
 nout=float(np.sum(1000*(S[NOidx,-1]-S[NOidx,0])/K.W[NOidx]));pump=Rfeed*T0*((1-alpha)*max(0,np.log(P[0]/P0))+alpha*max(0,np.log(P[-1]/P0)))
 mout=alpha*max(-gl,0)+(1-alpha)*max(gr,0)
 led=np.array([np.maximum(heater_cells,0).sum()/1e6,np.maximum(-heater_cells,0).sum()/1e6,(E[0]-E[-1])/1e6,(qs[-1]-qs[0])/1e6,F[0]-F[-1],nout,1+alpha*max(gl,0)+(1-alpha)*max(-gr,0),pump/1e6,mout])
 out=np.r_[dq.ravel(),dU/1e6,dTs/1000,led]
 if details:return {'P':P,'T':T,'Ts':Ts,'F':F,'heater':heater,'rho':rho,'Y':Y,'mach':Gmid/(rho*np.where(np.isin(np.arange(M),HI),1.,por))/np.sqrt(r['cp']/r['cv']*r['Rmix']*T),'clamps':int(np.count_nonzero(r['diagnostics']['energy_clamped'])),'instant_energy_residual_W_m2':float(np.dot(vol,dU)+CS*dx*dTs.sum()-heater-(E[0]-E[-1])+(qs[-1]-qs[0])),'header_pressure_spread_Pa':float(np.ptp(r['pressure'][HI])),'header_U_residual_J_m3':float(max(abs(s[6*M+HI]*1e6-eiH@q[:,HI])))}
 return out

def initial():
 saved=np.load(os.environ['RESTART']);oldN=int(saved['N']);assert oldN==N
 oldH=int(saved['NH']) if 'NH' in saved else 1;oldM=2*N+oldH
 def expand(a):
  q=a[:6*oldM].reshape(6,oldM);U=a[6*oldM:7*oldM];ss=a[7*oldM:7*oldM+2*N];led=a[-nc:]
  if oldH==NH:return a.copy()
  if oldH!=1:raise ValueError('Only unchanged heater mesh or conservative1→NH expansion admitted')
  nq=np.column_stack([q[:,:N],np.repeat(q[:,N:N+1],NH,axis=1),q[:,N+1:]])
  nu=np.r_[U[:N],np.repeat(U[N],NH),U[N+1:]]
  return np.r_[nq.ravel(),nu,ss,led]
 return expand(saved['state']),expand(saved['initial']),float(saved['t'])

def sparsity():
 n=ngas+nsolid+nc;J=lil_matrix((n,n));heatercols=[k*M+j for j in range(N-1,N+NH+1) for k in range(7)]
 for i in range(M):
  rows=[k*M+i for k in range(7)];cols=[k*M+j for j in range(max(0,i-1),min(M,i+2)) for k in range(7)]
  if N-1<=i<=N+NH:cols=list(set(cols+heatercols))
  for a in rows:
   J[a,cols]=1
   if i not in HI:J[a,ngas+(i if i<N else i-NH)]=1
 for k,i in enumerate(ids):
  cols=[a*M+j for j in range(max(0,i-1),min(M,i+2)) for a in range(7)]
  if i in [N-1,N+NH]:cols=list(set(cols+heatercols))
  J[ngas+k,cols]=1
  for j in range(max(0,k-1),min(2*N,k+2)):J[ngas+k,ngas+j]=1
 J[-nc:,:]=1;return J.tocsr()

def inventory(s):
 q=s[:6*M].reshape(6,M);return {'species_kg_m2':q@vol,'energy_MJ_m2':float(np.dot(vol,s[6*M:7*M])+CS*dx*np.sum(s[ngas:ngas+nsolid])*1000/1e6)}

def main():
 start=time.monotonic();s,s0,elapsed=initial();records=[]
 duration=float(os.environ.get('DURATION','2'));ramp=.02;previous={};tag=os.environ.get('RUN_TAG','reacting_inventory');jac=sparsity();last_cycle=None
 atol=np.r_[np.full(6*M,float(os.environ.get("MASS_ATOL","1e-12"))),np.full(M,1e-8),np.full(nsolid,1e-7),np.full(nc,1e-8)]
 while elapsed<duration-1e-12:
  if time.monotonic()-start>float(os.environ.get('WALL_SECONDS','300')):break
  phase=int(round(elapsed));target=phase%2;startalpha=target if phase==0 else 1-target;tbegin=elapsed
  def alpha(u):return startalpha+(target-startalpha)*min(1,max(0,(u-tbegin)/ramp))
  sol=solve_ivp(lambda u,v:evaluate(u,v,alpha(u)),[elapsed,min(duration,elapsed+1)],s,method='Radau',rtol=float(os.environ.get("RTOL","2e-6")),atol=atol,jac_sparsity=jac)
  s=sol.y[:,-1];elapsed=float(sol.t[-1]);np.savez_compressed(R/(tag+'_blow_'+str(phase)+'.npz'),t=sol.t,state=sol.y,phase=phase,N=N);d=evaluate(elapsed,s,target,True)
  rec={'t_s':elapsed,'success':sol.success,'message':sol.message,'steps':len(sol.t)-1,'nfev':sol.nfev,'nlu':sol.nlu,'pressure_range_Pa':[float(d['P'].min()),float(d['P'].max())],'T_range_K':[float(d['T'].min()),float(d['T'].max())],'Tsmax_K':float(d['Ts'].max()),'instant_energy_residual_W_m2':d['instant_energy_residual_W_m2'],'min_rho_species':float(s[:6*M].min()),'accepted_endpoint_energy_clamps':d['clamps'],'header_U_residual_J_m3':d['header_U_residual_J_m3']}
  sampled=[evaluate(float(tt),ss,alpha(float(tt)),True) for tt,ss in zip(sol.t,sol.y.T)]
  rec['accepted_step_extrema']={'max_Mach':float(max(max(v['mach']) for v in sampled)),'max_Ts_K':float(max(max(v['Ts']) for v in sampled)),'min_pressure_Pa':float(min(min(v['P']) for v in sampled)),'max_pressure_Pa':float(max(max(v['P']) for v in sampled)),'energy_clamp_count':int(sum(v['clamps'] for v in sampled)),'min_species_density':float(sol.y[:6*M].min())}
  if target in previous:
   old=previous[target];delta=s[-nc:]-old[-nc:];a=inventory(s);b=inventory(old);rec['cycle']={'delta_ledger':dict(zip(ledger_names,map(float,delta))),'solid_reset_max_K':float(max(abs(s[ngas:ngas+nsolid]-old[ngas:ngas+nsolid]))*1000),'species_inventory_reset_max_kg_m2':float(max(abs(a['species_kg_m2']-b['species_kg_m2']))),'stored_energy_change_MJ_m2':a['energy_MJ_m2']-b['energy_MJ_m2'],'gas_species_field_reset_max_kg_m3':float(max(abs(s[:6*M]-old[:6*M]))),'gas_energy_field_reset_max_J_m3':float(max(abs(s[6*M:7*M]-old[6*M:7*M]))*1e6),'gas_heat_MJ_per_export_NOx':float(delta[0]/delta[5]) if delta[5]>0 else None};last_cycle=rec['cycle']
  previous[target]=s.copy();records.append(rec);print(json.dumps(rec),flush=True)
  np.savez_compressed(R/(tag+'_checkpoint.npz'),state=s,initial=s0,t=elapsed,N=N,NH=NH)
  (R/(tag+'_progress.json')).write_text(json.dumps(records,indent=2)+'\n')
  if not sol.success or d['clamps'] or s[:6*M].min() < -1e-8:break
 a=inventory(s);b=inventory(s0);led=s[-nc:];result={'scope':__doc__,'N_per_bed':N,'NH':NH,'rtol':float(os.environ.get('RTOL','2e-6')),'mass_atol':float(os.environ.get('MASS_ATOL','1e-12')),'completed_t_s':elapsed,'records':records,'ledger':dict(zip(ledger_names,map(float,led))),'energy_balance_residual_MJ_m2':a['energy_MJ_m2']-b['energy_MJ_m2']-led[0]+led[1]-led[2]+led[3],'mass_balance_residual_kg_m2':float(sum(a['species_kg_m2']-b['species_kg_m2'])-led[4]),'restart':os.environ.get('RESTART'),'wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'last_cycle':last_cycle,'assumptions':{'solid_capacity_J_m3_K':CS,'heater_volume_m3_m2':VH,'switch_ramp_s':ramp,'no_actual_material_qualification':True,'radiation_factor':.2,'no_capture_or_startup_accounting':True,'output':'Net exported exchanger NOx; no transient tail or nitrate qualification'}}
 (R/(tag+'_result.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
