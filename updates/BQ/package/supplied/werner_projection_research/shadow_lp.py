"""Outer-relaxation diagnostic: feasible LP points need not be quantum states."""
import math, numpy as np
from scipy.optimize import linprog
from pathlib import Path
import json

def comb(n,k):
    return math.comb(n,k) if 0<=k<=n else 0

def probe(n,d=3,K=2):
    D=d**n
    # A_j are the squared error-basis coefficients by operator weight.
    B=np.array([[K/D*sum((-1)**l*(d*d-1)**(k-l)*comb(j,l)*comb(n-j,k-l)
                  for l in range(k+1)) for j in range(n+1)] for k in range(n+1)])
    T=np.array([[d**(-k)*comb(k,j)/comb(n,j) if j<=k else 0
                  for j in range(n+1)] for k in range(n+1)])
    S=np.array([[comb(n,k)/2**n*sum((-1)**l*comb(k,l)*comb(n-k,j-l)
                                 for l in range(j+1))
                 for j in range(n+1)] for k in range(n+1)])@T
    c=np.array([(1-d/2)**(n-j)/D for j in range(n+1)])
    res=linprog(c,A_ub=np.vstack([np.eye(n+1)-B,-S]),b_ub=np.zeros(2*(n+1)),
                A_eq=np.array([[1]+[0]*n,[1]*(n+1)]),b_eq=[1,D/K],
                bounds=[(0,None)]*(n+1),method='highs')
    return {'n':n,'d':d,'rank_projector':K,'success':res.success,
            'relaxed_minimum':res.fun,'A':None if not res.success else res.x.tolist(),
            'warning':'An outer relaxation only; a negative optimum is NOT a distillation witness.'}
if __name__=='__main__':
    out=[probe(n) for n in range(1,10)]
    print(json.dumps(out,indent=2))
    (Path(__file__).parent/'shadow_lp_receipt.json').write_text(json.dumps(out,indent=2))
