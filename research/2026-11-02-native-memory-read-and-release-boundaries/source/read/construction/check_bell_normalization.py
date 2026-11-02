import numpy as np
from itertools import product
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1]).astype(complex)
def kronall(xs):
 a=np.array([[1]],complex)
 for x in xs:a=np.kron(a,x)
 return a
n=3; d=2**n
V=np.zeros((d,2),complex); V[0,0]=V[-1,1]=1
Es=[kronall([I,I,I]),kronall([X,I,I]),kronall([I,X,I]),kronall([I,I,X])]
Vs=[E@V for E in Es]
assert np.linalg.norm(sum(v@v.conj().T for v in Vs)-np.eye(d))<1e-12
rng=np.random.default_rng(741)
# Source entangled with arbitrary reference: channel equality checked through Choi matrix.
Ks=[]; groups=[0]*len(Vs); corrected=[]
for axes in product([I,X,Y,Z],repeat=n):
 P=kronall(axes)
 for s,v in enumerate(Vs):
  L=V.conj().T@P@v
  if np.linalg.norm(L)>1e-10:
   K=L.conj().T@V.conj().T@P/np.sqrt(2*d)
   assert np.linalg.norm(K-v.conj().T/np.sqrt(2*d))<1e-12
   Ks.append(K);groups[s]+=1;corrected.append((P,L,K))
   break
J=lambda ks:sum(np.outer(k.flatten(),k.flatten().conj()) for k in ks)
print('outcome counts:',groups,'expected:',[2*d]*len(Vs))
print('channel Choi difference:',np.linalg.norm(J(Ks)-J([v.conj().T for v in Vs])))
print('TP difference:',np.linalg.norm(sum(k.conj().T@k for k in Ks)-np.eye(d)))
# Check A-fault transposition formula with actual observed-P correction.
E=kronall([Y,I,X]); F=kronall([I,Y,Z]); worst=0.
for P,L,K in corrected:
 direct=L.conj().T@V.conj().T@F.T@P@E/np.sqrt(2*d)
 EP=P.conj().T@F.T@P@E
 worst=max(worst,np.linalg.norm(direct-K@EP))
print('fault-through-Bell worst residual:',worst)
