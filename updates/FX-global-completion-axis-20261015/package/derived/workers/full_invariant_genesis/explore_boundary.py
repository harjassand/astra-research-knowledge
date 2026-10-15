import sympy as s
a,b,c,d=s.symbols('a b c d',real=True)
k,l,m,h,z=s.symbols('k l m h z',real=True)
x=s.Matrix((a,b,c,d))
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;j=a*d-b*c
H=(u+v-2*j)**2
G=k*w*w+l*v*j+m*v*v
F=h*H+G
R=s.Matrix((1,z*k,-z*(k+l),-z*z*k*(k+l)))
P=s.expand((R.T*s.hessian(F,x)*R)[0]/2)
point={a:1,b:0,c:0,d:1}
print('P(I,R)=',s.factor(P.subs(point)))
print('D=0 P(I,R)=',s.factor(P.subs(point).subs(m,l*(k+l)/(2*k))))
print('gradient-A linear-z=',[s.factor(s.diff(P,xx).subs(point).coeff(z,1).subs(m,l*(k+l)/(2*k))) for xx in x])
print('l+2m=0 gradient acoustic e22=',[s.factor(s.diff(s.diff(F,d,2)/2,xx).subs(point).subs(m,-l/2)) for xx in x])
print('k=0 acoustic e11=',s.factor(s.diff(F,a,2)/2))
