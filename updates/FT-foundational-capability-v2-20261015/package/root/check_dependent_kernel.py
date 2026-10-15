"""Symbolic derivatives and bounded grid checks for the explicit kernel."""
import json, math
from pathlib import Path
import sympy as sp
import numpy as np

s,L=sp.symbols('s L',positive=True)
t=1+s/L**2; ell=sp.log(t)
h=L*sp.sqrt(t)*ell/2
formulas=[(ell+2)/(4*L*sp.sqrt(t)), -ell/(8*L**3*t**sp.Rational(3,2)),
          (3*ell-2)/(16*L**5*t**sp.Rational(5,2)),
          (16-15*ell)/(32*L**7*t**sp.Rational(7,2))]
for j,f in enumerate(formulas,1): assert sp.simplify(sp.diff(h,s,j)-f)==0
x,y=sp.symbols('x y',real=True)
F=sp.Function('F'); z=x*x+y*y
want=4*sp.Subs(sp.diff(F(s),s,2),s,z)+8*z*sp.Subs(sp.diff(F(s),s,3),s,z)+16*x*x*y*y*sp.Subs(sp.diff(F(s),s,4),s,z)
assert sp.simplify(sp.diff(F(z),x,2,y,2)-want)==0
lv=5.; B=27/(math.e**2*lv)+(1.5+4/27)/lv**2+2.5/lv**3
minimum=(float('inf'),None,None)
radii=np.concatenate(([0.],np.geomspace(1e-8,1e60,1500)))
angles=np.linspace(0,math.pi/2,101)
for r in radii:
    ss=r*r; tt=1+ss/lv**2; ll=math.log(tt)
    h1=(ll+2)/(4*lv*math.sqrt(tt)); h2=-ll/(8*lv**3*tt**1.5)
    h3=(3*ll-2)*math.exp(-2.5*ll)/(16*lv**5)
    h4=(16-15*ll)*math.exp(-3.5*ll)/(32*lv**7)
    a2=h1*h1-h2; a3=-h1**3+3*h1*h2-h3
    a4=h1**4-6*h1*h1*h2+3*h2*h2+4*h1*h3-h4
    for angle in angles:
        x2y2=ss*ss*(math.sin(2*angle)**2)/4
        ratio=1+4*a2+8*ss*a3+16*x2y2*a4
        assert math.isfinite(ratio) and ratio>=1-B-1e-12
        if ratio<minimum[0]: minimum=(ratio,float(r),float(angle))
assert 1-B>0
result={'schema':'astra.genesis2.explicit-dependent-kernel-check.v1','symbolic_h_derivatives':4,
        'symbolic_mixed_derivative_identity':True,'L':lv,'analytic_lower_ratio':1-B,
        'finite_grid_points':len(radii)*len(angles),'grid_min_ratio':minimum[0],
        'grid_min_radius':minimum[1],'grid_min_angle':minimum[2],
        'all_assertions_passed':True,
        'numerical_evaluation':'negative powers via exp to avoid overflowing intermediate positive powers; floating-point underflow of negligible remote terms remains possible',
        'scope':'symbolic calculus and finite floating-point grid; all-point positivity uses written inequalities'}
Path(__file__).with_name('DEPENDENT_KERNEL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
