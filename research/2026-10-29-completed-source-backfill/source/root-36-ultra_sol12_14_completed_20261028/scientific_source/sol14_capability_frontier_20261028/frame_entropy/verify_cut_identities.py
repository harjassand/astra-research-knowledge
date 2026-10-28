"""Formal all-variable identities used by the analytic transport proof.
Dimension scans are deliberately not a premise.
"""
from pathlib import Path
from time import perf_counter
import json
N=3
def const(x):return{(0,)*N:x}if x else{}
def clean(p):return{k:v for k,v in p.items()if v}
def add(p,q):
 r=p.copy()
 for k,v in q.items():r[k]=r.get(k,0)+v
 return clean(r)
def scale(p,c):return clean({k:c*v for k,v in p.items()})
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
 out={}
 for a,x in p.items():
  for b,y in q.items():
   k=tuple(i+j for i,j in zip(a,b));out[k]=out.get(k,0)+x*y
 return clean(out)
def square(p):return mul(p,p)
def main():
 start=perf_counter();d={(1,0,0):1};k={(0,1,0):1};l={(0,0,1):1};one=const(1)
 dp1=add(d,one);a=sub(sub(d,k),l);b=mul(d,mul(k,l))
 v=sub(mul(d,add(k,scale(l,3))),square(add(k,l)))
 A=add(mul(dp1,square(a)),v)
 B=sub(scale(mul(dp1,mul(a,b)),2),mul(v,square(d)))
 C=mul(dp1,square(b))
 discriminant=sub(square(B),scale(mul(A,C),4))
 capacity=mul(mul(k,l),mul(sub(d,k),sub(d,l)))
 bracket=sub(mul(square(d),v),scale(mul(dp1,capacity),4))
 assert discriminant==mul(mul(square(d),v),bracket)
 reciprocal_numerator=add(add(mul(k,sub(d,k)),mul(l,sub(d,l))),scale(mul(l,sub(d,k)),2))
 assert v==reciprocal_numerator
 # The two universal bound remainders, after positive denominators clear.
 # 4(d+1)-3d^2/(d-1)=(d^2-4)/(d-1)>=0 for d>=2.
 first=sub(scale(mul(dp1,sub(d,one)),4),scale(square(d),3))
 assert first==sub(square(d),const(4))
 # 4(d+1)-2d^2/(d-2)=2(d^2-2d-4)/(d-2)>=0 for d>=4.
 second=sub(scale(mul(dp1,sub(d,const(2))),4),scale(square(d),2))
 assert second==scale(sub(sub(square(d),scale(d,2)),const(4)),2)
 n=square(d);nm1=sub(n,one);den=sub(scale(n,2),one)
 assert sub(mul(nm1,square(den)),scale(mul(n,square(nm1)),4))==nm1
 result={'status':'PASS','variables':['d','k','l'],'formal_discriminant_identity':True,
 'formal_reciprocal_identity':True,'dimension_uniform_remainders':['d^2-4','2(d^2-2d-4)'],
 'formal_universal_noise_slack_identity':True,
 'dimension_scan_used_as_premise':False,'seconds':perf_counter()-start}
 path=Path(__file__).resolve().parent/'CUT_IDENTITY_REPLAY.json'
 path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
