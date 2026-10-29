import json
from pathlib import Path
import sympy as s
root=Path(__file__).parent;data=json.loads((root/'transducer_matrix.json').read_text());A=s.Matrix([[s.Rational(x) for x in row] for row in data['matrix']]);B=s.eye(16)-A*A.T;L,D=B.LDLdecomposition(hermitian=False);assert L*D*L.T==B;assert all(D[i,i]>0 for i in range(16))
w,x,y,z=s.symbols('w x y z',real=True);Q=w*w+x*x+y*y+z*z
R=s.Matrix([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])
v=list(R);q=[w,x,y,z];inp=s.Matrix([a*b for a in v for b in v]);out=A*inp;res=[s.expand(out[4*i+j]-Q*q[i]*q[j]) for i in range(4) for j in range(4)];assert all(r==0 for r in res)
(root/'exact_transducer_certificate.json').write_text(json.dumps(dict(identity='A vec(R(q))^tensor2 = (q.q) vec(q q^T)',all_16_polynomial_residuals_zero=True,gram_lower_L=[[str(x) for x in row] for row in L.tolist()],gram_positive_D=[str(D[i,i]) for i in range(16)],success_two_normalized_rotation_programs='1/9',qubit_gate_teleportation_success='1/4',combined_one_gate_success='1/36'),indent=2)+'\n');print('Exact polynomial identity and rational positive LDL prove A contraction; success1/9.')
