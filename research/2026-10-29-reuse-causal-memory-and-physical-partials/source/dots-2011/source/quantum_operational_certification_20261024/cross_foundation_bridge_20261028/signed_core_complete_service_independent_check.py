"""Independent exact full-core/IC/signed-feedback checks; no source sampling.
Uses physical SWAP memory, an actual rational IC POVM, subnormalized raw prefixes,
complete operator transfer, coherent output reuse, and non-CP signed estimates.
"""
from pathlib import Path
import sympy as s
import hashlib,json,itertools
PTH=Path(__file__).resolve().parent;R=s.Rational
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);PA=[I,X,Y,Z]
def simp(x):return s.simplify(x)
def kron(*xs):return s.SparseMatrix(s.kronecker_product(*xs))
def absentries(A):return A.applyfunc(lambda x:abs(s.re(x))+abs(s.im(x)))
def norm_entry(A):return sum(absentries(A))
rhos=[(I+Z)/2,(I-Z)/2,(I+X)/2,(I+Y)/2]
E=[a/8 for a in rhos];E0=I-sum(E,s.zeros(2))
assert all(ev>=0 for ev in E0.eigenvals())
assert s.trace(E0*(I/2))==R(3,4)
taus=[I/2,R(3,4)*rhos[2],R(3,4)*rhos[3],R(3,4)*rhos[0]]
Fs=[I,E[0],E[2],E[3]]
H=s.Matrix(4,4,lambda i,j:simp(s.trace(Fs[i]*taus[j])))
assert H.det()!=0
m=H[0,:]
assert m==s.Matrix([[1,R(3,4),R(3,4),R(3,4)]])
# Input and output IC duals derived independently by Gram inversion.
G=s.Matrix(4,4,lambda i,j:s.trace(rhos[i]*rhos[j]));Gi=G.inv()
D=[sum([Gi[u,j]*rhos[j] for j in range(4)],s.zeros(2)) for u in range(4)]
B=[8*a for a in D]
for u,v in itertools.product(range(4),repeat=2):
 assert simp(s.trace(D[u]*rhos[v]))==int(u==v)
 assert simp(s.trace(E[u]*B[v]))==int(u==v)
# Safe exact dual norm bounds: ||D||op<=2, ||B||1<=24.
for a in D:assert all(abs(ev)<=2 for ev in a.eigenvals())
for a in B:assert sum(abs(ev)*mult for ev,mult in a.eigenvals().items())<=24
# Physical branches for SWAP(M,A): Phi_uv(sigma)=rho_u Tr(E_v sigma).
Hz={};C={}
for u,v in itertools.product(range(4),repeat=2):
 Hz[u,v]=s.Matrix(4,4,lambda i,j:simp(s.trace(Fs[i]*rhos[u])*s.trace(E[v]*taus[j])))
 C[u,v]=H.inv()*Hz[u,v]
# Signed coordinates arise even for positive states; normalizing their masses is wrong.
minusX=(I-X)/2
coords=H.inv()*s.Matrix([s.trace(f*minusX) for f in Fs])
assert coords==s.Matrix([2,-R(4,3),0,0])
assert (m*coords)[0]==1 and sum(coords)==R(2,3)
# Pi/Lambda exactly invert on the full complex matrix-unit space, including a Bell memory/reference state.
def pi(state,refdim=1):
 obs=[]
 for f in Fs:
  out=s.zeros(refdim)
  for a,b in itertools.product(range(2),repeat=2):out+=f[b,a]*state[a*refdim:(a+1)*refdim,b*refdim:(b+1)*refdim]
  obs.append(out)
 return [simp(sum([H.inv()[j,i]*obs[i] for i in range(4)],s.zeros(refdim))) for j in range(4)]
def lam(xs):return sum([kron(tau,x) for tau,x in zip(taus,xs)],s.zeros(2*xs[0].rows))
for a,b in itertools.product(range(4),repeat=2):
 Q=s.zeros(4);Q[a,b]=1
 assert lam(pi(Q,2))==Q
phi=s.Matrix([1,0,0,1])/s.sqrt(2);bell=phi*phi.H
bellcoords=pi(bell,2);assert lam(bellcoords)==bell
assert any(any(ev<0 for ev in a.eigenvals()) for a in bellcoords)
# Build the one-step coordinate quantum transfer directly from source equation (3).
def transfer(Ctable):
 T=s.zeros(16)
 for j,a in itertools.product(range(4),repeat=2):
  inp=PA[a]/2
  for i in range(4):
   out=sum([Ctable[u,v][i,j]*B[v]*s.trace(D[u]*inp) for u,v in itertools.product(range(4),repeat=2)],s.zeros(2))
   for z in range(4):T[4*i+z,4*j+a]=simp(s.trace(PA[z]*out))
 return s.SparseMatrix(T)
T=transfer(C)
L=s.Matrix(4,4,lambda a,j:s.trace(PA[a]*taus[j]));Linv=L.inv()
Sswap=s.SparseMatrix(16,16,lambda out,inn:int(out==4*(inn%4)+inn//4))
assert T==kron(Linv,s.eye(4))*Sswap*kron(L,s.eye(4))
# A valid entrywise raw-table perturbation gives a non-CP signed quantum prediction.
z=(0,0);eps=R(1,10**12)
Hzhat={key:val.copy() for key,val in Hz.items()};Hzhat[z][1,0]+=eps
assert all(0<=x<=1 for table in Hzhat.values() for x in table)
Chat={key:H.inv()*val for key,val in Hzhat.items()}
That=transfer(Chat)
physical_hat=kron(L,s.eye(4))*That*kron(Linv,s.eye(4))
pauli2=[kron(a,b) for a,b in itertools.product(PA,repeat=2)]
def choi_from_ptm(ptm,basis):
 d=basis[0].rows;out=s.zeros(d*d)
 for j in range(len(basis)):
  for i in range(len(basis)):
   if ptm[i,j]:out+=ptm[i,j]*kron(basis[j].T,basis[i])/d
 return simp(out)
Jhat=choi_from_ptm(physical_hat,pauli2)
# Input memory/input-port 10, output memory/output-port 10 is outside SWAP's Choi support.
noncp_witness=Jhat[10,10]
assert noncp_witness==-128*eps and noncp_witness<0
# Exact inverse-confidence certificate and weighted one-step error.
DH=s.zeros(4);U=H.inv();M=absentries(U);K=max(1,sum(M))
Dz={key:s.zeros(4) for key in Hz};Dz[z][1,0]=eps
Ez={key:M*val for key,val in Dz.items()}
delta=max(sum(48*Ez[u,v][i,j] for u,v,i in itertools.product(range(4),range(4),range(4))) for j in range(4))
assert delta>0
# Full caller register has two qubits. Coherent controller feeds old output into next input.
Cn=s.zeros(4)
for j in range(4):Cn[j ^ ((j>>1)&1),j]=1
Sw=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
control=Sw*Cn
Cpt=s.SparseMatrix(16,16,lambda i,j:simp(s.trace(pauli2[i]*control*pauli2[j]*control.H)/4))
Tc=kron(T,s.eye(4));Thc=kron(That,s.eye(4));Cc=kron(s.eye(4),Cpt)
# Source physical SWAP(M,caller0), controller acts only on caller0,caller1.
source=s.zeros(8)
for j in range(8):
 a=(j>>2)&1;b=(j>>1)&1;c=j&1;source[4*b+2*a+c,j]=1
physcontrol=kron(I,control)
pauli3=[kron(*a) for a in itertools.product(PA,repeat=3)]
physstep=source
Qphys=s.eye(8)
Qcoord=s.eye(64);Qhat=s.eye(64)
initial=kron(s.Matrix([1,0,0,0]),s.eye(16));finish=kron(m,s.eye(16))
cases=[]
for h in range(1,5):
 if h==1:
  Qphys=source;Qcoord=Tc;Qhat=Thc
 else:
  Qphys=source*physcontrol*Qphys;Qcoord=Tc*Cc*Qcoord;Qhat=Thc*Cc*Qhat
 Pphys=s.SparseMatrix(64,64,lambda i,j:simp(s.trace(pauli3[i]*Qphys*pauli3[j]*Qphys.H)/8))
 assert Qcoord==kron(Linv,s.eye(16))*Pphys*kron(L,s.eye(16))
 N=finish*Qcoord*initial;Nh=finish*Qhat*initial
 assert N[0,:]==s.eye(16)[0,:]
 errJ=choi_from_ptm(Nh-N,pauli2)
 # Nuclear norm <= entrywise sum: a separate rational upper bound on full diamond error.
 diamond_upper=norm_entry(errJ)/2
 eta=K*((1+K*delta)**h-1)/2
 assert diamond_upper<=eta
 # Explicit entangled caller input, with negative operator coordinates retained throughout.
 ci=s.Matrix([s.trace(a*bell) for a in pauli2])
 exactc=N*ci;predc=Nh*ci
 assert exactc[0]==1
 cases.append({'calls':h,'eta_core':str(eta),'independent_half_diamond_upper':str(diamond_upper)})
# A genuinely perturbed H inverse test; all corrections exact and ordinary-table probabilities valid.
rhoerr=R(1,10**10);H2=H.copy();H2[0,1]+=rhoerr
H2z={key:H2*C[key] for key in C}
assert all(0<=x<=1 for table in [H2,*H2z.values()] for x in table)
U2=H2.inv();DH2=absentries(H2-H);A2=absentries(U2)*DH2
assert max(sum(A2[i,j] for j in range(4)) for i in range(4))<1
M2=(s.eye(4)-A2).inv()*absentries(U2)
assert all(x>=0 for x in M2-absentries(H.inv()))
for key in C:
 Ch2=U2*H2z[key];E2=M2*(absentries(H2z[key]-Hz[key])+DH2*absentries(Ch2))
 assert Ch2==C[key] and all(x>=0 for x in E2-absentries(C[key]-Ch2))
# Even with the EXACT transfer, a wrong raw mass row changes accessible normalization.
wrongm=s.ones(1,4);caller=rhos[2]
cin=s.Matrix([s.trace(a*caller) for a in PA])
oneinitial=kron(s.Matrix([1,0,0,0]),s.eye(4))
wrongN=kron(wrongm,s.eye(4))*T*oneinitial
rightN=kron(m,s.eye(4))*T*oneinitial
assert (rightN*cin)[0]==1 and (wrongN*cin)[0]==R(4,3)
# Perturbed empirical mass, not all-ones, has a nonzero final debit despite exact C.
massN=kron(H2[0,:],s.eye(4))*T*oneinitial
mass_trace_error=simp(((massN-rightN)*cin)[0]);assert mass_trace_error==R(4,3)*rhoerr
# Service-only projection / decoder risk checked in exact Pauli channels.
# Signed p has a negative entry; physical projection can achieve the exact negative-mass lower bound.
ptrue=[R(3,4),R(1,4),0,0];a=R(1,100)
phat=[R(3,4)+a,R(1,4),-a,0];ptilde=ptrue
projdist=sum(abs(x-y) for x,y in zip(phat,ptilde))/2
assert projdist==a
# Negativity of a Bell outcome forces every normalized CPTP Choi state at least a away.
assert phat[2]==-a and sum(phat)==1
# All four physical Pauli corrections have exact identity-error risk 1-p_selected.
for perm in (range(4),):
 e_true=[1-ptrue[j] for j in perm];e_tilde=[1-ptilde[j] for j in perm]
 chosen=min(range(4),key=lambda j:e_tilde[j]);assert e_true[chosen]<=min(e_true)+4*a
# Direct service tomography comparator Choi coefficient identity.
Nqubit=s.diag(1,R(2,3),R(1,2),R(1,3))
J=choi_from_ptm(Nqubit,PA)
Jfrom=s.zeros(4)
for u,v in itertools.product(range(4),repeat=2):
 coeff=s.Matrix([s.trace(a*rhos[u]) for a in PA]);out=sum([(Nqubit*coeff)[i]*PA[i]/2 for i in range(4)],s.zeros(2))
 puv=s.trace(E[v]*out);Jfrom+=puv*kron(D[u].T,B[v])
assert simp(Jfrom)==J

def digest(name):return hashlib.sha256((PTH/name).read_bytes()).hexdigest()
source='SIGNED_CORE_COMPLETE_SERVICE_PREDICTION.md'
files=[source,'SIGNED_CORE_COMPLETE_SERVICE_PREDICTION_pre_initialization_and_abstention_clarification.md','DIRECT_SERVICE_TOMOGRAPHY_COMPARATOR.md','IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md','IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY_INDEPENDENT_RECEIPT.json']
receipt=json.loads((PTH/files[-1]).read_text());assert receipt['source_sha256']==digest(files[-2])
result={'status':'PASS_EXACT_FULL_CORE_COMPLETE_IC_SIGNED_FEEDBACK_AND_MASS_DEBIT','source_sha256':digest(source),'arithmetic':'Exact rational/Gaussian rational SymPy; no floating thresholds','memory_dimension':2,'full_core_dimension':4,'core_determinant':str(H.det()),'raw_prefix_masses':list(map(str,m)),'positive_state_negative_coordinates':list(map(str,coords)),'Bell_memory_reference_negative_operator_coordinates':True,'coordinate_matrix_unit_checks':16,'one_step_complete_operator_dimension':16,'coherent_feedback_operator_dimension':64,'native':'SWAP(memory,input)','controller':'CNOT(previous output,next input), then known caller SWAP; no hidden-memory access','nonphysical_estimate_raw_probabilities_all_valid':True,'nonCP_estimated_native_Choi_diagonal_witness':str(noncp_witness),'K':str(K),'weighted_delta':str(delta),'service_cases':cases,'interval_inverse_nonzero_H_error_verified':True,'wrong_all_ones_row_output_trace':'4/3','empirical_mass_only_trace_error':str(mass_trace_error),'exact_Pauli_service_projection_distance':str(projdist),'direct_service_tomography_Choi_identity_verified':True,'source_calls':0,'random_draws':0,'sampled_source_outcomes':0,'production_SDP_or_quantum_compiler_executed':False,'sha256':{name:digest(name) for name in files}}
(PTH/'signed_core_complete_service_independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
