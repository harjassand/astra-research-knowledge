"""Finite CTMC checks only. Not a quantum compiler verification."""
import numpy as np
from scipy.linalg import solve
import json

def cycle(D,r,k):
    Q=np.zeros((D+1,D+1))
    Q[0,1]=r
    for j in range(1,D): Q[j,j+1]=k
    Q[D,0]=k
    Q-=np.diag(Q.sum(axis=1))
    pi=np.array([k]+[r]*D)/(k+D*r)
    return Q,pi
out=[]
for D in [1,2,4,8]:
 for r in [.1,.01,.001]:
    k=1.; Q,pi=cycle(D,r,k); n=D+1
    Q2=np.kron(Q,np.eye(n))+np.kron(np.eye(n),Q)
    p2=np.kron(pi,pi)
    busy=np.array([0]+[1]*D); I=np.kron(busy,busy)
    f=D*r/(k+D*r)
    M=Q2.copy(); b=-(I-f*f); M[0,:]=0;M[0,0]=1;b[0]=0
    h=solve(M,b);h-=h.min()
    residual=np.max(abs(Q2@h+I-f*f))
    tau=1/r+D/k
    floor=2*k*tau*f*f
    assert residual<1e-9
    assert h.max()<=8*np.exp(4)*D/k+1e-9
    out.append(dict(D=D,r=r,poisson_residual=float(residual),h_span=float(h.max()),collision_floor=float(floor),source_pair_height=float(2*k*tau*h.max())))
print(json.dumps(out,indent=2))
