"""Finite diagnostics; analytical proof does not follow from these tests."""
import json, math
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
lam=F(1)
count=0
for kap in [F(1,2),F(1),F(2),F(4)]:
    for a in range(41):
        for b in range(41):
            W=lambda a,b:a-b//2
            val=lam*(W(a,b+1)-W(a,b))
            if b: val+=lam*b*(W(a+1,b-1)-W(a,b))
            if a and b>=2: val+=kap*a*b*(b-1)*(W(a-1,b-2)-W(a,b))
            p=b%2
            want=lam*(b-p)*(F(3,2)+F((-1)**p,2))
            assert val==want and val>=0
            if a and b>=2: assert W(a-1,b-2)==W(a,b)
            count+=1
# Killed excursion kernel exponential estimate uses r=sqrt(2), q=2sqrt(2)/3.
r=math.sqrt(2);q=2*r/3
kernel_count=0
for kap in [.1,1.,2.,4.,100.]:
    for a in range(31):
        for b in range(1,61):
            den=1+b+kap*a*b*(b-1)
            val=r/den
            if b>1: val+=b/den/r
            if b>2: val+=kap*a*b*(b-1)/den/r**2
            assert val <= q+1e-14
            kernel_count+=1
# Enumerate a finite event excursion, retain rigorous form of a geometric
# remainder bound. Values are floating diagnostics, not interval certificates.
results=[]
for kap in [1.,2.,4.]:
  for n in [10,100,1000,10000]:
    states={(n,1):1.}; m1=m2=mass=0.;L=45
    for j in range(L):
      new={}
      for (a,b),p in states.items():
        total=1+b+kap*a*b*(b-1)
        for aa,bb,rate in [(a,b+1,1.),(a+1,b-1,float(b)),(a-1,b-2,kap*a*b*(b-1))]:
          if not rate: continue
          v=p*rate/total
          if bb==0:
            d=aa-n;m1+=v*d;m2+=v*d*d;mass+=v
          else:new[(aa,bb)]=new.get((aa,bb),0.)+v
      states=new
    pleft=sum(states.values());vleft=sum(p*r**(b-1) for (a,b),p in states.items())
    err1=L*pleft+vleft/(1-q)
    err2=2*L*L*pleft+2*vleft*(1+q)/(1-q)**2
    results.append({'kappa':kap,'n':n,'mean':m1,'n_mean':n*m1,'target_n_mean':1/kap,'second_moment':m2,'mean_tail_bound_form':err1,'second_tail_bound_form':err2,'unfinished_probability':pleft})
out={'status':'finite diagnostic only; float arithmetic for excursion enumeration','exact_generator_fixtures':count,'kernel_fixtures':kernel_count,'q':q,'excursion_results':results}
(ROOT/'results'/'verification.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
