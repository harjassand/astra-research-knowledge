"""Symbolic/interval diagnostic supporting the analytic strict lower bound."""
import sympy as s
from pathlib import Path
import json
u,t=s.symbols('u t',positive=True)
K=(2*t*t-1)/(2*s.sqrt(2)*t*t*(t+1))
derivative=s.factor(s.diff(K,t))
assert s.simplify(derivative-s.sqrt(2)*(-2*t**3+3*t+2)/(4*t**3*(t+1)**2))==0
intervals=s.Poly(2*t**3-3*t-2,t).intervals(eps=s.Rational(1,10**15))
(tlo,thi),mult=[z for z in intervals if z[0][0]>1][0]
assert mult==1
# Exact rational enclosure of sqrt(2).
slo=s.Rational(1414213562373095048,10**18)
shi=s.Rational(1414213562373095049,10**18)
assert slo*slo<2<shi*shi
# Independent factor enclosures are deliberately conservative.
Llo=4*(slo-1)*tlo*tlo*(tlo+1)/(2*thi*thi-1)
Lhi=4*(shi-1)*thi*thi*(thi+1)/(2*tlo*tlo-1)
assert Llo>s.Rational(266,100)
assert Lhi<s.Rational(267,100)
tstar=s.nroots(2*t**3-3*t-2,maxsteps=100)[0]
# Use the real algebraic expression, not the ordering of numerical roots.
tstar=s.real_root(s.Rational(1,2)+1/(2*s.sqrt(2)),3)+s.real_root(s.Rational(1,2)-1/(2*s.sqrt(2)),3)
L=4*(s.sqrt(2)-1)*tstar*tstar*(tstar+1)/(2*tstar*tstar-1)
out={'status':'symbolic derivative and exact rational enclosure passed','root_equation':'2t^3-3t-2=0, unique t>1','t_interval':[str(tlo),str(thi)],'lower_bound_formula':'4*(sqrt(2)-1)*t^2*(t+1)/(2*t^2-1)','lower_bound_decimal':str(s.N(L,25)),'exact_lower_enclosure':str(Llo),'exact_upper_enclosure':str(Lhi),'lower_enclosure_decimal':str(s.N(Llo,20)),'upper_enclosure_decimal':str(s.N(Lhi,20)),'scope':'diagnostic for the analytic proof in PROOF.md; the global inequality is proved there, not inferred from sampling'}
Path(__file__).with_name('lower_bound_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','lower_bound_decimal','lower_enclosure_decimal','upper_enclosure_decimal']},indent=2))
