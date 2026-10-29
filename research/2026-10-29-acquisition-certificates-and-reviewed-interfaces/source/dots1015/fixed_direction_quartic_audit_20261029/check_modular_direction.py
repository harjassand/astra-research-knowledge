"""Independent low-to-high modular polynomial arithmetic for fixed good direction."""
import json,sympy as s,math,sys
sys.set_int_max_str_digits(0)
from pathlib import Path
r=Path('producer-workspace/quaternion_algebraic_completion_20261029');o=Path(__file__).parent;p=1000000007
assert all(p%d for d in range(2,math.isqrt(p)+1))
x,y,z=s.symbols('x y z');sh=json.loads((r/'shape.json').read_text());b=[s.Poly(s.sympify(v),x,y,z,domain=s.QQ).monic().as_expr() for v in sh['lex_basis']]
def rat(c):
 c=s.Rational(c);a,d=int(c.p),int(c.q);assert d%p;return a*pow(d,-1,p)%p
def trim(a):
 a=[v%p for v in a]
 while a and a[-1]==0:a.pop()
 return a
def poly(expr):
 a=s.Poly(expr,z,domain=s.QQ);return trim([rat(a.nth(i)) for i in range(a.degree()+1)])
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([c*v for v in a])
def mul(a,b):
 if not a or not b:return []
 v=[0]*(len(a)+len(b)-1)
 for i,c in enumerate(a):
  for j,d in enumerate(b):v[i+j]=(v[i+j]+c*d)%p
 return trim(v)
def div(a,b):
 a=trim(a);b=trim(b);assert b;out=[0]*max(0,len(a)-len(b)+1);iv=pow(b[-1],-1,p)
 while len(a)>=len(b):
  k=len(a)-len(b);c=a[-1]*iv%p;out[k]=c
  a=add(a,[0]*k+scale(b,-c))
 return trim(out),a
def gcdex(a,b):
 u,v=[1],[];u2,v2=[],[1]
 while b:
  q,t=div(a,b);a,b=b,t;u,u2=u2,add(u,scale(mul(q,u2),-1));v,v2=v2,add(v,scale(mul(q,v2),-1))
 iv=pow(a[-1],-1,p);return scale(a,iv),scale(u,iv),scale(v,iv)
H=poly(b[2]);assert len(H)==41;g,_,_=gcdex(H,[i*H[i]%p for i in range(1,len(H))]);assert g==[1]
def prod(a,b):return div(mul(a,b),H)[1]
def power(a,n):
 v=[1]
 for _ in range(n):v=prod(v,a)
 return v
P=poly(x-b[0]);Q=poly(y-b[1]);vars=[[1],P,Q,[0,1]];norm=[1]
for a in vars[1:]:norm=add(norm,prod(a,a))
norm=div(norm,H)[1];g,inv,_=gcdex(norm,H);assert g==[1] and prod(norm,inv)==[1]
inp=json.loads((r/'input.json').read_text());num=[]
for e,c in zip(inp['exponents'],inp['perturbed']):
 if e[0]==0:continue
 ee=list(e);ee[0]-=1;term=[rat(s.Rational(c)*e[0])]
 for a,k in zip(vars,ee):term=prod(term,power(a,k))
 num=add(num,term)
lam=scale(prod(num,inv),pow(4,-1,p));cols=[];v=[1]
for _ in range(40):cols.append(v+[0]*(40-len(v)));v=prod(v,lam)
A=s.Matrix(40,40,lambda i,j:cols[j][i]);from sympy.polys.matrices import DomainMatrix
D=DomainMatrix.from_Matrix(A).convert_to(s.GF(p));det=int(D.det())%p;assert det==438433815
ref=json.loads((r/'fixed_good_direction_modp.json').read_text());assert lam+[0]*(40-len(lam))==ref['lambda_coefficients_low_to_high']
report={'prime_certified_by_exhaustive_trial_division':p,'degree40_squarefree':True,'norm_inverse_exact_modp':True,'objective_polynomial_matches_author':True,'krylov_determinant_modp':det,'independent_arithmetic':'own polynomial convolution/division/extended Euclid; finite-field DomainMatrix determinant','scope':'Modular nonzero witness lifting through exact characteristic-zero shape and chart dependencies'}
(o/'modular_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
