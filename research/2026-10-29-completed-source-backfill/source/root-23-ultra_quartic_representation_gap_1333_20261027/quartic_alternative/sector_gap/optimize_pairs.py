"""Bounded ordinary search on the five-variable opposite-determinant pair.

No numerical non-witness is a PC proof. All extrema are exploratory.
"""
import json,time
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution,minimize
from matrix_pair_search import S

def pair(z):
    tm,dm,tp,dp,alpha=z
    minus=np.array([np.cos(tm),np.sin(tm)*np.cos(dm),0,np.sin(tm)*np.sin(dm)])
    plus=np.array([np.cos(tp)*np.cos(alpha),np.sin(tp)*np.cos(alpha+dp),
                   np.cos(tp)*np.sin(alpha),np.sin(tp)*np.sin(alpha+dp)])
    return minus,plus

def objective(z,tau):
    rm,rp=pair(z)
    return float(np.linalg.eigvalsh(S(rp,tau)[0]-S(rm,tau)[0])[0])

def main():
    start=time.monotonic();tau=11.3;eps=1e-5
    bounds=[(eps,np.pi/2-eps),(-np.pi+eps,-eps),(eps,np.pi/2-eps),
            (eps,np.pi-eps),(-np.pi,np.pi)]
    result=differential_evolution(lambda z:objective(z,tau),bounds,seed=20261027,
        popsize=12,maxiter=160,tol=1e-8,polish=True,workers=1)
    rm,rp=pair(result.x);vals,vec=np.linalg.eigh(S(rp,tau)[0]-S(rm,tau)[0])
    out={'status':'NUMERICAL_SEARCH_ONLY','tau':tau,'minimum_eigenvalue':float(vals[0]),
         'parameters':result.x.tolist(),'Rminus':rm.tolist(),'Rplus':rp.tolist(),
         'A':vec[:,0].tolist(),'iterations':result.nit,'evaluations':result.nfev,
         'optimizer_success':bool(result.success),'wall_seconds':time.monotonic()-start,
         'interpretation':'No exact PC or non-PC conclusion before a rigorous certificate'}
    Path('pair_optimization.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
