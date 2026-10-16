"""Exact own-derived polynomial/fraction identities. No numerical refutation."""
import json
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

c,d,a=sp.symbols('c d a',real=True)
b=1-a
p10=(1-c*c)*(a+b*d)**2
p01=(1-d*d)*(a+b*c)**2
p11=(b-a*a)*(1-c*c)*(1-d*d)
p00=a*b*(1-c-d-c*d)**2+(2*a-1)**2*c*c*d*d
identity=sp.expand(p10+p01+p11+p00-1)
assert identity==0
at=sp.factor((p10+p01).subs({a:sp.Rational(3,5),c:sp.Rational(4,5),d:sp.Rational(4,5)}))
q=F(369,625)
assert F(str(at))==F(9522,15625)
assert F(str(at))-q==F(297,15625)
result=dict(general_isometry_identity=str(identity),
            endpoint_abstract_probability=str(at),singleton_Q=str(q),
            abstract_endpoint_excess=str(F(str(at))-q),
            exact_strict_certificate=dict(old=str(F(18,25)**2),
                anchored=str(q*F(18,25)),desired=str(q*q),
                reduction=str(F(18,25)**2-q*F(18,25)),
                relative_reduction=str(1-q/F(18,25))),
            epistemic_status='exact algebraic identities; abstract map is not a legal comb counterexample')
(Path(__file__).resolve().parent/'exact_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
