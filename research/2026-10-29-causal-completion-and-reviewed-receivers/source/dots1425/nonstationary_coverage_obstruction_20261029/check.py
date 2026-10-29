import sympy as s,json
r=s.sqrt(3); I=s.eye(2); Z=s.diag(1,-1); X=s.Matrix([[0,1],[1,0]])
p=s.Matrix([r/2,s.Rational(1,2)]);m=s.Matrix([r/2,-s.Rational(1,2)]); w=s.Matrix([-s.Rational(1,2),r/2])
P=p*p.T;M=m*m.T
sigma=(I+r*X/4+Z/2)/2
N=lambda A:s.simplify(A[0,0]*P+A[1,1]*M)
axis=(r*X+2*Z)/s.sqrt(7)
D=lambda A:s.simplify((A+axis*A*axis)/2)
E=[s.Matrix([[int(i==a and j==b) for j in range(2)] for i in range(2)]) for a in range(2) for b in range(2)]
J=sum((s.kronecker_product(e,N(e)) for e in E),s.zeros(4))/2
JD=sum((s.kronecker_product(e,N(D(e))) for e in E),s.zeros(4))/2
W=s.kronecker_product(s.Matrix([1,0]),w)
assert N(sigma)==sigma and sigma.det()==s.Rational(9,64)
assert (W.T*J*W)[0]==0
assert s.simplify((W.T*JD*W)[0])==s.Rational(9,112)
result={'fixed_state_determinant':str(sigma.det()),'choi_rank':J.rank(),'pinched_input_choi_rank':JD.rank(),'w_J_w':'0','w_JDelta_w':'9/112','positive_CP_coverage_impossible':True}
open('CHECKS.json','w').write(json.dumps(result,indent=2)+'\n');print(result)
