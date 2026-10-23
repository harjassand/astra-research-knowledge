"""Actual five-qubit arbitrary-support-phase GHZ eigenbasis, all erasures."""
import itertools,json,math,time,platform,resource
from pathlib import Path
import numpy as np
start=time.perf_counter();cpu=time.process_time();n=5;D=2;q=D**n
bits=list(itertools.product((0,1),repeat=n));idx={x:i for i,x in enumerate(bits)}
labels=list(itertools.product((0,1),repeat=n));rng=np.random.default_rng(411)
theta={a:float(rng.uniform(-np.pi,np.pi)) for a in itertools.product((0,1),repeat=n-1)};theta[(0,)*(n-1)]=np.pi/4
U=np.zeros((q,q),complex)
y=[]
for j,L in enumerate(labels):
 a,c=L[:-1],L[-1];x=(0,)+a;xx=tuple(1-z for z in x)
 U[idx[x],j]=1/math.sqrt(2);U[idx[xx],j]=(-1)**c*np.exp(1j*theta[a])/math.sqrt(2)
 y.append((c,)+tuple(c^z for z in a))
subsets=[s for k in range(n+1) for s in itertools.combinations(range(n),k)]
def erasure(X,S):
 keep=tuple(i for i in range(n) if i not in S);out=np.zeros_like(X)
 for u in bits:
  for v in bits:
   if any(u[i]!=v[i] for i in S):continue
   total=0j
   for g in itertools.product((0,1),repeat=len(S)):
    xx=list(u);zz=list(v)
    for i,b in zip(S,g):xx[i]=zz[i]=b
    total+=X[idx[tuple(xx)],idx[tuple(zz)]]
   out[idx[u],idx[v]]=total/(2**len(S))
 return out
orth=float(np.max(np.abs(U.conj().T@U-np.eye(q))));residual=0.;cell_sizes={}
for S in subsets:
 keep=tuple(i for i in range(n) if i not in S)
 def key(L):
  a,c=L[:-1],L[-1];aa=(0,)+a
  if not S:return ('point',L)
  return tuple(sorted(tuple(g^aa[i] for i in keep) for g in (0,1)))
 cells={}
 for j,L in enumerate(labels):cells.setdefault(key(L),[]).append(j)
 for j in (0,7,q-1):
  cell=cells[key(labels[j])]
  pred=U[:,cell]@U[:,cell].conj().T/len(cell)
  act=erasure(np.outer(U[:,j],U[:,j].conj()),S)
  residual=max(residual,float(np.max(np.abs(act-pred))))
 fibers={}
 for j in range(q):
  fkey=tuple(y[j][i] for i in keep);ckey=key(labels[j])
  assert fkey not in fibers or fibers[fkey]==ckey
  fibers[fkey]=ckey
 cell_sizes[str(S)]=sorted(set(map(len,cells.values())))
assert orth<1e-12 and residual<1e-12
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
out={'dimension':q,'physical_qubits':n,'all_erasure_subsets':len(subsets),'sample_projectors_per_subset':3,'support_phase':'arbitrary support-dependent random phases, one exactly pi/4','basis_orthogonality_max_error':orth,'max_quantum_erasure_vs_cell_residual':residual,'coordinate_fiber_containment':'EXACT all labels/all subsets','wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':rss if platform.system()=='Darwin' else rss*1024,'scope':'finite algebra check, no optimization/no circuit lower bound'}
Path(__file__).with_name('QUBIT_PHASE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
