"""Exact rational interval exclusion; no floating arithmetic in certificate."""
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path
S=1<<80

def lo(x):return F(x.numerator*S//x.denominator,S)
def hi(x):return -lo(-x)
def box(a,b=None):return (lo(F(a)),hi(F(a if b is None else b)))
def add(x,y):return box(x[0]+y[0],x[1]+y[1])
def neg(x):return (-x[1],-x[0])
def sub(x,y):return add(x,neg(y))
def mul(x,y):
 p=[a*b for a in x for b in y];return box(min(p),max(p))
def inv(x):
 assert x[0]>0
 return box(1/x[1],1/x[0])
def div(x,y):return mul(x,inv(y))
def scale(x,n):return mul(x,box(n))
@lru_cache(None)
def exp_point(x):
 assert x>=0 and x<20
 term=F(1);s=term
 for n in range(1,121):term*=x/n;s+=term
 nxt=term*x/121
 return box(s,s+nxt/(1-x/F(122)))
@lru_cache(None)
def log_point(x):
 assert x>0
 k=0
 while x>2:x/=2;k+=1
 while x<1:x*=2;k-=1
 z=(x-1)/(x+1);p=z;s=F(0)
 for n in range(60):s+=p/F(2*n+1);p*=z*z
 ans=box(2*s,2*s+2*p/(F(121)*(1-z*z)))
 if k:
  # direct atanh series for log2, with the same exact tail
  z=F(1,3);p=z;s=F(0)
  for n in range(60):s+=p/F(2*n+1);p*=z*z
  l2=box(2*s,2*s+2*p/(F(121)*(1-z*z)))
  ans=add(ans,scale(l2,k))
 return ans
L2=log_point(F(2));L3=log_point(F(3))
@lru_cache(None)
def UD(t):
 if t==0:return box(2),box(1)
 e=exp_point(2*t)
 u=scale(div(add(e,box(1)),sub(e,box(1))),2*t)
 d=div(scale(e,4*t*t),mul(sub(e,box(1)),sub(e,box(1))))
 return u,d

def log_i(x):return (log_point(x[0])[0],log_point(x[1])[1])
def f_point(x):return sub(scale(log_point(x),2),box(x))
MAXLOG=sub(scale(L2,2),box(2)) # log(4/e²)
stack=[(F(1),F(3),F(0),F(3),0)];count=0;depthmax=0;reasons={};leaves=[]
def reject(reason,rect):
 reasons[reason]=reasons.get(reason,0)+1
 leaves.append({'box':[str(v) for v in rect[:4]],'reason':reason})
while stack:
 a,b,c,d,dep=rect=stack.pop();count+=1;depthmax=max(depthmax,dep)
 if c>=b:reject('theta>phi',rect);continue
 ua,da=UD(a);ub,db=UD(b);uc,dc=UD(c);ud,dd=UD(d)
 U=(ua[0],ub[1]);V=(uc[0],ud[1]);DT=(db[0],da[1]);DL=(dd[0],dc[1])
 logDT=log_i(DT)
 if logDT[0]>MAXLOG[1]:reject('m-moment maximum',rect);continue
 r=log_i(div(scale(DT,4),DL))
 if r[0]>=L3[1] or r[1]<0:reject('r range',rect);continue
 u=sub(U,V);u=(max(F(0),u[0]),u[1])
 if u[1]<0 or u[0]>=min(r[1],L3[1]):reject('q positivity',rect);continue
 m=sub(scale(V,2),U);m=(max(F(0),m[0]),m[1])
 if m[1]<=0:reject('m positivity',rect);continue
 fl=f_point(m[0]) if m[0]>0 else None;fh=f_point(m[1])
 ghigh=max(fh[1],fl[1] if fl else fh[1],MAXLOG[1] if m[0]<=2<=m[1] else fh[1])-logDT[0]
 glow=min(fl[0],fh[0])-logDT[1] if fl else None
 if (glow is not None and glow>0) or ghigh<0:reject('moment equation',rect);continue
 r=(max(r[0],F(0)),min(r[1],L3[1]));u=(u[0],min(u[1],r[1]))
 ff=sub(add(sub(mul(r,r),mul(u,u)),scale(DT,2)),scale(DL,4))
 if ff[0]>0 or ff[1]<0:reject('determinant equation',rect);continue
 if dep>=30:raise RuntimeError(('unresolved',rect))
 if b-a>d-c:
  mid=(a+b)/2;stack.extend([(a,mid,c,d,dep+1),(mid,b,c,d,dep+1)])
 else:
  mid=(c+d)/2;stack.extend([(a,b,c,mid,dep+1),(a,b,mid,d,dep+1)])
receipt={'status':'PASS','arithmetic':'Fraction; all transcendental enclosures exact positive series with rational geometric tails; outward dyadic rounding at 80 bits','domain':{'theta':['1','3'],'phi':['0','3']},'nodes':count,'max_depth':depthmax,'reasons':reasons,'leaves':leaves,'scope':'No negative balanced interior stationary candidate on compact domain; analytic tail and endpoint receivers supplied in governing theorem.'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(receipt,indent=2));print({k:v for k,v in receipt.items() if k!='leaves'})
