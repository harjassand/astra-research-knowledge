"""Actual C rail with finite monitors and abort to B: non-idempotent payload credit."""
import numpy as np,json
from scipy.linalg import solve,eigvalsh
from pathlib import Path
n=3;nc=5;nd=3;mu=.7;kappa=1.1;gamma=.4;t=.2;s=.3
H=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1);Gs=np.diag([0,0,kappa]);Ga=mu*np.eye(n)
mons=[np.sqrt(gamma)*np.diag([int(i==j) for i in range(n)]) for j in range(n)]
def K(O):return 1j*(H@O-O@H)+sum(J.conj().T@O@J-(J.conj().T@J@O+O@J.conj().T@J)/2 for J in mons)-((Gs+Ga)@O+O@(Gs+Ga))/2
basis=[]
for j in range(n*n):
 E=np.zeros((n,n),complex);E.flat[j]=1;basis.append(K(E).ravel())
KM=np.column_stack(basis)
R=solve(KM,-np.eye(n).ravel()).reshape(n,n);Ps=solve(KM,-Gs.ravel()).reshape(n,n)
R=(R+R.conj().T)/2;Ps=(Ps+Ps.conj().T)/2
beta=float(eigvalsh(Ps)[0]/(2*eigvalsh(R)[-1]));A=Ps-beta*R
assert eigvalsh(A)[0]>0 and eigvalsh(np.eye(n)-A)[0]>0
V=np.diag(np.exp(s*np.array([3,2,0])));kp=[]
for j in range(nd):
 J=np.zeros((nd,nd));J[min(j+1,nd-1),j]=1;kp.append(J)
def Phi(O):return sum(J.T@O@J for J in kp)
d=V-Phi(V);phi_d=Phi(d)
Hfull=np.zeros((nc,nc));Hfull[:n,:n]=H;Hfull=np.kron(Hfull,np.eye(nd));jumps=[]
for j in range(n):
 C=np.zeros((nc,nc));C[3,j]=np.sqrt(mu);jumps.append(np.kron(C,np.eye(nd)))
 C=np.zeros((nc,nc));C[j,j]=np.sqrt(gamma);jumps.append(np.kron(C,np.eye(nd)))
for J in kp:
 C=np.zeros((nc,nc));C[4,n-1]=np.sqrt(kappa);jumps.append(np.kron(C,J))
def L(O):return 1j*(Hfull@O-O@Hfull)+sum(J.conj().T@O@J-(J.conj().T@J@O+O@J.conj().T@J)/2 for J in jumps)
Ae=np.zeros((nc,nc),complex);Ae[:n,:n]=A;Pe=np.diag([1,1,1,0,0]);Gse=np.zeros((nc,nc));Gse[:n,:n]=Gs
TV=np.kron(np.eye(nc),V)-t*np.kron(Ae,d)
expected=-t*beta*np.kron(Pe,d)-(1-t)*np.kron(Gse,d)
err=float(np.linalg.norm(L(TV)-expected));assert err<1e-11
out={'C_positions':n,'abort_rate':mu,'terminal_rate':kappa,'monitor_rate':gamma,'success_probability_min_eigenvalue':float(eigvalsh(Ps)[0]),'credit_A_min_eigenvalue':float(eigvalsh(A)[0]),'credit_A_max_eigenvalue':float(eigvalsh(A)[-1]),'beta':beta,'exact_drift_identity_error':err,'nonidempotent_payload_difference':float(np.linalg.norm(Phi(Phi(V))-Phi(V))),'Phi_d_can_exceed_d':bool(np.max(np.diag(phi_d-d))>0),'substitute_comparison_min_gap':float(eigvalsh(d/(1-np.exp(-s))-phi_d)[0]),'all_checks_pass':True,'scope':'clean actual quantum C rail, monitor and rollback exit, unchanged non-idempotent finite payload; not whole native semantic guard/service theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
