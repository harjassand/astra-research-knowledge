from pathlib import Path
import math,time,json
from fractions import Fraction
import numpy as np
from scipy.optimize import brentq

def floor_rate(frac,b):
 num,den=frac.numerator,frac.denominator;e=num.bit_length()-den.bit_length()
 if (num < (den<<e) if e>=0 else (num<<(-e))<den):e-=1
 shift=b-1-e
 m=(num<<shift)//den if shift>=0 else num//(den<<(-shift))
 return m,shift

def compile_hist(n,eps):
 b=math.ceil(1+math.log2((n+1)/math.log1p(eps)))
 native=[Fraction(10*n+i,10*n*5**i) for i in range(n)]
 rr=[floor_rate(v,b) for v in native];shift=max(s for m,s in rr);rates=[m<<(shift-s) for m,s in rr];d={0:1}
 for r in rates[::-1]:
  new=d.copy()
  for a,c in d.items():
   v=a+r;drop=max(0,v.bit_length()-b);v=(v>>drop)<<drop
   new[v]=new.get(v,0)+c
  d=new
 assert sum(d.values())==2**n and d[0]==1
 del d[0];keys=sorted(d)
 return keys,[d[k] for k in keys],shift,b

def extract(x,w,q,delta=1e-7):
 rs=[];ws=[]
 for j,up in enumerate(x):
  lo=0 if j==0 else x[j-1]
  def f(y):
   r=lo+(up-lo)*y
   return q-r*np.dot(w,1/(x-r))
  try:y=brentq(f,1e-13,1-1e-13,xtol=1e-14)
  except ValueError:
   # Roots within 1e-13 relative interval endpoint have negligible weight;
   # for this exact integer-count family q/p<=1, giving a<=O(1e-26).
   continue
  r=lo+(up-lo)*y;a=q/(r*np.dot(w*x,1/(x-r)**2));rs.append(r);ws.append(a)
  if sum(ws)>=1-q-delta:return rs,ws,'tail threshold reached'
 return rs,ws,'all roots'

out=[]
for n in [18,32,64,128]:
 t=time.perf_counter();ki,ci,shift,b=compile_hist(n,.05);ct=time.perf_counter()-t
 x=np.array([v/ki[0] for v in ki]);w=np.array([c/2**n for c in ci]);q=2.**-n
 t=time.perf_counter();r,a,status=extract(x,w,q);rt=time.perf_counter()-t
 z=np.array([.1,.3,1,3,10]);mean=np.dot(w,1/x)/q;s=z/mean
 phi=np.array([q/(q+t*np.dot(w,1/(x+t))) for t in s]);approx=np.array([q+np.dot(a,np.array(r)/(np.array(r)+t)) for t in s])
 row=dict(n=n,K=len(x),b=b,grid_shift=shift,max_rate_integer_bits=max(ki).bit_length(),q=q,clock_relative_bound=(1+2.**(1-b))**(n+1)-1,compile_seconds=ct,root_seconds=rt,extracted_roots=len(r),mixture_mass=sum(a),root_status=status,max_LT_truncation_error=float(max(abs(phi-approx))))
 if n==128:
  np.savez(str(Path(__file__).resolve().parent)+'/dyadic128_float.npz',x=x,w=w,r=r,a=a)
  open(str(Path(__file__).resolve().parent)+'/dyadic128_exact.json','w').write(json.dumps(dict(n=n,shift=shift,b=b,rates=[str(v) for v in ki],counts=[str(c) for c in ci])))
 out.append(row);print(row,flush=True)
open(str(Path(__file__).resolve().parent)+'/dyadic_results.json','w').write(json.dumps(out,indent=2))
