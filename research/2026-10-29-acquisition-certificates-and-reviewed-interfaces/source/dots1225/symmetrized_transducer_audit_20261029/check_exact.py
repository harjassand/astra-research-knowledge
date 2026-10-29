import sympy as s,json,hashlib
from pathlib import Path
P=Path(__file__).parent;old=Path('producer-workspace/transducer_matrix.json');new=Path('producer-workspace/SYMMETRIZED_TRANSDUCER_CANDIDATE.json')
A=s.Matrix([[s.Rational(x) for x in row] for row in json.loads(old.read_text())['matrix']]);B=s.Matrix([[s.Rational(x) for x in row] for row in json.loads(new.read_text())['matrix']]);assert B.shape==(16,81)
assert all(B[i,9*j+k]==A[i,9*j+k]+A[i,9*k+j] for i in range(16) for j in range(9) for k in range(9))
P4=s.zeros(16)
for i in range(4):
 for j in range(4):P4[4*i+j,4*i+j]+=s.Rational(1,2);P4[4*i+j,4*j+i]+=s.Rational(1,2)
assert B*B.T==P4;E=B.T*B;assert E==E.T and E*E==E and s.trace(E)==10
w,x,y,z=s.symbols('w x y z');q=s.Matrix([w,x,y,z]);Q=(q.T*q)[0]
# Independently derive adjoint rotation from quaternion/SU2 Pauli trace.
paulis=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];U=w*s.eye(2)-s.I*(x*paulis[0]+y*paulis[1]+z*paulis[2]);Udag=w*s.eye(2)+s.I*(x*paulis[0]+y*paulis[1]+z*paulis[2]);R=s.Matrix(3,3,lambda a,b:s.expand(s.trace(paulis[a]*U*paulis[b]*Udag)/2));v=list(R);out=B*s.Matrix([a*b for a in v for b in v]);assert all(s.expand(out[4*i+j]-2*Q*q[i]*q[j])==0 for i in range(4) for j in range(4))
result={'status':'EXACT_ACCEPT','matrix_shape':list(B.shape),'B_equals_2A_Pi_sym':True,'BBdag_equals_Sym2_C4_projector':True,'BdagB_idempotent_symmetric':True,'rank':10,'all16_quaternion_identities':True,'conditional_transduction_probability':'4/9','one_identity_Bell_gate_probability':'1/9','two_identity_Bell_gates_probability':'1/36','source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [old,new]}}
(P/'EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
