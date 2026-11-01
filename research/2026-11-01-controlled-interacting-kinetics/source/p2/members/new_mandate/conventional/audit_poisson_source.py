"""Independent physical energy-source audit of PROOFS.txt section 10."""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from audit_gaussian_reference import root, spin_quotient


def check(n):
    rng=np.random.default_rng(9912026+n)
    J=rng.uniform(-1.1,.9,n)
    nu=rng.uniform(.3,1.8,n)
    m=root.model(J,nu)
    Q,K,p=spin_quotient(J,nu)
    walls=[s for s in range(1<<n) if s.bit_count()%2==0]
    energies=[]
    for w in walls:
        spin=np.ones(n,dtype=int)
        for i in range(1,n):
            spin[i]=spin[i-1]*(1-2*((w>>(i-1))&1))
        energies.append(-sum(J[i]*spin[i]*spin[(i+1)%n] for i in range(n)))
    observable=np.asarray(energies)
    f=(observable-p@observable)*np.sqrt(p)
    ground=np.sqrt(p)
    G=np.linalg.inv(K+np.outer(ground,ground))-np.outer(ground,ground)
    chi=float(f@G@f)
    B=m['U'].T@np.diag(2*J)@m['V']
    F=B-B.T
    a,b=np.triu_indices(n,1)
    weights=F[a,b]**2
    rates=m['eps'][a]+m['eps'][b]
    gaussian=float(np.sum(weights/rates))
    correlations=[]
    for t in [0.,.1,1.,10.]:
        exact=float(f@expm(-K*t)@f)
        computed=float(np.dot(weights,np.exp(-rates*t)))
        correlations.append(dict(t=t,absolute_error=abs(exact-computed)))
    _,Ke,_=spin_quotient(J,nu,.7)
    Ge=np.linalg.inv(Ke+np.outer(ground,ground))-np.outer(ground,ground)
    actual=float(f@Ge@f)
    c=1.35;rho=.7/2.7
    R=G/c;E=Ke-c*K
    estimate=0.
    series=[]
    for k in range(6):
        estimate+=(-1)**k*float(f@R@np.linalg.matrix_power(E@R,k)@f)
        series.append(dict(order=k,relative_error=abs(estimate/actual-1),
                           proved_bound=rho**(k+1)))
    return dict(n=n,variance_absolute_error=abs(float(f@f)-weights.sum()),
                reference_relative_error=abs(gaussian/chi-1),
                correlations=correlations,nonintegrable_series=series)


if __name__=='__main__':
    result=dict(scope="independent spin-energy source; full resolvent solves; floating point check",
                checks=[check(n) for n in [4,6,8]])
    Path(__file__).with_name('audit_poisson_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
