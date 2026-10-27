import sympy as S
s=S.symbols('s',positive=True);b=S.Rational(2,3);c=S.Rational(1,3);v=S.Matrix([S.Rational(1,3),2*S.I/3,0,S.Rational(2,3),0,0]);P=v*v.conjugate().T
p=S.Rational(1,9);d=S.Rational(4,81);Q=S.kronecker_product(S.eye(3),S.diag(1,c));A=S.eye(6)/s-b/(s*(s+b))*P
T=sum((A[2*i:2*i+2,2*i:2*i+2] for i in range(3)),S.zeros(2));W=S.Matrix(S.kronecker_product(S.eye(3),T))
for i in range(3):
 for j in range(3):W[2*i:2*i+2,2*j:2*j+2]-=A[2*j:2*j+2,2*i:2*i+2]
W/=2
ratio=(S.eye(6)+Q*W).det(method='domain-ge')**2/((S.eye(6)+Q*A/3).det(method='domain-ge')**3*(S.eye(2)+S.diag(1,c)*T).det())
w=s+b;q=p+(1-p)*c;r=1-p+p*c;D=(s+1)*(s+c);Di=(3*s+1)*(3*s+c);AA=2*w*D-b*(q*s+c);BB=4*w*w*D-2*b*w*(q*s+c)+b*b*c*d;J=9*s*s+(9*b+3+3*c)*s+c+3*b*r;R=w*w*(s+3)*(s+3*c)-b*w*(p*(s+3*c)+(1-p)*c*(s+3))+b*b*c*d
formula=3**18*s**5*D*D*AA*AA*BB*BB/(64*w*Di**6*J**3*R)
assert S.factor(ratio-formula)==0
print('Exact actual complex6x6 clock/output and2x2 marginal ratio PASS.')
