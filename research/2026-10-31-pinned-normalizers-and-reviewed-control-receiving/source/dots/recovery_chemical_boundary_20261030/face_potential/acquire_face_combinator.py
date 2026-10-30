"""Finite exact base-potential search + proof-checked killing combinator.
Restricted face-module prototype; NOT a full raw-network recurrence finder.
"""
import json, itertools
from pathlib import Path
import sympy as S
C,E,F,D=S.symbols('C E F D'); eu,fv,cw=S.symbols('eu fv cw',nonnegative=True)
raw=[dict(source={'C':1,'E':1},target={'C':1,'F':1},rate=1),
     dict(source={'C':1,'F':1},target={'C':1,'E':1},rate=1),
     dict(source={'C':1,'F':1},target={'C':1,'D':1},rate=1)]
syms={'C':C,'E':E,'F':F,'D':D}
def generator(psi):
 out=0
 for r in raw:
  rate=S.Integer(r['rate'])
  for name,p in r['source'].items():
   for j in range(p):rate*=syms[name]-j
  if r['target'].get('D',0)>0:dest=0
  else:
   shift={s:s+r['target'].get(n,0)-r['source'].get(n,0) for n,s in syms.items()}
   dest=psi.subs(shift,simultaneous=True)
  out+=rate*(dest-psi)
 return S.factor(out.subs(D,0))
tried=0;answer=None
for u,v in sorted(itertools.product(range(9),repeat=2),key=lambda x:(sum(x),x)):
 tried+=1
 psi=(u*E+v*F)/(C*(E+F))
 num,den=S.fraction(S.factor(-generator(psi)-1))
 if den not in [S.Integer(1),E+F]:continue
 checks=[]
 for ee,ff in [(0,1+fv),(1+eu,0),(1+eu,1+fv)]:
  p=S.Poly(num.subs({E:ee,F:ff,C:1+cw}),eu,fv,cw)
  checks.append(all(q>=0 for q in p.coeffs()))
 if all(checks):answer=(u,v,psi,num,den);break
assert answer is not None
u,v,psi,num,den=answer
x,y,c=S.symbols('x y c',nonnegative=True); f=lambda t:t/(1+c*t)
concavity=S.factor(S.diff(f(x),x)*(y-x)-(f(y)-f(x)))
assert S.simplify(concavity-c*(y-x)**2/((1+c*x)**2*(1+c*y)))==0
z=S.symbols('z',nonnegative=True)
kill=S.factor(S.Rational(4,3)*(1/(1+z)**2+z/(1+z))-1)
assert S.simplify(kill-(z-1)**2/(3*(1+z)**2))==0
regular=S.factor(S.Rational(4,3)*psi/(1+c*psi))
out=dict(status='LOCAL_FACE_CERTIFICATE_ACQUIRED',scope='Base finite ansatz + exact analytic combinator only; no full-network conclusion',
 raw_face_reactions=raw,candidates_checked=tried,coefficients=dict(E=u,F=v),
 psi0=str(psi),base_drift_numerator=str(num),base_drift_denominator=str(den),base_cells_all_nonnegative=True,
 domain='integer C>=1,E>=0,F>=0,E+F>=1; c>=0',
 concavity_remainder=str(concavity),killing_remainder=str(kill),psi_killed=str(regular),
 uniform_bound=str(S.Rational(4,3)*max(u,v)),
 ingress_C_rate_one_bound=str(S.Rational(4,3)*max(u,v)),
 ingress_a_rate_one_bound='4/(3*k*(a+1)) at actual a_out=a+1, c_out=k*a*(a+1), a>=1',
 comparison='Monolithic coefficient checker failed in F=0,a>=2; these square certificates are binding.')
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
