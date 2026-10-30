import numpy as np, math,json
from scipy.sparse.linalg import spsolve
from tree_residual_matrix import matrix,HEIGHTS
from joint_matrix import fall
K=8;alpha=.2;eta=.1;h=HEIGHTS[K];V={}
for R in range(8,85):
 M=matrix(R,K,alpha,eta)
 v=spsolve(-M.T,np.ones(M.shape[0]));ix={};j=0
 for b in range(K+1):
  for c in range(R+h[b]+1):ix[(c,b)]=j;j+=1
 V[R]=(v,ix)
 if min(v)<=0:print('NONPOS',R,min(v),flush=True)
# physical species order A,C,B
Y=[(0,0,0),(1,0,1),(3,0,4),(2,1,4),(1,2,4),(0,3,4)]
E=[(0,1,1),(1,2,1),(2,0,1),(5,4,6),(4,5,12),(4,3,1),(3,4,1),(3,2,7),(2,3,1)]
def logmu(x):
 a,c,b=x
 if min(x)<0 or b>K:return None
 R=a+c-h[b]
 if R not in V:return None
 v,ix=V[R]
 return -alpha*math.lgamma(R+1)+math.log(v[ix[(c,b)]])
def rate(x,y,k):return k*fall(x[0],y[0])*fall(x[1],y[1])*fall(x[2],y[2])
worst=[];positive=0;tested=0
for R in range(15,78):
 for b in range(K+1):
  for c in range(R+h[b]+1):
   x=(R+h[b]-c,c,b);lx=logmu(x);q=sum(rate(x,Y[i],k) for i,j,k in E);inc=0
   for i,j,k in E:
    prev=tuple(x[t]-Y[j][t]+Y[i][t] for t in range(3));lp=logmu(prev)
    if lp is not None:inc+=rate(prev,Y[i],k)*math.exp(lp-lx)
   err=(inc-q)/max(q,1);tested+=1
   if err>1e-8:
    positive+=1;worst.append((err,x,R))
worst.sort(reverse=True)
print('SUMMARY',tested,positive,worst[:15],flush=True)
json.dump({'tested':tested,'positive':positive,'worst':worst[:30],'alpha':alpha,'eta':eta,'K':K},open('chemical_joint_shell_20261030/ACTUAL_JOINT_CHECKS.json','w'),indent=2)
