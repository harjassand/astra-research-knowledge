"""Caloric construction, not kinetics or a reachable flow trajectory.
Fixed saved final composition, same packet enthalpy; N2 mode energy is separate.
NASA equilibrium enthalpy minus harmonic N2 vibration defines the residual bath.
No equilibrium chemical rates are used away from thermal equilibrium.
"""
from pathlib import Path
import sys,json,time,hashlib,resource
T0=time.monotonic();R=Path(__file__).resolve().parent;ROOT=R.parent
sys.path.insert(0,str(ROOT/'nitrogen_finite_cycle_20261021/thermo_helper'))
from helper import ThermoKernel
import numpy as np
from scipy.optimize import brentq
k=ThermoKernel();p=ROOT/'nitrogen_lamella_20261022/restored_cross_width400um_N48_trajectory.npz';d=np.load(p);N=int(d['N']);s=d['state'];mu=d['mu'];mhot=float(d['hot_mass_per_area']);weights=mu/mhot
Y5=s[:5*N].reshape(5,N,-1);Y=np.concatenate([(1-Y5.sum(0))[None],Y5]);temp=s[5*N:];mass=weights.sum();yf=Y[:,:,-1]@weights/mass
Ru=k.R/1000;theta=3395.;WN=k.W[0]/1000
nNfinal=mass*yf[0]/WN

def ev(T):return Ru*theta/np.expm1(theta/T)
def hv(T):return mass*float(np.dot(yf,k.thermochemistry(np.array([T]))[1][:,0]*k.R*T/k.W))
def vib(T):return nNfinal*ev(T)
Hinitial=float(np.sum(weights*np.sum(Y[:,:,0]*k.thermochemistry(temp[:,0])[1]*k.R*temp[:,0]/k.W[:,None],axis=0)))
Evinitial=float(np.sum(weights*Y[0,:,0]/WN*ev(temp[:,0])))
Teq=brentq(lambda T:hv(T)-Hinitial,1400,2000)
Tstored=brentq(lambda T:hv(T)-vib(T)+Evinitial-Hinitial,1200,2000)
Tv=theta/np.log1p(nNfinal*Ru*theta/Evinitial)
need=Hinitial-hv(1700)+vib(1700)
# Source-polynomial bath cp remains positive across construction bracket.
bathcp=[]
for T in np.linspace(1200,2000,161):
 cp=mass*np.dot(yf,k.thermochemistry(np.array([T]))[0][:,0]*k.R/k.W)
 x=theta/T;cvv=nNfinal*Ru*x*x*np.exp(x)/np.expm1(x)**2
 bathcp.append(cp-cvv)
assert min(bathcp)>0
out={'scope':__doc__,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'theta_N2_K':theta,'packet_mass_kg_per_kg_fresh':mass,'Hinitial_J_kg_fresh':Hinitial,'equilibrium_T_K':Teq,'same_H_same_composition_frozen_initial_N2_vibration_Tbath_K':Tstored,'uniform_vibrational_T_K_for_that_inventory':Tv,'initial_N2_vibration_J_kg_fresh':Evinitial,'required_N2_vibration_at_1700_J_kg_fresh':need,'excess_over_required_J_kg_fresh':Evinitial-need,'min_residual_bath_cp_J_kg_fresh_K':min(bathcp),'actual_reachability_established':False,'closed_reset_advantage_established':False,'limits':['A constructed caloric state, not trajectory or measured partition.','Redistribution into a uniform vibrational temperature is assumed only for the state construction.','Other species modes remain equilibrated with bath.','Frozen N2 mode inventory is a stipulated comparison, not inferred from measured finite relaxation.','NASA minus harmonic N2 defines a caloric model, not exact spectroscopic state populations.','Chemical nonequilibrium entropy production and rates are not assigned.'],'elapsed_s':time.monotonic()-T0,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(R/'caloric_counterexample.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
