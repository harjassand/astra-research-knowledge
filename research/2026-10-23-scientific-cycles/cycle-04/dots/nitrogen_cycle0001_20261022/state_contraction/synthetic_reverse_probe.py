"""One-state synthetic reversible completion, NOT source-identified reverse kinetics.
Forward interpolation retained; normalized finite-ladder equilibrium weights and
NASA Kc DEFINE the inverse. No flow solve and no claim of net process benefit.
"""
from pathlib import Path
import sys,json,hashlib,time,resource
import numpy as np
D=Path(__file__).resolve().parent;R=D.parents[1];sys.path.insert(0,str(D));import contract_on2 as c
sys.path.insert(0,str(R/'nitrogen_finite_cycle_20261021/thermo_helper'));from helper import ThermoKernel
K=ThermoKernel();p=R/'nitrogen_lamella_20261022/restored_cross_width400um_N48_trajectory.npz';z=np.load(p);N=int(z['N']);j=int(np.argmin(abs(z['t']-68e-6)));cell=N//2;T=float(z['state'][5*N+cell,j]);ys=z['state'][:5*N,j].reshape(5,N)[:,cell];Y=np.r_[1-ys.sum(),ys];assert Y.min()>0
rho=101325/(K.R*np.sum(Y/K.W)*T);C=rho*Y/K.W*1000;cp,h,ss=K.thermochemistry(np.array([T]));lnK=float(-K.nu[:,2]@(h[:,0]-ss[:,0]));KC=np.exp(lnK);EN=np.asarray(c.EN-c.EN[0],float);EO=np.asarray(c.EO-c.EO[0],float);kbEV=float(c.KB);EV=float(c.EVJ);NA=6.02214076e23

def prob(E,t):
 a=np.exp(-E/(kbEV*t));return a/a.sum()
peN=prob(EN,T);peO=prob(EO,T);rows=[]
for variant in ['literal','corrected_index']:
 f=np.asarray(c.rates(T,variant),float);b=f*peN[:,None]/(KC*peO[None,:])
 assert np.max(abs(f*peN[:,None]-KC*b*peO[None,:])/np.maximum(f*peN[:,None],1e-300))<1e-14
 for Tv in [T,1959.5075393144257,2700.]:
  pn=prob(EN,Tv);po=peO
  F=f*pn[:,None]*C[0]*C[3]*NA*1e-6/rho
  B=b*po[None,:]*C[4]*C[2]*NA*1e-6/rho;J=F-B
  sn=float(np.sum(-EN[:,None]*J)*EV);so=float(np.sum(EO[None,:]*J)*EV)
  sigma=float(K.R/1000*np.sum(J*np.log(F/B)))
  assert sigma>=-1e-12
  rows.append({'variant':variant,'TvN2_K':Tv,'TvNO_K':T,'added_N2_mode_energy_at_fixed_bath_J_kgmixture':float(Y[0]/(K.W[0]/1000)*EV*np.dot(EN,pn-peN)),'forward_mol_kgmixture_s':float(F.sum()),'reverse_mol_kgmixture_s':float(B.sum()),'net_forward_NO_formation_mol_kgmixture_s':float(J.sum()),'N2_mode_energy_source_W_kgmixture':sn,'NO_mode_energy_source_W_kgmixture':so,'chemical_channel_entropy_J_kgmixture_K_s':sigma,'contracted_forward_over_reverse_at_equilibrium':float(np.sum(f*peN[:,None])/np.sum(b*peO[None,:]))})
out={'scope':__doc__,'snapshot':{'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'time_s':float(z['t'][j]),'cell_index':cell,'T_K':T,'Y':Y.tolist(),'rho_kg_m3':rho,'Kc_NASA_dimensionless':KC},'construction':'kb_wv=kf_vw*pN2_eq(v)/(Kc_NASA*pNO_eq(w)); source1/3 already in kf, never applied twice','rows':rows,'limits':['Inverse rates are a declared synthetic completion, not recovered microscopic source data.','Both N2 and NO mode energy/entropy use NASA-minus-finite-ladder equilibrium plus actual-ladder contribution.','NO is constrained to bath population for point comparison; no time evolution, nascent mode relaxation or apparatus modeled.','Pressure1atm and composition are copied from one already-unqualified thermal path; altered modes are counterfactual probes.','Positive entropy follows construction and does not validate kinetics.','Tv scans at fixed bath temperature and composition change total stored energy; they are not equal-energy processes. Added mode energy is reported, but preparation work is not identified.','Full seven reactions, NO2 modes, transport, regeneration and complete reset are absent.'],'elapsed_s':time.monotonic()-c.START,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'synthetic_reverse_probe.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
