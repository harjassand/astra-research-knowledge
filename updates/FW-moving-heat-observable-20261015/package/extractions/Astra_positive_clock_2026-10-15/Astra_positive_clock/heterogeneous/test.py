from pathlib import Path
import numpy as np,time,json
from scipy.optimize import brentq

def exact(n):
 rates=5.**(-np.arange(n))*(1+np.arange(n)/(10*n))
 x=np.array([0.])
 for r in rates: x=np.r_[x,x+r]
 return np.sort(x[1:]), np.full(2**n-1,2.**-n),rates

def rounded(n,eta):
 rates=5.**(-np.arange(n))*(1+np.arange(n)/(10*n)); base=rates[-1]; logg=np.log1p(eta)
 # Integer probability counts: q exactly one outcome over 2**n.
 d={};zero=1
 for r in rates[::-1]:
  new=d.copy(); k=int(np.floor(np.log(r/base)/logg));new[k]=new.get(k,0)+zero
  for key,c in d.items():
   v=base*np.exp(logg*key)+r;k=int(np.floor(np.log(v/base)/logg));new[k]=new.get(k,0)+c
  d=new
 x=np.array([base*np.exp(logg*k) for k in sorted(d)]); w=np.array([d[k]/2**n for k in sorted(d)])
 return x,w,rates

def stats(n,x,w):
 q=2.**-n;A=np.dot(w,1/x); B=np.dot(w,1/x**2);mean=A/q
 zs=np.array([.1,.3,1.,3.,10.]); F=np.array([q/(q+z/mean*np.dot(w,1/(x+z/mean))) for z in zs]); ex=q+(1-q)/(1+zs/(1-q))
 return dict(mean=mean,D=q*B/A**2,LT=F.tolist(),expLT=ex.tolist(),maxLTgap=float(max(abs(F-ex))))
rows=[]
for n in [8,12,16,18,32,64,128]:
 eta=.05/n;t=time.perf_counter();x,w,r=rounded(n,eta);tm=time.perf_counter()-t; row=dict(n=n,q=2.**-n,K=len(x),round_seconds=tm,eta=eta,relative_bound=(1+eta)**n-1,**stats(n,x,w))
 if n<=18:
  t=time.perf_counter();xx,ww,_=exact(n);row['exact_seconds']=time.perf_counter()-t;row['exact']=stats(n,xx,ww)
  # compare transforms at common physical arguments
  mean=row['exact']['mean'];q=2.**-n;fs=[q/(q+z/mean*np.dot(w,1/(x+z/mean))) for z in [.1,.3,1,3,10]]
  row['max_exact_LT_error']=float(max(abs(np.array(fs)-row['exact']['LT'])))
 rows.append(row);print(json.dumps(row),flush=True)
open(str(Path(__file__).resolve().parent)+'/results.json','w').write(json.dumps(rows,indent=2))
