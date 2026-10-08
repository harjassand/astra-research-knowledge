"""Independent sector checks for a proposed sharp collective-thermal relaxation theorem."""
import numpy as np
from scipy.linalg import expm
from scipy.special import gammaln
from math import log,sqrt,pi

def sector(M,nu,s):
    i=np.arange(M+1,dtype=float)
    dn=(nu+1)*i*(M-i+1)
    up=nu*(M-i)*(i+1)
    Q=np.diag(-(dn+up))
    for k in range(M): Q[k+1,k]=up[k];Q[k,k+1]=dn[k+1]
    u=np.ones(M+1)/(M+1)
    p=expm(Q*s)@u
    q=nu/(nu+1)
    z=q**i; pi=z/z.sum()
    d=.5*np.sum(np.abs(p-pi))
    c=(sqrt(nu+1)-sqrt(nu))**2
    h=np.sum(1/np.arange(1,M+1))
    bound=2*np.exp(-log(2)*s*(M+1)/(8*h))+.5*sqrt(nu)*np.exp(-c*M*s/2)
    hitting=np.sum([(1-q**(M-k+1))/(k*(M-k+1)) for k in range(1,M+1)])
    return d,bound,hitting,2*h/(M+1),Q

ncheck=0
for nu in [.01,.2,1.,10.]:
    for M in [1,2,3,4,8,16,24]:
        for s in [.01,.1,.5,1.,2.5]:
            d,b,hit,hmax,Q=sector(M,nu,s)
            assert d<=b+1e-9,(M,nu,s,d,b)
            assert hit<=hmax+1e-9,(M,nu,hit,hmax)
            assert np.max(abs(Q.sum(axis=0)))<1e-7
            ncheck+=1
print(f'PASS: {ncheck} exact-matrix-exponential sector checks of stochasticity, hitting bound, total-variation envelope')
for nu,s in [(.2,1.),(.2,2.5)]:
    for parity in [0,1]:
        vals=[]
        for M in range(2 if parity==0 else 1,49,2):
            if M%2!=parity:continue
            d,b,*_=sector(M,nu,s)
            vals.append((M,d,b))
        C=2*sqrt(2/pi)*sum((M+1)**2*d for M,d,_ in vals)
        print(f'approx asymptotic parity constant ν={nu}, s={s}, N%2={parity}:',round(C,8),'max M',vals[-1][0], 'last 2 contributions',[(M,round((M+1)**2*d,8)) for M,d,_ in vals[-2:]])
