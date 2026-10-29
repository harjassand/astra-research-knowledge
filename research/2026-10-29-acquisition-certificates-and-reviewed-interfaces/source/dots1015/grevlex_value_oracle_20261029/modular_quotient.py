import numpy as np,sympy as sp,json,time,math
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).parent;n=40;data=json.loads((P/'quotient.json').read_text());raw=[[[F(x) for x in c] for c in m] for m in data['multiplication_columns']];terms=[(e,F(c)) for e,c in data['f0_terms']]
def inv(A,p):
 A=A.copy();B=np.eye(n,dtype=np.int64)
 for j in range(n):
  k=next((k for k in range(j,n) if A[k,j]),None)
  if k is None:raise ValueError('singular')
  A[[j,k]]=A[[k,j]];B[[j,k]]=B[[k,j]];v=pow(int(A[j,j]),-1,p);A[j]=A[j]*v%p;B[j]=B[j]*v%p
  fac=A[:,j].copy();fac[j]=0;A=(A-fac[:,None]*A[j])%p;B=(B-fac[:,None]*B[j])%p
 return B

def cp(p):
 assert 40*(p-1)**2<2**63
 def cv(x):return x.numerator*pow(x.denominator%p,-1,p)%p
 mats=[np.array([[cv(x) for x in c] for c in m],dtype=np.int64).T for m in raw];I=np.eye(n,dtype=np.int64)
 mul=lambda A,B:(A@B)%p
 powers=[[I,A,mul(A,A),mul(mul(A,A),A)] for A in mats]
 norm=(I+sum(ps[2] for ps in powers))%p;num=np.zeros((n,n),dtype=np.int64)
 for e,c in terms:
  v=I
  for j,k in enumerate(e):
   if k:v=mul(v,powers[j][k])
  num=(num+v*cv(c))%p
 L=mul(inv(norm,p),num)*pow(4,-1,p)%p
 cols=[];v=I[:,0]
 for k in range(n+1):cols.append(v);v=mul(L,v)
 K=np.array(cols[:n]).T;Ki=inv(K,p);co=(-mul(Ki,cols[n]))%p
 assert np.all((mul(K,co)+cols[n])%p==0)
 return [int(x) for x in co]+[1]
def rr(a,M):
 lim=math.isqrt(M//2);r0,r1=M,a;t0,t1=0,1
 while r1>lim:q=r0//r1;r0,r1=r1,r0-q*r1;t0,t1=t1,t0-q*t1
 if t1==0 or abs(t1)>lim or math.gcd(r1,t1)!=1:return
 if t1<0:r1=-r1;t1=-t1
 if (r1-a*t1)%M:return
 return F(r1,t1)
def main():
 st=time.time();mod=1;res=[0]*n;pr=10000019;records=[]
 for attempt in range(600):
  try:c=cp(pr)
  except ValueError:pr=int(sp.nextprime(pr));continue
  iv=pow(mod%pr,-1,pr)
  for j in range(n):res[j]+=mod*((c[j]-res[j])%pr*iv%pr)
  mod*=pr;records.append(pr)
  if len(records)%8==0:
   r=[rr(x,mod) for x in res];ok=all(x is not None for x in r);print(len(records),mod.bit_length(),ok,time.time()-st,flush=True)
   if ok:
    pp=int(sp.nextprime(pr));test=cp(pp)
    if all(x.denominator%pp and x.numerator*pow(x.denominator%pp,-1,pp)%pp==test[j] for j,x in enumerate(r)):
     r+=[F(1)];d=math.lcm(*(x.denominator for x in r));ints=[int(x*d) for x in r];g=math.gcd(*ints);ints=[x//g for x in ints]
     out={'status':'CANDIDATE_NOT_YET_EXACTLY_CERTIFIED','seconds':time.time()-st,'primes':records,'monic_coefficients_low_to_high':list(map(str,r)),'integer_coefficients_low_to_high':list(map(str,ints)),'modulus_bits':mod.bit_length()};(P/'candidate.json').write_text(json.dumps(out,indent=2)+'\n');return
  pr=int(sp.nextprime(pr))
 raise RuntimeError('600 primes exhausted')
if __name__=='__main__':main()
