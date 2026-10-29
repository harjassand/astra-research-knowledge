import numpy as np,json,math
from scipy.linalg import eigh,expm
from functools import reduce
from collections import defaultdict
rng=np.random.default_rng(2026102907)
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1]).astype(complex)]
kron=lambda xs:reduce(np.kron,xs)
n=4;d=16;m=2
ops=[[kron([P[a] if i==j else P[0] for i in range(n)]) for j in range(n)] for a in range(1,4)]
J=[sum(x)/2 for x in ops];v,Z=eigh(sum(A@A for A in J));E=Z[:,v<1e-8];K=E.shape[1];Ps=E@E.conj().T;Qbasis=Z[:,v>=1e-8];C=(n-1)*E.shape[1]/K
Ss=[]
for i in range(n):
 for j in range(i+1,n):
  idx=[]
  for x in range(d):
   a=(x>>(n-1-i))&1;b=(x>>(n-1-j))&1;idx.append(x^(((a^b)<<(n-1-i))|((a^b)<<(n-1-j))))
  Ss.append(np.eye(d)[idx])
Ds=[E.conj().T]+[np.outer(np.eye(K)[:,0],q.conj()) for q in Qbasis.T]
def ptrD(r):return np.einsum('abad->bd',r.reshape(d,m,d,m))
def super_from(fun):
 B=[]
 for i in range(m*m):
  x=np.zeros((m,m),complex);x.reshape(-1)[i]=1;B.append(fun(x).reshape(-1))
 return np.stack(B,axis=1)
def effect(S):return (S.conj().T@np.eye(m).reshape(-1)).reshape(m,m)
fixtures=[];maps=[]
for variant in range(2):
 H=rng.normal(size=(d*m,d*m))+1j*rng.normal(size=(d*m,d*m));H=(H+H.conj().T)/(2*np.sqrt(d*m));U=expm(-1j*(.45+.2*variant)*H)
 As=[np.kron(D,np.eye(m))@U@np.kron(E,np.eye(m)) for D in Ds]
 Bs=[]
 for pauli in P:
  Bs.append([np.einsum('aiaj->ij',(np.kron(pauli.conj().T,np.eye(m))@A).reshape(K,m,K,m))/K for A in As])
 phis=[super_from(lambda sig,b=b:sum(A@sig@A.conj().T for A in b)) for b in Bs]
 good=phis[0];bad=sum(phis[1:]);testmaps=[]
 for fail in [False,True]:
  def apply(sig):
   out=np.zeros((m,m),complex)
   for S in Ss:
    for s in [-1,1]:
     Pi=(np.eye(d)+s*S)/2;Pt=(np.eye(d)+(-s if fail else s)*S)/2
     rho=np.kron(Pi@Ps/E.shape[1],sig);Y=np.kron(Pt,np.eye(m));out+=ptrD(Y@U@rho@U.conj().T@Y)/len(Ss)
   return out
  testmaps.append(super_from(apply))
 F=effect(testmaps[1]);W=effect(bad);mineig=np.linalg.eigvalsh(C*F-W).min()
 # Exact full joint twirl equality on a random correlated logical-memory density matrix.
 X=rng.normal(size=(K*m,K*m))+1j*rng.normal(size=(K*m,K*m));rho=X@X.conj().T;rho/=np.trace(rho)
 direct=sum(np.kron(Q,np.eye(m))@A@np.kron(Q,np.eye(m))@rho@np.kron(Q,np.eye(m))@A.conj().T@np.kron(Q,np.eye(m)) for Q in P for A in As)/4
 instrument=sum(np.kron(Q,B)@rho@np.kron(Q,B).conj().T for Q,bs in zip(P,Bs) for B in bs)
 residual=np.linalg.norm(direct-instrument)
 assert mineig>-1e-10 and residual<1e-11 and np.linalg.norm(effect(good+bad)-np.eye(m))<1e-11 and np.linalg.norm(effect(sum(testmaps))-np.eye(m))<1e-11
 maps.append({'good':good,'bad':bad,'pass':testmaps[0],'fail':testmaps[1]})
 fixtures.append({'variant':variant,'operator_hazard_min_eigenvalue':float(mineig),'joint_twirl_residual':float(residual),'bad_effect':W.tolist(),'failure_effect':F.tolist()})
# Exact finite process DP with bath density matrices, history-dependent source variant.
s=.2;a=1-s;Jtarget=5;bmax=1;t=1;cap=35;R=C*s/a;p=1/(1+R);u=1-p
sigma=np.array([[.6,.12j],[-.12j,.4]],complex);states={(0,0,0,0):sigma.reshape(-1)};accepted=accepted_bad=aborted=0.
for r in range(cap):
 nxt={}
 for (services,faults,fails,lastfail),sig in states.items():
  M=maps[(lastfail+r)%2]
  for kind,prob in [('good',s),('bad',s),('pass',a),('fail',a)]:
   out=prob*(M[kind]@sig);ss=services+int(kind in ['good','bad']);ff=faults+int(kind=='bad');bb=fails+int(kind=='fail');lf=1 if kind=='fail' else (0 if kind=='pass' else lastfail);w=float(np.trace(out.reshape(m,m)).real)
   if bb>bmax:aborted+=w
   elif ss==Jtarget:accepted+=w;accepted_bad+=w*int(ff>t)
   else:
    key=(ss,ff,bb,lf);nxt[key]=nxt.get(key,np.zeros(m*m,complex))+out
 states=nxt
aborted+=sum(float(np.trace(x.reshape(m,m)).real) for x in states.values())
tail=sum(math.comb(t+j,j)*u**(t+1)*p**j for j in range(bmax+1))
assert abs(accepted+aborted-1)<1e-10 and accepted_bad<=tail+1e-10
# A saturating classical hazard process approaches exact comparison NB tail; no source IID needed for proof.
print(json.dumps({'seed':2026102907,'scope':'n4 bath-memory instrument and finite-count guard fixture; outer q8 correction is a separate exact-field fixture, not this same end-to-end Hilbert space','inner_logical_dimension':K,'C':C,'fixtures':fixtures,'finite_memory_guard':{'J_service_count':Jtarget,'fault_threshold':t,'test_failure_budget':bmax,'cap':cap,'service_probability':s,'R':R,'accept_probability':accepted,'accepted_bad_fault_probability':accepted_bad,'abort_probability':aborted,'NB_bound':tail}},default=lambda z:[z.real,z.imag] if isinstance(z,complex) else z,indent=2))
