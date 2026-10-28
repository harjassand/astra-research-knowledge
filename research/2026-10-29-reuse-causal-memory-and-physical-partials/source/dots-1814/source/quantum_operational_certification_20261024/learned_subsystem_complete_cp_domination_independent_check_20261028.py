"""Independent exact complete-CP and adaptive-feedback checks.
No source calls, random draws, floating tolerances, or author-check imports.
"""
from pathlib import Path
import hashlib,json,itertools
import sympy as s
ROOT=Path(__file__).resolve().parent;R=s.Rational
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
P=[I,X,Y,Z]
def simp(x):return s.simplify(x)
def kron(*xs):return s.SparseMatrix(s.kronecker_product(*xs))
def ptm(A):return s.SparseMatrix(4,4,lambda i,j:simp(s.trace(P[i]*A*P[j]*A.H)/2))
def vec(A):return s.Matrix([A[i,j] for i in range(A.rows) for j in range(A.cols)])
def choi_terms(terms):
 out=s.zeros(terms[0][1].rows*terms[0][1].cols)
 for weight,K in terms:out+=weight*vec(K)*vec(K).H
 return simp(out)
W=[R(12,13)*I-s.I*R(5,13)*X,R(4,5)*I-s.I*R(3,5)*Z]
B=s.Matrix([[R(3,5),R(4,5)],[-R(4,5),R(3,5)]])
assert B.H*B==I
A=[kron(W[l],B[l,:]) for l in range(2)]
assert simp(sum([a.H*a for a in A],s.zeros(4)))==s.eye(4)
# Recover Pauli rows from the actual 2-by-4 receiver Kraus matrices.
T=[]
for g in range(4):
 effect=s.zeros(2)
 for a in A:
  row=s.Matrix([[simp(s.trace(P[g].H*a[:,[j,2+j]])/2) for j in range(2)]])
  effect+=row.H*row
 T.append(simp(effect))
assert sum(T,s.zeros(2))==I
pclean=[R(144,169),R(16,25)];c=R(16,25);b=1-c
assert T[0]==B.H*s.diag(*pclean)*B
assert T[0][0,1]!=0
assert (T[0]-c*I).eigenvals()=={R(896,4225):1,0:1}
# A deliberately non-dominant native Pauli law: p_X > p_I, no service contrast assumption.
pnative=[R(1,5),R(3,5),R(1,5),0]
assert pnative[1]>pnative[0]
U=s.Matrix([[R(3,5),R(4,5)],[-R(4,5),R(3,5)]])
V=s.Matrix([[R(5,13),R(12,13)],[-R(12,13),R(5,13)]])
K=[[s.diag(R(3,5),R(4,5)),U*s.diag(R(4,5),R(3,5))],
   [s.diag(R(4,5),R(3,5)),V*s.diag(R(3,5),R(4,5))]]
Kp=[]
for t in range(2):
 assert sum([a.H*a for a in K[t]],s.zeros(2))==I
 assert K[t][0]*K[t][1]!=K[t][1]*K[t][0]
 assert sum([a*Y*a.H for a in K[t]],s.zeros(2))!=s.zeros(2)
 Kp.append([sum([B[l,g]*K[t][g] for g in range(2)],s.zeros(2)) for l in range(2)])
 assert sum([a.H*a for a in Kp[t]],s.zeros(2))==I
# Verify the non-diagonal gauge-effect contraction on every memory matrix unit.
def contract(effect,state):
 out=s.zeros(2)
 for g,h in itertools.product(range(2),repeat=2):out+=effect[h,g]*state[2*g:2*g+2,2*h:2*h+2]
 return simp(out)
for t in range(2):
 J=K[t][0].col_join(K[t][1]);assert J.H*J==I
 for i,j in itertools.product(range(2),repeat=2):
  E=s.zeros(2);E[i,j]=1
  for gamma in range(4):
   coeff=[simp((B*T[gamma]*B.H)[l,l]) for l in range(2)]
   expected=sum([coeff[l]*Kp[t][l]*E*Kp[t][l].H for l in range(2)],s.zeros(2))
   assert contract(T[gamma],J*E*J.H)==simp(expected)
# Direct 16-by-16 Choi check: framed CP map minus c exact map is the explicit positive residual.
residual_terms=[(0,0,pclean[0]-c),(0,1,R(25,169)),(1,3,R(9,25))]
for t in range(2):
 exact_terms=[];framed_terms=[];res_terms=[]
 for alpha,pa in enumerate(pnative):
  if not pa:continue
  for l in range(2):
   exact_terms.append((pa,kron(P[alpha],Kp[t][l])))
   for Q in P:framed_terms.append((pa/4,kron(Q.H*W[l]*P[alpha]*Q,Kp[t][l])))
  for l,gamma,w in residual_terms:res_terms.append((pa*w,kron(P[gamma]*P[alpha],Kp[t][l])))
 assert choi_terms(framed_terms)-c*choi_terms(exact_terms)==choi_terms(res_terms)
 assert all(weight>=0 for weight,_ in res_terms)
 assert simp(sum([weight*k.H*k for weight,k in res_terms],s.zeros(4)))==b*s.eye(4)
# Full two-slot process on payload1,payload2,retained memory; all 64 input operators.
S4=s.eye(4)
def slot(t,kind,frame=0):
 out=s.zeros(64)
 for alpha,pa in enumerate(pnative):
  if not pa:continue
  if kind=='residual':terms=[(l,P[gamma]*P[alpha],pa*w) for l,gamma,w in residual_terms]
  else:terms=[(l,P[alpha] if kind=='exact' else P[frame].H*W[l]*P[alpha]*P[frame],pa) for l in range(2)]
  for l,logical,weight in terms:
   factors=[S4,S4,ptm(Kp[t][l])];factors[t]=ptm(logical)
   out+=weight*kron(*factors)
 return s.SparseMatrix(out)
E=[slot(t,'exact') for t in range(2)]
Rmap=[slot(t,'residual') for t in range(2)]
F=[[slot(t,'framed',q) for q in range(4)] for t in range(2)]
L=[s.SparseMatrix(sum(F[t],s.zeros(64))/4) for t in range(2)]
for t in range(2):assert L[t]==c*E[t]+Rmap[t]
# Legitimate common controller: completed output1 coherently controls next input2.
C=s.zeros(8)
for z in range(8):C[z ^ (2*((z>>2)&1)),z]=1
basis=[kron(*ps) for ps in itertools.product(P,repeat=3)]
Cptm=s.SparseMatrix(64,64,lambda i,j:simp(s.trace(basis[i]*C*basis[j]*C.H)/8))
learned=sum([F[1][q2]*Cptm*F[0][q1] for q1,q2 in itertools.product(range(4),repeat=2)],s.zeros(64))/16
exact=E[1]*Cptm*E[0]
nonclean=c*E[1]*Cptm*Rmap[0]+c*Rmap[1]*Cptm*E[0]+Rmap[1]*Cptm*Rmap[0]
assert learned-c*c*exact==nonclean
assert nonclean[0,:]==(1-c*c)*s.eye(64)[0,:]
assert (nonclean/(1-c*c))[0,:]==s.eye(64)[0,:]
# A partial trace of final source memory preserves this map equality.
for i in range(0,64,4):assert learned[i,:]==c*c*exact[i,:]+nonclean[i,:]
# Retired-key violation: the key-aware controller removes twirling with reference access,
# even when it discards the key before the final test.
phi=s.Matrix([1,0,0,1])/s.sqrt(2);rho=phi*phi.H
Wkey=W[0];amp=R(5,13);ckey=R(144,169);bkey=R(25,169)
coherent=kron(Wkey,I)*rho*kron(Wkey,I).H
key_unwound=s.zeros(4)
for Q in P:
 out=kron(Q.H*Wkey*Q,I)*rho*kron(Q.H*Wkey*Q,I).H
 controller=kron(Q,s.conjugate(Q))
 assert simp(controller*rho*controller.H)==rho
 key_unwound+=controller*out*controller.H/4
assert simp(key_unwound)==simp(coherent)
evals=simp(coherent-rho).eigenvals()
assert evals=={0:2,amp:1,-amp:1} and amp>bkey
# In the explicitly key-flagged Choi output a single key block already violates CP domination.
phi_x=kron(X,I)*phi
witness=amp*phi+s.I*R(12,13)*phi_x
assert simp((witness.H*witness)[0])==1
neg=simp((witness.H*(coherent-ckey*rho)*witness)[0]/4)
assert neg==-R(900,28561)
# Retaining gauge cannot be controlled by the Bell effect: b=0 but gauge X differs from identity.
g0=s.Matrix([1,0]);assert (X*g0).H*g0==s.zeros(1)
# Exact approximate/exact acquisition-to-process scalar budgets.
scalar_cases=0
for Tn,q,eps,tau in itertools.product((1,2,5,19),(1,3),(R(1),R(1,17)),(R(0),R(1,32),R(1,4))):
 root=3*s.sqrt(R(q,2))*tau+s.sqrt(eps/Tn)/3
 bound=9*Tn*q*tau*tau+R(43,72)*eps
 assert simp(bound-(Tn*root**2+eps/8+eps/4))>=0
 assert R(9,32)*eps+eps/8+eps/4==R(21,32)*eps
 scalar_cases+=1

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
sources=['learned_subsystem_complete_cp_domination_20261028.md',
 'ordinary_approximate_onsite_frozen_memory_recovery_20261028.md',
 'ordinary_approximate_onsite_frozen_memory_recovery_statistics_receipt_20261028.json',
 'ordinary_approximate_onsite_frozen_memory_recovery_memory_receipt_20261028.json',
 'ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md',
 'ordinary_onsite_two_axis_frozen_memory_recovery_root_receipt_20261028.json',
 'ordinary_onsite_two_axis_frozen_memory_recovery_statistics_receipt_20261028.json']
for receipt in sources[2:4]:
 data=json.loads((ROOT/receipt).read_text())
 assert data['source_sha256']==digest(ROOT/sources[1])
 for name,expected in data['sha256'].items():assert digest(ROOT/name)==expected,(receipt,name)
assert digest(ROOT/sources[0])=='5890ae9c708c08aa4dd9909d1e6154fd8bbf64973f51395c5bf31552d3eebf6d'
sources+=['learned_cp_domination_astra_comparison_20261028.md','astra_task_effects_cp_comparison_20261028.json']
result={'status':'PASS_EXACT_COMPLETE_CP_ADAPTIVE_FEEDBACK_AND_KEY_BOUNDARY',
 'reviewer':'producer-workspace/review_repeated_service_factorization',
 'arithmetic':'Exact rational/Gaussian rational and symbolic square roots; no tolerances',
 'logical_slots':2,'full_operator_basis_dimension':64,'fresh_frame_histories':16,
 'non_diagonal_uniform_clean_gauge_effect':str(T[0]),'uniform_b':str(b),
 'positive_clean_effect_residual_eigenvalues':['896/4225','0'],
 'native_Pauli_probabilities':list(map(str,pnative)),
 'native_identity_dominance_satisfied':False,'source_weak_memory_instruments_noncommuting':True,
 'legitimate_feedback':'CNOT completed output1 -> future input2, no direct source-memory access',
 'two_slot_all_clean_probability':str(c*c),'two_slot_process_error_bound':str(1-c*c),
 'complete_CP_residual':'Explicit sum of nonnegative Kraus outer products, trace effect b I',
 'leaked_retired_key_final_half_trace_distance':str(amp),
 'private_averaged_bound_for_key_example':str(bkey),
 'key_flagged_CP_difference_negative_witness':str(neg),
 'retained_gauge_b_zero_failure_checked':True,
 'acquisition_scalar_budget_cases':scalar_cases,'source_calls':0,'source_outcomes':0,'random_draws':0,
 'quantum_circuit_or_production_synthesis_executed':False,
 'sha256':{name:digest(ROOT/name) for name in sources}}
(ROOT/'learned_subsystem_complete_cp_domination_independent_check_20261028.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
