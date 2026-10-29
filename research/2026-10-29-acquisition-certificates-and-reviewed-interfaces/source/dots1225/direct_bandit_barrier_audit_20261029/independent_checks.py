from fractions import Fraction as F
import sys,json,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'replay'))
from barrier_sampler import distribution,update
rng=random.Random(83179);cases=0
for M in [1,2,3,7,19]:
 for T in [1,2,13,100]:
  for rho in [F(1),F(1,17),F(3,1000)]:
   L=[F(rng.randrange(10**8),rng.randrange(1,10**4)) for _ in range(M)]
   q,d=distribution(L,rho/4,T);D=d['D'];W=d['total'];lo=F(d['root_lower']);hi=F(d['root_upper']);c=[rho/4*(x-min(L)) for x in L]
   pl=[1/(x+hi) for x in c];pu=[1/(x+lo) for x in c]
   assert sum(pl)<=1<=sum(pu)
   assert sum(q)==1 and all(x>0 for x in q)
   assert all(qi>=F(D,D+2*M)*upi for qi,upi in zip(q,pu))
   assert all(qi>=F(2,D+2*M) for qi in q)
   # Exact Bernoulli event enumeration, including nonobservation and zero flips.
   ell=[F(rng.randrange(13),12) for _ in q]
   mean=[F(0) for _ in q]
   for j in range(M):
    probability=rho*q[j]*ell[j]
    inc=update([0]*M,j,1,q,rho)
    for k in range(M):mean[k]+=probability*inc[k]
   assert mean==ell
   # Finite capped rejection: count/index independence conditional on success.
   bits=(W-1).bit_length();B=2**bits;r=F(B-W,B);K=4
   joint=[[r**(a-1)*F(w,B) for w in d['weights']] for a in range(1,K+1)]
   success=1-r**K
   assert all(sum(row[j] for row in joint)==success*q[j] for j in range(M))
   assert r**K<=F(1,2**K)
   cases+=1
out={'independent_exact_cases':cases,'checks':['root bracketing','rational normalization','interval-certified domination','positive floors','Bernoulli importance unbiasedness','cap/index independence'],'scope':'Exact arithmetic mathematical diagnostics; no physical execution'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
