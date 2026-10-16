import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np,json,pathlib
from scipy.linalg import expm,eigvalsh
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);Ps=[I,X,Y,Z];gens=[X,Z];rates=[2.,3.];T=.7;J=.4
kron=np.kron
def comm_L(H):
 n=len(H);return -1j*(kron(np.eye(n),H)-kron(H.T,np.eye(n)))
def jump_L(C):return kron(C.conj(),C)-np.eye(len(C)**2)
H=kron(X,X)+.7*kron(Z,Y)+.3*kron(Y,Z)
H*=J/np.linalg.norm(H,2)
# Ordering D,R,B.
HL=sum(kron(kron(P,I),B) for P,B in [(X,X), (Z,.7*Y),(Y,.3*Z)])
HL*=J/np.linalg.norm(kron(X,X)+.7*kron(Z,Y)+.3*kron(Y,Z),2)
Cs=[kron(kron(g,g.T),I) for g in gens]
L=comm_L(HL)+sum(r*jump_L(c) for r,c in zip(rates,Cs))
# Exact classical telegraph toggling generator, frame order I,X,Y,Z.
chars=np.array([[int(round(np.trace(g@p@g@p).real/2)) for g in gens] for p in Ps])
K=np.zeros((256,256),complex)
for f,F in enumerate(Ps):
 C=kron(kron(F,F.T),I);sl=slice(64*f,64*(f+1));K[sl,sl]=comm_L(C@HL@C.conj().T)
 for g,r in zip(gens,rates):
  target=next(j for j,P in enumerate(Ps) if abs(np.trace(P.conj().T@g@F))>1.9)
  K[sl,sl]-=r*np.eye(64);K[64*target:64*(target+1),sl]+=r*np.eye(64)
EL=expm(T*L);EK=expm(T*K)
phi=np.array([1,0,0,1])/np.sqrt(2);bells=[kron(p,I)@phi for p in Ps];Q=[kron(np.outer(v,v.conj()),I) for v in bells]
effect=np.zeros((2,2),complex);diff=0.
for b in range(2):
 for c in range(2):
  E=np.zeros((2,2));E[b,c]=1;rho=kron(np.outer(phi,phi.conj()),E);v=rho.reshape(-1,order='F')
  lifted=(EL@v).reshape(8,8,order='F');vin=np.zeros(256,complex);vin[:64]=v
  cv=EK@vin;classic=sum(cv[64*f:64*(f+1)].reshape(8,8,order='F') for f in range(4))
  for q in Q:diff=max(diff,abs(np.trace(q@(lifted-classic))))
  effect[c,b]=sum(np.trace(q@lifted) for q in Q[1:])
M=np.zeros((16,16))
for a in range(4):
 for b in range(4):
  row=4*a+b;M[row,row]=-2*sum(r for r,ca,cb in zip(rates,chars[a],chars[b]) if ca!=cb)
  for c in range(4):
   if c!=a:M[row,4*c+b]+=J
   if c!=b:M[row,4*a+c]+=J
EM=expm(T*M);qgroup=sum(EM[4*a+a,0] for a in range(1,4))
# Full joint-system Pauli-twirl identity for one arbitrary path unitary.
U=expm(-1j*T*H);Bs=[]
for P in Ps:
 A=(kron(P,I)@U).reshape(2,2,2,2);Bs.append(np.einsum('abad->bd',A)/2)
rng=np.random.default_rng(93);v=rng.normal(size=4)+1j*rng.normal(size=4);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
twirled=sum((kron(F,I)@U@kron(F,I))@rho@(kron(F,I)@U@kron(F,I)).conj().T for F in Ps)/4
labelled=sum(kron(P,B)@rho@kron(P,B).conj().T for P,B in zip(Ps,Bs))
completeness=sum(B.conj().T@B for B in Bs)
res={'lifted_vs_classical_endpoint_effect_max_difference':float(diff),'lifted_error_effect_eigenvalues':eigvalsh(effect).tolist(),'group_majorant':float(qgroup),'effect_bound_pass':bool(eigvalsh(effect).max()<=qgroup+1e-10),'joint_data_bath_twirl_identity_error':float(np.linalg.norm(twirled-labelled)),'bath_Kraus_completeness_error':float(np.linalg.norm(completeness-I)),'conjugation_generators_commutator_norm':float(np.linalg.norm(Cs[0]@Cs[1]-Cs[1]@Cs[0])),'normalization':'normalized Bell vector; Bp=Tr_D(P†U)/2','parameters':{'J':J,'rates':rates,'T':T}}
assert diff<1e-12 and np.linalg.norm(twirled-labelled)<1e-12 and res['effect_bound_pass']
p=pathlib.Path(__file__).parent;(p/'exact_matrix_check.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
