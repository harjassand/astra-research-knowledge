"""Ordinary finite-MUB sampling under adaptive public-history drift; not hardware data."""
import numpy as np, json, pathlib
rng=np.random.default_rng(312028)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);kron=np.kron
pairs=[(kron(Z,I),kron(I,Z)),(kron(X,I),kron(I,X)),(kron(Y,I),kron(I,Y)),(kron(X,Z),kron(Z,Y)),(kron(X,Y),kron(Y,Z))]
bases=np.array([np.linalg.eigh(A+2*B)[1] for A,B in pairs]);projectors=np.array([[np.outer(Q[:,j],Q[:,j].conj()) for j in range(4)] for Q in bases]);snap=5*projectors-np.eye(4)
U=np.eye(4,dtype=complex)
for a,b,c,s in [(0,2,3/5,4/5),(1,3,5/13,12/13),(0,1,8/17,15/17)]:
 G=np.eye(4);G[a,a]=G[b,b]=c;G[a,b]=-s;G[b,a]=s;U=G@U
U=np.diag([1,1j,(3+4j)/5,1])@U;V=U[:,:2];F=U[:,2:]
probes=np.array([np.outer(a,np.conj(a))/2 for a in [[1,1],[1,-1],[1,1j],[1,-1j]]]);w=np.array([1,-1,1j,-1j]);svals=np.array([.6,.8]);lams=np.array([1.,0.])
probs=np.zeros((2,4,5,4))
for h in range(2):
 tau=F@np.diag([lams[h],1-lams[h]])@F.conj().T;s=svals[h]
 for q,rho in enumerate(probes):
  out=V@np.diag([1,s])@rho@np.diag([1,s])@V.conj().T+(1-s*s)*rho[1,1]*tau
  for b in range(5):
   for j in range(4):probs[h,q,b,j]=np.trace(projectors[b,j]@out).real
assert np.max(abs(probs.sum(axis=-1)-1))<1e-12
# Simulator's private environment state is never an input to the learner.
T=250000;delta=.01;target=.5;counts=np.zeros((4,5,4),dtype=int);state=0;sum_s=0.
for t in range(T):
 q=int(rng.integers(4));b=int(rng.integers(5));j=int(np.searchsorted(np.cumsum(probs[state,q,b]),rng.random()))
 counts[q,b,j]+=1;sum_s+=svals[state]
 # Adversarial source chooses the next conditional channel from public history.
 state=(state+j+(q==3))%2
Chat=sum((counts[q,b,j]*2*w[q]*snap[b,j] for q in range(4) for b in range(5) for j in range(4)),np.zeros((4,4),complex))/T
sbar=sum_s/T;Cbar=sbar*np.outer(V[:,0],V[:,1].conj());observed_error=np.linalg.norm(Chat-Cbar,2)
R=9;v=28;ell=np.log(8/delta);eta=np.sqrt(2*v*ell/T)+2*R*ell/(3*T)
a,sv,bh=np.linalg.svd(Chat);W=np.column_stack([a[:,0],bh.conj().T[:,0]]);aa,ss,bb=np.linalg.svd(W,full_matrices=False);Vhat=aa@bb
phase=np.vdot(V,W);phase/=abs(phase);isometry_error=np.linalg.norm(Vhat-V*phase,2);certificate=min(1.,8*eta/sv[0]);accept=sv[0]>4*eta and certificate<=target
assert observed_error<=eta
assert isometry_error<=4*eta/sv[0]
# Explicit two-column elimination, including phases.
Q=np.eye(4,dtype=complex);A=Vhat.copy();rotations=0
for col in range(2):
 for row in range(3,col,-1):
  x,y=A[row-1,col],A[row,col];norm=np.sqrt(abs(x)**2+abs(y)**2)
  if norm<1e-15:continue
  G=np.eye(4,dtype=complex);G[np.ix_([row-1,row],[row-1,row])]=np.array([[np.conj(x),np.conj(y)],[-y,x]])/norm
  A=G@A;Q=G@Q;rotations+=1
for col in range(2):
 phase=A[col,col]/abs(A[col,col]);G=np.eye(4,dtype=complex);G[col,col]=phase.conjugate();A=G@A;Q=G@Q
assert np.linalg.norm(Q@Vhat-np.eye(4)[:,:2])<1e-12
assert rotations<=5
out={'status':'simulation only; no hardware or advantage claim','seed':312028,'T':T,'confidence_delta':delta,'target_half_diamond':target,'accepted':bool(accept),'radius':eta,'acquired_singular_values':sv.tolist(),'certified_half_diamond_upper_bound':certificate,'diagnostic_true_sbar_not_used_by_learner':sbar,'diagnostic_actual_statistic_error':observed_error,'diagnostic_actual_isometry_error':isometry_error,'QR_two_level_rotations':rotations,'counts_q_basis_outcome':counts.tolist(),'source':'two rank-one flag states with adaptive public-history drift; fixed unknown complex V','control_scope':'ideal finite measurement model; pseudorandom simulation, not physical coin/compilation certification'}
p=pathlib.Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='counts_q_basis_outcome'},indent=2))
