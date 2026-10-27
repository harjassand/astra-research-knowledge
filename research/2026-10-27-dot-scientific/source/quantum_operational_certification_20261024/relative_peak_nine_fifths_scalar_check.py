import sympy as s
from fractions import Fraction as F
from pathlib import Path
import json
t=s.symbols('t',positive=True)
f=t*s.log(16*t/(t+3)**2)-(t-1)/2
assert f.subs(t,1)==0 and s.diff(f,t).subs(t,1)==0
assert s.simplify(s.diff(f,t,2)+(t*t+6*t-9)/(t*(t+3)**2))==0
z=F(1,9);lo=2*(z+z**3/3)
assert F(9,5)*lo-F(2,5)==F(2,1215)
assert s.simplify(s.diff(s.log(16*t/(t+3)**2),t)-(3-t)/(t*(t+3)))==0
report={'status':'PASS','scalar_endpoint_strict_lower':'2/1215','second_derivative_single_turn_exact':True,'Stieltjes_log_primitive_sign':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
