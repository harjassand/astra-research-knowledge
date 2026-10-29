#!/usr/bin/env python3
import numpy as np, itertools, math, json, pathlib, hashlib
from scipy.linalg import expm
R=pathlib.Path(__file__).resolve().parent
rng=np.random.default_rng(202610290418)
def singlet(M):
 v=np.zeros(16)
 for c in range(4):
  ix=0;s=1
  for j,(a,b) in enumerate(M):
   bit=(c>>j)&1;ix|=1<<(a if bit else b);s*=(-1 if bit else 1)
  v[ix]=s/2
 return v
X=np.column_stack([singlet(m) for m in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]])
V=np.linalg.svd(X,full_matrices=False)[0][:,:2]
perms=[]
for p in itertools.permutations(range(4)):
 ix=np.array([sum(((x>>i)&1)<<p[i] for i in range(4)) for x in range(16)])
 W=np.eye(16)[ix,:];U=V.T@W@V
 assert np.linalg.norm(W@V-V@U)<1e-12
 perms.append((W,U))
def iso(a,b):
 Q,_=np.linalg.qr(rng.normal(size=(a,b))+1j*rng.normal(size=(a,b)));return Q

def choi(Ks):
 return sum(np.outer(k.ravel(),k.ravel().conj()) for k in Ks)
def effect(Ks):return sum(k.conj().T@k for k in Ks)
def apply(Ks,x):return sum(k@x@k.conj().T for k in Ks)
def ptrout(x,D,mo):return np.einsum('aiaj->ij',x.reshape(D,mo,D,mo))
def ptrin(x,d,mi):return np.einsum('aiaj->ij',x.reshape(d,mi,d,mi))
D,d,mi,mo=16,2,2,3
rows=[]
for c in range(20):
 K=list(iso(D*mo*3,d*mi).reshape(3,D*mo,d*mi))
 # Half the fixtures include a dominant ideal component, not only near-maximally
 # noisy generic channels.
 if c%2==0:
  B=np.zeros((mo,mi));B[:mi,:]=np.eye(mi)
  K=[np.sqrt(.8)*np.kron(V,B)]+[np.sqrt(.2)*k for k in K]
 Bs=[np.einsum('iiab->ab',np.einsum('xp,xayb->pyab',V.conj(),k.reshape(D,mo,d,mi)))/d for k in K]
 good=[np.kron(V,b) for b in Bs]
 Ktw=[];bad=[]
 for W,U in perms:
  for k,b in zip(K,Bs):
   kg=np.kron(W.conj().T,np.eye(mo))@k@np.kron(U,np.eye(mi))
   Ktw.append(kg/np.sqrt(24));bad.append((kg-np.kron(V,b))/np.sqrt(24))
 J=choi(Ktw);Jg=choi(good);Jb=choi(bad)
 split=float(np.linalg.norm(J-Jg-Jb))
 H=np.eye(mi)-sum(b.conj().T@b for b in Bs)
 eff=float(np.linalg.norm(effect(bad)-np.kron(np.eye(d),H)))
 # Check the complete reduced-memory superoperator on all matrix units, not
 # merely a handful of independent carrier states.
 marg=0.
 for i,j,a,b in itertools.product(range(d),range(d),range(mi),range(mi)):
  E=np.zeros((d*mi,d*mi),complex);E[i*mi+a,j*mi+b]=1
  Mab=np.zeros((mi,mi),complex);Mab[a,b]=1
  actual=ptrout(apply(bad,E),D,mo)
  expected=ptrout(apply(bad,np.kron(np.eye(d)/d,Mab)),D,mo)*(i==j)
  marg=max(marg,float(np.linalg.norm(actual-expected)))
 # Correlated carrier-memory state.
 psi=iso(d*mi,1).ravel();rho=np.outer(psi,psi.conj())
 stateerr=float(np.linalg.norm(apply(Ktw,rho)-apply(good,rho)-apply(bad,rho)))
 prob=float(np.trace(apply(bad,rho)).real)
 expectedprob=float(np.trace(H@ptrin(rho,d,mi)).real)
 assert max(split,eff,marg,stateerr,abs(prob-expectedprob))<2e-11
 rows.append({'case':c,'choi_split_residual':split,'effect_residual':eff,
  'full_memory_superoperator_residual':marg,'correlated_state_split_residual':stateerr,
  'correlated_bad_probability_error':abs(prob-expectedprob),'bad_probability':prob})
# A retained-key countercheck, using a traceless unitary on the singlet logical
# qubit. Each key block has distance |sin(theta)| from identity; discarding
# that key gives sin²(theta), checked directly from Choi trace norms.
Z=np.diag([1.,-1.]);theta=.1
K=[];keydistance=0
idvec=np.eye(d).ravel()/np.sqrt(d);Jid=np.outer(idvec,idvec)
for W,U in perms:
 a=U.T@expm(1j*theta*Z)@U
 ja=np.outer(a.ravel(),a.ravel().conj())/d
 keydistance+=np.sum(np.abs(np.linalg.eigvalsh(ja-Jid)))/48
 K.append(a/np.sqrt(24))
Jt=choi(K)/d
retired_choinorm=float(np.sum(np.abs(np.linalg.eigvalsh(Jt-Jid)))/2)
assert abs(retired_choinorm-np.sin(theta)**2)<1e-12
assert abs(keydistance-abs(np.sin(theta)))<1e-12
# Multiplicity-two output is a genuine counterexample to the norm identity.
# V1,V2 carry identical irreps. W=(V1+V2)/sqrt2 remains an intertwiner.
I=np.eye(d);V1=np.vstack([I,np.zeros_like(I)]);V2=np.vstack([np.zeros_like(I),I]);A=(V1+V2)/np.sqrt(2)
v1=V1.ravel()/np.sqrt(d);aa=A.ravel()/np.sqrt(d)
copydist=float(np.sum(np.abs(np.linalg.eigvalsh(np.outer(v1,v1)-np.outer(aa,aa))))/2)
assert abs(copydist-1/np.sqrt(2))<1e-12
out={'status':'author numerical checks, awaiting independent review','n':4,'singlet_dimension':2,'physical_output_dimension':16,'memory_input_dimension':2,'memory_output_dimension':3,
'group_size':24,'cases':rows,'all_checks_passed':True,
'key_retirement_counterexample':{'theta':theta,'retained_key_half_choi_distance':float(keydistance),'retired_key_half_choi_distance':retired_choinorm,'sin_theta':float(np.sin(theta)),'sin2_theta':float(np.sin(theta)**2)},
'multiplicity_two_counterexample':{'raw_infidelity':.5,'actual_half_distance':copydist},
'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(R/'check_joint_twirl_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'case_count':len(rows),'max_choi_split':max(x['choi_split_residual'] for x in rows),'max_memory_closure':max(x['full_memory_superoperator_residual'] for x in rows),'retained_key':float(keydistance),'retired_key':retired_choinorm,'multiplicity_two_distance':copydist},indent=2))
