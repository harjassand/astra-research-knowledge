"""Resolved local molecular lamella, not a flowing injector or complete process.
Two mechanical contracts are explicit. No prescribed turbulent mixing time.
"""
import time
TOTAL_START=time.monotonic()
from pathlib import Path
import os,sys,json,resource,importlib.util,hashlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import lil_matrix
D=Path(__file__).resolve().parent;ROOT=D.parent
sp=importlib.util.spec_from_file_location('lamella_signed',ROOT/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);K=m.SignedTrialKernel()
sys.path.insert(0,str(D/'transport'));from molecular_transport import BinaryDiffusion,logarithmic_face,maxwell_stefan_flux
sys.path.insert(0,str(D/'closure'));from nasa_secant import nasa7_h_secant,splice_diagnostics
CROSS=os.environ.get('THERMAL_CROSS','0')=='1';MULTI=os.environ.get('MULTI_CONDUCTIVITY','0')=='1' or CROSS
if MULTI:
 sys.path.insert(0,str(ROOT/'nitrogen_finite_cycle_20261021/thermo_helper'));from validate import native_corrected
 gas=native_corrected(K);gas.transport_model='multicomponent'
BD=BinaryDiffusion();P0=101325.;RR=.85;N=int(os.environ.get('CELLS','12'));assert N%4==0;NH=N//2;NC=N//4;L0=float(os.environ.get('WIDTH','0.0001'));MODE=os.environ.get('MODE','isobaric');assert MODE in ['isobaric','rigid'];HORIZON=float(os.environ.get('HORIZON','0.001'));TAG=os.environ.get('RUN_TAG',f'{MODE}_N{N}')
yhot=np.load(ROOT/'nitrogen_admissibility_20261022/recycle_quench/once_through_2700_reference.npz')['hot_Y'];rawcold=np.load(ROOT/'nitrogen_admissibility_20261022/recycle_quench/mix_tau_0p0001_trajectory.npz')['return_Y'];ycold=np.maximum(rawcold,0);ycold/=ycold.sum()
Tinit=np.r_[np.full(NC,300.),np.full(NH,2700.),np.full(NC,300.)];Yinit=np.column_stack([np.repeat(ycold[:,None],NC,axis=1),np.repeat(yhot[:,None],NH,axis=1),np.repeat(ycold[:,None],NC,axis=1)])
relmu=np.r_[np.full(NC,RR/(2*NC)),np.full(NH,1/NH),np.full(NC,RR/(2*NC))];Rmix0=K.R*np.sum(Yinit/K.W[:,None],axis=0);Mhot=L0/np.dot(relmu,Rmix0*Tinit/P0);MU=relmu*Mhot

def unpack(s):
 yy=s[:5*N].reshape(5,N);Y=np.vstack([1-yy.sum(0),yy]);T=s[5*N:];return Y,T

def thermo(T):
 cp,h,ss=K.thermochemistry(T);return cp*K.R/K.W[:,None],h*(K.R*T)/K.W[:,None],ss*K.R/K.W[:,None]

def hsecant(TL,TR):
 return np.column_stack([nasa7_h_secant(float(a),float(b),K.nasa[:,8:15],K.nasa[:,1:8],K.R/K.W) for a,b in zip(TL,TR)])

def evaluate(t,state,details=False):
 Y,T=unpack(state)
 try:K._signed_state(T,Y,P0,False)
 except ValueError as e:
  (D/(TAG+"_trial_failure.json")).write_text(json.dumps({"t_s":t,"minY":float(Y.min()),"negative_mass":(-np.minimum(Y,0).sum(0)).tolist(),"T":T.tolist(),"Y":Y.tolist(),"error":str(e)},indent=2));raise
 cp_i,h_i,s_i=thermo(T);cp=np.sum(Y*cp_i,axis=0);Rmix=K.R*np.sum(Y/K.W[:,None],axis=0)
 P=P0 if MODE=='isobaric' else np.dot(MU,Rmix*T)/L0
 if P<.5*P0 or P>2*P0:raise ValueError('Pressure compatibility domain exceeded')
 v=Rmix*T/P;rho=1/v;width=MU*v;dx=.5*(width[:-1]+width[1:]);X=(Y/K.W[:,None]);X/=X.sum(0)
 Xp=np.maximum(X,0);Xp/=Xp.sum(0);Xf=.5*(Xp[:,:-1]+Xp[:,1:]);gradient=(X[:,1:]-X[:,:-1])/dx;gradient_correction=-gradient[1:].sum(0)-gradient[0];gradient[0]=-gradient[1:].sum(0)
 Tf=.5*(T[:-1]+T[1:]);Dif=BD.binary_diffusivities(Tf,P,allow_below_300=True);Wf=K.W@Xf;rf=P*Wf/(K.R*Tf)
 ff=maxwell_stefan_flux(Xf,gradient,Dif,rf,K.W,trial_extension=bool(np.any(X<0)))
 J=np.zeros((6,N+1));J[:,1:N]=ff['j'];_,lam=K.pure_transport(Tf);kf=.5*(np.sum(Xf*lam,axis=0)+1/np.sum(Xf/lam,axis=0));qcross=np.zeros(N-1);soret=np.zeros((6,N-1))
 if MULTI:
  for j in range(N-1):
   gas.TPX=float(Tf[j]),float(P),Xf[:,j];kf[j]=gas.thermal_conductivity
   if CROSS:
    dt=gas.thermal_diff_coeffs;dt*=Xf[:,j]/np.maximum(Xf[:,j],1e-20);dt[int(np.argmax(Xf[:,j]))]-=dt.sum();soret[:,j]=-dt*(T[j+1]-T[j])/(Tf[j]*dx[j]);drive=np.divide(gradient[:,j],Xf[:,j],out=np.zeros(6),where=Xf[:,j]>0);qcross[j]=-Tf[j]*np.dot(dt*(K.R/K.W),drive)
  J[:,1:N]+=soret
 hb=hsecant(T[:-1],T[1:]);Q=np.zeros(N+1);Q[1:N]=-kf*(T[1:]-T[:-1])/dx+np.sum(hb*J[:,1:N],axis=0)+qcross
 rates=K.signed_rates(T,rho*Y/K.W[:,None])[0];omega=K.W[:,None]*(K.nu@rates);dY=-np.diff(J,axis=1)/MU+omega/rho
 A=-np.diff(Q)/MU-np.sum(h_i*dY,axis=0);Rdot=K.R*np.sum(dY/K.W[:,None],axis=0)
 Pd=0. if MODE=='isobaric' else np.dot(MU,Rmix*A/cp+T*Rdot)/(L0-np.dot(MU,Rmix*v/cp))
 Td=(v*Pd+A)/cp
 if details:
  U=np.dot(MU,np.sum(Y*h_i,axis=0)-Rmix*T);H=np.dot(MU,np.sum(Y*h_i,axis=0));nox=np.dot(MU,1000*np.sum(Y[[4,5]]/K.W[[4,5],None],axis=0))/Mhot
  return {'P_Pa':float(P),'width_m':float(width.sum()),'U_J_m2':float(U),'H_J_m2':float(H),'NOx_mol_per_kg_hot_fresh':float(nox),'max_T_K':float(T.max()),'min_T_K':float(T.min()),'mean_mass_T_K':float(np.dot(MU,T)/MU.sum()),'min_Y':float(Y.min()),'max_abs_mass_flux_sum':float(np.max(abs(ff['diagnostics']['mass_flux_sum_kg_m2_s']))),'radicals_mol_per_kg_hot_fresh':(np.sum(MU*Y[[2,3]]/K.W[[2,3],None],axis=1)*1000/Mhot).tolist(),'pressure_denominator_m':float(width.sum()-np.dot(MU,Rmix*v/cp)),'transport_trial_composition_change':float(np.max(abs(X-Xp))),'gradient_constraint_roundoff_correction_per_m':float(np.max(abs(gradient_correction)))}
 return np.r_[dY[1:].ravel(),Td]

def main():
 prep=time.monotonic()-TOTAL_START;initial=np.r_[Yinit[1:].ravel(),Tinit];initialrec=evaluate(0,initial,True)
 J=lil_matrix((6*N,6*N))
 for i in range(N):
  cols=[k*N+j for k in range(6) for j in range(max(0,i-1),min(N,i+2))]
  for k in range(6):J[k*N+i,cols]=1
 st=time.monotonic();sol=solve_ivp(evaluate,[0,HORIZON],initial,method='BDF',first_step=1e-11,max_step=1e-6,rtol=float(os.environ.get('RTOL','2e-6')),atol=np.r_[np.full(5*N,1e-13),np.full(N,1e-4)],jac_sparsity=J.tocsr() if MODE=='isobaric' else None)
 integration=time.monotonic()-st;recs=[evaluate(t,s,True) for t,s in zip(sol.t,sol.y.T)];final=recs[-1];ener=[r['H_J_m2'] if MODE=='isobaric' else r['U_J_m2'] for r in recs];k0='H_J_m2' if MODE=='isobaric' else 'U_J_m2';below=[float(t) for t,r in zip(sol.t,recs) if r['max_T_K']<=1700]
 np.savez_compressed(D/f'{TAG}_trajectory.npz',t=sol.t,state=sol.y,mu=MU,hot_mass_per_area=Mhot,N=N,mode=MODE,L0=L0)
 out={'scope':__doc__,'success':sol.success,'message':sol.message,'N':N,'mode':MODE,'thermal_cross_terms':CROSS,'native_Tiny_prefactor_restored':CROSS,'multicomponent_conductivity':MULTI,'initial_width_m':L0,'horizon_s':HORIZON,'completed_t_s':float(sol.t[-1]),'initial':initialrec,'final':final,'minimum_over_saved_times_of_max_T_K':min(r['max_T_K'] for r in recs),'first_saved_all_gas_below_1700_s':below[0] if below else None,'conserved_energy_max_drift_J_m2':float(max(abs(np.array(ener)-initialrec[k0]))),'pressure_work_export_J_m2':P0*(final['width_m']-L0) if MODE=='isobaric' else 0.,'internal_energy_plus_pressure_work_residual_J_m2':final['U_J_m2']-initialrec['U_J_m2']+(P0*(final['width_m']-L0) if MODE=='isobaric' else 0.),'minimum_saved_Y':min(r['min_Y'] for r in recs),'max_saved_transport_trial_change':max(r['transport_trial_composition_change'] for r in recs),'nfev':sol.nfev,'njev':sol.njev,'nlu':sol.nlu,'steps':len(sol.t)-1,'preparation_wall_s':prep,'integration_wall_s':integration,'total_wall_s':time.monotonic()-TOTAL_START,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cold_initial_roundoff_projection_L1':float(sum(abs(ycold-rawcold))),'limitations':['Arithmetic MS face is continuum-consistent but lacks the logface unconditional discrete entropy proof','No radiation, injector, wall surface or axial pressure-drop model; Soret/Dufour included only when thermal_cross_terms=true','Material mass-cell geometry expands; not fixed Eulerian width in isobaric mode','Boundary mode changes physical contract','Low-Mach and continuum checks required','No finite apparatus inventory/reset or energy superiority']}
 (D/f'{TAG}_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
if __name__=='__main__':main()
