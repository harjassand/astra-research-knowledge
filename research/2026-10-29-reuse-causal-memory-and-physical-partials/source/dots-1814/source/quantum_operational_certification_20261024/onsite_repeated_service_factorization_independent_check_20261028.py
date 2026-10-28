"""Independent exact algebra check; no random or acquired source data.
Full 64-dimensional Pauli operator basis on input_1,input_2,retained_memory.
The two source instruments are coherent, time-inhomogeneous, and satisfy the
actual uniform X/Z CP contrasts and identity dominance coefficientwise.
"""
from pathlib import Path
import hashlib,json,itertools
import sympy as s

ROOT=Path(__file__).resolve().parent
R=s.Rational
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
P=[I,X,Y,Z]
def ptm(A):
    return s.SparseMatrix(4,4,lambda i,j:s.simplify(s.trace(P[i]*A*P[j]*A.H)/2))
def kron(*xs):return s.SparseMatrix(s.kronecker_product(*xs))
S4=s.eye(4)
PA=[ptm(A) for A in P]
W=R(20,21)*I-s.I*(R(4,21)*X+R(5,21)*Y)
assert s.simplify(W.H*W)==I and s.simplify(W.det())==1
probs=[s.simplify(s.trace(A.H*W)/2*s.conjugate(s.trace(A.H*W)/2)) for A in P]
assert probs==[R(400,441),R(16,441),R(25,441),0]
WQ=[Q.H*W*Q for Q in P]
L=sum([ptm(A) for A in WQ],s.zeros(4))/4
assert L==sum([p*A for p,A in zip(probs,PA)],s.zeros(4))

# Weak, non-resetting memory instruments; noncommuting rational Kraus operators.
U=s.Matrix([[R(3,5),R(4,5)],[-R(4,5),R(3,5)]])
V=s.Matrix([[R(5,13),R(12,13)],[-R(12,13),R(5,13)]])
K=[[s.diag(R(3,5),R(4,5)),U*s.diag(R(4,5),R(3,5))],
   [s.diag(R(4,5),R(3,5)),V*s.diag(R(3,5),R(4,5))]]
p0=[R(2,5),R(3,10),0,R(3,10)]
p1=[R(1,2),R(1,5),R(1,10),R(1,5)]
weights=[[p0,p1],[p1,p0]]
contrast=[]
for t in range(2):
    assert sum([A.H*A for A in K[t]],s.zeros(2))==I
    assert K[t][0]*K[t][1]!=K[t][1]*K[t][0]
    assert sum([A*Y*A.H for A in K[t]],s.zeros(2))!=s.zeros(2)
    for p in weights[t]:
        assert sum(p)==1 and min(p)>=0 and p[0]>=max(p[1:])
        cx=p[0]+p[1]-p[2]-p[3]
        cz=p[0]-p[1]-p[2]+p[3]
        cy=p[0]-p[1]+p[2]-p[3]
        assert cx>=R(2,5) and cz>=R(2,5)
        contrast.append([str(cx),str(cy),str(cz)])

# These maps retain the final memory, not only the output marginal.
def slot(t,frame=None):
    out=s.zeros(64)
    for k in range(2):
      for a in range(4):
        weight=weights[t][k][a]
        if not weight:continue
        logical=P[a] if frame is None else P[frame].H*W*P[a]*P[frame]
        factors=[S4,S4,ptm(K[t][k])]
        factors[t]=ptm(logical)
        out+=weight*kron(*factors)
    return s.SparseMatrix(out)
E=[slot(t) for t in range(2)]
F=[[slot(t,q) for q in range(4)] for t in range(2)]
A=[s.SparseMatrix(sum(F[t],s.zeros(64))/4) for t in range(2)]
N=[kron(L,S4,S4),kron(S4,L,S4)]
for t in range(2):assert A[t]==N[t]*E[t]
# Directly enumerate all 16 fresh-frame histories rather than using the claimed factorization.
fresh=sum([F[1][q2]*F[0][q1] for q1,q2 in itertools.product(range(4),repeat=2)],s.zeros(64))/16
exact=E[1]*E[0]
predicted=N[1]*N[0]*exact
assert fresh==predicted
assert N[0]*E[1]==E[1]*N[0]
assert fresh[0,:]==s.eye(64)[0,:]

# Explicit entanglement challenge: three-party GHZ, including coherent initial source memory.
psi=s.zeros(8,1);psi[0]=psi[7]=1
rho=(psi*psi.H)/2
B=[kron(*b) for b in itertools.product(P,repeat=3)]
c=s.Matrix([s.trace(b*rho) for b in B])
assert fresh*c==predicted*c
# Equality on all 64 basis operators already implies equality after arbitrary external reference extension.

# Necessity witness: one reused private frame is not the tensor channel even for identity source.
reused=sum([kron(ptm(a),ptm(a)) for a in WQ],s.zeros(16))/4
independent=kron(L,L)
dreuse=reused-independent
assert dreuse!=s.zeros(16)
wreuse=next((i,j,dreuse[i,j]) for i in range(16) for j in range(16) if dreuse[i,j])

# Necessity witness: an excluded completed-output -> memory CNOT breaks commutation.
C=s.zeros(8)
for b in range(8):
    a=(b>>2)&1
    C[b ^ a,b]=1  # control input/output 1, target retained memory
CPTM=s.SparseMatrix(64,64,lambda i,j:s.simplify(s.trace(B[i]*C*B[j]*C.H)/8))
feedback_actual=A[1]*CPTM*A[0]
feedback_pred=N[1]*N[0]*E[1]*CPTM*E[0]
dfeedback=feedback_actual-feedback_pred
assert dfeedback!=s.zeros(64)
wfeedback=next((i,j,dfeedback[i,j]) for i in range(0,64,4) for j in range(64) if dfeedback[i,j])
# A product payload/memory witness, with the final source memory traced out.
product_witness=None
for axes in itertools.product((1,2,3),repeat=3):
    coeff=[]
    for axis in axes:
        v=s.zeros(4,1);v[0]=v[axis]=1;coeff.append(v)
    change=dfeedback*kron(*coeff)
    if any(change[i] for i in range(0,64,4)):
        k=next(i for i in range(0,64,4) if change[i])
        product_witness={'input_plus_axes':axes,'output_Pauli_index':k//4,'expectation_difference':str(change[k])}
        break
assert product_witness is not None

# Exact Pauli/Bell diamond formula: all nonidentity probabilities sum to 1-p0^T.
pauli_two=[p*q for p in probs for q in probs]
assert sum(pauli_two)==1
bell_trace_distance=(abs(pauli_two[0]-1)+sum(pauli_two[1:]))/2
assert bell_trace_distance==1-probs[0]**2 and bell_trace_distance<=2*(1-probs[0])

# The calibration-to-service error expectation never replaces random e by its mean inside a power.
for T in (1,2,3,10,101):
    for eps in (R(1,100),R(1,3),R(1)):
        emax=9*eps/(32*T)
        assert 1-(1-emax)**T<=T*emax==9*eps/32
        beta=eps/8;nu=eps/4
        assert 9*eps/32+beta+nu==21*eps/32<eps

# Bind governing source and all direct and recursive receipt hashes; no source files modified.
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipts=[
 'ordinary_onsite_two_axis_frozen_memory_recovery_root_receipt_20261028.json',
 'ordinary_onsite_two_axis_frozen_memory_recovery_statistics_receipt_20261028.json',
 'ordinary_local_multilogical_prequential_contractions_root_receipt_20261028.json',
 'ordinary_local_multilogical_prequential_contractions_statistics_receipt_20261028.json',
 'ordinary_one_sided_effect_finite_positive_cost_rounding_statistics_receipt_20261028.json']
verified={}
for name in receipts:
    data=json.loads((ROOT/name).read_text())
    bindings=data.get('sha256',data.get('bindings',{}))
    for file,expected in bindings.items():
        assert digest(ROOT/file)==expected,(name,file)
    verified[name]=len(bindings)
sources=['ordinary_onsite_repeated_service_factorization_20261028.md',
         'ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md',
         'ordinary_onsite_two_axis_frozen_memory_recovery_root_receipt_20261028.md',
         'ordinary_onsite_two_axis_frozen_memory_recovery_statistics_audit_20261028.md',*receipts]
result={
 'status':'PASS_INDEPENDENT_EXACT_FULL_OPERATOR_FACTOR_WITH_BOUNDARY_COUNTEREXAMPLES',
 'reviewer':'producer-workspace/review_repeated_service_factorization',
 'arithmetic':'Exact SymPy rationals and Gaussian rationals; no random draws and no floating tolerance',
 'full_operator_basis_dimension':64,'logical_slots':2,'logical_qubits_per_slot':1,
 'retained_memory_dimension':2,'fresh_frame_histories_enumerated':16,
 'time_inhomogeneous_noncommuting_memory_instruments':True,
 'uniform_XZ_CP_contrast':'2/5','memory_branch_XYZ_contrasts':contrast,
 'coherent_memory_retained_in_output':True,
 'initial_entangled_GHZ_payload_memory_state_checked':True,
 'all_reference_extensions_follow_from_complete_linear_map_equality':True,
 'single_output_Pauli_probabilities':list(map(str,probs)),
 'two_output_Pauli_identity_failure':str(bell_trace_distance),
 'reused_frame_counterexample_PTM_entry':[wreuse[0],wreuse[1],str(wreuse[2])],
 'excluded_output_memory_feedback_counterexample_PTM_entry':[wfeedback[0],wfeedback[1],str(wfeedback[2])],
 'feedback_product_input_payload_marginal_witness':product_witness,
 'finite_T_mean_budget_cases':15,'receipt_binding_counts':verified,
 'source_calls':0,'acquisition_outcomes':0,'random_draws':0,
 'physical_gates_or_hardware_executed':False,
 'sha256':{file:digest(ROOT/file) for file in sources}}
(ROOT/'onsite_repeated_service_factorization_independent_check_20261028.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
