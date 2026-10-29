"""Author diagnostic, uses root's separately reviewed physical/transducer formulas.
Compare discrete purification orderings at equal final one-Choi infidelity.
No PBT or finite-cap cost included.
"""
import json,sympy as s
from decimal import Decimal,getcontext
from pathlib import Path
getcontext().prec=60
D=Decimal
root=Path('producer-workspace/robust_frame_program_boundary_20261029')
g=json.loads((root/'check_growth_pollution.json').read_text());t=json.loads((root/'check_noisy_transducer.json').read_text());x,v=s.symbols('x v')
def dec(expr):return D(str(s.N(expr,65)))
def level(e,c,d):
 den=2-2*e+D(d)*e*e/(d-1)
 return e*(1+e/(d-1))/den,4*c/den
rows=[]
for eta in [s.Rational(1,100),s.Rational(1,10),s.Rational(1,2)]:
 xx=eta/(8+eta);e0=dec(s.sympify(g['infidelity']).subs(x,xx));base=dec(s.sympify(g['expected_minus_records']).subs(x,xx)/((8+eta)/18))
 for target in [D('.01'),D('.0001'),D('.000001')]:
  alternatives=[];e=e0;cost=base
  for j in range(25):
   p=(405*e*e-720*e+512)/864
   w=3*e*(62-9*e)/(405*e*e-720*e+512)
   c=2*cost/p;k=0
   while w>target:
    w,c=level(w,c,4);k+=1
   alternatives.append(dict(rotation_levels=j,quaternion_levels=k,final_error=str(w),expected_calls=str(c)))
   e,cost=level(e,cost,9)
  best=min(alternatives,key=lambda r:D(r['expected_calls']))
  rows.append(dict(eta=str(eta),target=str(target),best=best,transduce_first=alternatives[0],alternatives=alternatives))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='alternatives'} for r in rows],indent=2))
