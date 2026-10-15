import sympy as s

a,b,c,d = x = s.symbols('a b c d', real=True)
e,f,p,q = y = s.symbols('e f p q', real=True)
t=s.symbols('t', real=True)
u=a*a+c*c
v=b*b+d*d
w=a*b+c*d
j=a*d-b*c
mon=(u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j)
coeff=s.symbols('f0:9', real=True)
F=sum(k*m for k,m in zip(coeff,mon))
R=s.Matrix((e*p,e*q,f*p,f*q))
P=s.expand((R.T*s.hessian(F,x)*R)[0]/2)
point={a:1,b:0,c:0,d:1,e:1,f:0,p:1,q:t}
conditions=[P.subs(point)]+[s.diff(P,z).subs(point) for z in x+y]
M=s.linear_eq_to_matrix(conditions,coeff)[0]
for tv in (0,1,2,s.sqrt(2)):
    Mt=M.subs(t,tv)
    print('t=',tv,'rank',Mt.rank())
    for n in Mt.nullspace():
        print(' basis:',s.factor(F.subs(dict(zip(coeff,n)))))
print('generic rank',M.rank())
for n in M.nullspace():
    print(' generic basis coeff:',list(map(s.factor,n)))
    print(' generic basis poly:',s.factor(F.subs(dict(zip(coeff,n)))))
