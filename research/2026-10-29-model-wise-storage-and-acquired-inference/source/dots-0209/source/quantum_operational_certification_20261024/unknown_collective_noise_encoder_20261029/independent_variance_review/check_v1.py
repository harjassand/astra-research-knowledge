"""Independent covariance/leakage/completed-channel twirl diagnostics."""
from pathlib import Path
import numpy as np,json
from scipy.linalg import expm,eigh,null_space
from functools import reduce
rng=np.random.default_rng(61929026)
pa=[np.eye(2),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
kron=lambda a:reduce(np.kron,a)
def haar(d):
 a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));q,r=np.linalg.qr(a);return q
rows=[]
for n in [4,6]:
 D=1<<n;ops=[[kron([pa[a+1] if j==i else pa[0] for j in range(n)]) for i in range(n)] for a in range(3)];J=[sum(o)/2 for o in ops]
 vals,vec=eigh(sum(j@j for j in J));E0=vec[:,vals<1e-8];d0=E0.shape[1];K=1<<(d0.bit_length()-1);P=E0@E0.conj().T;Q=np.eye(D)-P
 assert K<=d0<2*K
 E=E0@haar(d0)[:,:K];Qbasis=null_space(E0.conj().T)
 for case,scale in [('tiny',.002),('moderate',.4),('large',2.)]:
  h=scale*rng.normal(size=(n,3));h/=np.maximum(1,np.linalg.norm(h,axis=1)/np.pi)[:,None];assert np.max(np.linalg.norm(h,axis=1))<=np.pi+1e-12
  H=sum(h[i,a]*ops[a][i]/2 for i in range(n) for a in range(3));W=expm(-1j*H);S=W@E
  var=np.trace(P@H@H).real/d0;formula=n/(4*(n-1))*np.sum((h-h.mean(0))**2);assert abs(var-formula)<1e-11
  leak=np.linalg.norm(Q@W@P,'fro')**2/d0;assert leak<=var+1e-11
  # Arbitrary protected-block bath unitary: stronger algebraic test than a specific collective Hamiltonian.
  U0=haar(2);UQ=haar((D-d0)*2)
  U=np.kron(E0,np.eye(2))@np.kron(np.eye(d0),U0)@np.kron(E0.conj().T,np.eye(2))+np.kron(Qbasis,np.eye(2))@UQ@np.kron(Qbasis.conj().T,np.eye(2))
  bvec=haar(2);bweights=[.31,.69];A=[];Fproject=0.;T=null_space(S.conj().T)
  for weight,v in zip(bweights,bvec.T):
   inp=np.kron(S,v[:,None]);out=(U@inp).reshape(D,2,K)
   for b in range(2):
    g=np.sqrt(weight)*S.conj().T@out[:,b,:];A.append(g);Fproject+=abs(np.trace(g))**2/K**2
    leakrows=np.sqrt(weight)*T.conj().T@out[:,b,:]
    for row in leakrows:
     bad=np.zeros((K,K),complex);bad[0,:]=row;A.append(bad)
  assert np.linalg.norm(sum(a.conj().T@a for a in A)-np.eye(K))<1e-11
  F=sum(abs(np.trace(a))**2 for a in A)/K**2;bound=4*np.linalg.norm(Q@S,'fro')**2/K
  assert 1-Fproject<=bound+1e-11 and F>=Fproject-1e-12 and bound<=4*d0/K*var+1e-11
  paul=pa if K==2 else [np.kron(a,b) for a in pa for b in pa]
  # Explicit physical pre/post Pauli average on the completed logical CPTP channel.
  choi=sum(np.outer(a.reshape(-1),a.reshape(-1).conj()) for a in A)/K
  tw=np.zeros_like(choi)
  for pp in paul:
   for a in A:
    aa=pp.conj().T@a@pp;v=aa.reshape(-1);tw+=np.outer(v,v.conj())/(K*len(paul))
  bell=np.column_stack([pp.reshape(-1)/np.sqrt(K) for pp in paul]);diag=bell.conj().T@tw@bell;off=np.linalg.norm(diag-np.diag(np.diag(diag)));assert off<1e-11
  phi=np.eye(K).reshape(-1)/np.sqrt(K);Ftw=float(np.vdot(phi,tw@phi).real);assert abs(Ftw-F)<1e-11
  halftrace=np.sum(abs(np.linalg.eigvalsh(tw-np.outer(phi,phi.conj()))))/2;assert abs(halftrace-(1-F))<1e-11
  rows.append({'n':n,'singlet_dimension':d0,'logical_dimension':K,'case':case,'variance_identity_error':float(abs(var-formula)),'projected_Bell_loss':float(1-Fproject),'completed_Bell_loss':float(1-F),'four_mean_leakage_bound':float(bound),'variance_bound':float(4*d0/K*var),'twirled_Bell_offdiagonal_norm':float(off),'twirled_half_Choi_trace_distance':float(halftrace)})
 # Identical logarithms implement a collective rotation and annihilate singlet H.
 h=np.tile([.3,-.4,.2],(n,1));H=sum(h[i,a]*ops[a][i]/2 for i in range(n) for a in range(3));assert np.linalg.norm(H@P)<1e-11
out={'seed':61929026,'cases':rows,'all_passed':True,'scope':'Numerical algebra and completed logical CPTP twirl checks; not a physical deployment or numerical diamond SDP. Arbitrary protected-block bath tests the algebraic inequality beyond the author fixture.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'cases':len(rows),'all_passed':True}))
