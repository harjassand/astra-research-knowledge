import numpy as np,json
from scipy.linalg import sqrtm
k=1.;g=.01;N=5
I=np.eye(N);a=[];n=[]
states=[0,1,2,4,6]
for h in [1,2,4]:
 z=np.zeros((N,N))
 for ii,S in enumerate(states):
  if S&h:z[states.index(S^h),ii]=1
 a.append(z);n.append(z.T@z)
H=g*sum((z+z.T for z in a),np.zeros((N,N)))
def LC(O):return 1j*(H@O-O@H)+sum((z.T@O@z-.5*(nn@O+O@nn) for z,nn in zip(a,n)),np.zeros((N,N),complex))
E=[]
for j in range(N*N):
 e=np.zeros((N,N));e.flat[j]=1;E.append(e)
M=np.stack([LC(e).reshape(-1) for e in E],axis=1)
B=[]
for nn in n:
 # Solve LC A + p I = n, fix Tr A=0
 aug=np.zeros((N*N+1,N*N+1),complex);aug[:-1,:-1]=M;aug[:-1,-1]=I.reshape(-1);aug[-1,:-1]=I.reshape(-1)
 rhs=np.r_[nn.reshape(-1),0];sol=np.linalg.solve(aug,rhs);A=sol[:-1].reshape(N,N);A=(A+A.conj().T)/2
 B.append(np.max(np.linalg.eigvalsh(A))*I-A)
 print('p',sol[-1].real,'Bdiag',np.diag(B[-1]).real)
f=[[0,1,1],[0,0,2],[0,1,2]]
def LL(O):return [1j*(H@O[x]-O[x]@H)+sum((z.T@O[fj[x]]@z-.5*(nn@O[x]+O[x]@nn) for z,nn,fj in zip(a,n,f)),np.zeros((N,N),complex)) for x in range(3)]
def T(O,h,t):
 S=np.asarray(sqrtm(t*B[h]),dtype=complex);R=np.asarray(sqrtm(I-t*B[h]),dtype=complex)
 return [R@O[x]@R+S@O[f[h][x]]@S for x in range(3)]
V=[v*I for v in [1,101,102]]
rows=[]
for t in [1e-2,1e-3,1e-4,1e-5]:
 for order in [[0,1,2],[2,1,0]]:
  F=V
  for h in order:F=T(F,h,t)
  drift=LL(F)
  # data 2 only h active; null of initial drift clock ready,j
  mat=drift[2][np.ix_([0,2,3,4],[0,2,3,4])]
  rows.append(dict(t=t,order=order,restricted_eigs_over_t=np.linalg.eigvalsh(mat).tolist(),max_full=float(np.max(np.linalg.eigvalsh(drift[2])))))
print(json.dumps(rows,indent=2))
