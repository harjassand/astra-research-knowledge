"""Author diagnostics only. The candidate analytic proof, not these examples, gives the limit."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parent
EXPECTED='7b21a27ccb6cfd0b73f987ba4683a9bda7e163b556dfd8cc2a4ea525b2e50e78'
assert hashlib.sha256((ROOT/'UNIFORM_ANGULAR_UNIVERSALITY_CANDIDATE.md').read_bytes()).hexdigest()==EXPECTED
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
y,k=s.symbols('y k',real=True,positive=True)
v=1+k*(1-y*y)**2;vs=1+k;d=k/vs;c=2*d
ck(s.simplify(v-(1+s.Rational(9,4)*k*(y-1)**2)-k*(y-1)**2*((y+1)**2-s.Rational(9,4)))==0)
u=1-v/vs
ck(s.simplify(u-s.Rational(7,4)*d*y*y-d*y*y*(s.Rational(1,4)-y*y))==0)
ck(s.simplify(u.subs(y,s.Rational(1,2))-s.Rational(7,16)*d)==0)
for fun,A in [(s.log(v/vs),d-c*c/2),(s.log(vs/(2*vs-v)),d+c*c/2)]:
 poly=s.series(fun,y,0,6).removeO().expand()
 ck(s.simplify(poly.coeff(y,2)+c)==0)
 ck(s.simplify(poly.coeff(y,4)-A)==0)
ck(s.simplify(3*((d+c*c/2)-(d-c*c/2))/(4*c*c))==s.Rational(3,4))
ck(s.simplify((s.sqrt(s.pi)/(2*s.sqrt(k)))*s.sqrt(s.pi/c)-s.pi*s.sqrt(1+k)/(2*s.sqrt(2)*k))==0)
# Exact sampled hypotheses/inequalities supplement, rather than replace, proofs.
ks=[F(1,100),F(1,7),F(1),F(3),F(100)]
for kap in ks:
 star=1+kap;ab=1+9*kap/16;G1=star*star/(2*star-1);Gb=star*star/(2*star-ab)
 ck(1<ab<star and 1<G1<Gb<star)
 for alpha in [4,5,8,16,64,128,1024]:
  delta=F(1,alpha);f=lambda x:1+kap*(1-x*x)**2
  ck(f(1+delta)<=ab)
  for i in range(33):
   z=F(i,64);q=kap/star*(2*z*z-z**4)
   ck(q>=7*kap*z*z/(4*star))
   ck(0<=q<=7*kap/(16*star)<F(7,16))
   a=F(i,8)+F(1,2)
   ck(f(a)>=1+F(9,4)*kap*(a-1)**2)
# Floating quadrature is labeled diagnostic only, no interval certification.
mp.mp.dps=60
numeric=[]
for kap in ['0.1','1','10']:
 K=mp.mpf(kap);V=1+K;cr=2*K/V
 for n in [16,64,256,1024]:
  root=mp.sqrt(n);cut=root/2
  def u(x):
   y=x/root;return K/V*(2*y*y-y**4)
  split=sorted(set([mp.mpf(0),min(cut,mp.mpf(1)),min(cut,mp.mpf(4)),cut]))
  r=2*mp.quad(lambda x:mp.power(1-u(x),n),split)
  p=2*mp.quad(lambda x:mp.power(1+u(x),-n),split)
  ck(p>=r>0)
  numeric.append({'kappa':kap,'alpha':n,'sqrt_alpha_R_over_vstar_power':mp.nstr(r,20),
   'limit':mp.nstr(mp.sqrt(mp.pi/cr),20),'alpha_times_witness_ratio_minus_one':mp.nstr(n*(p/r-1),20),
   'scope':'NONRIGOROUS floating quadrature diagnostic, not a finite certificate'})
report={'status':'AUTHOR DIAGNOSTICS PASS; independent theorem review pending','source_sha256':EXPECTED,'exact_symbolic_and_rational_assertions':checks-len(numeric),'floating_sanity_assertions':len(numeric),'total_assertions':checks,'numerical_diagnostics':numeric,
 'not_established_by_tests':['uniform theorem','finite asymptotic remainder constant','physical model acquisition','new receiver acceptance']}
(ROOT/'universality_candidate_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
