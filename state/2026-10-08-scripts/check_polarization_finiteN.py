"""Independent finite-N Schur prediction of macroscopic spin polarization at times c/sqrt N."""
import numpy as np
from math import sqrt
from scipy.linalg import expm
from scipy.special import gammaln
from macroscopic_polarization import polar

def actual(N,nu,c):
    s=c/sqrt(N)
    answer=0
    for M in range(N%2,N+1,2):
        k=np.arange(M+1); down=(nu+1)*k*(M-k+1); up=nu*(M-k)*(k+1)
        Q=np.diag(-(down+up))
        for i in range(M):Q[i+1,i]=up[i];Q[i,i+1]=down[i+1]
        p=expm(Q*s)@(np.ones(M+1)/(M+1))
        z=(N-M)//2
        w=(M+1)**2/(N/2+M/2+1)*np.exp(gammaln(N+1)-gammaln(z+1)-gammaln(N-z+1)-N*np.log(2))
        answer+= w * (M/2-k@p)/sqrt(N)
    return answer
for nu in [.2,1.,10.]:
    for c in [1.,2.]:
        lim=polar(c)
        values=[actual(N,nu,c) for N in [16,32,64,96]]
        print('nu',nu,'c',c,'limit',round(lim,8),'N16,32,64,96',tuple(round(x,8) for x in values),flush=True)
