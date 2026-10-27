"""Broader pointwise positivity attempt: |A|^2 times closed heat biform SOS.
Numerical only unless separately rationalized and verified exactly.
"""
from pathlib import Path
import numpy as np,itertools,json,time
OUT=Path(__file__).parent
d=np.load(OUT/'interfaces.npz');p=np.array([1,1,16,-13,0,0,4,-4,0.])
xpairs=[(i,j) for i in range(4) for j in range(i,4)]
zpairs=[(i,j) for i in range(6) for j in range(i,6)]
def exp(pair,n):
 e=np.zeros(n,dtype=int)
 for i in pair:e[i]+=1
 return tuple(e)
xe=[exp(pair,4) for pair in xpairs];ze=[exp(pair,6) for pair in zpairs]
x4=sorted(set(tuple(a+b for a,b in zip(c,e)) for c in xe for e in xe))
lookup={(xx,zz):21*h+k for h,xx in enumerate(x4) for k,zz in enumerate(ze)}
L=np.zeros((735,210))
for h,xx in enumerate(xe):
 for k,zz in enumerate(ze):
  for i in range(4):
   lifted=list(xx);lifted[i]+=2;L[lookup[tuple(lifted),zz],21*h+k]+=1
ON=L@d['ON'];U,sig,_=np.linalg.svd(ON,full_matrices=True);assert np.count_nonzero(sig>1e-8)==45
D=U[:,45:].T
feature=[(xx,i) for xx in xe for i in range(6)]
ij=np.triu_indices(60);wt=np.where(ij[0]==ij[1],1.,np.sqrt(2.))
P=np.zeros((735,len(ij[0])))
for h,(i,j) in enumerate(zip(*ij)):
 xx=tuple(a+b for a,b in zip(feature[i][0],feature[j][0]));zz=exp((feature[i][1],feature[j][1]),6)
 P[lookup[xx,zz],h]=1. if i==j else np.sqrt(2.)
Ed=L@d['Ed'];Ef=L@d['E']@p
T=np.column_stack((D@P,D@Ed));rhs=D@Ef
Ti=np.linalg.pinv(T,rcond=1e-10);anchor=Ti@rhs
print('lifted affine',T.shape,'residual',np.linalg.norm(T@anchor-rhs),flush=True)

def mat(v):
 M=np.zeros((60,60));M[ij]=v/wt;M[(ij[1],ij[0])]=v/wt;return M

def vech(M):return M[ij]*wt

for margin in [0.,1e-5]:
 y=anchor.copy();dual=y*0;tick=time.monotonic()
 for step in range(20000):
  v=y-dual;xx=v+Ti@(rhs-T@v)
  ev,V=np.linalg.eigh(mat(xx[:-1]+dual[:-1]));yp=np.r_[vech((V*np.maximum(ev,margin))@V.T),max(0.,xx[-1]+dual[-1])]
  dual+=xx-yp;res=float(np.linalg.norm(xx-yp));change=float(np.linalg.norm(yp-y));y=yp
  if step%1000==0:print(json.dumps({'margin':margin,'step':step,'residual':res,'change':change,'gamma':float(xx[-1]),'seconds':time.monotonic()-tick}),flush=True)
  if res<1e-9 and change<1e-9:break
 omega=np.linalg.lstsq(ON,P@xx[:-1]+xx[-1]*Ed-Ef,rcond=None)[0]
 np.savez(OUT/f'lifted_candidate_{margin:g}.npz',gram=mat(xx[:-1]),gamma=xx[-1],omega=omega,L=L,P=P,Ed=Ed,Ef=Ef,dual=dual)
 print('FINAL',margin,step,res,change,float(np.linalg.eigvalsh(mat(xx[:-1]))[0]),flush=True)
