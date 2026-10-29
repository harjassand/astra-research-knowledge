import numpy as np,itertools,json
from pathlib import Path
rng=np.random.default_rng(20261029)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex);PS=[I,X,Y,Z]
def choi(ks):
 v=np.array([k.reshape(-1) for k in ks]);return v.T@v.conj()
def random_channel(ni,no,r):
 a=rng.normal(size=(r*no,ni))+1j*rng.normal(size=(r*no,ni));q=np.linalg.qr(a)[0];return list(q.reshape(r,no,ni))
def conjugates(ks,gs,mi,mo):return [[np.kron(g.conj().T,np.eye(mo))@k@np.kron(g,np.eye(mi)) for k in ks] for g in gs]
def accepted(kg,m):
 out=np.zeros_like(choi(kg[0]));N=len(kg)
 for keys in itertools.product(range(N),repeat=m):out+=choi([sum(kg[j][a] for j in keys)/m for a in range(len(kg[0]))])/N**m
 return out
def cp_checks(ks,b,mi,mo):
 out=np.zeros_like(choi(ks))
 for pad in PS:
  kk=[np.kron(pad,np.eye(mo))@k@np.kron(pad,np.eye(mi)) for k in ks]
  for checks in itertools.product(PS,repeat=b):
   filt=kk
   for p in checks:filt=[(k+np.kron(p,np.eye(mo))@k@np.kron(p,np.eye(mi)))/2 for k in filt]
   out+=choi(filt)/4**(b+1)
 return out
results=[]
for trial in range(8):
 mi=2;mo=3;ks=random_channel(4,6,3);kg=conjugates(ks,PS,mi,mo)
 means=[sum(v[a] for v in kg)/4 for a in range(3)]
 good=choi(means);tw=sum(choi(v) for v in kg)/4;bad=tw-good
 for b in [1,2]:
  m=2**b;actual=accepted(kg,m);cpc=cp_checks(ks,b,mi,mo)
  target=good+bad/m
  results.append(dict(trial=trial,b=b,multibranch=float(np.max(abs(actual-target))),cpc=float(np.max(abs(cpc-target))),bad_min_eigen=float(np.linalg.eigvalsh(bad)[0])))
# Actual full flag-controlled matrix against accepted amplitude on a random key list.
ks=random_channel(4,6,3);keys=[0,1,3,2];m=4
pre=np.zeros((m*4,m*4),complex);post=np.zeros((m*6,m*6),complex)
for j,g in enumerate(keys):pre[j*4:(j+1)*4,j*4:(j+1)*4]=np.kron(PS[g],I);post[j*6:(j+1)*6,j*6:(j+1)*6]=np.kron(PS[g].conj().T,np.eye(3))
vin=np.kron(np.ones((m,1))/np.sqrt(m),np.eye(4));vout=np.kron(np.ones((1,m))/np.sqrt(m),np.eye(6))
kg=conjugates(ks,PS,2,3)
circuit=max(np.max(abs(vout@post@np.kron(np.eye(m),k)@pre@vin-sum(kg[j][a] for j in keys)/m)) for a,k in enumerate(ks))
# Leakage: qutrit replacer |2><i|, input code span 0,1; projective phase choices matter.
leakks=[np.outer(np.eye(3)[:,2],np.eye(3)[:,i]) for i in range(3)]
def physical_avg(gs):
 kg=conjugates(leakks,gs,1,1); kg=[[k[:,:2] for k in row] for row in kg]
 mean=[sum(row[a] for row in kg)/len(gs) for a in range(3)]
 tw=sum(choi(row) for row in kg)/len(gs)
 act=accepted(kg,2)
 return dict(mean_kraus_norm=float(sum(np.linalg.norm(k)**2 for k in mean)),wrong_good_zero_residual=float(np.max(abs(act-tw/2))),actual_accept=float(np.trace(sum(k.conj().T@k for k in mean)).real/2/2+.5))
def ext(g):
 v=np.eye(3,dtype=complex);v[:2,:2]=g;return v
badphase=physical_avg([ext(p) for p in PS]);q8=physical_avg([ext(s*p) for p in [I,1j*X,1j*Y,1j*Z] for s in [-1,1]])
# Clifford comparator counts, exact finite Pauli alphabet, k=1..3,b=1..3.
counts=[]
for k in range(1,4):
 for b in range(1,4):
  d=2**k;m=2**b;den=d*d*m*m-1
  counts.append(dict(k=k,b=b,accepted_bad=m*(d*d-1)/den,accepted_harmless=(m-1)/den,filter_bad=1/m))
res=dict(scope='floating full Choi map checks, rectangular retained memory 2 to 3; no hardware',cases=results,full_controlled_circuit_residual=float(circuit),leakage_wrong_projective_extension=badphase,leakage_honest_Q8_extension=q8,clifford_counts=counts)
assert max(max(x['multibranch'],x['cpc']) for x in results)<1e-12
assert circuit<1e-12 and badphase['wrong_good_zero_residual']>.01 and q8['wrong_good_zero_residual']<1e-12
Path(__file__).with_name('results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
