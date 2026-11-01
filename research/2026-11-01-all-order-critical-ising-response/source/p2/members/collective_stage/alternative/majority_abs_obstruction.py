"""Fixed physical contrast does not control signed-dual absolute variance.

A_i=1+(3/5)Maj(s_(i+1),s_(i+2),s_(i+3)), with
Maj(x,y,z)=(x+y+z-xyz)/2. Every rate stays in [.4,1.6] times its
clock, but the absolute Walsh perturbation has row sum 6/5 exactly.
The physical generator is reconstructed independently for a small check.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh


def matrices(n,nu):
    size=2**n-1
    d=np.array([2*sum(nu[i] for i in range(n) if s>>i&1) for s in range(1,2**n)])
    E=np.zeros((size,size))
    for s in range(1,2**n):
        for i in range(n):
            if not(s>>i&1):continue
            neigh=[(i+j)%n for j in [1,2,3]]
            for R,a in [([neigh[0]],.3),([neigh[1]],.3),([neigh[2]],.3),(neigh,-.3)]:
                t=s
                for j in R:t^=1<<j
                assert t!=0
                E[s-1,t-1]+=2*nu[i]*a
    C=E/np.sqrt(d[:,None]*d[None,:])
    abs_rows=np.abs(E).sum(axis=1)/d
    K=E+np.diag(d)
    return d,E,C,K,abs_rows


def physical_check(n):
    size=2**n
    K=np.zeros((size,size))
    H=np.empty((size,size))
    for x in range(size):
        spin=[1 if x>>i&1 else -1 for i in range(n)]
        for i in range(n):
            val=sum(spin[(i+j)%n] for j in (1,2,3))
            rate=1+.6*(1 if val>0 else -1)
            y=x^(1<<i)
            K[x,x]+=rate;K[y,x]-=rate
        for s in range(size):
            v=1
            for i in range(n):
                if s>>i&1:v*=spin[i]
            H[x,s]=v/np.sqrt(size)
    dw,E,C,Kw,rows=matrices(n,np.ones(n))
    return float(np.max(np.abs((H.T@K@H)[1:,1:]-Kw)))


if __name__=='__main__':
    out={'exact_rate_contrast':[.4,1.6],
         'exact_absolute_kernel_spectral_radius':'6/5',
         'proof':'Every nonempty row of |D^-1 E| sums to 6/5; Fourier singleton terms have one sign and triple terms the other, so component contributions with common XOR endpoint never cancel.',
         'physical_walsh_transform_max_error':physical_check(6),'cases':[]}
    for n in (4,6,8):
        for stiff in (False,True):
            nu=np.array([1e-20 if stiff and i%2==0 else 1. for i in range(n)])
            d,E,C,K,rows=matrices(n,nu)
            eigen=eigvalsh(C)
            out['cases'].append({'n':n,'stiff':stiff,
                'absolute_row_min':float(rows.min()),'absolute_row_max':float(rows.max()),
                'symmetric_relative_spectral_radius':float(max(abs(eigen))),
                'row_bound_failure':bool(rows.min()>1),
                'fixed_contrast_spectral_bound_holds':bool(max(abs(eigen))<=.6+1e-12)})
    path=Path(__file__).with_name('majority_abs_obstruction_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
