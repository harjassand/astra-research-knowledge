import sympy as S
s=S.symbols('s',positive=True);b=S.Rational(2,3);C=[S.Integer(1),S.Rational(1,3),S.Rational(2,5)];v=S.Matrix([1,0,0,0,1,0,0,0,1]);P=v*v.T/3;Q=S.kronecker_product(S.eye(3),S.diag(*C));A=S.eye(9)/s-b/(s*(s+b))*P;T=sum((A[3*i:3*i+3,3*i:3*i+3] for i in range(3)),S.zeros(3));W=S.Matrix(S.kronecker_product(S.eye(3),T))
for i in range(3):
 for j in range(3):W[3*i:3*i+3,3*j:3*j+3]-=A[3*j:3*j+3,3*i:3*i+3]
W/=2
ratio=(S.eye(9)+Q*W).det(method='domain-ge')**2/((S.eye(9)+Q*A/3).det(method='domain-ge')**3*(S.eye(3)+S.diag(*C)*T).det())
O=[6*(s+b)*(s+C[i])*(s+C[j])-b*(C[i]*(s+C[j])+C[j]*(s+C[i])) for i in range(3) for j in range(i)]
J=S.cancel((3*(s+b)*S.prod(3*s+x for x in C)-b*sum(C[i]*S.prod(3*s+C[j] for j in range(3) if j!=i) for i in range(3)))/s)
R=[3*(s+b)*(s+3*x)-b*x for x in C]
formula=3**27*s**9*S.prod((s+x)**2 for x in C)*S.prod(o**2 for o in O)/(64*S.prod((3*s+x)**6 for x in C)*J**3*S.prod(R))
assert S.factor(ratio-formula)==0
print('Exact actual9x9 output/input,3x3 reference paired-pencil identity PASS.')
