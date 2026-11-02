"""Small quantum-clock Gibbs and Holder checks; not a protected-code simulation."""
import numpy as np,json
from scipy.linalg import expm
from scipy.special import logsumexp
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.]);D=np.eye(4)
P=[[np.kron(X,I),np.kron(I,X),D],[np.kron(Z,I),np.kron(I,Z),D]]
S=[P[0][0]@P[0][1],P[1][0]@P[1][1]]
K=3;delta=20.;t=(delta**2/4)**(1/3);beta=2.
H=np.zeros((36,36));U=np.zeros_like(H)
for q in range(K):
 for r in range(K):
  k=(q*K+r)*4; H[k:k+4,k:k+4]+=delta*((q!=0)+(r!=0))*D
  u=D.copy()
  for a,n in enumerate([q,r]):
   for j in range(n):u=u@P[a][j]
  U[k:k+4,k:k+4]=u
  for a,n in enumerate([q,r]):
   c=[q,r];c[a]=(n+1)%3;l=(c[0]*K+c[1])*4
   H[l:l+4,k:k+4]-=t*P[a][n];H[k:k+4,l:l+4]-=t*P[a][n]
Hd=U.T@H@U
Vs={};Ha={};Za={}
for sx in [-1,1]:
 for sz in [-1,1]:
  p=(D+sx*S[0])@(D+sz*S[1])/4;ev,v=np.linalg.eigh(p);w=v[:,np.argmax(ev)]
  Q=np.kron(np.eye(9),w[:,None]);s=(sx,sz);Vs[s]=Q;Ha[s]=Q.T@Hd@Q;Za[s]=np.trace(expm(-beta*Ha[s]))
# Local physical perturbation, not commuting with the exact dressed syndrome algebra.
clock=np.zeros((3,3));clock[0,1]=clock[1,0]=1
V=np.kron(np.eye(9),np.kron(X,I))+.3*np.kron(np.kron(clock,np.eye(3)),D)
records=[]
for v in [1e-4,1e-3,1e-2]:
 G=U.T@expm(-beta*(H+v*V))@U
 changes={str(s):float(np.log(np.trace(Q.T@G@Q)/Za[s])) for s,Q in Vs.items()}
 osc=max(changes.values())-min(changes.values());records.append(dict(v=v,log_weight_changes=changes,oscillation=osc))
# Two insertion history across different syndrome sectors with unit-norm matrices.
s0=(-1,-1);s1=(-1,1);B=np.zeros((9,9));B[1,0]=1;C=B.T
A=expm(-beta*.2*Ha[s0])@B@expm(-beta*.3*Ha[s1])@C@expm(-beta*.5*Ha[s0])
lhs=abs(np.trace(A));bound=Za[s0]**.7*Za[s1]**.3
assert lhs<=bound*(1+1e-12)
N=36
block=np.zeros((3*N,3*N))
for j in range(3):block[j*N:(j+1)*N,j*N:(j+1)*N]=-beta*H
for j in range(2):block[j*N:(j+1)*N,(j+1)*N:(j+2)*N]=-beta*V
expblock=expm(block);C1=U.T@expblock[:N,N:2*N]@U;C2=U.T@expblock[:N,2*N:]@U
coeffs={str(s):dict(first=float(np.trace(Q.T@C1@Q)/Za[s]),second=float(np.trace(Q.T@C2@Q)/Za[s])) for s,Q in Vs.items()}
res=dict(dyson_coefficients=coeffs,scope='Two data qubits, XX/ZZ checks, no logical qubit. Full 36-dimensional thermal matrix. Corroborates insertion inequality only.',holder_lhs=float(lhs),holder_bound=float(bound),holder_ratio=float(lhs/bound),perturbations=records)
print(json.dumps(res,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(res,indent=2)+'\n')
