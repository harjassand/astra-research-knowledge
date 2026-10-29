import sympy as s,itertools,json,math,time
from pathlib import Path
st=time.time();q=s.symbols('w x y z');w,x,y,z=q;R=[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y),2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x),2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]
exps=[e for e in itertools.product(range(5),repeat=4) if sum(e)==4];polys=[s.Poly(a*b,*q) for a in R for b in R];M=s.Matrix([[p.coeff_monomial(e) for p in polys] for e in exps]);print('rank',M.rank(),flush=True);B=(M*M.T).inv()*M;assert B*M.T==s.eye(35)
mult=[math.factorial(4)//math.prod(math.factorial(v) for v in e) for e in exps];W=s.diag(*mult);F=B.T*W*B
print('eigenvalues',F.eigenvals(),flush=True)
root=Path(__file__).parent;ev=F.eigenvals();root.joinpath('certificate.json').write_text(json.dumps(dict(exponents=exps,multiplicities=mult,B=[[str(v) for v in row] for row in B.tolist()],eigenvalues={str(v):m for v,m in ev.items()},verified_left_inverse=True,seconds=time.time()-st),indent=2)+'\n')
