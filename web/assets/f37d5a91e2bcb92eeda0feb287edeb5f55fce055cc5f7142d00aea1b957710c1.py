from fractions import Fraction as F
from pathlib import Path
import json,time
start=time.monotonic()
def partitions(m,r,top=None):
 if r==0:yield ();return
 if top is None:top=m
 for h in range(top+1):
  for tail in partitions(m,r-1,h):yield (h,)+tail

def mu(m,d,p):
 q=F(1)
 for j,L in enumerate(p):
  for t in range(L):q*=F(m+j-t,m+d-j+t)
 return q
rec=[];big=F(0);worst=None;over=[];count=0
for d in range(2,17):
 for r in range(1,d//2+1):
  for m in range(1,5):
   for p in partitions(m,r):
    if not any(p):continue
    a=mu(2*m,d,p);b=mu(m,d,p);lam=b/a;c=(1-a)/(1-lam)
    count+=1
    if c>big:big=c;worst=(d,r,m,p)
    if c>2:over.append({'d':d,'r':r,'m':m,'partition':p,'c':str(c)})
    c0=F(2*(m+d),2*m+d)
    if c>c0:rec.append({'d':d,'r':r,'m':m,'partition':p,'c':str(c),'c0':str(c0)})
result={'status':'CONDITIONAL_FORMULA_DIAGNOSTIC','scalar_cases':count,'max_c':str(big),'parameters_d_rank_m_partition':worst,'above2':over,'above_first_harmonic_count':len(rec),'above_first_harmonic_first10':rec[:10],'wall_seconds':time.monotonic()-start,'boundary':'Grassmann Berezin formula is a candidate input, not yet independently derived. This is no compatible-channel counterexample or EB theorem.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
