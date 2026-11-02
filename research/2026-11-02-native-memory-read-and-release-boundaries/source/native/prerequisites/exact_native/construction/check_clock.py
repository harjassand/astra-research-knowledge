import numpy as np
from scipy.linalg import expm
from functools import reduce
I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1]); ID=np.eye(4)
kron=lambda xs: reduce(np.kron,xs)
P=[[kron([X,I]),kron([I,X]),ID],[kron([Z,I]),kron([I,Z]),ID]]
S=[P[0][0]@P[0][1],P[1][0]@P[1][1]]
K=3; d=K*K*4; H=np.zeros((d,d)); U=np.zeros((d,d)); delta=1.; t=.08
for q in range(K):
 for r in range(K):
  ix=(q*K+r)*4; H[ix:ix+4,ix:ix+4]+=delta*((q!=0)+(r!=0))*ID
  a=ID.copy();b=ID.copy()
  for j in range(q): a=a@P[0][j]
  for j in range(r): b=b@P[1][j]
  U[ix:ix+4,ix:ix+4]=a@b
  for g,v in enumerate([q,r]):
   qs=[q,r]; qs[g]=(v+1)%K; jx=(qs[0]*K+qs[1])*4
   H[jx:jx+4,ix:ix+4]+=-t*P[g][v]
   H[ix:ix+4,jx:jx+4]+=-t*P[g][v]
D=U.T@H@U
print('unitarity',np.linalg.norm(U.T@U-np.eye(d)))
for s in S:
 T=np.kron(np.eye(K*K),s)
 print('dressed stabilizer commutator',np.linalg.norm(D@T-T@D))
# Sector exact eigenvalues, Gibbs free energies including all clock levels.
for beta in [100.,1000.]:
 F={}
 for x in [-1,1]:
  for z in [-1,1]:
   proj=(ID+x*S[0])@(ID+z*S[1])/4
   vals,vecs=np.linalg.eigh(proj); v=vecs[:,np.argmax(vals)]
   V=np.kron(np.eye(K*K),v[:,None]); eig=np.linalg.eigvalsh(V.T@D@V)
   F[x,z]=eig[0]-np.log(np.exp(-beta*(eig-eig[0])).sum())/beta
 c=sum(F.values())/4; jx=-sum(x*f for (x,z),f in F.items())/4; jz=-sum(z*f for (x,z),f in F.items())/4; jxz=-sum(x*z*f for (x,z),f in F.items())/4
 print('beta',beta,'Jx',jx,'Jz',jz,'Jxz',jxz,'leading',2*t**K/delta**(K-1))
