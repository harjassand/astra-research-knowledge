"""Numerical identity/stress checks for analytic spin-character concentration lemma.
No claim about all-size proof or new priority.
"""
import json
import numpy as np
from scipy.linalg import expm

def spin_matrices(twice_j):
    j=twice_j/2
    m=np.arange(-j,j+1)
    D=len(m)
    Jz=np.diag(m)
    Jx=np.zeros((D,D))
    for k,mm in enumerate(m[:-1]):
        Jx[k,k+1]=Jx[k+1,k]=0.5*np.sqrt((j-mm)*(j+mm+1))
    return j,Jz,Jx

def stable_character(y,j):
    return np.exp(np.arange(-j,j+1)*y).sum()

def run():
    worst_id=0.; worst_bound=0.; checks=0
    nu_values=[0.01,0.2,1.,5.]
    t_values=[-1.5,-.7,-.2,0.,.2,.7,1.5]
    for twice_j in range(1,17):
        j,Jz,Jx=spin_matrices(twice_j)
        for nu in nu_values:
            beta=np.log1p(1/nu)
            C=2*nu+1
            rho=expm(-beta*Jz);rho/=np.trace(rho)
            for t in t_values:
                value=float(np.trace(rho@expm(t*Jx)).real)
                eta=2*np.arccosh(np.cosh(beta/2)*np.cosh(t/2))
                formula=stable_character(eta,j)/stable_character(beta,j)
                bound=np.exp(j*C*t*t/4)
                err=abs(value-formula)/max(1.,value)
                worst_id=max(worst_id,err)
                worst_bound=max(worst_bound,max(0.,value/bound-1))
                if err>2e-10:raise RuntimeError(('character mismatch',j,nu,t,err))
                if value>bound*(1+5e-12):raise RuntimeError(('subGaussian failure',j,nu,t,value,bound))
                checks+=1
    result={'checks':checks,'j_values':'1/2 to 8, by 1/2','nu_values':nu_values,'t_values':t_values,'maximum_relative_character_discrepancy':worst_id,'largest_bound_excess':worst_bound,'status':'all numerical checks passed','limitation':'Finite numerical verification only; analytic derivation is separate.'}
    print(json.dumps(result,indent=2))
    with open('spin_character_checks.json','w') as f:json.dump(result,f,indent=2)
    return result
if __name__=='__main__':run()
