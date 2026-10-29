import itertools,json
import numpy as np

def check(n,edges,g=.73,k=1.19):
 S=[s for s in range(1<<n) if all(not(s>>a&1 and s>>b&1) for a,b in edges)]
 idx={s:i for i,s in enumerate(S)}; m=len(S); I=np.eye(m)
 b=[]; ns=[]
 for x in range(n):
  a=np.zeros((m,m),complex)
  for j,s in enumerate(S):
   if s>>x&1:a[idx[s^(1<<x)],j]=1
  b.append(a);ns.append(a.conj().T@a)
 H=g*sum(a+a.conj().T for a in b)
 def dis(A):return k*sum(a.conj().T@A@a-(a.conj().T@a@A+A@a.conj().T@a)/2 for a in b)
 def L(A):return 1j*(H@A-A@H)+dis(A)
 out=[]
 for x in range(n):
  N={v for e in edges if x in e for v in e if v!=x}; D=max(sum(v in e for e in edges) for v in range(n))
  G=np.diag([all(not(s>>y&1) for y in N) for s in S]);P=ns[x];Q=I-P
  B=L(L(P))-2*g*g*G-(k*k-4*g*g)*P
  residual=max(np.linalg.norm(Q@B@Q,2),np.linalg.norm(P@B@P,2))
  diss=0
  for j in range(len(N)+1):
   Pj=np.diag([sum(s>>y&1 for y in N)<=j for s in S]);Pi=np.diag([sum(s>>y&1 for y in N)==j+1 for s in S])
   diss=max(diss,np.linalg.norm(dis(Pj)-k*(j+1)*Pi,2))
  bound=2*g*g*D+2*k*g*(D+1)+k*g
  assert residual<1e-10 and diss<1e-10 and np.linalg.norm(B,2)<=bound+1e-10
  out.append(dict(x=x,curvature_block_residual=residual,dissipative_identity_residual=diss,B_norm=float(np.linalg.norm(B,2)),B_bound=bound))
 return dict(n=n,edges=edges,dimension=m,sites=out)
R=[check(1,[]),check(4,[(0,1),(1,2),(2,3)]),check(5,[(0,1),(0,2),(0,3),(0,4)]),check(5,[(i,(i+1)%5) for i in range(5)]),check(4,list(itertools.combinations(range(4),2)))]
print(json.dumps(R,indent=2))
