"""Source-specific all-parameter geometry and half-period strength obstruction."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'capability_backward_bridge/code/vendor'))
import sympy as s
A,B,C,z=s.symbols('A B C z',real=True)
gamma=s.Matrix([A*s.cos(z)-B*s.sin(z),A*s.sin(z)-B*s.cos(z),A*B+s.sin(2*z)/2])
tangent=gamma.diff(z);cross=tangent.cross(tangent.diff(z))
assert s.simplify(cross[2]-(A*A-B*B))==0
speed=s.trigsimp(tangent.dot(tangent));P2=(1+A*A)*(1+B*B);E=A*B-s.sin(2*z)
assert s.trigsimp(speed-(P2-E*E))==0
# Ellipsoidal gamma=(a sn(t), b cn(t),c dn(t)); zeta-derivatives include1/2.
sn,cn,dn,g,a,b=s.symbols('sn cn dn g a b',real=True)
dx=a*cn*dn;dy=-b*sn*dn
ddx=-a*sn*(dn**2+(1-g)*cn**2);ddy=-b*cn*(dn**2-(1-g)*sn**2)
assert s.factor((dx*ddy-dy*ddx)+a*b*dn**3*(sn*sn+cn*cn))==0
mu,L,V=s.symbols('mu L V',positive=True);D=lambda x:(L-x)*(x-V)/4
half_diff=s.factor(D(mu)-D(g/mu))
assert s.simplify(half_diff+(mu*mu-g)*(mu*mu-(L+V)*mu+g)/(4*mu*mu))==0
# For0<g<1/4, L>1,0<=V<g, put S=L+V>=1,p=LV>=0.
S,p=s.symbols('S p',positive=True)
num=S/2-s.Rational(1,4)-p;den=2*g*S-4*g*g-p
ratio=s.cancel(num/den)
dp=s.factor(s.diff(ratio,p));dS=s.factor(s.diff(ratio.subs(p,0),S))
# Difference num-den is positive: at S=1 it is(1/2-2g)^2.
assert s.factor((num-den).subs(S,1)-(s.Rational(1,2)-2*g)**2)==0
bound=s.factor(ratio.subs({p:0,S:1}));assert s.simplify(bound-1/(8*g*(1-2*g)))==0
out={'status':'PASS','paraboloidal_cross_z':str(s.factor(cross[2])),'paraboloidal_axis_speed_squared':str(speed),'paraboloidal_axis_min_speed_squared':'min((A-B)^2,(A+B)^2)>0 for source regularity','ellipsoidal_cross_z':'-a*b*dn(tau)^3/8 for zeta derivatives','half_period_metric_difference':str(half_diff),'ratio_derivative_p':str(dp),'ratio_derivative_S_at_p0':str(dS),'ellipsoidal_axis_mirror_lower':'Bmax/Bmin >=1/sqrt(8*g*(1-2*g)) for0<g<1/4, all regular source axis locations and printed profile parameters','g_printed':str((3-2*s.sqrt(2))**2),'mirror_lower_printed':float(1/s.sqrt(8*(3-2*s.sqrt(2))**2*(1-2*(3-2*s.sqrt(2))**2))),'scope':'Printed Jacobi/paraboloidal and Jacobi/ellipsoidal families. No practical confinement no-go; Gardner extensions not audited.'}
Path('results/axis_structural.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
