import sympy as S
x=S.symbols('a b c d',real=True);a,b,c,d=x;q=a*d-b*c;N=sum(z*z for z in x)
F=N*N-4/S.sqrt(3)*N*q;HF=S.hessian(F,x);DF=S.Matrix([S.diff(F,z) for z in x]);A=S.Matrix([0,-S.sqrt(3)/3,1,0])
s,t=S.symbols('s t',real=True);k=t*(1-t);g=s*(1-s)
def meanpoly(P):
 ans=0
 for f,L,U in [(2*s,S.Integer(0),S.Rational(1,3)),(1-s,S.Rational(1,3),S.Integer(1))]:
  grad=[S.diff(f,s)*k,f*S.diff(k,t),S.diff(g,s)*k,g*S.diff(k,t)]
  pp=S.Poly(S.expand(P.subs(dict(zip(x,grad)),simultaneous=True)),s,t)
  ans+=sum(v*(U**(i+1)-L**(i+1))/S.Integer(i+1)/S.Integer(j+1) for (i,j),v in pp.terms())
 return S.simplify(ans)
h=meanpoly((A.T*HF*A)[0]);b=meanpoly((DF.T*A)[0]);c=meanpoly(F)
print('beta',b,'h',h,'c',c,'ratio',S.simplify(b/h),'loss',S.simplify(b*b/(2*h)))
HH=HF.applyfunc(meanpoly)
print('minors',[S.simplify(HH[:j,:j].det()) for j in range(1,5)])
