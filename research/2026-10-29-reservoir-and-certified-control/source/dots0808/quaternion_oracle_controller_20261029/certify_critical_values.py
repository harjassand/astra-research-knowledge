"""Exact interval evaluation of every real root of the executed shape basis."""
import sympy as s,json,time,sys,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from quartic_sos_oracle import bank_polynomial,rational_candidate,exact_eval
sys.set_int_max_str_digits(0)
root=Path(__file__).parent;j=json.load(open(root/'critical_chart_result.json'));iso=json.load(open(root/'critical_chart_isolation.json'));missing=json.load(open(root/'missing_chart_result.json'));assert missing['no_missing_stationary_point']
x,y,z=s.symbols('x y z');basis=[s.sympify(v) for v in j['lex_basis']];uni=s.Poly(basis[-1],z)
px=s.Poly(-basis[0].subs(x,0)/s.Poly(basis[0],x,y,z).coeff_monomial(x),z);py=s.Poly(-basis[1].subs(y,0)/s.Poly(basis[1],x,y,z).coeff_monomial(y),z)
assert s.degree(basis[0],x)==1 and s.degree(basis[0],y)==0 and s.degree(basis[1],y)==1 and s.degree(basis[1],x)==0
assert s.gcd(uni,uni.diff()).degree()==0
bank=json.load(open(root/'bank_one_axis.json'));raw=bank_polynomial(bank,0);f={e:F(v,4*bank['probe_calls']) for e,v in raw.items()}
def frac(q):return F(int(q.p),int(q.q))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):
 vals=[v*w for v in a for w in b];return min(vals),max(vals)
def power(a,k):
 if k==0:return F(1),F(1)
 if k%2:return a[0]**k,a[1]**k
 return (F(0) if a[0]<=0<=a[1] else min(a[0]**k,a[1]**k),max(a[0]**k,a[1]**k))
def horner(poly,interval):
 v=(F(0),F(0))
 for co in poly.all_coeffs():v=add(mul(v,interval),(frac(co),frac(co)))
 return v
def obj(vs):
 num=(F(0),F(0))
 for e,c in f.items():
  val=(c,c)
  for v,k in zip(vs,e):val=mul(val,power(v,k))
  num=add(num,val)
 den=(F(0),F(0))
 for v in vs:den=add(den,power(v,2))
 den=power(den,2);assert den[0]>0
 vals=[v/w for v in num for w in den];return min(vals),max(vals)
start=time.time();rows=[];best=None;bestq=None
for row in iso['real_intervals']:
 a,b=s.Rational(row['a']),s.Rational(row['b']);a,b=s.polys.polytools.refine_root(uni,a,b,eps=s.Rational(1,10**60));zz=(frac(a),frac(b));xx=horner(px,zz);yy=horner(py,zz);lo,up=obj([(F(1),F(1)),xx,yy,zz]);mid=(a+b)/2
 vv=np.array([1,float(px.eval(mid)),float(py.eval(mid)),float(mid)]);qr=rational_candidate(vv,bits=30);value=exact_eval(f,qr)
 if best is None or value<best:best,bestq=value,qr
 rows.append(dict(z_interval=[str(a),str(b)],x_interval=[str(t) for t in xx],y_interval=[str(t) for t in yy],objective_interval=[str(lo),str(up)],objective_float=[float(lo),float(up)]))
minimum=min(F(r['objective_interval'][0]) for r in rows);assert best>=minimum
out=dict(real_stationary_rays=len(rows),root_polynomial_degree=uni.degree(),root_polynomial_squarefree=True,all_missing_chart_complex_points_excluded=True,critical_intervals=rows,global_lower=str(minimum),rational_upper=str(best),rational_quaternion=[str(v) for v in bestq],global_gap=float(best-minimum),seconds=time.time()-start,scope='Executed exact critical-chart root isolation and objective intervals; globality relies on exact Groebner shape equivalence and missing-chart basis1. Receiving independent algebraic review pending.')
(root/'critical_global_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['critical_intervals','global_lower','rational_upper','rational_quaternion']},indent=2))
