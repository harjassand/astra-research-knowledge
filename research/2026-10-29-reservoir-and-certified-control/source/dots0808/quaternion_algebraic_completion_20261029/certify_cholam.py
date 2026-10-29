"""Arbitrary-precision rational completion of one perturbed non-SOS instance."""
import sympy as s,json,time,sys,math
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0);root=Path(__file__).parent;inp=json.load(open(root/'input.json'));shape=json.load(open(root/'shape.json'));boundary=json.load(open(root/'boundary.json'));assert all(r['basis']==['1'] for r in boundary['charts'])
x,y,z=s.symbols('x y z');basis=[s.sympify(v) for v in shape['lex_basis']];polyx=s.Poly(basis[0],x,y,z);polyy=s.Poly(basis[1],x,y,z)
assert polyx.degree(x)==1 and polyx.degree(y)==0 and polyy.degree(y)==1 and polyy.degree(x)==0
px=s.Poly(-basis[0].subs(x,0)/polyx.coeff_monomial(x),z);py=s.Poly(-basis[1].subs(y,0)/polyy.coeff_monomial(y),z);uni=s.Poly(basis[2],z);assert uni.degree()==40 and s.gcd(uni,uni.diff()).degree()==0
exps=[tuple(e) for e in inp['exponents']];ff={e:F(v) for e,v in zip(exps,inp['perturbed'])};orig={e:F(v) for e,v in zip(exps,inp['original'])};bias=F(inp['objective_bias_bound']);target=F(inp['target_gap'])
def fq(v):return F(int(v.p),int(v.q))
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
 v=[x*y for x in a for y in b];return min(v),max(v)
def power(a,k):
 if k==0:return F(1),F(1)
 if k%2:return a[0]**k,a[1]**k
 return (F(0) if a[0]<=0<=a[1] else min(a[0]**k,a[1]**k),max(a[0]**k,a[1]**k))
def horner(poly,I):
 v=(F(0),F(0))
 for c in poly.all_coeffs():v=add(mul(v,I),(fq(c),fq(c)))
 return v
def eigenvalue_interval(vs):
 # Euler stationary identity F_unit = partial_0 F(1,u)/(4Q).
 num=(F(0),F(0));den=(F(0),F(0))
 for e,c in ff.items():
  if not e[0]:continue
  ee=list(e);ee[0]-=1;v=(c*e[0],c*e[0])
  for q,k in zip(vs,ee):v=mul(v,power(q,k))
  num=add(num,v)
 for q in vs:den=add(den,power(q,2))
 den=(4*den[0],4*den[1]);assert den[0]>0
 rr=[a/b for a in num for b in den];return min(rr),max(rr)
def candidate(vs,bits):
 m=2**bits;v=[F(1)]+[F(((a+b)/2*m).__floor__(),m) for a,b in vs[1:]];Q=sum(t*t for t in v);rr=F(math.isqrt((Q.numerator*m*m)//Q.denominator),m);u=[t/(rr+1) for t in v[1:]];uu=sum(t*t for t in u);q=[(1-uu)/(1+uu)]+[2*t/(1+uu) for t in u];assert sum(t*t for t in q)==1;return q
def evalf(f,q):return sum(c*math.prod(q[i]**e[i] for i in range(4)) for e,c in f.items())
st=time.time();ivs=s.polys.polytools.intervals(uni);print('real_roots',len(ivs),'isolation_seconds',time.time()-st,flush=True);rows=[];best=None;bestq=None
for ix,((a,b),mult) in enumerate(ivs):
 assert mult==1;bits=64
 while True:
  a,b=s.polys.polytools.refine_root(uni,a,b,eps=s.Rational(1,2**bits));zz=(fq(a),fq(b));xx=horner(px,zz);yy=horner(py,zz);vs=[(F(1),F(1)),xx,yy,zz];lo,hi=eigenvalue_interval(vs)
  if hi-lo<=target/16:break
  bits*=2
  if bits>8192:raise RuntimeError('declared exploratory precision cap reached, no global certificate')
 qr=candidate(vs,bits);val=evalf(orig,qr)
 if best is None or val<best:best,bestq=val,qr
 rows.append(dict(index=ix,z_interval=[str(a),str(b)],precision_bits=bits,perturbed_value_interval=[str(lo),str(hi)],original_candidate_value=str(val),value_float=[float(lo),float(hi)]))
 print('root',ix,'bits',bits,'value',float(lo),float(hi),'seconds',time.time()-st,flush=True)
low=min(F(r['perturbed_value_interval'][0]) for r in rows)-bias;gap=best-low;assert 0<=gap<=target
out=dict(real_stationary_rays=len(rows),squarefree_degree=uni.degree(),projective_boundary_excluded=True,root_records=rows,original_global_lower=str(low),original_rational_upper=str(best),original_global_gap=str(gap),gap_float=float(gap),rational_unit_quaternion=[str(q) for q in bestq],objective_perturbation_budget=str(bias),requested_gap=str(target),seconds=time.time()-st,scope='One exact rational perturbed Choi-Lam global certificate with all critical roots. Original minimum0 independently known byAMGM. No generic success probability/bit-runtime theorem is asserted.')
(root/'global_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print('GLOBAL_CERTIFICATE',float(gap),'seconds',time.time()-st,flush=True)
