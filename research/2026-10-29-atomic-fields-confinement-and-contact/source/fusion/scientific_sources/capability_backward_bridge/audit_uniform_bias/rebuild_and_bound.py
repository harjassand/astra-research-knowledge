"""Independent source-map/cofactor rebuild and exact Bernstein coefficient bounds.
Reads root snapshot; writes only this worker's owned audit directory.
"""
from pathlib import Path
import sys,json,time,importlib.util
sys.path.insert(0,str(Path(__file__).parents[1]/'code/vendor'))
import sympy as s
from fractions import Fraction as F
from math import comb
start=time.time();here=Path(__file__).parent
parent=here/'source_snapshot'
z=s.symbols('z',nonzero=True);a=s.symbols('a',positive=True,real=True);b=s.symbols('b',real=True)
I=s.I;u=a*(z+1/z)/2;v=a*(z-1/z)/(2*I);l=a*a;d=1+l
gamma=(l-1)/d;kcoef=4*l/d**2
k=b-(gamma+kcoef)*u+(2*gamma+kcoef)*u*v;ell=v+u*u-v*v
X=s.Matrix([2*(u*k-v*ell)/d,2*(v*k+u*ell)/d,gamma*b+kcoef*((1-gamma)*u-(2-gamma)*u*v)]).applyfunc(s.cancel)
spec=importlib.util.spec_from_file_location('root_source_geometry',parent/'source_geometry.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
zr,ar,br,Xr=mod.geometry();Xr=Xr.subs({zr:z,ar:a,br:b})
assert all(s.cancel(x-y)==0 for x,y in zip(X,Xr))
phi=lambda q:s.diff(q,z)*I*z
lam=lambda q:s.diff(q,a)/(2*a)
Xp=X.applyfunc(phi);Xl=X.applyfunc(lam);Xb=X.diff(b)
gl=s.cancel(2*l*(Xb.cross(Xp))[1]);gb=s.cancel(2*l*(Xp.cross(Xl))[1]);gp=s.cancel(Xp[1])
def fourier(q):
 p=s.Poly(s.cancel(q*z**12),z)
 return {k[0]-12:s.cancel(c) for k,c in p.terms() if c!=0}
fl,fb,fp=map(fourier,[gl,gb,gp]);G=-8*a**6*(9-a*a+a**4-a**6)/(1+a*a)**7
assert fl.get(0,0)==0 and s.cancel(fb[0]-G)==0
chi={k:s.cancel(-c/(I*k)) for k,c in fb.items() if k}
assert all(s.cancel(chi[-k]-s.conjugate(c))==0 for k,c in chi.items())
assert all(s.cancel(I*k*c+fb[k])==0 for k,c in chi.items())
ref=json.loads((parent/'AVERAGING_RESULT.json').read_text())
for k,c in chi.items():assert s.cancel(c-s.sympify(ref['corrector_fourier'][str(k)],locals={'a':a,'b':b,'I':I}))==0
print('Independent rational-map, cofactor, mean and real corrector reconstruction PASS.',flush=True)
# Independent bound: exact bivariate Bernstein convex hull, rather than the
# producer's recursive interval-expression evaluator. Beta has no sign assumption.
t,w=s.symbols('t w',real=True)
def frac(q):return F(int(q.p),int(q.q))
def bernstein_range(poly,abox,bbox):
 aa0,aa1=[s.Rational(q.numerator,q.denominator) for q in abox]
 bb0,bb1=[s.Rational(q.numerator,q.denominator) for q in bbox]
 pp=s.Poly(s.expand(poly.subs({a:aa0+(aa1-aa0)*t,b:bb0+(bb1-bb0)*w})),t,w)
 if pp.is_zero:return F(0),F(0)
 n,m=map(int,[pp.degree(t),pp.degree(w)]);terms=[(i,j,frac(c)) for (i,j),c in pp.terms()]
 vals=[]
 for i in range(n+1):
  for j in range(m+1):
   vals.append(sum((c*F(comb(i,p),comb(n,p))*F(comb(j,q),comb(m,q)) for p,q,c in terms if p<=i and q<=j),F(0)))
 return min(vals),max(vals)

def real_bound(expr,parts=1):
 expr=s.cancel(expr)
 if expr==0:return F(0)
 num,den=s.fraction(expr);bound=F(0)
 for i in range(parts):
  for j in range(parts):
   ab=(F(1,3)+F(i,6*parts),F(1,3)+F(i+1,6*parts))
   bb=(-F(2,25)+F(j,5*parts),-F(2,25)+F(j+1,5*parts))
   nl,nh=bernstein_range(num,ab,bb);dl,dh=bernstein_range(den,ab,bb)
   if dh<0:nl,nh,dl,dh=-nh,-nl,-dh,-dl
   assert dl>0,(expr,dl,dh)
   bound=max(bound,max(abs(nl),abs(nh))/dl)
 return bound

def coefficient_bound(q,parts=1):
 re,im=s.expand_complex(q).as_real_imag()
 return real_bound(re,parts)+real_bound(im,parts)
def norm(q,parts=1):return sum((coefficient_bound(c,parts) for c in q.values()),F(0))
dicts={'gl':fl,'gb':fb,'gp':fp,'chi':chi,'chi_lambda':{k:lam(c) for k,c in chi.items()},'chi_beta':{k:s.diff(c,b) for k,c in chi.items()}}
C={k:norm(q) for k,q in dicts.items()}
m=F(8)*F(1,3)**6*(F(9)-F(1,4)-F(1,64))/(1+F(1,4))**7
M=C['chi_lambda']*C['gl']+C['chi_beta']*C['gb']+C['gb']*C['gp']
delta=F(ref['positive_delta_max'])
assert 1-delta*C['gp']>0
# Use the exact denominator bound, rather than weaken it to1/2.
margin=m-delta*M/(1-delta*C['gp'])
assert margin>0,(float(m),float(M),float(delta),float(margin))
out={'status':'PASS','scope':'Independent audit of source-specific all-fieldline finite-exit theorem, conditional on primary global embedding. No general coil/confinement no-go.','source_map_rebuild':'Pinned rational forward map, unrestricted real beta, matches producer Laurent map exactly.','identities':['physical cofactor equations','negative exact mean drift','real globally periodic corrector','corrector coefficients match producer snapshot'],'independent_bound_method':'Exact bivariate Bernstein convex-hull coefficients on a∈[1/3,1/2],beta∈[-2/25,3/25].','bounds':{k:str(v) for k,v in C.items()},'m':str(m),'M':str(M),'tested_delta_max':str(delta),'clock_numerator_lower':str(1-delta*C['gp']),'corrected_drift_magnitude_lower_per_delta':str(margin),'producer_bounds_dominate_independent':{k:C[k]<=F(ref['bounds'][k]) for k in C},'seconds':time.time()-start}
(here/'AUDIT_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
