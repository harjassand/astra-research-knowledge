"""Lossy complete-generator cavities and literal bath-cut compression regression."""
from pathlib import Path
base=Path(__file__).parent
src=(base.parent/'sources/check_cavity_bridge.py').read_text().split('locs=frozenset(range(4))')[0]
exec(src)
from functools import lru_cache
Id=np.eye(d*d,dtype=complex)
P1=np.diag([0.,1.]);A=np.kron(P1,I)
Loss=smap(lambda r:-.5*(A@r+r@A))
# Literal complete-loss compression of a bath-output jump; no loss is reinserted.
Jbath=np.array([[0.,0.],[1.,0.]],complex)
J=np.kron(A,Jbath);JJ=J.conj().T@J
ix=[0,2,4,6]
def compressed(r):
 full=np.zeros((8,8),complex);full[np.ix_(ix,ix)]=r
 out=J@full@J.conj().T-.5*(JJ@full+full@JJ)
 return out[np.ix_(ix,ix)]
compression_residual=float(np.linalg.norm(smap(compressed)-Loss))
assert compression_residual<1e-12

def effect(S):
 E=np.zeros((d,d),complex)
 for i,j in itertools.product(range(d),repeat=2):
  a=np.zeros((d,d),complex);a[i,j]=1
  E[j,i]=np.trace((S@a.reshape(-1)).reshape(d,d))
 return (E+E.conj().T)/2
locs=frozenset(range(4));rows=[]
for mu in [1e-5,1e-4,1e-3]:
 N1=mu*(diss(ops['Z0'])-diss(ops['X0']))
 N2=mu*(diss(ops['X0'])+diss(ops['XX']))
 N=N1+N2+mu*Loss
 eta=10*mu;x=np.sqrt(6*eta)
 gamma=.7 # potentially strong bath-only loss, not charged to processor incidence.
 Hs=[ham(.2*ops['X0']+.3*ops['Z1']),ham(.4*ops['Y0']+.2*ops['X1'])]
 Ts={}
 for R in subsets(locs):
  out=Id.copy()
  for layer in range(2):
   r={j-2*layer for j in R if 2*layer<=j<2*layer+2}
   K=Hs[layer]-gamma*Id+cavity(N,r)
   out=expm(K)@out
  Ts[R]=out
 mincp=min(float(np.linalg.eigvalsh(choi(T)).min()) for T in Ts.values())
 maxtni=max(float(np.linalg.eigvalsh(effect(T)).max()) for T in Ts.values())
 E={F:sum((-1)**len(A)*Ts[(locs-F)|A] for A in subsets(F)) for F in subsets(locs)}
 rec=float(np.linalg.norm(sum(E.values())-Ts[frozenset()]))
 maxratio=0.;cancel=0.
 for S in subsets(locs):
  if not S:continue
  inc=sum(T for F,T in E.items() if S<=F)
  fin=sum((-1)**len(R)*Ts[R] for R in subsets(S))
  cancel=max(cancel,float(np.linalg.norm(inc-fin)))
  Jc=choi(fin);ev,U=np.linalg.eigh((Jc+Jc.conj().T)/2);absJ=(U*np.abs(ev))@U.conj().T
  dual=float(np.linalg.eigvalsh(np.einsum('iaja->ij',absJ.reshape(d,d,d,d))).max())
  maxratio=max(maxratio,dual/x**len(S))
 assert mincp>-1e-10 and maxtni<=1+1e-10 and rec<1e-10 and cancel<1e-10 and maxratio<1
 rows.append({'mu':mu,'min_cavity_choi_eigenvalue':mincp,'max_cavity_effect_eigenvalue':maxtni,'reconstruction_residual':rec,'inclusive_cancellation_residual':cancel,'max_inclusive_diamond_dual_bound_ratio':maxratio})
print(json.dumps({'literal_complete_loss_compression_residual':compression_residual,'noncentered_loss_effect_norm':float(np.linalg.norm(effect(Loss),ord=2)),'strong_bath_only_loss_rate':gamma,'locations':4,'tests':rows},indent=2))
