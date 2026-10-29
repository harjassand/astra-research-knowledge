"""Independent exact Choi-Lam perturbed critical ideal/root completeness review."""
import sympy as s,json,itertools,time,sys
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path('producer-workspace/quaternion_algebraic_completion_20261029');o=Path(__file__).parent
inp=json.loads((r/'input.json').read_text());w,x,y,z=s.symbols('w x y z');qs=[w,x,y,z]
F=sum(s.Rational(c)*s.prod(q**e for q,e in zip(qs,ee)) for c,ee in zip(inp['perturbed'],inp['exponents']))
p=[s.diff(F,v).subs(w,1)-v*s.diff(F,w).subs(w,1) for v in [x,y,z]]
st=time.time();G=s.groebner(p,x,y,z,order='grevlex',method='buchberger');print('own_buchberger',len(G.polys),time.time()-st,flush=True)
lms=[tuple(g.LM(order=G.order).exponents) for g in G.polys];bounds=[min(e[i] for e in lms if e[i]>0 and all(e[j]==0 for j in range(3) if j!=i)) for i in range(3)]
std=[e for e in itertools.product(*(range(b) for b in bounds)) if not any(all(e[i]>=m[i] for i in range(3)) for m in lms)];assert len(std)==40
own=G.fglm(order='lex');author=[s.Poly(s.sympify(v),x,y,z,domain=s.QQ).monic() for v in json.loads((r/'shape.json').read_text())['lex_basis']]
assert [g.monic() for g in own.polys]==author;assert [tuple(g.LM().exponents) for g in author]==[(1,0,0),(0,1,0),(0,0,40)];print('shape_equal',time.time()-st,flush=True)
h=s.Poly(author[-1].as_expr(),z);_,h=h.clear_denoms(convert=True);assert s.gcd(h,h.diff()).degree()==0
isolated=s.polys.polytools.intervals(h,fast=True);assert len(isolated)==28 and all(m==1 for _,m in isolated);print('28_all_real_roots',time.time()-st,flush=True)
rows=json.loads((r/'global_certificate_fast.json').read_text())['root_records'];assert len(rows)==28;prior=None
for row in rows:
 a,b=map(s.Rational,row['z_interval']);assert a<b and h.eval(a)*h.eval(b)<0
 if prior is not None:assert prior<a
 prior=b
for pivot in [x,y,z]:
 free=[v for v in [x,y,z] if v!=pivot];sub={w:0,pivot:1};dp=s.diff(F,pivot).subs(sub);eq=[s.diff(F,w).subs(sub)]+[s.diff(F,v).subs(sub)-v*dp for v in free]
 gb=s.groebner(eq,*free,order='grevlex',method='buchberger');assert list(gb)==[1]
print('three_boundary_charts_empty',time.time()-st,flush=True)
report={'scope':'One perturbed Choi-Lam instance; exact independent Buchberger/FGLM/root/boundary checks','quotient_dimension':len(std),'independent_shape_identical':True,'squarefree_univariate_degree':h.degree(),'complete_real_root_count':len(isolated),'all28_stored_intervals_disjoint_and_sign_changing':True,'all_three_projective_boundary_charts_empty':True,'seconds':time.time()-st}
(o/'shape_roots_checks.json').write_text(json.dumps(report,indent=2)+'\n')
