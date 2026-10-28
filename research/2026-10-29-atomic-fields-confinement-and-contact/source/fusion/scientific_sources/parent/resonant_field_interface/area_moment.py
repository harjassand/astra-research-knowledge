"""Source-specific closed-orbit area, exact Laurent coefficient extraction."""
import sympy as s
import json,time
from pathlib import Path
start=time.monotonic()
z=s.symbols('z',nonzero=True);a,b=s.symbols('a b',positive=True,real=True);I=s.I
p=a*z;pb=a/z
N=s.Matrix([1-p*p,I*(1+p*p),2*p]);Nb=s.Matrix([1-pb*pb,-I*(1+pb*pb),2*pb])
A=(N+Nb)/2;C=(N-Nb)/(2*I)
H=2*p*p+2*I*p**3;Hb=2*pb*pb-2*I*pb**3
nv=s.Matrix([a*(z+1/z),a*(z-1/z)/I,a*a-1])/(1+a*a)
k=2*a**3*(z+1/z)*(1-a*(z-1/z)/(2*I))/(1+a*a)**2
X=(((H+Hb)/2*A+(H-Hb)/(2*I)*C)/(1+a*a)**2+(b-k)*nv).applyfunc(s.cancel)
Xp=X.diff(z)*I*z
area=[]
for v in X.cross(Xp):
    # Clear the known Laurent pole before using Poly; .coeff on an expanded
    # rational denominator alone would incorrectly return zero.
    polynomial=s.Poly(s.cancel(v*z**12),z,domain='EX')
    area.append(s.factor(polynomial.nth(12)))
print('area/pi:',area,flush=True)
Xl=X.diff(a)/(2*a);Xb=X.diff(b)
assert s.cancel(Xp.dot(Xl))==0
assert s.cancel(Xp.dot(Xb))==0
Jac=s.det(s.Matrix.hstack(Xl,Xb,Xp))
assert s.cancel(Jac-Xp.dot(Xp)/(2*a*a))==0
result={'source':'Lopez arXiv2610.29921v1 equation coordinate map',
    'variables':'a=sqrt(lambda)>0; b=beta; z=exp(i phi)',
    'area_vector_divided_by_pi':[str(v)for v in area],
    'flux_two_form_coefficient':'1/(2*lambda)',
    'checks':'Exact physical-coordinate orthogonality and Jacobian/metric identity pass',
    'seconds':time.monotonic()-start}
Path(__file__).with_name('AREA_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
