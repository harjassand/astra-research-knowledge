import sympy as s,json
from pathlib import Path
v=s.symbols('v');D=2-2*v+s.Rational(9,8)*v*v;r=(1+v/8)/D
assert s.factor(1-r)==(v-1)*(9*v-8)/(9*v*v-16*v+16)
assert s.simplify(s.diff(r,v)*D**2+s.Rational(9,64)*(v*v+16*v-16))==0
assert s.simplify((r-s.Rational(1,2))*D-s.Rational(9,16)*v*(2-v))==0
cases=0
for initial in [s.Rational(1,1000),s.Rational(1,4),s.Rational(4,5),s.Rational(8,9)-s.Rational(1,10000)]:
 x=initial;C=s.Integer(1);kap=r.subs(v,initial)
 for j in range(7):
  den=D.subs(v,x);y=x*(1+x/8)/den;CC=4*C/den
  assert x/2<=y<x and y<=kap*x
  assert CC*y/(C*x)<= (1+x/8)/(1-x)**2
  x,C=y,CC;cases+=1
out={'exact_recurrence_cases':cases,'ratio_derivative_times_D_squared':'-9(v^2+16v-16)/64','ratio_half_bound':True,'ratio_less_than_one_for_v_below_8_over_9':True,'cost_product_bound':True,'target_boundary':'0<epsilon<v0; otherwise C0=1, as frozen erratum'};Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
