import sympy as s
x,y,u,v,T=s.symbols('x y u v T',real=True); Z=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v;D=r-t
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;P=F+C+s.Rational(3,16)*(r+t)
R=s.Matrix([0,1,1,0]);H=s.hessian(P,Z);Ac={x:-s.Rational(1,4),y:T,u:-T/2,v:-s.Rational(1,4)}
print('nullscore',s.factor((R.T*H.subs(Ac)*R)[0]))
q=s.simplify(H.subs(Ac)*R);print('H.R',q)
lam=s.simplify(q[1]/2);print('lambda delta',lam,'relative to Qzz',s.factor(lam-s.Rational(3,16)))
print('PC H eig symbolic det',s.factor((H.subs(Ac)-lam*s.hessian(D,Z)).det()))
print('A0support',s.factor(P-P.subs(Ac).subs(T,0)-sum(s.diff(P,z).subs(Ac).subs(T,0)*(z-Ac[z].subs(T,0)) for z in Z)-lam.subs(T,0)*sum(s.hessian(D,Z)[i,j]*(Z[i]-Ac[Z[i]].subs(T,0))*(Z[j]-Ac[Z[j]].subs(T,0))/2 for i in range(4) for j in range(4))))
