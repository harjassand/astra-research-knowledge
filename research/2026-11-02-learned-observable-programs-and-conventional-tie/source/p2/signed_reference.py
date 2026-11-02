"""Microscopic evaluation-only simulator for the extended field mode."""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply
from execute import mean_spin
from source_device import BATHS
from signed_extension import HIDDEN

def reference(n,query,schedule):
    assert n<=10
    baths=[BATHS['baseline'],BATHS['reduced_noise'],HIDDEN]
    size=1<<n
    dist=np.empty(size)
    for x in range(size):
        v=1.
        for i in range(n):
            p=(1+mean_spin(n,i))/2
            v*=p if x>>i&1 else (1-p)
        dist[x]=v
    for dur,mode_map in schedule:
        row=[];col=[];val=[]
        for x in range(size):
            total=0.
            for i in range(n):
                l=1 if x>>((i-1)%n)&1 else -1
                c=1 if x>>i&1 else -1
                r=1 if x>>((i+1)%n)&1 else -1
                rate=baths[mode_map[i]].rate((l,c,r))
                assert rate>0
                row.append(x);col.append(x^(1<<i));val.append(rate)
                total+=rate
            row.append(x);col.append(x);val.append(-total)
        Q=coo_matrix((val,(row,col)),shape=(size,size)).tocsr()
        dist=expm_multiply(Q.T*dur,dist,traceA=float(Q.diagonal().sum())*dur)
    obs=np.array([np.prod([1 if x>>i&1 else -1 for i in query]) for x in range(size)])
    return float(np.dot(dist,obs))
