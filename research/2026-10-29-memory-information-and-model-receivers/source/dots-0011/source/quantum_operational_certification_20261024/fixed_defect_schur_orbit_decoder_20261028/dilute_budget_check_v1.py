import math,json
from pathlib import Path

def h(x):return 0 if x==0 or x==1 else -x*math.log2(x)-(1-x)*math.log2(1-x)
def run(c,R,Delta,eps,b=2):
 j=0
 while c**(j+1)/math.factorial(j+1)>eps/6:j+=1
 A=20/9;bb=(b-1)*(b+2)/2
 for z in range(4,40):
  k=2**z
  if k<=max(j,2*c):continue
  u=math.sqrt(2/k*math.log(6*(k+1)**bb/eps))
  if u>1:continue
  ll=sum(math.log2(k-i) for i in range(j));f=lambda x:x*math.log2(b-1)+h(x)
  lhs=k*(Delta-f(c/k)-f(u/2))-bb*math.log2(k+b)
  rhs=3*ll+math.log2(6*A/eps)
  if lhs>=rhs:return {'c':c,'R':R,'Delta':Delta,'epsilon':eps,'dimensionB':b,'j':j,'first_tested_power2_k':k,'lhs':lhs,'rhs':rhs,'log2_L':ll,'log2_alpha_bound':2*ll,'scope':'sufficient mathematical threshold, not practical gate execution'}
 raise RuntimeError('no threshold')
x=[run(1,.5,.25,e) for e in [.1,.01,.001]]
Path(__file__).with_suffix('.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
