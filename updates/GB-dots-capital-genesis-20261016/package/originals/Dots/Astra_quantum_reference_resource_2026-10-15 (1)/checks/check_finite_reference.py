import sympy as s,json
from pathlib import Path
e=s.symbols('e',positive=True);p,q,r=s.symbols('p q r');Q=s.Rational
assert s.expand(r*r*p+q-(r+1)**2*p*q-((r*p-q)**2+(1-p-q)*(r*r*p+q)))==0
v=[s.Matrix([1,0]),s.Matrix([-Q(1,2),s.sqrt(3)/2]),s.Matrix([-Q(1,2),-s.sqrt(3)/2])]
R0=[Q(2,3)*x*x.T for x in v]+[s.zeros(2)]
R=[(x+e*s.eye(2))/(1+4*e) for x in R0]
H=[R0[0],-R0[1],s.zeros(2),s.zeros(2)];K=sum(H,s.zeros(2))
E=s.factor(sum(s.trace(h*a.inv()*h) for h,a in zip(H,R))-s.trace(K*K))
T=s.factor(sum(s.trace((h/2+K/8)*(a/2+s.eye(2)/8).inv()*(h/2+K/8)) for h,a in zip(H,R))-s.trace(K*K))
ratio=s.factor(T/E);lim=s.limit(ratio,e,0);assert lim==Q(4,11)
assert s.simplify(sum(R,s.zeros(2))-s.eye(2))==s.zeros(2)
assert sum(s.trace(h) for h in H)==0
out={'projection_identity_exact':True,'m':4,'reference_dimension':2,'lambda':'1/2','input_excess':str(E),'target_excess':str(T),'ratio':str(ratio),'sharp_limit':str(lim),'ordinary_threshold':'1/3','unrestricted_threshold':'3/8'}
assert json.loads(Path(__file__).with_name('finite_reference_check.json').read_text()) == out, 'Exact fixture mismatch';print(out)
