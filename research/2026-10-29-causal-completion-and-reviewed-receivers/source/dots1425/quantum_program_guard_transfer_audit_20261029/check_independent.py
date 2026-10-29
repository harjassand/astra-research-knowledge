import numpy as np,json,hashlib,math
from pathlib import Path
p=Path(__file__).parent;src=p.parent/'astra_quantum_work/quantum_operational_certification_20261024/sequential_singlet_guard_20261029'
verified=0
for rn in ['RECEIPT_v1.json','RECEIPT_CORRELATED_v3.json']:
 for f,h in json.loads((src/'independent_audit'/rn).read_text())['sha256'].items():
  assert hashlib.sha256((src/f).read_bytes()).hexdigest()==h;verified+=1
rng=np.random.default_rng(1326);I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z]
probes=[np.array(v,complex)/np.linalg.norm(v) for v in [[1,0],[0,1],[1,1],[1,-1],[1,1j],[1,-1j]]]
def coeff(Ks,mi,mo):return [[np.einsum('ab,biaj->ij',pp.conj().T,K.reshape(2,mo,2,mi))/2 for K in Ks] for pp in P]
def adj(ks,E):return sum((k.conj().T@E@k for k in ks),np.zeros((ks[0].shape[1],ks[0].shape[1]),complex))
def test(Ks,mi,mo):
 passing=[];failing=[]
 for v in probes:
  w=np.array([-v[1].conjugate(),v[0].conjugate()])
  for K in Ks:
   A=K.reshape(2,mo,2,mi)
   passing.append(np.einsum('a,aibj,b->ij',v.conj(),A,v)/np.sqrt(6));failing.append(np.einsum('a,aibj,b->ij',w.conj(),A,v)/np.sqrt(6))
 return passing,failing
# Actual data-dependent controller record c is part of OUTPUT memory, not averaged away.
mi=2;mo=4;U=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))[0];Ks=[]
for c in range(2):
 weak=np.diag(np.sqrt([.9,.2] if c==0 else [.1,.8]));A=np.kron(P[c],I)@np.kron(weak,I)@U
 out=np.zeros((2,2,2,2,2),complex) # logicalout, oldmemoryout, record, logicalin, memoryin
 out[:,:,c,:,:]=A.reshape(2,2,2,2);Ks.append(out.reshape(8,4))
assert np.linalg.norm(sum(k.conj().T@k for k in Ks)-np.eye(4))<1e-12
bs=coeff(Ks,mi,mo);passing,failing=test(Ks,mi,mo);bad=[b for lst in bs[1:] for b in lst]
effect_res=float(np.linalg.norm(adj(bad,np.eye(mo))-1.5*adj(failing,np.eye(mo))))
assert effect_res<1e-12
# Correlated L-M-reference test with classical record retained.
v=rng.normal(size=12)+1j*rng.normal(size=12);v/=np.linalg.norm(v);rho=np.outer(v,v.conj());real=np.zeros((24,24),complex);tw=np.zeros_like(real)
for pp in P:
 for K in Ks:
  A=np.kron(np.kron(pp,np.eye(mo))@K@np.kron(pp,np.eye(mi)),np.eye(3));real+=A@rho@A.conj().T/4
for pp,lst in zip(P,bs):
 for b in lst:
  A=np.kron(np.kron(pp,b),np.eye(3));tw+=A@rho@A.conj().T
record_res=float(np.linalg.norm(real-tw));assert record_res<1e-12
# Finite guard with j-dependent ports and noncommuting pre-role memory refresh.
mi=mo=2;ports=[]
for z in range(3):
 V=np.linalg.qr(rng.normal(size=(12,4))+1j*rng.normal(size=(12,4)))[0];ks=list(V.reshape(3,4,4));bb=coeff(ks,2,2);tp,tf=test(ks,2,2);ports.append((bb[0],[b for lst in bb[1:] for b in lst],tp,tf))
rot=np.array([[np.cos(.31),-np.sin(.31)],[np.sin(.31),np.cos(.31)]],complex)
prep=[rot@np.diag([1,np.sqrt(.63)]),rot@np.array([[0,np.sqrt(.37)],[0,0]])]
s=.12;a=1-s;R=1.5*s/a;t=1;bmax=1;J=5;L=35
nb=sum(math.comb(t+j,j)*(R/(1+R))**(t+1)*(1/(1+R))**j for j in range(bmax+1))
zero=np.zeros((2,2),complex);eye=np.eye(2);F={(j,f,b):zero.copy() for j in range(J) for f in range(t+2) for b in range(bmax+1)}
for remaining in range(1,L+1):
 G={}
 def get(j,f,b):
  if b>bmax:return zero
  if j==J:return eye if f>t else zero
  return F[j,f,b]
 for j in range(J):
  good,bad,tp,tf=ports[j%3]
  for f in range(t+2):
   for b in range(bmax+1):
    E=s*adj(good,get(j+1,f,b))+s*adj(bad,get(j+1,min(t+1,f+1),b))+a*adj(tp,get(j,f,b))+a*adj(tf,get(j,f,b+1))
    G[j,f,b]=adj(prep,E)
 F=G
maxbad=float(np.linalg.eigvalsh(F[0,0,0])[-1]);assert maxbad<=nb+1e-12
out={'dependency_hashes_verified':verified,'record_output_memory_dimension':4,'record_retained_twirl_residual':record_res,'record_port_effect_identity_residual':effect_res,'adaptive_port_preparation_guard':{'services':J,'corrected_faults':t,'test_failure_budget':bmax,'trial_cap':L,'bad_accepted_effect_norm':maxbad,'negative_binomial_bound':nb,'scope':'j-dependent actual CPTP ports and common pre-role noncommuting memory preparation'},'scope':'Finite quantum-program/record/memory CP diagnostics, not the expensive learner or physical hardware; no yield inferred.'}
(p/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
