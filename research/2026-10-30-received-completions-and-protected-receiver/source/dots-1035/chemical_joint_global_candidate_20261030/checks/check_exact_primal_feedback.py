import math,json
from functools import lru_cache
from scipy.special import gammaln,logsumexp

def fall(n,k):
 return math.prod(range(n-k+1,n+1)) if n>=k else 0

def coefficient(a,c,b,alpha):
 @lru_cache(None)
 def logf(a,b):
  base=alpha*(gammaln(a+1)+gammaln(b+1))
  if b>=4:return base
  terms=[base,logf(a+1,b+1)]
  if a*b:terms.append(math.log(a*b)+logf(a+2,b+3))
  return float(logsumexp(terms)-math.log1p(a*b))
 def logF(a,c,b):return alpha*gammaln(c+1)+logf(a,b)
 v=logF(a,c,b)
 edges=[(a+1,c,b+1,1),(a+2,c,b+3,a*b),(a-3,c,b-4,fall(a,3)*fall(b,4)),
 (a+1,c-1,b,(6*fall(c,3)+a*fall(c,2)+7*fall(a,2)*c)*fall(b,4)),
 (a-1,c+1,b,(12*a*fall(c,2)+fall(a,2)*c+fall(a,3))*fall(b,4))]
 drift=sum(rate*math.expm1(logF(aa,cc,bb)-v) for aa,cc,bb,rate in edges if rate)
 return drift/max(1,(a+c)**3*fall(b,4))
out=[]
for r in [0,.01,.1,2.5,10,100]:
 for c in [100,1000,10000,100000]:
  a=int(r*c);out.append({'ratio':r,'A':a,'C':c,'B':4,'alpha':.2,'normalized_drift':coefficient(a,c,4,.2)})
print(json.dumps(out,indent=2))
