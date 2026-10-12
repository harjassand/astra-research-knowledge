"""Checks of the compressed repeated deterministic-control reduction over F2."""
import itertools
import numpy as np
from scipy.linalg import expm

def parity(x): return x.bit_count()&1
def apply(C,x): return sum(parity(row&x)<<i for i,row in enumerate(C))
def rank(vectors,D):
    basis={}
    for v in vectors:
        while v:
            p=v.bit_length()-1
            if p in basis: v^=basis[p]
            else: basis[p]=v;break
    return len(basis)

def recurrence_check(D=3):
    matrices=[C for C in itertools.product(range(1<<D),repeat=D) if rank(C,D)==D]
    tested=0; worst=1
    for C in matrices:
        for c in range(1,1<<D):
            values=[c]
            for _ in range(4*D): values.append(apply(C,values[-1]))
            for ell in range(1,1<<D):
                sequence=[parity(ell&v) for v in values]
                active=any(sequence[:D])
                for N in range(D,4*D+1):
                    count=sum(sequence[:N])
                    if active:
                        assert count>=N//D
                        assert count/N>=1/(2*D)
                        worst=min(worst,count/N)
                    else: assert count==0
                    tested+=1
    print(f'recurrence: D={D}, invertible matrices={len(matrices)}, scalar-prefix cases={tested}, minimum active density={worst:.4g}')

def controlled_endpoint_check(N=7,theta=0.6):
    D=3; n=1<<D; C=(3,6,4); initial=1
    # F(U)=u1*u2*e3, so the nonzero mark has probability 1/4.
    Q=np.zeros((n,n))
    for x in range(n): Q[x,x^4]+=theta/4;Q[x,x]-=theta/4
    interval=expm(Q)[0]
    law=np.zeros(n);law[initial]=1
    for _ in range(N):
        nxt=np.zeros(n)
        for x in range(n):
            for z in range(n): nxt[apply(C,x)^z]+=law[x]*interval[z]
        law=nxt
    G=np.zeros((n,n));mark=4
    for _ in range(N):
        for x in range(n): G[x,x^mark]+=theta/4;G[x,x]-=theta/4
        mark=apply(C,mark)
    shift=initial
    for _ in range(N): shift=apply(C,shift)
    aggregated=expm(G)[0]
    check=np.array([aggregated[x^shift] for x in range(n)])
    error=np.max(abs(law-check))
    print(f'control-plus-noise phase ordering: N={N}, endpoint residual={error:.3g}')
    assert error<1e-12

if __name__=='__main__':
    recurrence_check()
    for N in (1,2,3,7,12): controlled_endpoint_check(N)
