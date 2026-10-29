import numpy as np,json,itertools
from pathlib import Path
from functools import reduce
from scipy.spatial.transform import Rotation
rng=np.random.default_rng(2026102912);p=Path(__file__).with_name('check_exact_nonunital_v1.npz');data=np.load(p);N=data['channel'];Ttrue=data['Ts'];O=data['O'];J=data['Jembed'];n=4;D=16
P=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex);kron=lambda xs:reduce(np.kron,xs)
states=[(P[0]+sign*P[axis])/2 for axis in [1,2,3] for sign in [1,-1]];configs=np.array(list(itertools.product(range(6),repeat=n)),int);inputrho=np.stack([kron([states[x] for x in c]).reshape(-1) for c in configs]);out=inputrho@N.T
axes=np.array(list(itertools.product(range(3),repeat=n)),int);bits=np.array(list(itertools.product(range(2),repeat=n)),int)
projectors=np.stack([kron([states[2*a+b] for a,b in zip(ax,bit)]).reshape(-1) for ax in axes for bit in bits]);prob=(out@projectors.conj().T).real.reshape(len(configs),len(axes),D);prob=np.maximum(prob,0);prob/=prob.sum(axis=2)[:,:,None]
sums=np.zeros((n-1,16,9));done=0;rows=[]
def polar(A):
 u,s,v=np.linalg.svd(A);return u@np.diag([1,1,np.linalg.det(u@v)])@v
def rounding(v):
 A=np.sqrt(3)*v.reshape(3,3);cs=[polar(A),polar(-A)];return cs[0] if np.linalg.norm(cs[0]-A)<=np.linalg.norm(cs[1]+A) else cs[1]
for target in [10000,100000,1000000]:
 while done<target:
  m=min(100000,target-done);ii=rng.integers(len(configs),size=m);zz=rng.integers(len(axes),size=m);cdf=np.cumsum(prob[ii,zz],axis=1);yy=(rng.random(m)[:,None]>cdf).sum(axis=1);yy=np.minimum(yy,D-1)
  ci=configs[ii]//2+1;si=1-2*(configs[ii]%2);zi=axes[zz];yi=1-2*bits[yy]
  for i in range(1,n):
   col=3*zi[:,i]+zi[:,0];base=9*yi[:,i]*yi[:,0]
   for row,w in [(np.zeros(m,int),base),(4*ci[:,i],3*si[:,i]*base),(ci[:,0],3*si[:,0]*base),(4*ci[:,i]+ci[:,0],9*si[:,i]*si[:,0]*base)]:
    sums[i-1]+=np.bincount(row*9+col,weights=w,minlength=144).reshape(16,9)
  done+=m
 errors=[]
 for i in range(1,n):
  That=sums[i-1]/done;_,sv,v=np.linalg.svd(That-J);Chat=rounding(v[-1]);C=O[i]@O[0].T;errors.append({'pair':[i,0],'operator_estimation_error':float(np.linalg.norm(That-Ttrue[i-1],2)),'frame_F_error':float(np.linalg.norm(Chat-C)),'estimated_smallest_singular':float(sv[-1]),'estimated_second_smallest_singular':float(sv[-2])})
 rows.append({'full_array_calls':done,'physical_preparations_and_readouts_each':n*done,'pair_results':errors})
print(json.dumps({'seed':2026102912,'scope':'Actual independent product-Pauli inputs and simultaneous local output outcomes sampled from one full nonunital global channel per shot; no independent synthetic pair banks','results':rows,'finite_confidence_status':'These are empirical estimator/frame checks, not a claim that the conservative declared concentration stopping threshold is met at these sample counts.'},indent=2))
