import sys
sys.dont_write_bytecode=True
import sympy as s
from pathlib import Path
x,y,u,v=s.symbols('x y u v',real=True);V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C1=x*(u*u-v*v);C2=2*x*u*v;HF=s.hessian(F,V)
R=[s.Matrix([1,0,1,0]),s.Matrix([1,0,-1,0]),s.Matrix([2,0,0,2])]
A,B,D=s.symbols('A B D',positive=True);alpha=[A,B,D]
f=(9*A*A+4*A*B+48*A*D+9*B*B+48*B*D+144*D*D)/8
H=s.zeros(4);W=s.zeros(4,2);T=s.zeros(2)
grad=[s.Matrix([s.diff(C,j) for j in V]) for C in [C1,C2]]
for i,Ri in enumerate(R):
 Hi=HF.subs(dict(zip(V,Ri)));gi=s.Matrix.hstack(*[g.subs(dict(zip(V,Ri))) for g in grad]);weight=alpha[i]/2
 H+=weight*Hi;W+=weight*gi;T+=weight*gi.T*Hi.pinv()*gi
K=H.row_join(W).col_join(W.T.row_join(T));target=s.Matrix([-4,0,0,0,-1,0])
print('detK',s.factor(K.det()),flush=True)
X=(K.inv()*target).applyfunc(s.factor)
E=s.factor(A*B*D*(target.T*X)[0]/2);gap=s.factor(f-E)
rad=(3*A*A+4*A*B+24*A*D+3*B*B+24*B*D+48*D*D)/8
print('multipliers',X.T);print('E=',E);print('gap=',gap);print('gap minus 2rad',s.factor(gap-2*rad))
backs=[]
for i,Ri in enumerate(R):
 Hi=HF.subs(dict(zip(V,Ri)));gi=s.Matrix.hstack(*[g.subs(dict(zip(V,Ri))) for g in grad])
 ai=(X[:4,0]+Hi.pinv()*gi*X[4:,0]).applyfunc(s.factor);backs.append(ai)
 print('A',i,ai.T)
Path(__file__).with_name('full_face_exact.txt').write_text('\n'.join(['K='+str(K),'multipliers='+str(X),'E='+str(E),'gap='+str(gap),'gap_minus_2rad='+str(s.factor(gap-2*rad))]+['A'+str(i)+'='+str(a) for i,a in enumerate(backs)])+'\n')
for i,ai in enumerate(backs):
 kernel=[s.Matrix([1,0,-s.Rational(1,2),0]),s.Matrix([1,0,s.Rational(1,2),0]),s.Matrix([1,0,0,-s.Rational(1,2)])][i]
 bj=(ai-ai[0]*kernel).applyfunc(s.factor)
 print('gauge B',i,bj.T)
