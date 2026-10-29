"""Exact two/three-call adaptive memory port, not an IID simulator fixture."""
import sympy as s,json
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[I,X,Y,Z];H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
kron=s.kronecker_product
CNOT=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
U=kron(I,H)*CNOT
# One source call U acts on current query and the SAME retained memory.
# Fresh |+> program query followed by X readout gives these memory Kraus maps.
B=[H*(I+X)/2,H*(I-X)/2]
assert sum((b.H*b for b in B),s.zeros(2))==I
# After payload call: z=0 finishes; z=1 makes a second program call.
# z=1,w=1 invokes the declared reset fallback, never omits the loaded payload.
R=[s.Matrix([[1,0],[0,0]]),s.Matrix([[0,1],[0,0]])]
branches={'z0':[kron(I,B[0])*U], 'z1w0':[kron(H,B[0]*B[1])*U], 'z1w1_timeout':[kron(r,B[1]*B[1])*U for r in R]}
assert s.simplify(sum((a.H*a for aa in branches.values() for a in aa),s.zeros(4)))==s.eye(4)
# Explicitly reconstruct the program source call and its measurement.
plus=s.Matrix([1,1])/s.sqrt(2);minus=s.Matrix([1,-1])/s.sqrt(2)
for z,psi in enumerate([plus,minus]):
 actual=kron(psi.H,I)*U*kron(plus,I)
 assert s.simplify(actual-B[z])==s.zeros(2)
states=[s.Matrix([1,0]),s.Matrix([0,1]),plus,minus,s.Matrix([1,s.I])/s.sqrt(2),s.Matrix([1,-s.I])/s.sqrt(2)]
Ebad=s.zeros(2);Qfail=s.zeros(2);twirl_checks=0;record_effects={}
for record,Ks in branches.items():
 coeff=[]
 for p in P:
  arr=[]
  for A in Ks:
   arr.append(s.Matrix(2,2,lambda m,n:sum(s.conjugate(p[a,b])*A[2*a+m,2*b+n] for a in range(2) for b in range(2))/2))
  coeff.append(arr)
 bad=sum((a.H*a for arr in coeff[1:] for a in arr),s.zeros(2));Ebad+=bad
 for psi in states:
  perp=s.Matrix([-s.conjugate(psi[1]),s.conjugate(psi[0])])
  for A in Ks:
   f=kron(perp.H,I)*A*kron(psi,I)
   Qfail+=f.H*f/6
 # Check every matrix unit, with each actual public adaptive record retained.
 for i in range(4):
  for j in range(4):
   E=s.zeros(4);E[i,j]=1
   twirled=s.zeros(4)
   for p in P:
    for A in Ks:
     G=kron(p,I)*A*kron(p,I);twirled+=G*E*G.H/4
   refined=sum((kron(p,b)*E*kron(p,b).H for p,arr in zip(P,coeff) for b in arr),s.zeros(4))
   assert s.simplify(twirled-refined)==s.zeros(4);twirl_checks+=1
 record_effects[record]=str(s.simplify(sum((a.H*a for a in Ks),s.zeros(4))))
assert s.simplify(Ebad-s.Rational(3,2)*Qfail)==s.zeros(2)
# Extra role leakage invalidates common-port interface: TEST identity, SERVICE X.
# Then actual test failure=0, retired-Pauli bad-service weight=1.
out={'exact_total_TP':True,'same_retained_source_memory':True,'payload_source_calls':1,'adaptive_program_calls_max':2,'complete_calls_max':3,'public_record_branches':list(branches),'post_load_timeout_reset_is_included':True,'record_preserving_matrix_unit_twirl_checks':twirl_checks,'bad_effect':str(s.simplify(Ebad)),'test_failure_effect':str(s.simplify(Qfail)),'effect_identity':'Ebad=(3/2) Qfail exactly','privacy_counterexample':{'role_disclosed_test_map':'identity','role_disclosed_service_map':'X conjugation','test_failure':0,'service_bad_weight':1},'scope':'Finite exact sequential-memory interface check only; no learner completeness, IID programs, physical implementation or guard availability claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
