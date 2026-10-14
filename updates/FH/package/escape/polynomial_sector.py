"""Low-degree trial fields with a globally acquired slow-sector certificate.
Low-degree is a trial space, not a premise about the exact solution.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
import time,json
import numpy as np
from refine_sector import RefinedRing

def run(n,t,degree=2,nu=F(1),kappa=F(1),bits=32):
    started=time.perf_counter(); R=RefinedRing(n,F(t),F(nu),F(kappa));R.setup()
    setup=time.perf_counter()
    ids=[0]
    for p in range(1,degree+1):
        ids += [sum(1<<i for i in subset) for subset in combinations(range(n),p)]
    Kcols=[R.Kfloat({mask:1.}) for mask in ids]
    M=np.array([[sum(float(v)*R.corrfloat(mask^key) for key,v in col.items()) for col in Kcols] for mask in ids])
    b=np.array([R.corrfloat(mask) for mask in ids])
    M=(M+M.T)/2
    a=np.linalg.solve(M,b)
    proposed=time.perf_counter()
    ans=R.certificate(dict(zip(ids,a)),bits)
    ended=time.perf_counter()
    ans.update(n=n,t=str(t),nu=str(nu),kappa=str(kappa),degree=degree,bits=bits,
               setup_s=setup-started,proposal_s=proposed-setup,certification_s=ended-proposed,total_s=ended-started,
               gamma_complement=float(R.gamma),lambda_slow=float(R.lambdaslow))
    return ans
if __name__=='__main__':
    import sys
    n=int(sys.argv[1]);t=F(sys.argv[2]);degree=int(sys.argv[3]);dest=sys.argv[4]
    out=run(n,t,degree)
    json.dump(out,open(dest,'w'))
    print(json.dumps({k:v for k,v in out.items() if k not in ['witness','lower_exact','upper_exact']}))
