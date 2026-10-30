import numpy as np,json
from scipy.linalg import eigvalsh
# Reconstruct the full map from physical tuples, independently of the source script.
physical=[(a,b) for a in range(3) for b in range(6)] # A 0=vac,1/2=data; B vac,e0,e1,d0,d1,x
# Gauge order: source u0, u1, u2; excited e0,e1,e2; done d0,d1,d2.
pairs={}
for logical in range(2):
 pairs[(logical,0)]=(logical+1,0)
 pairs[(logical,1)]=(0,0 if logical==0 else 5)
 pairs[(logical,2)]=(logical+1,5)
 for a in range(3):
  pairs[(logical,3+a)]=(a,1+logical)
  pairs[(logical,6+a)]=(a,3+logical)
V=np.zeros((18,18),complex)
for (logical,g),p in pairs.items():V[physical.index(p),logical*9+g]=1
omega,kappa=1.7,.9
h=np.zeros((9,9),complex);j=np.zeros_like(h)
for a in range(3):h[a,3+a]=h[3+a,a]=omega;j[6+a,3+a]=np.sqrt(kappa)
H=np.zeros((18,18),complex)
for b in range(2):
 for p,q in [((b+1,0),(0,b+1)),((0,0 if b==0 else 5),(1,b+1)),((b+1,5),(2,b+1))]:
  ii,jj=physical.index(p),physical.index(q);H[ii,jj]=H[jj,ii]=omega
jb=np.zeros((6,6),complex);jb[3,1]=jb[4,2]=np.sqrt(kappa)
J=np.kron(np.eye(3),jb)
R=np.array([[2/kappa+kappa/(4*omega**2),-1j/(2*omega)],[1j/(2*omega),2/kappa]])
Rall=np.zeros((9,9),complex)
for a in range(3):Rall[np.ix_([a,a+3],[a,a+3])]=R
active=np.diag([1]*6+[0]*3)
Lstar=1j*(h@Rall-Rall@h)+j.conj().T@Rall@j-(j.conj().T@j@Rall+Rall@j.conj().T@j)/2
Pdone=np.diag([int(b in (3,4)) for a,b in physical])
# Retain a reference. Coherent physical receiver retirement preserves the Bell pair.
psi=np.zeros(12,complex);psi[1]=psi[6+2]=1/np.sqrt(2)
rho=np.outer(psi,psi.conj())
coh=np.kron(np.eye(2),jb)@rho@np.kron(np.eye(2),jb.conj().T)/kappa
split=np.zeros((12,12),complex)
for e,d in [(1,3),(2,4)]:
 op=np.zeros((6,6),complex);op[d,e]=1
 K=np.kron(np.eye(2),op);split+=K@rho@K.conj().T
bell=np.zeros(12,complex);bell[3]=bell[6+4]=1/np.sqrt(2)
res={'basis_unitarity':float(np.linalg.norm(V.conj().T@V-np.eye(18))),
 'H_factorization':float(np.linalg.norm(V.conj().T@H@V-np.kron(np.eye(2),h))),
 'J_factorization':float(np.linalg.norm(V.conj().T@J@V-np.kron(np.eye(2),j))),
 'full_gramian':float(np.linalg.norm(Lstar+active)),
 'R_eigenvalues':eigvalsh(R).tolist(),
 'HPdone':float(np.linalg.norm(H@Pdone)), 'JPdone':float(np.linalg.norm(J@Pdone)),
 'coherent_retirement_Bell_fidelity':float(np.vdot(bell,coh@bell).real),
 'resolved_retirement_Bell_fidelity':float(np.vdot(bell,split@bell).real)}
for key in ['basis_unitarity','H_factorization','J_factorization','full_gramian','HPdone','JPdone']:assert res[key]<1e-12
assert abs(res['coherent_retirement_Bell_fidelity']-1)<1e-12
assert abs(res['resolved_retirement_Bell_fidelity']-.5)<1e-12
print(json.dumps(res,indent=2))
