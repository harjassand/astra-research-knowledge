"""Sufficient separability diagnostics; numerical bounds only."""
import json
import numpy as np
from diagnostics import K,C,superop,choi

def invsqrt(a):
    w,v=np.linalg.eigh(a)
    return (v*(1/np.sqrt(w)))@v.T

def whiten(j,d,e,steps=40):
    x=np.eye(d); y=np.eye(e)
    for _ in range(steps):
        t=j.reshape(d,e,d,e)
        ma=np.einsum('iaja->ij',t)
        f=invsqrt(ma)
        ff=np.kron(f,np.eye(e)); j=ff@j@ff.T; x=f@x
        t=j.reshape(d,e,d,e)
        mb=np.einsum('iaib->ab',t)
        f=invsqrt(mb)
        ff=np.kron(np.eye(d),f); j=ff@j@ff.T; y=f@y
        j=j/np.trace(j)
    return j,x,y

def basis(d):
    b=[]
    for i in range(d):
        for k in range(i+1,d):
            z=np.zeros((d,d)); z[i,k]=z[k,i]=1/np.sqrt(2); b.append(z)
    for i in range(1,d):
        z=np.zeros((d,d)); z[np.arange(i),np.arange(i)]=1
        z[i,i]=-i; z/=np.sqrt(i*(i+1)); b.append(z)
    return np.array(b)

def bounds(j,d,e):
    a=basis(d); b=basis(e); t=j.reshape(d,e,d,e)
    corr=np.einsum('nij,mab,iajb->nm',a,b,t)
    u,s,vh=np.linalg.svd(corr,full_matrices=False)
    aa=np.einsum('ik,imn->kmn',u,a)
    bb=np.einsum('ki,imn->kmn',vh,b)
    cost=sum(z*max(abs(np.linalg.eigvalsh(x)))*max(abs(np.linalg.eigvalsh(y)))
             for z,x,y in zip(s,aa,bb))*d*e
    # elementary coordinate rectangle decomposition
    residual=np.diag(j).copy().reshape(d,e)
    for i in range(d):
      for k in range(i,d):
        for a0 in range(e):
          for b0 in range(a0,e):
            if i==k and a0==b0:continue
            c=abs(t[i,a0,k,b0])
            for ii in set([i,k]):
              for aa0 in set([a0,b0]):residual[ii,aa0]-=c
    return dict(purity=float(np.trace(j@j)),
       hs_distance=float(np.linalg.norm(j-np.eye(d*e)/(d*e))),
       standard_ball_radius=float(1/np.sqrt(d*e*(d*e-1))),
       correlation_cost=float(cost),coordinate_residual_min=float(residual.min()),
       min_eig=float(np.linalg.eigvalsh(j)[0]))

a=superop(K);b=superop(np.array([(C@k).T for k in K]));out={}
for name,m,d,e in [('ABA',a@b@a,10,6),('BAB',b@a@b,6,10),('AB',a@b,6,6),('BA',b@a,10,10)]:
    j=choi(m,d,e);j/=np.trace(j);out[name]={'original':bounds(j,d,e)}
    jw,x,y=whiten(j,d,e);out[name]['whitened']=bounds(jw,d,e)
print(json.dumps(out,indent=2))
