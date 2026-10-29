import sympy as s,json,sys,hashlib
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path('producer-workspace/quartic_value_polynomial_20261029');out=Path(__file__).parent
inp=json.loads((r/'received/input.json').read_text());c=json.loads((r/'candidate_value_polynomial.json').read_text());a=json.loads((r/'root_candidate_certificate.json').read_text());x=s.symbols('x');cs=list(map(int,c['integer_coefficients_low_to_high']));p=s.Poly.from_list(cs[::-1],x)
assert p.degree()==40 and s.gcd(p,p.diff()).degree()==0
iv=s.intervals(p,eps=s.Rational(1,2**45),fast=True);assert len(iv)==28 and all(m==1 for _,m in iv)
assert [[str(l),str(u)] for (l,u),_ in iv]==a['all_real_value_intervals']
q=list(map(F,a['ordinary_candidate_quaternion']));assert sum(t*t for t in q)==1
v=sum(F(c)*__import__('math').prod(t**k for t,k in zip(q,e)) for c,e in zip(inp['original'],inp['exponents']))
b=sum(abs(F(t)-F(u)) for t,u in zip(inp['perturbed'],inp['original']));assert b==F(inp['objective_bias_bound'])
lower=F(str(iv[0][0][0]))-b;assert v==F(a['original_exact_candidate_upper']);assert lower==F(a['original_lower_if_value_polynomial_verified']);assert v-lower==F(a['original_gap_if_verified']);assert v-lower<F(inp['target_gap'])
res={'degree':40,'simple_real_roots':28,'all_intervals_reproduced':True,'unit_quaternion_exact':True,'exact_original_upper':str(v),'exact_original_lower':str(lower),'gap':str(v-lower),'gap_float':float(v-lower)}
(out/'value_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
