import sympy as s,json
X=s.Matrix([[0,1],[1,0]]);A=[X*s.diag(1,1/s.sqrt(2)),X*s.Matrix([[0,1/s.sqrt(2)],[0,0]])]
F=lambda r:s.simplify(sum((a*r*a.T for a in A),s.zeros(2)))
sigma=s.diag(s.Rational(1,3),s.Rational(2,3));assert F(sigma)==sigma
E=[s.Matrix([[int(i==a and j==b) for j in range(2)] for i in range(2)]) for a in range(2) for b in range(2)]
J=sum((s.kronecker_product(e,F(e)) for e in E),s.zeros(4))/2
JD=sum((s.kronecker_product(e,F(s.diag(e[0,0],e[1,1]))) for e in E),s.zeros(4))/2
w=s.Matrix([0,1,-s.sqrt(2),0])/s.sqrt(3)
assert s.simplify((w.T*J*w)[0])==0
assert s.simplify((w.T*JD*w)[0])==s.Rational(1,3)
a,b=s.symbols('a b');assert s.Matrix([[0,a],[a/s.sqrt(2),b]]).det()==-s.sqrt(2)*a*a/2
out={'stationary_state':['1/3','2/3'],'choi_rank':J.rank(),'pinched_choi_rank':JD.rank(),'w_J_w':'0','w_JDelta_w':'1/3','product_vector_determinant':'-a^2/sqrt(2)'}
open('STRONGER_CHECKS.json','w').write(json.dumps(out,indent=2)+'\n');print(out)
