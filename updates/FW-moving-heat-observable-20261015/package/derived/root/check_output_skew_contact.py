import sympy as s
import json
from pathlib import Path
a,b,c,d=s.symbols("a b c d");x=s.Matrix([a,b,c,d]);z=s.Matrix(s.symbols("z0:6"));r,t,d1,d2,bb=s.symbols("r t d1 d2 bb")
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c;H=(u+v-2*j)**2
F=3*r*H/(8*(r+2))+r*(r-1)*u*u/6+j*j+r*u*j
HH=s.hessian(F,x);B1=s.Matrix([z[0],z[1],z[3],z[4]]);B2=s.Matrix([z[1],z[2],z[4],z[5]])
J=s.Matrix([[0,-1],[1,0]])
def outJ(q):return s.Matrix(list(J*s.Matrix(2,2,list(q))))
heat=d1*(B1.T*HH*B1)[0]+d2*(B2.T*HH*B2)[0]+bb*((B1.T*HH*outJ(B2))[0]+(B2.T*HH*outJ(B1))[0])
y=list(x)+list(z);base=dict(zip(y,[1,0,0,1,0,0,1,0,0,0]));w=s.Matrix([0,-r-1,r+1,0,0,1,0,0,0,0])
Hw=(s.hessian(heat,y)*w).subs(base).applyfunc(s.simplify)
assert list(Hw[:4])==[0,0,-4*bb,0]
curve=dict(zip(y,[1,-(r+1)*t,(r+1)*t,1,t*t,t,1,0,0,0]))
value=s.factor(heat.subs(curve))
assert s.factor(value-((d1*t*t+d2)*s.Rational(2,3)*r*(r+1)**2*(r+2)*t**4-s.Rational(4,3)*bb*r*(r+1)*(r+2)*t**4))==0
S=s.diag(1,-1);AA=s.Matrix(2,2,list(x));Fref=F.subs(dict(zip(x,list(S*AA*S))),simultaneous=True)
assert s.cancel(Fref-F)==0
o={"status":"EXACT_PASS","A_components_Hessian_times_flat_tangent":[str(q) for q in Hw[:4]],"curve_heat":str(value),"paired_reflection_invariance":True,"scope":"Exact output-skew flat-contact identity; correction A-components vanish by alternation, operator averaging and input-class separation are separately proved"}
Path(__file__).with_suffix(".json").write_text(json.dumps(o,indent=2)+"\n");print(json.dumps(o))
