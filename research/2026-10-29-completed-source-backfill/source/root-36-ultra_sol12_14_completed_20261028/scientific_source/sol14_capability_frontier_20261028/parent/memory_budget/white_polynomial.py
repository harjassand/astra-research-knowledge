"""Exact derivative polynomial for the constructed matrix-weight white ray."""
from pathlib import Path
import json,time,sys
sys.set_int_max_str_digits(0)
START=time.perf_counter()
import sympy as s
HERE=Path(__file__).resolve().parent
source=json.loads((HERE/'SOURCE.json').read_text())
M=s.Matrix([[s.Rational(z[0])+s.sqrt(-3)*s.Rational(z[1])for z in row]for row in source['M']])
x=s.symbols('x')
char=M.charpoly(x).as_poly()
assert all(c.is_Rational for c in char.all_coeffs())
P=s.Poly(s.expand(char.as_expr().subs(x,-3*x)/3**6),x,domain=s.QQ)
assert P.LC()==1
num=s.Poly(x**8*(x+500)**2*s.prod(x+j for j in range(1,9))*(x+s.Rational(518,9))**18,x)
R=num-P**6
coeff=R.all_coeffs()
print(json.dumps({'degree':R.degree(),'positive_coefficients':sum(int(bool(c>0)) for c in coeff),'negative_coefficients':sum(int(bool(c<0)) for c in coeff),'M_char_coefficients':list(map(str,char.all_coeffs())),'seconds':time.perf_counter()-START}),flush=True)
count=R.count_roots(0,s.oo)
print(json.dumps({'positive_root_count':int(count),'seconds':time.perf_counter()-START}),flush=True)
# A global Sturm count plus two sign brackets avoids negative-root work.
coeffq=[s.Rational(c)for c in coeff]
def value(t):
 z=coeffq[0]
 for c in coeffq[1:]:z=z*t+c
 return z
grid=[s.Rational(0)]+[s.Rational(2)**j for j in range(-40,41)]
brackets=[(lo,hi)for lo,hi in zip(grid,grid[1:])if value(lo)*value(hi)<0]
assert len(brackets)==2 and int(count)==2
roots=[]
for lo,hi in brackets:
 sign=value(lo)>0
 while hi-lo>s.Rational(1,2**40):
  mid=(lo+hi)/2;v=value(mid)
  assert v!=0
  if bool(v>0)==bool(sign):lo=mid
  else:hi=mid
 roots.append(((lo,hi),1))
out={'status':'EXACT_DERIVATIVE_POLYNOMIAL','M_char_coefficients':list(map(str,char.all_coeffs())),
 'P_coefficients':list(map(str,P.all_coeffs())),'R_coefficients':list(map(str,coeff)),
 'positive_root_count':int(count),'positive_critical_intervals':[[list(map(str,iv)),m]for iv,m in roots],
 'seconds_including_sympy':time.perf_counter()-START}
(HERE/'WHITE_POLYNOMIAL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'root_intervals':out['positive_critical_intervals'],'seconds':out['seconds_including_sympy']},indent=2))
