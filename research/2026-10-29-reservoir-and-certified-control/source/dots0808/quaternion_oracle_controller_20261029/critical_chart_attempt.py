"""Bounded exploratory exact critical-chart computation; no oracle success without roots."""
import sympy as s,json,time
from pathlib import Path
from quartic_sos_oracle import bank_polynomial
root=Path(__file__).parent;bank=json.load(open(root/'bank_one_axis.json'));f=bank_polynomial(bank,0);q=s.symbols('w x y z');F=sum(c*s.prod(q[i]**e[i] for i in range(4)) for e,c in f.items());u=q[1:];f0=s.diff(F,q[0]).subs(q[0],1)
polys=[s.Poly(s.diff(F,q[i]).subs(q[0],1)-q[i]*f0,*u).primitive()[1].as_expr() for i in range(1,4)]
print('start_exact_chart',len(polys),[s.total_degree(p) for p in polys],flush=True);st=time.time()
g=s.groebner(polys,*u,order='grevlex',method='f5b');print('grevlex_done',time.time()-st,'basis',len(g.polys),'zero_dim',g.is_zero_dimensional,flush=True)
lex=g.fglm(order='lex');print('fglm_done',time.time()-st,'basis',len(lex.polys),flush=True)
(root/'critical_chart_result.json').write_text(json.dumps(dict(seconds=time.time()-st,grevlex_basis_size=len(g.polys),lex_basis=[str(p.as_expr()) for p in lex.polys],scope='One projective chart only; no global root-isolation/candidate certificate yet.'),indent=2)+'\n')
