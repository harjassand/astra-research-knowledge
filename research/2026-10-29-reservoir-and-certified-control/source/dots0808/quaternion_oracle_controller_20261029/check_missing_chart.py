import sympy as s,json,time
from pathlib import Path
from quartic_sos_oracle import bank_polynomial
root=Path(__file__).parent;f=bank_polynomial(json.load(open(root/'bank_one_axis.json')),0);w,x,y,z,l=s.symbols('w x y z l');qs=(w,x,y,z);F=sum(c*s.prod(qs[i]**e[i] for i in range(4)) for e,c in f.items())
p=[s.diff(F,w).subs(w,0)]+[s.diff(F,v).subs(w,0)-l*v for v in (x,y,z)]+[x*x+y*y+z*z-1]
st=time.time();g=s.groebner(p,x,y,z,l,order='grevlex',method='f5b');result=dict(seconds=time.time()-st,basis=[str(a.as_expr()) for a in g.polys],no_missing_stationary_point=(list(g)==[1]),scope='Exact Groebner computation for q0=0 sphere stationary system. Independent recomputation/certificate needed for a full checked algebraic solver.')
(root/'missing_chart_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
