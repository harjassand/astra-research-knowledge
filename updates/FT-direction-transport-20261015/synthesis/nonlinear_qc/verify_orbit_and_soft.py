"""Exact algebra for the analytic DM orbit exclusion and soft-action corollary."""
from pathlib import Path
import json
import sympy as S

ROOT=Path(__file__).resolve().parent
checks=[]


def check(name,detail):
    checks.append({'name':name,'status':'PASS','detail':detail})
    print('PASS:',name,flush=True)


p1,p2,q1,q2,t,gamma=S.symbols('p1 p2 q1 q2 t gamma',real=True)
s=p1*p1+p2*p2+q1*q1+q2*q2
r=p1*q1+p2*q2
delta=p1*q2-p2*q1
norm=s+2*r*t+(q1*q1+q2*q2)*t*t
f=norm*norm-2*gamma*norm*delta
probe=S.expand(S.diff(f,t,2).subs(t,0))
assert S.expand(probe-8*r*r-4*(s-gamma*delta)*(q1*q1+q2*q2))==0
check('Exact transformed DM shear acoustic probe',str(probe))

aa,bb,cc=S.symbols('aa bb cc',real=True)
isotropic=aa*norm*norm+bb*norm*delta+cc*delta*delta
iso_probe=S.diff(isotropic,t,2).subs(t,0)
assert S.expand(iso_probe-8*aa*r*r-(4*aa*s+2*bb*delta)*(q1*q1+q2*q2))==0
ss,jj=S.symbols('ss jj',real=True)
assert S.expand(aa*ss*ss+bb*ss*jj+cc*jj*jj
  -(4*aa+bb)*(ss+2*jj)**2/8-(4*aa-bb)*(ss-2*jj)**2/8-(cc-4*aa)*jj*jj)==0
for sign in (1,-1):
    base_norm=(1+t)**2+1
    base_det=sign*(1+t)
    fun=aa*base_norm**2+bb*base_norm*base_det+cc*base_det**2
    assert S.expand(S.diff(fun,t,2).subs(t,0)-(16*aa+6*sign*bb+2*cc))==0
    endpoint=fun.subs(bb,-4*sign*aa)
    assert S.expand(S.diff(endpoint,t,2).subs(t,0)-2*(cc-4*aa))==0
check('Full isotropic generator compactification and endpoint identities',{
      'necessary_bounds':'a>=0, |b|<=4a, c>=-8a+3|b|',
      'polyconvex_threshold':'c>=4a',
      'endpoint_curvature':'b=-4 sign a implies 2(c-4a)'})

p_norm=p1*p1+p2*p2
q_norm=q1*q1+q2*q2
assert S.expand(s*s-4*delta*delta-(p_norm-q_norm)**2-4*r*r)==0
assert S.expand(p_norm*p_norm+q_norm*q_norm-s*s/2-(p_norm-q_norm)**2/2)==0
check('Determinant and orbit-mass square identities','s^2-4det^2=(|p|^2-|q|^2)^2+4(p.q)^2; row fourth powers >=s^2/2')

a,b,c,d=S.symbols('a b c d',real=True)
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
G=3*(u+v-2*j)**2+S.Rational(35,24)*u*u+j*j-S.Rational(5,2)*j*u
assert G.subs({a:1,b:0,c:0,d:0})+G.subs({a:0,b:1,c:0,d:0})==S.Rational(179,24)
assert S.diff(G,b,2).subs({a:1,b:0,c:0,d:1})==0
assert (36**4*G.subs({a:1,b:0,c:0,d:1})+36**2*G.subs({a:1,b:0,c:0,d:-1}))/(1+36**2)==-S.Rational(1350,1297)
check('G probe and separating law constants',{'rank_one_sum':'179/24','acoustic_probe':'0','law_gap':'-1350/1297'})

p,q,r,svar=S.symbols('p q r svar',real=True)
A=S.Matrix([[1+S.Rational(2,3)*svar*q,S.Rational(2,3)*svar*r],[svar*p,1+svar*q]])
poly=S.Poly(S.expand(G.subs(dict(zip((a,b,c,d),list(A))),simultaneous=True)),svar)
K=(8667*p**4+18792*p**3*r+576*p*p*q*q+16416*p*p*r*r+1440*p*q*q*r
   +6912*p*r**3+56*q**4+576*q*q*r*r+1152*r**4)/S.Integer(1944)
assert S.expand(poly.coeff_monomial(svar)+S.Rational(5,18)*q)==0
assert S.expand(poly.coeff_monomial(svar**2)-(5*p*p+4*p*r-4*q*q)/12)==0
assert S.expand(poly.coeff_monomial(svar**3)+S.Rational(5,162)*q*(9*p*p+4*q*q))==0
assert S.expand(poly.coeff_monomial(svar**4)-K)==0
assert K.subs({p:1,q:0,r:-S.Rational(3,2)})==-S.Rational(1,24)
assert S.Rational(5,3)*(S.Rational(162,5))**2==S.Rational(8748,5)
check('Full compatible soft action and compensated constant',{'quartic_negative_jet':'K(1,0,-3/2)=-1/24','integrated_constant':'8748/5'})

receipt={'status':'EXACT_PASS','groups':len(checks),'checks':checks,
         'scope':'finite algebra only; analytic orbit and heat implications are separately proved',
         'external_review':'UNKNOWN','historical_novelty':'UNKNOWN'}
(ROOT/'ORBIT_AND_SOFT_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
