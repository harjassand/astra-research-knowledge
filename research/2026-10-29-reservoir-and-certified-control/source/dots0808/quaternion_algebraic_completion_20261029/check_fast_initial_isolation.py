import sympy as s,json,time,sys
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path(__file__).parent;x,y,z=s.symbols('x y z');shape=json.load(open(r/'shape.json'));U=s.Poly(s.sympify(shape['lex_basis'][2]),z)
st=time.time();ivs=s.polys.polytools.intervals(U,fast=True);assert len(ivs)==28 and all(m==1 for I,m in ivs)
out=dict(seconds=time.time()-st,real_roots=len(ivs),intervals=[[[str(a),str(b)],m] for ((a,b),m) in ivs],scope='Same exact Descartes isolation with fast=True; diagnostic timing, not a new global certificate.')
(r/'fast_initial_isolation.json').write_text(json.dumps(out,indent=2)+'\n');print('completed',out['seconds'],out['real_roots'],flush=True)
