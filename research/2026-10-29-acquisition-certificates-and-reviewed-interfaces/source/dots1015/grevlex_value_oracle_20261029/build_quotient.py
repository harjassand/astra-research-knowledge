import sympy as s,json,time,itertools,sys
from pathlib import Path
sys.set_int_max_str_digits(0)
P=Path(__file__).parent;src=P/'received';inp=json.loads((src/'input.json').read_text());q=s.symbols('w x y z');w,x,y,z=q
F=sum(s.Rational(c)*s.prod(a**b for a,b in zip(q,e)) for e,c in zip(inp['exponents'],inp['perturbed']));f0=s.diff(F,w).subs(w,1)
eq=[s.Poly(s.diff(F,a).subs(w,1)-a*f0,x,y,z).primitive()[1].as_expr() for a in [x,y,z]]
st=time.time();g=s.groebner(eq,x,y,z,order='grevlex',method='f5b');print('basis',time.time()-st,flush=True)
lm=[tuple(p.LM(order=g.order).exponents) for p in g.polys]
basis=[]
for degree in range(20):
 level=[e for e in itertools.product(range(degree+1),repeat=3) if sum(e)==degree and not any(all(a>=b for a,b in zip(e,l)) for l in lm)]
 if not level:break
 basis.extend(level)
assert len(basis)==40; print('standard',basis,flush=True)
mons=[x**e[0]*y**e[1]*z**e[2] for e in basis]
matrices=[]
for a in [x,y,z]:
 cols=[]
 for mon in mons:
  rem=s.Poly(g.reduce(a*mon)[1],x,y,z);cols.append([str(rem.coeff_monomial(m)) for m in mons])
 matrices.append(cols)
 print('matrix',a,time.time()-st,flush=True)
out={'seconds':time.time()-st,'basis':basis,'grevlex':[str(p.as_expr()) for p in g.polys],'multiplication_columns':matrices,'f0_terms':[[list(e),str(c)] for e,c in s.Poly(f0,x,y,z).terms()]}
(P/'quotient.json').write_text(json.dumps(out,indent=2)+'\n')

boundary=[];bst=time.time()
for pivot in [1,2,3]:
 free=[a for i,a in enumerate(q) if i not in [0,pivot]];subs={w:0,q[pivot]:1};dp=s.diff(F,q[pivot]).subs(subs)
 eq=[s.diff(F,w).subs(subs)]+[s.diff(F,a).subs(subs)-a*dp for a in free]
 gb=s.groebner(eq,*free,order='grevlex',method='f5b');assert list(gb)==[1];boundary.append({'pivot':pivot,'basis':[str(a) for a in gb]})
(P/'boundary.json').write_text(json.dumps({'seconds':time.time()-bst,'charts':boundary},indent=2)+'\n')
