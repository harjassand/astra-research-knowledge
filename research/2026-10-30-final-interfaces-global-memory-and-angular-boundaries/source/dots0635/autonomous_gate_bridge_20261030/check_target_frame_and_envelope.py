"""Exact frame and unary/history envelope regression, not a code gate simulation."""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
rng=np.random.default_rng(30917)
# Memory order (native phase, workspace, DATA control, DATA target), program last.
dm=16;dp=3;D=dm*dp;Im=np.eye(dm);Ip=np.eye(dp)
def bits(j):return [(j>>k)&1 for k in [3,2,1,0]]
def idx(b):return sum(x<<k for x,k in zip(b,[3,2,1,0]))
def perm(fn):
 x=np.zeros((dm,dm),complex)
 for j in range(dm):x[idx(fn(bits(j))),j]=1
 return x
# F is identity on native-ready phase0. Active F writes DATA target into workspace.
def ff(b):
 c,w,a,t=b;return [c,w^(c&t),a,t]
def uu(b):
 c,w,a,t=b;return [c,w,a,t^a]
F=perm(ff);U=perm(uu)
P=[np.diag([int(j==p) for j in range(dp)]) for p in range(dp)]
G=np.kron(Im,P[0])+np.kron(U,P[1]+P[2])
Fbig=np.kron(F,Ip);Ubig=np.kron(U,Ip)
Ft=np.kron(U@F@U.conj().T,Ip)
E=Fbig.conj().T@Ubig.conj().T@G@Fbig
frame_error=np.linalg.norm(Ft.conj().T@G@Fbig-Ubig@E)
# Full arbitrary coherent joint density: no classical program assumption.
x=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));rho=x@x.conj().T;rho/=np.trace(rho)
def trprog(x):return np.einsum('ipjp->ij',x.reshape(dm,dp,dm,dp))
actual=trprog(E@rho@E.conj().T)
blocks=rho.reshape(dm,dp,dm,dp)
E0=F.conj().T@U.conj().T@F
mixture=E0@blocks[:,0,:,0]@E0.conj().T+blocks[:,1,:,1]+blocks[:,2,:,2]
mixture_error=np.linalg.norm(actual-mixture)
# All nonempty subsets are animals of a four-vertex complete toy graph.
# Occupancies are native phase, workspace-history token, and two DATA energy bits.
occ=[np.diag([bits(j)[k] for j in range(dm)]) for k in range(4)]
theta=.1;a=.25;V=np.zeros((dm,dm),complex);env=np.zeros((D,D),complex)
changed={1,3} # workspace/history token AND DATA target. Control/phase unchanged.
per_animal_max=-1.
for m in range(1,5):
 for A in itertools.combinations(range(4),m):
  f=np.eye(dm,dtype=complex)*np.exp(a*m)
  for k in A:f=f@(theta*np.eye(dm)+(1-theta)*occ[k])
  V+=f
  mult=theta**(-len(set(A)&changed))
  env+=np.kron(mult*f,P[0])+np.kron(f,P[1]+P[2])
  per_animal_max=max(per_animal_max,float(eigvalsh(E0.conj().T@f@E0-mult*f)[-1]))
envelope_max=float(eigvalsh(E.conj().T@np.kron(V,Ip)@E-env)[-1])
# Omitting the workspace/history token is FALSE already on its singleton.
fw=np.exp(a)*(theta*np.eye(dm)+(1-theta)*occ[1])
wrong_envelope_max=float(eigvalsh(E0.conj().T@fw@E0-fw)[-1])
# Initial native-ready c=w=0 and DATA |+0>: fixed target inverse does NOT gate it.
psi=np.zeros(dm,complex);psi[idx([0,0,0,0])]=1/np.sqrt(2);psi[idx([0,0,1,0])]=1/np.sqrt(2)
rhom=np.outer(psi,psi.conj())
def trctrl(x):return np.einsum('cwabcwde->abde',x.reshape(2,2,2,2,2,2,2,2)).reshape(4,4)
in_data=trctrl(rhom)
outs=[]
for p in [0,2]:
 init=np.kron(rhom,P[p]);physical=G@Fbig@init@Fbig.conj().T@G.conj().T
 out=trctrl(trprog(Ft.conj().T@physical@Ft));outs.append(out)
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
zero_error=np.linalg.norm(outs[0]-in_data)
done_error=np.linalg.norm(outs[1]-CNOT@in_data@CNOT.conj().T)
zero_vs_gate=np.linalg.norm(outs[0]-outs[1])
assert frame_error<1e-12 and mixture_error<1e-12
assert per_animal_max<1e-10 and envelope_max<1e-9
assert wrong_envelope_max>.1
assert zero_error<1e-12 and done_error<1e-12 and zero_vs_gate>.5
# Exact commutation is NOT enough for a Pauli-path footprint: SWAP's XX/YY cancel.
SWAP=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
X=np.array([[0,1],[1,0]],complex);XX=np.kron(X,X)
energy1=np.diag([0,1,1,1]).astype(complex)
exact_swap_comm=np.linalg.norm(SWAP@energy1-energy1@SWAP)
pauli_coefficient_comm=np.linalg.norm(XX@energy1-energy1@XX)
assert exact_swap_comm<1e-12 and pauli_coefficient_comm>1
out={'exact_swap_energy_commutator':exact_swap_comm,'swap_XX_coefficient_energy_commutator':pauli_coefficient_comm,'joint_dimension':D,'exact_target_frame_error':frame_error,'program_trace_mixture_error':mixture_error,'correct_full_envelope_max_eigenvalue':envelope_max,'per_animal_max_eigenvalue':per_animal_max,'omitting_history_token_violation':wrong_envelope_max,'time_zero_identity_error':zero_error,'completed_target_gate_error':done_error,'time_zero_vs_target_state_distance_frobenius':zero_vs_gate,'scope':'Exact local frame/envelope algebra. DATA here is a trivial full code; no fault-tolerant gate conclusion.'}
Path(__file__).with_name('target_frame_envelope_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
