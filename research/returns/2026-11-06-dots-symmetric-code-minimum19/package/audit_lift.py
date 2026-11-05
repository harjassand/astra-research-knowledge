import sys,math,itertools,numpy as np,sympy as s
from functools import lru_cache
from sympy.physics.wigner import clebsch_gordan,wigner_6j
from pathlib import Path
r=Path(__file__).resolve().parent
@lru_cache(None)
def cg(j1,j2,J,m1,m2,M):
 if abs(m1+m2-M)>1e-9 or abs(M)>J or J<abs(j1-j2) or J>j1+j2:return 0.
 ints=[J+j1-j2,J-j1+j2,j1+j2-J,j1+j2+J+1,J+M,J-M,j1-m1,j1+m1,j2-m2,j2+m2]
 if any(abs(round(v)-v)>1e-8 or v<0 for v in ints):return 0.
 l=[math.lgamma(v+1)for v in ints];front=.5*(math.log(2*J+1)+sum(l[:3])-l[3]+sum(l[4:]))
 lo=int(max(0,-J+j2-m1,-J+j1+m2));hi=int(min(j1+j2-J,j1-m1,j2+m2));result=0.
 for k in range(lo,hi+1):
  ints=[k,j1+j2-J-k,j1-m1-k,j2+m2-k,J-j2+m1+k,J-j1-m2+k]
  result+=(-1)**k*math.exp(front-sum(math.lgamma(v+1)for v in ints))
 return result
for j1,j2,J,m1,m2 in [(3.5,3.5,3,-1.5,2.5),(4,3.5,4.5,2,-1.5),(.5,.5,0,.5,-.5)]:
 exact=float(clebsch_gordan(s.Rational(j1),s.Rational(j2),s.Rational(J),s.Rational(m1),s.Rational(m2),s.Rational(m1+m2)));assert abs(cg(j1,j2,J,m1,m2,m1+m2)-exact)<1e-12

def audit(n):
 j=n/2;D=n+1;K=2
 if n==7: sparse=[(0,0,math.sqrt(.3)),(5,0,math.sqrt(.7)),(2,1,math.sqrt(.7)),(7,1,-math.sqrt(.3))];d=3
 else:sparse=[(0,0,math.sqrt(5/68)),(8,0,math.sqrt(7/12)),(17,0,math.sqrt(35/102)),(4,1,math.sqrt(35/102)),(13,1,-math.sqrt(7/12)),(21,1,-math.sqrt(5/68))];d=5
 V=np.zeros((D,2));
 for ix,b,v in sparse:V[ix,b]=v
 P=V@V.T;Jz=np.diag(np.arange(D)-j);Jplus=np.diag([math.sqrt((n-m)*(m+1))for m in range(n)],-1);Jminus=Jplus.T
 kl=0.
 for a in range(d):
  for b in range(d-a):
   for c in range(d-a-b):
    E=np.linalg.matrix_power(Jplus,a)@np.linalg.matrix_power(Jz,b)@np.linalg.matrix_power(Jminus,c);C=V.T@E@V;kl=max(kl,np.max(np.abs(C-np.trace(C)*np.eye(2)/2))/max(1,np.linalg.norm(E)))
 blocks=[]
 for J2 in range(n%2,3*n+1,2):
  J=J2/2;ls=[l for l in range(D)if abs(l-j)<=J<=l+j];h=len(ls);C=np.zeros((J2+1,h,8))
  for (i,b1,v1),(k,b2,v2),(p,b3,v3) in itertools.product(sparse,repeat=3):
   m1=i-j;m2=k-j;m3=p-j;M=m1+m2+m3
   if abs(M)>J:continue
   for li,l in enumerate(ls):C[round(M+J),li,4*b1+2*b2+b3]+=v1*v2*v3*cg(j,j,l,m1,m2,m1+m2)*cg(l,j,J,m1+m2,m3,M)
  R=np.einsum('mia,mja->ij',C,C)/(J2+1)
  sj=s.Rational(n,2);sJ=s.Rational(J2,2);U=np.array([[float((-1)**(n+l+lp)*s.sqrt((2*l+1)*(2*lp+1))*wigner_6j(sj,sj,l,sj,sJ,lp))for lp in ls]for l in ls]);blocks.append((J2,ls,R,U))
 norm=sum((J2+1)*np.trace(R)for J2,ls,R,U in blocks);comm=max(np.max(np.abs(R@U-U@R))for J2,ls,R,U in blocks)
 residual=0.;worst=None
 for rank in range(d):
  for l in range(D):
   for lp in range(l,min(D,l+rank+1)):
    if l+lp<rank:continue
    val=0.
    for J2,ls,R,U in blocks:
     if l not in ls or lp not in ls:continue
     J=s.Rational(J2,2);sj=s.Rational(n,2);coef=float((-1)**(lp+sj+J+rank)*wigner_6j(l,sj,J,sj,lp,rank));val+=(J2+1)*coef*(R@(U-np.eye(len(ls))/K))[ls.index(lp),ls.index(l)]
    if abs(val)>residual:residual=abs(val);worst=(rank,l,lp,val)
 print({'n':n,'KL':kl,'norm':norm,'commutator':comm,'lift_residual':residual,'worst':worst},flush=True)
if __name__=='__main__':audit(int(sys.argv[1])if len(sys.argv)>1 else 7)
