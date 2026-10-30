"""Exact sinusoidal gradient violation after attempting to subtract |A|^4.

This is a countertest for F_(299/301,1084/301) - (1/100)|A|^4,
not a counterexample to the accepted F. Four acoustic roots are kept
exact in their quotient algebra; decimals are only an illustration.
"""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
a,b,c,d,t,h=s.symbols('a b c d t h')
av=(a,b,c,d);tau=s.Rational(1,30);eps=s.Rational(1,100)
H=1+3*tau*tau;B=1-3*tau*tau
mod=s.Poly(B*B*(1-t*t)**2-(1-4*tau+3*tau*tau)*H*(1+t*t)**2,t).monic()
def rem(v):return s.rem(s.expand(v),mod.as_expr(),t)
K=[-B*(tau*(1-t*t)+H*t*t)*(1+t*t),
   B*t*(H-tau*(1-t*t))*(1+t*t),
   B*B*t*(1-t*t)-tau*H*t*(1+t*t)**2,
   B*B*t*t*(1-t*t)+tau*H*(1+t*t)**2]
K=list(map(rem,K))
inverse=s.invert(K[0],mod.as_expr(),t)
K=[rem(kk*inverse) for kk in K]
assert K[0]==1
R=s.Matrix([1,t,0,0]);Km=s.Matrix(K)
T=sum(z*z for z in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=T*T+4*(3-12*tau/H)*q*q+4*B/H*q*X
G=T*T;W=F-eps*G
HR=s.hessian(F,av).subs(dict(zip(av,R)))
assert all(rem(v)==0 for v in HR*Km)
cg=rem((Km.T*s.hessian(G,av).subs(dict(zip(av,R)))*Km)[0])
assert rem(cg-(4*sum(kk*kk for kk in K)*(1+t*t)+8*(K[0]+t*K[1])**2))==0
line=s.Poly(s.expand(W.subs(dict(zip(av,[kk+h*rr for kk,rr in zip(K,R)])),simultaneous=True)),h)
assert rem(line.nth(2)+eps*cg/2)==0
wr=(1-eps)*(1+t*t)**2
assert s.expand(line.nth(4)-wr)==0
delta2=eps*cg/(3*wr)
gap=s.cancel(-eps*cg*delta2/4+3*wr*delta2*delta2/8)
assert s.cancel(gap+eps*eps*cg*cg/(24*wr))==0
# Pick the smallest positive root only for the displayed numerical fixture.
C=-mod.nth(2)
root=s.sqrt((C-s.sqrt(C*C-4))/2)
approx={
    't':float(root.evalf()),
    'base_K':[float(kk.subs(t,root).evalf()) for kk in K],
    'delta_squared':float(delta2.subs(t,root).evalf()),
    'mean_energy_gap':float(gap.subs(t,root).evalf()),
}
assert approx['delta_squared']>0 and approx['mean_energy_gap']<0
record={'tau':str(tau),'epsilon':str(eps),'root_polynomial':str(mod.as_expr()),
    'base_K_mod_m':list(map(str,K)),'rank_one_R':[1,'t',0,0],
    'positive_acoustic_G_cost_mod_m':str(cg),
    'delta_squared':'epsilon*c_G/(3*(1-epsilon)*(1+t^2)^2)',
    'exact_mean_gap':'-epsilon^2*c_G^2/(24*(1-epsilon)*(1+t^2)^2) < 0',
    'gradient_field':'Dphi = delta * R * cos((1,t) dot x) on its periodic cell',
    'exact_line_coefficients_checked':True,
    'all_four_real_acoustic_roots_covered':True,
    'numerical_fixture_only':approx}
(OUT/'corrugation_data.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
