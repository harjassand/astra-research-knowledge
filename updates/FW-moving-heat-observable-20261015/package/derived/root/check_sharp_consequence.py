import sympy as s
import json
from pathlib import Path
r,t=s.symbols("r t",real=True)
a,b,c,d=s.symbols("a b c d")
x=s.Matrix([a,b,c,d]);u=a*a+c*c;v=b*b+d*d;j=a*d-b*c;H=(u+v-2*j)**2
F=3*r/(8*(r+2))*H+r*(r-1)*u*u/6+j*j+r*u*j
I={a:1,b:0,c:0,d:1}
lift=F-(r+2)*j
V=s.Matrix([1,0,0,-r-1])
assert s.simplify((s.hessian(lift,x).subs(I)*V))==s.zeros(4,1)
curve={a:1+t,b:0,c:0,d:1-(r+1)*t}
gap=s.expand(lift.subs(curve)-lift.subs(I)-(s.Matrix([s.diff(lift,y).subs(I) for y in x]).dot(t*V)))
cubic=s.factor(gap.coeff(t,3));quartic=s.factor(gap.coeff(t,4))
assert cubic==-r*(r+2)/3
assert s.factor(quartic-(r+2)*(9*r**3+36*r**2+40*r+12)/24)==0
assert s.simplify(s.diff(lift,b,c).subs(I))==0
alpha,beta,gamma,delta=s.symbols("alpha beta gamma delta")
rho=(6*beta+delta)/delta;lam=delta**2/(6*beta+delta)
F4=alpha*H+beta*u*u+gamma*j*j+delta*u*j
Fsharp=F.subs(r,rho)
assert s.cancel(F4-lam*Fsharp-(gamma-lam)*j*j-(alpha-delta**2/(8*(2*beta+delta)))*H)==0
out={"status":"EXACT_PASS","sharp_nonPC_support_gap_cubic":str(cubic),"quartic":str(quartic),"null_direction":[str(q) for q in V],"four_coefficient_decomposition":True,"scope":"Symbolic consequence checks; analytic PC support premise and QC heat proof separately reconstructed"}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
