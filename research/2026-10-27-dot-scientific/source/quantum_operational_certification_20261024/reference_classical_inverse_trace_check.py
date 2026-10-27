import sympy as s
from pathlib import Path
import json
p,q,r=s.symbols('p q r',real=True);e2=3-p;e3=1-p+q
F=3*e2**2+4*e2*e3-36*e3-3*e3**2
assert s.expand(F)==4*p*p+2*p*q+8*p-3*q*q-30*q
assert s.simplify(F.subs({p:3*r*r,q:2*r**3})-12*r*r*(1-r)**3*(r+2))==0
report={'status':'PASS','cleared_numerator_exact':True,'extremal_factorization':'12r^2(1-r)^3(r+2)','scope':'scalar/reference-classical pointwise inverse trace, no upper cap'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
