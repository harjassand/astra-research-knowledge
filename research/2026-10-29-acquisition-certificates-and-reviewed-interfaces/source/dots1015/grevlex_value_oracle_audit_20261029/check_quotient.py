import sympy as s,json,sys,itertools,math,time
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path('producer-workspace/grevlex_value_oracle_20261029');o=Path(__file__).parent
j=json.loads((r/'received/input.json').read_text());a=json.loads((r/'quotient.json').read_text());q=s.symbols('w x y z');w,x,y,z=q
f=sum(s.Rational(c)*math.prod(t**e for t,e in zip(q,ex)) for ex,c in zip(j['exponents'],j['perturbed']));f0=s.diff(f,w).subs(w,1);eq=[s.diff(f,t).subs(w,1)-t*f0 for t in q[1:]];st=time.time();g=s.groebner(eq,*q[1:],order='grevlex',method='buchberger');assert len(g.polys)==len(a['grevlex']); assert all(s.Poly(p,*q[1:],domain=s.QQ).monic()==s.Poly(t,*q[1:],domain=s.QQ).monic() for p,t in zip(g.polys,a['grevlex']))
lm=[p.LM(order='grevlex').exponents for p in g.polys];basis=[]
for degree in range(40):
 level=[e for e in itertools.product(range(degree+1),repeat=3) if sum(e)==degree and not any(all(i>=k for i,k in zip(e,l)) for l in lm)]
 if not level:break
 basis+=level
else:raise AssertionError('no empty standard level')
assert list(map(list,basis))==a['basis'];assert len(basis)==40;mons=[math.prod(v**e for v,e in zip(q[1:],ex)) for ex in basis]
for i,t in enumerate(q[1:]):
 for col,mon in enumerate(mons):
  rem=g.reduce(t*mon)[1];stored=sum(s.Rational(c)*m for c,m in zip(a['multiplication_columns'][i][col],mons));assert s.expand(rem-stored)==0
boundaries=[]
for pivot in range(1,4):
 subs={w:0,q[pivot]:1};free=[q[k] for k in range(1,4) if k!=pivot];dp=s.diff(f,q[pivot]).subs(subs)
 gg=s.groebner([s.diff(f,w).subs(subs)]+[s.diff(f,t).subs(subs)-t*dp for t in free],*free,method='buchberger');assert list(gg)==[1];boundaries.append(pivot)
c=json.loads((r/'candidate.json').read_text());ints=list(map(int,c['integer_coefficients_low_to_high']));frac=list(map(F,c['monic_coefficients_low_to_high']));assert len(ints)==len(frac)==41 and frac[-1]==1 and ints[-1]>0 and math.gcd(*ints)==1;assert all(F(v,ints[-1])==u for v,u in zip(ints,frac))
res={'independent_buchberger_basis_matches':True,'standard_basis_dimension':40,'empty_level':degree,'all120_exact_remainders_match':True,'boundary_charts':boundaries,'candidate_primitive_consistency':True,'seconds':time.time()-st}
(o/'quotient_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
