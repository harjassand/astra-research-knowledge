"""Independent exact rational interval replay of all stationary values and feasible upper."""
import json,math,sys,sympy as s
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0)
r=Path('producer-workspace/quaternion_oracle_controller_20261029');o=Path(__file__).parent
j=json.loads((r/'critical_chart_result.json').read_text());v=json.loads((r/'critical_global_certificate.json').read_text());b=json.loads((r/'oracle_one_axis_edge0.json').read_text());N=b['probe_calls'];x,y,z=s.symbols('x y z');lex=[s.Poly(s.sympify(t),x,y,z).monic().as_expr() for t in j['lex_basis']]
px=s.Poly(x-lex[0],z);py=s.Poly(y-lex[1],z)
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def times(a,b):
 c=[u*v for u in a for v in b];return min(c),max(c)
def power(a,n):
 if n==0:return F(1),F(1)
 if n%2:return a[0]**n,a[1]**n
 return (F(0) if a[0]<=0<=a[1] else min(a[0]**n,a[1]**n),max(a[0]**n,a[1]**n))
def horner(p,a):
 result=F(0),F(0)
 for c in p.all_coeffs():c=F(int(c.p),int(c.q));result=plus(times(result,a),(c,c))
 return result
rows=[]
for row in v['critical_intervals']:
 zz=tuple(map(F,row['z_interval']));xx=horner(px,zz);yy=horner(py,zz)
 assert xx==tuple(map(F,row['x_interval'])) and yy==tuple(map(F,row['y_interval']))
 coords=[(F(1),F(1)),xx,yy,zz];num=F(0),F(0);norm=F(0),F(0)
 for t in b['quartic_coefficients']:
  c=F(t['coefficient'],4*N);term=c,c
  for a,e in zip(coords,t['exponents']):term=times(term,power(a,e))
  num=plus(num,term)
 for a in coords:norm=plus(norm,power(a,2))
 den=power(norm,2);assert den[0]>=1
 vals=[a/b for a in num for b in den];bounds=min(vals),max(vals);assert bounds==tuple(map(F,row['objective_interval']))
 rows.append(bounds)
assert min(a for a,b in rows)==F(v['global_lower'])
q=list(map(F,v['rational_quaternion']));assert sum(a*a for a in q)==1
value=sum(F(t['coefficient'],4*N)*math.prod(a**e for a,e in zip(q,t['exponents'])) for t in b['quartic_coefficients']);assert value==F(v['rational_upper'])
gap=value-F(v['global_lower']);assert 0<=gap<F(2,10**19)
(o/'value_interval_checks.json').write_text(json.dumps({'all_four_rational_boxes_match':True,'strict_positive_denominators':True,'unit_quaternion_exact':True,'rational_feasible_upper_exact':True,'global_gap_float':float(gap),'scope':'Interval arithmetic and feasible upper independently replayed; globality depends separately on ideal/root-completeness check.'},indent=2)+'\n');print(float(gap))
