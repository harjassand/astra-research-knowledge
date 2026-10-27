"""Independent exact algebra audit of the Bernstein certificate implementation.
Uses the 4 by 4 Schur determinant directly, not the reduced numerator formula.
Also proves Bernstein elevation/product identities on a complete basis through degree4.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import importlib.util, contextlib,io,json
import sympy as S
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('cert',ROOT/'certify_background_bernstein.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
x,a=S.symbols('x a')
def rational(q):return S.Rational(q.numerator,q.denominator)
def expr(P):
 return S.expand(sum(rational(c.l)*comb(P.n,i)*x**i*(1-x)**(P.n-i) for i,c in enumerate(P.c)))
def basis(n,i):return mod.P([int(j==i) for j in range(n+1)])
basis_checks=0
for n in range(5):
 for i in range(n+1):
  p=basis(n,i)
  for target in range(n,5):
   assert S.expand(expr(p)-expr(p.elevate(target)))==0;basis_checks+=1
  for m in range(5-n):
   for j in range(m+1):
    q=basis(m,j);assert S.expand(expr(p*q)-expr(p)*expr(q))==0;basis_checks+=1
# Use exact binary64 lower endpoints as one algebraic input tuple. This is not a positivity proof.
raw=json.load(open(ROOT/'nu1_moments_N2048.json'));mom=raw['moments']
point={name:{'lower_hex':v['lower_hex'],'upper_hex':v['lower_hex']} for name,v in mom.items()}
pf=ROOT/'independent_point_algebra_input.json';pf.write_text(json.dumps({'moments':point},indent=2)+'\n')
with contextlib.redirect_stdout(io.StringIO()): ans=mod.run(str(pf),F(1))
f={name:S.Rational(F.from_float(float.fromhex(v['lower_hex']))) for name,v in mom.items()}
h0=S.Rational(99,200);sig=f['s'];m=3*h0/2-25*sig/4;c=S.Matrix([15*sig/4,h0-5*sig]);M=S.Matrix([[h0/2-9*sig/4,3*sig],[3*sig,h0-4*sig]])
alpha=2*(a+1)*(3*a+1);beta=12*(1-a*a);gamma=2*(a-1)*(3*a-1)
k=alpha*(f['A4']-S.Rational(81,22400))+beta*(f['B4']-S.Rational(51,22400))+gamma*(f['C4']-S.Rational(57,22400))-1
Q=S.zeros(3);Q[0,0]=(6*alpha+beta)*m;Q[0,1:3]=(2*beta*c).T;Q[1:3,0]=2*beta*c;Q[1:3,1:3]=m*(beta+2*gamma)*S.eye(2)+4*gamma*M
ell=S.Matrix([4*alpha*f['m1']+2*beta*f['m2'],2*beta*f['m3_1']+4*gamma*f['m4_1'],2*beta*f['m3_2']+4*gamma*f['m4_2']])
K=Q.row_join(ell/2).col_join((ell/2).T.row_join(S.Matrix([[k]])))
P=S.Poly(S.cancel(m*m*K.det(method='domain-ge')/(512*(1-a*a)**2)),a)
assert P.degree()<=4
px=S.Poly(P.as_expr().subs(a,2*x-1),x)
b=[sum(S.Rational(comb(i,j),comb(4,j))*px.nth(j) for j in range(i+1)) for i in range(5)]
assert all(v['lower_exact']==v['upper_exact'] for v in ans['bernstein_coefficients'])
assert all(S.Rational(v['lower_exact'])==bi for v,bi in zip(ans['bernstein_coefficients'],b))
# Reproducibility and actual interval certificate positivity.
re=json.load(open(ROOT/'independent_nu1_moments_N2048.json'));assert raw['moments']==re['moments']
final=json.load(open(ROOT/'independent_bernstein_N2048_delta1.json'));assert final['all_positive'] and all(F(v['lower_exact'])>0 for v in final['bernstein_coefficients'])
out={'passed':True,'bernstein_basis_identity_checks':basis_checks,'direct_schur_determinant_matches_bernstein_exactly':True,'moment_endpoints_reproduced_exactly':True,'all_certified_bernstein_lowers_strictly_positive':True,'minimum_bernstein_lower_exact':str(min(F(v['lower_exact']) for v in final['bernstein_coefficients']))}
(ROOT/'independent_certificate_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
