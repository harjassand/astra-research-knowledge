import sympy as s
from pathlib import Path
a,b,c,d=s.symbols('a b c d'); A=s.Matrix([a,b,c,d]); T=sum(z*z for z in A); D=a*d-b*c
F=s.expand(3*T*T-4*T*D-4*D*D)
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c]);alpha=(3*T+14*D)*theta+(9*T-6*D)*zeta
HF=s.hessian(F,A); Om=s.Matrix(4,4,lambda i,j:s.diff(alpha[j],A[i])-s.diff(alpha[i],A[j]))
h=s.symbols('h:6');B1=s.Matrix([h[0],h[1],h[3],h[4]]);B2=s.Matrix([h[1],h[2],h[4],h[5]])
expr=s.expand((B1.T*HF*B1)[0]+(B2.T*HF*B2)[0]+(B1.T*Om*B2)[0])
x1,x2,y1,y2=s.symbols('x1 x2 y1 y2');p,q,r,v,t,u=s.symbols('p q r v t u')
subs={a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2,h[0]:p+2*r+t,h[1]:-q+u,h[2]:-p+2*r-t,h[3]:q+2*v+u,h[4]:p-t,h[5]:-q+2*v-u}
E=s.factor(expr.subs(subs, simultaneous=True));print('density=',s.collect(E,[x1,x2,y1,y2]))
for AA in ([1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]):
 EE=E.subs(dict(zip([x1,x2,y1,y2],AA)));print('axis',AA,s.factor(EE))
