import sys,numpy as np,sympy as s
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audit_lift import cg
from sympy.physics.wigner import wigner_6j
rng=np.random.default_rng(214)
for n in [1,2,3,4]:
 D=n+1;j=n/2;sj=s.Rational(n,2);blocks=[];X=np.zeros((D**3,D**3))
 for J2 in range(n%2,3*n+1,2):
  J=J2/2;ls=[l for l in range(D)if abs(l-j)<=J<=l+j];h=len(ls)
  Q=np.zeros((D**3,J2+1,h))
  for i in range(D):
   for k in range(D):
    for p in range(D):
     m1=i-j;m2=k-j;m3=p-j;M=m1+m2+m3
     if abs(M)>J:continue
     for t,l in enumerate(ls):Q[(i*D+k)*D+p,round(M+J),t]=cg(j,j,l,m1,m2,m1+m2)*cg(l,j,J,m1+m2,m3,M)
  A=rng.normal(size=(h,h));R=(A+A.T)/2
  X+=np.einsum('ami,ij,bmj->ab',Q,R,Q)
  blocks.append((J2,ls,R,Q))
 # time reversal: Y|m>=(-1)^(j-m)|-m>; transpose third subsystem
 Y=np.zeros((D,D))
 for i in range(D):Y[n-i,i]=(-1)**(n-i)
 U=np.kron(np.eye(D*D),Y)
 XT=X.reshape(D,D,D,D,D,D).transpose(0,1,5,3,4,2).reshape(D**3,D**3)
 Z=U@XT@U.T
 expected={J2:np.einsum('ami,ab,bmj->ij',Q,Z,Q)/(J2+1)for J2,ls,R,Q in blocks}
 err=0
 for l in range(D):
  for lp in range(l,D):
   allowed=[b for b in blocks if l in b[1]and lp in b[1]];ranks=list(range(abs(l-lp),min(l+lp,n)+1))
   C=np.array([[float((-1)**(lp+sj+s.Rational(J2,2)+rank)*wigner_6j(l,sj,s.Rational(J2,2),sj,lp,rank))for rank in ranks]for J2,ls,R,Q in allowed])
   F=(C*np.array([(-1)**rank*(2*rank+1)for rank in ranks]))@C.T@np.diag([b[0]+1 for b in allowed])
   pred=F@np.array([R[ls.index(l),ls.index(lp)]for J2,ls,R,Q in allowed])
   for v,(J2,ls,R,Q)in zip(pred,allowed):err=max(err,abs(v-expected[J2][ls.index(l),ls.index(lp)]))
 print('n',n,'arbitrary-real-invariant PPT map error',err,flush=True)
 assert err<1e-10
