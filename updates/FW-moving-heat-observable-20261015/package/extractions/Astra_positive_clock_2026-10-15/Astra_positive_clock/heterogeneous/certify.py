from pathlib import Path
import json,time,math
from fractions import Fraction
import numpy as np
p=str(Path(__file__).resolve().parent)+'/'
j=json.load(open(p+'dyadic128_exact.json'));keys=[int(v) for v in j['rates']];counts=[int(c) for c in j['counts']];n=j['n'];data=np.load(p+'dyadic128_float.npz');roots=data['r'];D=2**80;P=n+100;S=2**P;W=2**80

def sign(a):
 lo=sum((a*c*S)//(k*D-a) for k,c in zip(keys,counts))
 if lo> S:return -1
 if lo+len(keys)< S:return 1
 return 0

def weight_bounds(a,b):
 low=0;high=0
 for k,c in zip(keys,counts):
  da=k*D-a;db=k*D-b
  if da*db<=0:raise ValueError('pole in root bracket')
  maxdist=max(da*da,db*db);mindist=min(da*da,db*db)
  low+=(a*D*c*k*S)//maxdist
  high+=(b*D*c*k*S)//mindist+1
 return (S*W)//high,(S*W+low-1)//low

t=time.perf_counter();rows=[];sumlo=0;sumhi=0
for idx,r in enumerate(roots):
 rat=Fraction(float(r))*keys[0]*D;center=rat.numerator//rat.denominator
 poleidx=int(np.searchsorted(data['x'],r));left=0 if poleidx==0 else keys[poleidx-1]*D;right=keys[poleidx]*D
 width=max(1,center//10**11)
 for _ in range(30):
  a=max(left+1,center-width);b=min(right-1,center+width)
  if sign(a)==1 and sign(b)==-1:break
  width*=4
 else:raise RuntimeError('no bracket')
 # Tighten until the probability enclosure is <=1e-9.
 for _ in range(80):
  lo,hi=weight_bounds(a,b)
  if hi-lo<W//10**12:break
  mid=(a+b)//2;s=sign(mid)
  if s>0:a=mid
  elif s<0:b=mid
  else:raise RuntimeError('precision insufficient')
 sumlo+=lo;sumhi+=hi
 rows.append(dict(root_index=poleidx,lower_numerator=str(a),upper_numerator=str(b),weight_lower_numerator=str(lo),weight_upper_numerator=str(hi)))
 if (W-sumlo)*2**n-W < W*2**n//2000000:break
 if idx%25==0:print(idx,'mass',sumlo/W,'seconds',time.perf_counter()-t,flush=True)
out=dict(n=n,root_denominator=str(D),weight_denominator=str(W),evaluation_precision=P,certified_roots=len(rows),mass_lower=sumlo/W,mass_upper=sumhi/W,omitted_mass_upper=1-2.**-n-sumlo/W,seconds=time.perf_counter()-t,intervals=rows)
json.dump(out,open(p+'mixture_certificate.json','w'),indent=2);print({k:v for k,v in out.items() if k!='intervals'})
