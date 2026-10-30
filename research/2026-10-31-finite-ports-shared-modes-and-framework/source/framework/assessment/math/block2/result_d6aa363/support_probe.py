import sympy as s
x1,x2,y1,y2=s.symbols('x1 x2 y1 y2');Z=s.Matrix([x1,x2,y1,y2]);N=x1*x1+x2*x2-y1*y1-y2*y2
F=2*(x1*x1+x2*x2)*(y1*y1+y2*y2)+(y1*y1+y2*y2)**2
C=x1*(y1*y1-y2*y2)+2*x2*y1*y2
nu=s.Rational(3,16);p=F+C+nu*(x1*x1+x2*x2+y1*y1+y2*y2)
base=s.Matrix([-s.Rational(1,4),0,0,-s.Rational(1,4)]);bs=dict(zip(Z,base));grad=s.Matrix([s.diff(p,z) for z in Z]).subs(bs)
inc=Z-base;Ninc=inc[0]**2+inc[1]**2-inc[2]**2-inc[3]**2
E=s.expand(p-p.subs(bs)-(grad.T*inc)[0]-s.Rational(1,16)*Ninc)
mins=s.solve([s.diff(E,x1),s.diff(E,x2)],(x1,x2));Elim=s.factor(E.subs(mins));print('base grad',grad);print('eliminated support',Elim)
num,den=s.fraction(Elim)
lo=(s.oo,None)
for i in range(-30,31):
 for j in range(-30,31):
  val=Elim.subs({y1:s.Rational(i,40),y2:s.Rational(j,40)})
  if val<lo[0]:lo=(val,(s.Rational(i,40),s.Rational(j,40)))
print('min grid exact',lo,'decimal',float(lo[0]))
print('background new X', {k:s.factor(v.subs(dict(zip([y1,y2],lo[1])))) for k,v in mins.items()})
