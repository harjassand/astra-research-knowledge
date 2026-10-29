import sympy as s,json,time,sys,hashlib
from pathlib import Path
sys.set_int_max_str_digits(0);root=Path(__file__).parent;src=Path('producer-workspace/quaternion_algebraic_completion_20261029');inp=json.load(open(src/'input.json'));w,x,y,z=s.symbols('w x y z');ss,lam=s.symbols('s lam');qs=[w,x,y,z]
F=sum(s.Rational(c)*s.prod(qs[i]**e[i] for i in range(4)) for e,c in zip(inp['exponents'],inp['perturbed']));f0=s.diff(F,w).subs(w,1);norm=1+x*x+y*y+z*z
p=[s.diff(F,v).subs(w,1)-v*f0 for v in (x,y,z)]+[lam*norm-f0/4];p=[s.Poly(v,x,y,z,lam).primitive()[1].as_expr() for v in p];st=time.time();print('begin normalized4var',flush=True);g=s.groebner(p,x,y,z,lam,order='grevlex',method='f5b');print('grevlex',time.time()-st,len(g.polys),g.is_zero_dimensional,flush=True);assert g.is_zero_dimensional
(root/'grevlex_shape4.json').write_text(json.dumps(dict(polynomials=[str(v.as_expr()) for v in g.polys],seconds=time.time()-st))+'\n');lex=g.fglm(order='lex');print('lex',time.time()-st,len(lex.polys),flush=True)
out=dict(input_sha256=hashlib.sha256((src/'input.json').read_bytes()).hexdigest(),variables=['x','y','z','lam'],source_polynomials=[str(v) for v in p],lex_basis=[str(v.as_expr()) for v in lex.polys],seconds=time.time()-st,scope='Exploratory normalized-eigenvalue primitive element, not a global certificate until exact shape/root/boundary checks complete.')
(root/'lambda_shape4.json').write_text(json.dumps(out,indent=2)+'\n')
