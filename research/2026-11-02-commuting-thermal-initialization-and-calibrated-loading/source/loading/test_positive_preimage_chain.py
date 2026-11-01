"""Actual small RX finite positive-chain check; not asymptotic/noisy hardware proof."""
import sys,contextlib,io,json
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
base=Path(__file__).parent
sys.path.insert(0,str(base/'recursive_initialization'))
with contextlib.redirect_stdout(io.StringIO()):
 import actual_rx_polymer_bijection_test as f
states=sorted(f.accept);ix={s:i for i,s in enumerate(states)};N=len(states)
E=np.array([s.bit_count() for s in states]);beta=2.;q=1e-5
p=np.exp(-beta*E);p/=p.sum();pre=p.copy()
cols=f.f.col
perms=[np.array([ix[s^v] for s in states]) for v in cols]
for perm in reversed(perms):pre=((1-q)*pre-q*pre[perm])/(1-2*q)
assert pre.min()>0
phi=np.log(pre/p)
rows=[];columns=[];values=[];exit_rates=np.zeros(N);edges=0;balance=0.;ratioerr=0.
for family,s in f.decompositions.items():
 for gamma in family:
  parent=tuple(x for x in family if x!=gamma);sp=f.decompositions[parent]
  a=ix[sp];b=ix[s];birth=pre[b]/pre[a]
  thermal=np.exp(-beta*gamma.bit_count());derived=thermal*np.exp(phi[b]-phi[a])
  ratioerr=max(ratioerr,abs(birth-derived));balance=max(balance,abs(pre[a]*birth-pre[b]))
  # Symmetric similarity transform of negative continuous-time generator.
  rows.extend([a,b]);columns.extend([b,a]);values.extend([-np.sqrt(birth),-np.sqrt(birth)])
  exit_rates[a]+=birth;exit_rates[b]+=1;edges+=1
rows.extend(range(N));columns.extend(range(N));values.extend(exit_rates)
A=coo_matrix((values,(rows,columns)),shape=(N,N)).tocsr()
stationarity=float(np.linalg.norm(A@np.sqrt(pre)))
evals=eigsh(A,k=3,which='SM',return_eigenvectors=False,tol=1e-10);evals=sorted(float(x) for x in evals)
cur=pre.copy()
for perm in perms:cur=(1-q)*cur+q*cur[perm]
res={'scope':'actual one-square RX19 finite classical syndrome channel and exact positive trace birth/death chain, not full recursive decoder/quantum loading implementation','beta':beta,'q':q,'states':N,'birth_death_edges':edges,'min_pre':float(pre.min()),'maximum_total_exit_rate':float(max(values[-N:])),'detailed_balance_residual':balance,'soft_potential_rate_identity_error':ratioerr,'symmetric_stationarity_residual':stationarity,'numerical_smallest_eigenvalues':evals,'inverse_then_noise_L1':float(np.abs(cur-p).sum())}
assert balance<1e-14 and ratioerr<1e-12 and stationarity<1e-12 and abs(evals[0])<1e-10 and evals[1]>0
(base/'positive_preimage_chain_results.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
