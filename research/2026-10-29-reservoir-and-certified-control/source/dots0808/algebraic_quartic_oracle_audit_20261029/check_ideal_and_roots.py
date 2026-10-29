"""Independent exact finite algebra/real-root completeness check for one supplied bank."""
import sympy as s,json,itertools,time
from pathlib import Path
r=Path('producer-workspace/quaternion_oracle_controller_20261029');o=Path(__file__).parent
w,x,y,z,lam=s.symbols('w x y z lam');qs=[w,x,y,z];bank=json.loads((r/'bank_one_axis.json').read_text());cert=json.loads((r/'oracle_one_axis_edge0.json').read_text());F=sum(t['coefficient']*s.prod(q**e for q,e in zip(qs,t['exponents'])) for t in cert['quartic_coefficients'])
# Independent exact Gröbner method (author used f5b), using saved independently checked bank coefficients.
p=[s.diff(F,v).subs(w,1)-v*s.diff(F,w).subs(w,1) for v in [x,y,z]]
start=time.time();G=s.groebner(p,x,y,z,order='grevlex',method='buchberger');print('own_grevlex',len(G.polys),time.time()-start,flush=True)
lms=[tuple(g.LM(order=G.order).exponents) for g in G.polys]
bounds=[min(e[i] for e in lms if e[i]>0 and all(e[j]==0 for j in range(3) if j!=i)) for i in range(3)]
std=[e for e in itertools.product(*(range(b) for b in bounds)) if not any(all(e[i]>=m[i] for i in range(3)) for m in lms)]
assert len(std)==40
raw=json.loads((r/'critical_chart_result.json').read_text());lex=[s.Poly(s.sympify(t),x,y,z,domain=s.QQ).monic() for t in raw['lex_basis']]
assert [tuple(t.LM(order='lex').exponents) for t in lex]==[(1,0,0),(0,1,0),(0,0,40)]
# Pairwise coprime leading monomials prove this supplied shape list is itself a Groebner basis.
ownlex=G.fglm(order='lex')
assert [p.monic() for p in ownlex.polys]==lex
print('independent_basis_identical',time.time()-start,flush=True)
h=s.Poly(lex[-1].as_expr(),z);_,hint=h.clear_denoms(convert=True)
assert s.gcd(hint,hint.diff()).degree()==0
allroots=s.polys.polytools.intervals(hint,eps=s.Rational(1,10**12));roots=sum(mult for _,mult in allroots)
assert roots==4 and len(allroots)==4
print('all_real_roots',roots,time.time()-start,flush=True)
intervals=json.loads((r/'critical_chart_isolation.json').read_text())['real_intervals'];assert len(intervals)==4
prior=None
for row in intervals:
 a,b=s.Rational(row['a']),s.Rational(row['b']);assert a<b and h.eval(a)!=0 and h.eval(b)!=0
 assert hint.eval(a)*hint.eval(b)<0  # four disjoint sign changes + only four real roots proves exact completeness
 if prior is not None:assert prior<a
 prior=b
missing=[s.diff(F,w).subs(w,0)]+[s.diff(F,v).subs(w,0)-lam*v for v in [x,y,z]]+[x*x+y*y+z*z-1]
GM=s.groebner(missing,x,y,z,lam,order='grevlex',method='buchberger');assert list(GM)==[1];print('missing_chart_excluded',time.time()-start,flush=True)
report={'scope':'One exact bank; independently recomputed Buchberger and FGLM basis and quotient dimension, exact complete real-root isolation plus endpoint signs and disjoint root intervals, missing-chart unit ideal. Software uses SymPy exact rational algebra; not a generic runtime theorem.','critical_quotient_dimension':len(std),'standard_monomials':std,'shape_leading_monomials':[[1,0,0],[0,1,0],[0,0,40]],'independent_Buchberger_FGLM_basis_identical':True,'prior_exact_generator_reductions_also_observed':True,'univariate_squarefree':True,'total_real_roots':int(roots),'all_four_disjoint_intervals_have_one_root':True,'missing_chart_basis':[1],'seconds':time.time()-start}
(o/'ideal_and_roots_checks.json').write_text(json.dumps(report,indent=2)+'\n')
