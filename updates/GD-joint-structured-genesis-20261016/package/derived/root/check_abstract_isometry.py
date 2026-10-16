import json
from pathlib import Path
import sympy as s
c,d=s.symbols('c d',real=True)
norm=(1-c*c)*(3+2*d)**2/25+(1-d*d)*(3+2*c)**2/25+(1-c*c)*(1-d*d)/25+6*(1-c-d-c*d)**2/25+c*c*d*d/25
assert s.expand(norm-1)==0
odd=s.Rational(9,25)*(s.Rational(23,5))**2*2/25
bound=1-s.Rational(4,5)**4
assert odd==s.Rational(9522,15625)
assert odd-bound==s.Rational(297,15625)
r={'status':'PASS','norm_polynomial_identity':True,'terminal_odd':str(odd),'abstract_bound':str(bound),'excess':str(odd-bound),'scope':'Abstract analytic shortcut only; no legal causal counterexample.'}
Path('ABSTRACT_ISOMETRY_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS abstract identity and strict rational excess; causal embedding OPEN')
