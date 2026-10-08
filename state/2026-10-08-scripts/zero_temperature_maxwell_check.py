"""Finite-size numerical check of the exactly derived zero-temperature Maxwell profile."""
from math import comb,sqrt,pi,exp,log,erf
import numpy as np
from scipy.linalg import expm
from scipy.special import gammaln

def total_distance(N,c):
    s=c*log(N)/sqrt(N)
    total=0
    for M in range(N%2,N+1,2):
        if M==0:continue
        l=np.arange(M+1,dtype=float)
        death=l*(M-l+1)
        Q=np.diag(-death)
        for j in range(1,M+1):Q[j-1,j]=death[j]
        p=expm(s*Q)@(np.ones(M+1)/(M+1))
        k=(N-M)//2
        weight=(M+1)**2/(N/2+M/2+1)*np.exp(gammaln(N+1)-gammaln(k+1)-gammaln(N-k+1)-N*log(2))
        total+=weight*max(0,1-p[0])
    return total

def maxwell(x):return erf(x/sqrt(2))-sqrt(2/pi)*x*exp(-x*x/2)
for c in [.2,.5,1.,2.]:
    lim=maxwell(1/(2*c))
    vals=[total_distance(N,c) for N in [16,32,64,96]]
    print('c',c,'Maxwell limit',round(lim,8),'N 16/32/64/96',tuple(round(x,8) for x in vals),flush=True)
