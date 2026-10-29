"""Independent exact verifier. Does not import or invoke certificate finder."""
import json,itertools,math
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
root=Path(__file__).parent;w,x,y,z=qs=sp.symbols('w x y z');norm=sum(t*t for t in qs)
R=sp.Matrix([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])
z2=[qs[i]*qs[j] for i,j in itertools.combinations_with_replacement(range(4),2)]
reports=[]
for path in sorted(root.glob('oracle_*_edge*.json')):
 c=json.load(open(path));bank=json.load(open(root/Path(c['source']).name));i=c['edge'];n=bank['probe_calls'];scale=c['scale']
 expr=3*n*norm**2
 for a,b in itertools.product(range(3),repeat=2):
  expr-=9*bank['B'][i][a][b]*norm*R[a,b]
  for cc,d in itertools.product(range(3),repeat=2):expr-=81*bank['C'][i][a][b][cc][d]*R[a,b]*R[cc,d]
 poly=sp.Poly(expr,*qs)
 for term in c['quartic_coefficients']:assert poly.coeff_monomial(tuple(term['exponents']))==term['coefficient']
 qr=[sp.Rational(v) for v in c['rational_quaternion']];assert sum(v*v for v in qr)==1
 RR=R.subs(dict(zip(qs,qr)));assert RR.T*RR==sp.eye(3) and RR.det()==1
 upper=sp.Rational(c['rational_upper']);lower=sp.Rational(c['rational_lower']);assert expr.subs(dict(zip(qs,qr)))/scale==upper
 G=sp.Matrix([[sp.Rational(v) for v in row] for row in c['rational_gram']]);assert G==G.T
 assert sp.Poly(expr/scale-lower*norm**2-(sp.Matrix(z2).T*G*sp.Matrix(z2))[0],*qs).is_zero
 LL,DD=G.LDLdecomposition(hermitian=False);assert LL*DD*LL.T==G and all(v>0 for v in DD.diagonal())
 assert upper>=lower
 reports.append(dict(file=path.name,exact_SO3=True,exact_35_coefficient_identity=True,exact_positive_LDL=True,certified_mean_loss_gap=float((upper-lower)*scale/(4*n))))
print(json.dumps(reports,indent=2));(root/'independent_certificate_checks.json').write_text(json.dumps(reports,indent=2)+'\n')
