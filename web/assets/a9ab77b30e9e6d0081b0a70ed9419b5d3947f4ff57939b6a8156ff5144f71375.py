"""Exact symbolic and independent Fock checks for optimal Gaussian filtering."""
import math,json,sys
from pathlib import Path
import numpy as np
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from gaussian_robustness import *
phi=np.zeros(16);phi[3]=phi[12]=1/math.sqrt(2)
def rho(e):
    r=e*e*np.outer(phi,phi);r[0,0]+=(1-e)**2
    for j in range(4):r[1<<j,1<<j]+=e*(1-e)/2
    return r
maxerr=maxrob=0.;cases=0
for q in [.2,.4,.5,.58,math.sqrt(2)/(1+math.sqrt(2))]:
    for e in [.01,.05,.1,q]:
        if e>q:continue
        info=optimal_loss_concentration(e,q);s=info['empty_mode_survival_s'];p=info['all_four_success_probability']
        k=np.diag([s**((4-i.bit_count())/2) for i in range(16)])
        out=k@rho(e)@k
        maxerr=max(maxerr,float(np.max(abs(out-p*rho(q)))))
        maxrob=max(maxrob,abs(p-info['optimality_bound']))
        assert np.max(np.diag(k))<=1+1e-12
        # Each first-failure branch is diagonal: thus a Slater mixture.
        for j in range(4):
            diag=[]
            for mask in range(16):
                prior=sum(not (mask>>i&1) for i in range(j))
                diag.append(0. if mask>>j&1 else math.sqrt(1-s)*s**(prior/2))
            f=np.diag(diag);failed=f@rho(e)@f
            assert np.max(abs(failed-np.diag(np.diag(failed))))<1e-12
        cases+=1
assert max(maxerr,maxrob)<1e-11
e,q=sp.symbols('e q',positive=True);s=e*(1-q)/(q*(1-e))
p=e**4*(1-q)**2/(q**4*(1-e)**2)
identities=[(1-e)**2*s**4-p*(1-q)**2,e*(1-e)*s**3-p*q*(1-q),e**2*s**2-p*q**2,
            p*(q**4/(4*(1-q)**2))-e**4/(4*(1-e)**2)]
assert all(sp.simplify(v)==0 for v in identities)
result={"status":"all assertions passed","parameter_pairs":cases,"first_failure_gaussian_branch_checks":4*cases,
        "exact_symbolic_identities":len(identities),"max_density_identity_error":maxerr,"max_robustness_saturation_error":maxrob,
        "example_eta_0_1_to_half":optimal_loss_concentration(.1,.5)}
Path(__file__).with_name('concentration_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
