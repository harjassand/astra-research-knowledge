"""Finite identities only: not asymptotic proof or priority verification."""
import json
import numpy as np
from scipy.linalg import expm
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1])
def kr(*xs):
 a=np.array([[1]],complex)
 for b in xs:a=np.kron(a,b)
 return a
S1=kr(Z,Z,I);S2=kr(I,Z,Z);U=(2*np.eye(8)-S1-S2)/2
P=kr(I,X,I);change=P@U@P-U
Pm=np.diag(np.isclose(np.diag(change),-2).astype(float));Pp=np.diag(np.isclose(np.diag(change),2).astype(float));A=P@Pm
sp=np.array([[0,0],[1,0]],complex);sm=sp.T.conj();V=kr(A,sp)+kr(A.T.conj(),sm)
H0=kr(U,I)+kr(np.eye(8),2*np.diag([0,1]))
beta=1.73;r=1/(1+np.exp(2*beta));tau=np.diag([1-r,r]);rng=np.random.default_rng(7)
a=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));rho=a@a.T.conj();rho/=np.trace(rho);errors=[]
for theta in [.29,np.pi/2]:
 W=expm(-1j*theta*V);out_joint=W@kr(rho,tau)@W.T.conj();out=np.trace(out_joint.reshape(8,2,8,2),axis1=1,axis2=3)
 q=np.sin(theta)**2;s=.41;Es=expm(s*U);formula=Es@(np.eye(8)+q*(1-r)*(np.exp(-2*s)-1)*Pm+q*r*(np.exp(2*s)-1)*Pp)
 errors.append(abs(np.trace(out@Es)-np.trace(rho@formula)))
 if abs(theta-np.pi/2)<1e-6:
  K0=np.eye(8)-Pm;K1=np.eye(8)-Pp
  down=K0@rho@K0+A@rho@A.T.conj();up=K1@rho@K1+A.T.conj()@rho@A
  errors.append(np.linalg.norm(out-(1-r)*down-r*up))
S=[kr(X,Z,Z,X,I),kr(I,X,Z,Z,X),kr(X,I,X,Z,Z),kr(Z,X,I,X,Z)]
Pc=np.eye(32,dtype=complex)
for g in S:Pc=Pc@(np.eye(32)+g)/2
Lx=kr(X,X,X,X,X);Lz=kr(Z,Z,Z,Z,Z)
e,vec=np.linalg.eigh(Pc@(np.eye(32)+Lz)/2);v0=vec[:,np.argmax(e)];v1=Lx@v0
bell=(np.kron(v0,[1,0])+np.kron(v1,[0,1]))/np.sqrt(2);phi=np.outer(bell,bell.conj());flip=kr(Lx,I)@phi@kr(Lx,I)
p=.017;out=(1-p)*phi+p*flip;Uc=sum((np.eye(32)-g)/2 for g in S)
report={'scope':'finite algebra diagnostics only','commutator_norm':float(np.linalg.norm(V@H0-H0@V)),'collision_identity_error':float(max(errors)),'code_dimension':int(round(np.trace(Pc).real)),'correlated_source_half_trace_error':float(np.sum(abs(np.linalg.eigvalsh(out-phi)))/2),'expected_error':p,'logical_error_energy':float(np.trace(out@kr(Uc,I)).real),'bell_branch_overlap':float(np.trace(phi@flip).real)}
assert report['commutator_norm']<1e-11 and report['collision_identity_error']<1e-11
assert abs(report['correlated_source_half_trace_error']-p)<1e-11 and abs(report['logical_error_energy'])<1e-11
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
