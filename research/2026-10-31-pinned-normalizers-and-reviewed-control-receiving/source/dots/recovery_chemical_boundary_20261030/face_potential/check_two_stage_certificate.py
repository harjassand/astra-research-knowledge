"""Exact orthant coefficient certificates, not finite-population testing."""
import json
import sympy as S
from pathlib import Path
a,C,E,F=S.symbols('a C E F'); u,v,w,t=S.symbols('u v w t', nonnegative=True)
z=E+F; V=3*E+2*F;c=a*(a-1)
d=C*z+c*V;dm=C*z+c*(V-1);dp=C*z+c*(V+1)
N=S.expand(4*C*C*z*(E*dp-F*dm)+4*(C*F+c)*V*dm*dp-3*d*dm*dp)
records=[]
for av in [S.Integer(0),S.Integer(1),2+w]:
 for ev,fv in [(S.Integer(0),1+v),(1+u,S.Integer(0)),(1+u,1+v)]:
  poly=S.Poly(N.subs({a:av,C:1+t,E:ev,F:fv}),u,v,w,t)
  vals=poly.coeffs(); neg=[str(x) for x in vals if x<0]
  records.append(dict(a=str(av),E=str(ev),F=str(fv),terms=len(vals),negative_coefficients=neg,pass_nonnegative=not neg))
out=dict(identity='(-Q_face psi-1) * 3*d*d_minus*d_plus = N',
 denominator_positive='C>=1,E+F>=1 implies V>=2, d,d_minus,d_plus>0; c>=0',
 psi='(4/3)*(3E+2F)/(C*(E+F)+a*(a-1)*(3E+2F))',
 domain='all integer a>=0,C>=1,E>=0,F>=0,E+F>=1',
 all_pass=all(x['pass_nonnegative'] for x in records),cells=records)
print(json.dumps(out,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
assert out['all_pass'], 'Coefficient cone failed: analytic proof may still hold.'
