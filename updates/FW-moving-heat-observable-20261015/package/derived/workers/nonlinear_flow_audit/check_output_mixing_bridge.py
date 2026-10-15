#!/usr/bin/env python3
"""Independent averaging and flat-contact identities; no SOS/dual input."""
from pathlib import Path
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
a,b,c,d,r,t=s.symbols('a b c d r t',real=True)
d1,d2,skew=s.symbols('d1 d2 skew',real=True)
x=s.Matrix([a,b,c,d]);z=s.Matrix(s.symbols('z0:6',real=True))
u,v,j=a*a+c*c,b*b+d*d,a*d-b*c
F=3*r/(8*(r+2))*(u+v-2*j)**2+r*(r-1)*u*u/6+j*j+r*u*j
H=s.hessian(F,x)
B1=s.Matrix([z[0],z[1],z[3],z[4]])
B2=s.Matrix([z[1],z[2],z[4],z[5]])
J=s.Matrix([[0,-1],[1,0]]);S=s.diag(1,-1)
J4=s.kronecker_product(J,s.eye(2))
E=(d1*(B1.T*H*B1)[0]+d2*(B2.T*H*B2)[0]
    +skew*((B1.T*H*J4*B2)[0]+(B2.T*H*J4*B1)[0]))
curve={a:1,b:-(r+1)*t,c:(r+1)*t,d:1,
       z[0]:t*t,z[1]:t,z[2]:1,z[3]:0,z[4]:0,z[5]:0}
value=s.factor(E.subs(curve,simultaneous=True))
expected=s.Rational(2,3)*r*(r+1)*(r+2)*t**4*((r+1)*(d1*t*t+d2)-2*skew)
assert s.simplify(value-expected)==0
background_kernel=[s.simplify(s.diff(s.diff(E,xx).subs(curve,simultaneous=True),t).subs(t,0)) for xx in x]
assert background_kernel==[0,0,-4*skew,0]
# Every alternating form has zero A gradient on the pure-jet curve.
omega=s.zeros(4)
count=0
for ii in range(4):
    for jj in range(ii+1,4):
        q=s.Function('omega'+str(count))(*x);count+=1
        omega[ii,jj]=q;omega[jj,ii]=-q
pullback=(B1.T*omega*B2)[0]
zcurve={z[0]:t*t,z[1]:t,z[2]:1,z[3]:0,z[4]:0,z[5]:0}
assert s.expand(pullback.subs(zcurve,simultaneous=True))==0
assert all(s.expand(s.diff(pullback,xx).subs(zcurve,simultaneous=True))==0 for xx in x)

c00,c01,c10,c11=s.symbols('c00 c01 c10 c11')
C=s.Matrix([[c00,c01],[c10,c11]])
rotation_average=(C+J.T*C*J)/2
assert rotation_average==(c00+c11)/2*s.eye(2)+(c10-c01)/2*J
aa11,aa12,aa22,bb11,bb12,bb22=s.symbols('aa11 aa12 aa22 bb11 bb12 bb22')
Cs=[aa11*s.eye(2)+bb11*J,aa12*s.eye(2)+bb12*J,aa22*s.eye(2)+bb22*J]
assert s.simplify((Cs[0]+S*Cs[0]*S)/2)==aa11*s.eye(2)
assert s.simplify((Cs[1]-S*Cs[1]*S)/2)==bb12*J
assert s.simplify((Cs[2]+S*Cs[2]*S)/2)==aa22*s.eye(2)
receipt={'status':'EXACT_PASS',
 'rotation_average':'a I + b J',
 'paired_reflection_survivors':['a11 I','b12 J','a22 I'],
 'flat_curve_full_heat':str(value),
 'background_joint_Hessian_times_tangent':[str(vv) for vv in background_kernel],
 'arbitrary_smooth_alternating_form_A_contribution_zero':True,
 'scope':'Exact identities + all-jet joint Hessian PSD imply b12=0; input no-go and tangent transfer are separate analytic dependencies.',
 'SOS_assumption':False}
(ROOT/'output_mixing_bridge_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
