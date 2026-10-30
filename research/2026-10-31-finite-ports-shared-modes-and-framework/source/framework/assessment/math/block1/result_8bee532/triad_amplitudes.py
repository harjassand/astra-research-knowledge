import sympy as s
from sympy.polys.matrices import DomainMatrix
from pathlib import Path
import time,json
start=time.time()
e=s.symbols('e',real=True)
alpha=s.symbols('A B C',nonnegative=True)
x,y,u,v=s.symbols('x y u v',real=True); V=s.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;Cub=x*(u*u-v*v)+2*y*u*v;Q=s.Rational(3,16)*(r+t)
cs=s.symbols('c1 c2 c3',real=True)
R=[]
for p,q in [(1,0),(2,1),(3,1)]:
 k=p+s.I*e*q;z=s.I*s.conjugate(k)**4;w=s.I*k*s.conjugate(k)**3
 R.append(s.Matrix([s.re(z),s.im(z),s.re(w),s.im(w)]).applyfunc(s.expand))
G=sum((R[j]*cs[j] for j in range(3)),s.zeros(4,1)); subs=dict(zip(V,G))
def avg(poly):
 ans=0
 for powers,coeff in s.Poly(s.expand(poly),*cs).terms():
  if sum(powers)==0:val=1
  elif sorted(powers)==[0,0,2]: val=alpha[powers.index(2)]/2
  elif powers==(1,1,1):val=s.Rational(1,4)
  elif sorted(powers)==[0,0,4]:val=3*alpha[powers.index(4)]**2/8
  elif sorted(powers)==[0,2,2]:
   ids=[j for j in range(3) if powers[j]==2];val=alpha[ids[0]]*alpha[ids[1]]/4
  else:val=0
  ans+=coeff*val
 return s.expand(ans)
def get(poly):return avg(poly.subs(subs,simultaneous=True))
H=s.hessian(F,V).applyfunc(get); vv=s.Matrix([s.diff(F,z) for z in V]).applyfunc(get);ww=s.Matrix([s.diff(Cub,z) for z in V]).applyfunc(get)
f=get(F);cc=get(Cub);q=get(Q);prod=s.prod(alpha)
M=H.row_join(vv).row_join(ww)
M=M.col_join((prod*vv.T).row_join(s.Matrix([[2*f,prod*cc]])))
M=M.col_join(ww.T.row_join(s.Matrix([[cc,2*q]])))
print('matrix ready',time.time()-start,flush=True)
dm=DomainMatrix.from_Matrix(M).convert_to(s.QQ.poly_ring(e,*alpha))
determinant=dm.det().as_expr()
print('det done',time.time()-start,flush=True)
poly=s.Poly(determinant,e,*alpha)
neg=[(powers,str(co)) for powers,co in poly.terms() if co<0]
print('monomials',len(poly.terms()),'negative',len(neg),'degrees',poly.degree_list(),flush=True)
out={'elapsed':time.time()-start,'monomials':len(poly.terms()),'negative_terms':neg,'degree_list':poly.degree_list(),'terms':[(powers,str(co)) for powers,co in poly.terms()]}
Path(__file__).with_name('triad_amplitudes_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
Path(__file__).with_name('triad_amplitudes_det.txt').write_text(str(s.factor(determinant))+'\n')
assert not neg
assert all(power[0]%2==0 for power,co in poly.terms())
print('all coefficients nonnegative',not neg,flush=True)
