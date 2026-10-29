from fractions import Fraction as F
from pathlib import Path
import json,random
import mpmath as mp
from barrier_sampler import distribution,update
mp.mp.dps=70;rng=random.Random(202610290957);cases=[]
for M in range(1,9):
 for T in [1,2,17,120]:
  rho=F(1,3*M);eta=rho/4;L=[F(rng.randrange(10000),rng.randrange(1,100)) for _ in range(M)]
  for step in range(10):
   q,cert=distribution(L,eta,T);lo=mp.mpf(cert['root_lower'].split('/')[0]);
   def cv(x):return mp.mpf(x.numerator)/x.denominator
   c=[eta*(x-min(L)) for x in L];a=mp.mpf(1);b=mp.mpf(M)
   for _ in range(260):
    mid=(a+b)/2
    if sum(1/(cv(x)+mid) for x in c)>1:a=mid
    else:b=mid
   p=[1/(cv(x)+(a+b)/2) for x in c];D=cert['D'];ratios=[cv(qi)/pi for qi,pi in zip(q,p)]
   assert min(ratios)>=mp.mpf(D)/(D+2*M)-mp.mpf('1e-60')
   tv=sum(abs(cv(qi)-pi) for qi,pi in zip(q,p))/2
   assert tv<=mp.mpf(2*M)/(D+2*M)+mp.mpf('1e-60')
   arm=rng.randrange(M);oldp=p;oldL=L;L=update(L,arm,1,q,rho)
   qn,cn=distribution(L,eta,T)
   # Recompute exact ideal next root numerically solely for diagnostic stability.
   cc=[eta*(x-min(L)) for x in L];a=mp.mpf(1);b=mp.mpf(M)
   for _ in range(260):
    mid=(a+b)/2
    if sum(1/(cv(x)+mid) for x in cc)>1:a=mid
    else:b=mid
   pn=[1/(cv(x)+(a+b)/2) for x in cc];g=cv(F(1)/(rho*q[arm]));st=(oldp[arm]-pn[arm])*g;bound=cv(eta)*oldp[arm]**2*g*g
   assert st<=bound+mp.mpf('1e-55') and st>=-mp.mpf('1e-55')
   cases.append(dict(M=M,T=T,minimum_ratio=float(min(ratios)),TV=float(tv),stability=float(st),stability_upper=float(bound),stored_max_bits=max(max(x.numerator.bit_length(),x.denominator.bit_length()) for x in L)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Exact rational sampler plus high-precision diagnostic of ideal normalization and stability; proof governs',cases=len(cases),max_stored_bits=max(x['stored_max_bits'] for x in cases),results=cases),indent=2)+'\n');print(len(cases))
