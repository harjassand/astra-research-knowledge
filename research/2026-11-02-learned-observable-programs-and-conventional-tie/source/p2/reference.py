"""Full microscopic CTMC reference for small chains. EVALUATION ONLY.
The source model is not imported into the learner/compiler.
"""
import math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply
from source_device import PrivateBath
from execute import mean_spin

def generator(n,mode_map,baths):
    size=1<<n
    rows=[];cols=[];dat=[]
    for x in range(size):
        diag=0.
        for i in range(n):
            spins=tuple(1 if x>>(j%n)&1 else -1 for j in (i-1,i,i+1))
            c=baths['reduced_noise' if mode_map[i] else 'baseline'].rate(spins)
            assert c>0
            rows.append(x);cols.append(x^(1<<i));dat.append(c)
            diag+=c
        rows.append(x);cols.append(x);dat.append(-diag)
    return coo_matrix((dat,(rows,cols)),shape=(size,size)).tocsr()

def exact_reference(n,query,forward_schedule,baths):
    assert n<=12
    m=np.array([mean_spin(n,i) for i in range(n)])
    dist=np.empty(1<<n)
    for x in range(1<<n):
        prob=1.
        for i in range(n):
            prob *= (1+m[i])/2 if x>>i&1 else (1-m[i])/2
        dist[x]=prob
    for dur,mode in forward_schedule:
        Q=generator(n,mode,baths)
        dist=expm_multiply(Q.T*dur,dist,traceA=float(Q.diagonal().sum())*dur)
    obs=np.array([math.prod(1 if x>>i&1 else -1 for i in query) for x in range(1<<n)])
    return float(np.dot(dist,obs))
