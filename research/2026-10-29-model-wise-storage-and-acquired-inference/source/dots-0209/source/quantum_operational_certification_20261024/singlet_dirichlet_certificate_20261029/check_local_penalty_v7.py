import json,math
import numpy as np
from functools import reduce
from scipy.linalg import eigh
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.])
kron=lambda a:reduce(np.kron,a)
rows=[]
for n in (4,6,8):
 D=2**n
 site=lambda a,i:kron([a if j==i else I for j in range(n)])
 spins=[sum(site(a,i) for i in range(n))/2 for a in (X,Y,Z)]
 w,v=eigh(sum(a@a for a in spins));E0=v[:,w<1e-8];d=E0.shape[1];K=2**int(math.log2(d));E=E0[:,:K];P=E0@E0.conj().T;A=site(Z,0)
 qs=[]
 for i in range(n):
  for j in range(i+1,n):
   idx=np.arange(D);bi=(idx>>(n-1-i))&1;bj=(idx>>(n-1-j))&1
   sw=idx^((bi^bj)<<(n-1-i))^((bi^bj)<<(n-1-j));S=np.eye(D)[sw]
   qs.append(float((1-np.trace(P@S@A.conj().T@S@A).real/d)/2))
 q=float(np.mean(qs));B=E.conj().T@A@E;leak=np.eye(K)-B.conj().T@B
 # Pure reset |0><0|. For trace(M rho)|0><0| its Fe contribution is M[0,0]/K².
 Fe=float((abs(np.trace(B))**2+leak[0,0].real)/K**2)
 residual=float(np.linalg.norm(P@A@P))
 assert residual<1e-10 and abs(q-1/(n-1))<1e-12 and abs(Fe-1/K**2)<1e-12
 rows.append(dict(n=n,singlet_dimension=d,logical_dimension=K,singlet_transition_residual=residual,test_failure=q,completed_decoder_Bell_loss=1-Fe,necessary_C=(1-Fe)/q,theorem_C=d/K*(n-1)))
print(json.dumps({'checks':rows,'scope':'Necessary coefficient for this weighted one-edge test only; fixed-state logical-output completion, not erasure.'},indent=2))
