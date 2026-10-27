from fractions import Fraction as F
from math import factorial
import sympy as s
from pathlib import Path
import json
x,y,z,c=s.symbols('x y z c',nonnegative=True)
S=x+y+z; Q=s.expand(c*c*(sum(t*t for t in (x,y,z))+sum((a+b)**2/4 for a,b in ((x,y),(x,z),(y,z)))-s.Rational(4,3)*sum(t*t for t in (x,y,z))))
assert s.simplify(Q-c*c*(3*S*S-x*x-y*y-z*z)/12)==0
assert s.simplify(Q-c*c*S*S/6)==c*c*(x*y+x*z+y*z)/6
exp_lower=sum((F(12**k,factorial(k)) for k in range(51)),F(0))
assert exp_lower>160000
margin=F(1,288)-F(13,5000)
assert margin==F(157,180000)>0
report={'status':'PASS','Q_identity':str(s.factor(Q)),'boundary_normalized_margin':'1/288','tube_trace_distance_radius':'1/20000','tube_margin':str(margin),'exp12_taylor_degree50_exceeds_160000':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
