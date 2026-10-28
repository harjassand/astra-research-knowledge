"""Elementary rational scalar certificates, generalized from the frozen sol12 control.

No eigensolver or approximate entropy is a proof premise.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import isqrt
BITS=80
TERMS=24
def iv(x):return Q(x),Q(x)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 values=[x*y for x in a for y in b];return min(values),max(values)
def scale(a,x):return mul(a,iv(x))
def sqrtq(x):
 x=Q(x);assert x>=0
 n=isqrt((x.numerator<<(2*BITS))//x.denominator);lo=Q(n,1<<BITS)
 return(lo,lo)if lo*lo==x else(lo,Q(n+1,1<<BITS))
def series(y):
 z=(y-1)/(y+1);assert 0<=z<=Q(1,3)
 lo=2*sum(z**(2*j+1)/Q(2*j+1)for j in range(TERMS))
 tail=2*z**(2*TERMS+1)/(Q(2*TERMS+1)*(1-z*z))
 return lo,lo+tail
LOG2=series(Q(2))
@lru_cache(None)
def logq(x):
 x=Q(x);assert x>0
 if x<1:return neg(logq(1/x))
 power=0
 while x>=2:x/=2;power+=1
 return add(series(x),scale(LOG2,power))
def logiv(x):return logq(x[0])[0],logq(x[1])[1]
def hterm(x):
 lo=max(Q(0),x[0]);hi=min(Q(1),x[1]);assert lo<=hi
 if hi==0:return iv(0)
 if lo==0:
  assert hi<=Q(1,4);return Q(0),-hi*logq(hi)[0]
 return neg(mul((lo,hi),logiv((lo,hi))))
def entropy(xs):
 out=iv(0)
 for x in xs:out=add(out,hterm(x))
 return out
def hmax(q,n):
 z=scale(add(iv(1),sqrtq((n-1)*(n*q-1))),Q(1,n))
 small=scale(sub(iv(1),z),Q(1,n-1))
 return add(hterm(z),scale(hterm(small),n-1))
def hmin(q,d):
 q=Q(q);assert Q(1,d)<=q<=1
 k=min(d-1,q.denominator//q.numerator)
 a=scale(add(iv(k),sqrtq(k*((k+1)*q-1))),Q(1,k*(k+1)))
 b=sub(iv(1),scale(a,k))
 return add(scale(hterm(a),k),hterm(b))
def trim(p):
 while len(p)>1 and p[-1]==0:p.pop()
 return p
def value(p,x):
 out=Q(0)
 for c in reversed(p):out=out*x+c
 return out
def remainder(p,q):
 p=p[:]
 while len(p)>=len(q)and p!=[0]:
  alpha=p[-1]/q[-1];shift=len(p)-len(q)
  for j,c in enumerate(q):p[shift+j]-=alpha*c
  trim(p)
 return p
def sturm(p):
 seq=[p,[i*p[i]for i in range(1,len(p))]]
 while len(seq[-1])>1:
  rest=remainder(seq[-2],seq[-1]);assert rest!=[0],'Fixture polynomial is not square-free'
  seq.append([-v for v in rest])
 return seq
def variation(seq,x):
 signs=[1 if z>0 else-1 for p in seq if(z:=value(p,x))!=0]
 return sum(a!=b for a,b in zip(signs,signs[1:]))
def roots01(p,bits=74):
 seq=sturm(p);degree=len(p)-1
 def count(lo,hi):return variation(seq,lo)-variation(seq,hi)
 assert value(p,0)!=0 and value(p,1)!=0 and count(Q(0),Q(1))==degree
 todo=[(Q(0),Q(1),degree)];roots=[];steps=0
 while todo:
  lo,hi,n=todo.pop()
  if n==1 and hi-lo<=Q(1,2**bits):roots.append((lo,hi));continue
  split=next(lo+(hi-lo)/z for z in range(2,degree+3)if value(p,lo+(hi-lo)/z)!=0)
  left=count(lo,split);right=count(split,hi);assert left+right==n
  if left:todo.append((lo,split,left))
  if right:todo.append((split,hi,right))
  steps+=1
 roots.sort();return roots,steps
def serial(x):
 x=Q(x);return str(x.numerator)+'/'+str(x.denominator)
def record(x):return{'lower':serial(x[0]),'upper':serial(x[1]),'display_only':list(map(float,x))}
