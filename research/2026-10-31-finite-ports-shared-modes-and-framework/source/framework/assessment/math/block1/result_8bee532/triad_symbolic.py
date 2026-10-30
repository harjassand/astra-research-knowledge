import sympy as s
from pathlib import Path
E=s.symbols('e',real=True)
x,y,u,v=s.symbols('x y u v',real=True)
V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;Q=s.Rational(3,16)*(r+t)
cs=s.symbols('c1 c2 c3',real=True)
R=[]
for p,q,amp in [(1,0,s.S.One),(2,1,s.Rational(1,16)),(3,1,s.Rational(1,81))]:
 k=p+s.I*E*q
 z=s.I*s.conjugate(k)**4
 w=s.I*k*s.conjugate(k)**3
 R.append(amp*s.Matrix([s.re(z),s.im(z),s.re(w),s.im(w)]).applyfunc(s.expand))
G=sum((R[j]*cs[j] for j in range(3)),s.zeros(4,1))
subs=dict(zip(V,G))
def avg(poly):
 poly=s.Poly(s.expand(poly),*cs); ans=0
 for powers,coeff in poly.terms():
  if sum(powers)==0: val=1
  elif sorted(powers)==[0,0,2]:val=s.Rational(1,2)
  elif powers==(1,1,1):val=s.Rational(1,4)
  elif sorted(powers)==[0,0,4]:val=s.Rational(3,8)
  elif sorted(powers)==[0,2,2]:val=s.Rational(1,4)
  else:val=0
  ans+=coeff*val
 return s.factor(ans)
def get(poly):return avg(poly.subs(subs,simultaneous=True))
H=s.hessian(F,V).applyfunc(get)
vect=s.Matrix([s.diff(F,z) for z in V]).applyfunc(get)
w=s.Matrix([s.diff(C,z) for z in V]).applyfunc(get)
f=get(F);c=get(C);q=get(Q)
print('moments formed',flush=True)
Hu=H.inv()*w; Hv=H.inv()*vect
print('inverted',flush=True)
b=s.factor(2*q-w.dot(Hu));a=s.factor(2*f-vect.dot(Hv));rr=s.factor(c-vect.dot(Hu))
exprs={'detH':s.factor(H.det()),'a':a,'b':b,'r':rr,'c':c,'ratio':s.factor(rr*rr/(a*b))}
out=[]
for name,ex in exprs.items():
 line=name+' = '+str(ex);print(line,flush=True);out.append(line)
 line=name+' series = '+str(s.series(ex,E,0,9));print(line,flush=True);out.append(line)
Path(__file__).with_name('triad_exact.txt').write_text('\n'.join(out)+'\n')
gap=s.factor(a*b-rr*rr)
num,den=s.fraction(gap)
print('gap factor',s.factor(gap),flush=True)
poly=s.Poly(num,E)
print('gap degree',poly.degree(),'all coefficients nonnegative',all(cc>=0 for cc in poly.all_coeffs()),flush=True)
Path(__file__).with_name('triad_gap.txt').write_text(str(gap)+'\n'+'nonnegative coefficients: '+str(all(cc>=0 for cc in poly.all_coeffs()))+'\n')
