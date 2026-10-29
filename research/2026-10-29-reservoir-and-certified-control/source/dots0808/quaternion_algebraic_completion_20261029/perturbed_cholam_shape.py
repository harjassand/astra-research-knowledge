"""Concrete all-coefficient rational perturbation; no generic runtime theorem assumed."""
import sympy as s,json,time,random,sys
from pathlib import Path
from fractions import Fraction as Q
sys.set_int_max_str_digits(0)
root=Path(__file__).parent;qs=s.symbols('w x y z');w,x,y,z=qs
exps=[(a,b,c,4-a-b-c) for a in range(5) for b in range(5-a) for c in range(5-a-b)]
orig={e:Q(0) for e in exps}
for e in [(2,2,0,0),(0,2,2,0),(2,0,2,0),(0,0,0,4)]:orig[e]=Q(1)
orig[(1,1,1,1)]=Q(-4)
eps=Q(1,10000);M=64;rng=random.Random(2026102909);pert={e:eps*Q(rng.randint(-M,M),140*M) for e in exps};ff={e:orig[e]+pert[e] for e in exps};budget=sum(abs(v) for v in pert.values());assert budget<=eps/4
F=sum(s.Rational(c.numerator,c.denominator)*s.prod(qs[i]**e[i] for i in range(4)) for e,c in ff.items())
(root/'input.json').write_text(json.dumps(dict(exponents=exps,original=[str(orig[e]) for e in exps],perturbation=[str(pert[e]) for e in exps],perturbed=[str(ff[e]) for e in exps],objective_bias_bound=str(budget),target_gap=str(eps),scope='One seeded rational perturbation trial; no uniform generic-success probability claimed.'),indent=2)+'\n')
st=time.time();f0=s.diff(F,w).subs(w,1);p=[s.Poly(s.diff(F,v).subs(w,1)-v*f0,x,y,z).primitive()[1].as_expr() for v in (x,y,z)]
print('begin',flush=True);g=s.groebner(p,x,y,z,order='grevlex',method='f5b');print('grevlex',time.time()-st,len(g.polys),g.is_zero_dimensional,flush=True)
assert g.is_zero_dimensional
lex=g.fglm(order='lex');print('lex',time.time()-st,len(lex.polys),flush=True)
(root/'shape.json').write_text(json.dumps(dict(seconds=time.time()-st,lex_basis=[str(p.as_expr()) for p in lex.polys]),indent=2)+'\n')
# Cover all projective boundary charts, stronger than only normalized real sphere.
boundary=[]
for pivot in [1,2,3]:
 free=[v for i,v in enumerate(qs) if i not in [0,pivot]];subs={w:0,qs[pivot]:1};dp=s.diff(F,qs[pivot]).subs(subs)
 eq=[s.diff(F,w).subs(subs)]+[s.diff(F,v).subs(subs)-v*dp for v in free]
 gb=s.groebner(eq,*free,order='grevlex',method='f5b');assert list(gb)==[1];boundary.append(dict(pivot=pivot,basis=[str(v) for v in gb]))
print('all_projective_boundary_excluded',time.time()-st,flush=True);(root/'boundary.json').write_text(json.dumps(dict(seconds=time.time()-st,charts=boundary),indent=2)+'\n')
