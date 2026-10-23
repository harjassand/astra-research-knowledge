"""Staggered compressible pressure-loaded material slab; NOT a free jet/device.
Comparison tests the low-Mach approximation within explicitly pressure-loaded,
impermeable moving boundaries. Total U+KE+P0*width is the energy invariant.
"""
import time
START=time.monotonic()
import os,sys,json,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,BDF
from scipy.sparse import lil_matrix
from types import SimpleNamespace
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import resolve_lamella as a
N=a.N;K=a.K;MU=a.MU;Mnode=np.r_[MU[0]/2,.5*(MU[:-1]+MU[1:]),MU[-1]/2];P0=a.P0;ns=6*N;TAG=os.environ.get('RUN_TAG','compressible_N24');HORIZON=float(os.environ.get('HORIZON','.0002'))
T0=a.Tinit;Y0=a.Yinit;v0=K.R*np.sum(Y0/K.W[:,None],0)*T0/P0;X0=np.r_[0,np.cumsum(MU*v0)]

def evaluate(t,s,details=False):
 Y,T=a.unpack(s[:ns]);K._signed_state(T,Y,P0,False);x=s[ns:ns+N+1];u=s[ns+N+1:];width=np.diff(x)
 if np.any(width<=0):raise ValueError('Crossed Lagrangian cell boundary')
 rho=MU/width;cp_i,h_i,s_i=a.thermo(T);rm=K.R*np.sum(Y/K.W[:,None],0);cp=np.sum(Y*cp_i,0);cv=cp-rm;P=rho*rm*T
 if np.any((P<.5*P0)|(P>2*P0)):raise ValueError('Pressure outside source compatibility range')
 X=Y/K.W[:,None];X/=X.sum(0);Xp=np.maximum(X,0);Xp/=Xp.sum(0);Xf=.5*(Xp[:,:-1]+Xp[:,1:]);Yf=Xf*K.W[:,None];Yf/=Yf.sum(0);dx=.5*(width[:-1]+width[1:]);Tf=.5*(T[:-1]+T[1:]);Pf=.5*(P[:-1]+P[1:]);rf=Pf*(K.W@Xf)/(K.R*Tf)
 drive=(X[:,1:]-X[:,:-1])/dx+(Xf-Yf)*np.diff(np.log(P))/dx;drive[0]=-drive[1:].sum(0)
 J=np.zeros((6,N+1));J[:,1:N]=a.maxwell_stefan_flux(Xf,drive,a.BD.binary_diffusivities(Tf,Pf,allow_below_300=True),rf,K.W,trial_extension=bool(np.any(X<0)))['j']
 _,lam=K.pure_transport(Tf);kf=.5*(np.sum(Xf*lam,0)+1/np.sum(Xf/lam,0));qcross=np.zeros(N-1)
 if a.MULTI:
  for j in range(N-1):
   a.gas.TPX=float(Tf[j]),float(Pf[j]),Xf[:,j];kf[j]=a.gas.thermal_conductivity
   if a.CROSS:
    dt=a.gas.thermal_diff_coeffs;dt*=Xf[:,j]/np.maximum(Xf[:,j],1e-20);dt[int(np.argmax(Xf[:,j]))]-=dt.sum();J[:,j+1]+=-dt*(T[j+1]-T[j])/(Tf[j]*dx[j]);dlog=np.divide(drive[:,j],Xf[:,j],out=np.zeros(6),where=Xf[:,j]>0);qcross[j]=-Tf[j]*np.dot(dt*K.R/K.W,dlog)
 Q=np.zeros(N+1);Q[1:N]=-kf*np.diff(T)/dx+np.sum(a.hsecant(T[:-1],T[1:])*J[:,1:N],0)+qcross
 # Positive physical-mixture transport-only continuation; chemistry is raw signed.
 prop=K.evaluate(T,np.maximum(Y,0)/np.maximum(Y,0).sum(0),P);muvis=prop['viscosity'];tau=(4/3)*muvis*np.diff(u)/width;stress=P-tau;ud=np.r_[P0-stress[0],stress[:-1]-stress[1:],stress[-1]-P0]/Mnode
 rate=K.signed_rates(T,rho*Y/K.W[:,None])[0];omega=K.W[:,None]*(K.nu@rate);dy=-np.diff(J,axis=1)/MU+omega/rho;ed=-(stress*np.diff(u)+np.diff(Q))/MU;ui=h_i-K.R*T/K.W[:,None];td=(ed-np.sum(ui*dy,0))/cv
 if details:
  U=np.dot(MU,np.sum(Y*ui,0));KE=.5*np.dot(Mnode,u*u);cs=np.sqrt(cp/cv*rm*T);cface=np.r_[cs[0],np.minimum(cs[:-1],cs[1:]),cs[-1]]
  return {'U_J_m2':float(U),'KE_J_m2':float(KE),'width_m':float(width.sum()),'invariant_J_m2':float(U+KE+P0*width.sum()),'P_min_Pa':float(P.min()),'P_max_Pa':float(P.max()),'T_min_K':float(T.min()),'T_max_K':float(T.max()),'max_Mach':float(max(abs(u)/cface)),'min_Y':float(Y.min()),'packet_NOx_mol_per_kg_hot_fresh':float(np.dot(MU,1000*np.sum(Y[[4,5]]/K.W[[4,5],None],0))/a.Mhot),'viscous_entropy_W_m2_K':float(np.sum(tau*np.diff(u)/T))}
 return np.r_[dy[1:].ravel(),td,u,ud]

def main():
 y=np.r_[Y0[1:].ravel(),T0,X0,np.zeros(N+1)];initial=evaluate(0,y,True);prep=time.monotonic()-START;st=time.monotonic();atol=np.r_[np.full(5*N,1e-13),np.full(N,1e-4),np.full(N+1,1e-12),np.full(N+1,1e-5)]
 dim=ns+2*(N+1);J=lil_matrix((dim,dim))
 for i in range(N):
  cells=range(max(0,i-1),min(N,i+2));cols=[k*N+j for k in range(6) for j in cells]+[ns+j for j in range(max(0,i-1),min(N+1,i+3))]+[ns+N+1+i,ns+N+2+i]
  for k in range(6):J[k*N+i,cols]=1
 for j in range(N+1):
  J[ns+j,ns+N+1+j]=1;cells=range(max(0,j-1),min(N,j+1));cols=[k*N+i for k in range(6) for i in cells]+[ns+i for i in range(max(0,j-1),min(N+1,j+2))]+[ns+N+1+i for i in range(max(0,j-1),min(N+1,j+2))];J[ns+N+1+j,cols]=1
 solver=BDF(evaluate,0,y,HORIZON,first_step=1e-11,max_step=1e-6,rtol=2e-6,atol=atol,jac_sparsity=J.tocsr());times=[0.];states=[y.copy()];last=st;reason=None
 while solver.status=='running':
  try:msg=solver.step()
  except Exception as e:reason=repr(e);break
  if solver.status=='failed':reason=msg;break
  times.append(float(solver.t));states.append(solver.y.copy())
  if time.monotonic()-last>=5 or solver.status=='finished':
   rec={'t_s':float(solver.t),'wall_s':time.monotonic()-st,'steps':len(times)-1,'nfev':solver.nfev,'nlu':solver.nlu,'status':solver.status};print(json.dumps(rec),flush=True);np.savez_compressed(D/(TAG+'_checkpoint.npz'),t=solver.t,state=solver.y,mu=MU,N=N,L0=a.L0);(D/(TAG+'_progress.json')).write_text(json.dumps(rec,indent=2));last=time.monotonic()
  if time.monotonic()-st>float(os.environ.get('WALL_SECONDS','120')):reason='wall_budget_between_accepted_steps';break
 sol=SimpleNamespace(t=np.array(times),y=np.array(states).T,success=solver.status=='finished',message=reason or solver.status,nfev=solver.nfev,njev=solver.njev,nlu=solver.nlu)

 integ=time.monotonic()-st;recs=[evaluate(t,s,True) for t,s in zip(sol.t,sol.y.T)];below=[float(t) for t,r in zip(sol.t,recs) if r['T_max_K']<=1700];np.savez_compressed(D/(TAG+'_trajectory.npz'),t=sol.t,state=sol.y,mu=MU,node_mass=Mnode,N=N,L0=a.L0)
 out={'scope':__doc__,'success':sol.success,'message':sol.message,'N':N,'initial_width_m':a.L0,'horizon_s':HORIZON,'completed_s':float(sol.t[-1]),'first_saved_all_gas_below1700_s':below[0] if below else None,'minimum_saved_max_T_K':min(r['T_max_K'] for r in recs),'initial':initial,'final':recs[-1],'max_invariant_drift_J_m2':max(abs(r['invariant_J_m2']-initial['invariant_J_m2']) for r in recs),'maximum_Mach':max(r['max_Mach'] for r in recs),'minimum_Y':min(r['min_Y'] for r in recs),'minimum_viscous_entropy_W_m2_K':min(r['viscous_entropy_W_m2_K'] for r in recs),'preparation_wall_s':prep,'integration_wall_s':integ,'total_wall_s':time.monotonic()-START,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'nfev':sol.nfev,'njev':sol.njev,'nlu':sol.nlu,'steps':len(sol.t)-1,'limits':['One-temperature equilibrium thermochemistry, not vibrational nonequilibrium','Zero bulk viscosity; Stokes longitudinal4mu/3','Pressure-loaded impermeable moving material boundaries, not a freejet','No injector, shear stability, radiation, wall or completeprocess','Arithmetic face; no universal discrete entropy certificate']};(D/(TAG+'_result.json')).write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
if __name__=='__main__':main()
