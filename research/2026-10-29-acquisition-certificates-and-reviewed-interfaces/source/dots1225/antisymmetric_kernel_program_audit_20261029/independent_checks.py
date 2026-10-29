import sympy as s,json,itertools
from pathlib import Path
root=Path(__file__).parent
A=s.Matrix([[s.Rational(v) for v in row] for row in json.loads((root/'replay/transducer_matrix.json').read_text())['matrix']])
assert (A*A.T).eigenvals()=={s.Rational(1,4):1,s.Rational(1,2):9,s.Integer(0):6}
# Exact d=9 Hodge minors, without materializing the 9^8 space.
w,x,y,z=s.symbols('w x y z',real=True)
q=s.Matrix([w,x,y,z]);V=s.Matrix([[w-s.I*z,-y-s.I*x],[y-s.I*x,w+s.I*z]])
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
R=s.Matrix([[s.expand(s.trace(pa[i]*V*pa[j]*V.conjugate().T)/2) for j in range(3)] for i in range(3)])
Q=sum(v*v for v in q)
assert all(s.expand(a-b)==0 for a,b in zip(A*s.Matrix([a*b for a in list(R) for b in list(R)]),Q*s.kronecker_product(q,q)))
# Choi resource V_ab/sqrt2 and identity Bell contraction delta_{input,b}/sqrt2 -> V/2.
tele=s.Matrix(2,2,lambda a,j:sum(V[a,b]*int(j==b)/2 for b in range(2)))
assert tele==V/2 and s.simplify(V.conjugate().T*V-Q*s.eye(2))==s.zeros(2)
minor_cases=0
for u in [(1,2,3),(-2,1,0),(0,0,0)]:
 den=1+sum(v*v for v in u);qr=[s.Rational(1-sum(v*v for v in u),den)]+[s.Rational(2*v,den) for v in u]
 rv=R.subs(dict(zip(q,qr)));c=s.Matrix(list(rv));pivot=next(i for i in range(9) if c[i]!=0);idx=[i for i in range(9) if i!=pivot]
 basis=s.zeros(9,8)
 for col,j in enumerate(idx):basis[j,col]=1;basis[pivot,col]=-c[j]/c[pivot]
 assert c.T*basis==s.zeros(1,8)
 h=s.Matrix([(-1)**a*basis.minor_submatrix(a,-1).det() if False else (-1)**a*basis.extract([i for i in range(9) if i!=a],list(range(8))).det() for a in range(9)])
 assert h*c[pivot]==c*h[pivot]
 minor_cases+=1
# New reviewer-originated improvement; not included in independent acceptance of author v1.
As=s.Matrix(16,81,lambda i,j:(A[i,j]+A[i,9*(j%9)+j//9])/2);B=2*As;P=B*B.T
assert P==P.T and P*P==P and P.trace()==10
assert all(s.expand(a-b)==0 for a,b in zip(B*s.Matrix([a*b for a in list(R) for b in list(R)]),2*Q*s.kronecker_product(q,q)))
(root/'SYMMETRIZED_TRANSDUCER_CANDIDATE.json').write_text(json.dumps({'status':'new reviewer-originated construction; separately review before acceptance','matrix':[[str(v) for v in row] for row in B.tolist()],'BBt_is_exact_rank10_orthogonal_projector':True,'conditional_transduction_success':'4/9','conditional_one_gate_success':'1/9'},indent=2)+'\n')
(root/'independent_checks.json').write_text(json.dumps({'exact_A_spectrum':{'0':6,'1/4':1,'1/2':9},'independent_symbolic_orientation_and_transducer_identity':True,'exact_d9_hodge_minor_cases':minor_cases,'all_input_teleportation_Kraus':'V/2','reviewer_originated_improvement_is_separate':True},indent=2)+'\n');print('Independent exact orientation, minors, teleportation and transducer checks passed')
