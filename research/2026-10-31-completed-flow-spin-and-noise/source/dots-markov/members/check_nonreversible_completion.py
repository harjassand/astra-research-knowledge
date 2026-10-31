"""Dense diagnostic of a nonreversible three-state completion.
Not a certified source or a general quantum compiler implementation.
"""
import json,numpy as np
from scipy.linalg import expm
Q=np.array([[-3,2,1],[1,-5,4],[3,1,-4]],float)
pi=np.array([16,9,13],float)/38
psi=np.sqrt(pi);P=np.outer(psi,psi);Pe=np.eye(3)-P
Ls=[]
for x in range(3):
 for y in range(3):
  if x==y:continue
  L=np.zeros((3,3),complex);L[y,x]=np.sqrt(Q[x,y]);L[y,y]=-np.sqrt(Q[x,y]*pi[x]/pi[y]);Ls.append(L)
He=np.zeros((3,3),complex)
for x in range(3):
 for z in range(3):
  if x!=z:He[x,z]=.5j*(Q[z,x]*np.sqrt(pi[z]/pi[x])-Q[x,z]*np.sqrt(pi[x]/pi[z]))
C0=sum(L.conj().T@L for L in Ls)
c=.99*np.linalg.eigvalsh(C0)[1]
assert np.linalg.norm(He@psi)<1e-12
assert max(np.linalg.norm(L@psi) for L in Ls)<1e-12
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);I=np.eye(2)
f1=np.array([1,-1,0],float);f1-=pi@f1
f2=np.array([0,1,-1],float);f2-=pi@f2
K=np.kron(X,np.diag(f1))+np.kron(Z,np.diag(f2))
B=np.kron(I,Pe)@K@np.kron(I,psi[:,None]);B02=np.linalg.norm(B,2)**2
rho=(I+Y)/2;init=np.kron(rho,P).reshape(-1,order='F');T=.3
def comm(H):return -1j*(np.kron(np.eye(len(H)),H)-np.kron(H.T,np.eye(len(H))))
rows=[]
for lam in [1,10,100,1000]:
 H=np.kron(.3*Y,np.eye(3))+np.kron(I,lam*He)+np.sqrt(lam)*K
 jumps=[np.sqrt(lam)*np.kron(I,L) for L in Ls];G=comm(H);JS=[]
 for J in jumps:
  C=J.conj().T@J;F=np.kron(J.conj(),J);JS.append(F);G+=F-.5*(np.kron(np.eye(6),C)+np.kron(C.T,np.eye(6)))
 out=(expm(T*G)@init).reshape((6,6),order='F');marg=np.trace(out.reshape(2,3,2,3),axis1=1,axis2=3)
 CG=np.kron(lam*Q.T,np.eye(4)).astype(complex)
 for x in range(3):CG[4*x:4*x+4,4*x:4*x+4]+=comm(.3*Y+np.sqrt(lam)*(f1[x]*X+f2[x]*Z))
 ci=np.concatenate([p*rho.reshape(-1,order='F') for p in pi]);co=expm(T*CG)@ci;cm=sum(co[4*x:4*x+4].reshape((2,2),order='F') for x in range(3))
 err=np.linalg.norm(marg-cm,ord='nuc');assert err<1e-9
 theta=min(pi)/4;kappa=np.expm1(theta);aa=np.exp(theta)*min(pi)-kappa;delta=2*kappa/aa
 V=np.kron(I,np.eye(3)+delta*Pe);rate=4*kappa*B02/(c*aa*aa)
 dual=1j*(H@V-V@H)
 for J in jumps:
  C=J.conj().T@J;dual+=np.exp(theta)*J.conj().T@V@J-.5*(C@V+V@C)
 maxev=np.linalg.eigvalsh(dual-rate*V).max();assert maxev<1e-9
 gt=G+kappa*sum(JS);mgf=np.trace((expm(T*gt)@init).reshape((6,6),order='F')).real
 bound=np.exp(T*rate);assert mgf<=bound+1e-9
 rows.append({'lambda':lam,'trace_norm_error':float(err),'tilted_operator_max_eigenvalue':float(maxev),'mgf':float(mgf),'mgf_bound':float(bound)})
print(json.dumps({'scope':'dense floating diagnostic only','pi':pi.tolist(),'c':float(c),'B0_squared':float(B02),'rows':rows},indent=2))
