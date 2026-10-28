"""Ordinary per-call RNG pilot. Floating signs/circuit diagnostics, not certified hardware."""
from pathlib import Path
import numpy as np,itertools,json,sys,hashlib
ROOT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);PA=[I,X,Y,Z]
def kron(xs):
 r=np.array([[1]],complex)
 for a in xs:r=np.kron(r,a)
 return r
def signmat(a):
 ev,v=np.linalg.eigh((a+a.conj().T)/2);return (v*np.where(ev>=0,1.,-1.))@v.conj().T
rng=np.random.default_rng(28101901);a=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));V,R=np.linalg.qr(a);V=V@np.diag(np.diag(R)/abs(np.diag(R))).conj()
e=[0,4,2,1];Um=np.zeros((8,8),complex)
for l in range(2):
 for g in range(4):Um[e[g]^(7*l),4*l+g]=1
U=V@Um
basis=[np.array([[1,1],[1,-1]],complex)/np.sqrt(2),np.array([[1,1],[1j,-1j]],complex)/np.sqrt(2),I]
settings=list(itertools.product(range(3),repeat=3));meas=[kron([basis[a] for a in ss]) for ss in settings]
shadow=np.empty((27,8,8,8),complex)
for si,ss in enumerate(settings):
 for o in range(8):
  shadow[si,o]=kron([3*np.outer(basis[ss[t]][:,((o>>(2-t))&1)],basis[ss[t]][:,((o>>(2-t))&1)].conj())-I for t in range(3)])
prob=np.empty((2,2,4,8,27,8))
for ax,sg,g,err in itertools.product(range(2),range(2),range(4),range(8)):
 s=2*sg-1;psi=np.zeros(8,complex)
 if ax==0:psi[e[g]]=1/np.sqrt(2);psi[e[g]^7]=s/np.sqrt(2)
 else:psi[e[g] if s==1 else e[g]^7]=1
 noisy=V@psi[np.arange(8)^err]
 for si,B in enumerate(meas):prob[ax,sg,g,err,si]=abs(B.conj().T@noisy)**2
assert np.max(abs(prob.sum(-1)-1))<3e-14
P0=np.diag([1,0]);P1=np.diag([0,1]);I8=np.eye(8)
def effects(sx,sz):
 cz=(np.kron(I8+sz,I)+np.kron(I8-sz,X))/2
 cx=np.kron(I8,P0)+np.kron(sx,P1);W=cz@cx@cz
 Ts=[np.zeros((4,4),complex) for _ in PA]
 for po in range(8):
  for ain in range(2):
   K=np.empty((2,8),complex)
   for ao in range(2):K[ao]=W[2*po+ao,ain::2]/np.sqrt(2)
   A=K@U
   for pi,P in enumerate(PA):
    row=sum((P.conj().T[aa,bb]*A[bb,aa*4:(aa+1)*4] for aa in range(2) for bb in range(2)),np.zeros(4,complex))/2
    Ts[pi]+=np.outer(row.conj(),row)
 assert np.max(abs(sum(Ts)-np.eye(4)))<2e-12
 return Ts,float(np.max(abs(W.conj().T@W-np.eye(16))))
trueX=U@np.kron(X,np.eye(4))@U.conj().T;trueZ=U@np.kron(Z,np.eye(4))@U.conj().T
Ttrue,_=effects(trueX,trueZ);assert np.max(abs(Ttrue[0]-np.eye(4)))<2e-13
signs=np.array([-1,1]);injbit=np.array([[(-1)**((j>>(2-t))&1) for t in range(3)] for j in e]);inj_sum=injbit.sum(1)
results=[];banks=[];counts_saved=[];seed=28102000
for p,N,rep in itertools.product([0.,.01,.1,.4],[512,2048,8192],range(16)):
 w=np.array([p**int(f).bit_count()*(1-p)**(3-int(f).bit_count()) for f in range(8)]);gi=w[e];gx=w[[7^j for j in e]];oracle=float(gx.sum())
 for active in [False,True]:
  seed+=1;rr=np.random.default_rng(seed);ax=rr.integers(0,2,N);sg=rr.integers(0,2,N);g=rr.integers(0,4,N) if active else np.zeros(N,int)
  erbits=rr.random((N,3))<p;err=erbits@np.array([4,2,1]);si=rr.integers(0,27,N);u=rr.random(N)
  cdf=prob[ax,sg,g,err,si].cumsum(-1);out=(u[:,None]>cdf).sum(1);assert np.max(out)<8
  flat=((((ax*2+sg)*4+g)*27+si)*8+out);cts=np.bincount(flat,minlength=2*2*4*27*8).reshape(2,2,4,27,8)
  counts_saved.append(cts.astype(np.uint32));bankid=len(banks)
  banks.append({'bank_id':bankid,'p':p,'N':N,'rep':rep,'active':active,'seed':seed,'actual_calls':N})
  def matrix(axidx,iw):
   weight=np.einsum('sgko,s,g->ko',cts[axidx],signs,iw)
   return 2*np.einsum('ko,koab->ab',weight,shadow)/N
  mx=matrix(0,np.ones(4));mz=matrix(1,np.ones(4));sx=signmat(mx)
  methods={'active_unlabelled' if active else 'native_unlabelled':signmat(mz)}
  if active:
   methods['active_label_sum']=signmat(matrix(1,inj_sum))
   methods['active_label_triple']=signmat(sum(signmat(matrix(1,injbit[:,i])) for i in range(3)))
  for name,sz in methods.items():
   tt,uniterr=effects(sx,sz);fidelity=float(np.dot(gi,np.diag(tt[0]).real)+np.dot(gx,np.diag(tt[1]).real));loss=1-fidelity;excess=loss-oracle
   assert excess>-2e-12
   b=float(1-np.linalg.eigvalsh(tt[0]).min());assert -2e-12<=b<=1+2e-12
   results.append({'bank_id':bankid,'method':name,'p':p,'N':N,'rep':rep,'oracle_native_loss':oracle,'native_loss':loss,'native_excess':excess,'worst_gauge_virtual_loss':b,'unitarity_residual':uniterr})
summary=[]
for p,N,name in itertools.product([0.,.01,.1,.4],[512,2048,8192],['native_unlabelled','active_unlabelled','active_label_sum','active_label_triple']):
 rows=[r for r in results if r['p']==p and r['N']==N and r['method']==name]
 summary.append({'p':p,'N':N,'method':name,'mean_native_excess':float(np.mean([r['native_excess'] for r in rows])),'mean_worst_gauge_loss':float(np.mean([r['worst_gauge_virtual_loss'] for r in rows])),'runs':len(rows)})
np.savez_compressed(ROOT/'ordinary_counts.npz',counts=np.stack(counts_saved))
meta={'status':'PASS_FLOATING_ORDINARY_CALL_AND_COHERENT_RECEIVER_PILOT','python':sys.version,'numpy':np.__version__,'source_seed':28101901,'source_V_real':V.real.tolist(),'source_V_imag':V.imag.tolist(),'actual_individually_rng_simulated_calls':sum(b['actual_calls'] for b in banks),'independent_calibration_banks':len(banks),'decoder_evaluations':len(results),'paired_estimators_note':'Three active estimators reuse the SAME active bank; they are not independent acquisition data. Native banks are separate. Different N banks are independent, not prefixes.','learner_access':'Only actual input axis/sign, chosen injection label, output Pauli axes/outcomes; source V,p used solely for generation and posthoc scoring.','not_claimed':['hardware','finite rational sign/Jacobi execution','gate synthesis','certified acceptance at these budgets','generic unknown-noise guarantee','advantage over every equally informed conventional estimator'],'summary':summary,'banks':banks,'results':results,'counts_file':'ordinary_counts.npz','counts_sha256':hashlib.sha256((ROOT/'ordinary_counts.npz').read_bytes()).hexdigest()}
(ROOT/'results.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:meta[k] for k in ['status','actual_individually_rng_simulated_calls','independent_calibration_banks','decoder_evaluations']},indent=2));print(json.dumps([x for x in summary if x['N']==8192],indent=2))
