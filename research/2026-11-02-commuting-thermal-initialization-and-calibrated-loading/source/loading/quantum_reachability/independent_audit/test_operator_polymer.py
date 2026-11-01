import numpy as np
from scipy.linalg import expm
from itertools import combinations
I=np.eye(2); X=np.array([[0,1],[1,0.]]);Z=np.diag([1.,-1]);Y=np.array([[0,-1j],[1j,0]])
k=np.kron; I4=np.eye(4)
H=.6*k(Z,I)+.4*k(I,Z); beta=.8
V=[.02*k(X,I),.03*k(I,X),.01*k(Z,X)]
P=[k(X,I),k(I,Z)]
q=[.01,.015]; r=[a/(1-a) for a in q]
T=expm(beta*H/2);Ti=expm(-beta*H/2)
B=[T@p@Ti for p in P]
U={s:T@expm(-beta*(H+sum((V[i] for i in range(3) if s>>i&1),np.zeros((4,4)))))@T for s in range(8)}
AV={}
for s in range(1,8):
 AV[s]=sum(((-1)**(s.bit_count()-t.bit_count())*U[t] for t in range(8) if not t&~s),np.zeros((4,4)))
 assert np.linalg.norm(AV[s]-AV[s].conj().T)<1e-12
support=[{0},{1},{0,1},{0},{1}]
def comps(s):
 left={i for i in range(5) if s>>i&1};out=[]
 while left:
  todo=[left.pop()];cc=set(todo)
  while todo:
   i=todo.pop();ns={j for j in left if support[i]&support[j]};left-=ns;cc|=ns;todo+=list(ns)
  out.append(sum(1<<i for i in cc))
 return out
A={}
for s in range(1,32):
 if len(comps(s))!=1:continue
 v=s&7;C=AV[v] if v else I4
 F=I4.copy();coeff=1.
 for j in range(2):
  if s>>(j+3)&1:F=F@B[j];coeff*=-r[j]
 A[s]=coeff*F@C@F.conj().T
 assert np.linalg.norm(A[s]-A[s].conj().T)<1e-12
Kgas=I4.copy()
for s in range(1,32):
 a=I4.copy()
 for c in comps(s):a=a@A[c]
 Kgas+=a
K=U[7].copy()
for j in range(2):K=K-r[j]*B[j]@K@B[j].conj().T
assert np.linalg.norm(Kgas-K)<1e-12
assert np.linalg.eigvalsh(Kgas).min()>0
# Fully incompatible, noncommuting matrix gas: all deletion ratios.
AA=[.01*X,.01*Y,.01*Z];mu=.05
for s in range(1,8):
 ZZ=I.astype(complex)+sum((AA[i] for i in range(3) if s>>i&1),np.zeros((2,2),complex))
 assert np.linalg.eigvalsh(ZZ).min()>0
 for i in range(3):
  if s>>i&1:assert np.linalg.norm(np.linalg.solve(ZZ,ZZ-AA[i]),2)<=1+mu
assert all(np.linalg.norm(a,2)*(1+mu)**3<=mu for a in AA)
# Explicit generic-reference counterexample to using only norm(H-PHP).
h=10*Z+.1*X;p=Z;b=expm(h/2)@p@expm(-h/2)
print('joint expansion norm residual',np.linalg.norm(Kgas-K),'K min eigenvalue',np.linalg.eigvalsh(Kgas).min())
print('all noncommuting deletion cases PASS')
print('generic-ref energy-change shortcut fails:',np.linalg.norm(b,2)**2,'>',np.exp(np.linalg.norm(h-p@h@p,2)))
