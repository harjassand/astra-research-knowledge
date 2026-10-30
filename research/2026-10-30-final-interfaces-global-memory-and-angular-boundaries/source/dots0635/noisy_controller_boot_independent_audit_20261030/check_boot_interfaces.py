"""Independent finite algebra checks; not a native bootstrap/lifetime simulation."""
import numpy as np
from scipy.linalg import expm
import json
from pathlib import Path
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]); H=(X+Z)/np.sqrt(2)
p0=np.diag([1,0]); p1=np.diag([0,1])
def kron(*xs):
 y=np.array([[1]],complex)
 for x in xs:y=np.kron(y,x)
 return y
def reset_jumps(n,target):
 return [kron(*(np.outer([1,0],np.eye(2)[s]) if j==target else I for j in range(n))) for s in range(2)]
# DATA, reset controller, retained bath; initial controller/bath Bell correlation.
kappa=1.3; T=3.; u=.2; eta=1e-5
P=kron(I,p1,I); Q=kron(p1,I,I); Id=np.eye(8)
Js=reset_jumps(3,1)
def L0star(O):return kappa*(sum(J.conj().T@O@J for J in Js)-O)
Hnoise=eta*kron(X,X,Z)
def Ns(O):return 1j*(Hnoise@O-O@Hnoise)
def F(s):return (u*Id+(1-u)*Q)@(u*Id+(1-u)*np.exp(-kappa*(T-s))*P)
def dF(s):return (u*Id+(1-u)*Q)@((1-u)*kappa*np.exp(-kappa*(T-s))*P)
backward=max(np.linalg.norm(dF(s)+L0star(F(s))) for s in [0,.4,1.7,T])
def Lrho(rho):return kappa*(sum(J@rho@J.conj().T for J in Js)-rho)-1j*(Hnoise@rho-rho@Hnoise)
L=np.column_stack([Lrho(np.eye(64)[:,j].reshape((8,8),order='F')).reshape(-1,order='F') for j in range(64)])
bell=np.array([1,0,0,1],complex)/np.sqrt(2); psi=np.kron([1,0],bell); rho=np.outer(psi,psi.conj())
rhoT=(expm(T*L)@rho.reshape(-1,order='F')).reshape((8,8),order='F')
C=2*u**(-2); pboot=np.exp(C*eta*T)*(u+(1-u)*np.exp(-kappa*T))
label_moments=[float(np.trace(O@rhoT).real) for O in [Q,P,Q@P]]
assert label_moments[0]<=pboot and label_moments[1]<=pboot and label_moments[2]<=pboot**2
# Actual forest structural form: clock A0/C, workspace, tag free/owned, DATA.
# Controlled nonmonomial V on workspace/DATA; only C and owned tag activate.
Fforest=np.eye(16,dtype=complex)
V=np.zeros((4,4),complex)
for w in range(2):
 for d in range(2):V[2*w+(d^w),2*w+d]=1
V=V@kron(H,I)
for w in range(2):
 for d in range(2):
  col=8+4*w+2+d
  Fforest[:,col]=0
  for ww in range(2):
   for dd in range(2):Fforest[8+4*ww+2+dd,col]=V[2*ww+dd,2*w+d]
P_h=np.eye(16)-kron(p0,p0,I,I); P_tag=kron(I,I,p1,I); Qd=kron(I,I,I,p1)
R=P_h+(np.eye(16)-P_h)@Qd
ready_comm=max(np.linalg.norm(Fforest@P-P@Fforest) for P in [P_h,P_tag])
cover_min=float(np.linalg.eigvalsh(R-Fforest@Qd@Fforest.conj().T).min())
invariance=float(np.linalg.norm(Fforest@R@Fforest.conj().T-R))
assert ready_comm<1e-12 and cover_min>-1e-12 and invariance<1e-12
# [[4,2,2]] stabilizer example: all syndrome labels zero despite logical change.
Sx=kron(X,X,X,X); Sz=kron(Z,Z,Z,Z); logical=kron(X,X,I,I)
psi=np.zeros(16,complex);psi[0]=psi[15]=1/np.sqrt(2); bad=logical@psi
syndrome=[float((bad.conj()@((np.eye(16)-S)/2)@bad).real) for S in [Sx,Sz]]
logical_trace_distance=2*np.sqrt(1-abs(psi.conj()@bad)**2)
assert max(abs(x) for x in syndrome)<1e-12 and abs(logical_trace_distance-2)<1e-12
out={'scope':'Backward reset test, retained-bath label moments, nonmonomial forest readiness/OR algebra, and undetected logical counterexample. Not a full native or Tanner lifetime simulation.', 'backward_equation_residual':float(backward),'p_boot_bound':float(pboot),'actual_Q_P_QP_moments':label_moments,'output_density_min_eigenvalue':float(np.linalg.eigvalsh(rhoT).min()),'forest_ready_commutator_norm':float(ready_comm),'forest_OR_cover_min_eigenvalue':cover_min,'forest_OR_invariance_norm':invariance,'logical_counterexample_syndrome_moments':syndrome,'logical_counterexample_trace_distance':float(logical_trace_distance)}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
