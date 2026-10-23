"""Independent entropy feasibility screen of parent caloric construction.
Necessary second-law screen only; not a reachable dynamics certificate.
"""
from pathlib import Path
import importlib.util,numpy as np,json,time
R=Path(__file__).resolve().parent;t=time.monotonic()
sp=importlib.util.spec_from_file_location('caloric',R/'caloric_counterexample.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
k=m.k

def entropy(Y,T):
 T=np.atleast_1d(T);Y=np.asarray(Y)
 if Y.ndim==1:Y=Y[:,None]
 X=Y/k.W[:,None];X/=X.sum(0)
 slog=np.zeros_like(X);mask=X>0;slog[mask]=np.log(X[mask])
 return np.sum(Y*(k.R/k.W[:,None])*(k.thermochemistry(T)[2]-slog),axis=0)
def sv(T):
 x=m.theta/T
 return m.Ru*(x/np.expm1(x)-np.log(-np.expm1(-x)))
Si=float(np.dot(m.weights,entropy(m.Y[:,:,0],m.temp[:,0])))
Seq=m.mass*float(entropy(m.yf,m.Teq)[0])
Sconstructed=m.mass*float(entropy(m.yf,m.Tstored)[0])+m.nNfinal*(sv(m.Tv)-sv(m.Tstored))
assert Si<Sconstructed<Seq
out={'scope':__doc__,'initial_packet_entropy_J_kg_fresh_K':Si,'uniform_equilibrium_entropy_J_kg_fresh_K':Seq,'two_temperature_constructed_entropy_J_kg_fresh_K':Sconstructed,'constructed_minus_initial_J_kg_fresh_K':Sconstructed-Si,'equilibrium_minus_constructed_J_kg_fresh_K':Seq-Sconstructed,'entropy_necessary_condition_pass':True,'attainability_established':False,'pressure_Pa':101325,'energy_contract':'same enthalpy, not same internal energy at fixed volume','elapsed_s':time.monotonic()-t}
(R/'caloric_entropy_check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
