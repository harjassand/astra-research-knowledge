"""Independent finite actual-monitor fixture; no effective dephasing.
Q0,Q1 and the R(Q1) abort leaf, one four-label resource, both real
2-level monitors. Keeps exact fast cleanup and complete abort reset.
This regression supplements, not replaces, the general proof.
"""
import json
import numpy as np
from scipy.linalg import solve, eigvalsh, eigh
P,L,M=3,4,2
n=P*L*M*M
ix=lambda p,l,a,b: (((p*L+l)*M+a)*M+b)
I=np.eye(n)
bad=np.zeros(n,bool)
for p in range(P):
 for l in range(L):
  for a in range(M):
   for b in range(M): bad[ix(p,l,a,b)]=(p==2 or (p==1 and l in [1,2]))
B=np.diag(bad.astype(float)); G=I-B
Hmain=np.zeros((n,n),complex)
def edge(i,j,v): Hmain[i,j]+=v;Hmain[j,i]+=v
for l in range(L):
 for a in range(M):
  for b in range(M):
   if l in [0,3]:edge(ix(0,l,a,b),ix(1,l,a,b),.7) # verified absence
   if l in [1,2]:edge(ix(1,l,a,b),ix(2,l,a,b),.8) # actual failed test
for p in [0,1]: # transactional R cleanup remains disabled
 for a in range(M):
  for b in range(M):edge(ix(p,1,a,b),ix(p,2,a,b),1.1)
Hhub=np.zeros_like(Hmain); Hres=np.zeros_like(Hmain); Hown=np.zeros_like(Hmain)
for p in range(P):
 for l in range(L):
  for b in range(M): Hhub[ix(p,l,0,b),ix(p,l,1,b)]=Hhub[ix(p,l,1,b),ix(p,l,0,b)]=.9
  for a in range(M):
   i,j=ix(p,l,a,0),ix(p,l,a,1)
   Hres[i,j]=Hres[j,i]=.6
   if l in [1,2]:Hown[i,j]=Hown[j,i]=.6
jumps=[]
def jump(mapping,rate):
 j=np.zeros((n,n),complex)
 for src,dst in mapping:j[dst,src]=np.sqrt(rate)
 return j
jumps.append(jump([(ix(2,l,a,b),ix(0,l,a,b)) for l in range(L) for a in range(M) for b in range(M)],1.3))
jumps.append(jump([(ix(p,2,a,b),ix(p,0,a,b)) for p in range(P) for a in range(M) for b in range(M)],.5))
for p in range(P):jumps.append(jump([(ix(p,l,1,b),ix(p,l,0,b)) for l in range(L) for b in range(M)],1.2))
resmon=[jump([(ix(p,l,a,1),ix(p,l,a,0)) for p in range(P) for a in range(M)],1.4) for l in range(L)]
bi=np.where(bad)[0];d=len(bi);Ib=np.eye(d)
def killed(H,js):
 h=H[np.ix_(bi,bi)];K=1j*(np.kron(Ib,h)-np.kron(h.T,Ib))
 for j in js:
  jb=j[np.ix_(bi,bi)];aa=(j.conj().T@j)[np.ix_(bi,bi)]
  K+=np.kron(jb.T,jb.conj().T)-.5*(np.kron(Ib,aa)+np.kron(aa.T,Ib))
 r=solve(K,-Ib.reshape(-1,order='F')).reshape((d,d),order='F');r=(r+r.conj().T)/2
 return K,r
Kown,Rown=killed(Hmain+Hhub+Hown,jumps+[resmon[1],resmon[2]])
Kfull,Rfull=killed(Hmain+Hhub+Hres,jumps+resmon)
R=np.zeros_like(Hmain);R[np.ix_(bi,bi)]=Rfull
rmin,rmax=eigvalsh(Rfull)[[0,-1]];Rmax=1.1*rmax;beta=.2/Rmax;s0=1-beta*Rmax
S=G+s0*B+beta*R
def psqrt(X):
 e,v=eigh((X+X.conj().T)/2);assert e[0]>-1e-12
 return (v*np.sqrt(np.maximum(e,0)))@v.conj().T
A=psqrt(S);C=psqrt(I-S)
erase=[jump([(ix(p,l,a,b),ix(0,l,a,b)) for l in range(L) for a in range(M) for b in range(M)],1) for p in range(P)]
ks=[A]+[e@C for e in erase]
T=lambda X:sum(k.conj().T@X@k for k in ks)
def adj(H,js,X):
 out=1j*(H@X-X@H)
 for j in js:
  q=j.conj().T@j;out+=j.conj().T@X@j-.5*(q@X+X@q)
 return (out+out.conj().T)/2
Aheal=-adj(Hmain+Hhub+Hres,jumps+resmon,B)
F=T(B)
service=adj(Hmain+Hhub+Hres,jumps+resmon,F)+beta*B+s0*Aheal
# Exact full owner algebra equality under the actual omitted monitor pieces.
other_action=adj(Hres-Hown,[resmon[0],resmon[3]],R)
# S is identity on good; raw flag no-jump order and unchanged good/bad blocks.
result={
 'full_controller_dimension':n,'bad_dimension':d,
 'full_vs_owned_resolvent_error':float(np.linalg.norm(Rown-Rfull)),
 'full_killed_residual':float(np.linalg.norm(Kfull@Rfull.reshape(-1,order='F')+Ib.reshape(-1,order='F'))),
 'resolvent_min':float(rmin),'resolvent_max':float(rmax),
 'omitted_monitor_adjoint_on_R':float(np.linalg.norm(other_action)),
 'OWN_monitor_noncommutation':float(np.linalg.norm(R@resmon[1]-resmon[1]@R)),
 'unitality':float(np.linalg.norm(T(I)-I)),
 'credited_flag_identity':float(np.linalg.norm(F-B@S)),
 'full_service_identity_error':float(np.linalg.norm(service)),
 'no_creation':float(max(np.linalg.norm(B@j@G) for j in jumps+resmon)),
 'Hamiltonian_flag_commutator':float(np.linalg.norm((Hmain+Hhub+Hres)@B-B@(Hmain+Hhub+Hres))),
 'nojump_order_min':float(eigvalsh(A@B@A-np.min(eigvalsh(S))*B)[0]),
}
assert rmin>0
assert result['OWN_monitor_noncommutation']>1e-4
for key in ['full_vs_owned_resolvent_error','full_killed_residual','omitted_monitor_adjoint_on_R','unitality','credited_flag_identity','full_service_identity_error','no_creation','Hamiltonian_flag_commutator']:assert result[key]<1e-10,(key,result[key])
print(json.dumps(result,indent=2))
