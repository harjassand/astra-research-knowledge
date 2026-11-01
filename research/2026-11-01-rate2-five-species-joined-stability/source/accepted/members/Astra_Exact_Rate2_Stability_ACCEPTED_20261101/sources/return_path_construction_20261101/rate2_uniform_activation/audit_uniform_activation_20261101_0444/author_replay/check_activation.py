"""Global exact identities and rational uniform envelopes, plus finite diagnostics."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json
import sympy as s
root=Path(__file__).resolve().parent
a,b,c,d,e=s.symbols('a b c d e');xx=(a,b,c,d,e)
z=lambda *ii:tuple(ii.count(i) for i in range(5))
A,B,C,D,E=range(5);two=z(A,A)
pairs=[(z(),z(A),1,1),(two,z(A,C),1,1),(two,z(A,D),1,1),(two,z(A,E),1,1),(z(A,E),z(C,D),1,2),(z(C,D),z(A,B),1,1)]
raw=[r for u,v,k,l in pairs for r in [(u,v,k),(v,u,l)]]
def rate(u,x):
 p=1
 for n,j in zip(x,u):
  for k in range(j):p*=n-k
 return p
def jump(x,u,v):return tuple(a+b-c for a,c,b in zip(x,u,v))
U=lambda x:x[E]-s.Rational(1,10)*x[A]
lu=sum(k*rate(u,xx)*(U(jump(xx,u,v))-U(xx)) for u,v,k in raw)
gamma=sum(k*rate(u,xx)*(U(jump(xx,u,v))-U(xx))**2 for u,v,k in raw)
lu_formula=s.Rational(17,10)*c*d+s.Rational(13,10)*a*a-s.Rational(6,5)*a-s.Rational(1,10)+a*(b/s.Integer(10)-(c+d)/10-2*e)
gamma_formula=(1+a)/s.Integer(100)+s.Rational(123,100)*a*(a-1)+a*(c+d)/100+a*b/100+s.Rational(163,100)*c*d+s.Rational(101,50)*a*e
assert s.expand(lu-lu_formula)==0
assert s.expand(gamma-gamma_formula)==0
assert all(abs(U(jump(xx,u,v))-U(xx))<=s.Rational(11,10) for u,v,k in raw)
# Integer A reserve: A=0,1 checked; for A>=2 the polynomial is increasing.
f=s.Rational(4,5)*a*a-s.Rational(6,5)*a+s.Rational(1,2)
assert f.subs(a,0)>=0 and f.subs(a,1)>=0
assert s.diff(f,a).subs(a,1)>0 and s.diff(f,a,2)>0
# Composition reserve expressed with R-bound slack t=b/100-R>=0.
t=s.symbols('t',nonnegative=True)
res=s.expand((lu_formula-(s.Rational(1,2)*(c*d+a*a)+s.Rational(2,25)*a*b-s.Rational(3,5))).subs(b,100*(c+d+e+t)))
# residual is positive via integer A reserve plus displayed nonnegative terms.
assert s.expand(res-f-s.Rational(6,5)*c*d-s.Rational(19,10)*a*(c+d)-2*a*t)==0
# Bracket upper estimate explicitly dominates positive monomial terms.
upper=s.Rational(1,100)+s.Rational(31,25)*a*a+s.Rational(163,100)*c*d+s.Rational(151,5000)*a*b
resg=s.expand((upper-gamma_formula).subs(b,100*(c+d+e+t)))
assert all(q>=0 for _,q in s.Poly(resg,a,c,d,e,t).terms())
P=s.Rational(1,2)*(c*d+a*a)+s.Rational(2,25)*a*b
assert all(q>=0 for _,q in s.Poly(s.expand(4*P+s.Rational(1,100)-upper),a,b,c,d,e).terms())
assert s.Rational(3,200)*16-s.Rational(601,10000)>=s.Rational(16,100)
# Uniform algebraic scale margins using y=N^(1/4)>=10^10 and m>=y^2/40000.
y=s.symbols('y')
assert 3*10**10>=33+2*10**10
assert 10**10>=1920000
assert Q(1,3)-Q(1,16)>Q(1,4)
assert Q(11,500)-Q(25,16)<-1
assert Q(1,4)-Q(2,3)<=-Q(1,3)
N=10**40;m=10**20//20000;T=10**12
assert N>=10**8*(m+1)**2
assert m*m>=Q(N,16*10**8)
assert 8*m+T<=10**20 and 8*m+T<=N//4
# Small and unbalanced diagnostics include absent A/CD and huge B rays.
checked=0
for aa,cc,dd,ee in product(range(5),repeat=4):
 for bb in [100*(cc+dd+ee),100*(cc+dd+ee)+1,10**8]:
  v={a:aa,b:bb,c:cc,d:dd,e:ee};M=aa+min(cc,dd)
  actual=lu_formula.subs(v);g=gamma_formula.subs(v)
  assert actual>=P.subs(v)-s.Rational(3,5)
  assert g<=4*actual+s.Rational(241,100)
  if M>=4:assert -actual/s.Integer(10)+g/100<=-s.Rational(M*M,100)
  checked+=1
result={'status':'PASS_AUTHOR_EXACT_IDENTITIES_AND_UNIFORM_ENVELOPES_NOT_INDEPENDENT_REVIEW','global_generator_polynomial_identities':2,'exact_jump_marks':12,'finite_diagnostics':checked,'all_actual_channels':12,'proof_sha256':hashlib.sha256((root/'UNIFORM_ACTIVATION_OR_REMOVAL.md').read_bytes()).hexdigest(),'LU':str(s.expand(lu)),'Gamma_U':str(s.expand(gamma))}
(root/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
