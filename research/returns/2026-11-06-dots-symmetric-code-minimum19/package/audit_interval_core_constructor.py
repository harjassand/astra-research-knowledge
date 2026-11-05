from pathlib import Path
from fractions import Fraction as F
import importlib.util,random,math,json,numpy as np
p=Path(__file__).resolve().parent/'audit_residual'/'verify_interval_dual.py'
spec=importlib.util.spec_from_file_location('verifier',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def encl(B,x):
 x=F(x);return F(int(B.m.item()-B.r.item()),m.Q)<=x<=F(int(B.m.item()+B.r.item()),m.Q)
rng=random.Random(20261105);count=0
for _ in range(1000):
 x=F(rng.randrange(-10**15,10**15),rng.randrange(1,10**12));y=F(rng.randrange(-10**15,10**15),rng.randrange(1,10**12));a=m.B.exact(x);b=m.B.exact(y)
 for z,q in [(a+b,x+y),(a-b,x-y),(a*b,x*y)]:assert encl(z,q);count+=1
 z=m.bsqrt(abs(x));lo=F(int(z.m-z.r),m.Q);hi=F(int(z.m+z.r),m.Q);assert lo<=0 or lo*lo<=abs(x);assert hi*hi>=abs(x);count+=1
for _ in range(100):
 a=[[F(rng.randrange(-1000,1000),rng.randrange(1,1000))for j in range(3)]for i in range(3)];b=[[F(rng.randrange(-1000,1000),rng.randrange(1,1000))for j in range(3)]for i in range(3)];c=m.B.exact(a)@m.B.exact(b)
 for i in range(3):
  for j in range(3):assert encl(c[i,j],sum(a[i][k]*b[k][j]for k in range(3)));count+=1
out={'status':'PASS','independent_rational_comparisons':count,'precision_bits':m.PREC,'note':'Additional constructor-side unit tests only; not a substitute for independent mathematical review.'};(p.parent/'constructor_core_unit_tests.json').write_text(json.dumps(out,indent=2));print(out)
