"""Focused actual-alphabet cleanup test plus abstract GKLS-tilt algebra diagnostic.
Not a full native-generator numerical simulation; terminal normalizers have their
separate accepted regressions. Deterministic seed; all files remain local.
"""
import itertools,json,numpy as np
from scipy.linalg import eigh
rng=np.random.default_rng(271828)
phases=['I','A0','A1','A2','C0','C1','Q0','Q1','Q2','R']
tags=list(itertools.product('foz',repeat=2))
basis=[(p,t,w) for p in phases for t in tags for w in range(2)]
idx={b:i for i,b in enumerate(basis)};n=len(basis)
def good(p,t,w):
 if w or p=='R':return False
 if p=='I':return all(x not in 'oz' for x in t)
 if p[0]=='A':
  i=int(p[1]);return all(x=='o' if j<i else x not in 'oz' for j,x in enumerate(t))
 if p[0]=='C':return all(x=='o' for x in t)
 if p[0]=='Q':return all(t[j] not in 'oz' for j in range(int(p[1])))
 raise ValueError(p)
bad=np.array([not good(*b) for b in basis],float);B=np.diag(bad);G=np.eye(n)-B
A=np.zeros((n,n),complex)
for group in [[('A0',('f','f'),0),('A1',('o','f'),0),('A2',('o','o'),0)], [('C0',('o','o'),0),('C1',('o','o'),0)]]:
 X=rng.normal(size=(len(group),len(group)))+1j*rng.normal(size=(len(group),len(group)))
 X=X@X.conj().T;X/=np.linalg.norm(X,2)*1.3
 q=[idx[b] for b in group];A[np.ix_(q,q)]=X
V=np.diag(np.exp(.7*bad));Vc=V@(np.eye(n)-.23*A)
maxcross=0.;maxcomm=0.;newbad=0.
for j in range(2):
 J=np.zeros((n,n),complex)
 for b,i in idx.items():
  p,t,w=b
  if t[j]=='z':
   tt=list(t);tt[j]='f';J[idx[p,tuple(tt),w],i]=1
 gain=J.conj().T@Vc@J
 cross=np.linalg.norm(G@gain@B,2);maxcross=max(maxcross,cross)
 maxcomm=max(maxcomm,np.linalg.norm(B@gain-gain@B,2))
 # New coefficient pulled back by cleanup must lie entirely in bad corner.
 pulled=J.conj().T@A@J
 newbad=max(newbad,np.linalg.norm(pulled-B@pulled@B,2))
# Actual negative pattern: target Q0/Q1 coherence at tags f,f pulls through
# z->f to Q0 good versus Q1 bad; this is why generic exposure is different.
J=np.zeros((n,n),complex)
for b,i in idx.items():
 p,t,w=b
 if t[0]=='z':J[idx[p,('f',t[1]),w],i]=1
u=np.zeros(n,complex);u[idx['Q0',('f','f'),0]]=1/np.sqrt(2);u[idx['Q1',('f','f'),0]]=1/np.sqrt(2)
R=np.outer(u,u.conj());negative=np.linalg.norm(G@(J.conj().T@R@J)@B,2)
# Abstract 3-state local algebra: an indefinite Hamiltonian Delta_e is legal.
# q=0 is an invariant clean state. Both dirty states reset separately to q=0.
q=np.diag([0.,1.,1.]);H=np.array([[0,0,0],[0,0,1.2],[0,1.2,0]],complex)
js=[]
for a in [1,2]:
 j=np.zeros((3,3),complex);j[0,a]=np.sqrt(5);js.append(j)
Gamma=sum(j.conj().T@j for j in js);v=np.diag([1.,4.,5.]);s=np.diag(np.sqrt(np.diag(v)));si=np.linalg.inv(s)
k=-1j*H-Gamma/2;jp=[s@j@si for j in js];kp=s@k@si
Delta=-(sum(j.conj().T@j for j in jp)+kp.conj().T+kp)
kh=s@(-1j*H)@si;DeltaH=-(kh.conj().T+kh)
hp=(kp.conj().T-kp)/(2j)
def tilted(o):return sum(j.conj().T@o@j for j in jp)+kp.conj().T@o+o@kp
def cons(o):
 gp=sum(j.conj().T@j for j in jp)
 return 1j*(hp@o-o@hp)+sum(j.conj().T@o@j for j in jp)-(gp@o+o@gp)/2
X=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));O=X+X.conj().T
identity=np.linalg.norm(cons(O)-(tilted(O)+(Delta@O+O@Delta)/2),2)
res={'actual_cleanup_dimension':n,'actual_cleanup_credit_good_bad_cross':float(maxcross),'actual_cleanup_gain_B_commutator':float(maxcomm),'new_A_coefficient_outside_dirty_corner':float(newbad),'generic_Q_clock_coherence_negative_cross':float(negative),'abstract_indefinite_H_Delta_eigenvalues':np.linalg.eigvalsh(DeltaH).tolist(),'abstract_total_Delta_min':float(np.linalg.eigvalsh(Delta).min()),'abstract_conservative_identity_error':float(identity),'abstract_conservative_zero_corner_error':float(np.linalg.norm((np.eye(3)-q)@cons(q),2))}
assert maxcross<1e-12 and maxcomm<1e-12 and newbad<1e-12
assert negative>.4 and np.linalg.eigvalsh(DeltaH)[0]<-.1
assert np.linalg.eigvalsh(Delta).min()>-1e-12 and identity<1e-12
assert res['abstract_conservative_zero_corner_error']<1e-12
print(json.dumps(res,indent=2))
open(__file__.replace('.py','.json'),'w').write(json.dumps(res,indent=2)+'\n')
