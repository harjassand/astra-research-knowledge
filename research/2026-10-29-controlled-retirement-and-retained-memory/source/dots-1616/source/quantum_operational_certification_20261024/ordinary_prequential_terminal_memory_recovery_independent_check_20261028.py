"""Independent exact/numerical checks of the frozen prequential proof.
No source records, source samplers, SDP learner, or hardware execution.
"""
from pathlib import Path
import hashlib, json, itertools
import sympy as S
import numpy as np
BASE=Path(__file__).resolve().parent
SOURCE=BASE/'ordinary_prequential_terminal_memory_recovery_20261028.md'
PIN='20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==PIN
I=S.I; q=S.Rational
paulis=[S.eye(2),S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-I],[I,0]]),S.diag(1,-1)]
kron=S.kronecker_product
phi=S.Matrix([1,0,0,1]); Phi=phi*phi.H/2
swap=S.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
U=q(3,5)*S.eye(4)+I*q(4,5)*swap
assert S.simplify(U.H*U)==S.eye(4)
mem=S.Matrix([[q(3,5),q(1,5)+I*q(1,10)],[q(1,5)-I*q(1,10),q(2,5)]])
def trace_second(r,da,db):
 return S.Matrix(da,da,lambda i,j: sum(r[i*db+k,j*db+k] for k in range(db)))
def E(r,m=mem): return trace_second(U*kron(r,m)*U.H,2,2)
K0=S.diag(1,q(3,5)); K1=S.Matrix([[0,q(4,5)],[0,0]])
ks=[K0,K1]
def D(r): return sum((k*r*k.H for k in ks),S.zeros(2))
def choi(channel,di):
 out=channel(S.eye(di)[:,0]*S.eye(di)[:,0].T).rows
 J=S.zeros(out*di)
 for a in range(di):
  for b in range(di):
   x=S.zeros(di); x[a,b]=1
   J+=kron(channel(x),x)/di
 return S.simplify(J)
JD=choi(D,2)
gmean=S.zeros(4); grad=S.zeros(4); six=q(1,2)
for j in range(1,4):
 for s in [-1,1]:
  r=E((paulis[0]+s*paulis[j])/2)
  grad-=q(2,12)*s*kron(paulis[j],r.T)
  six-=q(1,12)*s*S.trace(paulis[j]*D(r))
  for W in paulis:
   eb=S.trace(W*r)
   gmean-=q(1,24)*q(4,2)*s*eb*kron(paulis[j],W.T)
assert S.simplify(gmean-grad)==S.zeros(4)
fe=S.simplify(S.trace(Phi*choi(lambda x:D(E(x)),2)))
assert S.simplify(six-q(2,3)*(1-fe))==0
assert S.simplify(six-(q(1,2)+S.trace(JD*grad)))==0
for j in range(1,4):
 for W in paulis:
  g=-2*kron(paulis[j],W.T)
  assert S.trace(g.H*g)==16
# Exact repair and nonlinear squared-objective perturbation on a valid near-feasible point.
delta=q(1,1000000); Kstar=2*Phi
Ktilde=Kstar+delta*kron(paulis[1],paulis[3])
# Its negative eigenvalue residual is <=delta by Weyl; TP residual is exactly zero.
assert trace_second(Ktilde,2,2)==S.eye(2) # This example is TP under either marginal.
Kphys=(Ktilde+2*delta*S.eye(4))/(1+4*delta)
assert trace_second(Kphys,2,2)==S.eye(2)
for n in range(1,5):
 for ix in itertools.combinations(range(4),n): assert Kphys.extract(ix,ix).det()>0
Jphys=Kphys/2; Jtilde=Ktilde/2
Y=S.eye(4)/4-q(1,16)*(-2*kron(paulis[2],paulis[2].T))
normsq=lambda x:S.simplify(S.trace(x.H*x))
change=S.simplify(abs(normsq(Jphys-Y)-normsq(Jtilde-Y)))
assert change<=100*delta
# CP-dominance dual certificate: genuinely noncommuting gauge blocks.
plus=S.Matrix([1,1]); plusi=S.Matrix([1,I]); e0=S.Matrix([1,0])
H=[S.eye(2)/5,e0*e0.H/5,plus*plus.H/10,plusi*plusi.H/10]
assert sum(S.trace(x) for x in H)==1
assert H[1]*H[2]!=H[2]*H[1]
for a in range(1,4):
 x=H[0]-H[a]; assert x[0,0]>=0 and x[1,1]>=0 and x.det()>=0
cnot=S.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
V=q(5,13)*S.eye(4)+I*q(12,13)*cnot
baseks=[kron(S.eye(2),S.eye(2)[:,g].T) for g in range(2)]
decoders=[baseks,[k*V for k in baseks],[a*k*V for a in ks for k in baseks]]
oracle_fidelities=[]
for dec in decoders:
 effect=sum((kron(S.eye(2),k.H)*Phi*kron(S.eye(2),k) for k in dec),S.zeros(8))
 T=[]
 for a,P in enumerate(paulis):
  bell=kron(S.eye(2),P)*phi/S.sqrt(2)
  A=kron(bell,S.eye(2))
  block=S.simplify(A.H*effect*A)
  T.append(block)
  assert block[0,0]>=0 and block[1,1]>=0 and S.simplify(block.det())>=0
 assert S.simplify(sum(T,S.zeros(2)))==S.eye(2)
 fidelity=S.simplify(sum(S.trace(H[a]*T[a]) for a in range(4)))
 assert fidelity<=q(2,5)
 oracle_fidelities.append(str(fidelity))
assert oracle_fidelities[0]=='2/5'
# Numerical complete-instrument branch enumeration with coherent retained memory.
# Full local projector outcomes are retained; there is no memory reset.
P=[np.array(x).astype(complex) for x in paulis]
Un=np.array(U).astype(complex); mn=np.array(mem).astype(complex)
vec=np.array([1,1j,2,-1,2j,1],complex); rho=np.outer(vec,vec.conj())/12
# Arbitrary three-dimensional retained reference R, not just a Bell state.
def ptrM(r,n): return np.trace(r.reshape(n,2,n,2),axis1=1,axis2=3)
def mem_instr(m,j,s,W,b):
 a=(P[0]+s*P[j])/2
 joint=Un@np.kron(a,m)@Un.conj().T
 proj=P[0] if W==0 else (P[0]+b*P[W])/2
 op=np.kron(proj,P[0]); joint=op@joint@op
 return np.trace(joint.reshape(2,2,2,2),axis1=0,axis2=2)/24
# Channel instrumentation on M while preserving every QR block.
def big_instr(qrm,j,s,W,b):
 out=np.zeros_like(qrm)
 for a in range(6):
  for c in range(6): out[2*a:2*a+2,2*c:2*c+2]=mem_instr(qrm[2*a:2*a+2,2*c:2*c+2],j,s,W,b)
 return out
# A deliberately history-dependent but physical unitary decoder, frozen pre-call.
def decoder(h): return P[(sum((j+s+W+b) for j,s,W,b in h))%4]
def channel_choi(m,h):
 out=np.zeros((4,4),complex); V=decoder(h)
 for a in range(2):
  for b in range(2):
   x=np.zeros((2,2),complex); x[a,b]=1
   y=ptrM(Un@np.kron(x,m)@Un.conj().T,2)
   out+=np.kron(V@y@V.conj().T,x)/2
 return out
records=[(j,s,W,b) for j in [1,2,3] for s in [-1,1] for W in range(4) for b in ([1] if W==0 else [-1,1])]
# N=3 is sufficient for the transfer identity; power-of-four is only needed for rational OGD steps.
N=3; branches=[((),mn,np.kron(rho,mn))]
mixture=np.zeros((4,4),complex); direct=np.zeros((6,6),complex)
max_independence=0.; mass=[]; branchcounts=[]
for t in range(1,N+1):
 mass.append(float(sum(np.trace(m).real for _,m,_ in branches))); branchcounts.append(len(branches))
 for h,m,qrm in branches:
  max_independence=max(max_independence,float(np.max(np.abs(qrm-np.kron(rho,m)))))
  mixture+=channel_choi(m,h)/N
  op=np.kron(np.eye(3),Un); V=np.kron(np.eye(3),decoder(h))
  direct+=V@ptrM(op@qrm@op.conj().T,6)@V.conj().T/N
 if t<N:
  branches=[(h+(rec,),mem_instr(m,*rec),big_instr(qrm,*rec)) for h,m,qrm in branches for rec in records]
# Apply averaged normalized output-first Choi to arbitrary QR input independently.
via=np.zeros((6,6),complex)
for a in range(3):
 for b in range(3):
  x=rho[2*a:2*a+2,2*b:2*b+2]
  via[2*a:2*a+2,2*b:2*b+2]=2*np.einsum('oipj,ij->op',mixture.reshape(2,2,2,2),x)
error=float(np.max(np.abs(direct-via)))
assert error<1e-12 and max_independence<1e-12
assert max(abs(x-1) for x in mass)<1e-12
assert np.min(np.linalg.eigvalsh(mixture))>-1e-12
out={
 'status':'PASS','source_sha256':PIN,'evidence_type':'Independent deterministic exact matrix checks and finite branch enumeration; no samples',
 'exact':{'gradient_conditional_unbiasedness':True,'six_state_nonunital_Bell_identity':True,'Frobenius_gradient_norm_squared':16,
 'rational_repair_strict_principal_minors':15,'squared_objective_change':str(change),'squared_objective_change_bound':str(100*delta),
 'noncommuting_gauge_oracle_fidelities':oracle_fidelities,'common_oracle_fidelity':'2/5'},
 'terminal_branch_enumeration':{'N':N,'reference_dimension':3,'coherent_memory_dimension':2,'branch_counts':branchcounts,'prefix_masses':mass,
 'maximum_QR_memory_factorization_residual':max_independence,'actual_reference_output_vs_channel_mixture_residual':error,
 'warning':'The fixture decoder is physical and history-dependent but not the projected learner; it tests transfer identity independently of learning.'},
 'source_calls':0,'random_samples':0,'hardware_executions':0,'SDP_solver_executed':False}
print(json.dumps(out,indent=2,sort_keys=True))
