import numpy as np
from scipy.linalg import expm
from scipy.special import gammaln
from math import log,sqrt

def profile(M,nu,s):
    idx=np.arange(M+1)
    down=(nu+1)*idx*(M-idx+1)
    up=nu*(M-idx)*(idx+1)
    Q=np.diag(-(down+up))
    for k in range(M):
        Q[k+1,k]=up[k];Q[k,k+1]=down[k+1]
    p=expm(s*Q)@(np.ones(M+1)/(M+1))
    q=nu/(nu+1)
    pi=np.exp(idx*np.log(q)-np.log(np.sum(q**idx)))
    return np.abs(p-pi).sum()/2

def weights(N):
    mlist=np.arange(N%2, N+1,2) # M=2j, same parity as N
    out=[]
    for M in mlist:
        j=M/2
        k=int(N/2-j)
        logc=gammaln(N+1)-gammaln(k+1)-gammaln(N-k+1)-N*np.log(2)
        w=(M+1)**2/(N/2+j+1)*np.exp(logc)
        out.append((int(M),w))
    assert abs(sum(w for M,w in out)-1)<2e-10
    return out

if __name__=='__main__':
    nu=.2
    for s in [.1,.5,1.0,2.5]:
        print('s',s,flush=True)
        for N in [8,12,16,24,32,48,64,96]:
            w=weights(N)
            D=sum(wt*profile(M,nu,s) for M,wt in w if M>0)
            print(' N',N,'D',f'{D:.10g}','N^1.5 D',f'{D*N**1.5:.8f}', flush=True)
