"""Independent exact perturbation, all28 value boxes and feasible original upper."""
import sympy as s,json,sys,math
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path('producer-workspace/quaternion_algebraic_completion_20261029');o=Path(__file__).parent
inp=json.loads((r/'input.json').read_text());cert=json.loads((r/'global_certificate_fast.json').read_text());x,y,z=s.symbols('x y z');lex=[s.Poly(s.sympify(v),x,y,z,domain=s.QQ).monic().as_expr() for v in json.loads((r/'shape.json').read_text())['lex_basis']];px=s.Poly(x-lex[0],z);py=s.Poly(y-lex[1],z)
exps=[tuple(e) for e in inp['exponents']];f=dict(zip(exps,map(F,inp['original'])));rho=dict(zip(exps,map(F,inp['perturbation'])));fp=dict(zip(exps,map(F,inp['perturbed'])));b=sum(abs(v) for v in rho.values());eps=F(inp['target_gap']);assert b==F(inp['objective_bias_bound'])<=eps/4 and all(fp[e]==f[e]+rho[e] for e in exps)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
 v=[u*w for u in a for w in b];return min(v),max(v)
def power(a,k):
 if k==0:return F(1),F(1)
 if k%2:return a[0]**k,a[1]**k
 return (F(0) if a[0]<=0<=a[1] else min(a[0]**k,a[1]**k),max(a[0]**k,a[1]**k))
def horner(p,a):
 v=F(0),F(0)
 for c in p.all_coeffs():c=F(int(c.p),int(c.q));v=add(mul(v,a),(c,c))
 return v
lows=[]
for row in cert['root_records']:
 zz=tuple(map(F,row['z_interval']));coords=[(F(1),F(1)),horner(px,zz),horner(py,zz),zz];num=F(0),F(0);den=F(0),F(0)
 for e,c in fp.items():
  if e[0]==0:continue
  es=list(e);es[0]-=1;term=c*e[0],c*e[0]
  for a,k in zip(coords,es):term=mul(term,power(a,k))
  num=add(num,term)
 for a in coords:den=add(den,power(a,2))
 den=4*den[0],4*den[1];assert den[0]>=4
 v=[a/b for a in num for b in den];interval=min(v),max(v);assert interval==tuple(map(F,row['perturbed_value_interval']));assert interval[1]-interval[0]<=eps/16;lows.append(interval[0])
 print('exact_value',row['index'],flush=True)
lo=min(lows)-b;assert lo==F(cert['original_global_lower'])
q=list(map(F,cert['rational_unit_quaternion']));assert sum(v*v for v in q)==1
up=sum(c*math.prod(v**e for v,e in zip(q,ee)) for ee,c in f.items());assert up==F(cert['original_rational_upper']);gap=up-lo;assert gap==F(cert['original_global_gap'])<=eps
# Separate known-optimum cross-check, not used in lower-bound computation.
assert lo<=0<=up
out={'all28_exact_value_intervals_match':True,'perturbation_budget_exact':str(b),'original_objective_lower':str(lo),'rational_unit_quaternion_upper_exact':True,'original_objective_upper':str(up),'gap_float':float(gap),'gap_below_target':True,'scope':'Exact interval/perturbation/feasible-point validation; globality requires separate completed ideal/root check.'}
(o/'value_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('complete',float(gap),flush=True)
