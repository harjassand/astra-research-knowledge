"""Exact good k=1 A/C controller with actual hub/resource reset timers.
Canonical tag patterns (free at A0, owned at A1/C) are encoded isometrically
in clock basis. Tests success-before-abort resolvent and positive LOAD entry.
No guard-boundary or whole useful-energy composition is tested.
"""
import numpy as np,json
from scipy.linalg import solve,eigvalsh
from pathlib import Path
I2=np.eye(2);X=np.array([[0,1],[1,0]],complex);sm=np.array([[0,1],[0,0]],complex)
n=5;d=n*4;I=np.eye(d);Omegah=.8;Omegar=.65;kh=.6;kr=.5;ks=1.1;muA=.55;muC=.7;kc=.9
P=[np.diag([int(i==j) for i in range(n)]) for j in range(n)]
clockH=np.zeros((n,n));clockH[0,1]=clockH[1,0]=1;clockH[2,3]=clockH[3,2]=1;clockH[3,4]=clockH[4,3]=1
H=np.kron(clockH,np.eye(4))+Omegah*np.kron(np.eye(n),np.kron(X,I2))+Omegar*np.kron(np.eye(n),np.kron(I2,X))
js=[np.sqrt(kh)*np.kron(p,np.kron(sm,I2)) for p in P]
for tagP in [P[0],sum(P[1:])]:js.append(np.sqrt(kr)*np.kron(tagP,np.kron(I2,sm)))
C=np.zeros((n,n));C[2,1]=np.sqrt(kc);js.append(np.kron(C,np.eye(4)))
Gs=ks*np.kron(P[4],np.eye(4));Ga=np.kron(muA*(P[0]+P[1])+muC*sum(P[2:]),np.eye(4))
def K(O):return 1j*(H@O-O@H)+sum(J.conj().T@O@J-(J.conj().T@J@O+O@J.conj().T@J)/2 for J in js)-((Gs+Ga)@O+O@(Gs+Ga))/2
cols=[]
for q in range(d*d):
 E=np.zeros((d,d),complex);E.flat[q]=1;cols.append(K(E).ravel())
KM=np.column_stack(cols)
R=solve(KM,-I.ravel()).reshape(d,d);Ps=solve(KM,-Gs.ravel()).reshape(d,d)
R=(R+R.conj().T)/2;Ps=(Ps+Ps.conj().T)/2
beta=float(eigvalsh(Ps)[0]/(3*eigvalsh(R)[-1]));A=Ps-beta*R
err=float(np.linalg.norm(K(A)-(beta*I-Gs)));entry=float(eigvalsh(A[:4,:4])[0])
assert eigvalsh(A)[0]>0 and eigvalsh(I-A)[0]>0 and entry>0 and err<1e-10
out={'A_positions':2,'C_positions':3,'resource_count':1,'timer_factors':2,'transient_dimension':d,'actual_timer_types':'hub clock-label resolved reset timer and resource free/owned-label resolved reset timer','minimum_success_probability':float(eigvalsh(Ps)[0]),'minimum_credit_A':float(eigvalsh(A)[0]),'maximum_credit_A':float(eigvalsh(A)[-1]),'beta':beta,'minimum_LOAD_entry_credit':entry,'resolvent_credit_identity_error':err,'all_checks_pass':True,'scope':'good isolated A/C canonical-tag subspace with actual finite reset timers and actual irreversible COMMIT; no all-Hilbert guard or full memory claim'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
