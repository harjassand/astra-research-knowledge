import sympy as s,json,time,sys
from pathlib import Path
sys.set_int_max_str_digits(0);r=Path(__file__).parent;j=json.load(open(r/'input.json'));q=s.symbols('w x y z');w,x,y,z=q
F=sum(s.Rational(c)*s.prod(q[i]**e[i] for i in range(4)) for e,c in zip(j['exponents'],j['perturbed']))
d=[s.diff(F,v).subs(w,0) for v in q];eq=[d[0],x*d[2]-y*d[1],x*d[3]-z*d[1]];out=[];st=time.time()
for pivot in (x,y,z):
 free=[v for v in (x,y,z) if v!=pivot];g=s.groebner([v.subs(pivot,1) for v in eq],*free,order='grevlex',method='f5b');assert list(g)==[1];out.append({'pivot':str(pivot),'basis':[str(v) for v in g]});print(str(pivot),time.time()-st,flush=True)
(r/'resultant_boundary_witness.json').write_text(json.dumps({'charts':out,'seconds':time.time()-st,'scope':'Concrete exact nonzero witness for ternary degree3,4,4 boundary resultant on quartic-gradient coefficient space.'},indent=2)+'\n')
