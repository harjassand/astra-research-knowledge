import numpy as np, math
from scipy.special import gammaln, logsumexp

def coeff(Y,edges):
 Q=np.zeros((len(Y),len(Y)))
 for i,j,k in edges:Q[i,j]+=k;Q[i,i]-=k
 R=Q.T.copy();R[-1]=1;b=np.zeros(len(Y));b[-1]=1
 pi=np.linalg.solve(R,b);return pi*(-np.diag(Q))
def logfall(x,y):
 if any(a<b for a,b in zip(x,y)):return -np.inf
 return sum(sum(math.log(a-i) for i in range(b)) for a,b in zip(x,y))
def check(Y,edges,x,al):
 s=coeff(Y,edges)
 def lognu(v):
  return al*logsumexp([math.log(si)/al-sum(gammaln(a-b+1) for a,b in zip(v,y)) for si,y in zip(s,Y) if all(a>=b for a,b in zip(v,y))])
 def logq(v):return logsumexp([math.log(k)+logfall(v,Y[i]) for i,j,k in edges])
 qx=logq(x)
 if not np.isfinite(qx):return None
 logmu=lognu(x)-qx
 inc=[]
 for i,j,k in edges:
  prev=tuple(x[t]-Y[j][t]+Y[i][t] for t in range(len(x)))
  if min(prev)<0:continue
  lf=logfall(prev,Y[i])
  if not np.isfinite(lf):continue
  inc.append(math.log(k)+lf+lognu(prev)-logq(prev)-logmu-qx)
 return math.expm1(logsumexp(inc))
examples=[([(0,0),(0,1),(3,1)],[(0,1,1),(1,2,1),(2,0,1)]), ([(0,0),(2,0),(1,2),(2,1)],[(0,1,1),(1,2,100),(2,3,1),(3,1,1),(1,0,1)])]
for ei,(Y,E) in enumerate(examples):
 for al in [.2,.05,.01]:
  vals=[]
  for n in [100,10000,1000000]:
   for x in [(n,0),(n,1),(n,2),(0,n),(1,n),(2,n),(n,n),(n,int(math.sqrt(n)))]:
    r=check(Y,E,x,al)
    if r is not None and r>1e-7:vals.append((x,r))
  print(ei,al,vals[:12],flush=True)
Y=[(0,0),(1,1),(2,3)];E=[(0,1,1),(1,2,2),(2,0,3)]
for al in [.2,.1,.03]:
 vals=[]
 for n in [1000,100000,1000000]:
  for b in range(10):
   v=check(Y,E,(n,b),al)
   if v>1e-7: vals.append((n,b,v))
 print('triangle',al,vals,flush=True)
