#!/usr/bin/env python3
"""Independent theorem algebra; never imports or executes candidate consumer."""
import hashlib,json,math
from fractions import Fraction as Q
from pathlib import Path
import sympy as S
import mpmath as mp
HERE=Path(__file__).resolve().parent
SRC=HERE.parent
checks=[]
def eq(name,a,b=0):
    residue=S.cancel(a-b)
    assert residue==0,(name,residue)
    checks.append(name)
def truth(name,b):
    assert b,name
    checks.append(name)
t,x,y,k,d,e=S.symbols('t x y k d e', real=True)
s=1+k*(1-t)**2
s0=1+k
v=t/(1+t)**2
flat=t*(t-1)**2/(1+t)**4
eq('flat v representation',flat,v*(1-4*v))
eq('sensitive derivative',S.diff(v,t),(1-t)/(1+t)**3)
eq('flat derivative',S.diff(flat,t),-(t-1)*(t*t-6*t+1)/(1+t)**5)
eq('s upper slack',s0*(1+t)**2-s,t*t+2*t+4*k*t)
eq('quadratic tail helper',2*(t-1)**2+8-(1+t)**2,(t-3)**2)
eq('flat derivative absolute upper branch',2*(1+t)**2-(t*t-6*t+1),t*t+10*t+1)
eq('flat derivative absolute lower branch',2*(1+t)**2+(t*t-6*t+1),3*(t-S.Rational(1,3))**2+S.Rational(8,3))
for sign in [-1,1]:
    rr=s*(1+sign*d*v)
    eq('sensitive derivative factor '+str(sign),S.diff(rr,t),(t-1)*(2*k*(1+sign*d*v)-sign*d*s/(1+t)**3))
    rr=s*(1+sign*d*flat)
    eq('flat derivative factor '+str(sign),S.diff(rr,t),(t-1)*(2*k*(1+sign*d*flat)-sign*d*s*(t*t-6*t+1)/(1+t)**5))
    for degree in [2,4]:
        for E,prof in [(t*(1+t)**2,v),(t*(t-1)**2,flat)]:
            eq('denominator clearing '+str((sign,degree,str(prof))), (s*(1+sign*d*prof))**degree*(1+t)**16, s**degree*((1+t)**4+sign*d*E)**degree*(1+t)**(16-4*degree))
            poly=S.Poly(s**degree*((1+t)**4+sign*d*E)**degree*(1+t)**(16-4*degree),t)
            truth('profile degree '+str((sign,degree,str(prof))),poly.degree()==16+2*degree)
            eq('profile leading '+str((sign,degree,str(prof))),poly.LC(),k**degree)
            eq('profile anchor '+str((sign,degree,str(prof))),poly.eval(0),s0**degree)
# The four local Taylor expansions control the two separate Laplace locations.
sy=(1+(1-y*y)**2)
sens=sy*(1+e*y*y/(1+y*y)**2)
eq('sensitive barrier value',sens.subs(y,0),2)
eq('sensitive barrier quadratic',S.diff(sens,y,2).subs(y,0)/2,-2*(1-e))
eq('sensitive well value',sens.subs(y,1),1+e/4)
eq('sensitive well linear',S.diff(sens,y).subs(y,1),0)
eq('sensitive well quadratic',S.diff(sens,y,2).subs(y,1)/2,4+3*e/4)
for sign in [-1,1]:
    ff=sy*(1+sign*d*y*y*(y*y-1)**2/(1+y*y)**4)
    eq('flat barrier value '+str(sign),ff.subs(y,0),2)
    eq('flat barrier quadratic '+str(sign),S.diff(ff,y,2).subs(y,0)/2,-2*(1-sign*d))
    eq('flat well value '+str(sign),ff.subs(y,1),1)
    eq('flat well linear '+str(sign),S.diff(ff,y).subs(y,1),0)
    eq('flat well quadratic '+str(sign),S.diff(ff,y,2).subs(y,1)/2,4+sign*d/4)
# Exact projective transform and de Casteljau identities, not sampled positivity.
def split(bs):
    levels=[bs]
    while len(levels[-1])>1:
        old=levels[-1];levels.append([(old[i]+old[i+1])/2 for i in range(len(old)-1)])
    return [r[0] for r in levels],[r[-1] for r in reversed(levels)]
def bern(bs,z):
    D=len(bs)-1
    return sum(S.Rational(q.numerator,q.denominator)*math.comb(D,i)*z**i*(1-z)**(D-i) for i,q in enumerate(bs))
for D in range(0,25):
    aa=[Q((j*j+3*j+1)*(-1)**j,1+j%4) for j in range(D+1)]
    bs=[aa[j]/math.comb(D,j) for j in range(D+1)]
    P=sum(S.Rational(q.numerator,q.denominator)*t**j for j,q in enumerate(aa))
    eq('projective transform degree '+str(D),(1-x)**D*P.subs(t,x/(1-x)),bern(bs,x))
    left,right=split(bs)
    eq('de Casteljau left degree '+str(D),bern(left,x),bern(bs,x/2))
    eq('de Casteljau right degree '+str(D),bern(right,x),bern(bs,(1+x)/2))
# Exact rational log-derivative bound on representative atom profiles.
# This is supplementary: the general proof is in REVIEW.md.
for kap in [Q(1,100),Q(1),Q(100)]:
  for degree in [2,4]:
    delta=kap/(2*(1+kap))
    h=min(Q(1,8),kap/2)*(1-delta/4)
    st=1+S.Rational(kap.numerator,kap.denominator)*(1-t)**2
    for prof,E in [('sensitive',t*(1+t)**2),('flat',t*(t-1)**2)]:
      for sign in [-1,1]:
        N=S.Poly(st**degree*((1+t)**4+sign*S.Rational(delta.numerator,delta.denominator)*E)**degree*(1+t)**(16-4*degree),t)
        aa=[Q(a) for a in reversed(N.all_coeffs())]
        D=N.degree();L=sum(map(abs,aa));bound=2*D*L/h**degree
        for tv in [Q(0),Q(1,100),Q(1,2),Q(1),Q(2),Q(100)]:
          nv=sum(a*tv**j for j,a in enumerate(aa))
          tnp=sum(j*a*tv**j for j,a in enumerate(aa))
          truth('atom lower '+str((kap,degree,prof,sign,tv)),nv>=h**degree*(1+tv)**(16+2*degree))
          truth('logderivative '+str((kap,degree,prof,sign,tv)),abs(2*tnp/nv)<=bound)
# Frozen binding: all three exact inputs and the freeze itself must match.
inputs=json.loads((HERE/'review_input_hashes.json').read_text())
for name,row in inputs.items():
    b=(SRC/name).read_bytes()
    truth('source unchanged '+name,len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
# Numerical illustrations of proved asymptotics; these are NOT proof enclosures.
mp.mp.dps=60
numeric=[]
for eps in [mp.mpf('0.02'),mp.mpf('0.2')]:
  a=1+eps/4;quad=4+3*eps/4
  r=lambda yy:(1+(1-yy*yy)**2)*(1+eps*yy*yy/(1+yy*yy)**2)
  for m in [32,128,512]:
    p=4
    R0scaled=mp.quad(lambda yy:(r(yy)/2)**m,[-mp.mpf('.5'),0,mp.mpf('.5')])
    Rpscaled=mp.quad(lambda yy:(2-(r(yy)/2)**p)**(-mp.mpf(m)/p),[-mp.mpf('.5'),0,mp.mpf('.5')])
    Mscaled=mp.quad(lambda yy:(a/r(yy))**m,[mp.mpf('.5'),1,mp.mpf('1.25'),2,mp.inf])
    numeric.append({'epsilon':str(eps),'m':m,'Rplus_over_R0':str(Rpscaled/R0scaled),
      'R0_over_leading':str(R0scaled/mp.sqrt(mp.pi/(m*(1-eps)))),
      'MA_over_leading':str(Mscaled/mp.sqrt(mp.pi*a/(m*quad)))})
flat_delta=mp.mpf(1)/500
W=mp.sqrt((4+flat_delta/4)/(4-flat_delta/4))*mp.sqrt((1+flat_delta)/(1-flat_delta))
report={'status':'PASS','exact_assertions':len(checks),'scope':'independent theorem algebra only; no candidate code imported or accepted','checks':checks,'nonproof_numeric_laplace_diagnostics':numeric,'nonproof_flat_width_at_delta_1_over_500':str(W)}
(HERE/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
