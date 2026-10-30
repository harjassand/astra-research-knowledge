"""Derive the actual ROC boundary, without a sampled-direction inference."""
from pathlib import Path
import json,sympy as S,time
root=Path(__file__).resolve().parents[1];start=time.perf_counter()
base=json.loads((root/'outputs/hopf_structure/certificate.json').read_text())
graded=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
a,b,c,d,t,x,y=S.symbols('a b c d t x y');A=(a,b,c,d)
u,l,p,n,q,r=map(S.Rational,base['ray']['K_coefficients'])
X=a*a+c*c-b*b-d*d;Y=2*(a*b+c*d);Z=2*(a*d-b*c)
F=S.expand(u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z)
H=S.hessian(F,A).subs({a:1,b:t,c:0,d:0});det=S.Poly(H.det(),t);delta=S.div(det,S.Poly(t*t,t))[0].as_expr()
assert S.expand(det.as_expr()-t*t*delta)==0
adj=H.adjugate();cp=graded['cubic_powers'];ev=list(map(S.Rational,graded['example_cubic_coefficients']))
C=S.expand(sum(co*S.prod(v**e for v,e in zip(A,pw)) for pw,co in zip(cp,ev)))
Rv=S.Matrix([x,x*t,y,y*t]);U=S.Matrix([[x,0,-y,0],[0,x,0,-y],[y,0,x,0],[0,y,0,x]])
grad=S.Matrix([S.diff(C,v).subs(dict(zip(A,Rv)),simultaneous=True) for v in A]);h=U.T*grad
num=S.expand((h.T*adj*h)[0]);quot,rem=S.div(S.Poly(num,t,x,y),S.Poly(t*t,t,x,y));assert rem.is_zero
num=quot.as_expr();assert S.Poly(num,t).degree()<=6
delta0=delta.subs(t,0);num0=S.expand(num.subs(t,0))
g0=h.subs(t,0);H0=H.subs(t,0)
pinv=H0.pinv();at0=S.factor((g0.T*pinv*g0)[0]/(x*x+y*y)**2)
limit0=S.factor(num0/((x*x+y*y)**2*delta0));lost=S.factor(limit0-at0)
def pack(poly,variables):return [[*pw,int(co.p),int(co.q)] for pw,co in S.Poly(poly,*variables).terms()]
out={'F':pack(F,A),'cubic':pack(C,A),'H':[[pack(z,(t,)) for z in row] for row in H.tolist()],
 'delta':pack(delta,(t,)),'regularized_numerator':pack(num,(t,x,y)),
 'limit_minus_root_pseudoinverse':str(lost),
 'degrees':{'delta':int(S.degree(delta,t)),'numerator_t':int(S.degree(num,t)),'numerator_output':6},
 'seconds':time.perf_counter()-start,
 'scope':'Exact boundary reduction: 2*c*Q(R)*(x*x+y*y)^2*delta(t)-N_C(t,x,y)>=0 on all real projective directions, plus cubic compatibility.'}
(root/'work/actual_boundary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'degrees':out['degrees'],'lost_root_constraint':str(lost),'seconds':out['seconds']},indent=2))
