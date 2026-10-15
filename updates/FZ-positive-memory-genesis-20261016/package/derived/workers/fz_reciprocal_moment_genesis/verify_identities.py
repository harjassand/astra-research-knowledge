"""Exact symbolic verification, with complex conjugation as an involution."""
from pathlib import Path
import json, time
import sympy as s
ROOT=Path(__file__).resolve().parent
start=time.monotonic()
x,X,y,Y,u,U,v,V,alpha,A,beta,B=s.symbols('x X y Y u U v V alpha A beta B')
ai,aj,bi,bj=s.symbols('ai aj bi bj',positive=True)
swap=dict(zip((x,X,y,Y,u,U,v,V,alpha,A,beta,B),(X,x,Y,y,U,u,V,v,A,alpha,B,beta)))
def star(f):return f.xreplace(swap)
def norm(f):return s.expand(f*star(f))
def re(f):return s.expand((f+star(f))/2)
def degree(f):return s.Poly(s.expand(f),x,X,y,Y,u,U,v,V).total_degree()
hi=X*u-1;hj=Y*v-1
z=alpha*u+beta*v;q=alpha*Y+beta*X
delta=X*Y*z-q
assert s.expand(delta-alpha*Y*hi-beta*X*hj)==0
upper_terms=[norm(bi*Y*z-x*q)/bi,bi*(bj-norm(y))*norm(z),(bi-norm(x))*norm(q)/bi,2*re(star(q)*delta)]
lower_terms=[(norm(x)-ai)*norm(Y*z),ai*(norm(y)-aj)*norm(z),-2*re(star(q)*delta),-norm(delta)]
assert s.expand(bi*bj*norm(z)-norm(q)-sum(upper_terms))==0
assert s.expand(norm(q)-ai*aj*norm(z)-sum(lower_terms))==0
ideal_delta_square=-re(star(delta)*alpha*Y*hi)-re(star(delta)*beta*X*hj)
assert s.expand(-norm(delta)-ideal_delta_square)==0
dprime=u*v*q-z
assert s.expand(dprime-beta*v*hi-alpha*u*hj)==0
aug_terms=[aj*norm(v*q-ai*U*z),(1-aj*norm(v))*norm(q),ai*aj*(1-ai*norm(u))*norm(z),2*ai*aj*re(star(z)*dprime)]
assert s.expand(norm(q)-ai*aj*norm(z)-sum(aug_terms))==0
scalar_rhs=(norm(x)-ai)*norm(u)-2*re(hi)-norm(hi)
assert s.expand(1-ai*norm(u)-scalar_rhs)==0
out={'status':'PASS','identities_checked':['delta fixed-power decomposition','upper reciprocal identity','lower reciprocal identity','negative delta square equality-ideal decomposition','swapped delta decomposition','augmented degree4 lower identity','scalar current-bound certificate'],'upper_term_degrees':list(map(int,map(degree,upper_terms))),'lower_term_degrees':list(map(int,map(degree,lower_terms))),'augmented_lower_term_degrees':list(map(int,map(degree,aug_terms))),'scalar_current_certificate_term_degrees':list(map(int,map(degree,[(norm(x)-ai)*norm(u),-2*re(hi),-norm(hi)]))),'scalar_current_bound_target_degree':int(degree(1-ai*norm(u))),'representation':'Independent complex coordinate/conjugate indeterminates with exact involution; substitution to eight real coordinates preserves identities. u,v may then be any specified complex linear forms of finite voltage variables.','wall_seconds':time.monotonic()-start,'sympy_version':s.__version__}
(ROOT/'SYMBOLIC_IDENTITY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
