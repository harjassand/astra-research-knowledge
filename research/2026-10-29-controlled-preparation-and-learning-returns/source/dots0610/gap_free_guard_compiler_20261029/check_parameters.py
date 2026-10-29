from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,hashlib

def ceil_fourth(x):
 lo,hi=0,1
 while hi**4<x:hi*=2
 while lo+1<hi:
  mid=(lo+hi)//2
  if mid**4>=x:hi=mid
  else:lo=mid
 return hi
rows=[]
for h in [5,8,12,20,40,60,80,100]:
 B=2**h;n=4*h;T=9*B;p=F(1,3);C=F(n+2,n-1);s=(1-p)/(C+1);a=C*s
 assert p+s+a==1 and C*s/a==1 and T*s>=2*B
 t=B//8;b=B//32;N=t+b+1
 assert F((t-b+1)**2,2*N)>=F(3*B,128)
 m=ceil_fourth(625*T);eps=F(5,m);M=(2*m+1)**3;k=M.bit_length()
 assert m**4>=625*T and (m-1)**4<625*T
 eta=F(1)
 while eta>p/2 or eta*eta>p*k/T:eta/=2
 L=F(9,2)*eps*eps*T+45*(k/eta+eta*T/p)
 d=comb(n,n//2)//(n//2+1);A=F(2**n,d)
 fail=a*A*(n-1)*L/(b+1)
 fault=s*A*(n-1)*L/(t+1)
 rows.append(dict(h=h,n=n,B=str(B),T=str(T),net_m=m,net_size=str(M),eta=str(eta),
  source_roles=[str(p),str(s),str(a)],A_n=str(A),loss_upper=str(L),
  validation_abort_upper_exact=str(fail),validation_abort_upper_float=float(fail),
  virtual_uncorrectable_upper_float=float(fault),payload_exposure_ratio=str(F(h*(B-4*t),n*T))))
out={'scope':'Exact rational finite parameter certificates; no physical simulation or all-size learner execution. ln M upper bounded by bit_length(M). Source size n scales with B, not fixed-port capacity.','rows':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows: print(r['h'],r['validation_abort_upper_float'],r['payload_exposure_ratio'])
