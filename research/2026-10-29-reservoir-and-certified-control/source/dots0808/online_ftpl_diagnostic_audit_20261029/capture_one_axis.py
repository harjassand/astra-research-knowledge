import numpy as np, math,json,itertools,time
from scipy.linalg import expm
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex); pa=[X,Y,Z]
def kron(xs):
 r=np.array([[1.]],complex)
 for x in xs:r=np.kron(r,x)
 return r
# Exact-rational-quaternion m=1 net; numeric representation only in this physical simulation.
Vs=[];Cs=[]
for k in itertools.product(range(-1,2),repeat=3):
 r=sum(x*x for x in k);q=np.array([1-r,*[2*x for x in k]],float)/(1+r)
 v=q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3))
 c=np.array([[np.trace(pa[a]@v@pa[b]@v.conj().T).real/2 for b in range(3)]for a in range(3)])
 Vs.append(v);Cs.append(c)
Vs=np.array(Vs);Cs=np.array(Cs);M=len(Vs);D=16;n=4
rng=np.random.default_rng(20261029);hidden=[13,2,19,24];hidden[0]=13 # index13 is k=(0,0,0), identity
V=kron([Vs[j] for j in hidden]);
def op_at(p,i):return kron([p if j==i else I for j in range(n)])
J=[sum(op_at(p,i) for i in range(n))/2 for p in pa]
# Full physical data+bath unitary; all commute with SAME hidden permutations.
Us=[]
for axis,theta in [(2,0),(2,.8),(0,.65),(1,.7),(2,.5),(0,.9)]:
 H=np.kron(V@J[axis]@V.conj().T,Z)+.37*np.kron(np.eye(D),X)
 Us.append(expm(-1j*theta*H))
Us=np.array(Us);U4=Us.reshape(6,D,2,D,2)
# Spin-zero basis, exact projector numerically diagonalized.
J2=sum(j@j for j in J);vals,vecs=np.linalg.eigh(J2);E0=vecs[:,vals<1e-10];d=E0.shape[1]
# State prep/readout vectors for Pauli axes/signs.
base=[]
for p in pa:
 ev,es=np.linalg.eigh(p);base.append({-1:es[:,0],1:es[:,1]})
# Precompute star swap loss effects on source memory, all candidates/source choices.
swaps=np.empty((3,M,D,D),complex)
for i in range(1,n):
 for ci,c in enumerate(Cs):
  swaps[i-1,ci]=.5*(np.eye(D)+sum(c[a,b]*op_at(pa[a],i)@op_at(pa[b],0) for a in range(3) for b in range(3)))
effects=np.empty((6,3,M,2,2),complex)
for z,u in enumerate(Us):
 for i in range(3):
  for ci,S in enumerate(swaps[i]):
   A=np.kron(S,I);Q=(A@u.conj().T@A@u).reshape(D,2,D,2)
   b=np.einsum('ambn->mn',Q*np.eye(D)[:,None,:,None])/D
   effects[z,i,ci]=I-b
# effect Hermiticity follows trace cyclic; diagnostic numerical symmetrization.
effects=(effects+effects.conj().transpose(0,1,2,4,3))/2
max_true=0
for z in range(6):
 for i in range(3):max_true=max(max_true,np.linalg.norm(effects[z,i,hidden[i+1]]))
assert max_true<1e-12
T=60000;p=.5;eta=1/(math.sqrt(50*T/(p*math.log(M)))+24/p)
logw=np.zeros((3,M));bath=np.array([[.7,.12j],[-.12j,.3]],complex);last=0
sums=dict(service_bad=0.,service_delta_bound=0.,selected_delta=0.,uniform_delta=0.);nprobe=0;nservice=0;blocks=[];max_gap=-1.; min_bad=1.;max_imag=0.
bank0=np.zeros((3,3,3),dtype=np.int64);bank2=np.zeros((3,3,3,3,3),dtype=np.int64)
start=time.time()
for t in range(T):
 # nonanticipating source rule changes after identity and one-axis periods,
 # and later uses previous actual probe parity; it never sees current draws.
 z=0 if t<T//10 else 1 # permanent one-axis collective noise after identity prefix
 probs=np.exp(logw-logw.max(axis=1)[:,None]);probs/=probs.sum(axis=1)[:,None]
 choices=[rng.choice(M,p=probs[i]) for i in range(3)]
 cur=np.einsum('ijm,mj->i',effects[z,np.arange(3),choices],bath).real
 uni=np.einsum('ikab,ba->ik',effects[z],bath).real.mean(axis=1)
 sums['selected_delta']+=cur.sum();sums['uniform_delta']+=uni.sum()
 if rng.random()<p:
  nprobe+=1;c=rng.integers(0,3,n);sign=rng.choice([-1,1],n);a=rng.integers(0,3,n)
  vin=kron([base[c[j]][int(sign[j])].reshape(2,1) for j in range(n)]).ravel()
  # Output basis columns indexed binary outcomes, signs -1,+1.
  bout=kron([np.column_stack([base[a[j]][-1],base[a[j]][1]]) for j in range(n)])
  A=np.einsum('yx,xmzn,z->ymn',bout.conj().T,U4[z],vin,optimize=True)
  weights=np.einsum('ymn,nk,ymk->y',A,bath,A.conj(),optimize=True).real
  weights=np.maximum(weights,0);weights/=weights.sum();out=int(rng.choice(D,p=weights))
  yy=np.array([1 if (out>>(n-1-j))&1 else -1 for j in range(n)])
  K=A[out];bath=K@bath@K.conj().T;bath/=np.trace(bath)
  for i in range(1,n):
   bank0[i-1,a[i],a[0]]+=int(yy[i]*yy[0])
   bank2[i-1,a[i],a[0],c[i],c[0]]+=int(yy[i]*yy[0]*sign[i]*sign[0])
   ca=Cs[:,a[i],a[0]];cc=Cs[:,c[i],c[0]]
   loss=.75-2.25*yy[i]*yy[0]*ca-20.25*yy[i]*yy[0]*sign[i]*sign[0]*ca*cc
   assert np.max(np.abs(loss))<=24+1e-10
   logw[i-1]-=eta*loss/p
  last=int(np.sum(yy<0)%4)
 else:
  nservice+=1;W=kron([I]+[Vs[j] for j in choices]);E=W@E0;P=E@E.conj().T
  # Bath Kraus matrix of the full-singlet good branch.
  B=np.einsum('yx,xmyn->mn',P,U4[z])/d
  good=np.trace(B@bath@B.conj().T).real;bad=1-good
  bnd=D/d*cur.sum();max_gap=max(max_gap,bad-bnd);min_bad=min(min_bad,bad)
  assert bad<=bnd+2e-12 and bad>=-2e-12
  sums['service_bad']+=bad;sums['service_delta_bound']+=bnd
  inp=P/d
  bath=np.einsum('amxi,xy,ij,am yj->mm',U4[z],inp,bath,U4[z].conj()) if False else np.trace((Us[z]@np.kron(inp,bath)@Us[z].conj().T).reshape(D,2,D,2),axis1=0,axis2=2)
  bath/=np.trace(bath)
 if (t+1)%(T//10)==0:
  blocks.append(dict(t=t+1,probe=nprobe,service=nservice,**sums,mean_service_bad=sums['service_bad']/max(1,nservice),mean_selected_delta=sums['selected_delta']/(t+1),mean_uniform_delta=sums['uniform_delta']/(t+1)))
result=dict(T=T,p=p,eta=eta,net_size=M,hidden_indices=hidden,source_choices='identity prefix then permanently one-axis Z collective noise with retained coherent bath',actual_probe_calls=nprobe,actual_service_calls=nservice,true_loss_effect_residual=max_true,max_transfer_violation=max_gap,min_bad=min_bad,final_bath_real=bath.real.tolist(),final_bath_imag=bath.imag.tolist(),blocks=blocks,seconds=time.time()-start,scope='Floating diagnostic for a finite rational net containing true frames; no high-probability or full outer-code execution. Actual product input/output probe sampling and retained bath updates; service uses exact averaged private-orbit memory interface.')
print(json.dumps(result,indent=2))

from pathlib import Path
bank_result=dict(source_fixture='one_axis',T=T,probe_calls=nprobe,B=bank0.tolist(),C=bank2.tolist(),scope='Exact integer sufficient coefficient bank from actual sampled product-Pauli probes along the executed retained-memory trajectory.')
Path(__file__).with_name('bank_one_axis.json').write_text(json.dumps(bank_result,indent=2)+'\n')
