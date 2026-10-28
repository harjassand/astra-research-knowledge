"""Exact full-algebra quotient diagnostic; zero source samples."""
import sympy as s, pathlib, hashlib, json
root=pathlib.Path(__file__).parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);F=[I,X,Y,Z]
W=s.diag(1,s.Rational(1,4),s.Rational(1,4),s.Rational(1,4));W[1,3]=s.Rational(1,4)
P0=s.Matrix([[1,0,0,0],[0,0,0,1]])
Q=s.Matrix([[s.Rational(1,2)]*2,[s.Rational(1,4),s.Rational(1,16)]])
P=Q.inv()*P0;L=P0.T*Q;rho=s.Matrix([s.Rational(1,2),0,0,s.Rational(1,4)])
tau=s.Matrix([[2,0,0,0]]);m=s.ones(1,2)
assert P*L==s.eye(2) and m*P==tau and P*rho==s.Matrix([1,0])
J=sum((W[i,j]*s.kronecker_product(F[j].T,F[i])/2 for i in range(4) for j in range(4)),s.zeros(4))
assert all(z>=0 for z in (J-s.eye(4)/4).eigenvals())
C=P*W*L;assert P*W==C*P and tau*W==tau
u,v=s.symbols('u v');col=s.Matrix([0,u,v,1])
assert W*col-s.Rational(1,4)*col==s.Matrix([0,s.Rational(1,4),0,0])
Hp=s.Matrix([[1,1],[s.Rational(5,8),s.Rational(17,32)]])
assert Hp.det()==-s.Rational(3,32)
# Verify both full test-and-reset instrument branches and quotient invariance.
test_maps=[]
for sign in (-1,1):
    row=s.Matrix([[1,0,0,sign*s.Rational(1,2)]])
    B=rho*row
    JB=sum((B[i,j]*s.kronecker_product(F[j].T,F[i])/2 for i in range(4) for j in range(4)),s.zeros(4))
    assert min(JB.eigenvals())==s.Rational(1,16)
    CB=P*B*L;assert P*B==CB*P
    test_maps.append(B)
assert tau*sum(test_maps,s.zeros(4))==tau
# Symbolic correction and trace identity for an arbitrary trace-annihilating delta C.
x,y=s.symbols('x y');delta=s.Matrix([[x,y],[-x,-y]])
assert m*delta==s.zeros(1,2)
corrected=W+L*delta*P
assert P*corrected==(C+delta)*P and tau*corrected==tau
out={'kind':'exact algebra, zero source samples','full_choi_lower':'1/4','test_branch_choi_lower':'1/16',
     'core_determinant':str(Hp.det()),'surjection_and_trace_checks':True,
     'no_invariant_section_same_map':True,'symbolic_correction_check':True,
     'source_sha256':hashlib.sha256((root/'SURJECTIVE_CP_EXTENSION_ADDENDUM.md').read_bytes()).hexdigest(),
     'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(root/'surjective_cp_extension_exact_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
