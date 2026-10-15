import sympy as s
a,b,c,d=s.symbols('a b c d', real=True)
p,q=s.symbols('p q', real=True)
al,be,ga,de=s.symbols('alpha beta gamma delta', real=True)
x=s.Matrix((a,b,c,d)); R=s.Matrix((p,q,0,0))
u=a*a+c*c; v=b*b+d*d; w=a*b+c*d; j=a*d-b*c
F=al*v*v+be*w*w+ga*(u*j-u*u/4-s.Rational(3,2)*u*v)+de*v*j
P=s.expand((R.T*s.hessian(F,x)*R)[0]/2)
M=s.simplify(s.hessian(P,x)/2)
print('M=',M)
print('M(1,0)=',M.subs({p:1,q:0}))
print('M(0,1)=',M.subs({p:0,q:1}))
print('det=',s.factor(M.det()))
print('ga=0 det',s.factor(M.subs(ga,0).det()))
print('ga=0 kernel derivative',M.diff(q).subs({p:1,q:0,ga:0}).extract([0,2,3],[0,2,3]))
print('be=ga kernel derivative',M.diff(q).subs({p:1,q:0,be:ga}).extract([0,1,2,3],[0,1,2,3]))
