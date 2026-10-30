import sys
sys.dont_write_bytecode=True
import sympy as s
from sympy.polys.matrices import DomainMatrix
from pathlib import Path
import json
base=Path(__file__).parent
x,y,u,v=s.symbols('x y u v',real=True);V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;Q=s.Rational(3,16)*(r+t)
HF=s.hessian(F,V);dF=s.Matrix([s.diff(F,j) for j in V]);dC=s.Matrix([s.diff(C,j) for j in V])
R=[s.Matrix([1,0,1,0]),s.Matrix([1,0,-1,0]),s.Matrix([2,0,0,2])]
alpha=s.symbols('A B D',positive=True);A,B,D=alpha;cs=s.symbols('c0 c1 c2')
G=sum((R[j]*cs[j] for j in range(3)),s.zeros(4,1)); sub=dict(zip(V,G))
def avg(poly):
 out=0
 for powers,co in s.Poly(s.expand(poly),*cs).terms():
  if sum(powers)==0:val=1
  elif sorted(powers)==[0,0,2]:val=alpha[powers.index(2)]/2
  elif powers==(1,1,1):val=s.Rational(1,4)
  elif sorted(powers)==[0,0,4]:val=3*alpha[powers.index(4)]**2/8
  elif sorted(powers)==[0,2,2]:
   ids=[i for i in range(3) if powers[i]==2];val=alpha[ids[0]]*alpha[ids[1]]/4
  else:val=0
  out+=co*val
 return s.factor(out)
def get(p):return avg(p.subs(sub,simultaneous=True))
H=HF.applyfunc(get);w=dC.applyfunc(get);v0=dF.applyfunc(get);c0=get(C);f=get(F);q=get(Q)
tcost=0
for i,Ri in enumerate(R):
 sb=dict(zip(V,Ri));Hi=HF.subs(sb);gi=dC.subs(sb);cost=(gi.T*Hi.pinv()*gi)[0]
 print('ray',i,'cost',cost)
 tcost+=alpha[i]*cost/2
K=H.row_join(w).col_join(w.T.row_join(s.Matrix([[tcost]])))
z=v0.col_join(s.Matrix([c0]));T=A*B*D
N=K.row_join(z).col_join((T*z.T).row_join(s.Matrix([[2*f]])))
poly=s.Poly(DomainMatrix.from_Matrix(N).convert_to(s.QQ.poly_ring(*alpha)).det().as_expr(),*alpha)
print('H=',H);print('w=',w,'v0=',v0,'c0=',c0,'f=',f,'q=',q,'tcost=',tcost)
print('detK=',s.factor(K.det()));print('detN=',s.factor(poly.as_expr()))
print('negative',[(p,co) for p,co in poly.terms() if co<0])
Kinv=K.inv();X=s.simplify(Kinv*z)
E=s.factor(T*(z.T*X)[0]/2);gap=s.factor(f-E)
print('E=',E,'gap=',gap)
for i,Ri in enumerate(R):
 sb=dict(zip(V,Ri));Hi=HF.subs(sb);gi=dC.subs(sb)
 Ai=s.simplify(X[:4,0]+X[4]*Hi.pinv()*gi)
 print('background / product amplitudes',i,Ai.T)
(base/'exact.txt').write_text('\n'.join(['H='+str(H),'w='+str(w),'v0='+str(v0),'c0='+str(c0),'f='+str(f),'q='+str(q),'t='+str(tcost),'detK='+str(s.factor(K.det())),'detN='+str(s.factor(poly.as_expr())),'E='+str(E),'gap='+str(gap),'multipliers='+str(X)])+'\n')
(base/'certificate.json').write_text(json.dumps({'det_terms':[(p,str(co)) for p,co in poly.terms()],'negative_count':sum(1 for p,co in poly.terms() if co<0)},indent=2)+'\n')
