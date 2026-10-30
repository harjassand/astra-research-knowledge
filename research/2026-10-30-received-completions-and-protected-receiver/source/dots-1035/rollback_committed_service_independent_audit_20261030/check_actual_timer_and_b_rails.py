"""Independent clean-credit fixture with actual two-level reset timer and B rails.
The three-level DATA channel is deliberately non-idempotent, not a native GPT code.
"""
import numpy as np,json
from pathlib import Path
from scipy.linalg import solve,eigvalsh
I2=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);down=np.array([[0.,1.],[0.,0.]])
n=3;mu=.7;ks=1.1;ka=.9;omega=.8;km=.6;strength=.2;s=.3
C=list(range(n));B={};idx=n
for j in range(n):
 for l in range(j+1):B[j,l]=idx;idx+=1
Q=idx;nc=idx+1;nd=3;dc=2*n
HC=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
Hc=np.kron(HC,I2)+np.kron(np.eye(n),omega*X)
Gs=np.kron(np.diag([0.,0.,ks]),I2);Ga=mu*np.eye(dc)
mons=[]
for i in C:
 p=np.zeros((n,n));p[i,i]=1;mons.append(np.sqrt(km)*np.kron(p,down))
def K(O):return 1j*(Hc@O-O@Hc)+sum(j.T@O@j-(j.T@j@O+O@j.T@j)/2 for j in mons)-((Gs+Ga)@O+O@(Gs+Ga))/2
cols=[]
for j in range(dc*dc):
 E=np.zeros((dc,dc),complex);E.flat[j]=1;cols.append(K(E).ravel())
KM=np.column_stack(cols)
R=solve(KM,-np.eye(dc).ravel()).reshape(dc,dc);Ps=solve(KM,-Gs.ravel()).reshape(dc,dc)
R=(R+R.conj().T)/2;Ps=(Ps+Ps.conj().T)/2
beta=float(eigvalsh(Ps)[0]/(3*eigvalsh(R)[-1]));A=Ps-beta*R
assert eigvalsh(A)[0]>0
V=np.diag(np.exp(s*np.array([3.,2.,0.])));payload=[]
for j in range(nd):
 J=np.zeros((nd,nd));J[min(j+1,nd-1),j]=1;payload.append(J)
def Phi(O):return sum(j.T@O@j for j in payload)
d=V-Phi(V)
h=np.zeros((nc,nc));h[:n,:n]=HC
for j in range(n):
 for l in range(1,j+1):h[B[j,l],B[j,l-1]]=h[B[j,l-1],B[j,l]]=1
Hcm=np.kron(h,I2)+np.kron(np.eye(nc),omega*X);H=np.kron(Hcm,np.eye(nd));jumps=[]
for i in range(nc):
 p=np.zeros((nc,nc));p[i,i]=1;jumps.append(np.kron(np.sqrt(km)*np.kron(p,down),np.eye(nd)))
for i in C:
 j=np.zeros((nc,nc));j[B[i,i],i]=np.sqrt(mu);jumps.append(np.kron(np.kron(j,I2),np.eye(nd)))
for i in C:
 j=np.zeros((nc,nc));j[Q,B[i,0]]=np.sqrt(ka);jumps.append(np.kron(np.kron(j,I2),np.eye(nd)))
for p in payload:
 j=np.zeros((nc,nc));j[Q,C[-1]]=np.sqrt(ks);jumps.append(np.kron(np.kron(j,I2),p))
def L(O):return 1j*(H@O-O@H)+sum(j.T@O@j-(j.T@j@O+O@j.T@j)/2 for j in jumps)
Ae=np.zeros((2*nc,2*nc),complex);Ae[:dc,:dc]=A
PC=np.zeros((2*nc,2*nc));PC[:dc,:dc]=np.eye(dc)
Gse=np.zeros((2*nc,2*nc));Gse[:dc,:dc]=Gs
TV=np.kron(np.eye(2*nc),V)-strength*np.kron(Ae,d)
expected=-strength*beta*np.kron(PC,d)-(1-strength)*np.kron(Gse,d)
err=float(np.linalg.norm(L(TV)-expected,2))
assert err<1e-11
out={'C_positions':n,'actual_B_rail_positions':len(B),'physical_clock_labels':nc,'reset_monitor_timer_dimension':2,'timer_drive':omega,'timer_reset_rate':km,'full_fixture_dimension':2*nc*nd,'min_success_before_rollback_effect':float(eigvalsh(Ps)[0]),'min_credit_A':float(eigvalsh(A)[0]),'max_credit_A':float(eigvalsh(A)[-1]),'beta':beta,'committed_drift_identity_error':err,'nonidempotent_payload_difference':float(np.linalg.norm(Phi(Phi(V))-Phi(V))),'scope':'actual clean timer/rollback clock structure with abstract non-idempotent DATA payload; not semantic guard composition or native useful-demand coverage'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
