import numpy as np
from scipy.linalg import expm, sqrtm
rng=np.random.default_rng(431)
def kronall(xs):
 z=np.array([[1.]])
 for x in xs:z=np.kron(z,x)
 return z
I=np.eye(2); Z=np.diag([1,-1]); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]])
def majors(n):return [kronall([Z]*j+[p]+[I]*(n-j-1)) for j in range(n) for p in [X,Y]]
def cov(r,c):return np.array([[(1j*np.trace(r@(x@y-y@x))/2).real for y in c] for x in c])
def rootf(G,H):
 n=len(G)//2; A=np.eye(2*n)-G@H; B=np.eye(2*n)-H@G
 T=np.linalg.solve(B.T,(H+G).T).T
 S=np.asarray(sqrtm(np.eye(2*n)+T@T),dtype=np.complex128)
 return np.exp(-n*np.log(2)/2+(np.linalg.slogdet(A)[1]+np.linalg.slogdet(np.eye(2*n)+S)[1])/4)
for n in [1,2,3]:
 c=majors(n); out=[]
 for z in range(8):
  rs=[]
  for k in range(2):
   a=rng.normal(size=(2*n,2*n));a=a-a.T
   h=sum(1j*a[j,k]*c[j]@c[k]/4 for j in range(2*n) for k in range(2*n))
   r=expm(-h);rs.append(r/np.trace(r))
  sr=np.asarray(sqrtm(rs[0]),dtype=np.complex128)
  direct=np.trace(sqrtm(sr@rs[1]@sr)).real
  formula=rootf(cov(rs[0],c),cov(rs[1],c))
  out.append(abs(direct-formula))
 print('n',n,'max absolute discrepancy',max(out))
