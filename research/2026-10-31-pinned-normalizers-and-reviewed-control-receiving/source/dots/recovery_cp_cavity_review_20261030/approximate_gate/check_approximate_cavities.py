"""Repeated-site finite-gate reset/rotation regression, not an infinite-size proof."""
from pathlib import Path
from functools import lru_cache
base=Path(__file__).parent
src=(base.parent/'sources/check_cavity_bridge.py').read_text().split('locs=frozenset(range(4))')[0]
exec(src)
Id=np.eye(d*d,dtype=complex)
# A complete target reset on site0; finite reset generator is its mixture with I.
P0=np.diag([1,0]).astype(complex)
J0=np.kron(np.array([[1,0],[0,0]],complex),I)
J1=np.kron(np.array([[0,1],[0,0]],complex),I)
Reset=smap(lambda r:J0@r@J0.conj().T+J1@r@J1.conj().T)
rate=5.;tau=1.;Lreset=rate*(Reset-Id)
Lrot=ham(.23*ops['X1']);Urot=expm(ham(.24*ops['X1']))
intended=[Lreset,Lrot]
G=[expm(L) for L in intended];U=[Reset,Urot];Del=[G[i]-U[i] for i in range(2)]
# Safe complete-norm bounds: reset residual and Duhamel Hamiltonian difference.
deltas={0:2*np.exp(-rate),1:.02,2:2*np.exp(-rate),3:.02}
rows=[];locs=frozenset(range(4))
for mu in [0.,1e-5,1e-4]:
 N=mu*(diss(ops['Z0'])+diss(ops['XX']));eta=4*mu;x=np.sqrt(6*eta*tau)
 @lru_cache(None)
 def T(R,A=frozenset(),target=False):
  out=Id.copy()
  for layer in range(2):
   r={j-2*layer for j in R if 2*layer<=j<2*layer+2}
   comp=sum((intended[j] for j in range(2) if j not in r),np.zeros_like(Id))+cavity(N,r)
   C=expm(comp)
   for j in sorted(r):
    loc=2*layer+j
    C=(Del[j] if loc in A else (U[j] if target else G[j]))@C
   out=C@out
  return out
 Ts={R:T(R) for R in subsets(locs)}
 Hats={R:T(R,target=True) for R in subsets(locs)}
 max_expand=0.;max_ag1=0.;max_bound_ratio=0.;max_dual_ratio=0.;mincp=1.
 for R in subsets(locs):
  expansion=sum((-1)**len(A)*T(R,A) for A in subsets(R))
  max_expand=max(max_expand,float(np.linalg.norm(Hats[R]-expansion)))
  mincp=min(mincp,float(np.linalg.eigvalsh(choi(Hats[R])).min()))
 for S in subsets(locs):
  if not S:continue
  lhs=sum((-1)**len(R)*Hats[R] for R in subsets(S))
  rhs=sum(sum((-1)**len(B)*T(A|B,A) for B in subsets(S-A)) for A in subsets(S))
  max_ag1=max(max_ag1,float(np.linalg.norm(lhs-rhs)))
  # Nuclear Choi norm is a conservative diamond upper bound, but carries d.
  Jc=choi(lhs);upper=np.linalg.norm(Jc,ord='nuc')
  vals,vecs=np.linalg.eigh((Jc+Jc.conj().T)/2)
  absJ=(vecs*np.abs(vals))@vecs.conj().T
  partial=np.einsum('iaja->ij',absJ.reshape(d,d,d,d))
  dual=float(np.linalg.eigvalsh(partial).max())
  bound=np.prod([x+deltas[j] for j in S])
  max_bound_ratio=max(max_bound_ratio,float(upper/bound))
  max_dual_ratio=max(max_dual_ratio,dual/bound)
  assert dual<=bound+1e-10
 assert mincp>-1e-9 and max_expand<1e-10 and max_ag1<1e-10
 rows.append({'mu':mu,'modified_cavity_min_choi_eigenvalue':mincp,'isolated_slot_expansion_residual':max_expand,'AG1_residual':max_ag1,'conservative_choi_norm_bound_ratio':max_bound_ratio,'HP_dual_upper_bound_ratio':max_dual_ratio})
print(json.dumps({'locations':4,'repeated_system_sites':True,'target_reset_from_finite_dirty_reset':True,'note':'Choi nuclear ratio can exceed1; the tighter Hermitian-preserving dual certificate ||Tr_output |J||| is also checked against every claimed bound.','tests':rows},indent=2))
