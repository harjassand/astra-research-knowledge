from pathlib import Path
from certify import *
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / 'avalanche_boundary_dp'))
from boundary_dp import exhaustive
rng=np.random.RandomState(738)
maxerr=0;cases=0
for n in range(2,11):
 for repeat in range(3):
  s=rng.uniform(size=n);F=Fraction(7*n,40);T=Fraction(3,20);t=Fraction(1,10)
  for m in range(1,n+1):
   p=np.exp(-np.exp(-s/float(T))*float(t)*np.exp(float(F)/(m*float(T))))
   e=sum(exhaustive(s,float(F),p)[:m]);v=below(s,F,T,t,m)
   err=abs(e-float(v.mid));maxerr=max(maxerr,err);cases+=1
print({'exhaustive_cases':cases,'max_absolute_float_discrepancy':maxerr})
