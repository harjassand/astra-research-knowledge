"""Independent exact verifier for actual-bank perturbation query certificates."""
from pathlib import Path
import json,itertools
import sympy as s
root=Path(__file__).parent;q=s.symbols('q0:4');norm=sum(x*x for x in q);z=s.Matrix([q[i]*q[j] for i,j in itertools.combinations_with_replacement(range(4),2)]);rows=[]
for path in sorted(root.glob('perturbed_*_[0-9]_[0-9].json')):
 j=json.load(open(path));f=sum(s.Rational(c)*s.prod(q[i]**e[i] for i in range(4)) for e,c in zip(j['exponents'],j['query_coefficients']))/j['scale']
 G=s.Matrix([[s.Rational(x) for x in row] for row in j['gram']]);lo=s.Rational(j['lower']);up=s.Rational(j['upper']);qq=[s.Rational(x) for x in j['quaternion']]
 assert sum(x*x for x in qq)==1 and f.subs(dict(zip(q,qq)))==up
 assert s.Poly(f-lo*norm**2-(z.T*G*z)[0],*q).is_zero
 L,D=G.LDLdecomposition(hermitian=False);assert L*D*L.T==G and all(x>0 for x in D.diagonal())
 gap=(up-lo)*j['scale'];assert gap==s.Rational(j['actual_gap']) and bool(gap<=s.Rational(j['requested_gap']))==j['success']
 rows.append(dict(file=path.name,exact_certificate_pass=True,requested_gap_met=j['success']))
(root/'independent_perturbed_checks.json').write_text(json.dumps(rows,indent=2)+'\n');print('Exact verified',len(rows),'perturbed query certificates')
