import sympy as s
from fractions import Fraction as F
from pathlib import Path
import json
t=s.symbols('t',positive=True)
f=t*s.log(16*t/(t+3)**2)-(t-1)/2;g=t*s.log(t)-t+1;h=f-g/200
assert h.subs(t,1)==0 and s.diff(h,t).subs(t,1)==0
num=1791-1206*t-201*t*t
assert s.simplify(s.diff(h,t,2)-num/(200*t*(t+3)**2))==0
assert num.subs(t,1)>0 and num.subs(t,s.Rational(9,5))<0
exp_lower=1+F(3,5)+F(3,5)**2/2+F(3,5)**3/6
assert exp_lower==F(227,125)>F(9,5)
endpoint=F(2,1215)-F(7,5000)
assert endpoint>0
report={'status':'PASS','uniform_Din_margin':'1/200','kernel_coefficient':'99/200','source_specific_contraction':'199/400','scalar_endpoint_strict_lower':str(endpoint),'second_derivative_exact':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
