import sympy as s,json
from pathlib import Path
z=json.loads((Path(__file__).parent/'check_growth_pollution.json').read_text());x=s.symbols('x',positive=True);eta,t=s.symbols('eta t',nonnegative=True)
f=s.sympify(z['infidelity'],locals={'x':x});g=s.factor(f.subs(x,eta/(8+eta)));der=s.factor(s.diff(g,eta));num,den=s.fraction(der);poly=s.Poly(num,eta);n=poly.degree();bp=s.Poly(s.cancel((1+t)**n*num.subs(eta,t/(1+t))),t);co=bp.all_coeffs()
assert all(c>0 for c in co);assert den.subs(eta,0)>0
out=dict(physical_infidelity=str(g),derivative=str(der),positive_bernstein_numerator_coefficients=[str(c) for c in co],degree=n,endpoints=[str(g.subs(eta,a)) for a in [0,1]],scope='Exact monotonicity of eventual growth infidelity on physical contamination interval [0,1]; denominator factor positivity separately inspected')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
