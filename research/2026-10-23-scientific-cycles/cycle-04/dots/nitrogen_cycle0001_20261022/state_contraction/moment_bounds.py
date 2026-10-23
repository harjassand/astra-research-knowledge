"""Sharp finite-table bounds on FORWARD rate at fixed N2 mean excitation.
No assumed Boltzmann law in the feasible class; no reachability claim. The scalar
entropy screen uses a declared finite-ladder caloric split, not the earlier HO.
"""
from pathlib import Path
import sys,json,hashlib,time,resource
import numpy as np
from scipy.optimize import brentq
D=Path(__file__).resolve().parent;ROOT=D.parents[1];sys.path.insert(0,str(D));import contract_on2 as c
sys.path.insert(0,str(ROOT/'nitrogen_finite_cycle_20261021/thermo_helper'));from helper import ThermoKernel
K=ThermoKernel();Ru=K.R/1000;E=np.asarray(c.EN-c.EN[0],float);EV=float(c.EVJ)
p=ROOT/'nitrogen_lamella_20261022/restored_cross_width400um_N48_trajectory.npz';z=np.load(p);N=int(z['N']);s=z['state'];w=z['mu']/float(z['hot_mass_per_area']);mass=w.sum();small=s[:5*N].reshape(5,N,-1);Y=np.concatenate([(1-small.sum(0))[None],small]);T=s[5*N:];yf=Y[:,:,-1]@w/mass;nn=mass*yf[0]/(K.W[0]/1000)
def pop(tv):return np.asarray(c.population(tv),float)
def e(tv):return float(E@pop(tv))*EV
def entropy_pop(q):
 q=q[q>0];return -Ru*float(q@np.log(q))
def hv(t):return mass*float(yf@(K.thermochemistry(np.array([t]))[1][:,0]*K.R*t/K.W))
def seq(y,t):
 y=np.asarray(y)
 if y.ndim==1:y=y[:,None]
 ts=np.atleast_1d(t);x=y/K.W[:,None];x/=x.sum(0);lx=np.zeros_like(x);mask=x>0;lx[mask]=np.log(x[mask]);return np.sum(y*K.R/K.W[:,None]*(K.thermochemistry(ts)[2]-lx),axis=0)
Hi=float(np.dot(w,np.sum(Y[:,:,0]*K.thermochemistry(T[:,0])[1]*K.R*T[:,0]/K.W[:,None],axis=0)));Vi=float(np.dot(w*Y[0,:,0]/(K.W[0]/1000),[e(t) for t in T[:,0]]));mean=Vi/nn/EV
Tb=brentq(lambda t:hv(t)-nn*e(t)+Vi-Hi,1400,1900);Tv=brentq(lambda t:e(t)/EV-mean,300,4000);pb=pop(Tv)
Si=float(np.dot(w,seq(Y[:,:,0],T[:,0])));baseS=mass*float(seq(yf,Tb)[0])-nn*entropy_pop(pop(Tb));rows=[]
for variant in ['literal','corrected_index']:
 kv=np.asarray(c.rates(Tb,variant).sum(axis=1),float);candidates=[]
 for i in range(len(E)):
  if E[i]==mean:
   q=np.zeros(len(E));q[i]=1;candidates.append((float(q@kv),q))
  for j in range(i+1,len(E)):
   if E[i]<=mean<=E[j]:
    a=(mean-E[i])/(E[j]-E[i]);q=np.zeros(len(E));q[i]=1-a;q[j]=a;candidates.append((float(q@kv),q))
 lo=min(candidates,key=lambda x:x[0]);hi=max(candidates,key=lambda x:x[0]);r={'variant':variant,'Boltzmann_forward_k_cm3_s':float(pb@kv),'min_forward_k_cm3_s':lo[0],'max_forward_k_cm3_s':hi[0],'max_over_Boltzmann':hi[0]/float(pb@kv),'min_over_Boltzmann':lo[0]/float(pb@kv)}
 for name,(rate,q) in [('min',lo),('max',hi)]:
  inds=np.flatnonzero(q);r[name+'_support']=[{'v':int(i),'probability':float(q[i]),'excitation_eV':E[i]} for i in inds];r[name+'_mean_error_eV']=float(q@E-mean);r[name+'_global_entropy_J_kgfresh_K']=baseS+nn*entropy_pop(q);r[name+'_entropy_above_initial_J_kgfresh_K']=r[name+'_global_entropy_J_kgfresh_K']-Si
  assert abs(q.sum()-1)<1e-14 and abs(q@E-mean)<1e-12
  assert r[name+'_entropy_above_initial_J_kgfresh_K']>0
 rows.append(r)
out={'scope':__doc__,'proof':'With fixed sum p=1 and sum E*p=mean and p>=0, the feasible compact polytope has extreme points supported on at most two distinct levels. A linear forward-rate objective reaches min/max at such an extreme point; enumerate every bracketing pair. Scalar entropy constraint is inactive at these extrema because both pass the independent global entropy budget.','source_trajectory_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mean_excitation_eV':mean,'stored_N2_vibration_J_kgfresh':Vi,'N2_mol_kgfresh':nn,'same_H_bath_T_K':Tb,'Boltzmann_Tv_K_for_same_mean':Tv,'initial_entropy_J_kgfresh_K':Si,'Boltzmann_constructed_entropy_J_kgfresh_K':baseS+nn*entropy_pop(pb),'rows':rows,'limits':['Finite source-table forward rates only; reverse state weights and six-species closure missing.','No admissible evolution from initial distribution established; a static moment/entropy screen is not kinetics.','Common mean energy does not mean common higher moments or entropy.','Rotational-vibrational coupling of partition weights is not reconstructed; vibrational level probabilities explicitly defined.','Caloric model now subtracts finite-ladder equilibrium energy/entropy from NASA, not harmonic oscillator; original HO example remains unchanged.','QCT potentials and polynomial fits are not certified measurements.','No process gain or all-closure physical exclusion follows.'],'elapsed_s':time.monotonic()-c.START,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'moment_bounds.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
